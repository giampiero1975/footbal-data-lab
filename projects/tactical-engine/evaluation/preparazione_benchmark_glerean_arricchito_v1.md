# Preparazione benchmark Glerean arricchito — v1

Stato 20/10/2026: **preparazione offline verificata, benchmark modelli NON ancora eseguito**. Originale `334_principi_Glerean.pdf` recuperato da Google Drive (16 pagine PDF), figure 10–14, 18–21. Audit precedente: `evaluation/audit_figure_glerean_v1.md`.

## Materiali prodotti (allegati conversazione)
- `glerean_figure_evidence_v1.json`: mappa ruoli numeri 1,2,3,4,5,6,7,8,9,10,11 e descrizioni delle figure, evidenza visuale separata da testo+figura, livelli di certezza.
- `prepare_glerean_enriched_benchmark_v1.py`: generatore offline che legge il report Gemma V2 e sidecar e non chiama Ollama.
- `glerean_enriched_contexts_v1.json`: sei contesti con le cinque fonti originali immutate e sidecar integrativi. Coppie numeric/stable hanno sidecar identici.

## Controlli
- 6/6 contesti preparati; 3 coppie con hash identico per il solo sidecar; 5 chunk originali per caso conservati, insieme a source_sha256, prompt_sha256 e gold claims.
- Hash del contesto arricchito (numeric/stable): POSSESSO `52b04d1fd8a0c900` / `2e798f31de0b9c3e`; UNO `ab0470d2a9f4d4c3` / `16ec2c80997d272b`; VERTICALITA `25f01e591e7ee75a` / `c28fbc296282d317`.
- La differenza di hash numeric/stable e' attesa per le citazioni ID diverse. Le figure non sono nuove fonti numerate: citarle come figure e pagine originali.

## Caveat
- La figura 18 mostra il portiere che lancia e il n.10 che si porta incontro; il testo dice che uno degli attaccanti spizza, ma il disegno non etichetta con certezza l'autore della spizzata. Non trasformare l'inferenza in certezza.
- La mappa ruoli e' specifica per il 3-3-4 di Glerean; non e' universale.
- Non e' stato eseguito nessun modello e non e' stato modificato Qwen V4, Chroma, benchmark precedenti o prompt di produzione.
- Prima di un confronto definitivo: usare identici contesti arricchiti per entrambi i modelli, stessi parametri, correggere il parser di citazioni composte e valutare gold claims con attributi di evidenza.

API ufficiale: https://docs.ollama.com/api/generate
