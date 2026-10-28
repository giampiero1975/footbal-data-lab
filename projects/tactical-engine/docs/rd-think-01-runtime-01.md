# RD-THINK-01 — confronto runtime thinking off/on

Data: 2026-10-28. Stato: **ESEGUITO**. Nessun deploy o cambio del default produttivo.

## Obiettivo e metodo

Verificare se la modalità thinking di Qwen migliori autonomamente una risposta
applicativa, senza confondere l'effetto con retrieval, prompt, fonti o modello.
È stato riusato il caso congelato V10.2 `case_10.json`: domanda, piano tattico,
prompt e otto estratti identici. Il retrieval non è stato rieseguito.

Rubrica fissata prima dell'esecuzione: correttezza tattica 35%, copertura 25%,
coerenza squadra/ruolo/lato/fase 20%, supporto documentale 15%, vincoli 5%.
Non è una valutazione ufficiale FIGC/Coverciano.

## Runtime verificato

- commit VPS: `1a80fe0c6261b10f748a36c2b4fd96e8e2253971`;
- Ollama `0.40.5`;
- modello `qwen3.5:9b`, Q4_K_M, digest
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
- capability locale: completion, vision, tools, thinking;
- contesto dichiarato dal modello: 262144; contesto usato dalla prova: 8192;
- temperatura 0, `num_predict=4096`, timeout 900 s per chiamata.

Il digest coincide con il tag ufficiale `qwen3.5:9b-q4_K_M` consultato il
2026-10-28. La pagina ufficiale Ollama dichiara la capability thinking per la
famiglia Qwen 3.5.

## Pannello e memoria conversazionale

Il percorso pannello → `/v1/query` → `run_rag_v5_query.py` trasmette una sola
stringa `question`. Ogni job è indipendente: risposte precedenti, rettifiche e
scenario originario non vengono aggiunti automaticamente al nuovo prompt.
Quindi una domanda di seguito abbreviata raggiunge Qwen senza il caso iniziale.
Questo spiega almeno parte del restringimento osservato in RD-002-R1; non prova
che tutti gli errori precedenti abbiano la stessa causa.

## Risultati misurati

| Modalità | Stadio | Tempo | Token generati | Arresto | Output |
|---|---|---:|---:|---|---|
| thinking off | prima generazione | 204,932 s | 647 | stop | 348 parole |
| thinking on | prima generazione | 546,484 s | 4096 | length | 0 parole; 15.945 caratteri thinking |
| thinking on | repair | 552,773 s | 4096 | length | 0 parole; 16.004 caratteri thinking |

Thinking off non ha richiesto repair secondo il gate deterministico. Thinking
on ha consumato l'intero budget nel solo ragionamento interno sia alla prima
generazione sia al repair, senza produrre una risposta valutabile. Il confronto
qualitativo off/on non è quindi possibile: l'esito on è troncato due volte.

## Audit sostanziale della risposta thinking off

Il gate tecnico la dichiara completa, ma la lettura tattica rileva un errore
grave nella trasformazione 4-3-3 → 3-5-2. La risposta afferma nello stesso
passaggio che un'ala «esce per diventare terzino», che un centrale «entra come
ala», che «un difensore centrale scende a centrocampista» e poi che l'ala esce
e un centrale entra «nel reparto di mezzocampo». Le proposizioni sono tra loro
incompatibili e non descrivono una sostituzione o rotazione praticabile.

Ulteriori rilievi:

- copre formalmente tutti i sottopunti, ma diverse assegnazioni operative sono
  incoerenti;
- il comando live richiama un «difensore uscito» non stabilito dalla struttura;
- attribuisce automaticamente sicurezza e riduzione dell'ansia senza un nesso
  documentale sufficiente;
- assegna a un terzino alzato la copertura delle fasce per evitare contropiedi,
  confondendo occupazione offensiva e protezione preventiva;
- citazioni presenti non rendono supportate le trasformazioni contraddittorie.

Valutazione diagnostica interna: **non raggiunge 26/30**. Non viene inventato un
voto ufficiale; il difetto decisivo è la correttezza tattica, non la lunghezza o
lo stile. Il risultato dimostra inoltre che il gate V10.2 può produrre un falso
positivo sostanziale.

## Decisione

1. `think:false` resta il default: non è dimostrato causa degli errori e
   `think:true` è inutilizzabile con budget 4096/hardware corrente.
2. Nessun nuovo benchmark, deploy o cambio di modello viene autorizzato da
   questo singolo caso.
3. Il prossimo intervento strettamente giustificato è correggere il controllo
   relazionale sulle trasformazioni di sistema: entrata/uscita, ruolo iniziale,
   ruolo finale e struttura devono formare una sequenza non contraddittoria.
4. Le domande di follow-up nel pannello devono reincludere esplicitamente lo
   scenario oppure, in un'attività separata, introdurre sessioni conversazionali
   tracciate. Non assumere memoria che oggi non esiste.
5. Un eventuale nuovo test thinking richiede un budget separato per ragionamento
   e risposta o una modalità deliberativa limitata supportata e documentata;
   non è giustificato ripetere ora la stessa prova.

## Tracciamento

Attività → verifica causale RD-THINK-01.  
Script → `scripts/compare_frozen_thinking_rd01.py`.  
Commit → commit contestuale a report/TODO/registro.  
Report → questo documento e `evaluation/rd-think-01-result.json`.  
Risultato → off produce output ma contiene contraddizioni; on esaurisce il
budget senza output.  
Decisione → mantenere off, correggere gate relazionale e memoria/contesto dei
follow-up in attività distinte.  
Stato → **ESEGUITO**, non VALIDATO per qualità >=26/30.
