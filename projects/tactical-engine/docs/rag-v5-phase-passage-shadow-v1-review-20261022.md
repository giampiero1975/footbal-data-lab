# RAG V5 — Passage Shadow V1: adjudication mirata (2026-10-22)

## Provenienza e vincoli
Report fornito in chat: `rag_v5_phase_passage_shadow_v1.json`, schema `rag_v5_phase_passage_shadow_v1`, status `complete`, source_sha256 `84639f12da1fecbc6ca750626bb612bb2106b88b3e70847d5807d09144dce006`. Modello `qwen3.5:9b`. Policy dichiarata: `frozen evidence, unchanged labels, no Chroma`. Questa è un'analisi offline del report, non verifica SSH né certificazione della configurazione runtime. Confronto entro lo stesso report tra `previous_answer` e `answer`; non equivale a un confronto end-to-end V4/V5.

## holdout_06
Domanda: priorità della transizione positiva in funzione della zona di recupero. Ablazione: drop F5, F7; restano F1, F3, F4, F8. Durata 117.38 s; `invalid_citation_ids=[]`. La nuova risposta riconosce che F1 propone zona alta/media/bassa per *misurare* progressione controllata, non detta una matrice di priorità zona→azione. F3 chiede di valutare punto e situazione; F4 distingue sfruttamento squilibrio vs stabilizzazione. Rispetto alla risposta precedente, minore rischio di trasformare il contesto in regola universale. **Triage: miglioramento qualitativo plausibile; non PASS gold** (adjudication atomica indipendente mancante).

## holdout_10
Domanda: prima giocata dopo riconquista senza confondere transizione positiva e possesso consolidato. Modifica F3: `keep_definition`, 1507→270 caratteri; 7 evidenze F1,F2,F3,F4,F6,F7,F8. Durata 194.33 s; `invalid_citation_ids=[]`. Migliora la distinzione dalla transizione negativa. Persistono claim da correggere/verificare:
- «le zone alte sono generalmente più efficaci per generare progressioni controllate» non è supportato come confronto statistico da F1/F4: F1 descrive un esercizio e una valutazione sulla zona alta.
- «le zone basse richiedono tempi più lunghi per l'organizzazione» non deriva dagli estratti citati.
- Un primo passaggio di consolidamento **non determina di per sé** che la fase sia già possesso consolidato; F6 colloca il confine nella ricostruzione di un'organizzazione riconoscibile.
- Il collegamento tra 10 contro 0 (progressione didattica) e scelta di gioco in gara non va trattato come causalità.
**Triage: REVIEW, non PASS**.

## Esito e gate
Entrambe le risposte hanno zero citazioni con ID invalido; questo verifica solo sintassi, non entailment. Nessun punteggio 9/10 o promozione V5. Non modificare Chroma, collection, prompt canonico, baseline V4 o holdout pilota. Applicare `docs/rag-v5-quality-holdout-adjudication-rubric-20261022.md` e `docs/rag-v5-quality-9of10-validation-protocol-v1.md` prima di un test indipendente.

## TODO operativo
- [x] Ricezione e lettura Passage Shadow V1.
- [x] Confronto qualitativo previous/new per 06 e 10 e registrazione criticità.
- [ ] Adjudication atomica indipendente claim↔fonte, senza tuning sul pilota.
- [ ] Confronto con ablation e baseline usando artefatti originali e manifest; non inventare numeri mancanti.
- [ ] Preparare regressione separata per fase di gioco, zona e tipo di giocata.
- [ ] Verificare documentazione ufficiale delle API effettivamente coinvolte prima di implementare il prossimo script.

## Audit deterministico eseguito su report originale (22/10/2026)
- Input: `rag_v5_phase_passage_shadow_v1.json`; SHA256 del file `2d56c6058459542d5f920c1b93611d677f4f4d2a41ffcfa770f266b1c041ae57`.
- Script versionato: `scripts/audit_rag_v5_phase_passage_regression_v1.py`, eseguito in ambiente isolato con Python stdlib, non sulla VPS.
- Output: `rag_v5_phase_passage_regression_audit_v1.json`, schema valido, `QUESTIONS 2`.
- `holdout_06`: 0 citazioni invalide; 1 segnale positivo euristico; `semantic_pass=not_adjudicated`.
- `holdout_10`: 0 citazioni invalide; 3 flag `manual_review` (efficacia zone alte, durata zone basse, esercitazione 10 contro 0); `semantic_pass=not_adjudicated`.
- **Limite**: matching lessicale mirato; non è un giudice NLI né un test completo di regressione generativa. Nessun miglioramento end-to-end certificato.
- **Prossimo gate**: adjudication claim-by-claim e confronto con ablation originale; non eseguire nuove generazioni sull'holdout pilota per tuning.
