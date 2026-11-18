"""New tests only for revision03 paging/continuation; no network or worker execution."""
import ast
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=ROOT/"projects/tactical-engine/docs/quality-first-pilot-authorized-readiness-01/revision03_delta_checks.json"
worker=(HERE/"paired_pilot_remote_01.py").read_text()
controller=(HERE/"paired_pilot_01.py").read_text()
for name,source in (("worker",worker),("controller",controller)):
    compile(source,name,"exec")
tree=ast.parse(worker)
function=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=="pressure_step")
scope={}
exec(compile(ast.Module(body=[function],type_ignores=[]),"pressure_step_only","exec"),scope)
step=scope["pressure_step"]
rows=[]
def check(name,condition):
    assert condition,name
    rows.append({"check":name,"result":"PASS"})
def sample(mem=5500000000,i=100,o=100):
    return {"available_bytes":mem,"swap_in":i,"swap_out":o}
a=sample()
check("isolated_two_pages_allowed",step(a,sample(i=102),1,0,4096)[1] is None)
state=0
for t in range(1,6):
    state,reason,rate=step(sample(i=(t-1)*16384),sample(i=t*16384),1,state,4096)
    check("sustained_64MiB_second_%d"%t,(reason=="E_PERSISTENT_PAGING") == (t==5))
check("pressure_reset",step(a,a,1,4,4096)[0]==0)
check("ram_floor_immediate",step(a,sample(mem=3999999999),1,0,4096)[1]=="E_MEMORY_RESERVE")
check("high_memory_paging_diagnostic",step(a,sample(mem=6500000000,i=16484),1,0,4096)[1] is None)
check("actual_elapsed_and_page_size",step(a,sample(i=16484),2,0,8192)[2]==64*1024*1024)
check("counter_decrease_stops",step(a,sample(i=99),1,0,4096)[1]=="E_RESOURCE_COUNTER")
check("no_end_zero_paging_veto",'end["swap_in"], end["swap_out"]' not in worker)
check("explicit_http_error_requires_quiescence",'response.status >= 400' in worker and 'and not runner_processes() and not concurrent_processes()' in worker and 'safe_to_continue=safe' in worker)
check("no_retry_single_post_site",worker.count('connection.request("POST", "/api/chat"')==1)
check("revision_duplicate_guard",'evaluation/quality_first_paired_pilot_03' in controller and 'LEDGER.mkdir(exist_ok=False)' in controller and 'previous_stop_sha256' in controller)
# Safe controller import constructs no requests, workers or ledger.
spec=importlib.util.spec_from_file_location("pilot03",HERE/"paired_pilot_01.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
old=json.loads((HERE/"prepared/pilot_manifest_01.json").read_bytes())
plan=m.make_plan()
check("six_payloads_byte_identical_to_revision02",plan["calls"]==old["calls"])
for item in (ROOT/"projects/tactical-engine/evaluation/quality_first_paired_pilot_01").rglob("inventory.json"):
    import hashlib
    for row in json.loads(item.read_bytes())["files"]:
        b=(item.parent/row["path"]).read_bytes()
        assert len(b)==row["bytes"] and hashlib.sha256(b).hexdigest()==row["sha256"]
check("previous_ledger_inventory_unchanged",True)
assert not m.LEDGER.exists()
OUT.write_bytes((json.dumps({"scope":"revision03 delta; justification revision03_scope.md predates checks", "checks":rows,"generative_posts":0},indent=2)+"\n").encode())
print(json.dumps({"new_delta_checks":len(rows),"result":"PASS","posts":0}))
