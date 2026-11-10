"""Read-only static review facts; never imports or executes project modules/tests.

Run from repository root: python -B projects/tactical-engine/docs/remediation-a-independent-static-audit-01.py
Only AST, versioned JSON and Git object reads. No domain calls or assertions.
"""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
DOCS = Path(__file__).resolve().parent
TECH = '0ea62c0ef1f0adfcd928c2893f069de060275381'
BASE = '13814c20d80bca4d9cb4cb08a288b6e7b31dac0d'
PREFIX = 'projects/tactical-engine/scripts/'
JUDGE = PREFIX + 'shadow_nli_spatial_relations_v2_inference.py'
EXT = PREFIX + 'v5_tactical_semantic_support_s2_spatial_v2_extraction.py'
FINAL = PREFIX + 'v5_tactical_semantic_support_s2_spatial_v2.py'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def source(rev, path):
    return git('show', rev + ':' + path).decode('utf-8')

def funcs(text):
    return {n.name: n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef)}

def literal_assignment(text, name):
    return next(n.value for n in ast.parse(text).body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))

new = source(TECH, EXT)
old = source(TECH + '^', EXT)
final = source(TECH, FINAL)
# Decode only literal constant data; frozenset calls are read as syntax, not executed.
axes = ast.literal_eval(literal_assignment(final, 'AXIS_VALUES'))
pairs_node = literal_assignment(final, 'INCOMPATIBLE_VALUES')
pairs = {ast.literal_eval(k): sorted(sorted(ast.literal_eval(p.args[0])) for p in v.elts)
         for k, v in zip(pairs_node.keys, pairs_node.values)}
substitutions = {'matrix': {k: sorted(v) for k, v in sorted(axes.items())},
                 'incompatible': dict(sorted(pairs.items()))}
ret = next(n.value for n in funcs(new)['extraction_handoff_instructions'].body
           if isinstance(n, ast.Return))

def text_expression(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return text_expression(node.left) + text_expression(node.right)
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name) and node.func.value.id == 'json'
            and node.func.attr == 'dumps' and isinstance(node.args[0], ast.Name)):
        return json.dumps(substitutions[node.args[0].id], sort_keys=True)
    raise ValueError('Unsupported AST syntax: no project execution allowed')

instruction = text_expression(ret)
old_instruction = ast.literal_eval(literal_assignment(source(TECH + '^', JUDGE), 'EXTRACTION_INSTRUCTION'))
artifacts = ROOT / 'projects/tactical-engine/evaluation/runtime04_execution_01/artifacts'
payload = json.loads((artifacts / 'request_payload.json').read_bytes())['payload']
raw = json.loads((artifacts / 'raw_response.json').read_bytes())
inputs = json.loads((artifacts / 'input.json').read_bytes())
new_user = instruction + '\n\nFONTE:\n' + inputs['evidence'] + '\n\nAFFERMAZIONE:\n' + inputs['claim']
prior_results = json.loads((DOCS / 'runtime04-remediation-a-offline-results-01.json').read_bytes())
old_funcs, new_funcs = funcs(old), funcs(new)
critical = ['extraction_semantic_errors', '_occurrences', '_localize_fragments',
            '_materialize_relation', '_provenance', 'boundary_failure',
            'materialize_extraction', 'verify_materialization']
facts = {
    'activity': 'RD-RAG-V5-DUAL-BLOCKER-REMEDIATION-A-INDEPENDENT-REVIEW-01',
    'technical_commit': TECH,
    'reviewed_documentary_head': 'c864040a8e07885db700b01f4388d2ca47d9153a',
    'method': 'AST and literal/JSON/Git reads only; no application imports, domain calls or tests',
    'technical_changed_paths': git('diff', '--name-only', TECH + '^', TECH).decode().splitlines(),
    'reviewed_source_sha256': {p: hashlib.sha256(git('show', TECH + ':' + p)).hexdigest()
                               for p in (JUDGE, EXT, FINAL)},
    'critical_function_ast_unchanged': {n: ast.dump(old_funcs[n]) == ast.dump(new_funcs[n]) for n in critical},
    'final_validator_diff_since_baseline': git('diff', '--name-only', BASE, TECH, '--', FINAL).decode().splitlines(),
    'instruction_old_utf8_bytes': len(old_instruction.encode()),
    'instruction_new_utf8_bytes_static_reconstruction': len(instruction.encode()),
    'instruction_new_characters': len(instruction),
    'system_message': payload['messages'][0],
    'prior_user_utf8_bytes': len(payload['messages'][1]['content'].encode()),
    'new_user_utf8_bytes_same_published_case_static_reconstruction': len(new_user.encode()),
    'new_user_characters_same_published_case': len(new_user),
    'prior_format_compact_utf8_bytes': len(json.dumps(payload['format'], ensure_ascii=False, separators=(',', ':')).encode()),
    'new_format_compact_utf8_bytes_prior_published_result_not_reexecuted': prior_results['schema_json_utf8_bytes'],
    'prior_runtime_prompt_eval_count': raw.get('prompt_eval_count'),
    'prior_runtime_eval_count': raw.get('eval_count'),
    'prior_options': payload['options'],
    'prior_think': payload['think'],
    'actual_new_token_count': None,
    'deployed_decoder_compatibility': None,
    'blocking_static_branch_trace': {
        'new_handoff': 'numeric with differing literal requires different',
        'effective_expected_comparison': 'comparable quantifier slots with equal value numeric return same before quantifier helper',
        'helper_differing_literal_branch_reached': False,
        'effect': 'new handoff-compliant different rejected by unchanged semantic precheck',
        'proof_kind': 'static control-flow reading; not an executed fixture'
    },
    'decision': 'B',
    'tests_executed': 0,
    'application_imports': 0,
    'vps_accesses': 0,
    'model_calls': 0
}
print(json.dumps(facts, ensure_ascii=False, indent=2))
