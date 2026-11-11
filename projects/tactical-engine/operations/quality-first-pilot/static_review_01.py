"""New static delta review: six-case schedule, guard ordering and whitelist.

Not a model/application test suite; never imports either driver or worker.
Only AST/compile-in-memory, file identities and prepared JSON are inspected.
"""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PROJECT = ROOT / "projects/tactical-engine"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def main():
    results = []

    def record(name, condition, evidence):
        results.append({"check": name, "passed": bool(condition), "evidence": evidence})
        if not condition:
            raise AssertionError(name)

    sources = {}
    trees = {}
    functions = {}
    for name in ("paired_pilot_01.py", "paired_pilot_remote_01.py"):
        raw = (HERE / name).read_bytes()
        text = raw.decode("utf-8")
        trees[name] = ast.parse(text)
        compile(text, name, "exec")  # Compile a code object, never execute it.
        sources[name] = {"sha256": digest(raw), "bytes": len(raw),
                         "git_blob": subprocess.check_output(
                             ["git", "-C", str(ROOT), "hash-object", str(HERE / name)], text=True).strip()}
        functions[name] = {node.name: node for node in trees[name].body if isinstance(node, ast.FunctionDef)}
        record("syntax_" + name, True, "AST and in-memory compile only")
        imports = [node.module or "" for node in ast.walk(trees[name]) if isinstance(node, ast.ImportFrom)]
        imports += [a.name for node in ast.walk(trees[name]) if isinstance(node, ast.Import) for a in node.names]
        record("no_application_or_model_import_" + name,
               not any(x.startswith(("transformers", "torch", "llama", "v5_", "shadow_", "ctypes")) for x in imports), imports)

    driver = functions["paired_pilot_01.py"]
    # Reachability of local prepare/check through direct named function calls.
    reachable = set()
    pending = ["prepare", "check"]
    while pending:
        name = pending.pop()
        if name in reachable:
            continue
        reachable.add(name)
        for node in ast.walk(driver[name]):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in driver:
                pending.append(node.func.id)
    record("prepare_check_no_transport_reachability",
           not reachable.intersection({"execute", "one_remote", "git", "anonymize", "bind"}), sorted(reachable))
    record("local_modes_no_network_modules",
           not any(isinstance(n, ast.Import) and any(a.name.startswith(("urllib", "http", "socket")) for a in n.names)
                   for n in trees["paired_pilot_01.py"].body), "Networking exists only in dormant remote worker")

    plan = json.loads((HERE / "prepared/pilot_manifest_01.json").read_text(encoding="utf-8"))
    calls = plan["calls"]
    record("schedule_six_unique_slots", len(calls) == 6 and
           len({(x["case"], x["candidate"]) for x in calls}) == 6, [(x["case"], x["candidate"]) for x in calls])
    record("approved_execution_order", [x["candidate"] for x in calls] ==
           ["gemma", "qwen", "qwen", "gemma", "gemma", "qwen"], "Predefined alternating order; no balancing claim")
    for source in plan["inputs"]:
        raw = (PROJECT / source["source"]).read_bytes()
        item = json.loads(raw)["questions"][0]
        record("immutable_input_" + source["case"], digest(raw) == source["source_sha256"]
               and source["question"] == item["question"] and source["evidence"] ==
               [{k: f[k] for k in ("label", "id", "source", "pages", "text")} for f in item["evidence"]],
               source["source_sha256"])
        pair = [x for x in calls if x["case"] == source["case"]]
        messages = pair[0]["payload"]["messages"]
        record("equal_messages_" + source["case"], messages == pair[1]["payload"]["messages"], digest(canonical(messages)))
        rendered = "\n".join(x["content"] for x in messages)
        record("no_historical_answer_" + source["case"], item["answer"] not in rendered,
               "Plus construction whitelist; does not claim automated semantic proof of every possible leak")
    record("case_whitelist", all(set(x) == {"case", "source", "source_sha256", "question", "evidence"}
                                 for x in plan["inputs"]), "No tactical_plan, answer, Gold or evaluation copied")
    record("payload_limits_and_hashes", all(
        digest(canonical(x["payload"])) == x["payload_sha256"]
        and set(x["payload"]) == {"model", "messages", "think", "stream", "keep_alive", "options"}
        and x["payload"]["options"]["num_ctx"] == 8192
        and x["payload"]["options"]["num_predict"] == 4096
        and x["payload"]["stream"] is True and x["payload"]["think"] is True
        and x["payload"]["keep_alive"] == 0 for x in calls), "No JSON format, tools, continuations or model-supplied assistant turns")
    record("driver_worker_freeze", all(plan["code"][name] == facts["sha256"] for name, facts in sources.items()), sources)
    pending_binding = json.loads((HERE / "prepared/remote_binding.pending.json").read_text())
    pending_auth = json.loads((HERE / "prepared/execution_authorization.pending.json").read_text())
    record("execution_disabled_in_prepared_files", pending_binding["verified"] is False
           and not any(pending_binding["checks"].values()) and pending_auth["authorized"] is False
           and pending_auth["binding_sha256"] is None, "No valid remote dossier or authorization manufactured")
    record("no_pilot_attempt_created", not (PROJECT / "evaluation/quality_first_paired_pilot_01").exists(), "Canonical activity ledger absent")

    remote = trees["paired_pilot_remote_01.py"]
    parents = {child: parent for parent in ast.walk(remote) for child in ast.iter_child_nodes(parent)}
    posts = [node for node in ast.walk(remote) if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Attribute) and node.func.attr == "request"
             and len(node.args) >= 2 and isinstance(node.args[0], ast.Constant)
             and node.args[0].value == "POST" and isinstance(node.args[1], ast.Constant)
             and node.args[1].value == "/api/chat"]
    record("one_generative_call_site", len(posts) == 1, [n.lineno for n in posts])
    ancestors = []
    node = posts[0]
    while node in parents:
        node = parents[node]
        ancestors.append(node)
    record("post_outside_retry_loops", not any(isinstance(n, (ast.For, ast.While)) for n in ancestors), "Worker main one-shot path; six-call schedule is in local controller")
    remote_text = (HERE / "paired_pilot_remote_01.py").read_text()
    go_guards = [n.lineno for n in ast.walk(remote) if isinstance(n, ast.Compare)
                 and any(isinstance(x, ast.Constant) and x.value == bytes([71, 79, 10]) for x in ast.walk(n))]
    record("remote_go_precedes_post", len(go_guards) == 1 and go_guards[0] < posts[0].lineno,
           "AST: durable-GO guard precedes sole POST")
    local_text = (HERE / "paired_pilot_01.py").read_text()
    local_tree = trees["paired_pilot_01.py"]
    go_writes = [n.lineno for n in ast.walk(local_tree) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute) and n.func.attr == "write"
                 and n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value == bytes([71, 79, 10])]
    reservations = [n.lineno for n in ast.walk(local_tree) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Name) and n.func.id == "save"
                    and n.args and any(isinstance(x, ast.Constant) and x.value == "reserved-before-GO.json"
                                       for x in ast.walk(n.args[0]))]
    record("durable_reservation_precedes_go", len(go_writes) == len(reservations) == 1
           and reservations[0] < go_writes[0], "AST plus exclusive xb -> flush/fsync in save")
    record("exclusive_ledger_no_resume", 'LEDGER.mkdir(exist_ok=False)' in local_text and
           'choices=("prepare", "check", "execute", "anonymize")' in local_text,
           "Fixed activity-wide location; no reset/resume or alternate ledger option")
    record("read_only_existing_lock", 'os.O_RDONLY | os.O_NOFOLLOW' in remote_text and
           'fcntl.LOCK_EX | fcntl.LOCK_NB' in remote_text, "No lock-file create/chmod")
    record("memory_swap_deadline_guards", all(x in remote_text for x in
           ['4000000000', 'value["swap_in"] != baseline["swap_in"]',
            'value["swap_out"] != baseline["swap_out"]', 'time.monotonic() - began >= 900']),
           "Static guard presence, actual sampling/abort behavior not executed")
    record("context_proof_bound_to_payload", all(x in local_text for x in
           ['proof["payload_sha256"] != call["payload_sha256"]',
            'proof["tokenizer_sha256"] != model["tokenizer_sha256"]',
            'not 0 < proof["prompt_tokens"] <= 4096']), "Reviewed external proof required; no byte-to-token estimator")
    record("blind_export_final_only", '"answer": result["content"]' in local_text and
           'save(LEDGER / "custodian-map.json", mapping)' in local_text,
           "Random opaque IDs; private map outside blind folder; no inferred scores")
    record("raw_inventory_before_blind_export", 'E_REVIEW_ORIGINAL_CHANGED' in local_text and
           '"inventory": inventory' in local_text, "Hashes checked before export; metadata/resources withheld")

    output = {"activity": plan["activity"], "phase": "local technical preparation",
              "method": "Static AST/compile, file hashes and JSON manifest inspection only",
              "new_delta": "Six frozen unique slots, whitelist, durable GO, paired manifest, blocked remote binding; no historical suite repeated",
              "checks": results, "passed": len(results), "failed": 0, "sources": sources,
              "plan_sha256": digest(canonical(plan)), "pilot_status": "DA FARE",
              "remote_worker_executed": False, "SSH_executed": False,
              "generations": 0, "remote_runtime_compatibility_verified": False,
              "not_proven": ["remote ABI/profile/template compatibility", "token counts",
                             "resource/supervision behavior", "stream parsing on installed build",
                             "end-to-end driver runtime behavior", "tactical accuracy"]}
    destination = PROJECT / "docs/quality-first-pilot-local-preparation-static-01.json"
    with destination.open("xb") as handle:
        handle.write((json.dumps(output, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"static_checks": len(results), "failed": 0, "generations": 0,
                      "pilot_status": "DA FARE", "evidence": str(destination)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
