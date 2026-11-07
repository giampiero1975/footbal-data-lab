# FOOTBALL-DATA-LAB — Implementazione accesso diagnostico sudo controllato

Attività: `RD-FOOTBALL-VPS-SUDO-DIAGNOSTIC-IMPLEMENTATION-01`

Data: 2026-11-07

## Baseline e perimetro

- branch: `codex/tactical-state-contract-v1`;
- HEAD iniziale locale/remoto:
  `3941e392718d68186e7de3d4ae8202023618ac31`;
- working tree iniziale pulito;
- rotazione SSH v2 già **VALIDATO**, non riaperta;
- nessuna modifica a SSH, sshd, servizi VPS, gruppi o pipeline;
- singola sessione amministrativa protetta: password sudo inserita direttamente
  dal titolare nel terminale remoto, mai acquisita da Codex.

## Stato iniziale e preflight

Helper e regola dedicata erano assenti, inclusi symlink dangling.

Directory `/usr`, `/usr/local`, `/usr/local/sbin`, `/etc` e
`/etc/sudoers.d`: `root:root`, modalità `0755`. Dipendenze assolute verificate:
`journalctl`, `timeout`, `gawk` (destinazione reale del symlink `awk`), `stat`,
`sha256sum`, `visudo`, `install` e Bash sono root-owned e non modificabili da
`football`.

Prima dell'installazione `sudo -n -l` terminava con exit `1`.

## Artefatti installati

### Helper

- percorso: `/usr/local/sbin/football-rag-journal-export`;
- tipo: file regolare;
- proprietà/modalità: `root:root`, `0755`;
- SHA-256:
  `391b46d74eb61b0deaaea3b3b63860de33d38845efa8eec3289a76259892ea82`.

Contratto implementato:

- zero argomenti; qualunque argomento termina con exit `64`;
- sole query fisse `ollama.service` e kernel;
- finestra fissa `2026-11-07 12:19:00–12:25:30 Europe/Rome`;
- percorsi assoluti e ambiente controllato;
- pager disabilitato e nessuna lettura di stdin;
- nessun `eval`, file temporaneo o destinazione scelta dall'utente;
- limite di 30 secondi per query e 4 MiB per sezione;
- exit distinti per troncamento (`74`), timeout/incompletezza (`75`), errore
  journal (`70`) e filtro (`71`);
- output parziale accompagnato da exit non zero e mai promosso a completo.

### Sudoers

- percorso: `/etc/sudoers.d/football-rag-journal-export`;
- tipo: file regolare;
- proprietà/modalità: `root:root`, `0440`;
- SHA-256:
  `0631df75df5a2046b75174925e0f538a39ea385d87f8b895e0d22067c450772a`;
- `visudo -cf` sul candidato: PASS;
- `visudo -c` dopo installazione: PASS.

Regola effettiva:

```sudoers
Cmnd_Alias FOOTBALL_RAG_DIAG = /usr/local/sbin/football-rag-journal-export ""
football ALL=(root) NOPASSWD: FOOTBALL_RAG_DIAG
Defaults!FOOTBALL_RAG_DIAG use_pty
```

L'installazione root è stata atomica. Il manifest SHA-256 di `/etc/sudoers` e
dei file sudoers preesistenti, escludendo soltanto la nuova regola, è risultato
identico prima e dopo. Nessun privilegio preesistente è stato alterato.

## Verifiche di accettazione

| Controllo | Evidenza | Esito |
|---|---|---|
| Sintassi Bash | `/bin/bash -n` exit 0 | PASS |
| Regola candidata | `visudo -cf` exit 0 | PASS |
| Esecuzione senza argomenti | `sudo -n`, exit 0 | PASS |
| Output completo | 43.542 byte, 367 righe, due sezioni, stderr 0 byte | PASS |
| Integrità output test | SHA-256 `7e3446e82ab9df07bbdbed4bd8c5463688d3458810cfecb19fa73076db7dc002`; file eliminato dopo il controllo | PASS |
| Argomento aggiuntivo | sudo exit 1 | PASS, rifiutato |
| Altra unità/intervallo/file | non rappresentabili senza argomenti | PASS strutturale |
| Ambiente e pager manipolati | `PATH=/tmp`, pager falsi; helper exit 0 senza interazione | PASS |
| Altro comando sudo (`id`) | exit 1 | PASS, rifiutato |
| Regola elencata | `sudo -n -l`, regola esatta presente | PASS |
| `NOPASSWD: ALL` | assente | PASS |
| Helper e regola | hash, owner, mode e file type conformi | PASS |
| Timeout/troncamento | wrapper e rami exit 74/75 presenti | PASS statico; non forzato su log reali |
| Incompletezza/errori | diagnostica esplicita ed exit non zero | PASS statico |
| `eval`, `mktemp`, lettura stdin | zero occorrenze operative | PASS |
| Configurazioni sudo preesistenti | manifest esclusa nuova regola invariato | PASS |

I log grezzi del test non sono stati mostrati né versionati. I file temporanei
di output sono stati rimossi dopo hash, dimensione e conteggio.

## Rollback

Disponibile e non eseguito, perché tutti i controlli sono PASS:

1. sessione amministrativa protetta;
2. rimozione esatta di
   `/etc/sudoers.d/football-rag-journal-export`;
3. `visudo -c` obbligatorio;
4. rimozione esatta di
   `/usr/local/sbin/football-rag-journal-export`;
5. verifica che `sudo -n` torni allo stato precedente.

Poiché entrambi i target erano assenti prima dell'installazione, non esistono
file preesistenti da ripristinare. Lo script d'installazione disponeva di trap
selettivo per rimuovere soltanto gli artefatti creati in caso di errore.

## Closeout documentale e disponibilità del sorgente

Nel repository sono disponibili contratto, hash, metadati, risultati runtime e
controlli statici registrati al momento dell'installazione. Il testo sorgente
esatto dell'helper installato non è invece versionato né presente tra gli
artefatti locali verificabili di questo closeout.

Il solo SHA-256 non prova il contenuto e non consente di ricostruirlo. In base al
divieto di accesso VPS, non è stata eseguita una nuova lettura dell'helper e non
è stata ripetuta la revisione statica. I controlli statici e runtime elencati
sopra restano evidenze storiche già registrate, non una nuova verifica svolta in
questa sessione. Una revisione statica indipendente del sorgente esatto è quindi
**non verificabile** con gli artefatti Git attualmente disponibili; ciò non
modifica gli esiti runtime già acquisiti né amplia il perimetro validato.

## Decisione e stati

- helper diagnostico: **IMPLEMENTATO**;
- regola sudoers dedicata: **IMPLEMENTATO**;
- verifiche pertinenti: **ESEGUITO**;
- minimo privilegio, integrità, fail-closed e accesso senza password al solo
  helper: **VALIDATO** nel perimetro storico fisso;
- accesso amministrativo generale: non concesso;
- certificazione complessiva VPS: non attribuita;
- futura diagnostica generale o modifica dell'helper: **BLOCCATO** fino a nuova
  progettazione e autorizzazione.
