# Protocollo Coverciano 100 — RAG-only

Data: 2026-10-26  
Stato: **IMPLEMENTATO** per requisiti e isolamento; baseline ridotta dal
titolare a 10 casi ed **ESEGUITA**. Esito nel report omonimo.

> Emendamento del 2026-10-26: il titolare ha richiesto “arriviamo solo a 10 e
> ci fermiamo”. Le regole sotto restano la definizione del protocollo esteso,
> ma questa sessione si arresta tassativamente a 10 e non costituisce un
> benchmark 100/100.

## Obiettivo vincolante

Misurare e portare il RAG autonomo a un voto medio minimo di **26/30** su 100
domande inedite formulate e valutate da Gemini Cloud come commissione
Coverciano. Il voto riguarda sempre la risposta RAG non modificata.

## Flusso unico ammesso

1. Gemini Cloud formula una domanda inedita da esame allenatore/Coverciano.
2. La domanda viene inviata dal pannello pubblico al RAG.
3. Il pannello mostra la risposta RAG integrale e le evidenze recuperate.
4. La stessa risposta, senza correzioni o riscritture, viene sottoposta a Gemini
   Cloud per voto in trentesimi e motivazione.
5. Si registra il caso e si richiede la domanda successiva.

OpenRouter resta nel codice ma deve essere disabilitato durante l'intero
benchmark. Nessuna seconda AI puo correggere, completare o riscrivere la
risposta prima del voto.

## Tracciamento obbligatorio per ciascun caso

- numero progressivo 1–100 e identificativo job;
- testo integrale della domanda;
- risposta RAG integrale;
- evidenze e citazioni;
- tempi, token e stato tecnico;
- voto Gemini /30 e giudizio;
- errori tattici, omissioni, problemi di retrieval e problemi di generazione;
- versione del codice, modello, collection e configurazione rilevante.

I casi del benchmark precedente con spalla attiva restano evidenza storica ma
non concorrono alla nuova media.

## Regole di arresto e sviluppo

- Non fermarsi fra i casi per chiedere conferme ordinarie.
- Arresto obbligatorio dopo il caso 100.
- Nessun caso oltre il numero 100.
- Al caso 100 produrre report completo con distribuzione voti, media, mediana,
  minimo/massimo, tempi, token, errori per categoria, cause e costi esterni.
- Target di accettazione: media RAG >=26/30. Un voto finale alto prodotto da
  una seconda AI non conta.
- Le correzioni del RAG devono derivare dai risultati osservati. Ogni modifica
  richiede differenza tecnica documentata, test offline e nuova versione del
  benchmark; non alterare retroattivamente risposte o voti gia registrati.

## Ruolo futuro della spalla

Fuori da questo benchmark, la spalla potra essere riattivata solo dopo che il
RAG avra raggiunto autonomamente il target. Dovra esaminare, controbattere e
proporre delta supportati; non potra sostituire la risposta né superare il 30%
del contributo finale.

