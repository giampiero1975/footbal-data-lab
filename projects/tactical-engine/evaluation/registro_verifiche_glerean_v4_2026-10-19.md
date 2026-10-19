# Registro verifiche Glerean V4 — 2026-10-19

## Configurazione preservata
- Collection Chroma: `dribbling_tactics_v4_qwen3_embedding_06b`, 86 record.
- Embedding: qwen3-embedding:0.6b; reranker: BAAI/bge-reranker-v2-m3 CPU; LLM: qwen3.5:9b.
- Nessuno dei benchmark sotto modifica la collection.

## Risultati verificati dai report condivisi
1. **Audit citazioni V4**: sei risposte; nessun ID di citazione non valido; test unitari audit 3/3. La correttezza dell'ID non dimostra fedelta' semantica.
2. **Matrice semantica**: 6 risposte, 20 claim (10 numeric, 10 stable). Giudizi manuali usati come riferimento sperimentale, non gold standard indipendente.
3. **Primo giudice post-generazione** (`benchmark_verificatore_semantico_v4.json`): 1/3 accordi valutabili; 5/6 risposte fallite per controlli di citazione letterale/fonte inesistente. Risultato non utilizzabile come misura generale.
4. **Giudice answer-only V4-bis** (`benchmark_verificatore_semantico_v4_bis.json`): 15/20 accordi (75%), tutti i 20 claim valutati. Possesso numeric 1/3; possesso stable 2/3; uno-contro-uno numeric 2/3; uno-contro-uno stable 2/3; verticalita' numeric 4/4; verticalita' stable 4/4.
5. **Errore critico ancora non rilevato**: nella risposta UNO-CONTRO-UNO stable, la ricezione negli spazi laterali/centrali sulla linea difensiva avversaria e' attribuita anche a difensori e centrocampisti, mentre GLEREAN-C018 attribuisce a questi ultimi la gestione della palla e agli attaccanti la predisposizione alla ricezione. Il giudice V4-bis ha etichettato `parziale` invece di `incompatibile`.

## Esperimento successivo
Script `scripts/benchmark_ruoli_tattici_v4.py`:
- 10 affermazioni sintetiche pre-etichettate; fonte unica GLEREAN-C018.
- Controlli positivi, omissione e alterazioni di reparto, movimento e spazio.
- Una chiamata Ollama per affermazione, output JSON strutturato, report incrementale; nessuna modifica a Chroma.
- Limiti: un solo passaggio fonte, campione piccolo, dati sintetici. Non misurare con questo benchmark l'accuratezza globale di DRIBBLING.

## Fonti tecniche ufficiali
- Ollama structured outputs: https://docs.ollama.com/capabilities/structured-outputs
- Ollama API chat: https://docs.ollama.com/api/chat
- GitHub REST Contents API: https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents

## Decisioni
- Non promuovere il verificatore automatico in produzione prima di misurare il rilevamento delle contraddizioni.
- Conservare i risultati dei test falliti.
- Evitare modifiche a V4 prima di una verifica reversibile e di regressione.
