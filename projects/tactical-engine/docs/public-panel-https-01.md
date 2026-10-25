# Pubblicazione HTTPS del Knowledge Panel

Data: 2026-10-25. Stato: **DA FARE**.

## Attività

Pubblicare il pannello locale tramite `https://footballlab.byoursite.com`,
mantenendo API e worker su `127.0.0.1:8088` dietro reverse proxy.

## Prerequisito esterno

Record DNS richiesto:

- tipo `A`;
- nome `footballlab`;
- valore `163.5.26.155`;
- modalità solo DNS durante emissione e collaudo del certificato.

## Gate

1. verificare la risoluzione pubblica del nome verso l'IP VPS;
2. installare Nginx e il client ACME dai repository di Ubuntu;
3. applicare redirect HTTP→HTTPS, TLS, body/rate limit e timeout compatibili
   con il worker seriale;
4. conservare l'upstream esclusivamente su localhost;
5. verificare certificato, pannello, autenticazione, health/readiness e rinnovo;
6. documentare rollback e stato senza estendere la certificazione locked.

## Decisione

Procedere autonomamente; l'emissione del certificato resta **BLOCCATO** finché
il record DNS non risolve pubblicamente. Non esporre direttamente la porta 8088.
