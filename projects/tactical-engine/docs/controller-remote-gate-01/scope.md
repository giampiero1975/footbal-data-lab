# One remote synthetic gate, before execution

Existing RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01; baseline6937df6.
New difference: actual Linux process groups/signals, real elapsed monotonic time,
SSH client intentionally disconnected, remote journal and read-only recovery.
Do not replay the nine Windows fixtures or any historical model test.
One exclusive attempt controller-remote-gate-20261119-01, no retry after dispatch.
Core supervisor is byte-identical to d4d2ee6. The synthetic scenario explicitly
uses timeout12s and the unchanged grace15s, not an accelerated clock. Production
900s is unchanged; this cannot certify a 900s workload or actual Ollama cancel.
The child only writes NDJSON, ignores TERM to exercise real group SIGKILL,
and denies socket/subprocess/exec/spawn/system audit events. No memory stress.
Preflight requires RAM>=4GB, disk>=100MiB, both historical services active,
/api/ps empty, no runner/concurrent test, destination absent. No RAG lock.
At the third sample, the optional relay blocks and the client cuts only its
SSH process. The remote journal/control continue to deadline12+grace15 seconds.
Read-only export/import verifies chain/raw/terminal and post-cleanup receipt.
Deadline/kill tolerance is0.5s, cleanup<=deadline+18s; failures stop without retry.
Finish with process/service read-only snapshots; only owned synthetic processes
may be cleaned. No POST, application changes, model/weights/loading or services.
Technical code must be published before any remote session.
