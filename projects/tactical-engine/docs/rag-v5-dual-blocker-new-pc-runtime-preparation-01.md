# RAG V5 Dual Blocker — nuovo PC e preparazione runtime

Attività: `RD-RAG-V5-DUAL-BLOCKER-NEW-PC-PREPARATION-01`.
Data: 2026-11-10, Europe/Rome.

## Attività

Verifica del nuovo PC, riconciliazione GitHub e preparazione documentale della
sola futura prova `q3_04`. Nessuna inferenza, esecuzione wrapper, connessione
VPS, copia remota, modifica applicativa o suite offline in questa sessione.

## Script e commit

Comandi locali Git, inventario dei soli nomi file SSH e analisi statica con
stdlib Python; nessun modulo applicativo importato. Nessuno script runtime
creato. Pubblicazione limitata a questo report, TODO e Experiment Register.
Il commit documentale è identificabile con:

```text
git log -1 --format=fuller -- projects/tactical-engine/docs/rag-v5-dual-blocker-new-pc-runtime-preparation-01.md
```

Baseline applicativa congelata, distinta dal successivo commit documentale:
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.

## Report — nuovo PC e Git

| Verifica | Evidenza osservata |
|---|---|
| Repository | `C:\laragon\www\footbal-data-lab` |
| Git | `2.42.0.windows.2`, funzionante |
| origin fetch/push | `https://github.com/giampiero1975/footbal-data-lab.git` |
| Branch | `codex/tactical-state-contract-v1` |
| HEAD locale/remoto dopo fetch | `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d` |
| Divergenza iniziale | `0/0`, nessun commit locale non pubblicato sul branch |
| Working tree iniziale | pulito, nessun file non tracciato segnalato |
| Worktree registrati | uno, repository sopra indicato |

Il fast-forward di 111 commit da `3fa3a18` a `13814c2` era già stato eseguito
nel passaggio precedente della stessa chat. Il nuovo fetch non ha rilevato
ulteriori avanzamenti: nessun secondo pull necessario, reset, clean o merge.

### Connessione VPS

OpenSSH è presente in `C:\WINDOWS\System32\OpenSSH\ssh.exe`. Il sandbox ha
inizialmente negato la lettura di `.ssh`; l'inventario successivo autorizzato
ha verificato `C:\Users\giamp\.ssh` e i soli nomi/dimensioni dei file.

Sono presenti `football_data_lab`, `id_ed25519`, `id_rsa`, i corrispondenti
file pubblici, `known_hosts` e `known_hosts.old`. Non è presente il file
utente `config`; non è presente la chiave documentata
`codex-football-vps-ed25519-v2`. Anche
`C:\ProgramData\ssh\ssh_config` non risulta presente.

La configurazione verificata sul precedente PC nel report
`football-vps-ssh-key-rotation-phase-01.md` non è quindi disponibile qui:
alias `football-vps`, selezione dell'identità v2 e relativi parametri non
sono attestati. Le altre chiavi non sono state lette, selezionate né provate;
la loro presenza non dimostra autorizzazione o autenticazione VPS. Il contenuto
di `known_hosts` e la corrispondenza della host key non sono stati verificati.

Connessioni tentate: zero. Accessibilità VPS attuale non verificata;
readiness SSH **BLOCCATO**. Occorre rendere disponibile una configurazione e
un'identità autorizzate, verificando host key e fingerprint mediante il
canale già approvato. Nessuna configurazione o credenziale è stata inventata,
generata, copiata o modificata.

## Riconciliazione delle evidenze

Letti TODO, Experiment Register e i report:

- `tactical-semantic-support-s2-rag-v5-dual-blocker-causal-review-01.md`;
- `tactical-semantic-support-s2-rag-v5-dual-blocker-offline-remediation-01.md`;
- `tactical-semantic-support-s2-rag-v5-dual-blocker-independent-review-01.md`;
- `tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-03-run-01.md`;
- report runtime-03 di materializzazione/esecuzione e preparazione staging.

La patch tecnica `56a7b72135595e99a98ff2fb5b1bcc3d6a0c9ebf` è antenata
della baseline scelta. Nessun ulteriore commit negli script fra patch e
baseline. Sono già registrati 16/16 extraction/locator e 21/21 Spatial V2,
totale 37/37 PASS; revisione indipendente senza difetti bloccanti. Queste
sono evidenze precedenti, non test eseguiti sul nuovo PC.

Il confronto Git conferma il validatore finale identico a runtime-03.
Il confronto statico AST conferma identici `_occurrences`,
`_localize_fragments` e `_materialize_relation`; non è un replay o una suite.
`materialize_extraction()` invoca ora `extraction_semantic_errors()` dopo lo
shape check e prima del locator. Il precontrollo riusa `AXIS_VALUES` e
`_comparison_errors()` del validatore finale, senza correggere label o valori.

### Identità da verificare nello staging futuro

Hash sui byte dei blob Git LF, non su una riscrittura PowerShell o CRLF:

| Componente in `projects/tactical-engine/` | Blob Git | SHA-256 blob |
|---|---|---|
| `scripts/shadow_nli_spatial_relations_v2_inference.py` | `8ac93d07341e1079ee3ca6ff98327a8391b7ab5f` | `b6f30e76a2ccf98a4c027beff7fd2e36128da42797d2fcbbe144dc3e6089a9c6` |
| `scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py` | `1a64827b26fb30758773049eedeb342a2bb826b2` | `a1592fa491fe20590e2e85e35b5c4397365c8bdc9dbc898bc9d9e0c2d8b73aef` |
| `scripts/v5_tactical_semantic_support_s2_spatial_v2.py` | `0a8b92acbda67afeaee4bc057f89729e11e20ab5` | `06e071b50c69683c8ed69257a238c6fe53b00cc60ad589ec61ab1100b59a3b46` |
| `eval/claim_fidelity_gold_v1.json` | `4523eb746d666fdfb161c5d38d8db31f12e99b92` | `8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c` |

Il blob dataset è identico alla baseline runtime-03; il digest riportato per
esso è quello canonico storico, da ricontrollare sui byte remoti prima della
prova. Non si riutilizza il vecchio digest Windows CRLF.

## Piano operativo futuro — non eseguito

### Identità, differenza tecnica e isolamento

Identificativo proposto, non materializzato né autorizzato:
`spatial-v2-extraction-locator-q3-04-runtime-04`.

La prova differisce da runtime-03 (`db3ad66...`) esclusivamente per il codice
dual blocker: prompt side-specific, descrizioni dello schema e controllo
semantico prima del locator. Questo delta giustifica una nuova prova generativa;
nessun risultato post-patch equivalente è documentato. Non giustifica ripetere
i 37 test offline o le analisi forensi concluse.

Staging proposto:
`/home/football/.local/share/football-data-lab/staging/spatial-v2-dual-blocker-13814c2`.
Deve essere un clone indipendente, detached alla baseline completa indicata,
con `.git` interna, nessun alternate, nessun symlink, index e working tree
puliti. Una destinazione già esistente o discordante impone arresto, senza
sovrascriverla. Non usare `git worktree` del checkout operativo.

Prima di qualsiasi preparazione remota, fotografare HEAD, stato Git e common
directory del checkout operativo e degli staging storici pertinenti; verificare
gli stessi valori dopo. Non modificare `/opt/football-data-lab` né riutilizzare
lo staging `spatial-v2-extraction-locator-db3ad66`. La preparazione dello staging
e qualunque trasferimento richiedono autorizzazione separata.

### Riuso del wrapper e preparazioni mancanti

Riutilizzare il wrapper runtime-03 già verificato, senza eseguirlo:
`/home/football/.local/share/football-data-lab/runtime-wrappers/spatial-v2-extraction-locator-q3-04-runtime-03-approved.sh`.
Identità storica: 45.964 byte, SHA-256
`ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57`.

Il wrapper non è versionato nel repository; il vecchio percorso locale
`C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\...` non costituisce un
artefatto disponibile attestato sul nuovo PC. Con accesso autorizzato occorre
prima leggerne il sorgente e verificarne l'hash. Nessun wrapper alternativo è
stato ricostruito a memoria e nessun adattamento byte-per-byte è dichiarato.

Delta ammesso nella futura copia, da revisionare prima dell'esecuzione:

1. nuovo attempt ID, percorsi esclusivi e staging alla baseline aggiornata;
2. aggiornamento delle identità attese dei soli componenti modificati;
3. preservazione di lock comune, supervisione, trasporto singolo e finalizzazione;
4. conservazione di schema extraction effettivo, esito del precontrollo e
   diagnostica `details`, senza una seconda esecuzione del modello;
5. nuova dimensione, SHA-256 e diff esplicito del wrapper adattato, senza
   riutilizzare l'hash del wrapper storico.

Devono essere confermati dal sorgente precedente request completa, numero di
token, timeout applicativo e timeout supervisore; non basta dedurli dai default.
Il codice corrente offre `temperature=0`, `num_ctx=4096`, `think=false`,
`stream=false`, `extraction_locator=True` e timeout opt-in 360 secondi.
Ogni differenza aggiuntiva nei parametri reali deve essere motivata e approvata.
Non aggiungere dipendenze `pydantic`/`requests` al preflight dei tre moduli:
il precedente blocco era un prerequisito estraneo, già diagnosticato.

### Preflight immediato richiesto

Dopo autorizzazione delle preparazioni, prima di autorizzare l'invocazione:

1. attestare staging, quattro blob e hash, dataset e caso `q3_04` immutati;
2. verificare il wrapper adattato e la sua selezione del nuovo staging;
3. confrontare prompt e schema effettivi con la baseline, verificando che
   shape → `extraction_semantic_errors()` → locator → validatore sia il percorso usato;
4. attestare `/usr/bin/python3` e import dei soli tre moduli in ambiente senza
   bytecode; nessuna installazione o import del motore RAG;
5. verificare tramite endpoint non generativi modello `qwen3.5:9b`, digest
   `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`,
   e versione Ollama rispetto alla provenance runtime-03; mancata identità
   richiede arresto e riconciliazione;
6. controllare assenza di artefatti con nuovo attempt ID, concorrenza pertinente
   e modelli caricati, spazio disponibile e integrità del lock comune;
7. riesaminare l'intero wrapper e gli inventari prima di chiedere autorizzazione
   per una sola invocazione. Non eseguire il wrapper per fare preflight.

Il preflight non deve creare lock, artefatti o staging finché le relative
scritture non siano autorizzate. Le evidenze VPS storiche non attestano lo
stato corrente; tutte le verifiche remote sopra elencate restano **DA FARE**.

### Unica futura invocazione e artefatti

Una sola chiamata di trasporto e una sola generazione per il solo `q3_04`;
zero retry, repair, fallback o ripresa automatica. Un arresto o un risultato
non valutabile consuma il tentativo invocato e richiede decisione separata.
Nessuna prova guardia o campagna è implicitamente autorizzata.

Directory proposta, con creazione esclusiva e fuori dai checkout:
`/home/football/.local/share/football-data-lab/runtime-artifacts/spatial-v2-extraction-locator-q3-04-runtime-04`.

Conservare baseline, status prima/dopo, identità wrapper/modello/interprete,
input immutato, prompt, schema effettivo, request payload, raw response,
extraction, precontrollo con reason code e dettagli, localization, witness e
validation quando raggiunti, result/decision, contatori trasporto/generazione,
tempi, exit code, log supervisore e stato finale. Se una fase non è raggiunta,
registrare esplicitamente il motivo dell'assenza, senza fabbricare artefatti.

Riutilizzare la finalizzazione già verificata: `hashes.sha256`,
`attempt_state.sha256`, `hashes.sha256.digest`, verifica integrale e flag
`finalization_complete`; distinguere esito applicativo, wrapper e supervisore.
Inventariare tutti i file effettivamente prodotti. `promotion_authorized=false`
resta obbligatorio in ogni percorso. Conservare separatamente label proposta,
label derivata dal validatore e Gold, senza correzioni o promozioni.

### Criteri della futura prova

| Dimensione | Criterio |
|---|---|
| Tecnica | risposta completa, una generazione, zero retry/repair/fallback, finalizzazione e hash verificabili |
| Localizzazione | tutti i frammenti unici nel rispettivo lato, nessun trasferimento automatico |
| Extraction | shape e precontrollo semantico senza errori |
| Witness | validatore finale `technical_status=valid`, nessun errore strutturale |
| Semantica `q3_04` | referente spaziale corretto condiviso; valori spaziali incompatibili; label derivata `contradicted` concordante con Gold |

`not_evaluable` non soddisfa il criterio semantico. Un wrapper riuscito o un
fail-closed corretto non dimostrano accuratezza generativa. Anche una prova
positiva sul solo `q3_04` non dimostra generalizzazione né certifica il sistema.
Non introdurre regole lessicali specifiche per questo caso.

## Risultato → Decisione → Stato

Git locale riconciliato; preparazione documentale **ESEGUITO**. Proprietà della
patch già **VALIDATO** offline, senza riesecuzione. Accesso VPS su questo PC
**BLOCCATO** per configurazione/identità documentata non disponibile; stato
remoto attuale non verificato. Recupero/verifica wrapper, adattamento e staging
aggiornato **DA FARE**. Nessuno staging post-patch pronto è attestato.

Prossima azione: predisporre l'accesso SSH autorizzato sul nuovo PC e verificare
read-only sorgente del wrapper e stato VPS. Successivamente occorre
autorizzazione distinta per trasferimenti e creazione staging; solo dopo
wrapper revisionato e preflight, autorizzazione per l'unica inferenza.

Accuratezza generativa e problema delle contraddizioni, runtime, Gate,
integrazione e certificazione restano **BLOCCATO**. Nessuna preparazione
documentale autorizza questi passaggi.
