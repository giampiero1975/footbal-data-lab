# DRIBBLING — protocollo comparativo modelli locali (20 ottobre 2026)

## Scopo
Selezionare un generatore documentale per fonti tattiche italiane, senza confondere
la qualita' del generatore con quella del giudice LLM. Nessuna promozione
automatica in produzione.

## Stato e fonti
- Gold esistente: `evaluation/gold_glerean_principi_v1.json` (3 domande, 10 claim).
- Baseline e prompt v2: `benchmark_citazioni_stabili_v4.json`,
  `confronto_risposte_v4_prompt_v2.json`.
- V4 Chroma, embedding, reranker e produzione NON devono essere modificati.
- Modelli da confrontare in modo isolato: `qwen3.5:9b` (controllo),
  `gemma3:12b`, `ministral-3:8b-instruct-2512-q4_K_M`.
- `granite4:7b-a1b-h`: candidato giudice, non considerarlo affidabile
  finche' non supera la validazione contro etichette umane.
- Fonti ufficiali:
  - https://ai.google.dev/gemma/docs/core/model_card_3
  - https://ollama.com/library/gemma3
  - https://docs.mistral.ai/models/ministral-3-8b-25-12
  - https://ollama.com/library/ministral-3/tags
  - https://www.ibm.com/granite/docs/models/granite4-0
  - https://docs.ollama.com/api/chat

## Disegno sperimentale
1. Congelare e registrare i contesti TOP5 gia' salvati; non interrogare Chroma.
2. Usare le stesse 3 domande, le stesse fonti, lo stesso formato delle citazioni
   e lo stesso prompt per ogni modello; temperatura 0 o bassa e dichiarata.
3. Usare tag esatti e registrare digest, quantizzazione, RAM e parametri
   effettivi; non assumere che la dimensione su disco sia la RAM necessaria.
4. Eseguire i modelli **uno per volta**, senza cambiare il modello di produzione.
5. Registrare testo grezzo, latenza, token, errore di esecuzione e metadati.
6. Controllare ogni claim con evidenza del Gold e leggere le risposte per
   trovare affermazioni aggiuntive false o non supportate.
7. Non utilizzare il giudizio di Qwen come ground truth.
8. Separare ID citazione e riferimenti di pagina: `pagina [11]` non e'
   una citazione inventata. Verificare anche che l'ID valido supporti la frase.
9. Valutare: fedelta' (prioritaria), errori gravi di ruolo/zona/soggetto,
   copertura 10 claim, pertinenza, citazioni, rifiuti immotivati, tempo e RAM.
10. Esito: scegliere un candidato soltanto se non peggiora gli errori gravi,
    mostra copertura utile e rientra nel budget della VPS; altrimenti mantenere
    V4 e documentare la mancata promozione.

## Errori sentinella da ricercare
- U2: attribuire al portiere la spizzata eseguita da un compagno di reparto.
- V4/zone: confondere la nostra zona difensiva con quella avversaria.
- P1-P3: rifiutare la domanda pur avendo fonti pertinenti.
- U3: attribuire agli attaccanti compiti dei difensori/centrocampisti.
- V3: scambiare le regole di movimento dei centrocampisti con quelle dei difensori.

## Condizioni di sicurezza
Prima di qualsiasi download sulla VPS: verificare spazio libero, memoria
disponibile, processi Ollama attivi e compatibilita' del tag con la versione
installata. Non arrestare servizi, non sovrascrivere file, non sostituire
modelli, non modificare il database. Se mancano le condizioni, interrompere
il test e riportare il motivo. Non effettuare benchmark estesi prima del
controllo di fattibilita'.

## Limiti
Le schede dei produttori descrivono capacita' generali, non garantiscono
fedelta' tattica in italiano. Il Gold copre solo 3 domande e 10 claim:
utile per screening, insufficiente per dichiarare un vincitore definitivo.

## Rilievi VPS comunicati dall'operatore (20 ottobre 2026)
I seguenti valori derivano da output di comandi eseguiti dall'utente via PuTTY;
non sono misurazioni effettuate direttamente dall'assistente via SSH.

- `free -h`: RAM totale 15 GiB; usata 1.2 GiB; libera 13 GiB;
  disponibile 14 GiB. Swap totale 1.5 GiB, usata 1.5 GiB,
  libera 72 KiB. Swap piena: causa non ancora diagnosticata.
- `df -h`: filesystem root `/dev/vda1` 58 GB, usati 27 GB,
  disponibili 31 GB, occupazione 47%; /boot 881 MB, liberi 703 MB;
  /boot/efi 105 MB, liberi 99 MB.
- `ollama list`: `qwen3-embedding:0.6b` (ID ac6da0dfba84,
  639 MB); `qwen3.5:9b` (ID 56671c2ab938, 6.6 GB);
  `nomic-embed-text:latest` (ID 0a109f422b47, 274 MB).
- Gemma 3, Ministral 3 e Granite 4 non figurano tra i modelli
  installati al momento della rilevazione.
- `ollama ps`: richiesto, risultato non ancora ricevuto.
- Versione Ollama, CPU e carichi di inferenza: ancora da verificare.
- Accesso SSH diretto da ChatGPT: non disponibile negli strumenti
  connessi in questa conversazione. L'accesso SSH via PuTTY dell'utente
  e' operativo, ma non trasferibile automaticamente alla sessione ChatGPT.

**Valutazione preliminare:** RAM e spazio disco appaiono compatibili con
un test isolato di Gemma 3 12B quantizzato, ma la fattibilita' reale
richiede conferma di modelli caricati, RAM durante inferenza e prestazioni CPU.
Nessuna modifica alla configurazione V4 e nessun download eseguito.

- Aggiornamento operatore: `ollama ps` non riporta processi/modelli caricati al momento del controllo. Non equivale a dire che il servizio Ollama sia spento.
- Ricerca directory plugin ChatGPT (termini `SSH` e `SSH remote server terminal command execution`): nessun plugin SSH dedicato trovato tra i risultati disponibili; non e' stato installato nulla.

## Verifica canale remoto GitHub Actions (20 ottobre 2026)

- Repository `giampiero1975/footbal-data-lab`: visibilita' **public**
  verificata con GitHub API; accesso amministrativo disponibile.
- Documentazione ufficiale GitHub sconsiglia self-hosted runner su repository
  pubblici, specialmente su macchine con servizi e segreti di produzione:
  https://docs.github.com/en/actions/reference/security/secure-use
- I runner self-hosted sono tecnicamente supportati su Linux e usano
  connessioni in uscita HTTPS 443; il supporto non elimina il rischio:
  https://docs.github.com/en/actions/reference/runners/self-hosted-runners
- Gli strumenti GitHub collegati consentono lettura di workflow job/log e
  modifiche al repository, ma non espongono un'azione diretta di
  workflow_dispatch; l'uso di un workflow su push non sostituisce un
  terminale SSH interattivo.
- **Decisione:** NON installare un runner persistente sulla VPS di produzione
  collegato al repository pubblico. Nessuna modifica al server.
- Alternative da valutare solo se servono davvero: runner GitHub-hosted con
  accesso SSH limitato e credenziali in secrets (richiede configurazione),
  oppure integrazione MCP remota con autenticazione e autorizzazioni ristrette.
- Ricerca plugin SSH dedicato nella directory ChatGPT: nessun risultato.

- Versione Ollama rilevata dall'operatore con `ollama --version`: **0.40.5**. La compatibilita' specifica del tag Gemma 3 12B con questa versione non e' ancora stata confermata mediante un caricamento effettivo.

- L'operatore conferma completato il download/installazione di `gemma3:12b` tramite `ollama pull gemma3:12b`. Conferma dichiarata dall'operatore; digest e caricamento effettivo ancora da verificare. V4 non modificata.

- Smoke test `ollama run gemma3:12b "Rispondi esclusivamente con la parola OK."`: risposta `OK` confermata dall'operatore. Il modello genera correttamente su VPS; memoria di picco, tempi e fedelta' documentale ancora non misurati. Il test non e' parte del Gold.

- `ollama ps` dopo smoke test: `gemma3:12b`, ID `b92b218582c5`, SIZE `8.1 GB`, PROCESSOR `100% CPU`, CONTEXT `4096`, RUNNER `llamacpp`, UNTIL `4 minutes from now`. Output comunicato dall'operatore. SIZE non equivale alla misura di picco RSS/RAM. Inferenza esclusivamente CPU: latenza e sostenibilita' benchmark ancora da misurare.

- `free -h` con Gemma 3 12B caricata (output operatore): Mem totale 15 GiB, usata 9.7 GiB, libera 254 MiB, buff/cache 6.0 GiB, **available 5.9 GiB**; swap totale 1.5 GiB, usata 1.5 GiB, libera 212 KiB. Baseline precedente: Mem usata 1.2 GiB, available 14 GiB, swap gia' satura. Delta indicativo RAM usata +8.5 GiB, available -8.1 GiB; non e' una misura isolata di RSS o picco. La swap era gia' piena prima del caricamento, quindi non attribuire il suo stato a Gemma. Non usare il dato `free` (254 MiB) come disponibilita' effettiva perche' cache recuperabile.

## Preparazione benchmark — verifica fonti (20 ottobre 2026)
- Gold recuperato direttamente dal repository: `evaluation/gold_glerean_principi_v1.json`; 3 casi (`POSSESSO-002`, `UNO-CONTRO-UNO-003`, `VERTICALITA-004`), 10 claim P1-P3/U1-U3/V1-V4.
- PDF primario `334_principi_Glerean.pdf` individuato direttamente in Google Drive (ID `0B6maey1azXc5YnlONlQwd2EtMDA`).
- Le due baseline JSON citate dal protocollo (`benchmark_citazioni_stabili_v4.json`, `confronto_risposte_v4_prompt_v2.json`) non sono risultate accessibili ai percorsi `projects/tactical-engine/evaluation/` tentati né dalla ricerca Drive. La loro collocazione effettiva e soprattutto i contesti TOP5 congelati restano da individuare; **non ricostruire contesti a memoria né interrogare Chroma in sostituzione**.
- Prima di inviare prompt a Gemma, verificare dimensione dei contesti TOP5 in token rispetto a CONTEXT 4096; non troncare silenziosamente. Necessario anche registrare latenza e testo grezzo.

- Inventario VPS ricevuto dall'operatore: artefatti effettivamente presenti in `/opt/football-data-lab/projects/tactical-engine/` (non sotto `evaluation/`): `confronto_risposte_v4_prompt_v2.json`, `benchmark_citazioni_stabili_v4.json`, `benchmark_generazione_glerean_3casi.json`, relativi script sotto `scripts/`. Sono percorsi attestati da output `find`, ma contenuto/struttura dei JSON ancora da ispezionare. L'assenza precedentemente dichiarata era limitata al percorso repository tentato.
