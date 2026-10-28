# Tactical State Contract v1 — remediation consolidata 01

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit codice/test: `0d69be6`

## Attività

Chiusura differenziale dei sette difetti relazionali rimasti dopo
`RD-TSC-V1-RELATIONAL-CORRECTION-01`, senza intervenire su Qwen/Ollama, runner,
API, pannello, corpus, indici, produzione o servizi esterni.

## Difetti e correzioni minime

1. Le espulsioni proprie multiple sulla stessa transizione ora concorrono a un
   unico delta aggregato; sostituzioni, rotazioni ed espulsioni avversarie non
   riducono la cardinalità della nostra squadra.
2. Il rientro viene ricostruito sul grafo degli stati e non sull'ordine del
   vettore `events`; una cronologia non dimostrabile non viene inventata.
3. Il renderer sopprime gli eventi dipendenti da un ciclo globale o da una
   transizione bloccata, preservando i fatti indipendenti.
4. Le formulazioni `esce il 7, entra il 9` registrano entrambi gli attori come
   riferimenti espliciti con disponibilità ignota.
5. Gli archi verso stati inesistenti producono `invalid_event_edge`, senza
   eccezioni durante i controlli successivi.
6. `presence_complete=true` richiede che gli attori `on_field` coincidano con
   `effective_players`.
7. Quando mapping e assegnazioni concrete sono disponibili, la posizione
   finale di ogni attore persistente deve rispettare il mapping; dati
   insufficienti restano qualificati e non vengono inventati.

## Test differenziali

Sono stati aggiunti soltanto sette casi non equivalenti ai 41 già presenti:

- due espulsioni proprie sulla stessa transizione;
- stessi cambi serializzati in ordine inverso;
- ciclo globale con rendering degli eventi coinvolti;
- destinazione temporale inesistente;
- sostituzione con numeri nudi;
- presenza completa incoerente con cardinalità;
- assegnazione concreta incompatibile con il mapping dichiarato.

Risultati locali:

- contratto: **48/48 PASS**;
- planner storico: **18/18 PASS**;
- `py_compile`: **PASS**;
- `git diff --check`: **PASS**.

## Risultato e decisione

I sette difetti risultano riprodotti dai nuovi test rispetto al comportamento
precedente e chiusi dalla modifica minima del commit indicato. La validazione è
esclusivamente offline e riguarda gli invarianti coperti. Il percorso resta
isolato dal runtime: nessun merge o deploy è stato eseguito.

Stato: codice **IMPLEMENTATO**, test **ESEGUITO**, remediation consolidata
**VALIDATO** offline; non **INTEGRATO** e non **CERTIFICATO**.
