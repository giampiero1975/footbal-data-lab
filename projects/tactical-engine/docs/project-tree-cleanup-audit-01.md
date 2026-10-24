# PROJECT-TREE-CLEANUP-AUDIT-01

Data: 2026-10-24. Stato: VALIDATO per la pulizia dei componenti rigenerabili;
ESEGUITO per l'inventario iniziale.

## Attività

Rilevare l'alberatura reale del progetto e della VPS, classificare i principali
consumi e rimuovere soltanto componenti dimostrati inutilizzati e recuperabili.

## Script

Nessuno. Audit read-only con Git, `du`, `find`, `grep`, `ps`, `systemctl`, cron,
`lsof`, inventario Ollama e fingerprint V5. Rimozione limitata a quattro
percorsi cache/lock Hugging Face Alibaba verificati.

## Commit

`957f350` — `docs: audit project tree and retire Alibaba cache`.

## Alberatura sintetica

```text
/opt/football-data-lab                         3.6G
├── .git                                      23M
├── .github                                   16K
├── datasets                                  12K
├── knowledge                                510M  [mantenere]
├── shared                                     4K
└── projects                                  3.1G
    └── tactical-engine
        ├── .venv                            2.3G  [attivo]
        ├── .venv-ragas-eval                 766M  [candidato]
        ├── docs                             548K
        ├── eval                             248K
        ├── evaluation                       2.5M
        ├── experiments                        8K
        ├── scripts                           1.7M
        └── tests                              24K
```

Il repository contiene 199 file tracciati in `scripts/`, 91 in `docs/`, 29 in
`evaluation/`, 7 in `eval/` e 3 in `tests/`. Sulla VPS risultano 77 percorsi
non tracciati, in larga parte ambienti virtuali e report: non sono stati
cancellati perché richiedono classificazione puntuale.

## Verifica Alibaba

- Cache rilevate:
  `models--Alibaba-NLP--gte-multilingual-reranker-base` e
  `models--Alibaba-NLP--new-impl`, con le rispettive directory `.locks`.
- Nessun riferimento operativo nel repository, fuori dalle note di audit.
- Nessun riferimento in processi, servizi systemd, cron o unit file.
- Nessun file aperto nella cache al momento della rimozione.
- Le occorrenze residue erano soltanto documentazione e `.bash_history`.

Le quattro directory cache/lock sono state rimosse. Il precedente valore
`600M` proveniva da `du -L`, che dereferenziava link verso storage condiviso;
le directory eliminate occupavano circa 152K fisici. Non è corretto dichiarare
600 MB liberati. Lo storage Hugging Face condiviso non è stato toccato.

Rollback: un eventuale componente futuro può riscaricare il modello da
Hugging Face; non sono stati rimossi codice, configurazioni, indici o sorgenti.

## Verifica post-rimozione

- nessun percorso Alibaba residuo nella cache Hugging Face;
- mMARCO, BGE e Surya ancora presenti;
- runner V5 SHA-256
  `bafb61c30474e4946ba0a8d91b733363e3e7830fda0cb196cc37c5ed2130780e`;
- collection V5 principale 5319 record e candidata esercizi 34;
- fingerprint read-only concluso e file temporanei rimossi.

## Classificazione iniziale

| Componente | Decisione | Motivo |
|---|---|---|
| Qwen3 Embedding e Qwen3.5 9B | mantenere | runtime V5 certificato |
| mMARCO | mantenere | reranker del profilo certificato |
| BGE | mantenere per ora | baseline/rollback ancora documentata |
| Surya/Docling | mantenere | due processi Surya attivi dalla `.venv` |
| `.venv` | mantenere | ambiente runtime attivo, 2.3G |
| `.venv-ragas-eval` | candidato | 766M; decidere insieme al gate NLI/Ragas |
| `knowledge/` | mantenere | sorgenti, non artefatti rigenerabili |
| 77 percorsi non tracciati | classificare | includono report/evidenze e ambienti |
| cache Alibaba | rimuovere | inutilizzata e recuperabile; rimozione eseguita |

## Decisione

Pulizia fase 1 conclusa limitatamente ad Alibaba. Prima di altre rimozioni:
classificare i 199 file di script, i 77 percorsi non tracciati e le collection
storiche. Non eliminare `.venv`, knowledge base, benchmark, indici o modelli
attivi.

## Pulizia fase 2

Controlli preliminari:

- `.venv-ragas-eval` senza file aperti e fuori dal runtime certificato;
- cache pip interamente rigenerabile;
- processi Surya con `PPID 1`, attivi da otto giorni, senza connessioni client
  e privi di unità systemd associata;
- BGE 2.3G e Qwen3-Reranker 1.2G assenti dai file del runtime V5 corrente;
- mMARCO, modelli Docling/Surya, Qwen Ollama e `.venv` operativo preservati.

Rimozioni eseguite:

- `.venv-ragas-eval`: 766M;
- cache pip utente: 259M;
- cache Hugging Face `BAAI/bge-reranker-v2-m3`: 2.3G;
- cache Hugging Face `Qwen/Qwen3-Reranker-0.6B`: 1.2G;
- due blob condivisi non referenziati: 629M, rimossi con `hf cache prune`;
- due processi Surya orfani arrestati ordinatamente, liberando circa 565M RAM.

Lo strumento ufficiale `hf cache rm` ha gestito riferimenti e blob dei modelli;
non sono stati rimossi manualmente file dal pool condiviso. BGE, Qwen3-Reranker
e Ragas restano ripristinabili tramite download/reinstallazione. I server Surya
restano installati nella `.venv` e possono essere riavviati per una futura
ingestion.

## Risultato finale

- filesystem root: 27G usati / 31G liberi / 48% prima; 19G usati / 39G liberi
  / 33% dopo;
- repository VPS: da 3.6G a 2.9G;
- cache Hugging Face: da 5.0G a 1.1G;
- swap: da circa 1.5G occupati a 4.8M;
- processi Surya non più attivi;
- import runtime riusciti: Chroma 1.5.9, sentence-transformers 6.1.0,
  torch 2.6.0+cpu;
- collection V5 ancora 5319/34;
- hash runner ancora
  `bafb61c30474e4946ba0a8d91b733363e3e7830fda0cb196cc37c5ed2130780e`.

Test, script e report JSON non sono stati cancellati: occupano pochi MB e sono
necessari per riproducibilità, audit e ricostruzione delle decisioni.
