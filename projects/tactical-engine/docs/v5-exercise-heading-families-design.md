# V5-EXERCISE-HEADING-FAMILIES-DESIGN-01

Stato: ESEGUITO - progettazione documentale, non validazione.

## Evidenze
V5-EXERCISE-EXTRACT-V2-OFFLINE-01 e V5-EXERCISE-HEADING-COVERAGE-OFFLINE-01 sono gia registrati. Inventario read-only su 141 file Docling: 3 contengono intestazioni compatibili V2 (Ussia 34, DeRosa 8, Allegati_2832014181753 5); 38 documenti contengono 183 intestazioni alternative. I gruppi possono sovrapporsi. Non ripetere le verifiche Ussia.

## Famiglie e decisioni
1. Numerazione esplicita isolata: "Esercitazione 4/A", "Esecitazione 10". Mantenere il comportamento V2; non estendere automaticamente.
2. Numerazione alternativa: "Esercitazione n. 1", "Esercitazione 4:", "Situazione n.1", "ESERCITAZIONE POSSESSO 1". Candidati da contestualizzare. I numeri in "1 contro 1", "4>4" e "4 : 6" descrivono rapporti di gioco e non sono identificativi sicuri.
3. Titolo descrittivo singolare: "Esercitazione per il tiro al volo", "Situazione di 4>4 nella meta campo". Possibili unita con chiave basata su sorgente e riferimento Docling, senza inventare numerazioni.
4. Titolo di sezione o collettivo: "ESERCITAZIONI", "ESERCIZI", "SITUAZIONI DI GIOCO", "Esercitazioni per il pressing". Non aprire unita automaticamente.
5. Titoli generici: "PROPOSTA DIDATTICA", "Situazione didattica", "Allenamenti:". Richiedono evidenza sul contesto; default review_required.

## Confini e provenienza
Distinguere esplicitamente eventi exercise_start e section_boundary; un titolo generico puo chiudere l'esercitazione corrente senza avviarne una. Usare label title o section_header e conservare self_ref, provenienza, numero pagina, titolo originale e sorgente. Escludere voci del sommario come esercitazioni autonome. Per unita molto lunghe replicare titolo e provenienza su ogni segmento senza mescolare esercizi. Usare identificativi versionati e stabili basati almeno su sorgente e heading_ref, non sul solo numero esposto. Se non si trovano intestazioni riconosciute, non inferire assenza di esercitazioni; potrebbero stare nel corpo testo o nelle figure.

## Controlli futuri, non eseguiti
Prima riconciliare codice, report e commit esistenti. Solo se manca evidenza specifica, esaminare offline intestazioni e contesto Docling di una fonte con numerazione alternativa (esempio smarcamento_marcamento.json) e una con titoli descrittivi (esempio la_punta_centrale_Gritti.json). Documentare campione, accettazione e casi ambigui prima di implementare un classificatore opt-in. Non ripetere benchmark, mapping Ussia o retrieval gia completati.

## Decisione
Nessuna regex universale non verificata. Nessun cambiamento a collection Chroma V5, runner, gold o stato di certificazione. Prossimo passo: specifica dei casi e identificazione di evidenze ancora insufficienti.
