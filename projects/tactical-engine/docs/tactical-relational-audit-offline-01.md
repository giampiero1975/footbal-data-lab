# Audit tattico relazionale offline 01

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit codice/test: `b4a5f64`

## Attività

Affiancare al gate lessicale esistente una diagnosi relazionale per
sottoproblema, inizialmente offline, osservabile e non bloccante. Il percorso
predefinito del pannello, il flag `--tactical-plan` e il valore legacy
`complete` non sono stati modificati.

## Implementazione

`v5_tactical_query_plan_v1.py` ora:

- produce per ciascuna parte esplicita della domanda un involucro non
  prescrittivo, senza inventare attore o soluzione;
- estrae segnali per attore, fase, compito, spazio, trigger e finalità a livello
  di singola clausola;
- considera dimostrata una relazione solo quando le dimensioni richieste e gli
  eventuali vincoli espliciti convivono nella stessa clausola;
- distingue compito assegnato all'attore sbagliato e alla fase sbagliata;
- mantiene separato ogni sottoproblema, evitando che una sezione completa
  nasconda una sezione omessa;
- distingue ID di citazione valido, pertinenza tattica e supporto semantico.
  Quest'ultimo resta esplicitamente non verificato dal controllo deterministico.

L'output usa lo schema `tactical_relational_audit_v1`, dichiara
`mode=offline_non_blocking` e `affects_legacy_gate=false`.

## Differenza tecnica e test

Set differenziale non equivalente ai controlli V9/V10 basati su parole o regex:

1. copertura lessicale distribuita senza relazione locale;
2. ruolo e compito corretti in fase sbagliata;
3. compito assegnato al giocatore sbagliato;
4. preventiva generica senza comportamento operativo;
5. un sottoproblema completo e uno omesso;
6. citazione formalmente valida ma fonte tatticamente irrilevante;
7. generazione automatica di involucri non prescrittivi dalla domanda.

Risultati:

- planner/audit: **25/25 PASS** (18 storici + 7 nuovi);
- Tactical State Contract: **48/48 PASS**;
- compilazione: **PASS**;
- diff check: **PASS**.

## Risultato e decisione

La diagnosi ora distingue presenza lessicale e relazione tattica dimostrabile,
ma non assegna voti Coverciano e non certifica la verità semantica delle fonti.
Resta deliberatamente fuori dal runtime bloccante finché non sarà validata su
casi indipendenti completi di domanda, risposta, evidenze e versione runtime.

Stato: audit **IMPLEMENTATO**, test **ESEGUITO**, comportamento offline e
isolamento **VALIDATO**; non **INTEGRATO** e non **CERTIFICATO**.
