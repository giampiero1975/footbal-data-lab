# TSC V2 D3 — Semantic Support S1 offline

Attività: `RD-TSC-V2-D3-SEMANTIC-SUPPORT-S1-IMPLEMENTATION-01`
Baseline: `9f2e9faee8b51cf86986eb995864bfd9877a35d2`
Commit tecnico: `de457a9`

## Attività → Script → Commit → Report → Risultato → Decisione → Stato

- Attività: sostituire l'autorità sintetica `claim_id → status` di D3 con un
  checker deterministico, separato dal generatore e limitato alla classe S1.
- Script: `scripts/v5_tactical_semantic_support_s1.py`, integrazione opt-in in
  `scripts/v5_tactical_state_dual_output_v1.py` e adattamento minimo del runner.
- Commit: `de457a9`.
- Report: questo documento.
- Risultato: 29/29 test S1/D3 e 43/43 regressioni TSC V2 direttamente interessate,
  totale 72/72 PASS; `git diff --check` PASS.
- Decisione: S1 può promuovere solo l'esatta unità documentale atomica coperta;
  ogni altra classe resta fail-closed.
- Stato: checker **IMPLEMENTATO**, test **ESEGUITO**, proprietà deterministiche
  coperte **VALIDATO offline**. S2, Gate, integrazione e certificazione restano
  fuori perimetro e **BLOCCATO**.

## Riconciliazione e delta

TODO, experiment register, design S1 e report D3 sono stati riconciliati prima
della patch. Non esisteva un produttore S1 equivalente: D3 accettava soltanto un
dizionario sintetico opzionale usato dalle fixture. Il planner, il dominio TSC V2,
l'audit V1, retrieval, collection, API e pannello non sono stati modificati.

Il claim D3 richiede ora `statement`, `section_span`, `conditions` e
`requirement_refs`, oltre ai campi esistenti. Gli span sono indici di code point
Unicode sulla sezione normalizzata NFC/newline e intervalli semiaperti `[start,end)`.
Il validatore controlla limiti, identità statement/span, overlap, riferimenti,
condizioni dichiarate e copertura di tutti i caratteri non-whitespace della prosa.
Una porzione sostanziale non attribuita produce `not_evaluable`, non una copertura
presunta.

## Checker e assessment

`tactical_documentary_support_assessment_v1` registra versione, attempt ID opaco,
fingerprint del piano, claim ID, digest dello statement, digest e verdict per
evidenza, verdict aggregato, reason code e identità/configurazione dell'assessor.
L'assessor consentito è soltanto
`deterministic/s1_exact_atomic/1.0`; configurazione e input sono content-addressed.
Il consumer ricalcola l'intero assessment e rifiuta alterazioni di piano, claim,
statement, evidenza, verdict o assessor. Il payload Qwen non ammette campi di
assessment e il percorso di produzione non accetta più il dizionario libero.

La sola regola positiva richiede `direct`, un'unica evidenza, un unico anchor,
statement identico all'anchor e all'intera unità di evidenza normalizzata. L'ultima
restrizione è intenzionalmente conservativa: S1 non possiede un estrattore
indipendente di condizioni o quantificatori e quindi non promuove un sottoestratto
che potrebbe aver perso il contesto governante. NFC e normalizzazione newline sono
le sole trasformazioni.

Non esiste una regola negativa deterministica già autorizzata abbastanza precisa.
S1 non emette quindi `unsupported`: negazioni, parafrasi, contesto aggiuntivo,
claim compositi/multi-fonte, bounded inference e uncertainty restano
`not_evaluable`. Questo limite è deliberato; assenza di prova non diventa
contraddizione.

## Test ed evidenze

Comando offline eseguito:

```text
python -m unittest projects/tactical-engine/tests/test_v5_tactical_semantic_support_s1.py projects/tactical-engine/tests/test_v5_tactical_state_dual_output_v1.py projects/tactical-engine/tests/test_v5_tactical_state_contract_v2.py projects/tactical-engine/tests/test_v5_tactical_state_generation_v2.py
```

Risultato: `Ran 72 tests ... OK`.

I nuovi differenziali coprono percorso reale `supported`, parafrasi/quantificatore/
condizione e contesto parziale non promossi, multi-fonte, assenza di regola negativa,
statement/span, NFC, overlap, prosa scoperta, input malformato, digest alterati,
piano differente, assessor non autorizzato, verdict manomesso, assessment model-authored
e audit V1 negativo. La regressione D3 usa il checker reale; le suite V2 confermano
l'isolamento di dominio e generazione. Nessuna inferenza, rete, NLI, retrieval,
Chroma, API o runtime è stata invocata.

## Limiti e rischi residui

- La classe positiva ha copertura volutamente bassa e non risolve il supporto
  semantico generale.
- Nessuna contraddizione è classificata automaticamente senza una regola negativa
  separatamente approvata.
- S2/reviewer, composizione multi-fonte e bounded rules non sono implementati.
- Nessun Gate runtime dimostra la capacità di Qwen di produrre il nuovo envelope.
- `validated` vale soltanto per le proprietà offline e le fixture deterministiche
  eseguite; non significa **INTEGRATO** o **CERTIFICATO**.

## File tecnici

- `scripts/v5_tactical_semantic_support_s1.py`
- `scripts/v5_tactical_state_dual_output_v1.py`
- `scripts/smoke_test_rag_v5_e2e.py`
- `tests/test_v5_tactical_semantic_support_s1.py`
- `tests/test_v5_tactical_state_dual_output_v1.py`

## Stati finali

- S1 deterministic checker: **IMPLEMENTATO**.
- Test differenziali e regressioni interessate: **ESEGUITO**.
- Proprietà S1 coperte: **VALIDATO offline**.
- S2, Gate runtime, integrazione e certificazione: **BLOCCATO**.
