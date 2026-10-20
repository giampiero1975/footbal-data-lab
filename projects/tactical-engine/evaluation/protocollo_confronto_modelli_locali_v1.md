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
