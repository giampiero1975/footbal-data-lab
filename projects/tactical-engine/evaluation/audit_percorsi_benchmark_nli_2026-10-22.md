# Audit dei percorsi dei benchmark RAG/NLI — 22 ottobre 2026

## Perimetro verificato

Ispezionati direttamente su GitHub: albero del repository, `.gitignore`, `projects/tactical-engine/README.md`, `projects/tactical-engine/experiments/README.md` e gli script Atomic V1, Contrastive V1, Repeatability V1 e Evidence Audit V1.

Non è stato ispezionato il filesystem della VPS: le directory runtime eliminate o presenti non sono verificabili dal solo repository.

## Struttura già esistente nel repository

- `projects/tactical-engine/evaluation/`: valutazioni documentate, gold JSON e registri.
- `projects/tactical-engine/experiments/README.md`: registro esperimenti, manifest minimo, divieti di ripetizione.
- `projects/tactical-engine/eval/`: ulteriore directory esistente; funzione da accertare prima di consolidare.
- `projects/tactical-engine/docs/`: documentazione tecnica.
- `projects/tactical-engine/scripts/`: programmi di prova.

L'albero Git tracciato NON contiene `projects/tactical-engine/evaluation/reports/` al momento di questo audit. Questo non dimostra che la directory non fosse presente sulla VPS o che non fosse la sede storica dei report: Git non traccia directory vuote e i file locali possono non essere versionati.

## Errore introdotto nei nuovi script

I quattro script recenti adottano il percorso relativo predefinito `projects/tactical-engine/evaluation/reports/rag_v5_shadow_*.json` senza verificare il layout runtime preesistente. I benchmark usano `output.parent.mkdir(parents=True, exist_ok=True)`, creando implicitamente una directory se manca. L'audit richiede invece come input un file `rag_v5_shadow_baseline_20261022.json` non presente dopo la pulizia dell'utente.

I test Atomic V1, Contrastive V1 e Repeatability V1 sono stati eseguiti in precedenza e i rispettivi report condivisi nella conversazione. La loro riuscita dimostra che il baseline era disponibile allora, non che esista ancora.

L'audit più recente è fallito con `FileNotFoundError` prima di scrivere l'output. Non è un errore del modello NLI.

## Responsabilità e limiti

È stato un errore procedurale aggiungere output hardcoded e nuove generazioni JSON senza prima censire la struttura esistente e definire una policy di retention. Non è dimostrato che le directory runtime siano state create ex novo da questi script: è dimostrato che gli script possono crearle. Non cancellare né spostare automaticamente altri file.

## Correzioni progettuali da attuare

1. Inventariare le destinazioni runtime già in uso e identificarne una come directory canonica, senza crearne un'altra.
2. Separare i gold e gli input riproducibili dai report generati; un input baseline non deve essere confuso con un report temporaneo.
3. Eliminare l'assunzione che un baseline locale cancellabile sia sempre disponibile: validazione preventiva con messaggio esplicito, mai rigenerazione implicita.
4. Rendere esplicita la destinazione output e impedire `mkdir` silenziosi in percorsi arbitrari.
5. Usare un manifest sintetico per gli esperimenti, con data, commit, checksum, percorso, esito e retention.
6. Applicare una politica di pulizia sicura: mai cancellare gold, baseline o input necessari senza copia verificata.
7. Prima di altri test, verificare coerenza con `experiments/README.md` e documentazione operativa esistente.

## Stato

Audit documentale completato su GitHub. Nessuna modifica agli script runtime o ai dati; nessun test NLI ripetuto. Layout reale della VPS ancora da verificare.
