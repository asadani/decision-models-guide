"""Capture public sources with research-anything; retain fetch failures explicitly."""
from pathlib import Path
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
import requests

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path('C:/Users/anuj_/.codex/plugins/cache/research-anything/research-anything/0.1.0/scripts')
sys.path.insert(0, str(PLUGIN))
from snapshot import html_to_text

SOURCES = [
('https://www.langchain.com/blog/building-prod-with-jev-and-langgraph','Building Production Agents with Jev and LangGraph','T2','LangChain'),
('https://vllm-sr.ai/blog/decision-models/','Introducing Decision 1.0','T4','vLLM Semantic Router'),
('https://archestra.ai/blog/we-tested-jev-on-100-real-agent-calls','We Tested Jev on 100 Real Agent Calls','T3','Archestra'),
('https://github.com/nokia-applied-research/AnyJev','AnyJev README','T1','Nokia Applied Research'),
('https://typesafe.ai/blog/introducing-system-one-models-and-jev','Introducing System One Models and Jev','T4','TypeSafe AI'),
]
for slug in ['introduction/quickstart','primitives/choice','primitives/score','primitives/noul','confidence','introduction/machine-learning-primer','model-jaggedness/jev-1.13','sdk/python/api/types/responses','sdk/python/api/clients/sync','models','sdk/python/changelog']:
    SOURCES.append((f'https://docs.typesafe.ai/{slug}.md',f'TypeSafe documentation: {slug}','T2','TypeSafe AI'))
SOURCES += [
('https://proceedings.mlr.press/v70/guo17a.html','On Calibration of Modern Neural Networks','T1','PMLR'),
('https://arxiv.org/abs/2203.02155','Training language models to follow instructions with human feedback','T1','Ouyang et al.'),
('https://arxiv.org/abs/2501.12948','DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning','T1','DeepSeek-AI'),
('https://airc.nist.gov/airmf-resources/airmf/5-sec-core/','AI RMF Core','T1','NIST'),
]

def fetch(item):
    url,title,tier,publisher=item
    try:
        r=requests.get(url, timeout=40)
        r.raise_for_status()
        return item, html_to_text(r.text) if 'html' in r.headers.get('content-type','') else r.text, None
    except Exception as exc:
        return item, None, str(exc)

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raw=ROOT/'.research'/'web'; raw.mkdir(exist_ok=True)
    failures=[]
    for i,(item,content,error) in enumerate(ThreadPoolExecutor(max_workers=6).map(fetch,SOURCES),1):
        url,title,tier,publisher=item
        if error:
            failures.append(f'{url}: {error}'); continue
        path=raw/f'{i:03}.txt'; path.write_text(content,encoding='utf-8')
        cmd=[sys.executable,str(PLUGIN/'snapshot.py'),'--workspace',str(ROOT/'.research'),'--url',url,'--title',title,'--tier',tier,'--publisher',publisher,'--stdin','--notes','First-party source except Archestra practitioner experiment; vendor measurements are attributed, not independently reproduced. Captured 2026-09-26.','--append']
        result=subprocess.run(cmd,input=content,text=True,encoding='utf-8',capture_output=True)
        print(title,result.returncode,result.stdout[-250:],result.stderr[-250:])
    (ROOT/'.research'/'fetch-failures.txt').write_text('\n'.join(failures),encoding='utf-8')
