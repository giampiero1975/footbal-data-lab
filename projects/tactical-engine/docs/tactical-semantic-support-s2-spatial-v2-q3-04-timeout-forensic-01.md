# RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-TIMEOUT-FORENSIC-01

## Baseline e riconciliazione

Revisione forense read-only del singolo tentativo Spatial V2 `q3_04`.

- HEAD documentale iniziale:
  `ed0ba5403899687ff85cfb8b2e0631cb4a85803d`;
- baseline runtime congelata:
  `009f76e71c0351da9d2b797ad3c9ff1928671a4e`;
- staging e artefatti originali invariati;
- nessuna diagnosi forense equivalente già registrata.

TODO, experiment register, report del run, preflight e preparazione staging sono
stati riconciliati. Non è stato creato o eseguito alcuno script tecnico, test o
modello; sono state effettuate soltanto letture locali e VPS.

## Evidenze e integrità

Artefatti:
`/home/football/.local/share/football-data-lab/evaluation/spatial-v2-q3-04-runtime-run-01`.

SHA-256 verificato di `hashes.final.sha256`:
`f863f449b7eab8f8c174401eaa40e3e53a32b5c62ec33395291d569f7a6a84ed`.
`sha256sum -c` ha confermato tutti i dodici file elencati: caso,
configurazione, exit code, manifest, payload, prompt, risultato, metadati,
wrapper, stdout, stderr e validazione.

Presenti e verificati: manifest completato, configurazione, caso canonico,
prompt, payload completo, wrapper, stdout/stderr, risultato, validazione,
metadati, exit code e inventario. Mancanti perché non ricevuti/prodotti:
risposta HTTP grezza, metadata HTTP, witness e label. Non sono disponibili
conteggio token, tempi interni Ollama, timestamp di accettazione/first token o
stato conclusivo server-side della richiesta.

## Timeline ricostruibile

Timestamp filesystem VPS, CET:

1. `12:20:38.398`: wrapper conservato;
2. `12:20:38.403`: processo avviato e log aperti;
3. `12:20:38.461–462`: caso, configurazione, prompt, manifest e payload scritti;
   il manifest registra `actual_requests_started=1`;
4. durante il tentativo, una lettura `/api/ps` ha mostrato `qwen3.5:9b`
   caricato, context length 4096;
5. `12:23:38.586`: dopo 180,124 s sono stati scritti envelope
   `not_evaluable`, validazione e metadati;
6. `12:23:38.597–600`: exit code 0 e inventario iniziale;
7. `12:24:25.658–661`: inventario finale non autoreferenziale.

Non esistono timestamp sufficienti per distinguere apertura TCP, ricezione degli
header, durata del caricamento, inizio/fine token generation o eventuale
completamento server-side dopo la chiusura client.

## Timeout HTTP e comportamento del wrapper

Il wrapper passa `timeout=180` a `judge_pair()`. Il trasporto iniettato usa
`urllib.request.urlopen(req, timeout=timeout)` e legge la risposta intera in
modalità non streaming. `judge_pair()` intercetta `TimeoutError` e restituisce
`E_JUDGE_TIMEOUT`. Il risultato osservato coincide con questo percorso:
`not_evaluable`, label/witness null, comparison e semantic compatibility false,
`promotion_authorized=false`.

Il timeout è quindi **dimostrato lato client**. L'assenza di raw e metadata HTTP
non permette di stabilire se sia scaduto prima degli header o durante la lettura
del body. La scadenza client non prova che Ollama abbia cancellato la
generazione; al controllo successivo il processo diagnostico era terminato e,
più tardi, `/api/ps` non mostrava modelli caricati, ma manca una timeline server
completa.

## Caricamento modello e risorse

Prima della richiesta `/api/ps` era vuoto; durante la richiesta mostrava il
modello col digest atteso. È pertanto compatibile con un caricamento avvenuto
nella finestra, ma durata e quota del timeout consumata dal caricamento non sono
registrate.

L'utente SSH non può leggere i messaggi journal degli altri utenti; per la
finestra `12:19–12:25` `journalctl -u ollama.service` non ha restituito entry e
ha segnalato la limitazione dei gruppi `adm/systemd-journal`. Nei dati kernel
accessibili non compaiono eventi OOM pertinenti. Gli snapshot pre-run mostravano
circa 14 GiB disponibili; lo snapshot successivo mostra ancora circa 14 GiB e
245 MiB di swap usata. Questi snapshot non descrivono RAM/CPU/swap durante i
180 secondi. Non sono disponibili metriche GPU/offload o token/s.

## Prompt, payload e schema

- prompt: 741 byte;
- payload serializzato conservato: 29.863 byte;
- schema JSON canonico compatto: 10.649 byte;
- sei proprietà e sei campi top-level obbligatori;
- due messaggi;
- `num_ctx=4096`, `num_predict=2048`;
- `temperature=0`, `think=false`, `stream=false`.

Lo structured output e la lettura non streaming sono fattori tecnicamente
compatibili con maggiore latenza, ma nessuna evidenza attribuisce loro il
timeout. Non sono stati costruiti prompt o schemi alternativi.

## Matrice causale

| Possibile causa | Qualificazione | Evidenza/limite |
|---|---|---|
| Timeout client | **Dimostrata** | Durata 180,124 s, `urlopen(..., timeout=180)`, `E_JUDGE_TIMEOUT` |
| Caricamento iniziale modello | **Compatibile** | modello assente prima e presente durante; durata ignota |
| Lentezza della generazione | **Compatibile** | nessuna risposta entro 180 s; token e tempi interni assenti |
| Complessità structured output | **Compatibile** | schema/payload misurati; nessuna relazione causale diretta |
| Saturazione risorse | **Non supportata** | nessuna telemetria durante il run; nessun OOM accessibile |
| Concorrenza | **Non supportata** | nessun concorrente nello snapshot, ma monitoraggio non continuo |
| Errore o blocco server | **Non supportata** | log server non accessibili e nessun raw HTTP |
| Malfunzionamento fail-closed wrapper | **Esclusa** nel percorso osservato | una chiamata, envelope e non-promozione coerenti |

## Revisione fail-closed

Il manifest e il wrapper provano una sola chiamata avviata. Il codice non
contiene cicli di retry, repair o fallback e gli artefatti non mostrano un
secondo tentativo. Nessuna label o witness è stata promossa; il risultato resta
`not_evaluable` con `promotion_authorized=false`. L'exit code 0 prova il
completamento controllato del wrapper, non il completamento della generazione.

Il comportamento fail-closed osservato è **VALIDATO** esclusivamente per questo
tentativo. Il riconoscimento semantico della contraddizione non è valutabile.

## Decisione, limiti e stati

Limite diagnostico principale: assenza dei log server completi e della
telemetria temporale della richiesta. Non è possibile separare con prova
caricamento, generazione e attività server successiva al timeout.

Unico prossimo passo raccomandato, non eseguito: autorizzare una lettura
privilegiata ma read-only dei log storici Ollama e kernel nella sola finestra
`2026-11-07 12:19:00–12:25:30 CET`. È distinta dalle letture correnti perché
l'utente SSH non appartiene ai gruppi che rendono visibili tutte le entry. Non
richiede una nuova generazione, né modifica di timeout, modello o servizi.

| Componente | Stato |
|---|---|
| Revisione forense timeout | **ESEGUITO** |
| Integrità artefatti | **VALIDATO** |
| Fail-closed del singolo tentativo | **VALIDATO** |
| Diagnosi semantica `q3_04` | **BLOCCATO** |
| Accuratezza generale, Gate, integrazione, certificazione | **BLOCCATO** |

