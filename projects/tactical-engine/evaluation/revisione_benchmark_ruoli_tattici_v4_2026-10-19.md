# Revisione benchmark ruoli tattici V4 — 2026-10-19

## Evidenza osservata
Report VPS: `projects/tactical-engine/benchmark_ruoli_tattici_v4.json`, fornito dall'utente. Modello `qwen3.5:9b`; 10 affermazioni sintetiche riferite a GLEREAN-C018.

Risultato con etichette originali: **8/10**. T01, T02, T04, T05, T06, T07, T09 e T10 concordano; T03 e T08 non concordano.

### T03 — falso negativo critico
- Atteso: `contraddizione`; previsto: `coerente`.
- Frase: «Attaccanti, difensori e centrocampisti si posizionano tutti per ricevere palla negli spazi laterali e centrali, allineati ai difensori avversari».
- Fonte: difensori e centrocampisti **gestiscono la palla**; attaccanti **si mettono nella condizione di riceverla** negli spazi laterali e centrali in linea con i difensori avversari.
- Interpretazione: estensione indebita del ruolo di ricezione ai reparti che nella fonte sono descritti nella funzione di gestione. Il modello non riconosce questa alterazione.

### T08 — ambiguità nell'etichettatura del benchmark
- Atteso originale: `non_determinabile`; previsto: `coerente`.
- Frase: «Gli attaccanti cercano spazi per ricevere palla».
- La frase è compatibile con la fonte ma meno specifica: la fonte non è insufficiente per stabilire la compatibilità, bensì la frase omette dettagli. Secondo una tassonomia **compatibilità vs contraddizione**, `coerente` è plausibilmente corretto; secondo una tassonomia **completezza del claim**, sarebbe `parziale`.
- Non cambiare l'etichetta del test storico. Eventuale rietichettatura solo in una versione successiva con rubriche distinte e motivazione.

## Interpretazione
- 8/10 è l'accordo **con le etichette iniziali**, non accuratezza generale del sistema.
- 9/10 è solo una **stima controfattuale** qualora T08 venga rietichettato `coerente` in un benchmark futuro; non è un nuovo risultato misurato.
- Il problema T03 è prioritario perché replica l'errore tattico osservato nel benchmark V4-bis.
- Il test è limitato a un brano e a dieci casi sintetici: non giustifica promozione in produzione.

## Prossima progettazione
Separare due dimensioni di giudizio: (1) `compatibile` / `contraddittorio` / `insufficiente_evidenza`; (2) `completo` / `parziale`. Testare prima l'attribuzione strutturata di coppie **reparto → azione**, quindi il verdetto, senza basarsi sulla mera sovrapposizione lessicale. Conservare configurazione Chroma V4 invariata.

## Documentazione tecnica
- https://docs.ollama.com/capabilities/structured-outputs
- https://docs.ollama.com/api/chat
