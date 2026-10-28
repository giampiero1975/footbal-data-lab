# FOOTBALL-DATA-LAB — remediation consolidata 2026-10-28

Ramo: `codex/tactical-state-contract-v1`  
Base riconciliata: `c912826`  
Ultima evidenza prima del presente report: `ad97869`

## Perimetro preservato

Non sono stati modificati o eseguiti: pannello HTML, VPS, servizi, deploy,
merge, modelli Ollama, indice Chroma, corpus, profilo API predefinito, flag
`--tactical-plan`, benchmark V10.1/V10.2, confronto thinking o chiamate esterne.
Le evidenze storiche e gli stati non equivalenti a certificazione sono rimasti
distinti.

## Risultati per fase

### 1. Contratto relazionale

- Codice/test: `0d69be6`; evidenze: `d51d3f6`.
- Chiusi sette difetti differenziali: espulsioni aggregate, cronologia non
  dipendente dalla serializzazione, rendering fail-closed globale, numeri nudi,
  archi invalidi, presenza completa e continuità mapping/assegnazioni.
- Stato: **VALIDATO** offline; non integrato nel runtime.

### 2. Qualità tattica relazionale

- Codice/test: `b4a5f64`; evidenze: `8e846e5`.
- Aggiunto audit per sottoproblema e per clausola su attore, fase, compito,
  spazio, trigger e finalità.
- Distinte validità dell'ID, pertinenza della fonte e verifica semantica.
- L'audit è osservabile e non bloccante; il gate legacy non cambia.
- Stato: **VALIDATO** offline; casi indipendenti runtime ancora da validare.

### 3. Feedback persistente

- Codice/test: `8102eb1`; evidenze: `6920e38`.
- Feedback recuperabile dopo riavvio, associato al job corretto e ammesso solo
  per job riusciti, senza secondo archivio.
- Stato: **VALIDATO** offline; raccolta non equivale ad apprendimento.

### 4. Sessioni e cronologia

- Codice/test: `863a943`; evidenze: `ad97869`.
- Payload legacy invariato; estensione opzionale con sessione, caso, fatti
  confermati e riferimenti a job riusciti.
- Domanda originale preservata; nessuna risposta generata viene promossa a
  fatto; recovery dai sidecar esistenti.
- Stato: backend **VALIDATO** offline; collegamento UI e deploy **DA FARE**.

## Regressione finale

- Tactical State Contract: **48/48 PASS**.
- Planner e audit relazionale: **25/25 PASS**.
- API, feedback e sessioni: **32/32 PASS**.
- Totale pertinente: **105/105 PASS**.
- Compilazione dei tre moduli modificati: **PASS**.
- `git diff --check`: **PASS**.

## Rischi e limiti residui

1. L'audit relazionale non è ancora validato su casi indipendenti completi di
   domanda, risposta, evidenze e versione runtime; non deve bloccare produzione.
2. Il Tactical State Contract non è ancora collegato alla generazione Qwen.
3. Il backend sessioni non è collegato al pannello e non è distribuito.
4. Nessun esito offline dimostra da solo un voto Coverciano medio >=26/30.
5. Prima di merge o deploy servono revisione del commit GitHub, collaudo
   isolato dell'integrazione e decisione esplicita del titolare.

## Decisione

La base di sviluppo è più affidabile e verificabile e soddisfa i criteri
offline dell'incarico. Nessun componente nuovo viene dichiarato
**INTEGRATO** o **CERTIFICATO**. La produzione è rimasta invariata.
