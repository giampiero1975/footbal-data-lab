# RAG V5 — revisione indipendente remediation A

Attività: `RD-RAG-V5-DUAL-BLOCKER-REMEDIATION-A-INDEPENDENT-REVIEW-01`.
Data: 2026-11-10, Europe/Rome.

## Attività → Script → Commit → Report

Revisione architetturale statica autonoma del commit tecnico
`0ea62c0ef1f0adfcd928c2893f069de060275381`, senza assumere come prova
l'approvazione dell'autore o i sedici PASS. Decisione **B: patch da correggere
prima di ulteriori verifiche**. Un rilievo bloccante di coerenza dell'handoff;
nessuna correzione implementata.

Riconciliati TODO ed Experiment Register ufficiali con GitHub: branch
`codex/tactical-state-contract-v1`, HEAD locale/remoto iniziale
`c864040a8e07885db700b01f4388d2ca47d9153a`, working tree pulito, origin
`https://github.com/giampiero1975/footbal-data-lab.git`. Letti report remediation
A, forense runtime-04, risultati differenziali, codice dei sedici controlli,
originali input/payload/raw/config runtime-04 e diff tecnico completo.
Confrontati sorgenti prima/dopo `0ea62c0`; validatore finale invariato rispetto
a `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.

Script della revisione: `docs/remediation-a-independent-static-audit-01.py`.
Legge Git, AST, costanti letterali e JSON versionati; non importa moduli
applicativi e non chiama funzioni di dominio. Ricostruisce il testo mediante
sola concatenazione dei literal AST e serializzazione delle matrici costanti.
Fatti: `docs/remediation-a-independent-review-facts-01.json`.

Comando documentale eseguito dalla root:

```text
python -B projects/tactical-engine/docs/remediation-a-independent-static-audit-01.py
```

La prima raccolta ha incontrato l'envelope `payload` del JSON storico; corretto
soltanto il lettore documentale, la raccolta è terminata. Nessun test applicativo
eseguito, nessuna suite 37/37, 13/13 o 16 ripetuta, nessun replay applicativo.
I risultati storici sono letti, non ricertificati. Non ripetuta l'analisi
forense/hash di tutti gli originali: il diff tecnico non li modifica.

Commit della revisione: commit documentale che pubblica insieme questo report,
script/fatti, TODO e registro; identificabile senza autoriferimento circolare con:

```text
git log -1 --format=%H -- projects/tactical-engine/docs/rag-v5-dual-blocker-remediation-a-independent-review-01.md
```

## R1 — Bloccante: numeric/literal, prompt diverso dalla regola effettiva

Riferimenti puntuali, relativi a `projects/tactical-engine/scripts/` nel commit
tecnico esaminato:

- `v5_tactical_semantic_support_s2_spatial_v2_extraction.py:358`: il nuovo
  handoff richiede `different` per quantificatori numeric con literal diversi.
- `v5_tactical_semantic_support_s2_spatial_v2.py:344`, soprattutto `:363`:
  `_expected_comparison()` dopo le precedenze degli stati confronta i value;
  se entrambi sono `numeric`, restituisce immediatamente `{same}`.
- Il dispatch al quantifier helper è successivo, alla riga 370. La distinzione
  fra literal nel helper `:375–380` non viene raggiunta per value uguali.
- `_comparison_errors():388` usa il risultato effettivo del primo helper;
  il precontrollo extraction `..._extraction.py:402–428` lo riusa senza modifiche.

Dimostrazione per lettura dei rami, **non fixture eseguita**: due quantificatori
explicit, value numeric, literal rispettivamente `2` e `3`, ciascuno con
frammento letterale valido, superano le nuove correlazioni schema/shape. Non
sono ambiguous/unknown/absent. I value sono uguali: il primo return impone same,
prima di qualsiasi lettura dei literal. Seguire il nuovo prompt e proporre
comparison.quantifier=different produce quindi
`E_EXTRACTION_COMPARISON_INCONSISTENT` nel boundary
`E_EXTRACTION_SEMANTIC_INCONSISTENT`, senza arrivare al locator.

Non è una modifica introdotta nel validatore: la precedenza è preesistente.
La patch introduce però una nuova istruzione normativa incompatibile con il
comportamento versionato che dichiara di preservare. Non si può assumere che
l'intento del helper isolato prevalga sul suo chiamante effettivo.

Impatto: output conforme all'istruzione nuova respinto dal contratto, rischio di
falsa diagnosi generativa e contratto non univoco. Nessun bypass o promozione:
il fail-closed continua a funzionare. Il rilievo resta bloccante per l'obiettivo
specifico di allineare handoff e regole effettive, anche se non riguarda il raw
unknown/same di runtime-04.

I sedici controlli non risolvono questo punto: il test numeric verifica forma e
literal del singolo slot; il controllo sulle 1.050 combinazioni confronta
predicati di slot, non confronti fra due numeric con literal differenti. Il
controllo normativo della matrice esamina assi e coppie incompatibili; il mock
verifica presenza di istruzioni. Nessuno dimostra questa precedenza del caller.

Raccomandazione, non implementata: riconciliare l'istruzione col comportamento
effettivo congelato, rendendo esplicito il limite numeric. Qualsiasi decisione
di cambiare invece la semantica finale richiede un mandato separato: non rientra
nella remediation A né in questa revisione. Un futuro controllo differenziale
mirato a questo ramo avrebbe una differenza tecnica documentata; qui non è
stato eseguito. Nessuna modifica automatica di comparison o label proposta.

## Matrice indipendente

Le classi seguenti sono rilievi di revisione, non stati del progetto.
I riferimenti E, V, J e T indicano rispettivamente extraction, validatore finale,
judge e nuova suite, nei percorsi scripts/ o tests/ del progetto.

| Proprietà | Evidenza concreta nel codice | Rischio residuo | Severità / classe | Decisione |
|---|---|---|---|---|
| Correlazioni stati/entità | E:94–107, 286–298; V:211–228 | Schema consente ancora ID riservati nei rami concreti e absent sul claim; Python li respinge | Bassa, Non bloccante | Separazione accettabile, non equivalenza schema/Python |
| Asse/valore e sentinelle | E:54–85, 300–323, 405–418; V:231–247 | Incrocio asse/valore resta semantico, non grammaticale | Bassa, Non bloccante | Nessuna nuova esclusione legittima individuata nella lettura |
| Phase/polarity/quantifier, forma | E:129–150, 300–329; V:277–325 | Numeric max64 già limite di trasporto precedente, non vincolo nuovo finale | Bassa, Non bloccante | Implicit general/none/affirmed, unknown e ambiguous coerenti |
| Confronto numeric fra lati | E:358 contro V:363–372; helper V:375–380 | Istruzione different contraddice same effettivo | Alta, **Bloccante — R1** | Correggere contratto prima di ulteriori verifiche |
| Conditions e item | E:110–120, 322–334; V:250–274 | Grammar non impone child ambiguous né ID distinti/prefisso | Bassa, Non bloccante | Contenitore explicit con item ambiguous resta legittimo; Python chiude i residui |
| Frammenti e grounding | E:40–44, 200–268, 442–482; V:190–208 | JSON non prova esistenza, unicità, ordine, NFC o appartenenza al lato | Bassa per sicurezza, Non bloccante | Locator/final gate invariati; niente grounding inventato |
| Precedenza unknown/ambiguous | E:356; V:344–361; E:402–428 | Comparison è enum indipendente nel decoder | Bassa, Non bloccante | Stati precedono uguaglianza; incoerenza resta respinta |
| Incertezza e label | E:161, 345–359; V:413–435; E:527–589 | Root esige una proposta di label; frase «non dimostra supporto» meno precisa di «insufficient» | Media, Non bloccante | Unknown non forza contenuti; insufficient è disponibile, target ignoto non promosso |
| Alternative anyOf e refs | E:47–180 | Schema più grande e rami ripetuti da compilare | Non verificabile offline per decoder | Struttura statica coerente; nessuna prova sulla build |
| uniqueItems e residui | E:40–44, 200–268, 322–334 | Non si assume enforcement del decoder | Bassa, Non bloccante | Dedup Python e controlli successivi obbligatori |
| Budget contesto/output | J:58–65, 96–123; metriche sotto | Capienza e possibili troncamenti non misurati col nuovo handoff | Non verificabile offline | Non dichiarare compatibilità o margine token |
| Legacy, witness, provenance e promozione | Diff tecnico; E:431–603; J funzioni invariate | Helper nuovo calcolato all'import anche nel legacy, ma puro | Bassa, Non bloccante | Nessuna variazione di payload legacy o regole finali rilevata |
| Copertura delle 16 verifiche | T:203–210, 307–354 e risultati pubblicati | Parità limitata ai campioni, checker subset non Draft completo, manca R1 | Media, Non bloccante come limite probatorio | PASS letti come evidenza parziale; nessuna suite ripetuta |

## Schema: costruzione statica e limiti

Ogni anyOf di slot è costituito da oggetti completi, con required di tutti i
campi e additionalProperties=false. Le alternative numeric sono disgiunte per
value; gli altri rami per status. Nessun properties fratello di anyOf. Le
annotazioni description non aggiungono vincoli incompatibili. I soli riferimenti
locali sono relation e comparison, presenti in $defs: nessun ciclo o ref esterno
operativo; $schema e $id identificano il formato, non un download eseguito.

Costrutti usati: type, const, enum, properties, required, additionalProperties,
anyOf, $ref/$defs, min/maxItems, min/maxLength, pattern, uniqueItems e metadati.
Non introdotti if/then/else, dependentSchemas, contains, not o repair/default.
Non si conclude che il backend implementi tutti questi costrutti solo perché
sono JSON Schema. Il checker storico implementa un subset, non certifica né
Draft completo né grammar Ollama/llama.cpp effettiva.

Il trasporto è intenzionalmente più permissivo del deterministico per:
claim absent, ID concreti sentinella/alfabeto, prefisso e unicità condition_id,
almeno un item ambiguous nel relativo contenitore. Schema permette anche
comparison incoerenti, label incoerenti e valori fuori dall'asse scelto. Questi
casi restano respinti nei gate appropriati; non sono normalizzati.

Non trovata per lettura una nuova eliminazione indebita delle rappresentazioni
legittime di singolo slot: cardinalità corrispondono alle anchor finali; il
limite literal=64 e l'unicità frammenti erano già nel trasporto. L'assenza di
un controesempio nello scope letto non dimostra equivalenza esaustiva.
R1 è invece una divergenza normativa concreta fra handoff e semantica effettiva.

## Incertezza e responsabilità

Unknown conserva sentinella, zero frammenti e conditions vuote. Ambiguous
conserva frammenti ancorabili senza inventare un valore concreto; implicit è
limitato alle famiglie previste. Conditions distingue status dell'item e del
contenitore, come il contratto finale. Nessun bisogno di fabbricare ID concreti
per rappresentare un'entità unknown: entity:unknown è una sentinella.

Il formato non ammette label=null, limite preesistente; ammette insufficient.
La proposta di label non diventa autorevole per il solo schema. Claim core
ignoto produce E_RELATION_NOT_COMPARABLE nel finale; fase ignota o evidenza
non determinabile possono produrre insufficient secondo le precedenze. Il
trasporto non dimostra che il modello userà questi rami anziché inventare
certezza; questo rischio generativo non è verificato offline.

Nessun errore nuovo attribuito al locator o al validatore finale: la patch non
li modifica. R1 riguarda la rappresentazione normativa consegnata al modello;
il controllo effettivo resta quello preesistente. Nessuna normalizzazione,
correzione di label/comparison o promozione implicita individuata.

## Messaggio inviabile e budget

J:58–65 compone solo `EXTRACTION_INSTRUCTION + "\n\nFONTE:\n" + evidence +
"\n\nAFFERMAZIONE:\n" + claim`; non concatena anche il prompt legacy.
J:108–123 invia due messaggi: system «Rispondi soltanto con JSON conforme allo
schema.» e quel singolo user. Lo schema viaggia separatamente in format.
Il Gold del record input non è concatenato né passato come label corretta.
La parola contradicted è una categoria del contratto, non il Gold rivelato.

Parametri invariati: qwen3.5:9b di default, stream=false, think=false,
temperature=0, num_ctx=4096, num_predict=2048; una sola chiamata, zero
retry/repair/fallback. Timeout judge normale 180 s e opzione diagnostica 360 s
invariati; i limiti supervisore storici 450 s/kill-after15 non sono modificati.
Nessun nuovo wrapper autorizzato o creato.

| Componente | Runtime-04 pubblicato | Dopo patch, stessa coppia pubblicata |
|---|---:|---:|
| Istruzioni UTF-8 | 2.319 byte | 6.594 byte, ricostruzione statica |
| Messaggio user UTF-8 | 2.663 byte | 6.938 byte / 6.935 caratteri |
| Schema JSON compatto UTF-8 | 6.008 byte | 16.869 byte, misura pubblicata precedente non rieseguita |
| prompt_eval_count | 592 token osservati | Non verificato |
| eval_count | 846 token osservati | Non verificato |

Istruzioni cresciute di 4.275 byte; schema cresciuto di 10.861 byte. Le
ripetizioni fra istruzioni e schema esplicitano correlazioni, non un secondo
claim/evidence o doppio prompt. Il system e la chiusura user ripetono solo il
vincolo JSON. R1 è l'istruzione contraddittoria concreta; la sintesi di label
«non dimostra supporto» è un'ulteriore imprecisione non bloccante, con finale
più preciso e invariato.

**Nessuna conversione byte/token.** I 592 token precedenti non si estrapolano
al nuovo testo o schema. num_predict=2048 è un limite di generazione, non prova
che il nuovo input e l'output entrino nel contesto 4096. Manca il tokenizer e
chat template effettivo del GGUF, il trattamento di format da quella build,
la grammar realmente compilata e la politica di contesto/troncamento. Non si
assume che i 16.869 byte siano tutti token di input né che abbiano costo nullo.
Capienza reale, accettazione schema ed enforcement dei rami sono **non
verificabili offline con le evidenze disponibili**. Non richiedono né
autorizzano qui una nuova generazione o l'accesso VPS.

## Risultato → Decisione → Stato

**Unica decisione: B — Patch da correggere prima di ulteriori verifiche.**
Il nuovo handoff non è coerente col percorso semantico effettivo per numeric.
Pur restando sicuro il fail-closed, il mandato di coerenza non è soddisfatto:
non raccomando di passare ora alla successiva verifica del backend. Dopo una
correzione separatamente autorizzata di R1 servirà riconciliare di nuovo il
contratto; la compatibilità reale e il budget resteranno comunque da provare
in un'attività distinta. Nessuna nuova generazione autorizzata dalla revisione.

Revisione **ESEGUITO**, analisi documentale e rilievo statico **VALIDATO** nel
perimetro delle evidenze. Patch resta **IMPLEMENTATO**; i risultati offline
storici non sono cancellati, ma l'idoneità al passo backend è **BLOCCATO** da
R1. La correzione è **DA FARE** previa autorizzazione. Accuratezza delle
contraddizioni, Gate, integrazione e certificazione restano **BLOCCATO**.

Pubblicati contestualmente report, fatti/script, TODO ed Experiment Register.
Nessuna modifica applicativa, test applicativo, VPS, inferenza, wrapper,
staging, runtime-05, merge, deploy o promozione. STOP dopo pubblicazione.
