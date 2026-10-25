# RAG V5 API security remediation 01

Audit Codex Security `cc2a0cdd-2e17-4a97-b5ef-6c4e1bed4126`: un rilievo medio e due bassi.

Correzioni implementate:

- rifiuto esplicito del token placeholder e template deliberatamente invalido;
- limite di 32 connessioni concorrenti e timeout lettura di 15 secondi;
- rate limit applicato anche alla ricerca full-corpus;
- guida generativa rafforzata per distinguere possesso, non possesso, perdita e riconquista.

Verifica VPS: 10/10 test; placeholder respinto; limite server 32/daemon confermato; dieci ricerche 200 e undicesima 429; servizio riavviato `active`, health/readiness corretti. Stato: **VALIDATO e INTEGRATO**.
