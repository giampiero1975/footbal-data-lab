#!/usr/bin/env python3
"""Offline differential test of the reviewer Pacific-day ledger expressions."""
import ast
import datetime as dt
import json
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCE = Path(__file__).with_name("review_rag_v5_gemini_remaining_v1.py")
tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
body = main.body
target = next(i for i, n in enumerate(body) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "now" for t in n.targets))
snippet = body[target:target+2]
count_line = next(n for n in ast.walk(main) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "count" for t in n.targets))
write_line = next(n for n in ast.walk(main) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == "used" for t in n.targets))
def simulate(iso, ledger):
    now = dt.datetime.fromisoformat(iso)
    today = now.astimezone(ZoneInfo("America/Los_Angeles")).date().isoformat()
    used = dict(ledger)
    count = eval(compile(ast.Expression(count_line.value), str(SOURCE), "eval"), {"used": used, "now": now, "today": today})
    exec(compile(ast.Module(body=[write_line], type_ignores=[]), str(SOURCE), "exec"), {"used": used, "today": today, "count": count})
    return today, count, used
cases = [
    ("legacy_same_day", "2026-10-23T14:00:00+00:00", {"2026-10-23": 3}, "2026-10-23", 3, 4),
    ("before_pt_midnight", "2026-10-24T06:59:00+00:00", {"PT:2026-10-23": 4}, "2026-10-23", 4, 5),
    ("after_pt_midnight", "2026-10-24T07:01:00+00:00", {"PT:2026-10-23": 4}, "2026-10-24", 0, 1),
    ("winter_before_midnight", "2026-12-01T07:59:00+00:00", {"PT:2026-11-30": 2}, "2026-11-30", 2, 3),
    ("winter_after_midnight", "2026-12-01T08:01:00+00:00", {"PT:2026-11-30": 2}, "2026-12-01", 0, 1),
]
results = []
for name, instant, ledger, expected_day, expected_count, expected_new in cases:
    day, count, updated = simulate(instant, ledger)
    passed = day == expected_day and count == expected_count and updated["PT:" + day] == expected_new
    results.append({"case": name, "passed": passed, "day": day, "used_before": count})
report = {"status": "VALIDATO" if all(x["passed"] for x in results) else "BLOCCATO", "api_requests": 0, "real_ledger_modified": False, "cases": results}
print(json.dumps(report, indent=2))
if report["status"] != "VALIDATO":
    raise SystemExit(1)
