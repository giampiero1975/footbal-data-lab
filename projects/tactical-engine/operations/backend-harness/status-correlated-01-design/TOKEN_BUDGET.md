# Metodo separato — budget token senza pesi o generazione

Questo è un progetto documentale, non un tokenizer implementato o eseguito.
Valori documentali preservati: handoff 6.967 byte, user storico 7.311 byte,
schema 16.869 byte; num_ctx=4096, num_predict=2048, think=false.
Nessun rapporto byte/token e nessun conteggio reale prodotto.

## 1. Gate identità

Riutilizzare le evidenze già versionate: modello qwen3.5:9b, manifest
56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90;
GGUF tokenizer.ggml.model=gpt2, pre=qwen35, vocab 248.320, merges 247.587,
EOS 248046, padding 248044, add_bos_token=false. Pin degli array codificati e
del template GGUF dagli hash della ricognizione. Non risostituirli con un
tokenizer genericamente GPT-2, Hugging Face o con regex replicate a mano.

Il blob template {{ .Prompt }}, la stringa Jinja GGUF e il renderer Go qwen3.5
sono livelli distinti. La presenza del secondo non dimostra che venga usato.
Nel sorgente Ollama pubblico alla revisione di sources-lock.json, renderPrompt
sceglie il renderer configurato prima del template Go; req.Think esplicito passa
al renderer. Per questo candidato usare la configurazione renderer=qwen3.5,
tools vuoti, nessuna immagine/media, due messaggi system/user e think=false.
La corrispondenza al servizio installato resta da attestare: nessuna esecuzione
Go, renderizzazione o richiesta al runner è fatta adesso.

## 2. Rendering riproducibile previsto

Estrarre un adattatore puro dai sorgenti Ollama attestati con le dipendenze
originali; NON riscrivere il renderer. Congelare dati di input, percorso
selezionato e opzioni, preservando whitespace, special token, BOS/EOS e
prefisso assistant. Conservare hash dei messaggi e dei byte renderizzati.
Registrare separatamente template/renderer selezionato, think=false e flag
applicati; una stringa scelta manualmente non è una misura effettiva.

Nel candidato pubblico format oggetto viene passato come json_schema. Il ramo
ThinkingClose può convertirlo e incapsulare la grammatica. Non deriva che lo
schema sia testo del prompt né che non abbia alcun effetto indiretto. Tracciare
questo ramo e documentare se modifica i byte renderizzati. Non chiamare
schemaGrammar, che usa POST /completion su un runner, neppure con n_predict=0.
Nessuna scorciatoia HTTP è ammessa dal progetto.

## 3. Tokenizzazione ufficiale prevista, non alternativa

Il candidato API llama.h offre llama_tokenize con add_special e parse_special;
le differenze di flag incidono sul conteggio. Il percorso pubblico Ollama usa
Tokenize(addSpecial=false) per il conteggio di chatPrompt e un ulteriore
addSpecial=true nel possibile troncamento di completionPromptForRequest.
Occorre ricostruire entrambi, compreso il trattamento BOS del runner e il
default parse_special del relativo endpoint, non assumere un unico conteggio.

La via candidata senza pesi è un adattatore ufficiale vocabulary-only:
llama_model_params.vocab_only=true e API originale di vocabolario/tokenizzazione,
nessun contesto inferenziale o sampler. Non è implementato: prima servono
header/ABI attestati e verifica del loader/compat patch per dimostrare che
nessun tensore venga letto, mmap-pato o trasferito e nessun backend pesi venga
inizializzato. Il flag da solo non è prova sulla build installata.
Se questi requisiti non sono dimostrabili, il conteggio resta **BLOCCATO**;
non è autorizzato un caricamento completo come ripiego. Il worker grammatica
rimane completamente separato dal GGUF, anche se il worker token futuro
consumasse soltanto il vocabolario ufficiale.

## 4. Contesto, troncamento e output richiesto

Il sorgente pubblico chatPrompt prova suffissi della cronologia conservando
system e ultimo messaggio. completionPromptForRequest può rifiutare input troppo
lunghi oppure applicare context shift, in base alla configurazione; distingue
limite NumCtx-1 e num_keep. Non applicare una regola inventata
num_ctx-num_predict come se fosse la politica del server.

La misura futura deve conservare:

- token prima e dopo ciascun passaggio verificato di rendering/troncamento;
- flag add_special/parse_special e sequenza/hashes degli ID prodotti;
- messaggi mantenuti, byte/hashes prima e dopo; nessuna correzione silenziosa;
- contesto richiesto 4096 e contesto effettivo se attestato, ContextShift,
  num_keep, opzioni effettive e n_predict richiesto 2048;
- margine per l'output richiesto senza shift, distinto dalla politica effettiva.

Un conteggio inferiore a 4096 non garantisce 2048 token di output disponibili.
Il contesto modello dichiarato 262144 non cambia il contesto richiesto 4096.
Ogni parametro attivo non attestato lascia la relativa conclusione non
verificata; l'esito non può essere una generazione di prova.

## 5. Risultato attuale

Conteggio token: non verificato. Rendering: non eseguito. Tokenizer: non
implementato. Nessun peso, modello, servizio o richiesta HTTP utilizzato nella
progettazione. Metodo idoneo alla revisione indipendente come piano; la sua
realizzazione richiede evidenze separate dalle firme del convertitore.
