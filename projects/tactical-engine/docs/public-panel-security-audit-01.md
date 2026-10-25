# Audit sicurezza pannello pubblico 01

Data: 2026-10-25. Stato: **IMPLEMENTATO**.

## Perimetro

Audit pre-pubblicazione di API, pannello, reverse proxy, porte, segreti,
permessi, log e unità systemd. Nessuna inferenza RAG e nessuna esposizione della
porta 8088.

## Evidenze baseline VPS

- pubbliche soltanto SSH e porta 80 bootstrap; 443 non ancora attiva;
- API `127.0.0.1:8088` e Ollama `127.0.0.1:11434`;
- directory configurazione e runtime `700`, env/token e artefatti `600`;
- unità con `UMask=0077`, `NoNewPrivileges`, `PrivateTmp`, `ProtectSystem=strict`
  e scrittura limitata alla directory job;
- log applicativi osservati senza header Authorization né body;
- firewall host attivo;
- bootstrap Nginx restituisce 404 fuori dalla challenge ACME.

## Rischi individuati e correzioni

1. I tentativi con token errato non consumavano il rate limit ordinario.
   Aggiunto bucket separato, predefinito 20/minuto, senza penalizzare polling e
   richieste autenticate.
2. Il formato di log standard poteva includere la query string della ricerca.
   L'API registra ora soltanto metodo, percorso privo di query e stato. La
   configurazione HTTPS usa un formato Nginx basato su `$uri`, non `$request`.
3. Rafforzata la configurazione TLS prevista con TLS 1.2/1.3, session ticket
   disabilitati, HSTS, frame deny, nosniff, no-referrer e Permissions-Policy.

## Evidenza offline

Compilazione superata, suite API/catalogo 16/16 e diff check pulito. Deploy e
smoke VPS DA FARE; stato corrente **IMPLEMENTATO**, non ancora INTEGRATO.

## Limiti

Il certificato e il test Internet restano bloccati dal DNS. La CSP del pannello
consente ancora CSS e JavaScript inline per l'artefatto statico monofile; i dati
dinamici sono sottoposti a escaping e il token resta in memoria. Un'eventuale
separazione degli asset è un hardening successivo, non un prerequisito per il
reverse proxy autenticato.
