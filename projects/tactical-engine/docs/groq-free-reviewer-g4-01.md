# Groq Free reviewer — G4 singolo caso tattico reale

Data: 2026-10-25. Stato: **ESEGUITO**. Perimetro: una sola valutazione reale
autorizzata; nessuna rigenerazione RAG, modifica indici, integrazione o deploy.

## Attivita e input congelato

- Provider/modello: Groq Free, `openai/gpt-oss-120b`.
- Caso riutilizzato: `928f9702e19148c3a80e500ebe02fec9`, file VPS
  `evaluation/api-runs/928f9702e19148c3a80e500ebe02fec9.result.json`.
- Domanda: movimento del terzino sinistro quando il braccetto esce sull'ala
  collocata nell'half-space.
- Trasmissione limitata a domanda, risposta RAG e sei estratti gia presenti nel
  report. Nessun PDF completo, credenziale, indice o altro dato di progetto.
- Output separato:
  `evaluation/groq_g4_tactical_case_928f9702_v1.json`.
- SHA-256 output:
  `57df012dc027d1b16eadf155970bebdf218c7fe61535ae1b817a0be7834f4915`.

Il preflight offline e passato con `API_REQUESTS=0`. Successivamente e stata
eseguita una sola chiamata reale. La chiave e rimasta soltanto nella memoria del
processo, e stata rimossa subito dopo e non compare nel report o nel repository.
La directory temporanea VPS contenente copia del caso e client e stata rimossa.

## Risultato Groq

- HTTP 200; tempo applicativo 3,770 s.
- Telemetria API: queue 0,298 s; prompt 0,184 s; completion 3,218 s; totale API
  3,402 s.
- Token: 3.250 prompt, 1.544 completion, di cui 1.160 reasoning; **4.794
  totali**.
- Voto: **5,8/10**; verdetto: **REVISIONE**.
- Punti positivi: sovrapposizione del terzino, riconoscimento dello spazio
  liberato dal braccetto, conservazione dei ruoli originari.
- Correzione richiesta: descrivere la corsa diagonale nello spazio interno e la
  relativa tempistica; usare evidenze piu specifiche.

## Verifica indipendente delle citazioni

Il report RAG dichiara `citation_ids = [1, 2, 4, 5]`, nessuna citazione
invalida, e contiene le evidenze etichettate `F1`–`F6`. La risposta usa
`F1`, `F2`, `F4` e `F5`: la corrispondenza sintattica e quindi corretta.

Groq ha invece segnalato che F4/F5 non corrisponderebbero agli ID dichiarati e
che esisterebbe incoerenza fra numeri ed etichette. Entrambe le osservazioni
sono **false**: l'adapter usa intenzionalmente gli ID numerici senza prefisso e
li confronta con le label dopo la rimozione di `F`; il gate locale era passato.

Sul piano semantico la critica e parzialmente fondata: F2 sostiene
sovrapposizione e inserimento quando l'esterno si accentra, ma non codifica con
precisione una sotto-sovrapposizione/taglio diagonale interno. Le altre fonti
sono generiche rispetto all'azione richiesta. La risposta individua la
profondita, ma parla anche di linea parallela alla fascia e non esplicita con
sufficiente nettezza il taglio diagonale nello spazio lasciato dal braccetto.

## Confronto e decisione

La valutazione esterna gia comunicata dal titolare per lo stesso caso era
7,5/10: riconosceva il miglioramento ma chiedeva il termine e il gesto esatto
di sotto-sovrapposizione interna. Groq assegna 5,8/10, quindi -1,7 punti. La
direzione tattica della critica e coerente, ma il voto e sostenuto anche da due
errori inesistenti sulle citazioni.

Conclusione tecnica: il modello mostra utilita come secondo parere tattico, ma
**questo singolo risultato non e affidabile come giudice automatico** delle
citazioni. G4 e ESEGUITO, non VALIDATO per affidabilita generale e non
INTEGRATO. Non eseguire altri casi, modificare Gemini o effettuare deploy senza
nuova autorizzazione. La chiave gia comparsa in chat deve essere revocata.

