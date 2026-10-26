# Groq — completamento Coverciano 100 e spalla tattica, Fase A

> **SUPERATO il 2026-10-26.** Questo documento conserva una fase storica
> tecnicamente valida offline ma fondata su un'interpretazione errata del
> flusso. Groq non completerà le 50 domande e i casi Gemini esistenti non
> costituiscono benchmark corrente. Stato e decisione autorevoli:
> `coverciano-examiner-copilot-reset-01.md`.

Data: 2026-10-26. Stato: **VALIDATO offline**. Nessuna chiamata API Groq,
generazione, risposta RAG, modifica della pipeline certificata o deploy.

## Riconciliazione

GitHub, TODO, registro, report Gemini/Groq e VPS sono stati confrontati. Stato
runtime verificato sulla VPS:

- 50/100 domande valide, cinque categorie complete: `costruzione`,
  `sviluppo_rifinitura`, `transizione_positiva`, `transizione_negativa`,
  `pressing`;
- cinque categorie mancanti: `blocco_difensivo`, `gestione_partita`,
  `palle_inattive`, `adattamenti_strutturali`, `metodologia_allenamento`;
- nessun file parziale del tentativo Gemini 503;
- nessuna risposta RAG del benchmark 100 ancora da produrre;
- G4 Groq precedente non e ripetuto: il nuovo contratto e tecnicamente distinto.

L'heartbeat Gemini ogni 30 minuti e stato eliminato per evitare che due
provider generino contemporaneamente gli stessi ID. I 50 casi Gemini restano
immutati e autorevoli.

## Percorso 1 — completamento delle 50 domande

Script `scripts/generate_coverciano_100_groq_completion_v1.py`:

- inventario fail-closed dei chunk esistenti;
- genera soltanto categorie mancanti, in due parti da cinque;
- conserva ID, categoria, difficolta e rubrica nascosta del contratto Gemini;
- Structured Output strict, controllo locale di ID, lunghezza, rubrica,
  duplicati esatti e quasi-duplicati;
- non sovrascrive file e rifiuta una categoria gia completa;
- payload minimizzato a prefissi di 160 caratteri e hash delle domande esistenti;
- merge categoria e manifest finale misto con provider per categoria;
- dry-run predefinito; rete soltanto con `--execute` e
  `--confirm-free-tier`; ledger e hard stop Free Tier separati.

## Percorso 2 — spalla tattica Groq

Script `scripts/groq_tactical_copilot_v2.py`, solo preflight nella Fase A:

1. revisione indipendente di domanda e risposta, senza evidenze, distinguendo
   `ERRORE_CERTO`, `POSSIBILE_LACUNA` e `SUGGERIMENTO_OPZIONALE`;
2. verifica documentale separata, classificando ogni finding come
   `SUPPORTATO`, `ULTERIORE_RETRIEVAL` o `NON_SUPPORTATO`.

La sintassi degli ID e delle etichette e validata dal software, non affidata al
modello. Il passaggio 2 deve coprire esattamente tutti i finding del passaggio 1
e puo usare soltanto label realmente presenti. Un suggerimento supportato senza
evidenza e respinto. Nessun percorso modifica automaticamente la risposta RAG.

## Evidenze offline

- Commit implementazione: `7596ba4`, fixture `f03b66d` e `9031661`, hardening
  quota/payload `2d034c7`.
- Suite combinata: **10/10 PASS**.
- Compilazione Python dei due script: PASS.
- Inventario reale VPS: 50 complete, 50 mancanti, categorie esatte sopra.
- Preflight generatore `blocco_difensivo` parte 1: PASS, API_REQUESTS=0.
- Preflight copilot su caso congelato: PASS, API_REQUESTS=0.
- Checkout operativo VPS, indici, Gemini, RAG e pipeline locked: invariati.

## Piano proposto prima di autorizzare chiamate

### Generazione delle 50 mancanti

- 10 chiamate totali: cinque categorie per due parti da cinque;
- una chiamata per esecuzione, almeno 60 secondi tra chiamate;
- modello `openai/gpt-oss-120b`, solo Free Tier;
- budget locale prudente 7.500 token/chiamata, massimo pianificato 75.000 token;
- checkpoint per parte, nessuna sovrascrittura; merge solo dopo 5+5 validi;
- merge finale soltanto a 100/100, con controllo duplicati e provider map;
- dati inviati: prompt, prefissi/hash delle 50 domande e nuove domande/rubriche;
  nessun PDF, risposta RAG, evidenza o credenziale nel payload.

### Validazione differenziale della spalla tattica

Prima del benchmark 100: tre casi congelati e distinti dal G4, scelti come
risposta forte, risposta con omissione nota e risposta con ambiguita tattica.
Due passaggi per caso, quindi 6 chiamate. Budget prudente massimo 7.500 token
per caso (22.500 complessivi). Valutazione manuale di falsi positivi, utilita,
specificita e supporto documentale. Nessuna rigenerazione RAG.

### Benchmark successivo, non ancora autorizzato

Solo dopo manifest 100/100, risposte RAG e validazione differenziale: 200
chiamate logiche (due per caso), checkpoint per caso, ripresa senza duplicati.
Stima prudente 600.000–750.000 token: almeno 3–4 giorni con hard stop di
200.000 token/giorno. Costo previsto zero sul Free Tier; nessun billing.

## Decisione

Fase A **VALIDATA offline**. Groq e IMPLEMENTATO come candidato per completare
le 50 domande e come copilot tattico, ma non ha ancora generato nuovi casi e
non e INTEGRATO. Attendere autorizzazione esplicita prima della prima chiamata
di generazione e, separatamente, prima dei tre casi differenziali.

