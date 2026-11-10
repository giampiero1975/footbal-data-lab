# RAG V5 — closeout R1 numeric/literal

Attività: `RD-RAG-V5-REMEDIATION-A-R1-NUMERIC-LITERAL-01`.
Data: 2026-11-10, Europe/Rome.

## Attività → Script → Commit

Corretto soltanto R1 della revisione indipendente
`rag-v5-dual-blocker-remediation-a-independent-review-01.md`: il nuovo handoff
ora descrive il caller effettivo, senza cambiare la semantica dei quantificatori.

Riconciliazione prima delle modifiche: TODO e Experiment Register ufficiali,
report e fatti statici della revisione, diff remediation A `0ea62c0` rispetto
al parent, caller e helper finali. Branch `codex/tactical-state-contract-v1`,
origin `https://github.com/giampiero1975/footbal-data-lab.git`, HEAD iniziale
locale/GitHub `c00af6da364f3849f23d5d300e3c0e75b9d6a574`, tree pulito.
I documenti locali letti corrispondono al medesimo commit confermato su GitHub.
R1 presente e non ancora risolto; nessuna divergenza o patch duplicata.

Script applicativo: solo la costruzione delle istruzioni in
`scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py:358`.
Nuovo controllo: `tests/test_v5_spatial_extraction_numeric_literal_r1.py`.
Prima di eseguirlo registrata nella sua docstring la differenza tecnica:
i sedici controlli storici coprivano rappresentazioni di slot, non il ramo
caller fra due numeric con literal diversi. Nessuna suite storica ripetuta.

Commit tecnico: `5bfa4897e93d5d8edef0bc79371aa36b1b1409ae`.
Due soli file: una sostituzione di frase applicativa e il nuovo controllo.
Il commit documentale successivo pubblica insieme questo report, risultati,
TODO e registro; identificabile con:

```text
git log -1 --format=%H -- projects/tactical-engine/docs/rag-v5-remediation-a-r1-numeric-literal-closeout-01.md
```

## Report — delta esatto

Nel paragrafo Quantifier confrontabile, sostituita esclusivamente la frase:

```text
Quantifier confrontabile: valori uguali richiedono same, salvo numeric con literal diversi che richiede different.
```

con:

```text
Quantifier confrontabile: dopo la precedenza degli stati, _expected_comparison confronta i value prima del dispatch specifico del quantifier. Value uguali richiedono same: due value=numeric richiedono attualmente same anche con literal diversi. Il confronto dei literal nel helper non prevale sul return anticipato del caller. Questa e la semantica attuale del contratto versionato, non una regola di correttezza numerica generale. Solo con value diversi si applicano le regole seguenti.
```

Il resto del paragrafo, incluse scala di forza e coppia always/never, è identico.
Nessuna nuova versione o rappresentazione dei numeric; nessuna eccezione Gold,
normalizzazione, label modificata o riscrittura dei risultati.

## Risultato dei soli controlli nuovi

Eseguito una sola volta:

```text
python -B projects/tactical-engine/tests/test_v5_spatial_extraction_numeric_literal_r1.py
```

**5/5 PASS**, 0,017 s. Evidenze:
`docs/remediation-a-r1-numeric-literal-results-01.json`.

| Controllo | Risultato osservato sul caller reale | Dispatch helper |
|---|---|---|
| explicit numeric, literal 2 contro 3 | insieme ammesso `{same}` | Zero chiamate |
| explicit numeric, literal 2 contro 2 | insieme ammesso `{same}` | Zero chiamate |
| numeric contro many, nelle due direzioni | `{different}` | Una chiamata reale per direzione |
| unknown/ambiguous contro numeric, su entrambi i lati; unknown contro ambiguous nelle due direzioni | unknown nei primi due casi; ambiguous nei restanti quattro | Zero chiamate in tutti i sei sottocasi |
| Testo normativo | Presenti precedenze, return anticipato e limite versionato; assente vecchia eccezione numeric | Non applicabile |

Il mock del helper usa `wraps`: osserva le chiamate senza cambiare il valore
restituito o il codice. Nessun helper sostitutivo per ottenere un PASS.
I controlli sono locali e deterministici, non una generazione, un backend test
o una validazione end-to-end di witness. Nessuna suite 37/37, 13/13 o tutti i
16 controlli della remediation A eseguita. I sedici PASS storici restano
immutati e validi nel loro perimetro originario.

## Invarianti e budget

Confronto integrale dei blob prima/dopo: il sorgente nuovo coincide esattamente
con il vecchio dopo la sola sostituzione del paragrafo documentata. Tutto il
resto del file è byte-per-byte identico, inclusi schema, shape check,
precontrollo semantico, locator, witness, provenance e promotion_authorized.
Il diff sui percorsi protetti è vuoto: validatore finale e helper, judge e
legacy, Gold/dataset, originali evaluation, wrapper e operazioni storiche.
Parametri di generazione invariati; nessuna nuova versione di dominio implicita.
Gli hash dei due blob applicativi sono registrati nei risultati.

| Testo / formato | Prima R1 | Dopo R1 |
|---|---:|---:|
| Handoff normativo UTF-8 | 6.594 byte | 6.967 byte |
| User con la stessa coppia storica runtime-04 | 6.938 byte | 7.311 byte |
| Schema compatto, misura storica preservata | 16.869 byte | Invariato |

Delta **+373 byte**, interamente nella frase sostituita. Conteggi iniziali dalla
revisione pubblicata; delta calcolato dai literal AST e dai blob Git, senza
eseguire un payload o un modello. Nessuna conversione byte/token: costo
reale, margine su num_ctx=4096/num_predict=2048 e compatibilità decoder restano
non verificati. Nessun effetto collaterale di codice individuato nel diff;
l'effetto intenzionale sul modello è un'istruzione più lunga e coerente con il
comportamento osservabile, non una maggiore correttezza numerica dimostrata.

## Decisione → Stato

R1 **VALIDATO** offline nel suo perimetro: testo e caller descrivono ora lo
stesso comportamento coperto dai nuovi controlli. Correzione **IMPLEMENTATO**,
verifiche **ESEGUITO** e **VALIDATO** offline. Il precedente blocco R1 è
superato da queste nuove evidenze; il giudizio B storico resta conservato.

**Idonea a una nuova revisione del contratto**, perché il controesempio R1 è
ora descritto fedelmente senza alterare i gate. Non equivale all'approvazione
indipendente della patch complessiva o del backend; tali attività non sono
state eseguite. La limitazione dei numeric resta: literal diversi possono
essere same nel caller attuale, e questo non prova equivalenza numerica.
La formulazione label meno precisa e gli altri limiti non bloccanti già
segnalati dalla revisione restano documentati, senza correzioni automatiche.
Nessuna ulteriore divergenza emersa dai soli rami mirati R1.

Compatibilità reale del decoder e budget token ancora non verificati.
Accuratezza generativa, Gate, integrazione e certificazione **BLOCCATO**.
Report, risultati, TODO e Experiment Register pubblicati nella stessa sessione.
Zero VPS, modelli, Qwen, runtime-05, staging, wrapper, verifiche backend,
modifiche a servizi/Chroma/indici/panel, merge o deploy. STOP dopo pubblicazione.
