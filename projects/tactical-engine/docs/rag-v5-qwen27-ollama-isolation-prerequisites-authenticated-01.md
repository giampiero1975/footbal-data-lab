# Prerequisiti isolamento Qwen27 — predisposizione verificata

20 novembre 2026 · `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01` · `codex/tactical-state-contract-v1`

**IMPLEMENTATO e VALIDATO per i soli due prerequisiti.** Esistono l'account di servizio `football-qwen27` e la directory `/var/lib/football-qwen27-isolation`. Il Gate Linux e Qwen27 mmap restano **BLOCCATO**.

## Traccia

| Passaggio | Evidenza |
|---|---|
| Attività | Predisposizione dei due prerequisiti, nella stessa attività. Baseline del controllo iniziale `75f37955ded967219cf6e115d0aba40df0f361c6`. Riconciliati TODO, registro, [Gate preflight 01](rag-v5-qwen27-ollama-isolation-linux-gate-01.md) e [arresto iniziale](rag-v5-qwen27-ollama-isolation-prerequisites-01.md). La nuova autorizzazione esplicita riguarda l'autenticazione sudo esistente. |
| Script | [`qwen27_prerequisites_authenticated_01.py`](../operations/quality-first-pilot/qwen27_prerequisites_authenticated_01.py) applica lo [script di predisposizione](../operations/quality-first-pilot/qwen27_isolation_prerequisites_01.py) già congelato in `205c46c`. Sintassi del runner verificata prima dell'uso. |
| Commit | Runner pubblicato prima dell'unico SSH autenticato, `458061adfac0da75accdef5e35e175b6fb7689ba`. L'esito precedente, pubblicato con `4f812a2`, resta storico. |
| Report | Questo documento e aggiornamento contestuale a TODO e registro. [Invocazione, risultato, exit e inventario SHA-256](qwen27-isolation-prerequisites-authenticated-01/inventory.json). |
| Risultato | SSH ed esecuzione privilegiata exit 0. Prima dell'operazione account, gruppo e directory erano assenti. Entrambi i prerequisiti creati e verificati. |
| Decisione | Fermarsi dopo la predisposizione dei due prerequisiti. Gate e prova modello richiedono passaggi successivi separati. |
| Stato | Predisposizione **IMPLEMENTATO**. Verifica **ESEGUITO** e **VALIDATO** per account e directory. Gate Linux e Qwen27 mmap **BLOCCATO**. |

L'autenticazione ha usato la policy sudo già presente attraverso una sola connessione SSH con host key ED25519 verificata. La credenziale non figura nei comandi registrati, nel codice versionato o nelle evidenze. Nessuna modifica a sudoers. Lo SHA-256 dello script di predisposizione, `ee6dfcf2878da5f908877ae1917be39ed23d9da131cbe403ef09f7854048af69`, è stato verificato nel processo SSH e in quello privilegiato. Runner `63a75c3ee6ceb18463f057a350b9062eb0534c2d1b0812609a25ed51973c07d7`.

## Stato verificato sulla VPS

| Risorsa | Configurazione osservata |
|---|---|
| `football-qwen27` | Account di sistema UID `997`, distinto da root, `football` e `ollama`. Gruppo primario omonimo GID `987`, nessun gruppo supplementare. Shell `/usr/sbin/nologin`, password dell'account bloccata, home `/nonexistent` non creata. |
| `/var/lib/football-qwen27-isolation` | Directory reale `root:root`, modo `0755`, vuota, senza ACL aggiuntive e senza `open.json`. `football` può leggere e attraversare la directory e non può scriverci. Il codice richiede la lettura del futuro marker. [Verifica del percorso](../operations/quality-first-pilot/qwen27_isolation_01.py#L509). |
| Ollama di produzione | `active/running`, MainPID `188530`, stesso ID di invocazione, cgroup, istante di attivazione e SHA-256 del file unità prima e dopo. |
| RAG di produzione | `active/running`, MainPID `76562`, stesso ID di invocazione, cgroup, istante di attivazione e SHA-256 del file unità prima e dopo. |

La verifica è circoscritta a questi due prerequisiti. Nessuna ACL o accesso ai pesi aggiunto. Nessun Gate, unità transitoria, riavvio, istanza Ollama dedicata, caricamento modello, POST o inferenza. RAG, pannello, retrieval, corpus, modelli e configurazione di produzione invariati. STOP.
