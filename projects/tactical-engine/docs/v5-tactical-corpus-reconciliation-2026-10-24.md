# Riconciliazione corpus tattico — 2026-10-24

Stato: ESEGUITO (inventario nominale); indicizzazione aggiuntiva: DA FARE, non autorizzata.

## Perimetro
Solo cartella Google Drive **tattica** e `knowledge/sources/formations-and-systems` VPS; escluse `tecnica` e `Allenamenti`. Un file privato non calcistico è stato trovato accidentalmente in Drive: **escluso permanentemente dal corpus e da ogni download/ingestion**; nome e contenuti non riportati nel registro per riservatezza. Non eliminare da Drive senza istruzione esplicita.

## Evidenze
- Inventario VPS `football_pdf_inventory.txt`: 141 PDF.
- Log Chroma `lista_pdf_indicizzati.log`: 5319 chunk, 141 valori source distinti; corrispondenza nominale 140/141, più normalizzazione del nome Ussia (PDF `Transizioni.Ussia. Master Allenatore PRO.pdf`, source `Transizioni.Ussia.json`). Metadati di provenienza e completezza dei testi non ancora verificati.
- API Google Drive sulla cartella tattica: 153 PDF restituiti, mentre UI utente segnala 154; scarto di un elemento ancora non riconciliato. Confronto nomi: 12 file presenti su Drive ma non VPS, **uno privato da escludere**, dunque 11 candidati da valutare prima di trasferire.
- Gli 11 candidati calcistici, non ancora acquisiti: `tesi-lorenzon-uefa-pro.pdf`, `vulcano-luciano_tesi-master.pdf`, `06_i_TH_Principi_-_Sistema_di_gioco.pdf`, `baldini-francesco_tesi.pdf`, `maldera_tesi-uefa-pro.pdf`, `contran_uefa-pro.pdf`, `vincenzo-italiano_tesi.pdf`, `19_prestigiacomo.pdf`, `343_costruzione.pdf`, `01_redazionale.pdf`, `preview1.pdf`.
- Decisione storica confermata dall'utente: i PDF non erano stati caricati appositamente per non alterare gli esperimenti in corso. Non classificare come guasto di ingestion.
- Benchmark locked: 5/10, da non confrontare direttamente con altri set 7/10 o valutazioni preliminari 9/10. Obiettivo operativo intermedio almeno 8/10, gate progetto 9/10 ancora aperto.

## Decisione e prossimi passi
1. Conservare collection e benchmark esistenti senza modifiche; niente reindicizzazione della collection V5.
2. Verificare la discrepanza Drive 153/154 e analizzare pertinenza/duplicati dei soli 11 PDF candidati, senza scaricare file privati.
3. Prima di ogni patch consultare documentazione ufficiale pertinente (Drive API, Docling, Chroma, LlamaIndex, Sentence Transformers) e confrontare le versioni runtime.
4. Per l'eventuale espansione usare collection candidata isolata e differenziale tecnicamente motivato; non ripetere benchmark equivalente. Dopo ciascun report aggiornare TODO e registro.

Flusso: Attività = riconciliazione; Script = comandi read-only inventario VPS/Chroma e ricerca Drive; Commit = presente nella cronologia GitHub; Report = questo documento; Risultato = 141 VPS/141 source, 11 candidati calcistici non trasferiti; Decisione = esclusione file privato e preservazione baseline; Stato = ESEGUITO.
