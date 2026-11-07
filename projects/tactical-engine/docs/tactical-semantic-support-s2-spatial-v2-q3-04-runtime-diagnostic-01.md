# RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-RUNTIME-DIAGNOSTIC-01

## Riconciliazione

Preflight sulla baseline documentale
`009f76e71c0351da9d2b797ad3c9ff1928671a4e`, branch
`codex/tactical-state-contract-v1`. HEAD locale/remoto conformi e working tree
pulito prima dell'attività. TODO, experiment register, closeout R1/R2, judge,
validatore e artefatti storici `q3_04` sono stati riconciliati. Nessuna diagnosi
runtime Spatial V2 equivalente risultava già eseguita.

La novità tecnica prevista era una singola generazione reale con relation
witness V2; le precedenti campagne riguardano NLI V2 o Spatial V1 e non sono
equivalenti.

## Caso canonico recuperato

Fonte autorevole:
`eval/claim_fidelity_gold_v1.json`.

- dataset SHA-256:
  `fdd6d9383493f58abd6d9a07fe0a029ecc7dc35bad106fe91ce747fb2463a605`;
- case ID: `q3_04`;
- source: `verticalizzazione_Bonacini`, pagina 2;
- Gold congelato: `contradicted`;
- claim SHA-256 UTF-8:
  `ea9d4276219edd1e37781c328541cdda4dd54c13eabc3185618ba4e0c96039bd`;
- evidence SHA-256 UTF-8:
  `302019bbce33aea87ab218afedbb823a7400defd56a134d1f867f2c35dd6fce1`.

I testi sono stati letti dal dataset Git, non ricostruiti da riassunti. Non sono
stati inviati a un modello.

## Preflight

### Ambiente locale

- repository/branch/baseline: conformi;
- daemon `http://127.0.0.1:11434`: non disponibile, connessione rifiutata;
- nessun ambiente runtime locale utilizzabile.

### VPS read-only

Alias risolto: `football-vps` → `football@163.5.26.155:22`,
`IdentitiesOnly=yes`, chiave configurata `codex-football-vps`.

- host: `football-data-lab.localdomain`;
- utente: `football`;
- endpoint Ollama `/api/tags`: disponibile;
- modello `qwen3.5:9b`: presente, digest
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
- `/api/ps`: nessun modello caricato;
- processo osservato: solo `/usr/local/bin/ollama serve`;
- nessun processo Spatial V2/Qwen concorrente osservato nello snapshot.

Staging Git presenti nel parent autorizzato:

- `s2-first-controlled-b1946f8`;
- `s2-spatial-differential-0d40719`;
- `tsc-v1-3fa3a18`;
- `tsc-v2-965d6b6`.

Nessuno punta alla baseline `009f76e71c0351da9d2b797ad3c9ff1928671a4e`.
Gli staging storici non sono stati modificati o riutilizzati. Il checkout
operativo non è stato usato.

## Configurazione prevista, non eseguita

Dal judge pubblicato:

- contratto `nli_spatial_relations_v2` `2.0.0`;
- modello `qwen3.5:9b`;
- temperature `0`;
- `num_ctx=4096`;
- `num_predict=2048`;
- timeout `180` secondi;
- `stream=false`, `think=false`;
- una chiamata, zero retry, repair e fallback.

La configurazione non è stata inviata a Ollama.

## Condizione bloccante e arresto

Il codice Spatial V2 autorizzato non è disponibile in un checkout isolato alla
baseline documentale sulla VPS; il PC locale non dispone di un daemon Ollama.
Spostare codice, creare staging, usare il checkout operativo o modificare un
vecchio staging richiederebbe un'attività ulteriore non autorizzata.

Il preflight è quindi **BLOCCATO**. L'attività si è arrestata prima della
costruzione/invio della richiesta generativa.

## Comandi effettivamente eseguiti

- letture Git locali e ricerca delle evidenze storiche;
- calcolo SHA-256 locale di dataset, claim ed evidence;
- GET locale `/api/tags`, fallito per endpoint assente;
- singola sessione SSH read-only per staging, `/api/tags`, `/api/ps` e snapshot
  processi.

Nessun comando di inferenza è stato eseguito.

## Artefatti runtime

Nessun manifest runtime, prompt inviato, risposta raw, witness o validation
result è stato creato, perché la generazione non è iniziata. Numero effettivo di
chiamate/generazioni al modello: **0**. Non esistono exit code o durata di una
generazione da registrare.

## Risultato e analisi semantica

- esito tecnico: **FAIL operativo pre-inferenza / BLOCCATO**;
- witness: non prodotto;
- label Spatial V2: non prodotta;
- PASS tecnico: non conseguito;
- PASS semantico: non valutabile;
- fail-closed del judge: non invocato;
- causa: assenza di un ambiente isolato alla baseline corrente, non difetto
  dimostrato del judge o validatore.

Non è possibile esaminare soggetto, referente, asse, valori, comparison o label
senza inventare un output assente.

## Limiti probatori

La presenza del modello e l'assenza di concorrenza nello snapshot non provano
che una futura finestra rimanga esclusiva. Il preflight non prova compatibilità
runtime dello structured output V2. Nessuna conclusione su accuratezza o
correzione di `q3_04` è autorizzata.

## Decisione e stati

Decisione: non eseguire l'inferenza e preservare gli ambienti esistenti.

| Componente | Stato |
|---|---|
| Preflight runtime Spatial V2 q3_04 | **ESEGUITO** |
| Diagnosi runtime q3_04 | **BLOCCATO** |
| Numero generazioni | 0 |
| Revisione indipendente del risultato | **DA FARE** solo dopo un run futuro |
| Efficacia semantica generale | **BLOCCATO** |
| Gate, integrazione S2, certificazione | **BLOCCATO** |

Unico prossimo passo proposto, non eseguito: richiedere autorizzazione separata
per predisporre uno staging Git isolato alla baseline esatta e verificarlo senza
inferenze. L'autorizzazione runtime corrente termina senza essere consumata da
una generazione, ma non consente automaticamente la predisposizione mancante o
un futuro tentativo.
