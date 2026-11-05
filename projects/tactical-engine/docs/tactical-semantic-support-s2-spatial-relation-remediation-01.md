# RD-TSC-V2-D3-S2-SPATIAL-RELATION-REMEDIATION-01

## Attivita

Implementazione offline di un contratto NLI sperimentale, versionato e
strettamente opt-in per contraddizioni tra relazioni spaziali inverse. La
remediation nasce dal falso positivo reale `q3_04`, ma definisce una regola
generale e non contiene routing o label specifici del caso.

## Script e commit

- Contratto: `scripts/shadow_nli_spatial_relations_v1_inference.py`.
- Test: `tests/test_shadow_nli_spatial_relations_v1_inference.py`.
- Identificativo: `nli_spatial_relations_v1`.
- Versione: `1.0`.
- Contratto base riutilizzato lazily: `shadow_nli_v2_inference`.
- Commit tecnico: `2934d234868a1f4c6e05e9571a76d7a642eb3b86`.

## Differenze contrattuali rispetto a V2

Il nuovo contratto conserva le tre label canoniche e gli stessi parametri di
trasporto/structured output di V2. Aggiunge esclusivamente l'obbligo di
confrontare, prima della label:

- soggetto;
- proprieta o spazio;
- riferimento spaziale;
- direzione della relazione;
- condizioni e contesto;
- eventuale fase o tempo di gioco.

Predicati incompatibili sullo stesso referente e nelle stesse condizioni sono
`contradicted` anche senza negazione grammaticale esplicita. Gli esempi di
direzione inversa chiariscono il principio e sono dichiarati non esaustivi e non
utilizzabili come blacklist. Se identita, condizioni o direzione non sono
determinabili, oppure la fonte tace, il risultato resta `insufficient`. La mera
sovrapposizione lessicale non prova `supported`.

Quantificatori e garanzie conservano la distinzione fail-closed di V2: assenza
di prova non diventa automaticamente contraddizione.

## Isolamento e selezione

La nuova versione e inerte all'import e non e referenziata da judge V2, bridge
S2 o runner della Fase B. La selezione futura richiede esplicitamente:

```python
from shadow_nli_spatial_relations_v1_inference import judge_pair
```

Costruzione e import non contattano Ollama. Solo una chiamata esplicita a
`judge_pair()` importa lazily schema e parser Pydantic V2 e costruisce il
trasporto. Nessun default, routing, API, panel o pipeline e stato modificato.

Il blob di `benchmark_direct_three_label_nli_v2.py` resta identico prima e dopo:
`dabc6180a300a9239f5fc294ad50ce17fe1579d4`. L'istruzione V2 conserva SHA-256
`e7ce58bb021029f12b57ba306c8c0181a658f2a330bdbd0a2f83e0148129efdb`.

## Verifiche offline

Comando:

```text
python -m unittest tests/test_shadow_nli_spatial_relations_v1_inference.py -v
```

Risultato: **6/6 PASS** in 0,058 s.

Copertura differenziale:

1. identita/versione e selezione solo esplicita;
2. soggetto, referente, direzione, condizioni e fase obbligatori nel contratto;
3. distinzione tra `insufficient` e `contradicted`;
4. `q3_04` usato solo come input motivante, senza ID o label attesa nel prompt;
5. istruzione V2 e routing correnti invariati;
6. structured output e fail-closed verificati con trasporto mock, senza rete.

Compilazione dei due file e `git diff --check`: PASS. Nessuna suite storica e
stata ripetuta e nessun modello e stato chiamato.

## Limiti, decisione e stato

- Nuovo contratto: **IMPLEMENTATO**.
- Test differenziali: **ESEGUITO**.
- Integrita statica, isolamento, label e fail-closed: **VALIDATO** offline.
- Efficacia su `q3_04`, accuratezza generale e assenza di regressioni semantiche:
  **BLOCCATO**; i test statici non dimostrano che Qwen segua l'istruzione.
- Integrazione, Gate e certificazione: **BLOCCATO**.

Unico prossimo passo: revisione indipendente statica del commit e del contratto.
Qualunque futura prova runtime richiede una successiva decisione esplicita e non
e autorizzata da questa attivita.
