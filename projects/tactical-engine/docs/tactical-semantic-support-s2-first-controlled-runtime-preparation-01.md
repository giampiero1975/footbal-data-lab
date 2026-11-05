# RD-TSC-V2-D3-S2-FIRST-CONTROLLED-RUNTIME-01

## Attivita

Preparazione offline del primo esperimento reale controllato del percorso
D3 → S2 Shadow Adapter → NLI V2 Bridge. La fase descritta qui non ha eseguito
inferenze: rende riproducibile e fail-closed una futura osservazione singola,
subordinata a nuova autorizzazione del titolare.

## Script e fixture

- Runner: `scripts/run_tactical_semantic_support_s2_first_controlled_runtime_v1.py`.
- Fixture: `evaluation/tactical_semantic_support_s2_first_controlled_runtime_fixture_v1.json`.
- Dataset sorgente gia versionato: `eval/claim_fidelity_gold_v1.json`.
- SHA-256 del dataset sorgente:
  `fdd6d9383493f58abd6d9a07fe0a029ecc7dc35bad106fe91ce747fb2463a605`.
- Commit tecnico: `c985a916b35f88633cb37778a7a429fca218c807`.

La fixture riusa tre casi con etichetta umana gia presente; non crea label,
claim o evidenze nuove:

| Caso | Label attesa | Motivo diagnostico |
|---|---|---|
| `q3_05` | `supported` | preservazione di una condizione sull'offside |
| `q3_04` | `contradicted` | inversione della relazione spaziale contro blocco basso |
| `q5_08` | `insufficient` | quantificatore universale oltre l'enunciato modale della fonte |

Questi casi non costituiscono Gold S2 indipendente e non consentono una stima
dell'accuratezza semantica.

## Differenza tecnica

Le campagne precedenti hanno validato separatamente adapter e bridge con mock.
Questa preparazione verifica il loro attraversamento congiunto, l'identita
content-addressed degli input, il limite massimo di tre chiamate, l'arresto al
primo risultato non valutabile e l'invarianza dell'assessment S1. S2 resta
shadow: `promotion_authorized=false` in ogni esito. Il runner isolato non riceve
e non modifica `overall_status` o `promoted_answer`; la loro invarianza resta
coperta dalle regressioni dual-output gia registrate.

## Comando della futura Fase B — non eseguito

Da eseguire dalla directory `projects/tactical-engine`, soltanto dopo preflight
dell'ambiente e nuova autorizzazione esplicita:

```bash
python scripts/run_tactical_semantic_support_s2_first_controlled_runtime_v1.py \
  --fixtures evaluation/tactical_semantic_support_s2_first_controlled_runtime_fixture_v1.json \
  --output evaluation/tactical_semantic_support_s2_first_controlled_runtime_01.json \
  --model qwen3.5:9b \
  --ollama-url http://127.0.0.1:11434 \
  --timeout 180 \
  --max-tokens 1024 \
  --execute
```

Configurazione congelata: `temperature=0`, `num_ctx=4096`, `think=false` nel
judge NLI V2 esistente, massimo tre inferenze, timeout 180 secondi per chiamata,
nessun retry e nessun repair. Il limite interno massimo e 540 secondi piu
overhead locale. L'output e creato in modalita esclusiva e non sovrascrive un
artefatto esistente.

## Test offline eseguiti

Comando:

```text
python -m unittest tests/test_run_tactical_semantic_support_s2_first_controlled_runtime_v1.py tests/test_v5_tactical_semantic_support_s2_nli_v2_bridge.py tests/test_v5_tactical_semantic_support_s2.py -v
```

Risultato: **20/20 PASS** in 0,061 s. Copertura nuova: digest e bilanciamento
della fixture, tre chiamate mock senza promozione, timeout mock fail-closed con
arresto dopo una sola chiamata e digest sorgente alterato. Compilazione in
memoria PASS; guardia senza `--execute` PASS con exit 2 prima dell'import del
runtime NLI; `git diff --check` PASS. Nessuna inferenza e nessun artefatto runtime
sono stati prodotti.

## Prerequisiti e condizioni di arresto

Il Python locale 3.13 usato nella preparazione non dispone di `pydantic`,
dipendenza importata dal modulo NLI storico. Non sono state effettuate
installazioni. Prima della Fase B occorre attestare un ambiente isolato con le
dipendenze gia disponibili, il modello `qwen3.5:9b`, l'endpoint locale previsto,
l'assenza dell'artefatto di output e l'assenza di un'esecuzione concorrente.

Arresto senza retry in caso di digest divergente, fixture o caso malformato,
dipendenza/modello/endpoint non disponibile, output preesistente, eccezione o
risultato `not_evaluable`. Nessuna chiamata successiva e consentita dopo il
primo errore.

## Risultato, decisione e stato

- Runner e fixture: **IMPLEMENTATO**.
- Test differenziali offline: **ESEGUITO**.
- Identita, isolamento, non-promozione e fail-closed coperti dai mock:
  **VALIDATO** offline.
- Fase B con inferenze reali: **DA FARE** e **BLOCCATO** fino a nuova
  autorizzazione e preflight ambientale conforme.
- Accuratezza semantica, Gold S2 indipendente, Gate, integrazione e
  certificazione: **BLOCCATO**.

La presente preparazione non autorizza inferenze, benchmark, VPS, deploy o
integrazione.
