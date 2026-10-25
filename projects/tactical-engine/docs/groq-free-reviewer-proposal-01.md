# Proposta tecnica — Groq Free come revisore alternativo (V5-GROQ-01)

Data: 2026-10-25. **Stato corrente: G0/G1 VALIDATI offline; G3 VALIDATO su
payload sintetico; G4 BLOCCATO in attesa di consenso privacy; G5 DA FARE.**
Nessuna integrazione o deploy. **Destinatario: Codex.** Questo
documento e una proposta, non autorizza deploy, attivazione billing,
sostituzione del revisore o esecuzione del benchmark. Evidenze G0/G1:
`docs/groq-free-reviewer-g0-g1-01.md`.

## Contesto verificato in GitHub
- Fonte autorevole: `projects/tactical-engine/todo.md`, `docs/experiment-register.md`, `docs/coverciano-100-gemini-benchmark-01.md`.
- Benchmark richiesto: 100 domande stile Coverciano, 10 categorie, rubriche nascoste, RAG riceve solo domanda, giudizio esterno 0–10, target media >=8 e zero citazioni invalide.
- Ultima evidenza verificata: 50/100 domande generate e preservate in
  `evaluation/coverciano-100-chunks-v1/`; Gemini 3.6 resta intermittente. Non
  rigenerare i casi esistenti, non ripetere probe gia concluse.
- La certificazione V5 locked CLI resta separata dalla revisione esterna, dal pannello e dal benchmark 100.

## Decisione da sottoporre al titolare
Valutare **Groq Free**, modello primario candidato `openai/gpt-oss-120b`, come **provider opt-in** del revisore esterno; mantenere Gemini esistente e i dati pregressi immutati. Fallback futuro opzionale solo dopo approvazione. Non e una promozione a INTEGRATO o CERTIFICATO.

## Evidenza ufficiale Groq, verificata il 25/10/2026
1. Piano Free, `openai/gpt-oss-120b`: **30 RPM, 1.000 RPD, 8.000 TPM, 200.000 TPD** (limiti base; verificare quelli effettivi della propria organizzazione). I limiti sono organizzativi, con possibili soglie ITPM/OTPM. HTTP 429 e header `retry-after`.
2. `openai/gpt-oss-120b` supporta Structured Outputs `response_format.type=json_schema`, `strict:true`, con tutti i campi required e `additionalProperties:false`. `qwen/qwen3.8-27b` e `openai/gpt-oss-20b` sono alternative documentate, non validate tatticamente.
3. Endpoint compatibile OpenAI: `https://api.groq.com/openai/v1`; chiave `GROQ_API_KEY`; API perlopiu compatibile, non identica. `n=1`; streaming e tool-use non supportati insieme a Structured Outputs.
4. Batch/Flex richiedono verifica del piano: **non presupporre accesso gratuito**.
Fonti:
- https://console.groq.com/docs/rate-limits
- https://console.groq.com/docs/structured-outputs
- https://console.groq.com/docs/openai
- https://console.groq.com/docs/models
- https://console.groq.com/docs/errors

## Architettura richiesta (non implementata)
- Introdurre un adapter `ExternalReviewer` con provider selezionabile `gemini|groq`, default Gemini invariato fino a decisione; modello e versione espliciti nei report.
- Riutilizzare **esattamente** la rubrica congelata e il contratto semantico del reviewer esistente; non modificare le risposte RAG, collection, locked manifest, scoring o schema dati senza una migrazione documentata.
- Schema JSON: ID breve mappato a UUID runtime, voto numerico 0–10, verdetto, errori, evidenze, correzione, eventuali campi obbligatori gia previsti. Adattare schema alla compatibilita `strict:true` e validare localmente anche semantica, ID, citazioni e range; un JSON valido non prova correttezza tattica.
- Fail-closed: niente voto se ID/citazioni non corrispondono, se risposta incompleta o errore; non imputare zero ai casi senza revisione.
- Nessun segreto nei commit/log; nessun PDF completo o credenziale nel payload; minimizzazione di estratti. Chiave solo su VPS tramite env/secret manager; non inserirla nel pannello/browser.
- Report per caso: provider, model, prompt/rubric hash, case ID, hash payload, tempo, token usage se disponibili, stato HTTP, schema result, validita citazioni, voto, motivazione, commit; non sovrascrivere report precedenti.
- Limiti: scheduler conservativo, una richiesta alla volta; rispettare RPM/RPD/TPM/TPD e header; su 429 usare retry-after e backoff con jitter; su 5xx backoff limitato; stop su 400/401/403 senza retry automatici. Budget giornaliero hard stop, nessun upgrade/billing.

## Simulazione di capacita — solo aritmetica, NON chiamate Groq
Ipotesi per 100 revisioni: 2.200 token input + 650 output = **2.850 token/caso**; totale **285.000 token**, oltre i 200.000 TPD di un singolo giorno. Minimo teorico **2 giorni** (senza altri consumi). A 8.000 TPM servono almeno **36 minuti** per i soli token, ma la quota giornaliera domina. I token di ragionamento e gli overhead possono cambiare la stima. Non e un test prestazionale.
Ipotesi prudente: 5.000 token/caso => 500.000 token => minimo 3 giorni teorici. Misurare `usage` su un caso autorizzato prima di pianificare 100 revisioni.

## Piano per Codex — cancelli e anti-duplicazione
**G0 — Riconciliazione (VALIDATO offline):** TODO, registro, commit, VPS e
contratto reviewer riconciliati; stato 50/100, Groq assente dal runtime.
**G1 — Compatibilita offline (VALIDATO offline):** adapter isolato e suite
riproducibile 6/6 per schema strict, 200, 429, 503, 400/401/403, ID, citazioni,
interruzione/ripresa e quote. Nessuna chiamata di rete; nessuna regressione RAG.
**G2 — Autorizzazione utente e credenziali (ESEGUITO, con rotazione richiesta):** chiave Free fornita dal titolare e usata soltanto nel processo temporaneo; non salvata nel repository o nel servizio. Essendo stata incollata in chat, deve essere revocata e rigenerata.
**G3 — Singola probe reale (VALIDATO per compatibilita tecnica):** connettivita minima e Structured Output strict verificati su `openai/gpt-oss-120b`; il client completo ha prodotto una revisione valida di un caso sintetico. Non equivale a validazione tattica.
**G4 — Un solo caso tattico congelato (BLOCCATO, consenso privacy necessario):** nessun contenuto RAG reale e stato inviato a Groq. Serve autorizzazione esplicita per domanda, risposta ed estratti delle evidenze; niente PDF completi o segreti.
**G5 — Decisione (DA FARE):** promuovere a provider opt-in soltanto se compatibilita, indipendenza, costo zero e qualita sono accettabili; pianificare i restanti casi senza duplicati e senza consumare risposte gia valide.

## Workflow obbligatorio
**Attivita -> Script -> Commit -> Report -> Risultato -> Decisione -> Stato.**
Dopo ogni report eseguito aggiornare registro e TODO nella stessa sessione. Stati ammessi: DA FARE, IMPLEMENTATO, ESEGUITO, VALIDATO, INTEGRATO, CERTIFICATO, BLOCCATO. Nessun test equivalente a quelli gia eseguiti. Distinguere simulazione offline, probe API, revisione tattica, integrazione e certificazione.

## Cosa deve fare il titolare
1. Aprire https://console.groq.com/ e creare account Free.
2. Verificare nel pannello Limits il modello e le quote reali, senza abilitare pagamenti.
3. Creare API key dal pannello Keys; conservarla privatamente (non su GitHub).
4. Autorizzare esplicitamente a Codex una singola probe dopo G0/G1; solo successivamente decidere integrazione.

## Stato della proposta
**IMPLEMENTATO e VALIDATO offline** per G0/G1 e **VALIDATO tecnicamente** per
G3 con payload sintetico. G4 resta BLOCCATO per consenso privacy e G5 DA FARE.
Nessun costo, deploy o modifica al runtime/pipeline.

Aggiornamento successivo: probe minima esplicitamente autorizzata **ESEGUITA**
su `openai/gpt-oss-120b`; chiave valida, usage e tempi ricevuti, nessun deploy.
Structured Output live e stato poi VALIDATO su payload sintetico; la qualita
tattica resta DA FARE. La chiave incollata in chat deve essere ruotata prima
di un uso stabile.

## Esito Structured Output live (2026-10-25)

La prima esecuzione dell'adapter completo ha ricevuto HTTP 403, Cloudflare
`error code: 1010`. Una probe equivalente con `curl` e JSON Schema strict ha
risposto HTTP 200 con `{"result":"OK"}`: l'errore non dipendeva dallo schema,
dal modello o dal Free Tier, ma dallo User-Agent predefinito di `urllib`.
L'adapter ora dichiara `User-Agent: football-data-lab-groq-reviewer/1.0` e
conserva soltanto diagnostica HTTP redatta.

Con un caso interamente sintetico, senza dati o fonti del progetto, il client
completo ha risposto HTTP 200 in 1,628 s: 816 token prompt, 638 completion (488
reasoning), 1.454 totali; output validato, score 8,5, verdetto PASS, due punti
di forza e nessun errore strutturale/evidenza. Suite offline ancora 6/6 PASS.

Decisione: G3 e **VALIDATO per compatibilita tecnica**, non per competenza
tattica. Il tentativo G4 e stato fermato prima dell'invio: domanda, risposta
RAG ed estratti costituiscono contenuto reale da trasmettere a un nuovo
fornitore e richiedono consenso specifico. Nessun PDF, token o dato RAG reale
e stato inviato a Groq.

## Report simulazione offline (2026-10-25)
Attivita: verificare logica illustrativa di validazione fail-closed e aritmetica delle quote, senza rete.
Script: snippet Python temporaneo eseguito fuori repository (nessun adapter Groq implementato).
Commit: documentazione `0e8b369`; questo aggiornamento documentale ha commit separato.
Report/Risultato: **5/5 scenari mock** con esito atteso: caso conforme VALIDATO per sola struttura simulata; ID errato BLOCCATO; citazione inesistente BLOCCATO; voto 11 BLOCCATO; campo mancante BLOCCATO. Aritmetica: 285.000 token -> minimo 2 giorni; 500.000 token -> minimo 3 giorni.
Decisione: mock illustrativo sufficiente per verificare la logica proposta, **non** valida codice del progetto, schema Groq reale, API, disponibilita, output tattico o integrazione. Codex deve implementare test riproducibili G1 nel repository prima di ogni probe reale.
Stato: **ESEGUITO** per simulazione esterna; integrazione Groq **DA FARE**.
