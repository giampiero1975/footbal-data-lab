# Gemini independent benchmark review — V5-GEM-01

Stato: IMPLEMENTATO (client), non ESEGUITO su VPS. Il benchmark RAG e il gold sono invariati.

## Separazione e fonti

Client `scripts/review_rag_v5_gemini.py`: usa esclusivamente Gemini REST, non Ollama, non importa risultati o judge precedenti. Manifest esistente SHA-256 `f0d36bc5b35ddcfd42bfef234db2380db6a684a9b81fb9cd19ab75bea81755c0`. In questa fase accetta solo `fresh_01`.

La sola API key Gemini **non permette accesso a Google Drive**. Occorre preparare un bundle JSON locale **non committato** con la trascrizione verificata delle pagine 21–23 del PDF Ussia, usando accesso Drive autorizzato. Il documento originale e identificato da Drive ID `0B6maey1azXc5bUlKVEh4S0JUMjQ`. Non usare le note `source_verification` come sostituto della fonte. Il bundle e destinato a una directory privata sulla VPS.

Schema del bundle (un oggetto per pagina; ripetere per 21, 22 e 23):

```json
{
  "question_id": "fresh_01",
  "documents": [
    {
      "source_file_id": "0B6maey1azXc5bUlKVEh4S0JUMjQ",
      "source_title": "Transizioni.Ussia. Master Allenatore PRO.pdf",
      "origin_url": "https://drive.google.com/file/d/0B6maey1azXc5bUlKVEh4S0JUMjQ/view",
      "page": "21",
      "text": "TRASCRIZIONE VERIFICATA DELLA PAGINA 21"
    }
  ]
}
```

Il client controlla presenza delle fonti, identificativi, pagine, quote riportate letteralmente e copertura di tutti i claim; non puo dimostrare che un bundle sia autentico senza un controllo umano o di estrazione. Non usare placeholder in un test reale.

## Quota e costi

Modelli ammessi esplicitamente: `gemini-3-flash-preview` (5 RPM, 20 RPD secondo configurazione dichiarata) e `gemini-3.1-flash-lite-preview` (15 RPM, 500 RPD). Niente fallback automatico. Per la prima prova: una sola richiesta e zero retry automatici. Il limite locale usa `evaluation/.gemini_review_request_ledger.json` (file da non versionare). Se la richiesta fallisce, viene comunque consumato un tentativo locale. Le quote effettive dipendono dal progetto e dalle condizioni Google e vanno controllate su AI Studio. Il client **non puo garantire da solo assenza di fatturazione**: il flag `--confirm-free-tier` va usato soltanto dopo verifica che il progetto sia Free Tier e non associato a billing. Nessuna chiave nel repository, nei comandi o nei report.

## Comandi VPS, dopo predisposizione del bundle

```bash
cd /opt/football-data-lab
git pull --ff-only
projects/tactical-engine/.venv/bin/python projects/tactical-engine/scripts/review_rag_v5_gemini.py --source-bundle /percorso/privato/fresh_01_sources.json --output projects/tactical-engine/evaluation/gemini_fresh_01_review_v1.json --dry-run
```

Dopo preflight positivo, verificare Free Tier in Google AI Studio e impostare `GEMINI_API_KEY` come variabile d'ambiente VPS senza inserirla nella shell history. Per eseguire: stesso comando senza `--dry-run`, con `--confirm-free-tier`. Il file output deve non esistere gia. Il report e ESEGUITO, non approvazione del freeze: la revisione AI e separata ma non prova indipendenza umana. Esaminare il report prima di estendere alle altre domande.

## Decisione e rollback

Freeze BLOCCATO fino a review verificabile delle dieci domande e fingerprint runtime. Non inviare risposte Ollama. Rollback: non eseguire il client, nessun effetto su Chroma/V4/V5. Non committare bundle o ledger. L'archiviazione Git del report richiede controllo e rimozione di eventuali dati sensibili e deve avvenire dopo il test.
