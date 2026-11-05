# RD-TSC-V2-D3-S2-SPATIAL-RELATION-DIFFERENTIAL-01 — Fase A

## Attivita

Preparazione esclusivamente offline di un Gate diagnostico differenziale per il
contratto opt-in `nli_spatial_relations_v1` 1.0. Nessuna inferenza, chiamata NLI
V2, modifica di etichette, integrazione o attivita VPS e stata eseguita.

Baseline iniziale: `de060ec31a2f8276c33c726cbb765d3a98aefdec`.
Commit tecnico: `9aac9ea761ba29099332d95fbff7d0f2ee8bf9e8`.

## Casi congelati

| Ruolo | Caso | Gold umano | Fonte/pagina | Motivazione |
|---|---|---|---|---|
| regressione nota | `q3_04` | `contradicted` | `verticalizzazione_Bonacini`, 2 | relazione lascia/toglie spazio; il prompt nuovo e lessicalmente esposto, quindi nessuna prova indipendente |
| relazione inversa distinta | `q5_06` | `contradicted` | `Gioco a zona nel calcio`, 2 | avanzamento rapido contro avanzamento piu lento; soggetto e proprieta coincidono, direzione differente e lessico distinto dall'esempio lascia/toglie spazio |
| protezione insufficient | `q5_02` | `insufficient` | `variazione_sistema_gioco_Pane`, 8 | la fonte descrive il ruolo del metodista, ma non dimostra ne smentisce l'effetto immediato del cambio di sistema |

Claim, evidenze e label provengono senza modifiche da
`eval/claim_fidelity_gold_v1.json`, digest canonico LF
`8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c`.
La fixture conserva le label attese separatamente e il runner non le include nel
payload inviato al judge.

`q5_08` e stato escluso: era gia presente nella precedente Fase B e non avrebbe
aggiunto una differenza tecnica. Non sono stati creati casi o giudizi artificiali.

## Confrontabilita V2

Solo `q3_04` dispone di un risultato V2 direttamente attribuibile: stessa claim,
stessa evidenza, `qwen3.5:9b`, V2 storico, temperatura 0, contesto 4096,
`num_predict=1024`, `think=false`, `stream=false`; risultato `supported`
nell'artefatto
`evaluation/tactical_semantic_support_s2_first_controlled_runtime_01.json`.

Per `q5_06` e `q5_02` non e disponibile un artefatto V2 equivalente con tutti i
vincoli verificabili. Non sono quindi pianificate chiamate V2: tali casi misurano
solo la corrispondenza del nuovo contratto alle label congelate. Non sara lecito
dichiarare un miglioramento comparativo generale rispetto a V2.

## Runner e isolamento

- Runner: `scripts/run_tactical_semantic_support_s2_spatial_relation_differential_v1.py`.
- Fixture: `evaluation/tactical_semantic_support_s2_spatial_relation_differential_fixture_v1.json`.
- Test: `tests/test_run_tactical_semantic_support_s2_spatial_relation_differential_v1.py`.
- Attivazione solo tramite `--execute`; modulo inerte all'import.
- Import runtime esplicito del solo
  `shadow_nli_spatial_relations_v1_inference`; nessuna chiamata V2.
- Massimo tre chiamate, nessun retry, repair o fallback positivo.
- Temperatura 0, `num_ctx=4096`, `think=false`, 1024 token e timeout 180 s.
- Digest fixture/dataset e descriptor/digest del contratto registrati.
- Output creato in esclusiva; un output esistente o symlink e rifiutato.
- Primo errore produce `not_evaluable`, arresto e nessuna corrispondenza
  semantica.
- S1 resta invariato e `promotion_authorized=false`; il runner non modifica
  `overall_status` o `promoted_answer`.

## Verifiche offline nuove

Comando eseguito soltanto sulla nuova suite:

```text
python -m unittest tests/test_run_tactical_semantic_support_s2_spatial_relation_differential_v1.py -v
```

Risultato finale: **6/6 PASS** in 0,031 s. Verificati casi/ruoli/digest, separazione
delle label dal judge, limite di tre chiamate, non-promozione, arresto al primo
errore, mismatch digest/label, selezione esclusiva del nuovo contratto e
attribuzione del solo confronto V2 disponibile. Compilazione in memoria dei due
file Python e `git diff --check`: PASS.

La prima esecuzione locale della nuova suite si e arrestata fail-closed con un
mismatch noto CRLF/LF del working tree Windows (1 failure, 4 errori, zero judge
call). Il test harness e stato quindi corretto per materializzare in una directory
temporanea i byte LF canonici gia congelati da `.gitattributes`, senza modificare
dataset, runner o digest. La seconda e definitiva esecuzione ha prodotto 6/6.
Nessuna suite storica e stata ripetuta.

## Interpretazione futura predefinita

- PASS tecnico: chiamate completate con record validi, S1 invariato e nessuna
  promozione.
- Corrispondenza semantica: label valida uguale al Gold congelato.
- `q3_04`: sola regressione nota, senza valore di generalizzazione.
- `q5_06`: controllo distinto della relazione inversa.
- `q5_02`: controllo contro falsa contraddizione.
- Fail-closed: qualsiasi errore resta `not_evaluable`, non semantic match.

Tre casi non definiscono accuratezza generale. Un successo non attribuisce
automaticamente miglioramento su V2, integrazione o certificazione.

## Comando futuro proposto, non eseguito

```bash
cd projects/tactical-engine
python scripts/run_tactical_semantic_support_s2_spatial_relation_differential_v1.py \
  --fixtures evaluation/tactical_semantic_support_s2_spatial_relation_differential_fixture_v1.json \
  --output evaluation/tactical_semantic_support_s2_spatial_relation_differential_01.json \
  --model qwen3.5:9b \
  --ollama-url http://127.0.0.1:11434 \
  --timeout 180 \
  --max-tokens 1024 \
  --execute
```

Il comando richiede una nuova autorizzazione, ambiente isolato riconciliato,
dataset LF con digest conforme, modello disponibile, output assente e assenza di
esecuzioni concorrenti. Non e autorizzato da questa Fase A.

## Risultato, decisione e stato

- Runner e fixture: **IMPLEMENTATO**.
- Verifiche offline differenziali: **ESEGUITO** e proprieta coperte **VALIDATO**.
- Fase A: **ESEGUITO**.
- Esecuzione reale, efficacia semantica e confronto generale V2: **BLOCCATO**.
- Integrazione e certificazione: **BLOCCATO**.

Decisione: preparazione sostenibile e pronta per revisione indipendente. Nessun
runtime deve essere avviato senza nuova decisione esplicita del titolare.
