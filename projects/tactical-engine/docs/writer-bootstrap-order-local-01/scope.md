# Writer bootstrap order: scope recorded before the new check

Existing RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01, baseline e6f1fbf.
New delta only: writer fsynced initialization acknowledgement before reader/relay
threads and child READY, active-thread fork rejection, one-shot persistence uses
spawn so final receipts cannot fork after stdin/control threads are running.
One differential local check with its unready-writer and active-thread branches;
no replay of nine fixtures, remote gate, model suites or historical benchmarks.
Production deadlines/guard/cleanup/model payloads unchanged. No SSH or POST.
No Linux distro installed in WSL; Windows results cannot prove native Linux fork.

Targeted rerun: exercise one-shot spawn persistence with the stdin reader already active; use the identical builtin exec target on Windows and Linux. Initial successful bootstrap result preserved, no historical suite repeated.
