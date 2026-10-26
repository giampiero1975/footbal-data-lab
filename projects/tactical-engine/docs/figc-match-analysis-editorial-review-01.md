# Revisione editoriale candidati FIGC match analysis

Data: 2026-10-26. Stato: **ESEGUITO**; registrazione runtime **DA FARE**.

Sono stati ispezionati testo, indice e pagine rappresentative dei tre candidati,
senza indicizzazione o inferenze LLM.

- Di Camillo: `candidate_tactical`. Contiene un caso studio del Rayo Vallecano
  con strutture, costruzione, catene esterne, mezzi spazi e pressione alta.
- Rausse: `candidate_tactical`. Contiene un caso studio del RB Leipzig con
  sezioni esplicite su fase offensiva, costruzione, sviluppo/rifinitura e fase
  difensiva.
- Venturini: `exclude_tactical`. È uno studio utile di analytics e metriche,
  ma non una fonte primaria per principi/correttivi tattici del RAG corrente.

È stata rilevata un'incongruenza: il catalogo marca Venturini come scaricato,
ma il file locale indicato non è presente. L'URL FIGC ufficiale è ancora
accessibile e il PDF è stato verificato soltanto in area temporanea. La
decisione editoriale non deve mascherare questa anomalia operativa.

Le decisioni sono congelate in `figc-match-analysis-decisions-v1.json` e
possono essere applicate atomicamente con
`apply_figc_editorial_decisions_v1.py`. Nessuna promozione in Chroma è inclusa.
