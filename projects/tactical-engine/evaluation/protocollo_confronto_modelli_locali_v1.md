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
