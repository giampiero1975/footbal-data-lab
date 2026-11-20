# Prerequisiti isolamento Qwen27 — predisposizione bloccata

20 novembre 2026 · `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01` · `codex/tactical-state-contract-v1`

**BLOCCATO.** L'unica invocazione non interattiva della policy sudo già presente ha restituito `sudo: a password is required`, exit 1. Lo script privilegiato non è partito. L'account `football-qwen27`, il suo gruppo primario e `/var/lib/football-qwen27-isolation` risultano assenti sia prima sia dopo. Serve un'autorizzazione separata per l'esecuzione amministrativa delle due operazioni. Il Gate Linux e Qwen27 mmap restano **BLOCCATO**.

## Traccia

| Passaggio | Evidenza |
|---|---|
| Attività | Predisposizione di soli due prerequisiti del pilot esistente. Branch e HEAD GitHub iniziale `75f37955ded967219cf6e115d0aba40df0f361c6`. Working tree iniziale pulito. |
| Script | [`qwen27_isolation_prerequisites_01.py`](../operations/quality-first-pilot/qwen27_isolation_prerequisites_01.py), spedito via stdin dopo verifica host key storica. SHA-256 `ee6dfcf2878da5f908877ae1917be39ed23d9da131cbe403ef09f7854048af69`, confermato dal processo SSH non privilegiato. |
| Commit | `205c46ce7d1d3e4f7c73c4d4c0e0243c91ab3b21`, pubblicato e verificato prima dell'SSH. |
| Report | Questo documento con aggiornamenti contestuali a TODO e Experiment Register. [Invocazione, raw, exit e inventario SHA-256](qwen27-isolation-prerequisites-01/inventory.json). |
| Risultato | Diagnostica prima e dopo **ESEGUITO**. Sudo non interattivo rifiutato prima della predisposizione. Entrambi i prerequisiti assenti. |
| Decisione | Fermarsi senza retry o percorso alternativo. |
| Stato | Predisposizione, Gate Linux e Qwen27 mmap **BLOCCATO**. |

## Requisiti riconciliati

- Il [preflight 01](rag-v5-qwen27-ollama-isolation-linux-gate-01.md), TODO e registro riportano entrambi i prerequisiti mancanti. Il codice esige un UID diverso da root, `football` e `ollama`. Lo script prepara un account di sistema con gruppo primario omonimo, senza altri gruppi, con `/usr/sbin/nologin`, home assente e password bloccata. Nessuna ACL sui modelli, membership aggiuntiva o permesso sudo è parte di questa predisposizione. [Codice isolamento](../operations/quality-first-pilot/qwen27_isolation_01.py#L489) · [useradd](https://manpages.ubuntu.com/manpages/noble/man8/useradd.8.html) · [nologin](https://manpages.ubuntu.com/manpages/noble/man8/nologin.8.html).
- La directory prevista è `root:root` con modo `0755`, vuota, senza symlink, ACL aggiuntive o marker. I bit di lettura e attraversamento per `football` sono richiesti dal codice per il futuro `open.json`. La scrittura resta riservata a root. La custodia per singolo attempt usa directory private, separate dalla radice. Lo script rifiuta risorse preesistenti incompatibili. [Verifica lato supervisore](../operations/quality-first-pilot/qwen27_isolation_01.py#L509) · [Lettura lato worker](../operations/quality-first-pilot/paired_pilot_remote_01.py#L134).
- Nessuna esecuzione equivalente risultava conclusa. Il precedente `sudo -n -l` elencava il comando consentito dalla policy, ma non provava la possibilità di eseguirlo senza autenticazione. La richiesta corrente autorizzava solo la creazione delle due risorse. Non sono stati richiesti grant, password o modifiche a sudoers. La sintassi dello script e il singolo sito di creazione della directory sono stati controllati localmente prima del commit.

## Verifica dei servizi

Le due istantanee sono identiche per entrambi i servizi, inclusi `ActiveState=active`, `SubState=running`, cgroup, orario monotonic di attivazione, file unità e SHA-256. RAG PID `76562`, Ollama PID `188530`, con gli stessi ID di invocazione. I file unità e gli ID completi sono nel [raw](qwen27-isolation-prerequisites-01/stdout.json).

Nessuna predisposizione parziale, modifica a utenti o directory, unità transitoria, avvio Ollama dedicato, Gate, caricamento, POST o inferenza. Un solo SSH. Nessuna modifica a RAG, pannello, retrieval, corpus, modelli o configurazione di produzione. STOP.
