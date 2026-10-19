# Verifica runtime mirata — esecuzione futura sulla VPS

**Non eseguita.** Scopo: colmare esclusivamente i dati mancanti rispetto a `environment.md`, senza ripetere l'inventario CPU/Python/Ollama già documentato. Nessuna modifica, nessuna cancellazione.

## Regole

- Un comando alla volta, attendere e registrare l'output prima del successivo.
- Prima di qualunque modifica confrontare commit GitHub/VPS, preservare configurazione funzionante e predisporre rollback.
- Non eseguire automaticamente `git pull`, `pip install`, `ollama pull`, `chroma delete` o migrazioni.
- Registrare data, output sintetico e stato in `environment.md`; non ripetere controlli invariati.

## Sequenza di controlli read-only

1. **Servizi/entry point:** censire systemd/cron e processi effettivi che richiamano tactical-engine, annotando script e parametri. Non assumere che `ask_dribbling.py` sia la pipeline attiva.
2. **Collection Chroma:** leggere nome, count, configurazione metrica e metadati; accertare se V4 usa cosine o metrica predefinita. Non inferire la metrica dalla sola metadata description.
3. **Dipendenze degli script:** mappare import, invocazioni, output e report per classificare in uso/storico/esperimentale; non eliminare file sulla base del nome.
4. **Cache e spazio disco:** occupazione Chroma, Hugging Face, Ollama e file temporanei; distinguere dati sorgente, modelli condivisi e artefatti rigenerabili.
5. **Wrapper versionati:** verificare nel venv reale l'implementazione `OllamaEmbedding` (istruzioni query), `CitationQueryEngine` (split/citazioni) e `SentenceTransformerRerank` (truncation).
6. **Baseline:** snapshot leggibile di commit, digest modelli, collection, prompt, filtri, parametri, test gold, latenza e RAM/CPU sotto carico. Backup verificato prima di scrivere.
7. **Esperimenti:** solo dopo i passi precedenti, eseguire quelli in `../experiments/README.md`, una variabile alla volta.

## Criteri di chiusura

Il controllo è chiuso soltanto quando output, data, versione, fonte ufficiale pertinente e decisione sono registrati. Se un controllo non può essere eseguito, annotare “non verificato”, non inventare il risultato.
