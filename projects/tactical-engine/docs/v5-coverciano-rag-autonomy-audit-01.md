# V5 Coverciano — audit autonomia RAG 01

Data: 2026-10-26  
Stato: **ESEGUITO** per diagnosi offline; correzioni **DA FARE**  
Perimetro: prime 16 prove effettuate dal pannello pubblico. Nessuna nuova
generazione RAG, chiamata OpenRouter o modifica alla collection.

## Decisione immediata

Il benchmark Coverciano e sospeso. Le valutazioni elevate ottenute sulla
risposta finale non dimostrano la qualita autonoma del RAG: il revisore e stato
implementato come secondo autore e produce una risposta sostitutiva completa.
Non riprendere le prove finche la bozza RAG non raggiunge almeno 26/30 e non e
dimostrato un rapporto di contributo RAG >=70%, spalla <=30%.

Il voto 28/30 attribuito nominalmente alla prova 16 dopo la sospensione e
**INVALIDO**: alla riapertura del pannello la sessione non era autenticata e il
testo trasmesso alla commissione era il segnaposto `Connettiti per iniziare`.
La commissione ha ricostruito impropriamente un giudizio dal contesto storico.
La domanda 17 generata in quella risposta non deve essere usata.

## Evidenza quantitativa disponibile

| Prova | RAG s | token RAG | voto interno bozza /10 | caratteri RAG | caratteri finale | voto esterno finale /30 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 127,25 | 555 | 2 | 2.257 | 5.831 | 30 |
| 2 | 167,13 | 554 | 3 | 2.399 | 6.742 | 30 |
| 3 | 143,57 | 591 | 10 | 2.281 | 5.892 | 30 |
| 4 | 161,40 | 623 | 2 | 2.401 | 6.102 | 30 |
| 5 | 168,00 | 524 | 2 | 2.199 | 5.892 | 30 |
| 6 | 182,16 | 658 | 2 | 2.391 | 5.713 | 30 |
| 7 | 178,72 | 568 | 3 | 2.434 | 6.123 | 30 |
| 8 | 178,84 | 684 | 3 | 2.721 | 5.271 | 30 |
| 9 | 163,01 | 399 | 4 | 1.621 | 6.262 | 30 |
| 10 | 136,13 | 523 | 4 | 1.957 | 6.355 | 29 |
| 11 | 186,70 | 633 | 3 | 2.711 | 6.643 | 29 |
| 12 | 158,23 | 478 | 2 | 1.948 | 6.892 | 29 |
| 13 | 158,16 | 449 | 2 | 1.693 | 7.023 | 29 |
| 14 | 163,24 | 485 | 3 | 1.923 | 6.467 | 29 |
| 15 | 132,47 | 456 | 2 | 1.921 | 7.122 | 29 |
| 16 | 161,27 | 499 | 2 | 2.026 | 5.799 | non valutato validamente |

Sintesi:

- 15 bozze su 16 ricevono 2–4/10 dal revisore interno;
- media interna 3,06/10 e mediana 2/10;
- il solo 10/10 della prova 3 e un outlier da verificare, non una prova di
  affidabilita;
- lunghezza media bozza RAG 2.180 caratteri, risposta finale 6.258 caratteri:
  espansione media 2,87x;
- i voti 29–30/30 riguardano la risposta riscritta, non la bozza RAG;
- il revisore interno non e un giudice indipendente: e lo stesso percorso che
  successivamente riscrive la risposta. I suoi voti sono diagnostici, non una
  misura causale definitiva.

La precedente stima RAG 25–35% / spalla 65–75% resta una stima qualitativa. Il
campione prova la dominanza operativa della spalla, ma non consente ancora una
percentuale validata concetto per concetto.

### Stima diagnostica per caso

La persistenza attuale non conserva un diff semantico concetto per concetto.
Le percentuali seguenti non sono quindi una misura certificata di authorship:
sono intervalli diagnostici ricavati congiuntamente da voto interno della
bozza, rapporto di lunghezza bozza/finale, ampiezza delle correzioni ed errori
strutturali. Il `massimo testuale RAG` e soltanto un limite superiore: assume,
in modo irrealistico, che ogni carattere della bozza sia sopravvissuto.

| Prova | massimo testuale RAG | stima RAG | stima spalla | motivazione sintetica |
|---:|---:|---:|---:|---|
| 1 | 38,7% | 15–25% | 75–85% | bozza 2/10; finale 2,58 volte piu lunga |
| 2 | 35,6% | 25–35% | 65–75% | bozza 3/10; correzione strutturale ampia |
| 3 | 38,7% | 70–85% | 15–30% | unico 10/10; outlier da non generalizzare |
| 4 | 39,3% | 15–25% | 75–85% | bozza 2/10; riscrittura dominante |
| 5 | 37,3% | 15–25% | 75–85% | bozza 2/10; riscrittura dominante |
| 6 | 41,9% | 15–25% | 75–85% | bozza 2/10; riscrittura dominante |
| 7 | 39,8% | 25–35% | 65–75% | bozza 3/10; finale molto piu estesa |
| 8 | 51,6% | 25–35% | 65–75% | bozza 3/10; lunghezza non prova sopravvivenza semantica |
| 9 | 25,9% | 30–40% | 60–70% | bozza 4/10 ma testo finale 3,86 volte piu lungo |
| 10 | 30,8% | 30–40% | 60–70% | bozza 4/10; correzione ancora maggioritaria |
| 11 | 40,8% | 25–35% | 65–75% | bozza 3/10; finale 2,45 volte piu lunga |
| 12 | 28,3% | 15–25% | 75–85% | bozza 2/10; finale 3,54 volte piu lunga |
| 13 | 24,1% | 15–25% | 75–85% | bozza 2/10; finale 4,15 volte piu lunga |
| 14 | 29,7% | 25–35% | 65–75% | bozza 3/10; correzione maggioritaria |
| 15 | 27,0% | 15–25% | 75–85% | bozza 2/10; finale 3,71 volte piu lunga |
| 16 | 34,9% | 15–25% | 75–85% | bozza 2/10 con ruoli incompatibili; voto esterno invalido |

Usando il centro degli intervalli, il campione e circa **29% RAG / 71%
spalla**. Il dato e coerente con la precedente stima aggregata, ma resta
diagnostico finche non esiste il diff semantico persistente richiesto dal gate
di attribuzione.

## Conformita ai requisiti e origine della deviazione

Il requisito originario era esplicito. La Fase A del copilot dichiarava che
Groq doveva produrre diagnosi tattica e verifica documentale e che **nessun
percorso modifica automaticamente la risposta RAG**. Il reset del protocollo
definiva la seconda AI come spalla per errori, omissioni, geometria e
miglioramenti. La successiva espressione `si compone una risposta finale` non
autorizzava una sostituzione integrale e avrebbe dovuto essere subordinata a un
limite di contributo e a una misura separata della bozza.

La deviazione e entrata nel codice in due passaggi:

1. commit `a77420e`: l'integrazione live ha aggiunto a PASS2 l'ordine di
   `riscrivere una risposta finale concreta e completa`, mentre il progetto
   originario prevedeva soltanto finding e verifica;
2. commit `86a64b0`: dopo un voto esterno 25/30, per inseguire il target >=28,
   PASS1 e stato obbligato a produrre `replacement_answer` e PASS2 a usarla
   come ossatura e a sostituire integralmente le parti errate.

Questa e una non conformita dell'implementazione, non una modifica richiesta
dal titolare. I test verificavano schema, ID, citazioni, fail-closed e trasporto,
ma mancava un test sul rapporto di contributo RAG/spalla. L'ottimizzazione sul
voto finale ha quindi premiato il secondo autore e nascosto la debolezza della
bozza.

Non e ancora dimostrato che il RAG sia regredito rispetto a un benchmark
Coverciano equivalente: il benchmark locked precedente aveva dominio e rubriche
piu circoscritti. Le 16 prove dimostrano invece che il profilo corrente non
generalizza ai nuovi scenari complessi. Per distinguere regressione software da
limite preesistente serve un confronto offline sugli stessi casi congelati tra
commit precedenti e corrente, senza spalla e senza nuove valutazioni esterne.

## Cause accertate

### 1. La spalla e configurata come autore sostitutivo

In `scripts/groq_tactical_copilot_v2.py`, il PASS1 impone una
`replacement_answer` completa e autosufficiente. Il PASS2 ordina di usare tale
risposta come ossatura, riscrivere la risposta finale e sostituire integralmente
le parti errate. Questa configurazione contraddice il ruolo dichiarato di spalla
e rende inevitabile che OpenRouter faccia il lavoro principale.

### 2. Retrieval semanticamente vicino ma tatticamente mal orientato

Le domande sono scenari lunghi e multi-vincolo. Il dense retrieval usa la
domanda intera, recupera 24 candidati e il cross-encoder sceglie gli estratti
piu simili lessicalmente. Non esiste ancora una scomposizione generale della
traccia in sistema proprio, sistema avversario, fase, lato, problema,
transizione, punteggio, minuto e vincoli.

La conseguenza e documentata dalla ricorrenza di poche fonti anche quando la
prospettiva non coincide:

- `Affrontare con il 4-4-2 un avversario schierato con il 3-4-1-2`: 14
  evidenze distribuite in 10 prove;
- `Allegati_2832014181753`: 14 evidenze in 10 prove;
- manuale sul trequartista 3-4-3/5-3-2: 8 evidenze in 6 prove.

Nella prova 16 il RAG risponde a un problema di possesso 3-4-2-1 contro 4-4-2
introducendo un trequartista avversario, due nostre punte e nostri terzini:
ruoli incompatibili con la traccia e derivati da evidenze con prospettiva
diversa.

### 3. Il controllo strutturale avviene troppo tardi

`structural-routing` riserva estratti aggiuntivi, ma non costruisce prima una
mappa vincolante dei 22 ruoli e non rifiuta evidenze che descrivono la squadra,
la fase o la direzione del confronto sbagliate. Il prompt contiene avvertenze,
ma un'istruzione testuale non compensa un contesto contraddittorio.

### 4. Il prompt grounded-only impedisce l'applicazione prudente dei principi

Il system prompt richiede che ogni affermazione tattica sostanziale abbia una
citazione e permette ruoli/azioni solo quando la fonte li specifica. Per
domande applicative arbitrarie e impossibile aspettarsi una fonte che descriva
esattamente minuto, risultato, sistemi, lato e giocatori. Con retrieval debole,
il modello sceglie fra rifiutare la soluzione o trasferire letteralmente ruoli
da uno scenario diverso. Entrambi i comportamenti sono osservati.

### 5. Modello e budget non sono proporzionati al compito

La bozza usa `qwen3.5:9b`, `think=False`, contesto 8192 e risposta concisa entro
350 parole quando e configurato il limite. Le prove richiedono lettura
geometrica, piu fasi, alternative, trigger, preventiva e talvolta cambi/slot.
Le uscite osservate sono 399–684 token. Questo profilo era sufficiente per il
benchmark locked a rubriche note, ma non dimostra generalizzazione su casi
Coverciano complessi.

### 6. I gate verificano forma e integrita, non adeguatezza tattica

`run_rag_v5_query.py` accetta la risposta se esiste una citazione, gli ID sono
validi e l'indice non cambia. Non verifica:

- coerenza dei ruoli con i sistemi della domanda;
- copertura di tutti i vincoli;
- direzione corretta del confronto;
- pertinenza semantica delle citazioni;
- presenza di un piano operativo completo.

La certificazione locked 10/10 resta valida nel proprio perimetro, ma non era
una certificazione delle domande arbitrarie. Il pannello ha impropriamente
esposto il profilo certificato come se generalizzasse a qualunque scenario.

### 7. Persistenza insufficiente per un benchmark auditabile

La cronologia completa resta nel browser e viene cancellata alla chiusura.
Domande e risposte sono conservate nei file privati della VPS, ma il pannello
non consente un export cumulativo affidabile. La perdita della sessione ha gia
prodotto una valutazione esterna falsa per la prova 16.

## Piano correttivo vincolante

1. Disattivare la composizione sostitutiva della spalla. La risposta mostrata
   come finale deve restare quella del RAG; la spalla produce soltanto delta
   strutturati, massimo 30% dei concetti.
2. Introdurre un parser deterministico della domanda e una mappa strutturale
   esplicita prima del retrieval: squadre, sistemi, ruoli, lati, fase, minuto,
   risultato, cambi/slot e richieste.
3. Eseguire retrieval per sottoproblemi e non soltanto sulla domanda intera;
   applicare filtri di prospettiva e fase prima del rerank.
4. Separare tre classi di contenuto: fatti documentali citabili, applicazione
   dei principi al caso e giudizio tecnico dichiarato. Le ultime due non devono
   fingere una citazione letterale inesistente.
5. Aggiungere gate pre-generazione e post-generazione su ruoli, sistemi,
   copertura dei punti, attribuzione dei lati e vincoli numerici.
6. Rivalutare modello locale, ragionamento e budget solo dopo aver corretto il
   retrieval; non usare la spalla per mascherare il confronto.
7. Salvare per ogni caso domanda, evidenze, bozza RAG, delta spalla, risposta
   finale, tempi, token, costo e giudizio esterno in un report persistente.
8. Ripartire con tre casi congelati rappresentativi e punteggio esterno della
   bozza RAG **prima** della spalla. Gate di prosecuzione: media RAG >=26/30,
   nessun errore strutturale grave e contributo spalla <=30%.

## Decisione

Non ripetere le 100 prove e non usare i voti finali gia ottenuti come prova di
qualita RAG. Prima attivita tecnica: trasformare OpenRouter da autore a revisore
delta-only e costruire il gate strutturale del RAG. Nuovi test soltanto dopo
implementazione documentata, su casi congelati e senza riutilizzare il voto
finale come misura della bozza.
