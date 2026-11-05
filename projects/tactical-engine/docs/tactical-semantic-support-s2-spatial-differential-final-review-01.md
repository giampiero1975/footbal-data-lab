# RD-TSC-V2-D3-S2-SPATIAL-DIFFERENTIAL-FINAL-REVIEW-01

## Attivita

Revisione statica conclusiva della Fase A del Gate differenziale
`nli_spatial_relations_v1`, limitata al valore probatorio di `q5_06` e alla
tracciabilita del runner. Baseline iniziale:
`3aa5764c82f84cea4db188b3866e2603c29800cb`. Nessuna inferenza, rete, NLI V2,
modifica al Gold o intervento operativo e stato eseguito.

## `q5_06`: qualificazione probatoria

Claim congelata: `Il gioco a zona garantisce un avanzamento più rapido durante
il possesso.` Evidenza: il gioco a zona puo presentare come svantaggio un `più
lento avanzamento durante la fase di possesso palla` (`Gioco a zona nel calcio`,
pagina 2). Il soggetto e il gioco a zona; referente e proprieta sono la velocita
dell'avanzamento in possesso; contesto e fase coincidono. `più rapido` e `più
lento` sono intensita/direzioni incompatibili sulla stessa proprieta.

Il caso non e la regressione `q3_04` e non riusa la coppia lasciare/togliere
spazio. Appartiene pero alla stessa famiglia concettuale di inversioni gia
esemplificata dal contratto (`aumentare/ridurre`, `avanzare/arretrare`). La
classificazione corretta e quindi **controllo distinto ma correlato**, non
controllo indipendente. Puo osservare trasferimento oltre la coppia letterale
`q3_04`, ma non sostenere da solo generalizzazione indipendente.

## Difetto di tracciabilita accertato

Il runner precedente esponeva `actual_inferences`, incrementato soltanto dopo il
ritorno di `s2.assess_claim()`. Il valore contava record restituiti dal confine
S2, non richieste HTTP osservate direttamente. Un errore del judge e contenuto da
S2 e produceva un record `not_evaluable`, ma una eccezione non intercettata o
un'interruzione prima del ritorno non poteva essere rappresentata dal contatore.
Il report distingueva `stopped_early`, ma non possedeva una attestazione positiva
di completamento; il rischio era interpretare un JSON parziale come Gate completo.

## Rettifica minima

Commit tecnico: `3e630a5e6aba2e402adeea01f3f8dc4cf4f6e419`.

Nel solo runner differenziale:

- `planned_evaluations=3` indica i casi pianificati;
- `attempted_evaluations` aumenta prima della valutazione applicativa del caso e
  non pretende di contare richieste HTTP;
- `completed_evaluations` aumenta soltanto per `evaluation_status=evaluated`;
- `run_complete=true` richiede tre tentativi, tre valutazioni tecnicamente valide,
  tre record e nessun arresto anticipato;
- `report_exit_code()` restituisce 0 soltanto per `run_complete=true`, altrimenti
  2.

Un errore o timeout intercettato dal confine S2 produce un report parziale,
`not_evaluable`, `run_complete=false`, exit 2 e nessuna promozione. Una eccezione
esterna al confine o un'interruzione del processo prima della scrittura finale
puo lasciare nessun JSON: non viene quindi attestato alcun completamento. Il file
e scritto solo al termine e con modalita esclusiva. Il runner non osserva il
trasporto HTTP e non dichiara un conteggio server-side.

## Verifiche differenziali

Eseguita nuovamente soltanto la suite direttamente interessata dalla rettifica:

```text
python -m unittest tests/test_run_tactical_semantic_support_s2_spatial_relation_differential_v1.py -v
```

Risultato: **6/6 PASS** in 0,025 s. Il percorso completo verifica
`planned/attempted/completed=3/3/3`, `run_complete=true`, exit 0. Il mock timeout
verifica `planned/attempted/completed=3/1/0`, `run_complete=false`, stop
anticipato, `not_evaluable`, exit 2
e `promotion_authorized=false`. Compilazione in memoria e `git diff --check`:
PASS. Nessuna suite storica o inferenza eseguita.

## Isolamento

Modificati soltanto runner differenziale, relativo test e documentazione. Fixture,
Gold, contratto spatial, NLI V2, bridge S2, S1, modello, routing, RAG, Chroma, API
e panel sono invariati. Restano massimo tre valutazioni, nessun retry/repair,
`promotion_authorized=false` e nessuna autorita su `overall_status` o
`promoted_answer`.

## Decisione e stato

**REVISIONE FAVOREVOLE.**

La qualificazione probatoria e ora corretta e nessun report parziale puo attestare
`run_complete=true` o exit 0. Il Gate differenziale e tecnicamente pronto per una
futura autorizzazione runtime separata; efficacia semantica, confronto generale
V2, integrazione e certificazione restano **BLOCCATO**.

- Revisione finale: **ESEGUITO**.
- Rettifica tracciabilita: **IMPLEMENTATO**.
- Proprieta differenziali coperte: **VALIDATO** offline.
- Runtime: **BLOCCATO**.

Unico prossimo passo: decisione esplicita del titolare su una singola esecuzione
runtime controllata del comando gia congelato. Questa revisione non la autorizza.
