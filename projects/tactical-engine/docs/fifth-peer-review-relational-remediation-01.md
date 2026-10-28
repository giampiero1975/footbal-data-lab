# Quinta revisione paritaria — remediation audit relazionale

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit iniziale: `d95f226a01428446db85eb896b47335b6ec6342d`  
Commit codice/test: `b4eb68b`

## Diagnosi differenziale prima della patch

I quattro rischi sono stati riprodotti senza modificare il runtime:

1. **B3 negativo**: la variante con punto e virgola era già respinta; la
   variante nella stessa clausola attribuiva erroneamente `copre` al centrale
   nominato dopo, benché fosse responsabile soltanto della comunicazione.
2. **Requisito aperto non pertinente**: la domanda sulla copertura preventiva
   accettava `Alla perdita l'ala attacca la fascia` perché conteneva comunque
   attore, compito e trigger.
3. **Atomizzazione**: entrambi gli atomi ricevevano `centrale` e `profondità`;
   la relazione `ala → accorcia → portatore` veniva persa.
4. **Polarità multipla**: `non copre ... successivamente copre` veniva ridotto
   a `NEGATED`, nascondendo la seconda occorrenza.

Non sono emerse criticità soltanto teoriche: tutti i casi richiedevano una
correzione, ma il caso 4 non consente di ricostruire una cronologia affidabile.

## Correzioni implementate

- Il soggetto postverbale è riconosciuto soltanto nel costrutto delimitato
  `a <compito> ... è <attore>`, ancorato a inizio clausola o dopo virgola/punto
  e virgola. Una generica occorrenza successiva di `è il centrale` non collega
  più il compito.
- I requisiti aperti congelano `objective_terms` ricavati esclusivamente da
  locuzioni presenti nella domanda. La pertinenza è esposta separatamente come
  `objective_relevance`; non prova correttezza tattica o supporto documentale.
- La coordinazione esplicita con `mentre` crea segmenti locali. Attore, compito,
  spazio e finalità sono estratti dal segmento; fase e trigger comuni della
  sottodomanda sono condivisi. I vincoli non dimostrabili non vengono copiati.
- La polarità esamina tutte le occorrenze del compito. La compresenza di
  affermazione e negazione produce `AMBIGUOUS`, che non può soddisfare il
  requisito. Non viene inferito quale evento prevalga.

La mappa degli obiettivi è volutamente piccola e positiva: propone alternative
pertinenti per copertura/marcatura preventiva e ripartenza, non una blacklist
offensiva/difensiva e non una soluzione tattica universale.

## Diff del comportamento

| Caso | Prima | Dopo |
|---|---|---|
| B3 negativo con `;` | non soddisfatto | non soddisfatto |
| B3 negativo nella stessa clausola | falso positivo | non soddisfatto |
| B3 positivo `a coprire ... è il centrale` | soddisfatto | soddisfatto |
| Aperto, relazione estranea | soddisfatto | `relation_objective_not_demonstrated` |
| Centrale/ala con `mentre` | vincoli replicati | due relazioni locali corrette |
| Compito con polarità mista | `NEGATED` | `AMBIGUOUS` |

## Test e compatibilità

Quattro test nuovi coprono esclusivamente le nuove differenze. Suite
planner/audit: **42/42 PASS** (38 baseline + 4 nuovi). Compilazione di script e
test: **PASS**. `git diff --check`: **PASS**.

Le suite Tactical State Contract e API non sono state ripetute perché nessun
loro file o dipendenza comune è cambiato. `audit_answer()["complete"]`, quality
gate legacy, runner, API, pannello, `DEFAULT_PROFILE_FLAGS`, corpus, indici e
pipeline Qwen/Ollama sono invariati. Nessuna VPS, inferenza, API esterna,
benchmark, merge o deploy.

## Gold E / Gold V e limiti residui

La separazione resta invariata:

- Gold E deve misurare la fedeltà dell'estrazione dei requisiti dalla domanda;
- Gold V deve ricevere requisiti umani già corretti e misurare soltanto il
  verificatore.

Lo schema è disponibile nel report della quarta revisione, ma nessun insieme
indipendente viene dichiarato pronto. Drive11 non è rappresentativo e
Coverciano V10 non è indipendente dalla remediation. Lo stato resta
**BLOCCATO**.

Limiti residui:

- la segmentazione copre soltanto la coordinazione esplicita `mentre`;
- la mappa degli obiettivi copre un vocabolario circoscritto e può restituire
  `not_demonstrated` su formulazioni equivalenti non previste;
- `AMBIGUOUS` non ricostruisce ordine temporale, trigger diversi o prevalenza;
- pertinenza testuale, correttezza tattica e supporto documentale rimangono tre
  verifiche distinte.

Decisione: proprietà differenziali **VALIDATO offline**; audit ancora offline e
non bloccante. Non **INTEGRATO** o **CERTIFICATO**. La prossima revisione deve
controllare controesempi alle regole circoscritte; la validazione indipendente
non può iniziare senza Gold E e Gold V congelati.
