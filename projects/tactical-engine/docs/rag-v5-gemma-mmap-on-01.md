# Gemma26 con mmap — singolo tentativo gemma-mmap-on-01

Data: 2026-11-19. Attività esistente
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.

## Risposta conclusiva

**No: questo tentativo non ha dimostrato una risposta completa entro tutti i
vincoli.** È arrivato HTTP200 con stream di ragionamento, ma non il finale.
La raccolta termina con `E_DEADLINE_AMBIGUOUS` nel controller locale.
Il minimo MemAvailable ricevuto è **6156517376 byte (6,157GB)**: nessuna guardia
RAM/paging è scattata nei circa397s campionati. È un cambiamento operativo
rilevante rispetto allo STOP RAM precedente, non un PASS del test completo.

Non attribuire il risultato a insufficienza hardware assoluta, bug Ollama o
impossibilità del modello. Non è dimostrato che Gemma non sappia terminare:
mancano evidenze durante una parte dell'intervallo. Nessun secondo tentativo.

Correzione vincolante del titolare: **Qwen3.5 9B genera, ma la sua qualità
tattica è giudicata insufficiente**. Non viene presentato come soluzione
qualitativamente adeguata; la precedente eseguibilità non risolve tale giudizio.

## Attività → Script → Commit → Report → Risultato → Decisione → Stato

Baseline GitHub/local `44843c9f0c73a5ec82c171caf0f985c129043c03`, branch corretto,
working tree pulito. TODO/registro, audit hardware, protocollo e ledger
storici riconciliati; destinazione gemma-mmap-on-01 assente. Nuova differenza
registrata prima dei controlli: **solo options.use_mmap=true**, mai provato.
Nessuna suite storica ripetuta. Consenso allegato esplicito, max1 POST.

Script: operations/quality-first-pilot/gemma_mmap_on_01.py; osservatore separato
gemma_mmap_observation_01.py, sole letture opzionali senza nuovi privilegi.
Controller one_remote e worker03 riusati byte-per-byte, nessuna alterazione
di monitor, timeout o chiusura. Commit tecnico congelato e pubblicato prima
dell'invocazione: **72ef28eed796c5267711da06e10474f66c6a778c**. Otto controlli nuovi del solo
delta PASS. Scope/consenso/hash in docs/quality-first-pilot-authorized-readiness-01/.

Ledger nuovo fisso esclusivo `evaluation/gemma_mmap_on_01/`, fsync-before-GO,
nessun reset/resume/retry. Richiesta **ESEGUITO**; raccolta custodita e verificata
nel perimetro sotto; completamento/validazione operativa **BLOCCATO**. Nessuna
qualità tattica **VALIDATO**, integrazione, certificazione o promozione.
Il commit finale è quello che introduce questo report, artefatti/TODO/registro
insieme ed è restituito nella consegna, senza SHA autoreferenziale inventato.

## Configurazione e unico delta

- Gemma4:26b Q4_K_M, digest
  001e5dafc3c77684c2307ebc6ab8e336e10c9b18eca52acf547d72fc83c3ca8c.
- Identico V10-02 della revisione03, ordinal1, domande/fonti/istruzioni originali.
- Solo aggiunta use_mmap=true. Rimuovendola dal payload registrato si ottiene
  esattamente il precedente oggetto; verifica finale collection-verification.json.
- Originale payload SHA256 c8211bdb4d43048bbf54aaab32d44b86879329d3eba1c18ead7e899e211038c0;
  nuovo7bc057b52a120ebbc5415ebd22da236f66fd1240421f4b114fcde629a6de97ce.
- num_ctx8192, num_predict4096, temperature1, top_p0.95, top_k64, seed42,
  think=true, keep_alive0 e default draft invariati. Nessuna riduzione qualitativa.
- Supervisore remoto900s TERM/kill-after15s e controller900s invariati;
  MemAvailable>=4000000000 byte, pressione persistente03 immutata.

Preflight prima del GO: host key ED25519 già autorizzata/StrictHostKeyChecking,
utente football, parent timeout/process group, lock esistente esclusivo non
bloccante, versione0.40.5/digest/Q4_K_M, servizi active, nessun altro modello/
runner o generazione concorrente osservabile, memoria iniziale15935758336 byte.
Nessun nuovo modello, Qwen27, warmup, repair, fallback o richiesta ulteriore.

## Confronto con revisione03

| Proprietà | Revisione03 senza opzione esplicita | gemma-mmap-on-01 |
|---|---|---|
| Delta richiesto | use_mmap assente | true, tutto il resto identico |
| Esito trasporto | Nessuno status HTTP | HTTP200, body NDJSON incompleto |
| Ultimo tratto remoto osservato |28,308s allo STOP RAM|397.188s fino all'ultimo campione ricevuto |
| MemAvailable minimo, byte |3763400704|6156517376 |
| RSS runner max campionato, byte |12204212224|15990546432 |
| Guardia RAM/paging |E_MEMORY_RESERVE|Nessuna nei campioni ricevuti |
| Testo finale |Assente|Assente |
| Arresto conclusivo |Monitor RAM|E_DEADLINE_AMBIGUOUS locale, intervallo non osservato |

Il fatto che RSS sia più alto con Available migliore non è contraddittorio:
sono state osservate pagine file-backed, recuperabili diversamente dall'anon.
Picchi opzionali del runner: RssAnon9792454656 byte,
RssFile15696969728 byte; cgroup file_mapped fino
15703814144 byte. **Massimi non necessariamente simultanei,
non sommarli.** Non sono un peak continuo garantito o il fabbisogno minimo.
Campioni cgroup/observer nominali2s; monitor principale nominale1s, timestamp reali.

Memoria/swap e rate/persistenza sono conservati integralmente. C'è stato paging,
ma nessuna condizione E_PERSISTENT_PAGING osservata: non scrivere “zero swap”.
Il margine è rispettato soltanto nell'intervallo ricevuto, non attestabile nel
gap. Servizi monitorati active durante le osservazioni, non SLA RAG sotto carico.

## Caricamento effettivo e limiti di osservabilità

L'osservatore ha letto cmdline su allowlist: modello originale, contesto8192,
parallel1, draft-mtp con3, flash-attn auto, batch/ubatch1024. Nessun flag
load-mode esplicito: compatibile col default auto del backend, **non prova
sufficiente del mode effettivo**. Parametri automatici non furono catturati
nel precedente run: non dichiarare un confronto runtime completo dei default.

RssFile e file_mapped multi-GB sono evidenza concreta di attività file-backed
nel runner/cgroup, coerente con l'ipotesi mmap; non identificano da soli ogni
mapping GGUF o dimostrano l'attribuzione causale esclusiva del miglioramento.
Maps/smaps diretti negati al normale utente (PermissionError): nessun nuovo
privilegio. Nessuna riga mmap disponibile nel filtro journal post-stop,
exit0/stderr vuoto: non è prova di assenza mmap. Non basta HTTP200 per dire
che il flag abbia avuto esattamente l'effetto atteso su tutti i tensori.

## Tempo, token e interruzione della raccolta

- HTTP200 osservato dopo105.658s dal post_started
  remoto: tempo ai soli header, include più fasi, **non load_duration**.
- Ultimo campione remoto ricevuto dopo397.188s.
- Ledger locale GO→STOP wall-clock: **2211.531s**,
  maggiore dei900s configurati. Il controllo locale rientra con scadenza ambigua.
  Le due cronologie non provano900s di copertura continua del modello.
- L'osservatore si interrompe anch'esso senza observer_finished/journal_selection,
  exit1 senza stderr. Non inventare un'uscita ordinata o una causa verificata.
- Manca evidenza nel tratto successivo agli ultimi eventi ricevuti: non
  attribuire senza prova il gap a sleep del PC, rete, scheduler o modello.
  Non è autorizzata un'ulteriore indagine o una seconda POST per recuperarlo.
- Ollama load_duration, eval_duration e durata generazione effettiva: **non
  disponibili**, manca l'evento finale. Tempo totale della generazione non
  attestabile univocamente; riportare separatamente le due misure precedenti.
- 707 chunk ricevuti, 3006 caratteri thinking,
  0 caratteri finale, nessun done=true. **Non sono707 token.**
  Numero token input/output: non disponibile, nessun prompt_eval_count/eval_count.

Una sola POST avviata; il server ha trasmesso ragionamento, quindi non è “zero
attività generativa”. Il numero esatto di token prodotti internamente e
l'eventuale evoluzione non catturata non sono attestabili. Nessun secondo invio,
nessun contenuto ricostruito o corretto. Non esiste una risposta completa da
predisporre per revisione tattica indipendente; il thinking parziale non la
sostituisce, non viene votato o presentato come finale.

## Stato finale e custodia

Una sola diagnostica successiva read-only: ps vuoto, nessun llama-server/runner,
solo daemon Ollama; servizi football-rag-api e Ollama active. MemAvailable
16037191680 byte. Nessun modello lasciato residente
osservato. Non dimostra l'istante esatto di cancellazione o l'esito nel gap.
Nessuna modifica permanente VPS/servizi/config, RAG/panel/corpus/embedding,
modelli, spese, merge o deploy.

Artefatti: invocation/request, activity-created/reserved-before-GO, stdout.raw/
stderr.raw, STOP.json, observer raw/exit, diagnostica finale, summary,
response-body.partial.ndjson, thinking.partial.txt e answer.partial.txt vuoto.
I707 wire originali restano intatti localmente e sono pubblicati byte-per-byte
in wire-originals.zip con wire-inventory.json; stdout conserva anche le copie
base64. Il .gitignore esclude solo le copie individuali duplicate, non il raw
né l'archivio. Verificati archivio↔chunk locali↔stdout e inventario SHA256/dimensioni.
Originali storici01/03/Qwen preservati e hash verificati dopo il tentativo.

**Decisione: STOP, risultato operativo non conclusivo/BLOCCATO.** Mmap ha
permesso un tratto osservato con risposta streaming e margine RAM superiore
rispetto allo STOP precedente, ma nessuna risposta completa dimostrata.
Non dichiarare il modello impossibile né riuscito, INTEGRATO o CERTIFICATO.
Qualsiasi ulteriore prova richiede una nuova autorizzazione e una differenza
tecnica esplicita; nessun retry o altra variante viene eseguito dopo questo esito.
Report, TODO e registro pubblicati contestualmente, GitHub/working tree verificati.
