# Preparazione locale del pilot esistente

Attività: `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
Baseline decisionale `227a862dedf5f36c947ec63dface69c723af1e99`.
Il pilot rimane **DA FARE**. Questa fase autorizza solo preparazione e controlli
locali non generativi. Nessuna modalità execute o worker è stata eseguita.

## File e comandi locali

- `paired_pilot_01.py`: preparazione, verifica identità del package, controllo
  dell'autorizzazione separata, controller futuro e anonimizzazione.
- `paired_pilot_remote_01.py`: worker futuro Linux stdin-only; una sola POST
  loopback per slot dopo GO, lock esistente read-only e monitoraggio. Oggi
  soltanto AST/compilazione in memoria, mai importato/eseguito.
- `static_review_01.py`: controlli nuovi sul delta, senza import dei driver;
  non ripete test applicativi o benchmark. Scrive un'evidenza esclusiva.
- `prepared/pilot_manifest_01.json`: tre input filtrati, sei payload e ordine,
  hash dei casi e del codice. Nessuna risposta precedente o Gold.
- `prepared/remote_binding.pending.json`: dossier remoto mancante, non una
  dichiarazione di compatibilità. Tutti i gate restano false.
- `prepared/execution_authorization.pending.json`: autorizzazione false.
- `prepared/blind_review_form.json`: scheda vuota, nessun voto attribuito.

Eseguiti soltanto `python -B paired_pilot_01.py prepare`, `check` e il lettore
statico. `prepare` rifiuta una directory prepared esistente; `check` non usa
rete, SSH, app RAG, modelli o tokenizer. Il package è congelato byte-per-byte
con `.gitattributes`; modificare driver/worker/casi invalida il check. Non
rigenerare package o risultati per rimuovere una divergenza senza registrarla.

## Profilo predisposto, non verificato sul backend

Input: V10 case02, V10 case03, V10.2 case10 con hash approvati. Ogni coppia ha
identici messaggi, fonti, pagine, ordine e istruzioni generali; whitespace/OCR
delle stringhe originali preservati. Whitelist: domanda e cinque campi delle
sei evidenze (label/id/source/pages/text); non l'intero record storico.

Gemma26: `gemma4:26b`, Q4_K_M llama.cpp, prefisso catalogo `001e5dafc3c7`.
Qwen27: `qwen3.8:27b`, Q4_K_M llama.cpp, prefisso `aaee06c39dcf`.
Serve comunque digest completo e corrispondenza effettiva sul servizio;
un prefisso non è attestazione sufficiente. Stesso think=true nei payload;
la sua risoluzione al profilo Gemma thinking e Qwen xhigh è **non verificata**.
Il driver non sostituisce xhigh con medium, né inventa campi API.

Parametri predisposti: contesto 8192, output totale 4096, stream=true,
keep_alive=0, seed 42, temperatura 1/top_p0.95; top_k 64 Gemma  / 20 Qwen.
Qwen esplicita min_p 0/presence_penalty0/repeat_penalty1; per Gemma i restanti
valori effettivi devono essere documentati dal dossier prima dell'approvazione.
Seed42 è un punto predefinito senza ricerca del seed migliore, non garanzia di
determinismo. Il supporto effettivo di ogni opzione è un gate, non un PASS
locale. Risposta finale entro 350 parole: conteggio whitespace split, separato
dal reasoning, nessun taglio automatico o giudizio tattico del driver.

Non c'è un tokenizer alternativo o un conteggio byte→token. Il dossier deve
legare ciascun conteggio al payload esatto, digest modello, identità template/
tokenizer, metodo supportato ed evidenza con hash. Il controller richiede
prompt_tokens positivo <=4096, così da riservare output 4096 nel contesto 8192.
Il worker confronterebbe inoltre il contatore del servizio col valore attestato.
Questo confronto successivo non sostituisce la prova prima della POST.

## Ledger, custodia e STOP predisposti

Una sola directory canonica `evaluation/quality_first_paired_pilot_01`, senza
--output alternativo, reset o resume. Creazione esclusiva all'avvio esecutivo;
qualunque esistenza impedisce un nuovo tentativo. Tale directory oggi non esiste.
Prima di ogni GO il controller salva una prenotazione con apertura xb,
flush/fsync; errori e stati ambigui arrestano l'intero pilot. Una prenotazione
non prova che il servizio abbia ricevuto la POST: conteggi e ambiguità vanno
letti dai raw, senza secondo tentativo. Può terminare prima di sei risposte.

Il worker predisposto controlla identità football, parent timeout e process
group, versione/digest/quantizzazione, modelli già caricati, processi noti,
servizi richiesti, symlink/proprietario e flock non bloccante del lock storico.
Non crea/chmod lock o directory remota, non cambia servizi o configurazioni.
Campiona MemAvailable, swap e RSS/HWM dei processi osservabili; target un secondo,
con letture servizi/processi periodiche. Cadenza/reazione reali non misurate:
riportare timestamp e massimo campionato, non un picco continuo garantito.

Margine proposto 4 GB decimali, nessun nuovo paging swap; timeout del controller
900s per slot e 5400s totale, supervisore remoto GNU timeout 900s TERM /kill-after15s.
La finestra di cleanup del supervisore può aggiungere 15s al processo remoto;
il controller smette di attendere al proprio tetto 900s. Non si dichiara che il
modello Ollama sia terminato entro quel tempo: socket chiuso, timeout e kill
SSH **non dimostrano cancellazione della generazione**. Lo stato resta ambiguo,
STOP e nessun altro invio; è limite concreto da verificare nel preflight.

Raw NDJSON in byte, stdout/stderr e metadati sono preservati; errore HTTP,
stream incompleto, length, mancato finale/contatori, memoria, servizi o unload
non osservato portano a STOP. Nessun post aggiuntivo di warm-up/unload o repair.
Un arresto tecnico non attribuisce zero tattico o una vittoria al superstite.

L'export cieco è consentito solo con sei slot conclusi e inventario verificato.
Conserva il content esatto, esclude thinking/metadati/prestazioni/identità e
mescola i pacchetti con ID opachi. La mappa custode resta FUORI dalla cartella
blind: inviare al revisore soltanto blind, non l'intero ledger. Eventuale
identità auto-rivelata nel testo va annotata come rottura del cieco senza
riscrivere l'originale. Voti e cause restano vuoti per il revisore umano.

## Prerequisiti remoti ancora mancanti

Nessun digest completo, template effettivo, controllo thinking o contatore
token della build installata è attestato dal package. Il dossier non è un
verificatore remoto automatico: richiede evidenze reali e revisione esplicita,
poi un'autorizzazione separata legata agli hash del piano e del dossier.
I boolean verified/checks non sostituiscono le evidenze: non compilarli
per far superare i gate. Nessuna API tokenizer attendibile è dimostrata qui.
Se non esiste un metodo supportato senza generazione/caricamento pesi, STOP;
nessun vecchio percorso ABI, installazione o conteggio inventato.

Il successivo preflight da autorizzare separatamente comprende esclusivamente:
SSH alias football-vps con host key verificata; GET version/tags/ps; eventuale
POST non generativa /api/show dei soli due modelli già presenti; letture di
metadati/template/config e del metodo di rendering/tokenizzazione esistente;
memoria/swap/processi/servizi/spazio e metadata/symlink/permessi del lock, senza
acquisirlo o modificarlo. Assenza di tentativi precedenti da riconciliare.
Nessun download/caricamento, chiamata chat, warm-up o cambio runtime implicito.
Acquisizione lock, modelli mancanti, sei generazioni e raccolta esecutiva
richiedono le autorizzazioni successive appropriate.

Le 32 verifiche sono statiche/di manifest, non test funzionali del trasporto,
monitoraggio o compatibilità della VPS. La prima versione del lettore statico
si è fermata su un matcher della stringa GO; corretto con ispezione AST senza
eseguire il worker. Risultati finali in
`docs/quality-first-pilot-local-preparation-static-01.json`.

Preparazione **IMPLEMENTATO**; controlli locali **ESEGUITO** e **VALIDATO**
solo nel perimetro dichiarato. Pilot **DA FARE**, esecuzione non autorizzata;
prerequisiti non attestati impediscono invio. Accuratezza 28/30, Gate,
integrazione e certificazione generale restano **BLOCCATO**. RAG preservato.


## Revisione operativa02 (2026-11-11)

Le sezioni precedenti descrivono la preparazione storica. Il titolare ha
autorizzato esecuzione e revisione mirata: Qwen think="xhigh" esplicito,
conteggi API osservati dopo la risposta invece di prova preventiva non disponibile.
Binding execution_binding_02.json: non attesta tokenizer, no-truncation o
applicazione interna dei profili. Limiti e STOP invariati, massimo sei invii.
Dettagli e limiti nel report protocollo, addendum Revisione operativa02.
