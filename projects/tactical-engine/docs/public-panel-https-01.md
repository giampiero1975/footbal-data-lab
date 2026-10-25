# Pubblicazione HTTPS del Knowledge Panel

Data: 2026-10-25. Stato: **IMPLEMENTATO**; emissione TLS **BLOCCATO** dal DNS.

## Attività

Pubblicare il pannello locale tramite `https://football-lab.byoursite.com`,
mantenendo API e worker su `127.0.0.1:8088` dietro reverse proxy.

## Prerequisito esterno

Record DNS richiesto:

- tipo `A`;
- nome `football-lab`;
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

Nginx 1.24 installato dai repository Ubuntu, attivo e abilitato; Certbot 5.8
installato tramite snap. Virtual host bootstrap installato: porta 80 disponibile
soltanto per `/.well-known/acme-challenge/`, tutte le altre richieste ricevono
404. API invariata su `127.0.0.1:8088`, health `ok`.

Configurazioni versionate:

- `deploy/nginx-footballlab-bootstrap.conf`;
- `deploy/nginx-footballlab-https.conf`.

Il nome inizialmente pianificato senza trattino è stato sostituito dal nome
effettivamente creato `football-lab.byoursite.com`. Il DNS pubblico risolve
correttamente verso `163.5.26.155`; emissione del certificato e collaudo sono
ora autorizzati. Non esporre direttamente la porta 8088.
