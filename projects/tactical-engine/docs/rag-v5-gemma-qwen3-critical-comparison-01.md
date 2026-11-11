# Confronto critico incrementale — Gemma 4 12B / Qwen3 30B-A3B

Data: 2026-11-11. Attività: `RD-RAG-V5-GEMMA-QWEN3-INDEPENDENT-COMPARISON-01`.

## Decisione unica: A — Gemma 4 12B

Confermo il candidato precedente, per il compromesso sulla CPX52 dichiarata
(12 vCPU, 24 GB RAM, nessuna GPU), senza upgrade o aumento del canone.
Non dimostro che ragioni meglio di Qwen3 30B-A3B. Entrambi hanno evidenze
pubbliche di capacità generali e licenza Apache-2.0; a parità di qualità
locale sconosciuta, Gemma lascia un rischio di pressione sulla memoria
sensibilmente inferiore per mantenere RAG, contesto e servizi. La scelta
riguarda un candidato all'eventuale confronto, non una migrazione autorizzata.
Non è una probabilità numerica di raggiungere 9/10 o 26/30.

La principale obiezione è concreta: un MoE con 3,3B parametri attivi potrebbe
avere un costo per token inferiore al dense 12B, e Qwen potrebbe ragionare
meglio. Dimensione del download, anzianità e parametri totali non risolvono
questa obiezione. Non esiste qui una misura CPX52 che la elimini.

## Riconciliazione e differenza nuova

HEAD iniziale locale/GitHub `405f8d09a98201609e36928f4c10eac9e60ab07b`, branch
`codex/tactical-state-contract-v1`, working tree iniziale pulito. TODO e registro
ufficiali confrontati con le copie raw GitHub allo stesso SHA; consultati
report strategico e inventario collegato. Si riutilizzano le loro evidenze
su configurazione, codice, risultati Qwen storici, grounding, licenze e RAG.
Non sono stati ripetuti benchmark, suite, audit ABI o diagnosi q3_04.

Il report nuovo è giustificato dal candidato **Qwen3 30B-A3B**, assente dalla
shortlist precedente, dalla sua ambiguità di versione e dal calcolo
condizionale della cache dai config ufficiali. Non riapre l'audit di Gemma
26B-A4B o Qwen3.8 27B: nessuna nuova evidenza pratica ne giustifica il riesame.
La posizione ChatGPT esaminata è quella fornita nell'allegato dell'utente;
non è stata richiesta un'altra risposta a un modello né una perizia esterna.

Metodo: lettura statica Git/JSON e fonti ufficiali pubbliche, soli piccoli
metadati/config, senza pesi. Fatti, revisioni e inventario SHA-256 in
[`gemma-qwen3-comparison-evidence-01.json`](gemma-qwen3-comparison-evidence-01.json).
Quattro snapshot originali in `gemma-qwen3-comparison-public-sources-01/`;
quelli Gemma già pubblicati restano nel precedente inventario.

## Identità prima del confronto

**DOCUMENTATO:** il Qwen originario è `Qwen/Qwen3-30B-A3B`, pubblicato il
29 aprile 2025, con modalità thinking/non-thinking. Esistono anche
`Qwen3-30B-A3B-Instruct-2507` e `Thinking-2507`. Il repository ufficiale segnala
che nell'agosto 2025 l'alias Ollama `qwen3:30b-a3b` puntava al Thinking-2507:
è un avvertimento datato, non la verifica dell'alias odierno.
[Release originale](https://qwenlm.github.io/blog/qwen3/),
[repository ufficiale](https://github.com/QwenLM/Qwen3).

Per rendere B determinato confronto la variante **Instruct-2507**, non-thinking,
pertinente alle risposte naturali del coach. Non la confondo con il modello
originario né uso il nome generico come identità congelata. Revisione pubblica
`0d7cf23991f47feeb3a57ecb4c9cee8ea4a17bfe`; l'originale ha revisione
`ad44e777bcd18fa416d9da3bd8f70d33ebb85d39`.
[Card Instruct alla revisione](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507/blob/0d7cf23991f47feeb3a57ecb4c9cee8ea4a17bfe/README.md).

## Matrice richiesta

**DOCUMENTATO (D)** indica specifiche o dichiarazioni pubblicate, oppure
risultati storici versionati; non misure indipendenti. **STIMATO (S)** indica
inferenze tecniche condizionali, non RAM o velocità osservate.
**MISURATO (M): nessuna misura dei due candidati sulla VPS è disponibile.**
Gli hash dei piccoli file attestano l'integrità documentale, non il runtime.
Queste sono classi di evidenza, non stati del progetto.

| Proprietà | Gemma 4 12B | Qwen3 30B-A3B, variante scelta per B |
|---|---|---|
| Identificativo | D: `google/gemma-4-12B-it`, revisione `43c9d014b231474fa7212dbb48a762566c2b255d`; catalogo `gemma4:12b` Q4_K_M, hash breve `6114515d63c1` | D: `Qwen/Qwen3-30B-A3B-Instruct-2507`, revisione sopra; `qwen3:30b-a3b-instruct-2507-q4_K_M`, hash breve `19e422b02313` |
| Data/generazione | D: 3 giugno 2026, famiglia Gemma 4 | D: originale aprile 2025; variante luglio 2025. Generazione Qwen3, non Qwen3.5 |
| Licenza | D: Apache-2.0, esecuzione autonoma ammessa nei relativi termini | D: Apache-2.0, stessa qualificazione; non inferenza proprietaria |
| Architettura/attivi | D: dense circa 12B, senza selezione sparse di esperti | D: MoE 30,5B totali, 3,3B attivi; 128 esperti, 8 selezionati |
| Quantizzazione/file | D: variante llama.cpp Q4_K_M circa 8,0 GB, distinta da MLX; componenti draft/projector da contabilizzare se usati | D: Q4_K_M circa 19 GB; tag originale Q4_K_M anch'esso circa 19 GB. Non tutte le quantizzazioni hanno questa dimensione |
| RAM operativa/margine | S: pressione attesa inferiore, ma picco e margine non quantificabili dal file; cache, buffer, runtime e servizi si aggiungono | S: vincolo severo; cache F16 condizionale 0,75 GiB a contesto 8192, oltre a pesi residenti/buffer/runtime/OS/servizi. Totale e margine non misurati |
| Runtime locale | D: distribuzione Ollama/llama.cpp pubblicata; non prova di supporto della 0.40.5 installata | D: distribuzione Ollama pubblicata; compatibilità del tag preciso con la build installata non verificata |
| Ragionamento generale | D: card ufficiale con risultati pubblici; nessun confronto controllato omogeneo qui con Qwen30 | D: card ufficiale Instruct con risultati pubblici; non prova di superiorità tattica o nella nostra quantizzazione |
| Latenza CPU | S: dense 12B può essere lento; nessun token/s o tempo CPX52 osservato | S: attivi ridotti possono aiutare; routing, banda memoria e accesso agli esperti possono limitare. Non deducibile dai 30B totali |
| Integrazione | S: nuova famiglia/template, compatibilità runtime e comportamento delle istruzioni da verificare; nessun cambio embeddings implicito | S: alias ambiguo, scelta Instruct/Thinking e template da congelare; pressione memoria può interferire con RAG/servizi |
| Differenza dal Qwen3.5 9B attuale | D: altra famiglia e generazione; S: diversifica il candidato, non garantisce migliore ragionamento | D: altra versione Qwen e architettura MoE; S: vantaggio non derivabile né dal marchio né dai parametri |
| Qualità tattica dimostrata | D: nessun risultato locale ai criteri 9/10 e 26/30 pubblicato | D: nessun risultato locale ai medesimi criteri pubblicato; i risultati Qwen3.5 9B non sono risultati Qwen3 30B |
| CPX52 | S: candidato più prudente, fattibilità effettiva subordinata a compatibilità, picco RAM e latenza | S: possibile in configurazioni particolari, ma non giustificato come scelta primaria entro 24 GB condivisi senza misure |

Fonti nuove della matrice: [catalogo Qwen Instruct Q4_K_M](https://ollama.com/library/qwen3:30b-a3b-instruct-2507-q4_K_M),
[catalogo originale Q4_K_M](https://ollama.com/library/qwen3:30b-a3b-q4_K_M),
[rilascio Gemma 12B](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12B/).
Per Gemma, riuso anche fonti e snapshot del
[report precedente](rag-v5-local-models-final-strategic-review-01.md).
Gli hash brevi dei cataloghi non sostituiscono un digest completo e una verifica
dell'artefatto eventualmente installato. Nessuno è stato installato qui.

## Memoria e velocità: ciò che il MoE non dimostra

**DOCUMENTATO:** i config originali e Instruct riportano 48 layer, 4 KV head,
head dimension 128. **STIMATO:** con una sequenza, contesto 8192 e K/V F16
interamente allocati, la cache teorica è
`2 × 48 × 4 × 128 × 8192 × 2 = 805306368 byte = 0,75 GiB`.
[Config esatto](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507/blob/0d7cf23991f47feeb3a57ecb4c9cee8ea4a17bfe/config.json).
Non include padding/allocatore, buffer di calcolo, pesi, servizi o OS.
Formato cache, parallelismo e allocazione reali non sono stati osservati.

I 3,3B attivi riguardano il lavoro per token, non una RAM equivalente a un 3B.
I circa 19 GB sono il pacchetto quantizzato pubblicato, non il picco residente:
non calcolo `24-19` come margine effettivo. Mappatura dei file, page cache,
resident set e swapping dipendono dall'esecuzione. Tenere più pagine su disco
non prova una latenza accettabile su CPU. L'ipotesi di caricamento può essere
plausibile, ma **un esercizio sostenibile con RAG e margine non è dimostrato**.
Non aumento RAM/canone né riduco automaticamente contesto per farlo entrare.

## Ragionamento, modernità e RAG

**DOCUMENTATO:** Gemma dichiara MMLU-Pro 77,2; Qwen Instruct-2507 78,4.
[Card Gemma](https://huggingface.co/google/gemma-4-12B-it),
[card Qwen](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507).
Sono dichiarazioni di produttori diversi, non un confronto eseguito con
stesso harness, prompt, modalità, precisione e budget. Non deduco una classifica
dalla differenza; AIME 2025 e 2026 non sono neppure lo stesso set.
Nelle fonti esaminate non emerge un confronto ufficiale diretto omogeneo
fra queste due versioni. Nessuna di queste metriche misura il nostro standard
tattico italiano o la quantizzazione scelta sulla CPX52.

**STIMATO:** modernità, dati/addestramento e architettura possono compensare
parametri, ma la data più recente non è una prova che Gemma lo faccia meglio.
La preferenza per Qwen basata soltanto su 30B o sul MoE sarebbe insufficientemente
fondata; anche una preferenza per Gemma basata soltanto sull'età sarebbe tale.
La scelta incorpora capacità generali documentate e autonomia/licenza, poi
usa la sostenibilità come discriminante poiché la superiorità non è nota.

**DOCUMENTATO, storico:** l'inventario precedente distingue errori nei testi
Qwen, grounding, prospettiva del retrieval e limiti delle valutazioni. Non
isola una sola causa dominante. La diagnosi q3_04 non dimostra che il RAG sia
l'unico problema né che un modello diverso risolva la duplicazione fuori lato.
Cambiare generatore non corregge automaticamente retrieval, fonti o giudizi.
Corpus, embedding/reranker e controlli conservano il loro valore distinto;
nessun contratto o gate viene aggirato o cambiato da questa raccomandazione.

## Giudizio sulla posizione ChatGPT e criterio di revisione

Concordo con la conclusione prudente riportata dall'utente e con la distinzione
fra fattibilità e intelligenza. Nessun errore sostanziale è dimostrato in quella
formulazione. Preciso 30,5B/3,3B, versione e quantizzazione; contesto, cache e
servizi impediscono di trattare 19 GB come consumo totale. Non concorderei
con l'inferenza che Qwen sia più lento perché ha 30B o che Gemma ragioni meglio
perché è recente: nessuna delle due è dimostrata. La precedente preferenza
utente per Qwen non basta a giustificarlo come primo candidato, ma non è
confutata come ipotesi di qualità. Non attribuisco a ChatGPT affermazioni
più forti di quelle effettivamente fornite.

Ribalterebbero la scelta evidenze sull'esatto Qwen30 quantizzato, sulla stessa
CPX52 con i servizi necessari: picco sostenibile, almeno 4 GB MemAvailable
come margine prudenziale già proposto (non requisito empirico del modello),
assenza di swapping persistente, latenza entro il budget precedente e qualità
tattica indipendente migliore, con almeno 9/10, media 26/30 e zero errori gravi.
Anche l'incompatibilità o l'insostenibilità misurata di Gemma imporrebbe di
rivedere A; non autorizzerebbe automaticamente B. Nessuna nuova campagna è
proposta o eseguita qui: questi sono criteri di falsificazione della scelta.

## Tracciamento e arresto

Attività sopra → metodo di analisi statica, nessuno script esecutivo nuovo →
commit documentale contenente report, evidenza e TODO/registro contestuali →
questo report → matrice e differenza di versione/cache → decisione **A** →
analisi **ESEGUITO**. Il commit di pubblicazione è quello che introduce questo
file, identificabile da `git log -1 --format=%H -- <percorso-report>`; evitare
uno SHA autoreferenziale inventato.

La prova già proposta resta **DA FARE**, non autorizzata. Nessun modello,
compatibilità o miglioramento tattico è dichiarato **VALIDATO**. Accuratezza
generativa, Gate e certificazione generale del coach restano **BLOCCATO**;
risultati storici nei propri perimetri preservati. Nessuna SSH, installazione,
pesi, inferenza, test, benchmark, modifica applicativa/VPS/runtime, merge o
deploy. STOP dopo pubblicazione e verifica GitHub/working tree.
