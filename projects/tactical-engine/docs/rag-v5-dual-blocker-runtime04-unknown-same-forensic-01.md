# RAG V5 — analisi forense offline unknown/same runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-UNKNOWN-SAME-FORENSIC-01`.
Data: 2026-11-10, Europe/Rome.

## Attività → Script → Commit → Report

Analisi esclusiva della nuova incoerenza runtime-04: `status=unknown` con
`comparison=same`. Non riaperte le analisi runtime-03 su lato errato,
`space_availability/between` o quantificatori many/some.

Riconciliati TODO, Experiment Register, report runtime-04 e originali pubblicati.
HEAD iniziale locale/GitHub
`86bfcfc8b193b43e9863f3a4e16c051a2aa3cdcc`, branch
`codex/tactical-state-contract-v1`, working tree pulito. Baseline applicativa:
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`; nessuna modifica successiva nei
sorgenti applicativi esaminati.

Script: sola lettura locale, Git e stdlib Python per hash, parsing JSON e
lettura AST di costanti. Nessun import di moduli applicativi, chiamata di
funzioni di dominio, wrapper, suite o modello; zero accessi VPS.
Commit: documentale con questo report, fatti derivati, TODO e registro
pubblicati insieme; identificabile dalla storia di questo report.

Fatti derivati verificabili: `docs/runtime04-unknown-same-forensic-facts-01.json`.
Originali immutati: `evaluation/runtime04_execution_01/` al commit `86bfcfc`.

## Diagnosi principale

**Osservazione accertata:** l'output generato è già incoerente nella risposta
grezza. Il parsing e la persistenza non introducono unknown, same o supported.
Il precontrollo applica correttamente le regole versionate e blocca prima della
localizzazione. Non è dimostrato un difetto del locator o del validatore finale.

**Lacuna oggettiva dell'handoff:** il prompt non esplicita la precedenza degli
stati sul confronto e lo schema di trasporto espone enum indipendenti senza
vincolare status, sentinelle e frammenti. Questo consente formalmente la
rappresentazione osservata; non dimostra che tale lacuna abbia causato da sola
le scelte del modello. La causa cognitiva rimane non determinabile.

## 1. Integrità e percorso dei dati

Confrontati i byte di tutti i 27 originali con hash registrati e blob pubblicati
a `86bfcfc`: conformi. Nessun originale modificato. Hash chiave già registrati:

| Artefatto | SHA-256 |
|---|---|
| `request_payload.json` | `addc8f60fc5aec7aa21f41868ca3def1e0f3a0dc95ad19e3ebadd1c8b7a4d001` |
| `prompt.txt` | `e005b09968ce8fc93cb9493041f80b1b51088bb5e260855600834dbf7fc727f5` |
| `raw_response.json` | `15aae8e9a6d71619f1a5d26e42e922c75adc5eb66a9027d6d3dd7fa5fa46a9eb` |
| `extraction.json` | `aaca6e99d5a3b165827954f5a67b135ed80ff8832bf3209f6cd65bd27dcc721c` |

Percorso ricostruito:

1. `build_extraction_prompt()` concatena `EXTRACTION_INSTRUCTION`, FONTE e
   AFFERMAZIONE (`shadow_nli_spatial_relations_v2_inference.py:57`). Il messaggio
   user effettivo nel payload coincide con questa costruzione della baseline.
   Non viene concatenato il diverso `INSTRUCTION` del percorso legacy.
2. `prompt.txt` differisce dal messaggio inviato soltanto per un LF finale:
   è scritto come `prompt + "\n"` dal wrapper, riga 611. Il primo confronto
   documentale di uguaglianza stretta ha rilevato quel LF; il confronto corretto
   ne ha confermato l'origine. Non è una mutazione dell'handoff al modello.
3. Il payload trasmette `format=EXTRACTION_SCHEMA`, think false, temperatura 0,
   contesto 4.096, 2.048 token massimi e i due messaggi registrati. Il sistema
   chiede soltanto JSON conforme. Il Gold non è passato come risposta corretta:
   resta nel record input e nella decisione del wrapper, correttamente separato.
4. La risposta è completa: `done_reason=stop`, 846 token generati, nessun
   troncamento registrato. `json.loads(raw_response.message.content)` coincide
   con l'intero oggetto `extraction.json`, inclusi tutti gli stati e comparison.
   La serializzazione cambia formato/ordine dei campi, non i valori.
5. Il judge fa solo parsing JSON e chiama `materialize_extraction()`
   (`shadow_nli_spatial_relations_v2_inference.py:146–154`), senza repair.
6. `materialize_extraction()` verifica shape, poi chiama
   `extraction_semantic_errors()` (`..._extraction.py:426–441`). Il gate riusa
   `_comparison_errors()` e produce il boundary semantico con dettagli.
7. Il nuovo verificatore wrapper conserva il risultato come
   `fail_closed_extraction_semantic`, exit 80. Provenance con `records=[]`,
   witness/validation assenti, label osservata e semantic match nulli,
   `promotion_authorized=false`.

L'ordine di arresto è quindi: shape superato → comparison incoerente →
boundary semantico. Il locator e `validate_spatial_v2()` non vengono chiamati.

## 2. Inventario degli slot e dei confronti

Otto slot per lato: tutti hanno status unknown, quindi **16 slot principali**.
Ogni contenitore conditions include inoltre un item ambiguous, con frammenti
vuoti: **due item aggiuntivi**, distinti dallo status unknown del contenitore.

| Dimensione | Claim: contenuto oltre a unknown | Evidence: contenuto oltre a unknown | Comparison generato | Prescritto dal codice |
|---|---|---|---|---|
| subject | ID `difesa_bassa`, frammento `La difesa bassa` | ID `squadre_che_difendono_basse`, frammento corrispondente | same | unknown |
| reference | ID `spazio_tra_linea_porta`, frammento spaziale | stesso ID e stesso frammento | same | unknown |
| semantic_axis | `space_availability`, nessun frammento | `space_availability`, nessun frammento | same | unknown |
| value | `abundant`, nessun frammento | `abundant`, nessun frammento | same | unknown |
| conditions | item ambiguous `linea_difensiva_bassa`, senza frammenti | stesso item e assenza di frammenti | same | unknown |
| phase | valore unknown, nessun frammento | valore unknown, nessun frammento | same | unknown |
| quantifier | valore unknown, literal null, nessun frammento | identico | same | unknown |
| polarity | `affirmed`, nessun frammento | `affirmed`, nessun frammento | same | unknown |

I valori prescritti nell'ultima colonna derivano da lettura statica delle regole,
non dall'esecuzione di un nuovo test. Il runtime conserva soltanto il codice
aggregato `E_EXTRACTION_COMPARISON_INCONSISTENT`, path comparison.

### Precedenza di `_expected_comparison()`

In `v5_tactical_semantic_support_s2_spatial_v2.py:344`:

- Per conditions: ambiguous del **contenitore** precede unknown del contenitore;
  se uno dei due contenitori è unknown il confronto ammesso è unknown, prima
  del controllo degli ID. Gli item ambiguous interni non rendono automaticamente
  ambiguous lo status esterno.
- Per le altre dimensioni: ambiguous precede absent/unknown; uno slot
  absent/unknown impone l'insieme ammesso `{unknown}`, prima dell'uguaglianza
  di ID o valori.
- Solo oltre quei controlli si confrontano entity ID, valori o quantificatori.
  In `_comparison_errors()` anche il raffinamento value/asse viene saltato se
  l'insieme ammesso contiene unknown/ambiguous.

Qui entrambi i lati sono unknown in tutte le dimensioni: gli otto same sono
incompatibili. L'uguaglianza delle stringhe unknown, degli ID o dei valori
non prova l'uguaglianza di due relazioni conoscibili. Il gate è coerente.

## 3. Rappresentazione e handoff

### Combinazioni ammesse dalla shape, insufficienti per il dominio

Nel payload lo schema elenca status e value separatamente e permette array
di frammenti vuoti. Non contiene default che impongano unknown o same. Non
collega con vincoli condizionali gli stati alle sentinelle, agli ID o al numero
di frammenti; comparison e label sono anch'essi enum indipendenti.

Quindi lo shape check accetta il JSON osservato. Ciò non è una validazione
semantica positiva: il gate successivo lo respinge correttamente. Già le regole
finali versionate distinguono unknown da un valore concreto, senza bisogno
di inventare nuove categorie:

- unknown per un'entità richiede la sentinella e nessuna anchor
  (`_entity_errors`, riga 211);
- unknown per asse/valore richiede value unknown e nessuna anchor
  (`_value_slot_errors`, riga 231);
- conditions unknown non contiene item (`_conditions_errors`, riga 250);
- polarity affirmed senza anchor è implicit, non unknown
  (`_polarity_errors`, riga 314).

Nel raw sono invece presenti unknown con entità/frammenti concreti,
`space_availability`, `abundant`, `affirmed` e item di condizioni. Phase e
quantifier unknown/unknown senza frammenti sono rappresentazioni plausibili
di incertezza, ma non giustificano comunque comparison same.

Queste sono incongruenze documentali con il contratto finale, non errori
aggiuntivi **osservati** dal validatore finale: quel validatore non è stato
raggiunto e non viene eseguito in questa analisi. Cambiare soltanto i comparison
in unknown non risolverebbe stati/valori/frammenti né il riconoscimento del Gold.

### Cosa contiene e cosa omette il prompt effettivo

Il prompt nomina le tre disponibilità `abundant`, `scarce`, `neutral` e separa
`space_availability` da `relative_position`. La distinzione nominale esiste:
non è corretto dire che abbondanza e scarsità siano del tutto assenti.

Mancano però definizioni operative generali degli stati, precedenza
status→comparison, accoppiamenti stato/sentinella/frammenti e la coppia
esplicita abundant/scarce della tabella `INCOMPATIBLE_VALUES`. Il generico
«same richiede identita deterministica» non sostituisce quella precedenza.
«Non rendere intercambiabili status, value e sentinelle» non spiega come
rappresentarli. Le descrizioni dello schema definiscono i ruoli degli slot,
non tali correlazioni.

Manca anche una spiegazione generale che distingua disponibilità della regione
spaziale dalla posizione della regione e dall'avanzamento consentito in un'altra
regione. La matrice di enum è necessaria ma non costituisce da sola una
specifica sufficiente di grounding. Non si deduce che una sua estensione
migliorerebbe sicuramente la generazione.

Il `format` completo è registrato nel payload; non esiste una traccia della
rappresentazione interna usata dal backend per il decoding né della visibilità
effettiva delle sue description al modello. Non si attribuisce quindi alle
description un effetto causale provato.

## 4. Perché compare supported e limiti causali

Osservabile: claim ed evidence sono entrambi rappresentati con disponibilità
abundant e tutti i comparison same. Questo quadro, se si ignorassero gli stati,
è compatibile con il ramo superficiale che associa confronti same a supported.
Non è dimostrato che questo sia il ragionamento interno effettivamente seguito.

La fonte dice che le squadre basse tolgono spazio fra linea difensiva e porta;
il claim afferma che ne lasciano molto. Il Gold contradicted è coerente con
questa opposizione. Il valore abundant della fonte non la rappresenta, e non
seleziona un frammento nel campo value che permetta di tracciarne il grounding.
Questo errore generativo è distinto dalla sola incoerenza degli stati.

Il Gold non viene imposto al modello. Non sono disponibili rationale,
probabilità dei token, alternative scartate, decoder trace o controlli
controfattuali sul medesimo input. Non si può stabilire se status unknown sia
una scelta prudenziale, un effetto del formato, un errore di comprensione o
un altro meccanismo. Neppure overlap lessicale, ordine degli enum, capacità del
modello o ignoranza del lessico inglese sono cause dimostrate. Una risposta
completa sotto il limite token non prova da sola comprensione del contratto.

## 5. Responsabilità

| Responsabilità | Diagnosi e limite |
|---|---|
| Generazione | Il raw propone supported e abundant su entrambi i lati; non rappresenta l'opposizione della fonte. Errore osservato, causa cognitiva ignota. |
| Rappresentazione strutturata | 16 unknown con otto same e combinazioni di sentinelle/frammenti incoerenti già nel raw. Accertato. |
| Handoff/trasporto | Payload e prompt corretti rispetto alla baseline, nessuna mutazione successiva. Specifica di stati e correlazioni sottodeterminata: lacuna accertata, suo contributo causale al comportamento del modello non isolato. |
| Parsing/persistenza | Raw parsato ed extraction identici come oggetti; nessun errore introdotto, solo formattazione JSON e LF del file prompt. |
| Localizzazione | Non raggiunta. Non si attribuiscono errori o successi al locator. |
| Precontrollo semantico | Respinge correttamente comparison incompatibili con gli stati; nessuna falsa promozione osservata. |
| Validatore finale | Non raggiunto. Le sue regole sono riferimento documentale, non un risultato runtime aggiuntivo. |
| Wrapper | Nuovo ramo correttamente conserva boundary, dettagli, null e assenza witness/validation; finalizzazione già verificata, non rieseguita. |

## 6. Due alternative, solo proposte

### A — Handoff normativo completo con schema extraction correlato

**Problema:** il trasporto permette rappresentazioni che le regole versionate
considerano incoerenti e il prompt non esplicita la precedenza degli stati.

**File interessati:** `scripts/shadow_nli_spatial_relations_v2_inference.py`
per le istruzioni extraction; `scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py`
per il solo schema/shape di trasporto; un nuovo controllo differenziale
documentato per il contratto rivisto. Locator e validatore finale immutati.

**Delta proposto:** specificare regole generali per explicit/implicit/absent/
ambiguous/unknown, sentinelle e frammenti; esporre la precedenza di comparison
e le incompatibilità versionate. Correlare nello schema status, contenuto e
cardinalità dei frammenti, mantenendo rappresentabile l'incertezza legittima.
Definire semanticamente disponibilità/spazio e grounding per ciascun lato
senza esempi o regole lessicali costruiti su q3_04. Il modello continua a
proporre comparison/label, che restano sottoposti ai controlli esistenti.
Nessuna riscrittura automatica di unknown, same o supported; un nuovo raw
incoerente resta rifiutato.

**Evidenza:** schema e shape indipendenti, assenza di default, nuova combinazione
raw unknown con valori concreti, tutti i same e nessun value fragment.

**Rischi:** vincoli non supportati dal backend, aumento del prompt, deriva fra
schema e regole finali; pressione a scegliere stati apparentemente certi solo
per soddisfare il formato. Anche un extraction formalmente perfetto può
assegnare alla fonte il valore sbagliato. La revisione dovrà restare allineata
al contratto, senza modificare le regole per agevolare il caso.

**Criterio di verifica nuovo:** replay immutabile di questo raw contro il
contratto di trasporto rivisto per attribuire gli errori ai campi status/value/
fragments, conservando la rejection; casi differenziali nuovi di unknown
legittimo contro unknown con contenuto concreto, senza eliminare l'incertezza.
Verificare nel payload mock la nuova tabella normativa e l'invarianza dei lati
e del percorso legacy. Non ripetere la vecchia suite 37/37 o i 13 controlli
wrapper. Si controlla il nuovo contratto, non si presenta una rejection più
precoce come maggiore accuratezza. Nessun controllo eseguito qui.

**Limite generativo:** nessuna garanzia di comprendere la riduzione dello spazio;
servirebbe poi una distinta prova generativa autorizzata, con guardie indipendenti.

### B — Nuovo trasporto di sole relazioni, derivazione sistemica limitata

**Problema:** il modello produce tre rappresentazioni ridondanti e potenzialmente
discordanti: relazioni, comparison e label.

**File interessati:** nuovo modulo/contratto opt-in di trasporto; adapter in
`scripts/shadow_nli_spatial_relations_v2_inference.py` e percorso dedicato di
materializzazione nell'extraction adapter. Il contratto finale Spatial V2 e
il suo validatore non vanno alterati. Richiede progetto/versionamento distinto,
non una modifica implicita di runtime-04.

**Delta proposto:** in un nuovo formato il modello emette soltanto relazioni
grounded, senza comparison o label. Dopo controlli completi su stato, sentinelle,
frammenti e localizzazione, un adapter deriva confronti e label solo dove le
regole versionate danno un esito univoco. Assenza o ambiguità della base impedisce
il risultato; non si sceglie arbitrariamente fra compatible/different.
Coreferenza semantica non provata resta una lacuna, non viene risolta con ID
identici. Nessuna seconda chiamata, correzione del raw storico o sostituzione
della sua label. L'origine sistemica delle nuove derivazioni è esplicita.

**Evidenza:** runtime-04 mostra concretamente la discordanza fra campi generati
separatamente. Il nuovo contratto eliminerebbe tale ridondanza, senza dichiarare
corretti i valori spaziali proposti dal modello.

**Rischi:** ampliamento architetturale, incompatibilità con la telemetria
model-label, falsi positivi se si scambia l'uguaglianza degli ID con identità
semantica o si decide un confronto non univoco. La fonte rappresentata
erroneamente come abundant potrebbe ancora condurre a supported: cambiare
responsabilità della derivazione non migliora da solo il grounding.

**Criterio di verifica nuovo:** contratto relations-only versionato, raw senza
comparison/label, tracciabilità di ogni derivazione, rifiuto di relazioni
non valide e di confronti non univoci, nessuna chiamata aggiuntiva. Casi nuovi
relativi al nuovo adapter, non replica dei test di comparison del validatore
esistente. Nessuna simulazione o implementazione eseguita qui.

**Limite generativo:** elimina una fonte di incoerenza formale, non l'errore
di estrazione o la coreferenza; non abilita automaticamente il Gold q3_04.

## Decisione → Stato

**Raccomandazione: A**, come eventuale primo intervento circoscritto, perché
la lacuna di specifica è osservabile e non richiede di cambiare le responsabilità
di modello e sistema. Va progettata e revisionata separatamente; nessuna
implementazione o nuova esecuzione è autorizzata da questa analisi. B resta
un'alternativa architetturale distinta, da valutare solo con un incarico dedicato.

Revisione **ESEGUITO**; catena probatoria, origine nel raw, precedenza unknown
e limiti dell'handoff **VALIDATO** come analisi documentale. Causa cognitiva
interna non determinabile. Nessun miglioramento generativo dichiarato.
Alternative non implementate, stato **DA FARE** previa decisione del titolare.
Accuratezza delle contraddizioni, nuovi runtime, Gate, integrazione e
certificazione restano **BLOCCATO**. STOP dopo pubblicazione.
