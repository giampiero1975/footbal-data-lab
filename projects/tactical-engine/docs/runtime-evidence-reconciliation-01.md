# RUNTIME-EVIDENCE-RECONCILIATION-01

Data: 2026-10-24. Stato: VALIDATO.

## Attività

Riconciliare i JSON runtime non tracciati sulla VPS senza pubblicare contenuti
potenzialmente riservati o perdere evidenze richiamate dai report Git.

## Script e manifest

- scanner: `scripts/inventory_runtime_evidence.py`;
- manifest pubblico senza contenuti: `evaluation/runtime_evidence_manifest_v1.json`;
- 87 file JSON, 2.724.476 byte complessivi;
- per ogni file: percorso, dimensione, SHA-256 e classe.

## Classificazione

| Classe | File | Decisione |
|---|---:|---|
| certificazione | 4 | mantenere sulla VPS; hash pubblicabile |
| diagnostica | 55 | mantenere come archivio runtime |
| storica | 26 | mantenere come archivio runtime |
| review riservata | 2 | non pubblicare senza revisione privacy |

I contenuti non sono stati copiati in Git. I 2.7M complessivi non giustificano
una cancellazione che renderebbe non verificabili report e decisioni. Il
manifest consente controllo duplicati e integrità senza esporre estratti.

## Riordino fisico

Quindici JSON sperimentali e diagnostici presenti direttamente nella radice
`projects/tactical-engine/` sono stati spostati in
`evaluation/runtime-archive/`. La radice ora contiene zero JSON. L'unico
default di output che puntava ancora alla radice è stato corretto; i riferimenti
documentali sono stati aggiornati e il manifest rigenerato.

## Decisione

Conservare i JSON in sede sulla VPS e trattarli come archivio runtime. Ogni
nuovo report deve essere scritto sotto `evaluation/`, mai nella radice. Prima di
pubblicare, spostare o eliminare un file, verificarne hash e riferimenti nel
registro. Non considerarli working tree sorgente.

## Stato

VALIDATO.
