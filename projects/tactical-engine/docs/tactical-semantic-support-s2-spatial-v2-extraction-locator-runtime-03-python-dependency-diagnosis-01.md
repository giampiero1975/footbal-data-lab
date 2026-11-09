# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03 — diagnosi dipendenza Python

## Attività e perimetro

Diagnosi read-only del blocco documentale
`E_PYTHON_DEPENDENCY_MISSING_PYDANTIC`, senza installazioni, modifiche a
virtualenv, wrapper, staging o produzione e senza runtime, trasporti o
inferenze.

- data: 2026-11-09;
- branch: `codex/tactical-state-contract-v1`;
- HEAD GitHub iniziale: `b9786bd207c02ea9af6fa4ef273676d0f189cb29`;
- baseline applicativa: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- host/utente verificati: `football-data-lab.localdomain` / `football`.

TODO, Experiment Register e report
`tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-03-execution-01.md`
sono stati riconciliati prima della diagnosi.

## Interpreti e pacchetti disponibili

### Python di sistema selezionato dal wrapper

- percorso dichiarato nel wrapper, riga 15: `/usr/bin/python3`;
- percorso reale: `/usr/bin/python3.12`;
- versione: Python 3.12.3;
- `sys.prefix` e `sys.base_prefix`: `/usr`, quindi non è una virtualenv;
- `pydantic`: assente, nessuna versione o origine disponibile;
- `requests`: presente, versione 2.31.0, origine
  `/usr/lib/python3/dist-packages/requests/__init__.py`.

Il wrapper riusa la variabile assoluta `PYTHON` in tutti i processi Python
incorporati, alle righe 471, 524, 736, 805 e 1390. Una modifica del solo
`PATH` non può quindi selezionare un interprete differente.

### Virtualenv operativa esistente

È presente, senza essere stata modificata:

`/opt/football-data-lab/projects/tactical-engine/.venv`

- interprete: Python 3.12.3;
- `sys.prefix` distinto da `/usr`, virtualenv effettiva;
- `pydantic`: 2.14.1;
- `requests`: 2.34.2;
- `include-system-site-packages=false`;
- `pyvenv.cfg` dichiara base `/usr/bin` e Python 3.12.3.

La virtualenv appartiene al checkout operativo. Il wrapper approvato non la
usa. Sostituire l'interprete assoluto richiederebbe una modifica del wrapper e
legherebbe il tentativo allo stato dell'ambiente operativo; tale modifica non
è necessaria né autorizzata.

## Dipendenze effettive del percorso Extraction Locator

La baseline non contiene `requirements*.txt`, `pyproject.toml`, `Pipfile`,
`environment.yml` o manifest equivalenti che vincolino versioni Python per
questo percorso.

Il grafo diretto dei tre moduli caricati dal runner è:

- `shadow_nli_spatial_relations_v2_inference.py`: `json`, `urllib.error`,
  `urllib.request` e i due moduli Spatial V2 locali;
- `v5_tactical_semantic_support_s2_spatial_v2_extraction.py`: `hashlib`,
  `json` e il validatore Spatial V2 locale;
- `v5_tactical_semantic_support_s2_spatial_v2.py`: `unicodedata`.

Non risultano import di `pydantic`, `requests`, import dinamici o subprocessi
Python in questi tre file. `pydantic` è invece una dipendenza del modulo
storico distinto `shadow_nli_v2_inference.py`, non del modulo Extraction
Locator `shadow_nli_spatial_relations_v2_inference.py` usato dalla baseline.

Con `PYTHONDONTWRITEBYTECODE=1` e `PYTHONPATH` limitato agli script della
baseline, `/usr/bin/python3` ha importato con successo tutti e tre i moduli
effettivi: `RELEVANT_IMPORTS=PASS`. Non è stata contattata alcuna rete e non è
stato eseguito alcun test applicativo.

## Diagnosi causale

1. **Dipendenza realmente assente:** `pydantic` è assente da
   `/usr/bin/python3`.
2. **Dipendenza presente altrove:** `pydantic 2.14.1` è presente nella
   virtualenv operativa.
3. **Incompatibilità di versione:** non dimostrata e non applicabile al
   percorso autorizzato, che non importa `pydantic`.
4. **Selezione dell'interprete:** il wrapper seleziona intenzionalmente e in
   modo assoluto `/usr/bin/python3`; `PATH` non può cambiarlo.
5. **Causa diretta del blocco:** il preflight esterno precedente richiedeva
   impropriamente l'import di `pydantic` e `requests` insieme ai moduli
   applicativi. Il primo import ha prodotto `ModuleNotFoundError` prima che
   fossero verificati separatamente gli import realmente necessari. Non è un
   difetto del runner Extraction Locator né una dipendenza mancante del suo
   grafo effettivo.

## Correzione minima proposta, non applicata

Per un'eventuale nuova autorizzazione è sufficiente correggere la procedura di
preflight esterna, senza modificare wrapper, staging o ambiente:

- mantenere l'interprete assoluto `/usr/bin/python3` previsto dal wrapper;
- impostare `PYTHONDONTWRITEBYTECODE=1` e il `PYTHONPATH` degli script dello
  staging;
- verificare esclusivamente l'import dei tre moduli effettivamente caricati;
- non imporre `pydantic` o `requests` come prerequisiti di questo percorso.

Non sono proposte installazioni e non è necessario riusare la virtualenv
operativa. Un futuro runtime resta subordinato a una nuova autorizzazione e al
resto del preflight approvato.

## Risultato, decisione e stato

- diagnosi: **ESEGUITO**;
- assenza di `pydantic` nel Python di sistema: **VALIDATO**;
- presenza di `pydantic 2.14.1` nella virtualenv operativa: **VALIDATO**;
- importabilità del percorso Extraction Locator con `/usr/bin/python3`:
  **VALIDATO** nel solo controllo read-only;
- correzione proposta: procedura preflight esterna, **DA FARE** previa nuova
  autorizzazione;
- runtime-03, Gate, integrazione e certificazione: **BLOCCATO**.

Flusso: Attività = diagnosi dipendenza; Script = comandi read-only; Commit =
esclusivamente documentale; Report = questo documento; Risultato = falso
prerequisito identificato; Decisione = nessuna installazione o modifica;
Stato = diagnosi **VALIDATO**, runtime **BLOCCATO**.
