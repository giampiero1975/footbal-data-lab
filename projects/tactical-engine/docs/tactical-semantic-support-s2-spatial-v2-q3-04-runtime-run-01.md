# RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-RUNTIME-RUN-01

## Baseline e riconciliazione

Singola diagnosi runtime autorizzata sul caso canonico `q3_04`.

- HEAD documentale iniziale:
  `eb40cbd15aeb1eb01d61bc70e5044468f2c1c910`;
- staging esclusivo:
  `/home/football/.local/share/football-data-lab/staging/spatial-v2-q3-04-009f76e`;
- baseline runtime detached:
  `009f76e71c0351da9d2b797ad3c9ff1928671a4e`;
- working tree staging pulito prima e dopo il tentativo;
- nessuna esecuzione Spatial V2 equivalente risultava già registrata.

TODO, experiment register, remediation/closeout R1/R2, preflight bloccato e
preparazione dello staging sono stati riconciliati. I 18 test offline non sono
stati ripetuti.

## Preflight immediato

Il preflight fail-closed ha confermato HEAD, detached HEAD, repository autonomo,
working tree pulito e file Spatial V2 regolari. Il caso è stato letto dal
dataset Git senza ricostruzioni:

- fonte `verticalizzazione_Bonacini`, pagina 2;
- claim SHA-256 UTF-8:
  `ea9d4276219edd1e37781c328541cdda4dd54c13eabc3185618ba4e0c96039bd`;
- evidence SHA-256 UTF-8:
  `302019bbce33aea87ab218afedbb823a7400defd56a134d1f867f2c35dd6fce1`.

Ollama esponeva un solo `qwen3.5:9b` col digest atteso
`56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
`/api/ps` non mostrava modelli caricati e lo snapshot non mostrava un'altra
diagnosi equivalente. Questa osservazione non prova esclusività futura.

## Metodo e configurazione

È stato usato `judge_pair()` della baseline con un trasporto iniettato che ha
conservato prompt e payload e ha eseguito la stessa unica richiesta HTTP. Il
wrapper temporaneo è esterno al repository Git e non modifica il judge.

- modello `qwen3.5:9b`;
- endpoint `http://127.0.0.1:11434/api/chat`;
- contratto `nli_spatial_relations_v2` `2.0.0`;
- temperatura 0, contesto 4096, massimo 2048 token;
- timeout 180 secondi, stream/think false;
- una richiesta massima, zero retry, repair e fallback.

La label Gold è conservata nell'artefatto del caso per attribuzione, ma non è
presente nel prompt o nel payload destinato al modello.

## Artefatti

Percorso esterno al repository:
`/home/football/.local/share/football-data-lab/evaluation/spatial-v2-q3-04-runtime-run-01`.

Sono presenti manifest, configurazione, caso e digest, prompt, payload, wrapper,
stdout/stderr, exit code, risultato, validazione, metadati e inventario SHA-256.
SHA-256 di `hashes.final.sha256`:
`f863f449b7eab8f8c174401eaa40e3e53a32b5c62ec33395291d569f7a6a84ed`.

La risposta HTTP grezza, witness e metadata HTTP non sono presenti: il timeout
si è verificato prima che `urlopen()` restituisse una risposta. Non vengono
dichiarati artefatti inesistenti.

## Risultato tecnico

- richieste generative effettivamente avviate: **1**;
- durata osservata: `180.12447399506345` secondi;
- exit code del wrapper: `0`;
- `evaluation_status`: `not_evaluable`;
- errore: `E_JUDGE_TIMEOUT`;
- `promotion_authorized=false`;
- witness: assente;
- label dichiarata/derivata: assente;
- confronto e compatibilità semantica: non verificati.

L'exit code 0 descrive il completamento controllato del wrapper e la
serializzazione dell'esito fail-closed; non trasforma il timeout in PASS tecnico.
L'autorizzazione alla singola richiesta è consumata e non è stato effettuato
alcun rilancio.

## Analisi semantica e limiti

Soggetto, referente, asse `space_availability`, valori, confronto, ancoraggi,
coreferenza e label non sono valutabili perché non esiste un witness. Non è
possibile attribuire un errore semantico al modello né verificare la correzione
del falso positivo storico.

Classificazione:

- PASS tecnico: non conseguito;
- PASS semantico: non valutabile;
- fail-closed: osservato correttamente;
- esito operativo: timeout della singola richiesta;
- causa direttamente dimostrata: assenza di risposta entro il timeout
  contrattuale, non una specifica insufficienza semantica.

## Decisione e stati

| Componente | Stato |
|---|---|
| Singolo tentativo runtime | **ESEGUITO** |
| Fail-closed sul timeout | **VALIDATO** nel singolo tentativo |
| Diagnosi semantica `q3_04` | **BLOCCATO** |
| Revisione indipendente del run | **DA FARE** |
| Accuratezza semantica generale | **BLOCCATO** |
| Gate, integrazione S2 e certificazione | **BLOCCATO** |

Decisione: nessun retry o intervento correttivo. Un eventuale nuovo tentativo
richiede una nuova decisione esplicita e non è autorizzato da questo report.
