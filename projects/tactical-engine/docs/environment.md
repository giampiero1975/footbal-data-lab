# Inventario VPS — evidenze raccolte

Data: 2026-10-19 (riepilogo delle verifiche comunicate in chat, eseguite nella sessione precedente). Fonte: output CLI VPS incollati dall'utente; **non** verifica remota indipendente. Ambiente: `/opt/football-data-lab`. Nessuna modifica runtime effettuata.

## Codice e Python
- VPS: branch `main`, working tree pulito al controllo, HEAD `e8242d3175dfc3a579fc75bf7cbea7d2237beb22`; non implica allineamento con GitHub corrente.
- Python sistema: `3.12.3`; venv individuato: `projects/tactical-engine/.venv` (versione interprete venv da verificare).
- Pacchetti nel venv: `docling==2.140.0`, `docling-core==2.101.1`, `chromadb==1.5.9`, `llama-index-core==0.14.25`, `llama-index-vector-stores-chroma==0.6.0`, `llama-index-embeddings-ollama==0.10.0`, `llama-index-llms-ollama==0.11.0`, `llama-index-node-parser-docling==0.5.0`, `llama-index-postprocessor-sbert-rerank==0.6.0`, `ollama==0.6.3` (SDK Python), `sentence-transformers==6.1.0`, `transformers==5.20.1`, `torch==2.6.0+cpu`, `pymupdf==1.28.2`, `pytest==9.1.1`, `numpy==2.5.4`.
- `python -m pip check`: “No broken requirements found”. Verifica solo metadata delle dipendenze, non compatibilità funzionale.

## Hardware
- KVM x86_64, 6 vCPU virtuali, host CPU AMD EPYC 7702P, AVX2; 1 nodo NUMA.
- RAM: 15 GiB totali, 14 GiB disponibili nel campione inattivo. Swap: 1,5 GiB quasi interamente occupati; `vmstat 1 5` non mostrava swap-in/out negli ultimi quattro campioni; CPU ~100% idle. Nessuna conclusione sulle prestazioni sotto inferenza.
- PCI VGA `1234:1111`: adattatore VGA virtuale QEMU; **nessuna GPU per accelerazione AI identificata** (non equivale a esclusione definitiva di ogni acceleratore).
- Disco, servizi, eventuali acceleratori pass-through: non verificati.

## Ollama — runtime e modelli
- Server/CLI Ollama `0.40.5`; SDK Python separato `0.6.3`.
- `ollama ps`: nessun modello caricato al momento del controllo.
- `ollama list`: `qwen3-embedding:0.6b` ID `ac6da0dfba84`, 639 MB; `qwen3.5:9b` ID `56671c2ab938`, 6,6 GB; `nomic-embed-text:latest` ID `0a109f422b47`, 274 MB.
- `ollama show qwen3.5:9b`: architettura `qwen35`, 9.0B, Q4_K_M, contesto dichiarato 262144, embedding length 4096, `requires 0.30.0`; completion/vision/tools/thinking, thinking default true; projector CLIP 456.01M; parametri nel modello `presence_penalty=1.5`, `temperature=1`, `top_k=20`, `top_p=0.95`. Non dimostra i parametri effettivi applicati dagli script.
- `ollama show qwen3-embedding:0.6b`: architettura `qwen3`, 595.78M, Q8_0, contesto dichiarato 32768, dimensione vettore 1024, capability embedding (anche tools/thinking riportate).
- `ollama show nomic-embed-text:latest`: architettura `nomic-bert`, 137M, F16, contesto dichiarato 2048, dimensione vettore 768, parametro `num_ctx=8192`; il parametro non prova supporto effettivo oltre il contesto dichiarato.
- Dimensioni vettoriali Nomic (768) e Qwen (1024) diverse: non scambiare embedding tra collection.

## Baseline e limiti della verifica
- Storico codice: V3 usa Docling HybridChunker con tokenizer Nomic, 86 chunk; V4 riusa i testi V3 con Qwen3-Embedding 0.6B; collection indicata `dribbling_tactics_v4_qwen3_embedding_06b`; V3 `dribbling_tactics_v3_contextualized`. **Presenza reale delle collection sulla VPS da verificare.**
- Storico V4: retrieval top_k=15, reranker mMARCO top_n=10 su CPU, Qwen3.5 9B con thinking disabilitato, contesto 8192, temperatura 0.1, CitationQueryEngine chunk_size 2048 e overlap 0; **parametri operativi ancora da confrontare con codice/servizio effettivamente eseguito**.
- Possibile disallineamento tokenizer Nomic/Qwen: ipotesi di ottimizzazione da verificare, **non difetto accertato**.
- Documentazione ufficiale e compatibilità incrociata delle versioni: revisione ancora da completare. Non dichiarare architettura ottimale sulla base del solo inventario.
- Non ripetere questi controlli senza motivo: rieseguirli solo dopo cambio VPS, aggiornamento, deploy o evidenza di deriva.

## Da verificare una sola volta, poi registrare
Collection Chroma e conteggi, entry point/servizi, versione interprete venv, storage, cache modelli/reranker, config runtime, backup e test rollback V4, benchmark semantici.

## Verifiche runtime aggiuntive — 2026-10-19

**Fonte:** output dei comandi eseguiti dall'utente sulla VPS e riportati nella conversazione. Non è un accesso SSH diretto dell'assistente. Checkout VPS aggiornato con `git pull --ff-only origin main` da `e8242d3` a `075bd1498819d782eea1d4107ca5b9c4c70c0a6e`; aggiornamento fast-forward senza conflitti, nessuna modifica agli indici.

- **Servizi:** `systemctl list-units --type=service --all` ha mostrato `ollama.service loaded active running`; non ha evidenziato un servizio nominato football/dribbling/tactical/surya. Il controllo dei processi ha trovato due helper Surya (`surya.fast_layout.server` e `surya.ocr_error.server`), ma nessun processo con nome dribbling/tactical-engine/uvicorn/gunicorn/streamlit. Questi controlli **non escludono** avvii manuali, cron, unità con nomi diversi o processi terminati.
- **Modelli installati, confermati con `ollama list`:** `qwen3-embedding:0.6b` ID `ac6da0dfba84` (639 MB), `qwen3.5:9b` ID `56671c2ab938` (6,6 GB), `nomic-embed-text:latest` ID `0a109f422b47` (274 MB). `ollama ps`: nessun modello residente nel campione.
- **Memoria:** `free -h`: RAM 15 GiB totale, 1,2 GiB usata, 8,6 GiB libera, 14 GiB available; swap 1,5 GiB totale e circa 1,5 GiB occupata. `vmstat 1 5`: nei quattro intervalli misurati `si=0`, `so=0`, CPU idle 100%, `wa=0`. La prima riga di vmstat è una media storica: non attribuirla all'intervallo. Nessuna evidenza di swapping attivo **durante il campione**; non implica che la swap sia inutilizzata in generale o che la latenza sotto carico sia validata.
- **Architettura:** non è stato ancora identificato un entry point di produzione V4. Ollama attivo non significa che DRIBBLING sia un servizio avviato.

**Nessuna modifica richiesta a RAM/swap o ai servizi.** Ripetere i controlli solo se cambiano risorse, processi, deployment o compaiono sintomi.
