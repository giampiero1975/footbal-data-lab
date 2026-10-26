# Reset protocollo Coverciano — Gemini esaminatore, Groq copilot

Data: 2026-10-26. Stato: **ESEGUITO** per riconciliazione e singola prova
manuale; automazione e benchmark **DA FARE**.

## Decisione corretta

Il flusso autorevole è:

1. Gemini Cloud formula una domanda inedita da commissione UEFA Pro/Coverciano.
2. Il RAG risponde usando il corpus documentale e citazioni verificabili.
3. Groq analizza la risposta come spalla tattica: errori, omissioni, geometria
   di campo e possibili miglioramenti.
4. Un passaggio separato verifica quali suggerimenti sono supportati dalle
   evidenze recuperate e quali richiedono ulteriore retrieval.
5. Si compone una risposta finale senza inventare contenuti non supportati.
6. Gemini Cloud, nello stesso contesto d'esame, valuta la risposta finale.

Gemini non è il generatore batch del benchmark e Groq non deve completare le
50 domande mancanti. I 50 casi prodotti dal vecchio protocollo non sono casi
validi del nuovo percorso e non concorrono ad alcuna media.

## Evidenza preliminare

Caso manuale del 2026-10-26: costruzione 4-3-3 contro pressione alta a uomo del
4-2-3-1. Job RAG `ad41e872d5f44a66a7626f8429f30e5e`, durata osservata circa
170 secondi. La prima risposta era generica e non descriveva adeguatamente lo
spazio creato, il movimento chiave e l'uso del portiere.

Groq `openai/gpt-oss-120b` ha evidenziato le lacune tattiche; il controllo
documentale ha mostrato anche classificazioni imperfette, quindi i suoi giudizi
non sono accettati automaticamente. La risposta finale ha esplicitato:

- portiere più due centrali come prima linea 3 contro 2;
- terzini alti e larghi per allungare i riferimenti;
- numero 4 mosso lateralmente per svuotare il corridoio centrale;
- mezzala o numero 9 come terzo uomo in controtempo;
- preventiva 2+1 dopo il superamento della pressione.

Google AI Mode ha valutato la risposta **30/30 con lode**, assegnando 10/10 ai
quattro nuclei. L'evidenza è stata osservata nell'interfaccia conversazionale;
non esiste un export firmato del provider. Per questo il caso è **ESEGUITO** e
promettente, ma non `VALIDATO`, `INTEGRATO` o `CERTIFICATO`.

## Artefatti obsoleti

La VPS contiene `evaluation/coverciano-100-chunks-v1/` con 50 domande del
vecchio protocollo. La directory è separata da indici, PDF, report RAG e
collection. Il titolare ne ha richiesto l'eliminazione e il riavvio del
benchmark secondo il flusso corretto. Prima e dopo la rimozione devono essere
registrati percorso risolto, numero di file e dimensione; nessun altro artefatto
Gemini/Groq deve essere rimosso.

Gli script di generazione restano temporaneamente come evidenza storica nel
repository, ma non sono entry point operativi e non devono essere eseguiti.

## Prestazioni e criteri del prossimo intervento

La qualità della prova non compensa la latenza. Il target iniziale è 30–45 s
end-to-end. L'ottimizzazione deve misurare separatamente retrieval, reranking,
generazione RAG, due passaggi Groq e composizione. Nessun risultato può essere
ottenuto disattivando il gate citazioni o riducendo arbitrariamente le fonti.

## Stato

- riconciliazione del protocollo: **ESEGUITO**;
- prova manuale singola: **ESEGUITO**;
- vecchio benchmark 50/100: **BLOCCATO** e fuori perimetro;
- pulizia runtime mirata: **VALIDATO**; percorso risolto esattamente, 9 file e
  156 KB prima della rimozione, directory assente dopo; nessun altro artefatto
  Gemini/Groq o indice interessato;
- ottimizzazione latenza: **DA FARE**;
- copilot applicativo: **DA FARE**;
- benchmark 100 corretto: **DA FARE**.
