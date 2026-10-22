# RAG V5 — Revisione atomica dei passaggi, 22 ottobre 2026

## Metodo e limiti
Confronto manuale delle singole affermazioni di `holdout_06` e `holdout_10` con gli **estratti effettivamente forniti** nel JSON `rag_v5_phase_passage_shadow_v1.json` (SHA256 `2d56c6058459542d5f920c1b93611d677f4f4d2a41ffcfa770f266b1c041ae57`). Non sono stati consultati qui i documenti integrali né la VPS. Questa revisione **non è gold indipendente**: i casi sono già stati usati per il debug; non è un punteggio sul target 9/10.

## holdout_06 — sette claim esaminati
| Claim | Fonti | Verdetto |
|---|---|---|
| Zone alta/media/bassa usate per misurare la qualità della transizione, non come tabella prescrittiva | F1 | Supportato |
| Zona e contesto del recupero vanno analizzati | F3 | Supportato |
| Sfruttare squilibrio o stabilizzare il possesso dopo il recupero | F1, F4 | Supportato |
| Primo passaggio condizionato da avversari e distanze | F1 | Supportato nel contesto degli esempi |
| Gli estratti non definiscono una regola distinta per ogni zona | F1,F3,F4,F8 | Supportato **solo per questi estratti**, non per l'intero corpus |
| Le decisioni sono «indipendenti dalla zona geografica» | F1,F3 | **Non supportato**: F3 impone di considerare il punto di recupero |
| Superiorità numerica e sistema come criteri decisivi | F1,F3 | Parzialmente supportato; evitare nessi non esplicitati |

**Decisione 06: REVIEW, non PASS.** Miglioramento rispetto alla risposta precedente, ma rimane un'inferenza eccessiva («indipendentemente dalla zona»).

## holdout_10 — undici claim esaminati
| Claim | Fonti | Verdetto |
|---|---|---|
| Transizione dalla riconquista alla ricostruzione di un'organizzazione riconoscibile, non durata fissa | F3,F6 | Supportato |
| Sfruttare squilibrio o stabilizzare | F4,F6 | Supportato |
| Prima giocata verticale/diagonale/di consolidamento secondo contesto | F4 | Supportato |
| Verticalità se portatore ha tempo e copertura non compromessa | F2 | Supportato |
| Primo passaggio sicuro o recupero basso/medio = possesso già consolidato | F4,F6 | **Non giustificato e in tensione con F6** |
| Zona alta più efficace per progressioni controllate | F1,F4 | **Non supportato**: F1 parla dell'efficacia della *riconquista* alta nell'esercitazione |
| Recupero basso richiede più tempo | F1,F4 | **Non supportato** |
| Progressione didattica 10 contro 0 determina la prima giocata in partita | F1,F7 | **Non supportato**: è una sequenza d'allenamento |
| Pressing inefficace/disorganizzato implica consolidamento | F7 | **Non supportato**: la fonte tratta pressing alto organizzato |
| F8 prescrive di «congelare» la situazione sotto pressione | F8 | **Non supportato** |
| Confine della fase quando una squadra ricostruisce organizzazione riconoscibile | F6 | Supportato con precisazione del soggetto («una delle squadre») |

**Decisione 10: FAIL nel controllo semantico mirato.** Le citazioni sono formalmente valide ma non giustificano diversi nessi causali.

## Decisione operativa
1. **Non promuovere V5** e non trasformare questo holdout già esaminato in gold indipendente.
2. Congelare report e hash; V4, Chroma e prompt canonico invariati.
3. Formalizzare criteri generali di grounding per fase, zona, causalità, quantificatori e fonte didattica vs partita.
4. Preparare un nuovo set prospettico di domande, non riutilizzare 06/10 per dichiarare miglioramenti.
5. Prima di ogni modifica implementativa consultare la documentazione ufficiale dei componenti interessati; il presente audit è una lettura semantica offline, non richiede API.

## Riferimenti interni
- `docs/rag-v5-quality-holdout-adjudication-rubric-20261022.md`
- `docs/rag-v5-quality-9of10-validation-protocol-v1.md`
- `docs/rag-v5-phase-passage-shadow-v1-review-20261022.md`
