# Groq Free reviewer — G0/G1 offline

Data: 2026-10-25. Perimetro: sola ipotesi parallela opt-in. Nessuna chiamata
Groq, chiave, configurazione runtime, deploy, modifica Gemini o pipeline locked.

## G0 — Riconciliazione

- GitHub era quattro commit avanti rispetto al checkout locale; fast-forward a
  `a045246` senza conflitti.
- La proposta `groq-free-reviewer-proposal-01.md`, TODO e registro concordavano
  su Groq come opzione futura, non sostituzione di Gemini.
- Stato VPS read-only: HEAD `93a427e`, servizio RAG attivo, cinque categorie
  Gemini complete e quattro file parte; avanzamento consolidato 50/100.
- Nessun adapter Groq presente sulla VPS (`GROQ_RUNTIME=ABSENT`).
- Contratto reviewer identificato in `review_runtime_series_gemini_v1.py`:
  stesso prompt congelato, ID brevi, score 0–10, PASS/REVISIONE coerente,
  strengths, structural_errors, evidence_issues, minimum_fix e limiti serie.
- Differenza tecnica: provider OpenAI-compatible con JSON Schema strict,
  policy HTTP/quote e ledger separati. Nessun test Groq precedente aveva
  esercitato codice riproducibile del repository.

**Risultato G0: VALIDATO.** La proposta era arretrata a 40/100 ed e stata
riconciliata a 50/100; certificazione locked, Gemini e dati runtime invariati.

## G1 — Compatibilita offline

Implementati, senza collegamento al servizio:

- `scripts/groq_free_reviewer_v1.py`, dry-run predefinito e `--execute`
  esplicito protetto da conferma Free Tier e `GROQ_API_KEY`;
- riuso diretto del prompt e dei validatori Gemini esistenti;
- request OpenAI-compatible `n=1`, non streaming, JSON Schema `strict:true`,
  tutti i campi required e `additionalProperties:false`;
- gate fail-closed sugli ID, score/verdetto e citazioni RAG in ingresso;
- policy 200 accept, 429/5xx retry con `retry-after`, 400/401/403 stop;
- hard stop locale richieste/token e funzione di ripresa che salta ID conclusi;
- report con provider/modello/hash e divieto di sovrascrittura.

Suite `tests/test_groq_free_reviewer_v1.py`: **6/6 PASS** in directory
temporanea isolata, API_REQUESTS=0. Coperti schema/prompt, 200, 429, 503,
400/401/403, ID mismatch, score/verdetto invalidi, citazioni invalide, quota e
ripresa dopo interruzione. Compilazione Python superata.

## Criticita

1. Nessuna prova che `openai/gpt-oss-120b` sia disponibile o qualitativamente
   adeguato nell'organizzazione del titolare: richiede G2/G3 autorizzati.
2. Le quote documentate sono organizzative e vanno verificate nel pannello;
   100 revisioni richiederebbero almeno 2–3 giorni nelle ipotesi correnti.
3. Structured JSON garantisce forma, non competenza tattica; G4 deve confrontare
   un caso congelato senza assimilare automaticamente voti Gemini e Groq.
4. L'adapter non e collegato ad API/pannello/scheduler e non e deployato: stato
   corretto **IMPLEMENTATO e VALIDATO offline**, non INTEGRATO.

## Decisione

Chiudere G0 e G1. Fermarsi prima di G2/G3 come richiesto. Non creare chiavi,
non chiamare Groq, non modificare Gemini e non effettuare deploy. Una futura
probe richiede autorizzazione esplicita e configurazione privata della chiave.

## Appendice — Probe autorizzata successiva

Il titolare ha successivamente fornito e autorizzato la prova di una chiave
etichettata `football-data-lab`. La chiave non e stata salvata su disco, Git,
env del servizio o pannello. Una prima richiesta e stata rifiutata prima
dell'inferenza per escaping JSON del comando; la probe corretta successiva ha
raggiunto `openai/gpt-oss-120b` e restituito un completion ID valido, nessun
errore, 78 token prompt, 16 completion (14 reasoning), 94 totali, queue time
0,208 s e model time 0,036 s. Il contenuto finale era vuoto per il tetto minimo
di 16 token assorbito dal ragionamento.

Risultato: autenticazione, endpoint, modello e telemetria **ESEGUITI**; qualita,
JSON Schema strict e revisione tattica non VALIDATI. Nessun deploy o modifica
runtime. Poiche la chiave e stata incollata in chat, deve essere revocata e
rigenerata prima di qualsiasi uso futuro.

