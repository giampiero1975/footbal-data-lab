# RD-TSC-V2-D3-S2-Q3-04-ADMIN-LOG-EXPORT-01

## Baseline, autorizzazione e accesso

Recupero amministrativo read-only dei log storici del run Spatial V2 `q3_04`.

- HEAD documentale iniziale:
  `49dac1fd9d3625665b16d63669e5229f0893c18d`;
- baseline runtime:
  `009f76e71c0351da9d2b797ad3c9ff1928671a4e`;
- finestra: `2026-11-07 12:19:00–12:25:30 CET`;
- timezone verificata: `Europe/Rome`, UTC+01:00.

La configurazione iniziale esponeva soltanto l'utente `football`. Dopo il primo
arresto fail-closed, il titolare ha fornito autorizzazione esplicita per usare la
password sudo già nota. La password è stata immessa una sola volta nel prompt
interattivo, non è stata inserita in comandi, file, log, report o repository.
Sono stati eseguiti soltanto i due `journalctl` read-only autorizzati.

## Export e integrità

Directory protetta esterna a repository e staging:
`/home/football/.local/share/football-data-lab/evaluation/spatial-v2-q3-04-admin-log-export-01`.

- `ollama.log`: 51.697 byte, 345 righe, SHA-256
  `b744afe6de243a4c4b65305293c629781c3832a57f8a06e766f160f2b69cbc8f`;
- `kernel.log`: 5.312 byte, 20 righe, SHA-256
  `2ef94823ec8e7c7c31e7ad942890d950070921bf20ab1e1e733a00de78fc76b6`;
- `hashes.sha256`: 394 byte, SHA-256
  `d3083a5ce59172e25c72534872f4901f9763dd8fa7627d93d4b86bf426e131eb`.

L'inventario ha verificato anche comando, timezone e timestamp di acquisizione.
`sha256sum -c` è PASS per tutti i file elencati. Gli export grezzi restano fuori
dal repository; nel report sono riportati solo dati tecnici pertinenti.

## Evidenze Ollama

La correlazione è elevata: un solo POST `/api/chat` appare nella finestra e
coincide al millisecondo con l'avvio/timeout degli artefatti client.

1. `12:20:38.573`: avvio `llama-server`, CPU-only, memoria di sistema 15,6 GiB,
   14,8 GiB liberi e 1,3 GiB swap libera;
2. `12:20:39.353`: fitting completato in 0,68 s, proiezione 2.597 MiB host e
   13.348 MiB lasciati liberi;
3. `12:20:47.369`: server avviato in **8,80 s**;
4. `12:20:47.379`: task 0 avviato, prompt da 188 token;
5. `12:20:53.507`: prompt processing 184 token in **6,13 s**, 30,02 token/s;
6. `12:21:06–12:23:36`: generazione continua, da 100 a **1.325 token**,
   velocità stabilizzata a circa **8,13 token/s**;
7. `12:23:38.596`: POST `/api/chat` termina HTTP **500** dopo esattamente 3m0s;
8. `12:23:38.713`: Ollama cancella task 0 e rilascia lo slot con **1.529 token
   totali**, `truncated=0`.

Non è registrato un EOS o un completamento valido prima della cancellazione.
Il limite `num_predict=2048` non era stato raggiunto. Il server ha continuato a
generare fino alla chiusura client e ha cancellato il task subito dopo.

## Evidenze kernel e risorse

Nella finestra non risultano OOM, processi uccisi, errori memoria, swap, GPU,
segfault, I/O error o task bloccati. Ollama ha usato sei thread CPU; non emerge
offload GPU. La memoria proiettata era ampiamente compatibile con quella libera.

Saturazione memoria ed errore di caricamento sono quindi esclusi dalle evidenze
disponibili. Il log non dimostra saturazione CPU: mostra invece generazione
regolare e continua a circa 8 token/s.

## Timeline client/server integrata

| Timestamp CET | Componente | Evento | Significato |
|---|---|---|---|
| 12:20:38.403 | client | wrapper avviato | artefatti client |
| 12:20:38.573 | Ollama | avvio caricamento | richiesta accettata |
| 12:20:47.369 | Ollama | server pronto dopo 8,80 s | caricamento non dominante |
| 12:20:47.379 | Ollama | task generativo avviato | 188 token prompt |
| 12:20:53.507 | Ollama | prompt elaborato in 6,13 s | inizio decode |
| 12:21:06–12:23:36 | Ollama | 100→1.325 token a ~8,13 t/s | generazione attiva |
| 12:23:38.586 | client | `E_JUDGE_TIMEOUT` | timeout 180 s |
| 12:23:38.596 | Ollama HTTP | POST chiuso 500 dopo 3m0s | client senza risposta completa |
| 12:23:38.713 | Ollama | task cancellato, 1.529 token totali | nessun completamento post-timeout |

## Causa e matrice aggiornata

La causa documentabile è una **generazione CPU troppo lunga rispetto al timeout
client di 180 secondi**: il caricamento ha richiesto solo 8,80 s, ma il modello
ha continuato a produrre output strutturato a circa 8,13 token/s senza terminare
entro il limite. Il client è scaduto, Ollama ha restituito 500 e ha cancellato il
task. Non risultano errori memoria, server bloccato o concorrenza nella finestra.

| Possibile causa | Qualificazione aggiornata |
|---|---|
| Timeout client | **Dimostrata** |
| Generazione oltre la finestra disponibile | **Dimostrata** |
| Caricamento iniziale dominante | **Esclusa** (8,80 s) |
| Errore caricamento/modello | **Esclusa** |
| Saturazione memoria/OOM | **Esclusa** nella finestra osservata |
| Errore o stallo server | **Esclusa**: avanzamento token continuo |
| Concorrenza | **Non supportata** |
| Structured output come causa primaria | **Non determinabile** |
| Completamento server dopo timeout | **Esclusa**: cancellazione immediata |
| Fail-closed wrapper | **VALIDATO** nel singolo tentativo |

## Decisione e stati

Il recupero e l'analisi amministrativa sono **ESEGUITO**. Le evidenze di log e
la causa operativa sono **VALIDATO** nel singolo tentativo. La correttezza
semantica resta non valutabile perché non è stato prodotto un witness completo.

Unico prossimo passo raccomandato, non eseguito: progettare e sottoporre a
revisione statica una singola variante diagnostica che riduca il massimo output
generabile mantenendo invariati modello, schema, prompt e timeout, con stima
preventiva del budget token compatibile con ~8,13 token/s. Qualunque nuova
generazione richiede autorizzazione distinta.

| Componente | Stato |
|---|---|
| Export amministrativo log | **ESEGUITO** |
| Integrità export e causa operativa | **VALIDATO** |
| Fail-closed del singolo tentativo | **VALIDATO** |
| Diagnosi semantica `q3_04` | **BLOCCATO** |
| Accuratezza, Gate, integrazione, certificazione | **BLOCCATO** |

