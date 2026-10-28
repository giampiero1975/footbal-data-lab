# Quarta revisione paritaria — remediation audit relazionale

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit iniziale: `4f640096f0875f650fcf425add6475a0ee419bbf`  
Commit codice/test: `6f20bcd`

## Differenza tecnica

La revisione read-only ha riprodotto tre difetti non coperti dalla baseline:

- B2: falso negativo con inciso comitativo `insieme all'ala`;
- B3: falso negativo con soggetto postverbale `a coprire ... è il centrale`;
- B4: falso positivo con `uno/l'altro` e due attori candidati.

Ha inoltre mostrato che A2/A3 non possono essere promossi a relazione
affermata e che l'estrazione part-level confondeva requisiti aperti ed
espliciti. Queste differenze giustificano i nove test nuovi; i casi già coperti
non sono stati duplicati e la regressione storica 114/114 non è stata
rieseguita integralmente.

## Correzione implementata

`scripts/v5_tactical_query_plan_v1.py` ora:

1. associa il compito al soggetto precedente quando il secondo attore compare
   soltanto nell'inciso circoscritto `insieme a/con`;
2. riconosce esclusivamente la costruzione postverbale delimitata
   `a <compito> ... è <attore>`;
3. classifica `uno/l'altro` con più attori come associazione ambigua;
4. espone la polarità testuale `AFFIRMED`, `NEGATED`, `AMBIGUOUS` o
   `NOT_FOUND`; soltanto `AFFIRMED` può concorrere al soddisfacimento;
5. tratta `non lascia scoperta` e `non deve mai abbandonare` come ambigue
   quando il requisito riguarda copertura/protezione;
6. congela ogni sottodomanda con `question_part_id`, distingue requisito
   `explicit` e `open` e separa i compiti sovrapposti in obblighi atomici;
7. consente a un requisito aperto di riconoscere una relazione concreta
   proposta dalla risposta, senza inventare un attore obbligatorio.

La finestra anaforica non è stata modificata. Il wrapper compatibile
`_task_is_negated()` è preservato. `audit_answer()["complete"]`, runner,
`DEFAULT_PROFILE_FLAGS`, API e pannello non sono stati modificati.

## Test differenziali

Nove test nuovi documentano:

1. B2 inciso comitativo;
2. B3 soggetto postverbale;
3. B4 pronome ambiguo;
4. A2 negazione del comportamento rischioso;
5. A3 negazione modale;
6. multipart aperto/esplicito indipendente;
7. compiti sovrapposti trasformati in atomi distinti;
8. requisito aperto con relazione operativa concreta;
9. requisito aperto con testo soltanto generico.

Risultato planner/audit: **38/38 PASS** (29 baseline pertinenti + 9 nuovi).
Compilazione di script e test: **PASS**. `git diff --check`: **PASS**.
Le suite contratto/API non sono state ripetute: nessun loro file o dipendenza è
stato modificato. Nessuna inferenza, API esterna, VPS o benchmark è stato usato.

## Separazione Gold E / Gold V

Lo schema seguente è definito, ma non costituisce ancora un dataset gold:

```json
{
  "case_id": "stable-id",
  "independence": {"origin": "...", "used_in_development": false},
  "question": "testo originale",
  "answer": "testo originale non modificato",
  "evidence": [{"id": "F1", "text": "...", "provenance": "..."}],
  "requirements": [{
    "requirement_id": "...",
    "question_part_id": "...",
    "type": "explicit|open",
    "required_dimensions": ["actor", "task"],
    "constraints": {},
    "admissible_relations": [],
    "equivalent_alternatives": [],
    "forbidden_contradictions": [],
    "undetermined": []
  }],
  "human_reference": {"motivation": "...", "frozen_before_audit": true}
}
```

- **Gold E** confronta i requisiti estratti dalla domanda con quelli annotati e
  congelati dall'essere umano.
- **Gold V** passa al verificatore requisiti già corretti e confronta soltanto
  il riconoscimento delle relazioni nella risposta.

Domanda, risposta ed evidenze mancanti rendono non valutabile il relativo
criterio. Drive11 non è rappresentativo dell'obiettivo relazionale e i casi
Coverciano V10 non sono indipendenti dalla remediation. Pertanto nessun gold
indipendente viene dichiarato disponibile e la validazione controllata resta
**BLOCCATO**.

## Limiti e decisione

La patch non è un parser italiano generale. Le costruzioni riconosciute sono
intenzionalmente delimitate; formulazioni linguistiche diverse possono restare
`AMBIGUOUS` o `NOT_FOUND`. La coerenza testuale non prova correttezza tattica o
supporto documentale; `semantic_support_verified` resta falso.

Decisione: considerare la remediation **IMPLEMENTATO**, i test **ESEGUITO** e
il solo perimetro differenziale **VALIDATO offline**. Mantenere l'audit offline
e non bloccante. Non dichiararlo **INTEGRATO** o **CERTIFICATO** e non avanzare
alla validazione controllata finché Gold E e Gold V non dispongono di casi
indipendenti congelati.
