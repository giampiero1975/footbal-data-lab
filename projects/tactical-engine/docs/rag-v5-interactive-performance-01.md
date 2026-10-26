# RAG V5 — profilo interattivo e latenza

Data: 2026-10-26. Stato iniziale: **IMPLEMENTATO**, runtime **DA FARE**.

## Diagnosi senza nuova inferenza

Il report esistente del job `ad41e872d5f44a66a7626f8429f30e5e` misura
173,34 s end-to-end. La telemetria Ollama attribuisce 165,92 s alla generazione:

| fase | durata |
|---|---:|
| caricamento modello | 10,40 s |
| valutazione prompt, 2.242 token | 75,90 s |
| generazione, 638 token | 79,58 s |
| resto della pipeline | circa 7,42 s |

I due test prestazionali storici confermano la diagnosi: 193,54 s a freddo e
161,09 s a caldo. Retrieval e reranking non sono il collo di bottiglia
principale. La VPS ha 6 CPU, 15 GiB RAM e il solo modello generativo installato
è `qwen3.5:9b` da 6,6 GB.

## Differenza tecnica autorizzante

I test storici hanno mantenuto il modello 9B. Il nuovo candidato è un profilo
applicativo esplicito, reversibile e separato dal locked:

- modello `qwen3.5:4b`, variante ufficiale Ollama;
- contesto 4096 invece di 8192;
- massimo 450 token in uscita;
- sei evidenze, con eventuale confronto successivo a quattro solo se necessario;
- `keep_alive=30m` per eliminare caricamenti ripetuti.

Il codice espone modello, contesto e keep-alive come opzioni; i default locked
restano `qwen3.5:9b`, 8192 e nessun keep-alive esplicito. La modifica non tocca
collection, embedding, reranker, routing o gate delle citazioni.

## Criteri

Un solo scenario differenziale già noto verrà rieseguito dopo il deploy del
candidato, perché modello e parametri sono tecnicamente diversi. Gate:

- job completo e arresto naturale;
- almeno una citazione e zero citazioni invalide;
- indice 6410/157 invariato;
- risposta tatticamente utilizzabile dal copilot;
- target aspirazionale 30–45 s, soglia provvisoria massima 60 s.

Il profilo non sarà promosso soltanto in base alla velocità. Se perde i nuclei
tattici essenziali resta **ESEGUITO** ma non `VALIDATO`.
