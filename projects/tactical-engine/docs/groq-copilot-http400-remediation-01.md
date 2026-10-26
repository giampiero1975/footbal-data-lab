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

