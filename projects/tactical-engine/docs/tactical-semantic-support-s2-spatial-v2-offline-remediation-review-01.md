# RD-TSC-V2-D3-S2-SPATIAL-V2-OFFLINE-REMEDIATION-REVIEW-01

## Baseline

Closeout esclusivamente documentale della revisione indipendente statica sul
commit `3c935b03a65e461088dacd27c73344c465d7f985`, branch
`codex/tactical-state-contract-v1`. HEAD locale/remoto conformi e working tree
pulito prima della registrazione. Nessun closeout equivalente risultava già
pubblicato.

## Oggetto e perimetro

La revisione ha esaminato esclusivamente la remediation offline R1/R2:

- restrizione delle incompatibilità fra valori spaziali;
- conversione fail-closed degli errori operativi del judge;
- test differenziali e report pubblicati;
- isolamento e non-promozione.

Questa attività non introduce codice e non rivaluta accuratezza, q3_04, Gate,
integrazione o certificazione. Non è stato creato o eseguito alcuno script
tecnico nel closeout.

## Evidenze GitHub esaminate

- validatore `v5_tactical_semantic_support_s2_spatial_v2.py`;
- judge `shadow_nli_spatial_relations_v2_inference.py`;
- suite `test_v5_tactical_semantic_support_s2_spatial_v2.py`;
- report `tactical-semantic-support-s2-spatial-v2-offline-remediation-01.md`;
- TODO ed experiment register;
- commit iniziale `128f014...` e remediation `3c935b0...`.

## Esito R1

**VALIDATO — revisione statica mirata.**

Nel percorso esaminato `_comparison_errors()` restringe il confronto:

- assi differenti: solo `different`;
- valori uguali: solo `same`;
- coppie in `INCOMPATIBLE_VALUES`: solo `incompatible`;
- altre coppie diverse: solo `different`;
- sentinelle `unknown`/`ambiguous`: precedenza conservata.

Un comparison non ammesso produce `E_COMPARISON_INCONSISTENT` e
`not_evaluable`. L'insieme permissivo intermedio di `_expected_comparison()` non
è un difetto residuo nel percorso, perché viene ristretto prima
dell'accettazione. Non è richiesto refactoring cosmetico.

## Esito R2

**VALIDATO — revisione statica mirata.**

Il judge restituisce envelope strutturati non promotabili per timeout, errori
operativi di trasporto, risposta incompleta, contenuto mancante, JSON invalido e
witness non valido. Sono preservati:

```text
evaluation_status="not_evaluable"
label=null
promotion_authorized=false
```

Il percorso invoca il trasporto una volta, senza retry, repair o fallback. Gli
errori di programmazione non classificati restano eccezioni.

## Risultati test già documentati

La remediation registra:

- baseline pubblicata: 16/16 PASS, prima dei nuovi casi;
- primo run remediation: 16/18 PASS, 2 FAIL;
- run finale: **18/18 PASS**, exit code 0;
- mock del trasporto e assenza di inferenze reali;
- moduli legacy invariati e `git diff --check` PASS.

La revisione indipendente ha verificato staticamente codice, test e report su
GitHub, ma **non ha rieseguito personalmente la suite**. Il closeout non registra
una seconda esecuzione indipendente dei 18 test e non modifica retroattivamente
i risultati originali.

## Limiti residui

- validazione complessiva del contratto ancora bloccata;
- accuratezza e generalizzazione non dimostrate;
- q3_04 non verificato runtime con Spatial V2;
- coreferenza `compatible` non semanticamente verificata;
- nessuna integrazione S2, Gate o certificazione.

## Decisione indipendente

**REMEDIATION R1/R2 APPROVATA NEL PERIMETRO STATICO MIRATO.**

R1, R2 e le relative proprietà nel percorso esaminato sono **VALIDATO**. Il
significato non si estende alla correttezza complessiva del contratto o al
comportamento semantico/runtime.

## Stati ufficiali

| Componente | Stato |
|---|---|
| Specifica Spatial V2 | **ESEGUITO** |
| Remediation documentale R1–R5 | **ESEGUITO** |
| Revisione documentale R1–R5 | **VALIDATO** |
| Implementazione offline Spatial V2 | **IMPLEMENTATO** |
| Test deterministici iniziali | **ESEGUITO** |
| Remediation R1/R2 | **IMPLEMENTATO** |
| Test differenziali R1/R2 | **ESEGUITO** |
| Revisione indipendente statica R1/R2 | **VALIDATO** |
| Proprietà R1/R2 nel percorso esaminato | **VALIDATO** |
| Validazione complessiva Spatial V2 | **BLOCCATO** |
| Accuratezza semantica e correzione runtime q3_04 | **BLOCCATO** |
| Gate runtime, integrazione S2, certificazione | **BLOCCATO** |
| Provenance Spatial V1 | **VALIDATO** |

## Chiusura

Il ciclo documentale della remediation R1/R2 è chiuso. Non servono ulteriori
remediation o revisioni equivalenti senza nuova evidenza concreta. Nessuna
attività successiva è autorizzata automaticamente.
