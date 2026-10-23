# V5-EXERCISE-HEADING-ACCEPTANCE-PLAN-01

Stato: ESEGUITO - piano documentale, nessun nuovo test.

## Evidenze gia disponibili
- V5-EXERCISE-EXTRACT-V2-OFFLINE-01: Ussia 34 unita, confini specifici corretti. Non ripetere.
- V5-EXERCISE-HEADING-COVERAGE-OFFLINE-01: 141 documenti, 3 con intestazioni V2, 38 con altre convenzioni, 183 intestazioni alternative. Inventario, non ground truth.
- V5-EXERCISE-HEADING-FAMILIES-DESIGN-01: cinque famiglie, distinzione exercise_start/section_boundary, review_required.

## Campione minimo motivato
A. `smarcamento_marcamento.json`: numerazione alternativa, esempi `Esercitazione n. 1` (ripetuto), `ESERCITAZIONE n. 2 - 8 > 8 con due jolly`, `ESERCITAZIONE n. 3 - 2 > 2+8`. Delta rispetto a V2: prefisso n., descrizione nello stesso heading e numeri ripetuti.
B. `la_punta_centrale_Gritti.json`: intestazioni descrittive senza identificativo progressivo, come `Esercitazione per il tiro al volo.`. Delta rispetto a V2: ID assente, titolo semantico.
C. `Allegati_2832014181753.json`: 5 intestazioni V2 e tre esempi con due punti `Esercitazione 4:`, `7:`, `8:`. Delta: convenzioni miste nella stessa fonte. Questo documento NON sostituisce un benchmark V2 completo.

## Protocollo proposto per successiva ispezione read-only (non eseguito)
Per ogni documento del campione, raccogliere solo heading candidati e i due heading adiacenti, label, self_ref e pagine. Escludere testo integrale, embedding, generazione e Chroma. Annotare manualmente per ciascuno: exercise_start, section_boundary, review_required, oppure non_exercise; giustificazione e riferimento Docling. Le etichette non sono verita fino a revisione.

## Criteri di accettazione prima di implementare V3
1. Ogni heading candidato ha sorgente, self_ref e pagina quando disponibile; nessun riferimento inventato.
2. I titoli plurali/di capitolo non diventano esercitazioni per semplice match lessicale.
3. `n. 1` ripetuto non collide: identita distinta tramite source + self_ref.
4. Rapporti giocatori `8 > 8`, `2 > 2+8` non vengono interpretati come ID.
5. `Esercitazione 4:` e varianti con suffisso sono candidate ma non automaticamente confermate senza contesto.
6. Ambiguita e pagine assenti sono esplicite, non corrette per supposizione.
7. Se l'evidenza non consente una separazione affidabile, lasciare review_required e NON indicizzare come unita certa.
8. Nessun replay Ussia, test retrieval V5, benchmark E2E o scrittura Chroma.

## Condizione per autorizzare una verifica nuova
Controllare nuovamente TODO, registro, codice e report. Solo se nessun precedente contiene gia una revisione di confini per i tre documenti indicati, eseguire una singola ispezione differenziale documentata. Altrimenti riconciliare i risultati esistenti e non ripetere il lavoro.

## Decisione
La fase successiva e la raccolta di evidenze di contesto per famiglie alternative, non una nuova regex universale o indicizzazione. La V2 rimane invariata.
