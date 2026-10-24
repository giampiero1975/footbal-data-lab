# SCRIPT-CLASSIFICATION-V2

Data: 2026-10-24. Stato: VALIDATO.

## Attività

Classificare tutti gli script Python senza spostarli o cancellarli, preservando
import, link documentali e riproducibilità.

## Script e report

- scanner: `scripts/audit_script_dependencies.py`;
- manifest: `evaluation/script_inventory_v2.json`;
- conteggio: 200 script, inclusi i due scanner di inventario; zero errori di
  sintassi.

## Classi operative

| Azione | Numero | Significato |
|---|---:|---|
| `keep` | 32 | runtime, manutenzione/freeze o test di regressione |
| `keep_guarded` | 7 | ingestion e builder che possono scrivere indici |
| `archive_in_place` | 161 | benchmark, diagnostiche, shadow e strumenti storici |

`archive_in_place` è una classificazione logica: i file restano in `scripts/`
per non spezzare import e riferimenti nei report. Tutti i 199 script occupano
circa 1.7M, quindi una rimozione fisica produrrebbe un risparmio trascurabile e
peggiorerebbe la tracciabilità.

## Decisione

Non cancellare o spostare script. Usare il manifest per distinguere il percorso
operativo dal materiale storico. Un futuro refactoring della struttura richiede
test di import/regressione e aggiornamento atomico dei link.

## Stato

VALIDATO sulla VPS: compilazione dei due scanner superata e classificazione
completa senza errori sintattici.
