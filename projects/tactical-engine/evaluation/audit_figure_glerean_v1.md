# Audit figure Glerean — 20 ottobre 2026

Fonte: PDF originale `334_principi_Glerean.pdf` trovato su Google Drive, 16 pagine PDF; pagine stampate 13, 16, 17, 18 corrispondono a pagine PDF 8, 11, 12, 13.

## Verifiche visive
- Fig. 12 (PDF p.8, stampata p.13): n.4 portatore centrale di centrocampo; n.6 e n.8 centrocampisti; n.11 e n.7 attaccanti esterni; n.9 e n.10 attaccanti centrali. Quattro linee di passaggio dal n.4. I difensori n.3,5,2 sono visibili nelle fig.13–14, non nella fig.12.
- Fig. 13 (PDF p.8): n.4 centrocampista con palla; n.6 e n.8 centrocampisti che si allargano; n.3,5,2 difensori. Testo dice espressamente «dietro le spalle del centrocampista avversario».
- Fig. 14 (PDF p.8): n.3,5,2 arretrano per appoggio al n.4 portatore.
- Fig. 18 (PDF p.11, stampata p.16): n.1 portiere lancia lungo verso n.10; n.11,9,7 sono avanzati. La «spizzata» è nel testo; non etichettata graficamente come tale.
- Fig. 19 (PDF p.11): n.8 centrocampista controlla la palla dopo respinta; n.11,10,9,7 si posizionano in spazi centrali/laterali; n.3,5,2 difensori.
- Fig. 20 (PDF p.12, stampata p.17): n.3,5,2 arretrano rispetto al portatore n.4.
- Fig. 21 (PDF p.13, stampata p.18): n.11 e n.7 esterni, n.9 e n.10 centrali, movimenti in profondita/ampiezza e diagonali. Numeri pallidi rappresentano posizioni precedenti.

## Diagnosi
Le figure assenti dai chunk creano un deficit informativo reale su ruoli, numeri, posizione e traiettorie: non e' corretto imputare interamente tali errori ai modelli. Altri errori rimangono di generazione quando il testo e' esplicito (centrocampista vs difensore avversario, portiere vs attaccante nella spizzata, verticalita avanti/indietro).

## Procedura senza impatto sulla produzione
1. Non alterare i PDF, chunk, benchmark e Qwen V4.
2. Creare sidecar testuali `figure_evidence` con ID figura, pagina PDF/stampata, ruoli, movimenti, certezza e distinzione fra lettura visiva e inferenza congiunta.
3. Preparare sei nuovi contesti identici per Gemma e Qwen; congelare hash e valutare su 10 gold claims piu' errori di ruolo. Mantenere confronto prima/dopo.
4. Correggere prima il parser delle citazioni composte, per evitare falsi `used_refs=[]`.

Documentazione API Ollama: https://docs.ollama.com/api/chat
