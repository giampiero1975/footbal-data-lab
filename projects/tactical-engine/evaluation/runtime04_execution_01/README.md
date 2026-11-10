# Evidenze originali runtime-04

`artifacts/` contiene i 27 file originali riletti dalla directory runtime VPS
senza modificarne i byte. Gli attributi Git impediscono conversioni newline.
`metadata/` conserva preflight immediato, unica invocazione locale e verifica
di raccolta. `summary.json` è un riepilogo derivato, non sostituisce gli originali.

Verifica locale degli inventari, senza eseguire alcun wrapper o codice RAG:

```bash
cd artifacts
sha256sum -c hashes.sha256
sha256sum -c attempt_state.sha256
sha256sum -c hashes.sha256.digest
```

Gli inventari coprono rispettivamente 23 payload, lo stato finale e il digest
dell'inventario payload. `witness.json` e `validation.json` sono assenti perché
il precontrollo semantico ha bloccato il percorso prima della localizzazione.
Nessun risultato è promosso e l'autorizzazione alla singola invocazione è consumata.
