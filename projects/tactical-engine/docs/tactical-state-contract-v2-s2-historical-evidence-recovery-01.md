# TSC V2 D3 — recupero probatorio evidenze S2 storiche

Attività: `RD-TSC-V2-D3-S2-HISTORICAL-EVIDENCE-RECOVERY-01`

Baseline: `e75bd2086d3aa79cf3bb5fda7900cc68dddc5cf9`

## Attività → Script → Commit → Report → Risultato → Decisione → Stato

- Attività: ricercare e verificare gli originali NLI/alignment già eseguiti.
- Script: nessun benchmark o test; sole letture, ricerche nominali, confronti e
  inventari metadata-only locali/remoti.
- Commit: commit documentale di report, manifest di riconciliazione e registri.
- Report: questo documento.
- Risultato: 11 artefatti cercati; 0 verificati, 0 parzialmente verificati,
  11 non reperiti, 0 con integrità divergente.
- Decisione: ricognizione probatoria completa e verificabile; recupero dei singoli
  originali ancora **BLOCCATO**.
- Stato: riconciliazione **VALIDATO**; metriche storiche non promosse.

## 1. Perimetro e riconciliazione

Branch, HEAD locale/remoto e working tree coincidevano con la baseline. Sono stati
letti TODO, experiment register, readiness S2, report storici e
`evaluation/runtime_evidence_manifest_v1.json`. La storia Git completa non contiene
gli output originali ai percorsi attesi: il manifest fu pubblicato ai commit
`48e18c1` e `58aa912`, ma conserva soltanto metadata, non blob dei report.

Non sono stati eseguiti inferenze, NLI, reviewer, benchmark, test, retrieval, Chroma,
API, deploy o modifiche a checkout/servizi. Nessun JSON originale è stato copiato,
normalizzato o ricostruito.

Manifest di riconciliazione separato:
`evaluation/nli_historical_evidence_reconciliation_v1.json`.

## 2. Ubicazioni controllate

La ricerca ha usato esclusivamente nomi esatti e percorsi documentati:

1. indice e storia Git locale completa per i percorsi attesi;
2. `C:/Users/Giampiero/Documents/FOOTBALL-DATA-LAB`;
3. `C:/Users/Giampiero/.codex/attachments`;
4. checkout operativo VPS `/opt/football-data-lab/projects/tactical-engine/evaluation`;
5. staging V2 `/home/football/.local/share/football-data-lab/staging/tsc-v2-965d6b6/.../evaluation`;
6. staging V1 `/home/football/.local/share/football-data-lab/staging/tsc-v1-3fa3a18/.../evaluation`.

L'alias SSH risolto era quello approvato (`football@163.5.26.155:22`,
`IdentitiesOnly=yes`). Le directory `runtime-archive` esistono. L'archivio operativo
contiene oggi soltanto `figc_discovery_latest.json` e
`rag_v5_external_drive11_holdout_v1.json`; i due staging contengono soltanto il
secondo. `evaluation/reports` è assente nel checkout operativo. Nessun percorso è
stato creato o modificato.

## 3. Inventario probatorio

| Esperimento | Percorso previsto | Byte/hash attesi | Esito | Predizioni/matrice |
|---|---|---|---|---|
| FIGC/FA 30 | `runtime-archive/benchmark_tactical_nli_source_disjoint_30_v2.json` | 42977 / `f3ef699c…38c81` | NON REPERITO | no |
| stress 100 | `runtime-archive/benchmark_tactical_nli_stress_100_v2.json` | 83135 / `8109e1bf…6140e` | NON REPERITO | no |
| direct external | `runtime-archive/benchmark_direct_three_label_external_v1.json` | 11943 / `45aac88c…3f67` | NON REPERITO | no |
| direct fresh V1 | `runtime-archive/benchmark_direct_three_label_fresh_v1.json` | 16847 / `7910a445…4fde` | NON REPERITO | no |
| direct fresh V2 | `runtime-archive/benchmark_direct_three_label_v2_fresh_v1.json` | 17290 / `a7f478db…82eb` | NON REPERITO | no |
| Atomic 15 | `reports/rag_v5_shadow_atomic_v1_20261022.json` | non registrati | NON REPERITO | no |
| Contrastive 12 | `reports/rag_v5_shadow_contrastive_v1_20261022.json` | non registrati | NON REPERITO | no |
| alignment controls | `reports/rag_v5_alignment_controls_v1.json` | 12080 / `a2ebc19d…0ca2` | NON REPERITO | no |
| alignment judge V1 | `reports/rag_v5_alignment_judge_results_v1.json` | 5441 / `9c4cbdf5…57bd` | NON REPERITO | no |
| alignment judge V2 A/B | `reports/rag_v5_alignment_judge_results_v2_ab.json` | 7913 / `0d2e49c6…8b92` | NON REPERITO | no |
| FA 32 | originale non identificato univocamente | non registrati | NON REPERITO | no |

Gli hash abbreviati in tabella sono solo leggibilità; il manifest JSON conserva gli
otto SHA-256 completi disponibili. Poiché nessun originale è stato trovato, nessun
hash osservato è dichiarato e non esiste alcun caso `INTEGRITÀ NON CONFERMATA`.

## 4. Metriche ricostruibili

Nessuna metrica può essere ricalcolata dagli originali, perché predizioni e label
accoppiate non sono disponibili. Rimangono consultabili soltanto dati aggregati già
documentati:

- sviluppo 24: V2 23/24;
- FA 32: 30/32;
- stress 100: 93/100, distribuzione riportata 28/30 supported, 29/30 contradicted,
  36/40 insufficient;
- FIGC/FA 30: 29/30 3-way, 30/30 binario;
- Atomic 15: 13/15;
- Contrastive 12: 4/12;
- alignment V1: 6/10 complessivi, NLI 4/5, alignment 2/5.

Questi valori non sono stati “verificati” in questa attività. Non sono state
ricostruite artificialmente matrici, falsi positivi o falsi negativi. Restano
documentati, non ricalcolati, gli errori nominati nei report: FIGC/FA
`novel_fa_wide_new_04`, Atomic `low_block_reverse` e `methodist_every`, nonché il
falso positivo alignment `negative_scope_q5`.

## 5. Formato, firme e configurazioni

Senza originali non è possibile verificare leggibilità JSON, firme input,
configurazione effettiva, modello registrato, numero dei risultati o matrice interna.
Codice e dataset sorgente restano disponibili, ma non sostituiscono l'output. Il
manifest storico prova che, il 24 ottobre, file con quei percorsi, byte e digest
furono inventariati; non prova il loro contenuto attuale né consente il replay delle
predizioni.

## 6. Limiti del Gold

Anche un futuro recupero con hash coincidente dimostrerebbe integrità e identità,
non indipendenza scientifica. I dataset NLI erano piccoli/curati, in parte riusati
nello sviluppo e senza doppia review/adjudication/freeze S2. Gold E/V relazionale è
distinto e ancora vuoto. La decisione B della readiness S2 rimane invariata.

## 7. Impatto e intervento minimo

La ricognizione chiarisce che non serve un nuovo benchmark: serve una copia originale
preesistente. Il minimo intervento è individuare un backup esplicitamente nominato o
una copia dell'operatore, quindi trasferire/leggere ciascun file senza trasformazioni
e confrontare byte/hash con questo manifest. Tale accesso richiede una nuova
autorizzazione sul percorso concreto; non è autorizzata una scansione generale o una
rigenerazione.

## 8. Stati ufficiali

- Ricognizione probatoria: **VALIDATO**.
- Recupero degli 11 originali: **BLOCCATO**.
- Metriche storiche: evidenza documentale aggregata, non promossa a **VALIDATO**.
- Readiness S2: decisione **B** invariata; attività precedente **ESEGUITO**.
- Gold S2, implementazione S2 e Gate: **BLOCCATO**.
- Integrazione e certificazione runtime: **BLOCCATO**.
