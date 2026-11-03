# TSC V2 D3 — readiness Semantic Support S2

Attività: `RD-TSC-V2-D3-SEMANTIC-SUPPORT-S2-READINESS-01`

Baseline: `b46acf3f03104984b8bfbb242f3d83dcf8f45ae0`

## Attività → Script → Commit → Report → Risultato → Decisione → Stato

- Attività: valutazione statica dei candidati semantici già presenti.
- Script: nessuno eseguito; sono stati letti codice, dataset, report e storia Git.
- Commit: commit documentale di questo report.
- Report: questo documento.
- Risultato: esiste un candidato shadow riutilizzabile, ma nessun candidato ha
  indipendenza, Gold e copertura sufficienti per diventare gate D3.
- Decisione: **B — NLI diretto V2 utilizzabile soltanto in shadow**.
- Stato: readiness **ESEGUITO**; S2, gate, integrazione e certificazione
  **BLOCCATO**.

## 1. Riconciliazione

Branch, HEAD remoto e locale coincidevano con la baseline e il working tree era
pulito. Sono stati riconciliati TODO, experiment register, design semantic support,
report S1, codice e report storici. Non è stato eseguito alcun test, modello,
reviewer, retrieval o accesso runtime.

La ricognizione ha confermato che molti output storici non sono file Git correnti.
Il manifest `evaluation/runtime_evidence_manifest_v1.json` ne conserva percorso,
dimensione e SHA-256, ma non il contenuto. Per esempio registra il report
source-disjoint 30 con SHA-256
`f3ef699c3aaa69ced2d802b4f5fb4af5cbcbf7033139eb25780b0d0a0f338c81` e lo
stress 100 con SHA-256
`8109e1bf1562a62a84c37e2a73ed74f2a5879309ea06cf8bd539a8542ef6140e`;
nessuno dei due è presente nella storia Git ispezionabile. Le metriche registrate
restano evidenze storiche documentali, non risultati integralmente riproducibili dal
solo repository.

## 2. Inventario dei candidati

| Candidato | Funzione, modello e input | Evidenze verificabili | Errori/limiti | Stato |
|---|---|---|---|---|
| NLI diretto V2 | `benchmark_direct_three_label_nli_v2.py`; Qwen `qwen3.5:9b`; una coppia claim↔evidenza; JSON `supported/contradicted/insufficient` | codice al commit `efcb53d`; dataset Git 24/18/20/30/100 casi; TODO e report storici con metriche e singoli errori | report originali principali non in Git; gold provisional/non indipendente; stesso modello del generatore; nessuna motivazione nel verdict V2 | riutilizzabile in shadow, non gate |
| NLI/alignment V1/V2 | `judge_rag_v5_alignment_controls_v1.py` e V2 A/B; Qwen 9B; 10 controlli separati NLI/alignment | codice ai commit `92b5b61`, `9e29900`; report documentale 10/10 completati | 6/10 accordi provisional; NLI 4/5, alignment 2/5; falso positivo di scope e confusione evento/causalità; etichette non gold | diagnostica shadow |
| Atomic/contrastive NLI | `benchmark_shadow_nli_atomic_v1.py` e controlli contrastivi | casi e adjudication esatta documentati; Atomic 13/15; contrastive 4/12 | inversione di preferenza, universali e parafrasi instabili; output originali forniti in chat, non Git correnti | diagnostica dei failure mode |
| Ragas Faithfulness 0.4.3 | estrazione statement + verdict binari con due chiamate Qwen | codice adapter, report sorgente e benchmark 16 casi documentati | score binario, non distingue contradicted/insufficient; soglia 0,5 esplorativa; errori q3_03/q5_04; estrazione e reviewer non indipendenti | non idoneo a gate S2 |
| Reviewer Gemini | client REST source-grounded, modello Gemini configurabile | client Git (`ca8383b` e correzioni), un percorso tecnico e report storici | rete/costo/privacy; bundle fonte richiede verifica; voti conversazionali hanno talvolta aggiunto contenuto prima del voto; nessun benchmark claim-level S2 congelato | revisione esterna separata, non gate |
| Reviewer Groq | `groq_free_reviewer_v1.py`, `openai/gpt-oss-120b`, rubrica risposta/evidenze | adapter offline (`fe8be6a`), singolo G4 archiviato con hash | un solo caso; due contestazioni di citazioni false; affidabilità generale esplicitamente non validata | secondo parere, non gate |
| Gold E/V relazionale v2 | schemi, provenance registry, ledger A/B/C e freeze | contratti e validatore ai commit `d26f364`, `596c4ba`, `454ebad` | template con zero casi; misura estrazione/verifica relazionale, non entailment claim↔evidenza S2 | infrastruttura riutilizzabile, Gold assente |
| Gold claim-fidelity | `claim_fidelity_gold_v1.json` (16), external (18), fresh (24), adversarial (20) | casi e distribuzioni presenti in Git; adjudication motivata per il set atomico 15 | set piccoli/curati; etichette provisional o non doppio-adjudicate; riuso nello sviluppo; non rappresentativi | development/diagnostica |
| Worksheet umano | `build_rag_v5_quality_adjudication_worksheet_v1.py` e rubriche | prepara claim, fonti e review senza assegnare automaticamente score | non è un dataset popolato/frozen; richiede revisori umani | base S4/calibrazione |

## 3. NLI diretto V2

### Contratto effettivo

V2 importa integralmente il runner V1 e cambia soltanto l'istruzione. Il runner
concatena una singola evidenza e un claim, usa output strutturato Pydantic e restituisce
una sola label, senza reason code:

- `supported`: la fonte dimostra l'intero claim, incluse parafrasi fedeli;
- `contradicted`: la fonte afferma una proposizione esplicitamente incompatibile;
- `insufficient`: la fonte non dimostra né smentisce direttamente.

Il giudice vede una sola fonte per chiamata. Non estrae claim, non associa citazioni,
non gestisce composizione multi-fonte e non è collegato a D3. Il runner salva firma
input, configurazione, predizione, durata e matrice di confusione quando il report è
disponibile.

### Evidenze storiche

| Campagna | Risultato registrato | Provenienza e limite |
|---|---:|---|
| sviluppo 24 | V2 23/24 | report comunicato in chat, non archiviato come artefatto Git verificabile |
| FA 32 | 30/32 | gold non revisionato indipendentemente |
| stress 100 | 93/100; S 28/30, C 29/30, I 36/40 | estratti già usati, non source-disjoint; dataset presente, report solo manifestato |
| FIGC/FA 30 | 29/30 3-way, 30/30 binario | tre estratti; non completamente source-disjoint; report non presente in Git; gold non indipendente |
| adversarial 11 | 9/11 | fallimenti su opposizione tattica e universale; ipotesi curate |
| atomic 15 | 13/15 | fallimenti su preferenza invertita e universalizzazione |
| contrastive 12 | 4/12 | forte sensibilità a parafrasi e quantificatori; Bonacini 0/6 |
| alignment 10 | 6/10 provisional | falso `supported` su generalizzazione da tre sistemi a tutti |

Il 29/30 è quindi confermato come dato storico coerente con TODO, report e manifest,
ma non è verificabile riga per riga dal ramo corrente e non stima affidabilità
generale. Il singolo errore registrato è una contraddizione esplicita classificata
`insufficient`; altri controlli documentano il rischio opposto, cioè generalizzazioni
non provate classificate `supported`.

Le campagne coprono esempi di negazione, direzione, quantificatori e scope. Non
dimostrano copertura rappresentativa di condizioni, causalità, attori/fasi errati,
composizione multi-fonte o claim reali estratti da D3. Predizioni individuali e
matrici complete dei report principali non sono recuperabili dal repository corrente.

## 4. Indipendenza

| Dimensione | NLI V2 | Gemini | Groq |
|---|---|---|---|
| processo | chiamata separata possibile | processo/provider separato | processo/provider separato |
| modello | stesso `qwen3.5:9b` del generatore | famiglia esterna diversa | modello esterno diverso |
| configurazione | prompt/schema diversi, ma stessa base e runtime | configurazione versionabile, non calibrata S2 | configurazione versionabile, non calibrata S2 |
| dati Gold | provisional, piccoli o contaminati dallo sviluppo | nessun Gold S2 congelato | nessun Gold S2 congelato |
| evidenze | passate direttamente, retrieval escluso | estratti selezionati; autenticità bundle non automatica | estratti selezionati |
| giudizio | etichette spesso create/revisionate nello stesso ciclo di sviluppo | AI esterna, non revisione umana indipendente | AI esterna, due errori documentati nel solo G4 |

Due prompt diversi sullo stesso Qwen non danno indipendenza di modello. NLI V2 può
essere indipendente come chiamata, ma condivide bias e capacità del generatore. Gemini
e Groq migliorano l'indipendenza di modello, non quella del Gold o del giudizio, e non
hanno una calibrazione claim-level sufficiente.

## 5. Gold disponibile

I Gold E/V v2 forniscono provenance, doppia review, adjudication, freeze e hash, ma i
template hanno zero casi e il loro obiettivo è relazionale. Non sono equivalenti a un
Gold S2 claim↔evidence. I set claim-fidelity hanno casi reali e distribuzioni note,
ma sono piccoli, curati e già coinvolti nello sviluppo; diverse etichette sono
provisional. Il set atomico da 15 ha rationale umano sul testo congelato, ma non una
doppia revisione cieca/adjudication e non consente stime robuste.

Manca dunque un Gold S2 che sia contemporaneamente source-disjoint, claim-level,
con evidenza congelata, doppia review/adjudication, freeze/versione e copertura di:
parafrasi, negazione, condizioni, quantificatori, causalità, attore, fase, scope,
supporto parziale e composizione multi-fonte.

## 6. Compatibilità D3/S1 e contratto shadow possibile

D3 ora fornisce già statement atomico, span, conditions, relation/requirement refs,
bindings, polarity, evidence refs/anchors, plan fingerprint e assessment S1. Un
futuro shadow S2 può consumare una copia immutabile di tali campi senza cambiare
l'autorità S1.

Il record separato dovrebbe includere almeno:

- schema/versione, attempt ID, plan/claim/statement digest;
- digest di ciascuna evidenza e digest dell'assessment S1 consumato;
- provider, model ID/digest, prompt/config/schema fingerprint;
- label per evidenza (`supported`, `contradicted`, `insufficient`), rationale e
  riferimenti al passaggio valutato;
- aggregazione conservativa predefinita, disagreement S1↔S2 ed errori;
- stato fisso `shadow_only` e `promotion_authorized=false`.

Il modello non scrive questo record nel payload D3: un adapter di sistema lo crea
dopo il parsing. Il record deve essere verificabile e content-addressed come S1. Un
positivo S2 non modifica `promoted_answer`, non sostituisce S1 e non rende il percorso
`validated`; ogni disagreement resta non promuovibile.

## 7. Rischi di falso positivo

| Rischio | Evidenza esistente | Copertura attuale |
|---|---|---|
| plausibile ma non documentato | casi insufficient e rubriche | parziale, non rappresentativa |
| evidenza pertinente ma insufficiente | alignment/atomic | presente, con falsi positivi documentati |
| condizione omessa | pochi casi curati | non dimostrata sistematicamente |
| quantificatore alterato | stress/atomic/contrastive/alignment | presente; errori ripetuti |
| negazione invertita | dataset curati | presente, non indipendente |
| attore o fase errati | audit relazionale, non Gold NLI | non validata per S2 |
| causalità invertita | controlli alignment | copertura piccola e provisional |
| generalizzazione indebita | `methodist_every`, `negative_scope_q5` | falso positivo documentato |
| composizione impropria di fonti | contratto shadow solo progettato | non validata |
| conclusione non implicata | Ragas/NLI diagnostics | errori presenti; nessuna soglia calibrata |

Non è attribuibile alcuna percentuale di affidabilità generale.

## 8. Matrice di readiness

| Candidato | Evidenze verificabili | Indipendenza | Gold affidabile | Falsi positivi | Compatibilità D3 | Decisione |
|---|---|---|---|---|---|---|
| NLI diretto V2 | codice/dataset sì; report principali solo manifest/documenti | processo parziale; modello no | no | scope/quantificatori documentati | alta come coppia atomica | shadow candidato principale |
| Alignment V1/V2 | codice e report sintetico | stesso Qwen | provisional | 4/10 mismatch complessivi | media; task distinto | diagnostica, non S2 gate |
| Ragas Faithfulness | codice e comportamento 0.4.3 documentati | stesso Qwen, due chiamate | 16 casi piccoli | q5_04 e soglia non calibrata | bassa; binario e statement propri | non gate |
| Gemini | client e alcuni report | modello/processo sì | no | aggiunte/attribuzioni documentate | media, richiede adapter | revisione separata |
| Groq | adapter e un G4 | modello/processo sì | no | due contestazioni false nel G4 | media, richiede adapter | non gate |
| Gold E/V + worksheet | contratti/strumenti forti | processo umano progettato | zero casi S2 | non misurabili | alta come governance | base per futuro Gold |

## 9. Decisione

**B — il NLI diretto V2 è tecnicamente credibile come diagnostica shadow, ma non è
idoneo a gate.** La scelta deriva da codice semplice e compatibile con claim atomici,
etichette utili e diversi dataset già presenti; è bloccata per promozione dalla
mancanza di Gold S2 indipendente, predizioni principali non recuperabili, falsi
positivi di scope/quantificatore, assenza di copertura multi-fonte e mancata
indipendenza del modello.

## 10. Delta minimo successivo, non eseguito

1. **Recupero probatorio dei report esistenti:** acquisire esclusivamente i JSON già
   registrati nel manifest, verificarne SHA-256, firme input, configurazione,
   predizioni individuali e matrici. Delta: rende verificabili risultati già eseguiti,
   senza nuova inferenza. Output: inventario content-addressed. Costo: sola gestione
   documentale/locale, non quantificabile dal repository. Richiede autorizzazione di
   accesso alla copia che li conserva.
2. **Gold S2 claim-evidence indipendente:** riusare provenance registry, ledger A/B/C,
   freeze e worksheet; creare un dataset distinto da Gold E/V e dai casi usati per
   tuning. Delta: misura direttamente supporto semantico. Criterio: doppia review,
   adjudication, freeze, source-disjointness e copertura dei rischi elencati. Costo:
   lavoro umano significativo, non stimabile senza numerosità approvata. Richiede
   autorizzazione separata per raccolta/annotazione.
3. **Solo dopo 1–2, adapter shadow offline D3:** riusare il runner V2 con record
   content-addressed, nessuna promozione. Accettazione: input immutabili, provenance
   completa, tre label, disagreement fail-closed e metriche per classe predefinite.
   Richiede autorizzazione implementativa e, separatamente, eventuale inferenza.

Non va ripetuta alcuna campagna Qwen esistente, né riusati i set di sviluppo come
holdout. S2, reviewer automatico e Gate restano non autorizzati.

## 11. Stati ufficiali

- S1 deterministic checker: **VALIDATO offline** nel perimetro deterministico.
- Readiness S2: **ESEGUITO**.
- NLI diretto V2: riutilizzabile come shadow; non promosso a **VALIDATO** per S2.
- Gold S2 indipendente: **BLOCCATO**.
- S2 implementazione/gate: **BLOCCATO**.
- Integrazione e certificazione runtime: **BLOCCATO**.
