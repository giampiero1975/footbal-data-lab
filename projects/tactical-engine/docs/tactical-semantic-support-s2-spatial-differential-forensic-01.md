# RD-TSC-V2-D3-S2-SPATIAL-DIFFERENTIAL-FORENSIC-01

## Attivita e baseline

Revisione forense indipendente, esclusivamente offline, del Gate differenziale
`nli_spatial_relations_v1` concluso 2/3. Baseline GitHub:
`4a4f84f8c4930503b8db5c3e0cf07beb119e8db0`. Sono stati letti integralmente
artefatto, fixture, Gold, runner, contratto spatial, judge V2, bridge S2, adapter
S2 e report precedenti. Nessun test runtime, modello, rete o modifica applicativa
e stato eseguito.

## Integrita dell'artefatto

Artefatto:
`evaluation/tactical_semantic_support_s2_spatial_relation_differential_01.json`.

- Byte: 13.138.
- SHA-256: `a06ba357471681f2ac047af9cff8293d23e75f1c8c8e364f1b14fc4990f8c42d`.
- Schema: `tactical_semantic_support_s2_spatial_relation_differential_report_v1`.
- Fixture blob: 1.764 byte, SHA-256
  `45c26718605d5edf1bbe9463bd516b85050b352b712653d112f39d1397f3d1d7`.
- Gold blob: 7.612 byte, SHA-256
  `8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c`.
- Contratto: `nli_spatial_relations_v1` 1.0, instruction SHA-256
  `861dbec3daac9ac34169356ad51a453f6267175afaa5d296f84c92586d2f3a00`.
- Plan fingerprint ricalcolato e conforme:
  `sha256:846044fb3bc0d4e9224b085cf8ac1c140421b11f60135681309d26c596cb6b84`.
- I tre `record_sha256` ricalcolati sul JSON canonico sono conformi.
- Summary ricalcolato: technical pass 3, semantic match 2.
- `planned/attempted/completed=3/3/3`, `run_complete=true`, S1 invariato 3/3,
  `promotion_authorized=false` e `authoritative_outputs_modified=false`.

Classificazione: **A — dimostrato**.

## Catena applicativa `q3_04`

1. Il Gold e la fixture selezionano senza modifica `q3_04`, Gold
   `contradicted`, fonte `verticalizzazione_Bonacini`, pagina 2.
2. `load_inputs()` verifica digest, ID, label e contenuti; non normalizza claim o
   evidenza.
3. `_claim()` conserva lo statement e aggiunge soltanto metadati deterministici:
   `conditions=[]`, `polarity=affirmed`, `bindings={}` e riferimenti locali.
4. S1 restituisce `not_evaluable` per `statement_not_exact_anchor`; il record
   resta invariato e non decide S2.
5. L'adapter S2 costruisce il payload del judge con claim ed evidenza esatte.
6. `project_claim()` del bridge produce:

```text
S2_CLAIM_V1
claim_id=claim:q3_04
statement=La difesa bassa lascia molto spazio tra la linea difensiva e la porta.
conditions_json=[]
polarity=affirmed
bindings_json={}
```

7. Il callable iniettato e
   `shadow_nli_spatial_relations_v1_inference.judge_pair`; `build_prompt()`
   concatena istruzione spatial, `FONTE`, evidenza, `AFFERMAZIONE` e proiezione,
   senza troncamenti o normalizzazioni.
8. Il payload previsto usa `qwen3.5:9b`, temperature 0, `num_ctx=4096`,
   `num_predict=1024`, `think=false`, `stream=false` e schema a tre label.
9. Il judge accetta soltanto `done_reason=stop`, contenuto non vuoto e JSON
   validabile; restituisce la label al bridge.
10. Bridge e S2 non rimappano `supported`; la label entra invariata nel record e
    nel JSON finale.

Non emerge perdita, inversione, troncamento, fallback o sostituzione della coppia
claim/evidence. Classificazione: **A — dimostrato** per la catena deterministica.

## Prompt ricostruito

Il prompt e stato ricostruito dai blob e dalle funzioni congelate, senza importare
o interrogare Ollama:

- caratteri: 2.377;
- byte UTF-8: 2.386;
- SHA-256:
  `597088f1d9e9304fd0a5dcda8219a176a292a16db3480602f49d67d286e9b264`.

Il digest riguarda il prompt deterministicamente ricostruito. Non esiste una
cattura della richiesta HTTP originale: l'identita byte-per-byte del payload
trasmesso non e direttamente verificabile. La corrispondenza con il percorso
codice/configurazione e **B — fortemente supportata**.

## Analisi semantica `q3_04`

Soggetto: la squadra/difesa bassa. Referente: spazio tra linea difensiva e porta.
Proprieta: disponibilita/quantita di quello spazio. Condizioni e fase: squadra
che difende bassa mentre l'avversario cerca profondita. La fonte dice che lascia
avanzare gli avversari ma **toglie spazio** tra linea e porta; la claim dice che
**lascia molto spazio** nello stesso referente. Il movimento concesso davanti
alla linea non equivale allo spazio dietro/tra linea e porta.

La Gold `contradicted` resta coerente. Il risultato `supported` e semanticamente
errato. Poiche input, routing, parsing e propagazione sono coerenti, l'errore si
manifesta nel verdetto semantico restituito sotto il contratto spatial:
**B — fortemente supportato**. Il ragionamento interno non e registrato; overlap
lessicale, confusione con `lasciano avanzare` o mancata osservanza dell'istruzione
sono soltanto **C — ipotesi**. Non e dimostrato che il testo dell'istruzione sia
la causa sufficiente del fallimento.

## Routing e provenance del bridge

Il runner importa esplicitamente `shadow_nli_spatial_relations_v1_inference`,
crea una closure che chiama il suo `judge_pair()` e passa quella closure a
`build_bridge()`. `runtime_config.judge`, descriptor del contratto e instruction
digest identificano correttamente spatial V1. Nessun percorso chiama il judge V2.
Routing spatial: **A — dimostrato** dal codice, configurazione e staging
riconciliati.

Il bridge e pero storicamente specifico V2:

- `descriptor()` assegna sempre `name=shadow-nli-v2-s2-bridge`;
- `config.nli_contract` e hard-coded a
  `shadow_nli_v2_inference.judge_pair(claim,evidence)`;
- `_normalise_result()` trasforma ogni label stringa nella rationale fissa
  `NLI V2 returned the recorded label...`.

Quella rationale non proviene dal modello e non spiega il verdetto. Il record S2
content-addressa coerentemente questi valori tramite `record_sha256`, ma il digest
prova integrita, non veridicita semantica della provenance.

Conclusione: non e un difetto di routing, ma un **difetto effettivo di provenance
strutturata** (**A — dimostrato**), non una mera etichetta cosmetica. Identita del
callable e contratto sono corrette al livello del report; identita adattatore,
`nli_contract` annidato e origine dichiarata della rationale sono fuorvianti e non
sono affidabili come evidenza autonoma.

## Limiti di osservabilita

Non sono conservati:

- richiesta HTTP originale o relativo digest;
- risposta Ollama originale/envelope;
- JSON grezzo restituito dal modello;
- rationale semantica o token di reasoning (`think=false`);
- durata individuale delle tre chiamate;
- contatori server-side;
- versione Ollama nel JSON;
- digest effettivo dei pesi caricati (e registrato solo il tag modello).

Sono conservati label, configurazione client, digest di input/contratto, identita
staging, record S2 e durata complessiva esterna. Questi dati bastano a verificare
integrita e routing applicativo, non il meccanismo cognitivo del falso positivo.

## Confronto V2 storico

Per `q3_04`, claim ed evidenza sono identiche nei due artefatti. Modello,
temperature 0, contesto 4096, limite 1024, `think=false`, `stream=false` e timeout
180 coincidono. Cambia il contratto/import del judge; il bridge tecnico resta lo
stesso. V2 storico: `supported`; spatial V1: `supported`. La remediation non ha
corretto la regressione nota. Questa e una constatazione sul singolo caso, non una
misura di accuratezza generale.

## Controlli concorrenti

`q5_06=contradicted` e coerente col Gold ed e un controllo distinto ma correlato,
non indipendente. `q5_02=insufficient` e coerente col Gold e non mostra una falsa
contraddizione in quel caso. Nessuno dei due compensa il fallimento principale o
dimostra accuratezza generale.

## Matrice delle conclusioni

| Conclusione | Livello |
|---|---|
| Integrita JSON, digest, fingerprint, record e summary | A |
| Claim/evidenza e costruzione deterministica corrette | A |
| Routing al callable spatial, nessuna chiamata V2 | A |
| Parsing e propagazione non rimappano la label | A |
| Provenance annidata V2 e rationale fissa sono inesatte | A |
| Falso positivo localizzato nel giudizio semantico restituito | B |
| Payload HTTP effettivo uguale a quello ricostruito | B |
| Modello confuso da overlap o da `lasciano avanzare` | C |
| Istruzione spatial intrinsecamente insufficiente | C |

## Decisione tecnica e stato

- Gate runtime tecnicamente valido: si, **VALIDATO** nel singolo run.
- Verdetto attribuibile al percorso spatial: si, **A** nel percorso applicativo;
  payload HTTP originale non catturato.
- Errore deterministico input/bridge/parsing: non rilevato.
- Provenance annidata affidabile autonomamente: no, **BLOCCATO** dal difetto
  strutturato dimostrato.
- Spiegazione interna del falso positivo: non determinabile.
- Remediation tecnica: giustificata esclusivamente per la provenance del bridge;
  non e giustificata una nuova rettifica semantica senza evidenza differenziale.

Stati:

- Revisione forense: **ESEGUITO**.
- Integrita, routing e ricostruzione deterministica: **VALIDATO** offline.
- Gate tecnico del singolo run: **VALIDATO**.
- Corrispondenza semantica complessiva, affidabilita generale, integrazione e
  certificazione: **BLOCCATO**.

Unico prossimo passo ad alto valore: progettare e revisionare offline una
rettifica minima del descriptor/rationale del bridge affinche identita del
callable, contratto e assenza di rationale semantica siano registrate
correttamente, senza cambiare verdict, prompt o routing e senza eseguire un nuovo
Gate. Ogni ulteriore indagine semantica richiedera poi una differenza tecnica e
una distinta decisione del titolare.
