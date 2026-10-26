# Groq copilot — remediation HTTP 400

## Attività

Diagnosticare offline il `GROQ_HTTP_400` emerso nella seconda smoke autorizzata,
senza ripetere la chiamata, trasmettere dati o modificare la pipeline RAG locked.

## Evidenze ufficiali consultate

- Groq Structured Outputs: `openai/gpt-oss-120b` supporta `strict:true`; tutti i
  campi devono essere required e ogni object deve dichiarare
  `additionalProperties:false`:
  <https://console.groq.com/docs/structured-outputs>.
- Groq OpenAI compatibility: `temperature=0` viene convertita a `1e-8` e, in
  caso di problemi, Groq raccomanda un float positivo `<=2`; alcuni parametri
  non supportati producono HTTP 400:
  <https://console.groq.com/docs/openai>.
- Groq error codes: HTTP 400 indica una richiesta non valida e il body contiene
  la categoria diagnostica:
  <https://console.groq.com/docs/errors>.

## Diagnosi

I due schemi applicativi rispettano offline i requisiti strict e il modello è
ufficialmente compatibile. Il report precedente conservava però soltanto
`GROQ_HTTP_400`, insufficiente per distinguere schema, parametro, modello,
dimensione o output. Il client inviava inoltre `n` e `stream` espliciti e
`temperature=0`, non necessari nell'esempio ufficiale.

## Correzione isolata

- payload ridotto a modello, `temperature=0.1`, messaggi e response format;
- schema strict e validatori fail-closed invariati;
- lettura massima di 64 KiB del body di errore solo per classificare categorie
  predefinite; messaggio, body, prompt ed evidenze non vengono salvati;
- nessun fallback permissivo e nessun retry automatico.

## Verifica

Suite combinata copilot, reviewer precedente e API: **33/33 PASS**;
`py_compile` PASS; chiamate API reali: **0**. La correzione è
**VALIDATA offline**, non ancora INTEGRATA. Serve una singola smoke differenziale
autorizzata sul caso congelato; se fallisce, il nuovo codice redatto renderà
identificabile la categoria senza divulgare dati.

## Deploy controllato

Commit `301d3dd` distribuito con fast-forward sulla VPS. Suite VPS 33/33,
`py_compile` PASS, servizio `football-rag-api.service` attivo e checkout pulito.
Il deploy non ha eseguito inferenze né chiamate Groq. Stato applicativo:
**IMPLEMENTATO** e **VALIDATO offline**; validazione runtime ancora **DA FARE**.

## Prova utente successiva e contratto locale

Il titolare ha eseguito dal pannello un caso 4-3-3 contro 5-4-1. Il trasporto
Groq ha completato in 8 secondi, ma il risultato e stato respinto come
`GROQ_INVALID_STRUCTURED_RESPONSE`: il precedente HTTP 400 e quindi risolto.
Telemetria completa: RAG 168 s, Groq 8 s, reviewer Gemini legacy 8 s in HTTP
503, totale 184 s, quattro evidenze. La bozza RAG e rimasta disponibile come
previsto dal fail-closed.

La revisione del contratto normalizza ora esclusivamente campi meccanici:
identificativo del caso, ID finding e verdetto derivato deterministicamente
dal voto. Domanda, voto, osservazioni e contenuto tattico non vengono modificati.
Gli altri errori restano fail-closed e sono riportati con un codice specifico
PASS1/PASS2 redatto. Suite combinata: **34/34 PASS**, zero API nella correzione.

Il reviewer Gemini API legacy deve essere disabilitato nella configurazione VPS:
nel protocollo corrente Gemini Cloud e l'esaminatore manuale, mentre Groq e il
copilot applicativo. Questo elimina una chiamata 503 inutile senza toccare RAG,
indice o copilot.

## Smoke isolata autorizzata sul risultato esistente

Autorizzazione esplicita ricevuta per il job `a5b991d0`, con domanda, risposta
RAG e quattro estratti; nessun PDF o segreto. Nessun nuovo retrieval o RAG.
Il primo passaggio Groq ha superato normalizzazione e validazione; il secondo ha
fallito in 6,697 s con `GROQ_PASS2_FINDING_COVERAGE`, cioe non ha restituito un
check per ogni finding. Il sistema non ha inventato classificazioni e ha
bloccato la composizione.

Correzione offline: ogni check omesso viene aggiunto deterministicamente come
`ULTERIORE_RETRIEVAL`, senza label e con motivazione locale; eventuali finding
non supportati vengono rimossi dagli applicati e mantenuti tra gli irrisolti.
Check sconosciuti o duplicati restano errori. Suite combinata **35/35 PASS**,
compilazione PASS, nessuna ulteriore API. Stato: **IMPLEMENTATO e VALIDATO
offline**; una nuova smoke richiede una nuova autorizzazione.

