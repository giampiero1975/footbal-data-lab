# Protocollo di verifica incrementale

Prima di ogni nuovo controllo: leggere todo.md, verificare l'ultima evidenza registrata e ripetere solo ciò che è cambiato.

Per ogni verifica annotare: componente, versione effettiva, configurazione, data UTC, fonte ufficiale, evidenza, risultato, evento che ne richiede la ripetizione.

Distinguere: verificato nel repository, verificato sulla VPS, raccomandazione ufficiale, ipotesi ed esperimento.

Trigger: cambio prompt -> fedeltà; cambio embedding -> retrieval e compatibilità; cambio reranker -> ranking; cambio LLM -> generazione; cambio dipendenze -> versioni e regressioni; cambio VPS -> inventario runtime.

Durante troubleshooting: un comando per volta e attendere output. Preservare baseline V4 e definire rollback prima di modificare. Non eliminare modelli, collection o dati senza inventario, verifica dipendenze, backup e approvazione.

Conservare su Git solo manifest e report sintetici non sensibili. Indici, PDF, pesi e dump grandi restano fuori Git. Riferimenti: https://git-scm.com/docs/gitignore e https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits
