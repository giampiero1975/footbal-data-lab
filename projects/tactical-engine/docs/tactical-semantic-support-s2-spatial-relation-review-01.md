# RD-TSC-V2-D3-S2-SPATIAL-RELATION-REVIEW-01

## Attivita e perimetro

Revisione tecnica indipendente, esclusivamente statica, del contratto opt-in
`nli_spatial_relations_v1` introdotto dal commit
`2934d234868a1f4c6e05e9571a76d7a642eb3b86` e tracciato dal commit
`0bfa3de4fec7a1f4b787d99ab76bbbe7aea75430`. Sono stati letti integralmente
modulo, sei test, contratto NLI V2 storico, bridge S2, runner della Fase B e
report forense `q3_04`. Non sono stati eseguiti test, modelli o chiamate di rete.
Non risultava una revisione equivalente gia conclusa.

## Riconciliazione

- Branch e HEAD iniziale: `codex/tactical-state-contract-v1` a
  `0bfa3de4fec7a1f4b787d99ab76bbbe7aea75430`, coincidente con GitHub.
- Working tree iniziale: pulito.
- File revisionati:
  `scripts/shadow_nli_spatial_relations_v1_inference.py` e
  `tests/test_shadow_nli_spatial_relations_v1_inference.py`.
- Confronti: `scripts/shadow_nli_v2_inference.py`,
  `scripts/benchmark_direct_three_label_nli_v2.py`,
  `scripts/v5_tactical_semantic_support_s2_nli_v2_bridge.py` e
  `scripts/run_tactical_semantic_support_s2_first_controlled_runtime_v1.py`.

## Revisione semantica

L'istruzione richiede esplicitamente il confronto separato di soggetto,
proprieta/spazio, riferimento spaziale, direzione, condizioni, contesto e fase o
tempo (`shadow_nli_spatial_relations_v1_inference.py`, righe 20-29). Predicati
incompatibili sono `contradicted` solo a parita di soggetto, referente e
condizioni; elementi non determinabili o fonte silente restano `insufficient`.
La sovrapposizione lessicale non prova il supporto. Negazioni, quantificatori,
obiettivi, possibilita e garanzie conservano la distinzione prudente del V2.
Le label restano esattamente `supported`, `contradicted`, `insufficient`.

Queste regole riducono il falso `supported` su relazioni inverse senza
trasformare automaticamente l'assenza di prova in contraddizione. Restano rischi
teorici dipendenti dall'interpretazione del modello: identita apparente ma non
reale di soggetto/referente, condizioni implicite, fasi temporali differenti e
predicati graduati. La sola lettura statica non dimostra che Qwen applichi
correttamente tali distinzioni; non e stato individuato un difetto deterministico
nel testo che imponga una classificazione permissiva.

## Caso `q3_04` e contaminazione

La coppia letterale `lasciare molto spazio` / `togliere spazio` deriva
chiaramente dal caso osservato. E una esplicitazione coerente della regola
generale e non contiene ID, label attesa o routing specifico; quindi non e un
hard-code del verdetto. E tuttavia anche un adattamento al caso noto e crea un
rischio di contaminazione probatoria: un futuro successo su `q3_04` misurerebbe
una regressione guidata, non generalizzazione indipendente.

Classificazione: **A** per la validita contrattuale, con componente **B/C**
limitata alla futura interpretazione sperimentale. Non e necessario rimuovere
l'esempio prima di una prova di regressione dichiarata. Per una futura misura di
generalizzazione indipendente sono necessari casi disgiunti che non riusino la
stessa coppia lessicale; sostituire ora l'esempio non eliminerebbe retroattivamente
l'esposizione gia avvenuta.

## Revisione tecnica e fail-closed

- Import: nessuna chiamata di rete o esecuzione; schema e parser V2 sono importati
  lazily soltanto dentro `judge_pair()` (righe 55-63).
- Selezione: nessun riferimento al nuovo ID nel bridge, nel runner o nel V2;
  occorre import esplicito del nuovo callable.
- Prompt: ordine corretto `FONTE` poi `AFFERMAZIONE`; claim ed evidence devono
  essere stringhe non vuote (righe 47-52).
- Trasporto: stessi endpoint, modello di default, structured schema, temperatura,
  contesto, token, `think=false` e `stream=false` del V2 (righe 55-79).
- Parsing: output accettato soltanto con `done_reason=stop`, contenuto non vuoto e
  label validabile dal `Verdict` V2 (righe 80-84).
- Errori HTTP, timeout, JSON malformato, risposta di forma inattesa e validazione
  Pydantic non sono convertiti in label positive: propagano eccezioni. Nel
  confine S2 esistente ogni eccezione del judge produce `not_evaluable` e
  `promotion_authorized` resta sempre `false`
  (`v5_tactical_semantic_support_s2.py`, righe 149-176 e 45-74).
- Nessun retry, repair, fallback positivo o side effect applicativo e presente.

Il modulo conserva quindi il fail-closed nel percorso per cui e progettato. Come
nel V2 storico, il callable grezzo propaga le eccezioni invece di produrre da
solo un record S2: e una separazione di responsabilita, non un fallback.

## Valutazione dei sei test pubblicati

| Test | Proprieta verificata | Non verificato / limite |
|---|---|---|
| 01 | ID, versione, label e selezione esplicita | Nessuna prova semantica del modello |
| 02 | Presenza testuale di soggetto, referente, direzione, condizioni e fase | Non prova che Qwen applichi le istruzioni |
| 03 | Presenza delle regole che separano insufficienza, contraddizione e overlap | Non misura falsi positivi/negativi reali |
| 04 | Claim/evidence `q3_04` entrano senza ID o label attesa | Il caso resta esposto lessicalmente nell'istruzione e non e indipendente |
| 05 | Fingerprint istruzione V2 e assenza del nuovo ID nei tre percorsi default | Non e una prova runtime; il diff statico conferma comunque l'isolamento |
| 06 | Payload strutturato, parsing di un successo mock e rifiuto del troncamento | Non copre singolarmente HTTP, timeout, JSON malformato e schema invalido; tali percorsi propagano eccezioni dal codice |

I test dimostrano contratto, isolamento e orchestrazione mock, non accuratezza
semantica. Non producono un falso segnale sufficiente a cambiare la decisione,
poiche il report originale limita gia esplicitamente la validazione all'offline.

## Isolamento e compatibilita

Il diff dalla baseline `1597ae68...` aggiunge soltanto modulo, test e
documentazione della remediation. Il contratto V2 storico, il bridge S2, il
runner Fase B, S1, RAG, Chroma, API e panel sono invariati. Il runner continua a
importare esplicitamente `shadow_nli_v2_inference`; il nuovo contratto non viene
selezionato automaticamente. La policy S2 resta shadow-only e
`promotion_authorized=false`.

## Rilievi

Nessun rilievo bloccante o maggiore.

Rilievo minore/probatorio: l'esempio `lasciare molto spazio` / `togliere spazio`
e vicino al caso `q3_04`. Conseguenza: `q3_04` non puo essere usato come prova
indipendente di generalizzazione. Correzione minima non applicativa: classificare
quel caso esclusivamente come regressione nota e usare in futuro casi disgiunti
per qualsiasi valutazione di generalizzazione. Non e richiesta una modifica al
contratto per candidarlo a una prova runtime separatamente autorizzata.

## Risultato, decisione e stato

**REVISIONE FAVOREVOLE.**

Il contratto e tecnicamente coerente e puo essere candidato a una futura prova
runtime separatamente autorizzata. La revisione non dimostra efficacia semantica,
accuratezza generale o assenza di regressioni e non autorizza integrazione.

- Revisione statica: **ESEGUITO**.
- Coerenza tecnica, isolamento e fail-closed nel perimetro statico: **VALIDATO**.
- Contratto: **IMPLEMENTATO**.
- Efficacia semantica, Gate, integrazione e certificazione: **BLOCCATO**.

Unico prossimo passo tecnicamente motivato: sottoporre al titolare una richiesta
separata per una prova runtime controllata e non promuovibile, con `q3_04`
qualificato come regressione nota e con casi disgiunti necessari per qualsiasi
conclusione di generalizzazione. Nessun runtime e autorizzato da questo report.
