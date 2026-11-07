# RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-WITNESS-ROOT-CAUSE-01

## Baseline e fonti

Revisione statica del witness prodotto dall'unico runtime `q3_04` a 360 s.

- HEAD iniziale: `4c72ec1442279bdac62520c1a5535073b671c2f0`;
- codice effettivamente eseguito: `69ec127cddbba114d8c37f3eefde5dba9200520c`;
- inventario runtime: 22/22 file conformi; SHA-256 di `hashes.sha256`
  `4c98996be698a45c400360643fc575b5e970d04822ec74a24f029a313570bace`.

Fonti esaminate: `case.json`, `prompt.txt`, `payload.json`,
`raw_response.json`, `result.json`, `config.json`, `manifest.json`; schema e
validatore `v5_tactical_semantic_support_s2_spatial_v2.py`; judge
`shadow_nli_spatial_relations_v2_inference.py`; specifica, implementazione,
remediation R1/R2, test Spatial V2, TODO ed experiment register. Nessun runtime,
rete, SSH o modifica degli artefatti.

## Percorso verificato

Il testo canonico è inserito da `build_prompt()` senza normalizzazioni o
trasformazioni. Qwen riceve prompt, schema `SPATIAL_V2_SCHEMA`, `claim` ed
`evidence`, restituisce JSON completo, quindi `judge_pair()` esegue
`json.loads()` e passa witness e testi originali a `validate_spatial_v2()`.
Il validatore confronta ogni ancora con `source_text[start:end]` e verifica le
regole status/value/anchor. Non corregge l'output.

## Inventario degli anchor invalidi

Convenzione normativa: offset zero-based in Unicode code point, intervallo
semiaperto `[start,end)`, sul testo originale NFC; deve valere esattamente
`source_text[start:end] == exact_span`.

| Campo | `exact_span` | Dichiarato | Sottostringa dichiarata | Offset corretto |
|---|---|---:|---|---:|
| claim subject | `La difesa bassa` | `[0,12)` | `La difesa ba` | `[0,15)` |
| claim semantic_axis | `lascia molto spazio` | `[13,20)` | `sa lasc` | `[16,35)` |
| claim reference | `tra la linea difensiva e la porta` | `[21,46)` | `a molto spazio tra la lin` | `[36,69)` |
| claim value | `lascia molto spazio` | `[13,20)` | `sa lasc` | `[16,35)` |
| claim condition 1 | `La difesa bassa` | `[0,12)` | `La difesa ba` | `[0,15)` |
| claim condition 2 | `tra la linea difensiva e la porta` | `[21,46)` | `a molto spazio tra la lin` | `[36,69)` |
| claim phase | claim completo | `[0,46)` | prefisso troncato | `[0,70)` |
| claim polarity | `lascia molto spazio` | `[13,20)` | `sa lasc` | `[16,35)` |
| evidence subject | `difendono basse` | `[208,223)` | `zio tra la line` | `[136,151)` |
| evidence semantic_axis | `togliendo però spazio` | `[240,263)` | `la porta.` | `[190,211)` |
| evidence reference | `tra la linea difensiva e la porta` | `[264,293)` | fuori testo | `[212,245)` |
| evidence value | `togliendo però spazio` | `[240,263)` | `la porta.` | `[190,211)` |
| evidence condition 1 | `difendono basse` | `[208,223)` | `zio tra la line` | `[136,151)` |
| evidence condition 2 | `tra la linea difensiva e la porta` | `[264,293)` | fuori testo | `[212,245)` |
| evidence phase | frase da `che difendono...` | `[208,319)` | coda diversa/fuori testo | `[132,246)` |
| evidence polarity | `togliendo però spazio` | `[240,263)` | `la porta.` | `[190,211)` |

Tutti i 16 `exact_span` sono presenti nel rispettivo testo originale. Gli
offset dichiarati non coincidono né con i testi sorgente né con le posizioni
degli span nel prompt completo; gli scarti non sono costanti. Claim, evidence e
span sono NFC e la punteggiatura è invariata. Non emerge una convenzione
one-based, byte-based, token-based o inclusiva coerente. La causa immediata di
`E_ANCHOR_INVALID` è quindi la generazione di offset numericamente errati.

## Status/value del quantificatore

Entrambe le relazioni dichiarano:

```json
{"status":"explicit","value":"absent","literal":"","anchors":[]}
```

La matrice normativa consente:

- `explicit` con un valore non sentinella e diverso da `none`, 1–2 anchor;
- `implicit/none/literal=null/[]` quando non è osservato un quantificatore
  grammaticale;
- `absent/absent/literal=null/[]` come sentinella distinta;
- `ambiguous/ambiguous` con anchor oppure `unknown/unknown/[]`.

`explicit/absent/[]` è quindi invalido; anche `literal=""` non è il `null`
previsto per la sentinella. Il validatore applica coerentemente la specifica e
produce `E_STATUS_VALUE_INCONSISTENT`. Il modello ha mescolato dichiarazione
esplicita e assenza dell'informazione.

## Prompt, schema e validatore

Classificazione causale:

| Area | Categoria | Evidenza |
|---|---|---|
| Offset prodotti | **A — generazione del modello** | numeri errati e incoerenti, nonostante span esatti copiati correttamente |
| Istruzione runtime | **B — specifica insufficiente nell'handoff** | il prompt dice solo di ancorare al testo; non definisce code point, zero-based, `[start,end)` o uguaglianza della slice |
| Schema inviato | **B/C — informazione insufficiente/disallineamento** | tipizza start/end/span ma non può imporre la corrispondenza col testo; non codifica tutte le combinazioni status/value/anchor applicate dal validatore |
| Specifica completa | nessun difetto dimostrato | definisce offset e matrice in modo esplicito |
| Validatore | nessun errore dimostrato | applica esattamente slice, NFC e matrice normativa; i test offline coprono già tali invarianti |
| Trasformazioni testo | escluse | caso, prompt, payload e validazione conservano gli stessi testi |

Il witness può rispettare la shape JSON e tuttavia violare il contratto
deterministico più forte. Questa differenza era progettata fail-closed, ma le
regole complete non sono state consegnate al modello nel prompt effettivo.

## Non duplicazione

L'implementazione `128f014` e la remediation `3c935b0` hanno già verificato
offset/NFC, status/sentinelle, confronto e gestione fail-closed con test mock.
Non hanno verificato che il prompt runtime comunichi al modello le stesse regole
normative. La presente attività analizza per la prima volta un witness completo
reale rispetto a tale handoff; non ripete i test del validatore e non riapre il
timeout.

## Unica correzione prioritaria proposta

**Completare il solo handoff normativo in `INSTRUCTION`/`build_prompt()` di
`shadow_nli_spatial_relations_v2_inference.py`.** Il prompt deve dichiarare in
modo compatto e non ambiguo:

1. offset Unicode code-point zero-based e intervallo semiaperto `[start,end)`;
2. uguaglianza case-sensitive `source_text[start:end] == exact_span`;
3. nessun quantificatore osservato → `implicit/none/literal=null/anchors=[]`;
4. `explicit` richiede valore non sentinella e anchor testuale;
5. nessuna correzione, repair o approssimazione degli offset.

Non si propone di modificare o indebolire schema/validatore, derivare offset
automaticamente o correggere silenziosamente il witness. Il limite residuo è
che un prompt più esplicito non garantisce la conformità del modello: una futura
prova runtime richiederebbe autorizzazione separata.

### Verifica offline differenziale proposta

Un solo test nuovo deve intercettare il payload tramite trasporto mock e
verificare che il prompt contenga le cinque regole, che claim/evidence siano
byte-invariati, che modello/schema/2.048 token e singola chiamata restino
invariati e che un witness mock con gli stessi errori continui a essere
`not_evaluable`. Criterio di accettazione: handoff normativo completo nel
payload, nessun cambiamento del validatore e nessuna promozione dell'output
invalido. Il test dimostra il contratto trasmesso, non l'accuratezza Qwen.

## Decisione e stati

Flusso: Attività = root cause witness; Script = nessuno eseguito; Commit =
documentale; Report = questo documento; Risultato = cause attribuite; Decisione
= sottoporre la singola correzione del prompt ad autorizzazione.

| Componente | Stato |
|---|---|
| Analisi causale statica | **ESEGUITO** |
| Cause anchor/status e gap di handoff | **VALIDATO** |
| Correzione prompt proposta | **DA FARE** |
| Runtime storico 360 | invariato: **ESEGUITO** |
| Semantica, promozione, Gate, integrazione e certificazione | **BLOCCATO** |
