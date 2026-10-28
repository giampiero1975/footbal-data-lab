# Settima verifica differenziale conclusiva — audit relazionale

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit iniziale: `d1a9cc70b7c58a691d3b09422792d7c96fba2d1c`  
Commit codice/test: `084cb5b`

## Matrice diagnostica prima della patch

| Rischio | Output baseline | Esito atteso | Classificazione |
|---|---|---|---|
| A positivo: relazione propria più avversario | non soddisfatto | soddisfatto | falso negativo riprodotto |
| A negativo: copertura avversaria più azione propria | non soddisfatto | non soddisfatto | comportamento corretto |
| B1: parole-obiettivo su azioni diverse | non soddisfatto | non soddisfatto | comportamento corretto |
| B2: `contropiede` con protezione della profondità | soddisfatto | non respinto solo per il sinonimo | comportamento corretto |
| C: terzo segmento dopo cambio di cornice | eredita `alla perdita` | eredita `alla riconquista` | difetto riprodotto |

Gli output sono stati acquisiti sulla baseline prima di scrivere i test nuovi.

## Correzioni applicate

### Unità relazionali interne alla clausola

La clausola completa resta l'unità usata dalle verifiche storiche. Per i soli
requisiti aperti con obiettivo o ambito vengono inoltre estratte unità
relazionali circoscritte mediante virgola, `mentre` e coordinazione esplicita
seguita da un attore.

Ogni unità conserva:

- testo;
- dimensioni attore/compito/spazio/trigger/finalità;
- ambito esplicito `own`, `opponent` o `unspecified`.

Un requisito aperto è pertinente soltanto se una singola unità contiene
attore, compito, ambito compatibile e almeno un'alternativa per ciascun gruppo
obiettivo. Non può quindi combinare la protezione di un attore con la
ripartenza descritta da un'altra azione.

La clausola non viene genericamente spezzata ai fini degli altri controlli:
restano preservate finalità distribuite, anafora e B3/B4 precedenti.

### Cornice sequenziale

`relation_requirements()` usa ora una cornice corrente. Un trigger o una fase
locale esplicita aggiorna la cornice; i segmenti successivi senza valore locale
ereditano l'ultimo valore dimostrato, non sempre quello del primo segmento.
Gli ID `question_part/segment/relation` restano invariati.

Nel caso conclusivo:

1. centrale → `alla perdita`;
2. ala → `alla riconquista`;
3. punta → `alla riconquista`.

## Comportamenti preservati

- L'azione propria corretta passa anche quando la stessa clausola confronta un
  avversario.
- La copertura esplicitamente avversaria non prende in prestito la presenza del
  centrale proprio.
- Il caso B1 con parole distribuite resta non soddisfatto.
- Il caso B2 con `contropiede` resta accettabile perché la stessa unità dimostra
  anche protezione della profondità; non è stato aggiunto un sinonimo ad hoc.
- Il trigger iniziale comune continua a essere ereditato quando nessun segmento
  successivo lo sostituisce.

## Test e isolamento

Quattro test differenziali nuovi. Planner/audit: **50/50 PASS** (46 baseline +
4 nuovi). Compilazione di script e test: **PASS**. `git diff --check`: **PASS**.

Tactical State Contract e API non sono stati rieseguiti perché non condividono
file modificati. `audit_answer()["complete"]`, quality gate legacy, runner,
API, pannello, `DEFAULT_PROFILE_FLAGS`, corpus, indici e Qwen/Ollama sono
invariati. Nessuna VPS, inferenza, chiamata esterna, benchmark, merge o deploy.

## Limiti residui

- Le unità relazionali coprono coordinazioni esplicite circoscritte, non la
  sintassi italiana generale.
- `unspecified` non viene trasformato in un'appartenenza inventata.
- I gruppi-obiettivo restano una misura di pertinenza testuale, non una
  certificazione tattica o documentale.
- Trigger semanticamente equivalenti fuori dal vocabolario restano un limite
  dichiarato; non è stato introdotto un sistema aperto di sinonimi.
- La polarità multipla resta conservativamente `AMBIGUOUS`.

## Decisione conclusiva

Il ciclo di remediation basato su controesempi costruiti durante lo sviluppo
si arresta qui. Le proprietà differenziali della settima verifica sono
**VALIDATO offline**; l'audit resta non bloccante e non è **INTEGRATO** o
**CERTIFICATO**.

Il passo successivo non è un'ottava euristica: è la preparazione indipendente e
supervisionata di Gold E e Gold V secondo lo schema già pubblicato. Finché tali
insiemi non esistono e non sono congelati prima dell'audit, la validazione
indipendente resta **BLOCCATO**.
