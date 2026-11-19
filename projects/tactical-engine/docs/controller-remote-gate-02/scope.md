# Differential remote bootstrap gate — scope before execution

Existing RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01, baseline e8cf22c.
One new exclusive attempt controller-remote-gate-20261119-02; never reuse01.
Technical difference: core40590ee, byte-identical, initializes/fsyncs writer
journal/raw/checkpoint0 and awaits custody_ready ack before reader/relay.
Only remaining blocked properties: real Linux bootstrap, durable READY/reserve
before single synthetic GO, durable sample barrier before SSH cut, journal
continuity after transport EOF and complete read-only recovery/terminal.
Instrumentation records ack before threads and links cut to an acknowledged
sample; no application/pilot/model changes. Prior deadline/TERM/KILL/cleanup
findings reused; same 12s timeout/15s grace and safety bounds retained as
consistency requirements, not additional scenarios. No replay of nine fixtures.
No POST, model loads, services/config/RAG changes, locks, installations or retry.
Preflight resource floors and all previous acceptance bounds unchanged.
Publish technical commit first. On failure stop with artifacts, never rerun.
