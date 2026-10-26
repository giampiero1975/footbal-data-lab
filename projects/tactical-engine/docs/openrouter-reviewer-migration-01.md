# Migrazione del revisore applicativo a OpenRouter — 01

Data: 2026-10-26  
Stato: **IMPLEMENTATO** (offline; runtime e deploy ancora **DA FARE**)

## Obiettivo e perimetro

OpenRouter diventa l'unico trasporto esterno attivo del pannello. Le integrazioni
dirette Gemini e Groq sono state rimosse da worker, configurazione e interfaccia.
Script, report e risultati storici restano nel repository per audit e non sono
richiamati dal percorso applicativo.

La pipeline RAG V5 certificata, gli indici e i risultati precedenti non sono
stati modificati. Non è stata eseguita alcuna chiamata API reale.

## Flusso implementato

`domanda -> RAG e fonti -> OpenRouter -> revisione tattica -> verifica delle evidenze -> risposta migliorata`

Il copilot mantiene due passaggi separati e fail-closed. OpenRouter riceve un
elenco ordinato di modelli e può applicare il fallback solo tra endpoint che
supportano i parametri richiesti. È richiesta la non raccolta dei dati lato
provider (`data_collection=deny`). Prompt, estratti e credenziali non vengono
salvati nei report d'errore.

Configurazione prevista sulla VPS:

- `OPENROUTER_API_KEY` nel file privato del servizio;
- `RAG_OPENROUTER_COPILOT_ENABLED=1`;
- `RAG_OPENROUTER_COPILOT_MODELS` per la cascata ordinata;
- `RAG_OPENROUTER_COPILOT_TIMEOUT_SECONDS` per il limite applicativo.

## Modifiche

- nuovo adapter `scripts/openrouter_tactical_copilot_v1.py`;
- API e persistenza migrate a `openrouter_copilot` e file
  `*.openrouter-copilot.json`;
- rimossi dal runtime i doppi passaggi Gemini/Groq;
- pannello reso provider-neutral e collegato a OpenRouter;
- esempi di configurazione privi delle vecchie chiavi dirette;
- test specifici per fallback ordinato, preflight senza rete, chiave obbligatoria
  e report d'errore redatto.

## Evidenze offline

- compilazione Python: PASS;
- suite API + adapter OpenRouter: **22/22 PASS**;
- sintassi JavaScript pannello: PASS;
- ricerca nelle superfici attive di variabili e invocazioni dirette Gemini/Groq:
  zero occorrenze;
- chiamate API: **0**.

## Decisione

La migrazione è **IMPLEMENTATA**, non ancora **VALIDATA** né **INTEGRATA**.
Prima della promozione servono installazione della chiave solo sulla VPS,
deploy anti-conflitto, test offline VPS e una singola prova completa dal
pannello pubblico. I risultati storici Gemini/Groq non vanno cancellati.

## Prima prova pubblica e correzione differenziale

La prima prova dal pannello, job `7cb0da28`, ha completato il RAG in 128,2 s
e raggiunto OpenRouter: tempo totale 187 s, 555 token generativi e quattro
evidenze. `openai/gpt-oss-120b` ha restituito structured output, poi bloccato
dal gate locale con `PASS1_CASE_COUNT_MISMATCH`. Il trasporto e la chiave sono
quindi operativi; il contratto non imponeva la cardinalità dell'array.

Correzione: schema per-request con `minItems=maxItems=numero casi` sia per
`reviews` sia per `revised_answers`, più istruzione esplicita nel primo prompt.
Suite aggiornata: **23/23 PASS**, zero ulteriori chiamate API. Una nuova prova
del medesimo caso è tecnicamente giustificata dalla variazione del contratto.

## Prove differenziali e risultato completo del caso 001

| Job | Differenza tecnica | RAG | Revisore | Totale | Esito |
| --- | --- | ---: | ---: | ---: | --- |
| `7cb0da28` | prima integrazione OpenRouter | 128,2 s | ~34 s | 187 s | `PASS1_CASE_COUNT_MISMATCH` |
| `111f3235` | cardinalità schema corretta | 73,35 s | timeout 240 s | 335 s | `openrouter_copilot_timeout` con `gpt-oss-120b` |
| `efb84ad8` | `openai/gpt-4o` primario | 127,6 s | 21,6 s | 171 s | revisore **verified**, voto bozza 5/10 |

Nel job riuscito i due passaggi OpenRouter hanno utilizzato complessivamente
4.343 token (3.087 input, 1.256 output) e sono costati **$0,0202775**:
$0,010385 il primo passaggio e $0,0098925 il secondo. Il provider effettivo
riportato è OpenAI, modello `openai/gpt-4o`.

La risposta migliorata è stata sottoposta alla stessa conversazione Gemini
esaminatrice e ha ricevuto **18/30**. Criticità: confusione tra terzino, ala e
“centrocampista esterno” nel 4-3-3; rimozione dell'ala sinistra dal mismatch sul
terzino ammonito; preventiva indebolita; mancato uso concreto di due slot e tre
cambi. Il percorso tecnico è quindi operativo, ma la qualità tattica non è
VALIDATA e resta sotto l'obiettivo medio 8/10.

È inoltre **IMPLEMENTATA** l'esposizione nel pannello di token e costo reale per
ogni revisione, ricavati esclusivamente dai campi `usage` OpenRouter. Test e
deploy di questa sola visualizzazione restano DA FARE.

## Remediation qualità verso 28/30

Il 18/30 ha mostrato due cause implementative, non soltanto un limite del
modello: il secondo passaggio riceveva finding ed evidenze ma non la domanda né
la bozza completa; inoltre poteva applicare solo correzioni documentate, anche
quando si trattava di geometria e coerenza interna direttamente verificabili
nel caso.

Correzione differenziale:

- PASS1 preserva esplicitamente sistema, lato, ruoli, minuto, punteggio e vincoli;
- ogni finding deve correggere concretamente l'errore, non ripeterlo;
- PASS2 riceve domanda, bozza, finding ed evidenze;
- nuova classe `GIUDIZIO_TECNICO`, ammessa solo quando
  `needs_document_check=false` e sempre senza citazioni;
- la risposta finale deve essere autonoma, completa e coprire struttura,
  movimenti, preventiva e cambi;
- gate fail-closed per impedire che un finding documentale venga promosso a
  giudizio tecnico.

Suite combinata Groq storico + OpenRouter + API: **40/40 PASS**. Nessuna API
usata nella correzione. Nuovo test autorizzato dalla differenza tecnica; criterio
di arresto: voto Gemini almeno **28/30**.

### Prova differenziale qualità 2 — job `8de1cbcc`

La correzione di preservazione del contesto è stata eseguita dal pannello
pubblico sul medesimo caso: RAG 73,3 s, revisore 15,701 s, totale 113 s,
quattro evidenze e stato `verified`. I due passaggi hanno usato 5.155 token
(3.472 input, 1.683 output) al costo totale di **$0,02551** ($0,01222 e
$0,01329). Gemini ha assegnato **25/30**, contro 18/30 della prova precedente.

Il progresso conferma la rimozione delle confusioni di ruolo, ma resta un
difetto implementativo: la risposta finale diagnostica la vecchia bozza invece
di sostituirla con un piano proattivo; omette ancora tre cambi/due slot,
rotazione per liberare l'ala e preventiva. Stato: **ESEGUITO**, non VALIDATO.

Differenza tecnica successiva: PASS1 deve produrre una `replacement_answer`
operativa completa (minimo locale 400 caratteri); PASS2 la usa come ossatura e
deve coprire struttura, movimenti, tutti i vincoli espliciti, area,
preventiva/transizione e trigger. Questa variante giustifica un solo nuovo test
del caso; criterio invariato: almeno **28/30**.
