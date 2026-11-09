# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03 — esecuzione singola

## Attività e identità

Il 2026-11-09 è stata autorizzata una sola invocazione diagnostica del wrapper
`spatial-v2-extraction-locator-q3-04-runtime-03`, subordinata al PASS del
preflight corretto.

- branch: `codex/tactical-state-contract-v1`;
- HEAD GitHub iniziale: `85953234789ba1707918cf41e85c31d06fe8bfa4`;
- baseline applicativa: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- caso: `q3_04`, Gold `contradicted`;
- wrapper remoto esclusivo:
  `/home/football/.local/share/football-data-lab/runtime-wrappers/spatial-v2-extraction-locator-q3-04-runtime-03-approved.sh`;
- dimensione wrapper: 45.964 byte;
- SHA-256 wrapper:
  `ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57`.

TODO, Experiment Register e report precedenti sono stati riconciliati. Non
risultava una precedente invocazione runtime-03; working tree locale e branch
GitHub erano puliti e allineati.

## Preflight corretto

Il preflight esterno ha mantenuto i controlli approvati e ha limitato la
verifica Python ai tre moduli realmente caricati, con `/usr/bin/python3`,
`PYTHONDONTWRITEBYTECODE=1` e `PYTHONPATH` dello staging. Non ha richiesto
`pydantic` o `requests` come prerequisiti autonomi.

Esito: PASS.

- staging presente, non symlink, detached a `db3ad66...`;
- index e working tree puliti, status SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- common directory interna e alternates assenti;
- quattro blob Git e dataset conformi;
- dataset SHA-256
  `8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c`;
- wrapper remoto conforme;
- tre moduli Extraction Locator importabili con il Python assoluto previsto;
- modello `qwen3.5:9b` disponibile con digest
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
- zero modelli caricati prima del tentativo;
- lock acquisibile, artefatti runtime-03 assenti e nessuna concorrenza
  pertinente osservata;
- spazio disponibile: 40.528.096 KiB.

## Unica invocazione

Il wrapper è stato letto dal percorso remoto verificato e invocato esattamente
una volta. Non sono stati effettuati retry, repair, fallback o seconde
invocazioni.

- invocazioni wrapper: 1;
- chiamate di trasporto: 1;
- generazioni Qwen: 1;
- risposta ricevuta: sì;
- generazione completata: sì;
- durata registrata: 142,340508 secondi;
- processo generativo supervisionato: exit 0;
- wrapper: exit 80;
- stato finale: `completed_fail_closed`;
- reason code: `E_EXTRACTION_LOCALIZATION_NOT_UNIQUE`;
- `promotion_authorized=false`.

## Valutazione distinta

### Completamento generativo

PASS tecnico nel singolo tentativo: risposta JSON di tipo oggetto ricevuta,
generazione completata e nessun timeout o errore di trasporto.

### Extraction e localizzazione

L'extraction JSON è presente e supera il parsing/shape richiesto dal percorso.
Il locator ha prodotto 11 record: 10 frammenti sono stati localizzati una sola
volta sul lato assegnato; un frammento è risultato assente dal lato claim:

- campo:
  `claim_relation.reference.selected_fragments[0]`;
- frammento selezionato:
  `squadre che difendono basse e che lasciano avanzare gli avversari togliendo però spazio tra la linea difensiva e la porta`;
- lato assegnato: `claim`;
- occorrenze: 0;
- risultato: `missing`.

Il frammento corrisponde invece a testo presente nell'evidence. Il contratto
side-bound vieta di ricollocarlo automaticamente sul lato opposto. La
localizzazione è quindi `not_evaluable` e il reason code aggregato resta
`E_EXTRACTION_LOCALIZATION_NOT_UNIQUE`.

### Witness e validità strutturale

Il witness non è stato materializzato e `validation.json` non è stato prodotto.
La validità strutturale del witness è non valutabile, non un PASS.

### Correttezza semantica

L'extraction proposta da Qwen contiene label `supported`, mentre il Gold del
caso è `contradicted`. Poiché la localizzazione è fallita e non esiste un
witness validato, `observed_label=null` e `semantic_match=null`. Non è
corretto classificare il caso come semplice discordanza semantica verificata:
il risultato autorevole è `not_evaluable`.

### Fail-closed e idoneità Gate

Il comportamento fail-closed è osservato correttamente: nessun witness o
validation artefatto, nessuna label promossa, exit wrapper 80 e
`promotion_authorized=false`. Il singolo risultato non è idoneo a un Gate e
non dimostra integrazione o certificazione.

## Artefatti e integrità

Directory:
`/home/football/.local/share/football-data-lab/runtime-artifacts/spatial-v2-extraction-locator-q3-04-runtime-03`.

`sha256sum -c` ha verificato integralmente `hashes.sha256`,
`attempt_state.sha256` e `hashes.sha256.digest`. Non esiste
`finalization_errors.log`; `finalization_complete=true`. Lo staging è rimasto
alla baseline richiesta e pulito dopo l'esecuzione.

| Artefatto | SHA-256 |
|---|---|
| `attempt_progress.json` | `896bfae2631b5790b2ec7adecc2dc9231bf5fb9555ee179994524647f3f6682d` |
| `attempt_state.json` | `23bd2b3fdfccd618899330ae0506debc834efd3e4c918e07b521b601f557478b` |
| `attempt_state.sha256` | `209127f7068636c5e47f271ac7710ef23cc495e961cff9bfdd6318e864706832` |
| `config.json` | `49c84c060a310061af62f54c20d1b058eabcfbd8d3038db1a9025cb8f64380fd` |
| `decision.json` | `fd9026b1babfab7320291d8b75e8812ad8c00a3b44a8f28220c13e2d72fe406b` |
| `extraction.json` | `caeb9d256461ebc75e3aaf9b61f9cddbd6aa00a3e464405e9ab80fce6ee32c10` |
| `generation_record.json` | `f00e9bd3fb58fb26097003250e99f8cab4fc8cfd88e7fb124639cc48c64084a7` |
| `git_head_after.txt` | `9bb2e1204175a779dc56a6a5321405f210d7bf5e179d904949d1ae331dd79731` |
| `git_head_before.txt` | `9bb2e1204175a779dc56a6a5321405f210d7bf5e179d904949d1ae331dd79731` |
| `git_status_after.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `git_status_before.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `hashes.sha256` | `110a288d9cf9ee9e6133121c481cb6baee1031c65d10f9911034546c27cd2dfd` |
| `hashes.sha256.digest` | `0317eaac9ecf7e56444eb3267ea4c4c4c2528ecdef6d4e31d2d2be1087437996` |
| `input.json` | `6927b40d3a9973fa4697df47d652eab80fc1a5ff5c92b09571c27f9234a875e5` |
| `ollama_ps_after.json` | `81b00a1bcb751cfb4b71768a4ce4471b426ce033caf158592580f3debc587237` |
| `ollama_ps_before.json` | `a6fe9ec6e26a38d99fca418b69826e0238b7a2bb319ff05eb153a6fcfd1fa28d` |
| `ollama_tags_before.json` | `4602ecdbd1d2e59b3c521e14756bf0fa13154bd0e4af9e2b1ce90377e6983814` |
| `process_snapshot_before.txt` | `b217f41182f0afa8e36363adee9035851833dc84630c93d36b3c38274d16c3df` |
| `prompt.txt` | `1def1a03c3c399658a89e8b7c7d4cdfb8a0bfb1ce43acc41c187a08349bec87f` |
| `provenance.json` | `4e1c547fc72d724cf0e287d2033cd41f7dd866933350733d5aaf147fe2b5f769` |
| `raw_response.json` | `f1a28ba8f5910ba665de25c036734a7c98cbd757c971b3e5270905688a1e9034` |
| `request_payload.json` | `8670e9a944ac4f1bbe13f5dba51f199b33285462b38e2dde61daf2c1e06ab2ec` |
| `result.json` | `7b1cfcb923b9008d9781e1a5b1a9ef5b9c4ce320472d69f0f98a89c4192d43fe` |
| `stdout.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `supervised_exit_code.txt` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `time_stderr.log` | `3dbfafc6076e6303456bf0dad2f77bad5b0f62a35f1c990cff0ea1d48cec3a8f` |
| `transport_state.json` | `085f332d7a1a54c45e56ef68b19b949f29e34e2b8343d4729ffe2dd009ff0bb0` |

## Decisione e stato

L'unica invocazione autorizzata è consumata. Il completamento tecnico e il
fail-closed del singolo caso sono **VALIDATO**; localizzazione, witness,
validità strutturale e correttezza semantica restano **BLOCCATO** o non
valutabili. Nessun runtime-04 o secondo tentativo è autorizzato.

Flusso: Attività = runtime-03 singolo; Script = wrapper remoto conforme;
Commit = esclusivamente documentale; Report = questo documento; Risultato =
generazione completa ma localization fail-closed; Decisione = nessuna
promozione o retry; Stato = tentativo **ESEGUITO**, completamento tecnico e
fail-closed **VALIDATO**, Gate, integrazione e certificazione **BLOCCATO**.
