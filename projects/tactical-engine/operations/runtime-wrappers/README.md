# Preparazione locale runtime-04

Attività `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-LOCAL-PREPARATION-01`.

L'originale `spatial-v2-extraction-locator-q3-04-runtime-03.original.sh` è stato
recuperato in sola lettura dal percorso VPS già documentato. Deve restare di
45.964 byte con SHA-256
`ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57`.
Gli attributi Git disabilitano conversioni newline sui wrapper e sul diff.

`prepare_runtime04_wrapper.py` produce esclusivamente una copia locale nuova
e il diff completo; non esegue shell, SSH, trasporti o codice applicativo.
La copia contiene un launcher SSH: non eseguirla per fare preflight.

## Giustificazione delle verifiche nuove, registrata prima dell'esecuzione

I 37 test extraction/Spatial V2 già VALIDATI non sono ripetuti. Non coprivano
il verificatore Python incorporato in questo wrapper e il nuovo ramo dedicato
al boundary semantico. Le sole verifiche autorizzate qui sono:

- `bash -n` sul launcher e separatamente sul corpo remoto (sola sintassi);
- parsing/compilazione dei blocchi Python senza eseguirli;
- confronto completo del delta con l'originale e invarianti statiche;
- esecuzione del solo verificatore estratto, su artefatti sintetici temporanei,
  per distinguere schema, boundary semantico, localizzazione e witness;
- controlli negativi del nuovo ramo: reason/details/provenance alterati,
  witness o validation indebiti, promozione indebita;
- controllo che il wrapper originale respinga quel medesimo nuovo boundary,
  mentre la copia lo descriva come fail-closed senza successo semantico.

Le fixture deterministiche riusano soltanto dati/helper già versionati; nessuna
suite precedente è lanciata. Il test del verificatore non esegue wrapper,
generazione, trasporto, finalizzatore o import del motore RAG. Finalizzatore e
inventari vengono verificati come blocchi invariati rispetto all'originale.

Baseline applicativa obbligatoria:
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.
Staging futuro e trasferimenti non sono autorizzati dalla preparazione locale.

Prima esecuzione nuova suite: 12 controlli superati, un confronto statico
respinto perché non normalizzava l'attempt ID autorizzato nel finalizzatore.
Corretto esclusivamente il confronto del test, senza cambiare wrapper o
finalizzatore. È giustificata la riesecuzione del solo controllo fallito;
gli altri dodici non vengono ripetuti.
