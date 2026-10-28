# Runtime Coverciano remediation V9

Data: 2026-10-27. Ramo: `codex/rag-coverciano-remediation`.

## Esito

Rerun RAG-only delle stesse dieci domande congelate, senza spalla e senza nuove
chiamate Gemini. Sei evidenze, contesto 8.192, limite 900 token; indice invariato
a 6.410 chunk.

- 10/10 casi salvati, zero citazioni invalide e zero troncamenti;
- tempo medio 215,72 s: -15,1% rispetto a V8 e -5,2% rispetto a V7;
- 9/10 PASS al gate runtime; il solo caso 9 è stato respinto;
- il caso 9 è tatticamente coerente sul principio principale (palla scoperta:
  arretrare; palla coperta: salire), ma il gate interpretava come
  contraddizione la successiva risalita condizionata dopo l'arretramento;
- dopo la correzione relazionale V9.1, la rivalutazione deterministica degli
  output conservati è 10/10 completa.

## Confronto

| Ciclo | Complete al gate | Troncamenti | Tempo medio |
|---|---:|---:|---:|
| V7 | 3/10 | 2 | 227,45 s |
| V8 | 3/10 | 0 | 254,05 s |
| V9 runtime | 9/10 | 0 | 215,72 s |
| V9.1 re-audit | 10/10 | 0 | nessuna nuova inferenza |

I rilievi Gemini congelati della baseline chiedevano soprattutto preventive,
geometria applicativa, azioni successive, comunicazione e distinzione
palla coperta/scoperta. Tali voci risultano ora esplicitamente coperte dal gate
e dalle risposte. Non sono state però richieste nuove valutazioni Gemini: perciò
il miglioramento tecnico è dimostrato, mentre il voto esterno medio >=26/30 non
può essere dichiarato VALIDATO da questo ciclo.

## Decisione

V9 è **ESEGUITA** e il percorso RAG-only è **VALIDATO tecnicamente** sui dieci
casi congelati dopo re-audit 10/10. V9.1 corregge soltanto il falso positivo
relazionale e non rigenera risposte. Il target di voto Coverciano resta
**DA VALIDARE esternamente** su risposte RAG non modificate; non riattivare la
spalla per mascherare eventuali insufficienze.
