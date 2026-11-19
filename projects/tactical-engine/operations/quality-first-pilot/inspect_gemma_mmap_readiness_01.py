"""Read versioned files only; no imports of pilot code, SSH or model calls."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
OUT=PROJECT/'docs/gemma26-mmap-post-gate02-readiness-01'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def main():
    OUT.mkdir(exist_ok=False)
    (OUT/'.gitattributes').write_bytes(b'* -text\n')
    historical=PROJECT/'evaluation/gemma_mmap_on_01/call-01/request.json'
    call=json.loads(historical.read_bytes())
    manifest=json.loads((HERE/'prepared/pilot_manifest_01.json').read_bytes())
    proposal=next(c for c in manifest['calls'] if c['candidate']=='gemma' and c['case']=='V10-02')
    proposal['payload']['options']['use_mmap']=True
    assert proposal['payload']==call['payload']
    raw=json.dumps(call['payload'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
    assert sha(raw)==call['payload_sha256']
    binding=json.loads((PROJECT/'docs/quality-first-pilot-authorized-readiness-01/execution_binding_03.json').read_bytes())
    gate=json.loads((PROJECT/'evaluation/controller_remote_gate_02/remote-code-manifest.json').read_bytes())
    code={name:sha((HERE/name).read_bytes()) for name in (
        'paired_pilot_01.py','pilot_supervision_01.py','paired_pilot_remote_01.py',
        'gemma_mmap_on_01.py','gemma_mmap_observation_01.py')}
    assert gate['files']['pilot_supervision_01.py']['sha256']==code['pilot_supervision_01.py']
    (OUT/'payload.frozen.json').write_bytes(raw)
    facts={'activity':'RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01',
        'baseline':'12a6c113757bbe5531b28f1516fee5d1bad332e0',
        'scope':'offline documentary inspection only; no application test',
        'payload_sha256':sha(raw),'payload_bytes':len(raw),'source':historical.relative_to(PROJECT).as_posix(),
        'case':'V10-02','ordinal':call['ordinal'],'payload_identical_to_historical':True,
        'model':binding['models']['gemma'],'parameters':{k:v for k,v in call['payload'].items() if k!='messages'},
        'draft_in_payload':{k:v for k,v in call['payload']['options'].items() if 'draft' in k or 'speculat' in k},
        'core_identical_to_Gate02':True,'code_sha256':code,
        'proposed_attempt_id':'gemma-mmap-on-02','proposed_local_ledger':'evaluation/gemma_mmap_on_02',
        'proposed_remote_attempt_id':'gemma-mmap-on-02-call-01',
        'authorization':False,'launchable_now':False,
        'pending':['new explicitly authorized single-case launcher and frozen binding',
                   'exclusive new ledger and remote custody authorization',
                   'immediate volatile preflight before any POST',
                   'real Ollama terminal and post-STOP quiescence not demonstrated by synthetic Gate02'],
        'SSH':0,'POST':0,'models_loaded':0,'tests_replayed':0}
    (OUT/'facts.json').write_bytes((json.dumps(facts,indent=2)+'\n').encode())
    inputs=[historical,HERE/'prepared/pilot_manifest_01.json',
            PROJECT/'docs/quality-first-pilot-authorized-readiness-01/execution_binding_03.json',
            PROJECT/'evaluation/controller_remote_gate_02/remote-code-manifest.json']
    inputs += [HERE/name for name in code]
    (OUT/'inputs.json').write_bytes((json.dumps([{'path':p.relative_to(PROJECT).as_posix(),
        'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in inputs],indent=2)+'\n').encode())
    print(json.dumps({'payload_sha256':sha(raw),'identical':True,'authorization':False,'SSH':0,'POST':0}))


if __name__=='__main__':main()
