# RAG V5 — Gate di revisione indipendente del candidato v2

Data: 2026-10-23. Stato: DA FARE.

## Artefatti immutabili da esaminare

- Manifest: `evaluation/rag_v5_independent_candidate_v2.json`
- SHA-256 atteso: `f0d36bc5b35ddcfd42bfef234db2380db6a684a9b81fb9cd19ab75bea81755c0`
- Protocollo: `docs/rag-v5-quality-9of10-validation-protocol-v1.md`
- Wrapper read-only: `scripts/run_rag_v5_locked_candidate_v2.py`
- Baseline V4, indice Chroma e manifest originali: non modificare.

## Revisione prima della generazione

Il revisore indipendente non deve aver scritto le domande o corretto il prompt sulla base delle loro risposte. Verificare per ciascuno dei dieci casi, senza eseguire il modello:

1. Fonte originale, pagina e testo effettivo rispetto a `mandatory_claims`.
2. Che `forbidden_claims` descrivano davvero un errore e non una lettura legittima della fonte.
3. Che la domanda sia risolvibile, o richieda astensione, secondo le fonti ammissibili.
4. Assenza di ambiguita tattiche, inversione dei soggetti e confusione tra allenamento e partita.
5. Indipendenza dal set diagnostico e assenza di esposizione precedente del quesito al tuning.

Casi: `fresh_01`–`fresh_10`. Il caso `fresh_10` richiede verifica di entrambe le fonti; `fresh_03` distingue modulo fisso e cambio in gara; `fresh_01` distingue giudizio qualitativo e prova statistica.

## Verbale richiesto

Per ciascun caso: ID, PASS/REVISIONE, pagina verificata, rilievo specifico, identificativo del revisore e data. Per il freeze: identita del revisore, approvazione esplicita delle dieci rubriche, hash del manifest e fingerprint della configurazione runtime (modello, prompt, embedding, reranker, collection, commit). Non compilare approvazioni in assenza di evidenze.

## Decisione

Solo dopo approvazione indipendente e verifica della configurazione: predisporre un manifest congelato versionato, preservando il candidato originale, poi eseguire una sola volta il gate 10/10 read-only. Il wrapper attuale rifiuta correttamente `--approved-gold` sul candidato non congelato. Nessuna generazione o certificazione anticipata.

## Requisiti di resilienza del revisore ausiliario (23 ottobre 2026)

- **REQ-GEM-01 — Non bloccante:** l'indisponibilita di Gemini (inclusi HTTP 503, timeout e limiti di quota) non interrompe il flusso operativo RAG. Registrare causa, data, modello e revisione saltata; proseguire con le fasi indipendenti dal revisore. Nessun PASS implicito e nessuna certificazione senza evidenze.
- **REQ-GEM-02 — Prova preliminare:** prima della revisione, effettuare un controllo leggero della raggiungibilita del servizio e del modello. Se non disponibile, saltare la revisione e proseguire. Il controllo di rete non garantisce la successiva inferenza; una chiamata generateContent di prova consumerebbe quota e va contabilizzata. Evitare richieste diagnostiche ridondanti e retry illimitati.

Questi requisiti sono **DA FARE** a livello di implementazione e test; non modificano retroattivamente i report. Il gate di approvazione indipendente resta obbligatorio per il freeze, anche quando il flusso operativo non viene bloccato.
