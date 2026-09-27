"""Generate tutorial footnotes from checked ledgers."""
from pathlib import Path
import json
import re
root=Path(__file__).resolve().parents[1]
sources={r['sid']:r for r in map(json.loads,(root/'.research/sources.jsonl').read_text(encoding='utf-8').splitlines())}
claims={r['cid']:r for r in map(json.loads,(root/'.research/claims.jsonl').read_text(encoding='utf-8').splitlines())}
path=root/'tutorial/decision-models.md'
text=path.read_text(encoding='utf-8').split('## References')[0]
text=text.replace('"urgency": Score(criteria=[','"urgency": Score(instructions="Rate urgency from stated facts.", criteria=[')
ids=sorted(set(re.findall(r'\[\^(c-\d+)\]',text)))
refs=[]
for cid in ids:
    claim=claims[cid]
    source=sources[claim['bindings'][0]['sid']]
    url=source['url']
    if url=='manual:jev-3.pdf':
        url='https://towardsdatascience.com/jev-vs-llms-when-ai-moves-from-generation-to-decision-making/'
        title='Nhu Hoang: Jev vs. LLMs (supplied PDF pp. 20-22)'
    elif url.startswith('manual:'):
        url='../'+url.removeprefix('manual:')
        title=source['title']+' (supplied file)'
    else:
        title=source['title']
    refs.append(f"[^{cid}]: {claim['statement']} - [{title}]({url}). Accessed 2026-09-26; {source['tier']}. Evidence: {source['sid']} in the [source ledger](../.research/sources.jsonl).")
path.write_text(text+'## References\n\n'+'\n\n'.join(refs)+'\n',encoding='utf-8')
print(f'Generated {len(refs)} references.')
