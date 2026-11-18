# Revisione03 — differenza registrata prima dei controlli
2026-11-18, attività invariata RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01.
Consenso: prosecuzione del prompt operativo conclusivo con «ok andiamo avanti allora».
Baseline81143cd, branch/GitHub allineati, tree pulito; nuovo ledger03 assente.
Il ledger01 resta immutabile. Nessuna suite storica viene ripetuta.
Delta: non arrestarsi per due pagine globali swap-in. Soglia RAM invariata:
STOP immediato sotto4000000000 byte MemAvailable. Pressione persistente:
STOP se il tasso globale swap-in+out è >=64MiB/s per almeno5 secondi
consecutivi e MemAvailable<6000000000 byte. Campioni nominali1s, intervalli
monotonic reali, page size dal kernel; campioni con contatori decrescenti
arrestano per incoerenza. È una protezione operativa prudenziale, non una
soglia scientifica di thrashing né attribuzione esclusiva al modello.
Rifiuti HTTP espliciti conclusi possono proseguire agli slot successivi solo
con servizi attivi, RAM>=4GB, modello scaricato e nessun runner residuo.
Timeout, EOF/incompletezza, monitor abort e stato ambiguo fermano tutto.
Nuovo tentativo fisso03 con creazione esclusiva, max6, zero retry, nessun
reset/resume. Parametri, fonti, ordine e limiti restanti preservati.
Controlli sintetici nuovi: paging isolato, pressione persistente, reset,
RAM sotto soglia, elapsed reale/page size e contatori invalidi; controlli
statici sul ramo HTTP, duplicati e identità del payload preesistente.
