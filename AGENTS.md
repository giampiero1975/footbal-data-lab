# FOOTBALL-DATA-LAB operating protocol

GitHub is the authoritative source for project status.

Before any technical activity:

1. Read `projects/tactical-engine/todo.md` and
   `projects/tactical-engine/docs/experiment-register.md`.
2. Reconcile both documents with the relevant code, commits, reports, and
   previous results.
3. Check whether an equivalent test has already been completed.

For every activity, preserve this trace in order:

`Activity -> Script -> Commit -> Report -> Result -> Decision -> Status`

Use only these status labels:

- `DA FARE`
- `IMPLEMENTATO`
- `ESEGUITO`
- `VALIDATO`
- `INTEGRATO`
- `CERTIFICATO`
- `BLOCCATO`

Do not propose or execute a test equivalent to one already completed. A new
test is allowed only when a documented technical difference exists or earlier
evidence is insufficient. Record that justification before executing the test.

After every report, update both the experiment register and the TODO in the
same operational session. Do not call an activity complete without verifiable
evidence.

Keep these meanings separate:

- A shadow result can be `VALIDATO` without being `INTEGRATO`.
- Pipeline integration does not imply system `CERTIFICATO` status.
- A successful command can be `ESEGUITO` while its technical hypothesis is not
  `VALIDATO`.

Before declaring work missing, reconcile GitHub state with all available
evidence. Do not reopen or repeat completed work without a newly documented
reason.
