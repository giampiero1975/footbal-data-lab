# RD-TSC-V2-D3-S2-Q3-04-FORENSIC-01

## Attivita

Analisi forense esclusivamente offline del falso positivo `q3_04` osservato nel
primo runtime controllato S2. Nessuna inferenza, test o modifica applicativa e
stata eseguita.

## Evidenza sorgente e integrita

Artefatto autorevole:
`evaluation/tactical_semantic_support_s2_first_controlled_runtime_01.json`.

- SHA-256 verificato:
  `0768ca581b2bc6996d13f2b000600735663966ad9959695e11b54cd34c318afa`.
- Dataset: `eval/claim_fidelity_gold_v1.json`.
- Caso: `q3_04`.
- Fonte: `verticalizzazione_Bonacini`, pagina 2.
- Label umana congelata: `contradicted`.
- Label prodotta: `supported`.

Claim:

> La difesa bassa lascia molto spazio tra la linea difensiva e la porta.

Evidenza:

> La ricerca della verticalizzazione e della profondità del gioco è, per
> contro, di difficile attuazione quando si affrontano squadre che difendono
> basse e che lasciano avanzare gli avversari togliendo però spazio tra la linea
> difensiva e la porta.

Nel file UTF-8 originale sono presenti gli accenti italiani. Claim ed evidenza
nel dataset coincidono con quelli conservati nell'artefatto; i digest NFC
registrati sono rispettivamente `ea9d4276...` e `302019bb...`.

## Input ricostruito deterministicamente

Il bridge produce esattamente:

```text
S2_CLAIM_V1
claim_id=claim:q3_04
statement=La difesa bassa lascia molto spazio tra la linea difensiva e la porta.
conditions_json=[]
polarity=affirmed
bindings_json={}
```

Il judge concatena senza normalizzazioni o troncamenti l'istruzione NLI V2, la
sezione `FONTE` con l'evidenza sopra e la sezione `AFFERMAZIONE` con questa
proiezione. Prompt ricostruito: 1.480 caratteri, 1.494 byte UTF-8.

L'istruzione definisce `contradicted` quando la fonte afferma esplicitamente
qualcosa di incompatibile e richiede di controllare negazioni, direzione dei
confronti e quantificatori. Lo schema Pydantic richiede un oggetto JSON con il
solo campo obbligatorio `label`, limitato a `supported`, `contradicted` o
`insufficient`.

Parametri effettivi conservati: `qwen3.5:9b`, `temperature=0`, `num_ctx=4096`,
`num_predict=1024`, `think=false`, `stream=false`, timeout 180 secondi. Il judge
accetta il risultato soltanto con `done_reason=stop`, contenuto non vuoto e JSON
validabile.

## Ricostruzione del percorso

1. La fixture seleziona `q3_04` e verifica che il Gold sia `contradicted`.
2. Il runner copia senza modifica claim, evidenza, fonte e pagina dal dataset.
3. S1 produce legittimamente `not_evaluable`: la claim non e un estratto esatto
   dell'evidenza. Tale assessment resta invariato e non decide S2.
4. L'adapter passa statement ed evidenza esatta al bridge, con `conditions=[]`,
   `polarity=affirmed` e `bindings={}`.
5. Il bridge conserva l'ordine `judge_pair(claim, evidence)` e aggiunge soltanto
   metadati espliciti alla claim. Nessun termine tattico viene sostituito.
6. Il judge costruisce il prompt sopra, riceve JSON valido e restituisce
   `supported`.
7. Il bridge ammette la label canonica senza rimapparla; l'adapter la registra
   come `supported`. Non esistono fallback positivi.

Non emerge alcun difetto deterministico di serializzazione, ordine degli
argomenti, mapping o aggregazione. La risposta non e stata troncata secondo il
contratto del judge; il raw JSON Ollama e la catena di ragionamento non sono
conservati, quindi il motivo interno della scelta non e determinabile.

## Analisi semantica

Il soggetto logico e lo stesso: una squadra/difesa bassa. Anche lo spazio e lo
stesso: tra linea difensiva e porta. La relazione e invertita:

- evidenza: la difesa bassa **toglie spazio** in quella zona;
- claim: la difesa bassa **lascia molto spazio** nella stessa zona.

Non si tratta di semplice omissione, quantificatore non documentato o
insufficienza della fonte. `toglie spazio` e `lascia molto spazio` sono
predicazioni incompatibili nella medesima configurazione. L'avanzamento concesso
agli avversari non modifica questa conclusione: l'evidenza distingue proprio lo
spazio per avanzare dallo spazio dietro la linea difensiva.

La label umana `contradicted` e quindi difendibile rispetto all'estratto esatto.
Non vi sono inversioni soggetto/oggetto, condizioni perdute o ambiguita tali da
giustificare `supported`.

Evidenza storica concorrente: un controllo precedente sullo stesso nucleo
`low_block_wrong` aveva prodotto `insufficient` con NLI V2 e `supported` con V3.
Questo non prova il meccanismo interno, ma documenta una debolezza preesistente
nella gestione della direzione spaziale/contrasto lessicale.

## Classificazione causale

**B — Errore semantico del judge.**

Confidenza alta sull'attribuzione del risultato: input, ordine, integrita e
mapping sono verificati, mentre la label e incompatibile con una contraddizione
esplicita. Confidenza bassa sulla causa cognitiva interna: non sono conservati
raw response o rationale semantica e non e lecito inferire se Qwen sia stato
fuorviato dalla sovrapposizione lessicale, dai metadati della claim o dalla forma
verbale `togliendo`.

## Unico intervento minimo proposto

Versionare, senza sostituire il giudice corrente, una rettifica minima del
contratto NLI che renda obbligatorio confrontare la direzione della relazione
`soggetto → proprieta/spazio` e specifichi in forma generale che predicati
inversi sulla stessa relazione devono essere `contradicted`, anche senza una
negazione grammaticale esplicita. La proposta dovra essere valutata offline sul
solo controllo congelato interessato e sulle regressioni direttamente collegate
prima di qualunque nuova inferenza; nessuna modifica o rerun e autorizzato da
questo report.

## Risultato, decisione e stato

- Analisi forense: **ESEGUITO**.
- Integrita e ricostruzione deterministica: **VALIDATO** offline.
- Causa B nel perimetro osservabile: **VALIDATO** con i limiti sopra dichiarati.
- Correzione del contratto: **DA FARE** previa autorizzazione distinta.
- Affidabilita semantica, Gate, integrazione e certificazione: **BLOCCATO**.
