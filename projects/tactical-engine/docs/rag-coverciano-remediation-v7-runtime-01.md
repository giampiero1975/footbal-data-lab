# RAG Coverciano — runtime remediation V7

Data: 2026-10-27  
Ramo: `codex/rag-coverciano-remediation`  
Stato: **ESEGUITO (10/10), NON VALIDATO**

## Perimetro

Secondo rerun differenziale dei dieci casi Coverciano congelati. OpenRouter e
ogni altra spalla sono rimasti disabilitati; nessuna chiamata Gemini nuova.
Confronto qualitativo esclusivamente con i giudizi Gemini originali della
baseline. Collection 6.410 invariata.

Artefatti: `evaluation/coverciano-remediation-v7/case_01.json` fino a
`case_10.json` e `run.log`.

## Risultato tecnico

| Caso | Tempo | Output token | Arresto | Repair | Audit finale |
|---:|---:|---:|---|---|---|
| 1 | 187,59 s | 650 | stop | no | completo |
| 2 | 251,77 s | 601 | stop | si | incompleto |
| 3 | 256,65 s | 443 | stop | si | incompleto |
| 4 | 284,53 s | 472 | length | si | incompleto e troncato |
| 5 | 135,49 s | 470 | stop | no | completo |
| 6 | 244,53 s | 516 | stop | si | incompleto |
| 7 | 268,01 s | 605 | stop | si | incompleto |
| 8 | 201,85 s | 586 | stop | no | completo |
| 9 | 196,54 s | 655 | stop | no | falso positivo semantico |
| 10 | 247,54 s | 224 | length | si | incompleto e troncato |

- Tempo totale: **2.274,50 s**; media **227,45 s**.
- Miglioramento rispetto a V6: **-22,6%** sul tempo medio.
- Output token: **5.222**.
- Citazioni sintatticamente invalide: **0**.
- Repair attivato: **6/10**.
- Audit finale realmente completo: **3/10** (1, 5, 8). Il caso 9 e marcato
  completo dal controllo ma contiene una contraddizione tattica.
- Risposte troncate: **2/10** (4 e 10).

## Audit qualitativo per caso

1. **Transizione negativa:** ora tratta densita, zona, palla coperta/scoperta e
   struttura preventiva. Miglioramento netto, ma identifica ancora in modo
   semplicistico palla coperta con palla “vicina” e non specifica uomini e
   rapporti numerici della preventiva. Vicino alla soglia, non certificato.
2. **Costruzione dal basso:** contiene portiere, terzo uomo, uscita lunga e
   seconda palla, ma introduce zona 14 e ruoli non sostenuti, confonde il primo
   attaccante con un compagno e usa fonti sul portiere in fase difensiva.
3. **Difesa del cross:** migliora postura, contatto e traiettoria; resta ambigua
   la frase secondo cui il difensore “blocca l'uscita” del portiere, manca una
   chiamata operativa e il repair non chiude tutti i dettagli.
4. **Scaglionamento:** introduce cinque corridoi, ma ricade in numeri di maglia
   e movimenti difensivi, non definisce 2+3/3+2 e termina con `6`. Non valutabile
   come risposta completa.
5. **Scivolamento:** la nuova riserva recupera finalmente i passaggi esatti su
   tempo di volo e lato debole. La risposta distingue traslazione e ripiegamento,
   assegna il mediano allo schermo e chiude i corridoi interni. E il miglior
   recupero della V7, pur con una frase finale impropria sull'area avversaria.
6. **Contro-pressing:** recupera e usa correttamente la regola dei cinque
   secondi e la preventiva; tuttavia apre con una sezione etichettata
   “Possesso”, contiene una frase incoerente sulla densita che “deve cedere” e
   non stabilizza la relazione palla coperta/scoperta.
7. **Rifinitura:** più completa nelle trasmissioni, ma ricezione orientata,
   attacco della linea e scarico-inserimento restano elencati invece che
   coordinati. Il repair non chiude i due requisiti principali.
8. **Costruzione alta/cross:** copre formalmente quattro zone e segnale del
   cross, ma inventa numeri/ruoli, introduce difesa del cross non richiesta e
   produce movimenti contraddittori. Il gate lessicale sovrastima la qualita.
9. **Fuorigioco:** le fonti corrette entrano nel contesto, ma la risposta prima
   afferma erroneamente `palla coperta -> scappare` e `palla scoperta -> salire`,
   poi fornisce la versione corretta nel punto successivo. Il gate cerca parole
   presenti in qualunque posizione e non riconosce la contraddizione. Errore
   grave non risolto.
10. **Tattica in itinere:** inizia correttamente e prepara un esempio concreto,
    ma viene troncata subito dopo `Un difensore centrale`; comunicazione,
    equilibrio transizionale e impatto emotivo restano incompleti.

## Conclusione

La V7 dimostra due miglioramenti reali: fonti più mirate e latenza inferiore.
Dimostra anche che una sola rigenerazione con lo stesso modello 9B non garantisce
la chiusura del contratto. Il target medio 26/30 **non e dimostrato e non e
ragionevolmente raggiunto**; non esiste un nuovo voto Gemini da dichiarare.

Cause residue:

1. audit lessicale non sensibile a negazione, soggetto e contraddizioni;
2. repair non fail-closed: l'output resta pubblicabile anche se il secondo audit
   fallisce;
3. secondo output ancora soggetto al tetto token;
4. contesto con fonti scenario-specifiche e fonti generiche concorrenti;
5. modello locale 9B insufficiente nel mantenere più vincoli e ruoli senza
   contraddirsi.

La prossima versione deve introdurre un controllo relazionale deterministico
per le decisioni critiche, rifiutare output incompleti dopo il repair, conservare
la prima risposta se il repair peggiora, e misurare separatamente un generatore
più capace mantenendo retrieval e citazioni del RAG come componente dominante.
