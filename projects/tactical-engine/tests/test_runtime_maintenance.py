import importlib.util
from pathlib import Path
import tempfile,time,unittest

PATH=Path(__file__).parents[1]/"scripts/maintain_rag_v5_runtime.py"
spec=importlib.util.spec_from_file_location("maintain",PATH); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class MaintenanceTests(unittest.TestCase):
    def test_only_old_job_artifacts_are_planned(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); now=time.time(); old=now-40*86400
            for name in ("a"*32+".request.json","a"*32+".result.json","metrics.json","report.json"):
                p=root/name;p.write_text("{}");
                if name.startswith("a"): p.touch(); __import__('os').utime(p,(old,old))
            plan=m.cleanup_plan(root,now,30,1)
            self.assertEqual(plan,[])
            plan=m.cleanup_plan(root,now,30,0)
            self.assertEqual({x.name for x in plan},{"a"*32+".request.json","a"*32+".result.json"})

    def test_new_and_non_job_files_are_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/("b"*32+".request.json");p.write_text("{}")
            (root/"control-plane-load-v1.json").write_text("{}")
            self.assertEqual(m.cleanup_plan(root,time.time(),30,100),[])

if __name__=="__main__": unittest.main()
