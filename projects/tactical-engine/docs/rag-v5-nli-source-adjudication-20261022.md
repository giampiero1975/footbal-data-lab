# Verifica documentale dei controlli NLI — 2026-10-22

Fonti originali lette direttamente da Google Drive (testo estratto dai PDF):

1. Roberto Bonacini, *La verticalizzazione nelle fasi di gioco*, Allenatore.net, aprile 2004, https://drive.google.com/file/d/0B6maey1azXc5ZU9TYl9RNXNZbzA/view. L'autore raccomanda ampiezza e cross contro difese basse; verticalizzazione quando c'è spazio dietro; nota che sui campi pesanti si può privilegiare il verticale. Precisa che la verticalizzazione non è un mezzo assoluto per segnare; evidenzia rischio di fuorigioco con intesa imperfetta contro difese in linea.
2. Alessandro Pane, *Variazione del sistema di gioco partendo da una base fissa di 7 giocatori*, tesi Master 2005/06, https://drive.google.com/file/d/0B6maey1azXc5UUV0ZkxMeklvRHM/view. Descrive tre variazioni del reparto offensivo con sette giocatori fissi; il centromediano metodista protegge la difesa e partecipa alla costruzione. Non generalizza a ogni sistema calcistico. La strategia del contrattacco veloce è descritta nel contesto della squadra; le singole variazioni vanno valutate con cautela.
3. *Superiorità in possesso palla* (file Tesser), https://drive.google.com/file/d/0B6maey1azXc5a2l4bW5wVUp6djA/view. Esercizio 5: 3>3 + jolly, sfruttare la superiorità in possesso e segnare sulle due portine. Non documenta la liceità di jolly aggiuntivi in gare ufficiali.

Gold-label adjudication: `low_block_reverse` contradicted; `offside_universal` insufficient (fonte espone rischio condizionale, non controesempio esplicito); `methodist_every` insufficient; `jolly_official` insufficient. `vertical_always` contradicted because Bonacini esclude espressamente la verticalizzazione come mezzo assoluto. La presenza di 'campi pesanti' nella fonte NON giustifica l'affermazione 'sempre scelta migliore' sul campo pesante.

Caveat: il benchmark legge estratti F1/F2/F3 congelati nel report, non necessariamente l'intero PDF. Le etichette devono essere giudicate rispetto all'estratto effettivamente passato al classificatore. Prima di usare il punteggio come metrica definitiva, confrontare i singoli estratti con queste fonti e ricontrollare i casi `counterattack_intent`, `methodist_build` e ogni formulazione che ecceda il testo disponibile.

Policy: V2 resta baseline shadow; V3 rifiutato; produzione RAG/Chroma invariata.
