from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = 'C:/Users/anuj_/.codex/plugins/cache/research-anything/research-anything/0.1.0/scripts/snapshot.py'

def capture(path, url, title, tier, publisher, notes):
    subprocess.run([sys.executable, SNAPSHOT, '--workspace', str(ROOT/'.research'), '--from-file', str(path), '--url', url, '--title', title, '--tier', tier, '--publisher', publisher, '--notes', notes, '--append'],check=True)

for row in map(json.loads,(ROOT/'.research/alternatives/sources.jsonl').read_text(encoding='utf-8').splitlines()):
    capture(ROOT/'.research/alternatives'/row['snapshot'],row['url'],row['title'],row['tier'],row.get('publisher','Project maintainer'),row.get('notes','')+' Imported from isolated source-hunter capture; original retained.')
for path in (ROOT/'.research/extracted').glob('*.txt'):
    capture(path,'manual:'+path.stem+'.pdf',path.stem,'T4','User-supplied article','OCR except coding-agent PDF; discovery/context only. Consult original pages for numbers and code; primary sources govern technical claims.')
for name in ['jev.txt','other-model.txt','links.txt']:
    capture(ROOT/name,'manual:'+name,name,'T4','User-supplied notes','Research input, not verified evidence. Links and hypotheses require independent checking.')
urls=[]
for name in ['links.txt','jev.txt','other-model.txt']:
    for url in re.findall(r'https?://[^\s<>\]\)"]+',(ROOT/name).read_text(encoding='utf-8')):
        if url not in [x['url'] for x in urls]: urls.append({'url':url,'found_in':name,'scope':'required capture' if name=='links.txt' else 'embedded reference; follow selectively'})
(ROOT/'.research/url-inventory.json').write_text(json.dumps(urls,indent=2),encoding='utf-8')
