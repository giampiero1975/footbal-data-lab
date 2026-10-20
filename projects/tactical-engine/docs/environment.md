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

## Verifica runtime Docling — 2026-10-20

Output riportato dall'utente dopo esecuzione sulla VPS con l'interprete `projects/tactical-engine/.venv/bin/python`.

- Versione: `docling 2.140.0`.
- `generate_picture_images`: disponibile, default `False`.
- `generate_page_images`: disponibile, default `False`.
- `do_picture_description`: disponibile, default `False`.
- `do_picture_classification`: disponibile, default `False`.
- `picture_description_options`: disponibile; default visualizzato solo parzialmente (`batch_size=8 scale=2.0 picture_area_threshold=0.05 ...`).
- `images_scale`: disponibile, default `1.0`.
- `enable_remote_services`: disponibile, default `False`.

Questo conferma la presenza delle API, non l'efficacia sui diagrammi tattici. Nessuna modifica a V4 o agli indici.

## Audit figure già estratte — 2026-10-20

**Evidenza:** output VPS riportato dall'utente dopo esecuzione dello script read-only `projects/tactical-engine/scripts/audit_existing_docling_figures.py` (commit `f702890`). Cartella esaminata: `/opt/football-data-lab/knowledge/processed`.

| Documento | Pipeline | Figure Docling | Manifest | Metadati estratte | JSON/manifest mancanti |
| --- | ---: | ---: | ---: | ---: | --- |
| `formations-and-systems/334_principi_Glerean.pdf` | 2 | 27 | 27 | 27 | no/no |
| `formations-and-systems/il_3412_Giustinetti.pdf` | 2 | 21 | 21 | 21 | no/no |
| **Totale** | | **48** | **48** | **48** | **nessuno** |

**Interpretazione:** copertura del 100% delle *figure già riconosciute da Docling*, non prova di recall su tutte le figure reali del PDF né di correttezza dei ritagli o della semantica tattica. L'audit ha verificato i conteggi e la presenza dei manifest, non ha aperto singoli PNG. Prossimo passo: analisi isolata e riproducibile dei 48 ritagli, poi test di descrizione su un sottoinsieme, mantenendo intatti pipeline V2 e indice V4.

## Primo pilot vision Qwen — 2026-10-20

**Evidenza runtime riportata dall'utente:** `pilot_vision_existing_figure.py` ha interrogato `qwen3.5:9b` su `334_principi_Glerean.pdf`, `figure_index=1`, `figure_001_page_01.png` (pagina PDF 1), senza modificare V4. Tempo 24,14 s; `eval_count=64`; output conservato in `knowledge/experiments/vision_pilot/334_principi_Glerean_figure_001_1792530202.json` sulla VPS.

**Risposta del modello:** non identifica un diagramma calcistico, descrive una lettera S bianca su fondo blu. **Non verificata visivamente** l'immagine PNG in questa sessione: non dichiarare che la descrizione sia corretta. Il test conferma soltanto l'esecuzione dell'inferenza visiva, non la comprensione di schemi tattici. **Errore di disegno del pilot:** figura 1 scelta per indice, senza selezione semantica. Prossimo esperimento: selezione deterministica di figure su pagine tattiche, usando metadati preesistenti, poi confronto visivo/semantico con gold esclusivamente in valutazione.

## Candidati figure tattiche Glerean — 2026-10-20

**Evidenza VPS comunicata dall'utente:** output di `list_tactical_figure_candidates.py` sul manifest esistente di `334_principi_Glerean.pdf`, pagine PDF 7–13. Trovati 13 ritagli: pagina 7 indici 15–16; pagina 8 indici 17–19; pagina 9 indici 20–21; pagina 10 indici 22–23; pagina 11 indici 24–25; pagina 12 indice 26; pagina 13 indice 27. Le dimensioni sono circa 246–248 punti di larghezza, con altezze variabili 243–392 punti. Caption refs presenti per 11/13 (assenti 20 e 23).

**Candidato al prossimo pilot:** indice Docling 17, pagina PDF 8, presumibilmente figura stampata 12 sulla base dell'ordine delle figure; mappatura ancora da confermare visivamente. Test Qwen isolato, gold consultato soltanto dopo la generazione. Nessuna modifica a V4.
