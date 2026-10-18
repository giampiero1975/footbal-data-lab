# DRIBBLING — indice operativo

Questo repository documenta configurazioni, verifiche e sperimentazioni del RAG tattico. **Non assumere che il codice Git corrisponda allo stato runtime della VPS senza un controllo di sincronizzazione.**

## Punto di partenza (evitare controlli ripetuti)
1. Leggere [todo.md](todo.md) per priorità e attività aperte.
2. Leggere [docs/environment.md](docs/environment.md) per l'ultima fotografia verificata della VPS e la sua validità.
3. Leggere [docs/components.md](docs/components.md) per modelli, versioni, abbinamenti e stato dei componenti.
4. Leggere [docs/verification.md](docs/verification.md) per verificare **solo** i dati mancanti o scaduti.
5. Consultare [experiments/README.md](experiments/README.md) prima di ripetere un benchmark.
6. Leggere [docs/decisions.md](docs/decisions.md) per evitare di riaprire scelte già motivate.

**Non cambiare V4, cancellare collection o disinstallare modelli durante un audit.** I report di sola lettura possono essere versionati dopo revisione per escludere segreti e dati personali. I file voluminosi e gli indici restano fuori da Git.

La struttura qui è documentale: nessuno script è stato spostato, nessuna configurazione runtime è stata modificata.
