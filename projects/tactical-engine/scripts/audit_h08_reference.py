#!/usr/bin/env python3
import json
import sys
report=json.load(open(sys.argv[1],encoding='utf-8'))
reference=json.load(open(sys.argv[2],encoding='utf-8'))
for item in reference['figures']:
    found=[f for f in report['figures'] if item['id'] in f['figure_ids_from_caption']]
    print(item['id'], 'page_ok=',len(found)==1 and found[0]['page']==item['pdf_page'], 'links=',sum(len(f['paragraph_candidates']) for f in found))
