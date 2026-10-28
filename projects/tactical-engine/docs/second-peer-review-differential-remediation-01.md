# Seconda revisione paritaria — remediation differenziale 01

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit iniziale revisionato: `ebc6722`  
Commit codice/test: `d34ad7c`

## Criticità confermate

### Audit tattico relazionale

- Una relazione negata poteva risultare soddisfatta.
- Due attori nella stessa clausola potevano condividere impropriamente il
  compito del secondo.
- I requisiti automatici privi di attore e compito espliciti erano troppo
  generici per sostenere una copertura positiva.
- La segmentazione per singola frase perdeva relazioni anaforiche distribuite
  su due frasi consecutive.

Correzione minima: negazione conservativa sul comportamento, associazione al
più vicino attore precedente, stato `requirement_underspecified` e finestra di
due frasi soltanto con indicatore anaforico esplicito. L'audit resta
diagnostico e non modifica `complete`.

### Sessioni

- Un job riuscito di altra sessione o altro caso poteva essere referenziato.
- Lo snapshot non aveva paginazione e restituiva il dettaglio completo.
- `explicit_confirmed_facts_only` attribuiva al server una garanzia di
  provenienza che il client autenticato non dimostra da solo.

Correzione minima: corrispondenza obbligatoria di sessione e caso, rifiuto dei
job legacy come riferimenti contestuali, elenco paginato e limitato a metadati,
dettaglio conservato nell'endpoint job, policy rinominata
`authenticated_client_declared_context` con provenienza `client_declared`.
L'API resta intenzionalmente mono-operatore con token condiviso.

### Feedback

Il nome temporaneo fisso era vulnerabile a due aggiornamenti concorrenti dello
stesso job. La scrittura è ora serializzata dal lock dello stato, conserva
`os.replace()`, un solo sidecar e la semantica “ultima chiamata completata”.

### Tactical State Contract

- Una contraddizione concreta mapping/assegnazione poteva essere saltata se la
  presenza non era completa.
- Un possibile rientro non ordinabile non veniva qualificato.

Le assegnazioni concrete condivise vengono ora controllate indipendentemente
dalla completezza della presenza; la continuità totale degli attori continua a
richiedere presenza completa. Un rientro senza ordine dimostrabile produce
`actor_reentry_order_unknown`, non un blocco inventato.

## Osservazioni non confermate come nuovi difetti

- Citazione valida, pertinenza e supporto semantico erano già separati;
  `semantic_support_verified` resta sempre falso. Sono stati preservati.
- Non è stato introdotto un sistema multiutente: l'accesso resta deliberatamente
  mono-operatore e autenticato con un unico token. Il vincolo è ora esplicito.
- Non occorre un secondo archivio sessioni né feedback; i sidecar esistenti
  restano la fonte unica.

## Test differenziali nuovi

1. relazione richiesta negata;
2. doppio attore con compito del secondo;
3. relazione anaforica su due frasi adiacenti;
4. sottodomande sovrapposte ma non specificate;
5. job riuscito di sessione/caso differente;
6. cronologia di 75 job con paginazione e payload metadata-only;
7. due aggiornamenti feedback concorrenti;
8. mapping concreto contraddittorio con presenza parziale;
9. possibile rientro non ordinabile.

## Regressione

- Planner/audit: **29/29 PASS**.
- Tactical State Contract: **50/50 PASS**.
- API: **35/35 PASS**.
- Totale pertinente: **114/114 PASS**.
- Compilazione dei tre moduli: **PASS**.
- `git diff --check`: **PASS**.
- `knowledge_panel.html`: invariato rispetto a `ebc6722`.
- `DEFAULT_PROFILE_FLAGS`: invariato e senza `--tactical-plan`.

## Decisione e stato

Le nove lacune differenziali sono chiuse offline. Nessun merge, deploy,
benchmark, inferenza o chiamata esterna è stato eseguito. Il prossimo passo
consigliato è la validazione indipendente dell'audit su casi congelati completi
di domanda, risposta ed evidenze, ancora senza blocchi automatici.

Stato: correzioni **IMPLEMENTATO**, test **ESEGUITO**, perimetro differenziale
offline **VALIDATO**; non **INTEGRATO** e non **CERTIFICATO**.
