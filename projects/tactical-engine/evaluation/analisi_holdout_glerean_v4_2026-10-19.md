# Analisi holdout Glerean V4 — 2026-10-19

## Report osservato
File: `projects/tactical-engine/benchmark_holdout_glerean_v4.json`, fornito dall'utente.
Modello: `qwen3.5:9b`. Metodo: `holdout_two_axes_with_relation_extraction`.
12 frasi sintetiche tratte dalle evidenze testuali P1, P2, V1, V3, V4 del gold dataset.

- Fedelta' 9/12 = 75%; errori H07, H09, H10.
- Copertura 7/12 = 58,3%; disaccordi H01, H04, H09, H11, H12.
- Numeri = accordo con etichette predefinite, non accuratezza del RAG in produzione.

## Errori di fedelta' prioritari
- **H07 / V4**: inverte ampiezza/profondita' di attaccanti centrali e laterali; giudice `coerente` anziche' `contraddittorio`. L'estrazione `source_roles` ripete l'attribuzione invertita della frase di test, mentre `statement_roles` contiene il contenuto della fonte: probabile confusione dei due testi.
- **H09 / P1**: affermazione compatibile con la fonte (sicurezza prima della giocata rischiosa), giudice `contraddittorio`. Il ragionamento interpreta la fonte nel senso opposto.
- **H10 / P1**: affermazione incompatibile con la fonte (giocata immediata rischiosa), giudice `coerente`. Il ragionamento interpreta la fonte nel senso opposto.

## Disaccordi sulla copertura
- **H01**: giudice richiede la sfumatura «ricerca costante», non esplicitata nella frase; da definire se essenziale nel gold.
- **H04**: giudice introduce un requisito temporale aggiuntivo non chiaramente giustificato dal frammento di evidenza.
- **H09**: deriva anche dal fraintendimento del principio P1; la motivazione penalizza «guadagnare tempo».
- **H11/H12**: giudice richiede che l'attaccante sia esplicitamente «in possesso»; discutibile se la condizione sia implicita nel contesto, da risolvere nella rubrica.

## Decisioni
1. Non promuovere il verificatore personalizzato in produzione.
2. Non modificare collection Chroma, embedding, reranker o RAG V4 sulla base di questi test del giudice.
3. Prima di ulteriore sviluppo personalizzato, confrontare framework consolidati Ragas e DeepEval, con documentazione ufficiale e verifica compatibilita' locale.
4. Validare anche l'estrazione intermedia e separare esplicitamente fonte da affermazione.
5. Preservare tutti i report originali e le etichette iniziali.

## Riferimenti
- Gold dataset: `evaluation/gold_glerean_principi_v1.json`
- Ollama structured outputs: https://docs.ollama.com/capabilities/structured-outputs
- Ragas: https://docs.ragas.io/
- DeepEval: https://deepeval.com/docs/getting-started
