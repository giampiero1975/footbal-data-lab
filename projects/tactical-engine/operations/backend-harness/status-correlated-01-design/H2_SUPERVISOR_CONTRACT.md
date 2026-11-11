# H2 — Contratto futuro del supervisore e finalizzazione esterna

Precisazione documentale IMPLEMENTATO. Nessun supervisore, script o gruppo di
processi è creato o eseguito. Nessuna soglia definitiva viene assegnata.
Implementazione/esecuzione BLOCCATO; attestazione ABI DA FARE.

## Policy di risorse da definire e approvare separatamente

Ogni parametro deve avere unità, ambito, meccanismo di enforcement attestato e
provenienza dell'approvazione. Un campo assente/non approvato non significa
illimitato: impedisce l'avvio. I timeout Qwen non sono default di questo progetto.

| Parametro futuro | Contratto richiesto | Valore attuale |
|---|---|---|
| deadline_wall_clock | Durata massima positiva e finita misurata con clock monotono; indipendente dalla CPU; include exec/loader, conversione e parser | NON DEFINITO, non approvato |
| cpu_budget | Budget CPU approvato con ambito di gruppo e metodo di misura/enforcement; per-processo non equivale a totale dei discendenti | NON DEFINITO, non approvato |
| memory_budget | Limite memoria approvato del gruppo e registrazione del picco; distinguere RSS, memoria totale e address space, senza chiamarli equivalenti | NON DEFINITO, non approvato |
| output_budget | Limiti separati e aggregati per stdout, stderr, grammatica, diagnostica e inventari; registrazione dei byte realmente conservati | NON DEFINITO, non approvato |
| stop_grace | Intervallo finito fra arresto controllato e terminazione forzata; non estende il permesso di svolgere lavoro utile | NON DEFINITO, non approvato |
| finalization_budget | Risorse e durata proprie del finalizzatore esterno, con spazio e destinazione attestati; non consumabili dal worker | NON DEFINITO, non approvato |

Le soglie richiedono analisi di risorse e successiva approvazione distinta.
Non è stata eseguita tale analisi, né importata una durata da runtime precedenti.
Prima del lancio il supervisore deve avere già capacità di misurare/enforzare
la policy e finalizzare; se non può, non deve creare il worker.

## Contenimento e arresto

H1 e la policy approvata devono essere soddisfatti prima di qualsiasi tool o
worker. Il gruppo controllato comprende il processo iniziale e tutti i
processi figli/ausiliari. Un semplice PID o process group senza prova contro
escape, riuso di identità o discendenti distaccati non è sufficiente. Il futuro
meccanismo deve essere attestato (contenimento OS e identificazione stabile),
con rete/servizi esclusi, ambiente minimo, FD e filesystem controllati.

Il supervisore/finalizzatore deve rimanere fuori dal gruppo da terminare,
con risorse proprie limitate e riservate. Il deadline monotono inizia prima
dell'avvio del gruppo e non viene riavviato dai messaggi di progresso. Il tempo
UTC serve alle evidenze, non al calcolo del limite di durata.

Fasi tecniche, non nuovi stati del progetto:

1. **Pre-avvio:** policy, identità H1, contenimento, risorse, clock, destinazione
   e possibilità di finalizzare verificati. Altrimenti arresto E_H2_PRESTART.
2. **Osservazione:** acquisire flussi separati entro i limiti, metadati del
   gruppo e metriche; non affidare al worker la vigilanza sui suoi limiti.
3. **Arresto controllato:** al primo trigger registrato interrompere nuovo
   lavoro, registrare clock/causa, richiedere arresto dell'intero gruppo.
   Nessun retry o riavvio automatico.
4. **Terminazione forzata:** se il gruppo non termina entro la grace approvata,
   forzare la terminazione di tutti i membri tramite identità/contenimento
   attestati; osservare terminazione e raccogliere gli esiti disponibili.
5. **Finalizzazione esterna:** indipendente dalla presenza di JSON del worker;
   scrivere il risultato del supervisore e gli inventari parziali.
6. **Chiusura:** marcatore finale soltanto dopo evidenze di terminazione e
   inventario coerente. Se tale prova manca, finalizzazione incompleta, non
   completamento tecnico o successo.

## Categorie di arresto e prove minime

Sono reason code tecnici, non etichette di stato del progetto. Cause multiple
vanno conservate; il trigger primario è scelto dall'ordine osservabile dei log,
non per produrre un esito favorevole. Concorrenza/ordine incerto va dichiarato.

| Categoria | Evidenza necessaria | Cosa non inferire |
|---|---|---|
| E_H2_EXCEPTION | Diagnostica tipata/strutturata affidabile e stadio del worker, con exit/stream associati | Non è automaticamente incompatibilità schema |
| E_H2_LOADER | Fallimento exec/loader o diagnostica verificabile prima dell'ingresso nel worker | Un generico crash non basta a classificare il loader |
| E_H2_CRASH | Segnale, core metadata se disponibili e exit osservati dal supervisore | Non attribuire causa C++ o ABI senza prova |
| E_H2_OOM | Evento/counter del contenimento memoria o evidenza OS correlata al gruppo/intervallo | SIGKILL o exit 137 da soli non provano OOM |
| E_H2_WALL_TIMEOUT | Scadenza del deadline monotono registrata dal supervisore | Non confondere durata con consumo CPU |
| E_H2_CPU_LIMIT | Evidenza del limite CPU applicato al suo ambito attestato | Un exit nonzero non prova superamento CPU |
| E_H2_MEMORY_LIMIT | Evidenza del limite memoria e dell'azione applicata | Limite address-space e OOM del sistema non sono sinonimi |
| E_H2_OUTPUT_LIMIT | Soglia approvata raggiunta, flusso/byte conservati e troncamento registrati | Non presentare un file troncato come cattura integrale |
| E_H2_WORKER_PROTOCOL | JSON assente/non valido, stadio non verificabile o stadio dichiarato incoerente | Il finalizzatore non deve inventare un JSON converter riuscito |
| E_H2_SIGNAL_UNKNOWN | Segnale/exit osservato senza causa sufficientemente provata | Conservare causa non determinata, non sostituirla con OOM |
| E_H2_CONTAINMENT | Impossibilità di garantire/controllare l'intero gruppo | Arresto e prova di sicurezza incompleta, non successo |
| E_H2_FINALIZATION | Errore inventario, hash, I/O o durata del finalizzatore | Nessun marcatore finale di successo con evidenze mancanti |

Ogni categoria arresta il flusso utile e passa alla raccolta esterna. Se i limiti
output sono raggiunti, il supervisore mantiene la capacità di fermare il gruppo:
non deve bloccarsi attendendo un pipe pieno. La parte persa è dichiarata, non
ricostruita. Le eccezioni C++ non sono l'unico canale di errore.

## Evidenze parziali e stato finale verificabile

Il finalizzatore esterno conserva almeno: attività/identità del tentativo,
policy e autorizzazione di riferimento, gate H1 disponibili, tempi UTC e
monotoni, identità del gruppo, trigger e segnali/exit osservati, metriche,
stdout/stderr separati, grammatica e JSON effettivamente ricevuti, byte persi
o non quantificabili, e prova di cessazione dei processi quando ottenibile.
Per ogni artefatto: ruolo, percorso autorizzato, tipo file, byte realmente
persistiti e SHA-256. Rifiutare collisioni, symlink e sovrascrittura di evidenze
precedenti; non alterare il contenuto per farlo risultare valido.

Hash e inventario possono essere parziali ma non inventati. Un worker senza
JSON non impedisce al supervisore di emettere la sua diagnostica strutturata;
se anche la finalizzazione fallisce, segnalarne esplicitamente l'incompletezza.
Il marcatore finale deve essere pubblicato in modo atomico e verificabile
soltanto dopo il controllo dell'inventario; la strategia I/O va attestata prima
dell'avvio. Non è creata alcuna directory di artefatti in questa attività.

Esiti di conversione, parsing, ledger H3 e finalizzazione sono campi separati.
Un exit zero non basta; un inventario coerente non prova enforcement semantico.
`promotion_authorized=false` sempre. Nessuna fase può promuovere backend o
accuratezza generativa. I manifest approvati non sono modificati da H2.
