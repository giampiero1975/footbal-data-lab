"""Documentary inventory only: immutable answers/context, no imports or tests."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

PROJECT=Path(__file__).resolve().parents[2]
OUT=PROJECT/'docs/gemma26-qwen9-tactical-review-01'
REV='5b2df052b0260139acfa12684ae1267677fd7047'


def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path):return json.loads(path.read_bytes())
def save(name,value):(OUT/name).write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())


def main():
    OUT.mkdir(exist_ok=False)
    (OUT/'.gitattributes').write_bytes(b'* -text\n')
    payload=read(PROJECT/'evaluation/gemma_mmap_on_02/call-01/request.json')['payload']
    gemma=(PROJECT/'evaluation/gemma_mmap_on_02/answer.txt').read_text(encoding='utf-8')
    originals=[];rows=[]
    for version in ('v6','v7','v8','v9','v10'):
        path=PROJECT/('evaluation/coverciano-remediation-'+version+'/case_02.json')
        data=read(path);q=data['questions'][0]
        user='DOMANDA:\n'+q['question']+'\n\nFONTI:\n'+'\n\n'.join(
            '[F%d] Fonte: %s | Pagine: %s\n%s'%(i,e['source'],e['pages'],e['text'])
            for i,e in enumerate(q['evidence'],1))
        rows.append({'version':version,'original_path':path.relative_to(PROJECT).as_posix(),
            'original_sha256':sha(path.read_bytes()),'model_recorded':data['model'],
            'model_digest_in_individual_record':data.get('model_digest'),
            'question':q['question'],'answer':q['answer'],'evidence':q['evidence'],
            'same_question_as_Gemma':payload['messages'][1]['content'].split('\n\nFONTI:')[0]=='DOMANDA:\n'+q['question'],
            'reconstructed_user_message_identical_to_Gemma':user==payload['messages'][1]['content'],
            'generation':q.get('generation'),'elapsed_seconds':q.get('elapsed_seconds'),
            'answer_words':len(q['answer'].split()),'actual_wire_system_prompt_available':False,
            'pipeline_final_not_unsanitized_wire':True,'RAM_trace_in_individual_record':False})
        originals.append(path)
    assert all(x['model_recorded']=='qwen3.5:9b' and x['same_question_as_Gemma'] for x in rows)
    rd=read(PROJECT/'evaluation/rd-think-01-result.json')
    rubric=rd['rubric_fixed_before_execution']
    save('comparison-inputs.json',{'Gemma':{'answer':gemma,'payload':payload,'runtime':read(PROJECT/'evaluation/gemma_mmap_on_02/summary.json')},
         'Qwen9_same_question':rows,'rubric_weights_only':rubric,
         'numeric_scores_assigned':False,'reason':'Approved sources give weights, not complete anchored /30 scoring grid.',
         'case':'A: same question, V7-V10 same sources; prompt/configuration not equivalent'})
    source=subprocess.check_output(['git','show',REV+':projects/tactical-engine/scripts/smoke_test_rag_v5_e2e.py']).decode()
    tree=ast.parse(source);extract={}
    for n in tree.body:
        if isinstance(n,ast.FunctionDef) and n.name in ('chat','scoped_guidance','generation_guidance','generation_contract','sanitize_tactical_output'):
            extract[n.name]=ast.get_source_segment(source,n)
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SYSTEM' for t in n.targets):
            extract['SYSTEM']=ast.get_source_segment(source,n)
    save('historical-caller-source.json',{'commit':REV,'path':'scripts/smoke_test_rag_v5_e2e.py',
        'source_sha256':sha(source.encode()),'source_only_not_recorded_wire':True,
        'executed_source_revision_not_attested_by_case_file':True,'extracts':extract})
    references=['docs/rag-v5-gemma-mmap-on-02.md','evaluation/gemma_mmap_on_02/answer.txt',
        'evaluation/gemma_mmap_on_02/call-01/request.json','evaluation/gemma_mmap_on_02/summary.json',
        'evaluation/rd-think-01-result.json','scripts/compare_frozen_thinking_rd01.py',
        'docs/rd-think-01-runtime-01.md','docs/rag-v5-quality-first-paired-pilot-protocol-review-01.md',
        'docs/rag-v5-quality-first-local-coach-selection-01.md','docs/coverciano-rag-only-100-protocol-01.md',
        'docs/coverciano-rag-only-100-report-01.md','docs/rag-coverciano-remediation-v10-runtime-01.md']
    originals += [PROJECT/x for x in references]
    save('source-inventory.json',[{'path':p.relative_to(PROJECT).as_posix(),'bytes':p.stat().st_size,
         'sha256':sha(p.read_bytes())} for p in originals])
    print(json.dumps({'same_question_Qwen9_answers':len(rows),'same_reconstructed_user_messages':sum(x['reconstructed_user_message_identical_to_Gemma'] for x in rows),
          'numeric_scores_assigned':False,'SSH':0,'POST':0,'new_tests':0}))


if __name__=='__main__':main()
