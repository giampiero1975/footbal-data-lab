# H1 — Gate documentali prima di toolchain, linking e loading

Precisazioni IMPLEMENTATO nel solo progetto documentale. Non è un gate
eseguibile, non attesta l'ABI VPS e non autorizza alcun tool o worker.
Riferimento: revisione indipendente H1 al commit c99a456.

## Sequenza cumulativa fail-closed

G0 è una verifica documentale, G1–G6 definiscono prove future. In questa sessione
non vengono eseguiti compiler/linker, probe di versione, loader o librerie.
L'ordine è obbligatorio: nessun passo successivo può compensare un precedente
mancante. Prima di qualsiasi invocazione della toolchain devono essere risolti
G0 e G1–G6 sugli input della build; prima di ogni linking/loading si ripete solo
il controllo di validità dello snapshot pertinente e delle sue dipendenze, se
successivamente autorizzato. Non è una ripetizione automatica di test storici.

G0 — Mandato separato, provenienza del dossier e perimetro approvato.
L'approvazione documentale non è autorizzazione alla compilazione/esecuzione.
`execution_authorized=false` e le attestazioni null del target-contract restano
invariati; nessun documento integrativo li converte in true. Identità e flag
non possono essere inferiti dal solo commit o da un nome di simbolo.

| ID | Prerequisito e ordine | Evidenza necessaria prima dell'uso | Condizione di arresto | Proprietà non ancora dimostrata |
|---|---|---|---|---|
| H1-G1 | Compiler, assembler, linker, sysroot e toolchain | Percorsi assoluti reali, hash, origine/versione da dossier attendibile; componenti invocati dal driver inclusi cc1/collect2 o equivalenti; snapshot sysroot e librerie standard | Elemento assente, versione/hash/origine non approvati, selezione tramite PATH o wrapper non attestato: E_H1_TOOLCHAIN | Coerenza della toolchain con il binario installato; nessun compiler viene avviato per colmare il vuoto |
| H1-G2 | Origine di header, oggetti, archivi e librerie | Manifest revisionato dei byte di ogni input e closure degli include; associazione sorgenti/patch/build all'hash VPS; origine degli object anche quando precompilati | File modificato, header sintetico, oggetto non attestato o source override non ricostruito: E_H1_INPUT_PROVENANCE | Layout dei tipi reali e identità integrale sorgente/binario |
| H1-G3 | Flag ABI e macro | Dossier di standard C++, architettura/target, ABI libstdc++, eccezioni, RTTI, allineamento/packing, visibilità, opzioni debug/LTO, macro pertinenti incluse LLAMA_USE_LLGUIDANCE e modalità del parser | Flag ignoto/incompatibile, default assunto o modifica per ottenere GBNF: E_H1_ABI_FLAGS | Compatibilità ABI e dialetto effettivo; C++17 e tag cxx11 da soli non bastano |
| H1-G4 | Percorsi, plugin e ambiente | Allowlist di include/library search path e file reali; opzioni driver/linker, plugin/LTO, file di risposta, variabili di ambiente, preload/audit, cwd e FD ereditabili; toolchain-specific search variables incluse | Include shadowing, plugin o input implicito non attestato, ambiente/FD non chiudibili nel perimetro: E_H1_SEARCH_ENV | Assenza di caricamenti/esecuzioni indotte dalla toolchain e dal loader |
| H1-G5 | Closure dinamica e ABI transitiva | Dipendenze del worker e della toolchain, loader/libc/libstdc++/ggml; percorsi realmente risolti, hash e moduli potenzialmente caricati da plugin o dlopen; regole di isolamento attestabili | DT_NEEDED assunto esaustivo, dipendenza/modulo non inventariato o risoluzione ambigua: E_H1_DEPENDENCY_CLOSURE | Insieme effettivo di codice caricato e compatibilità delle dipendenze transitive |
| H1-G6 | Custodia e assenza di alterazioni fra verifica e uso | Strategia revisionata per snapshot immutabile, directory/symlink, permessi e controllo degli scrittori; associazione stabile fra file verificato e input realmente usato; isolamento dei percorsi e inventario dei prodotti di build | Possibile sostituzione, race, symlink non controllato o impossibilità di vincolare i byte usati: E_H1_CUSTODY | Assenza di TOCTOU e corrispondenza fra hash verificati e byte compilati/linkati/caricati |

## Tre confini da non confondere

- **Prima della toolchain:** attestare driver e strumenti richiamati, include,
  object, flag, ambiente e closure. Il compiler/linker può caricare plugin:
  la verifica non può essere rinviata al main del programma prodotto.
- **Prima del linking:** richiedere provenienza degli oggetti generati e dei
  file di risposta/opzioni effettivi, identità del linker e plugin. La riuscita
  della compilazione non attesta ABI o provenienza degli object.
- **Prima del loading:** verificare il worker e le dipendenze realmente
  risolvibili nello snapshot approvato; il gate è esterno al processo linkato.
  Costruttori/loader possono agire prima del main. Nessun caricamento di prova
  è un sostituto del gate, e non è autorizzato qui.

Nessuno dei confini è superabile mediante ctypes, cast ABI, ricompilazione
upstream sostitutiva o cambiamento dei manifest già approvati.

## Custodia e fallimento

Il disegno futuro deve scegliere e revisionare il meccanismo concreto di
immutabilità/ispezione prima di implementarlo. Rileggere hash o inode subito
prima dell'uso, senza impedire scritture concorrenti, non elimina da solo una
race. Devono risultare controllati anche antenati, directory e risoluzione di
symlink. Ogni prodotto generato deve essere attribuito a input/toolchain/flag
attestati prima che diventi input del passo seguente.

Se una prova di G1–G6 manca, è contraddittoria o non vincola l'uso effettivo,
arresto prima dell'invocazione interessata: registrare ID gate, atteso/osservato,
provenienza, hash disponibili e proprietà non dimostrata. Non eseguire il tool
per vedere se funziona. Nessun percorso operativo, servizio o libreria VPS
viene toccato per raccogliere queste prove in questa attività.

## Collegamento ai manifest congelati

sources-lock.json e target-contract.json restano byte-identici al commit
c99a456. Questa specifica dettaglia le attestazioni già richieste, non aggiunge
un'attestazione e non riscrive un'identità. Il metodo di acquisizione delle
prove ABI è DA FARE in un'attività separata. Implementazione e backend BLOCCATO.
