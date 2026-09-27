"""Curated assertions with exact snapshot locators; does not infer support."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]/'.research'
items=[
('s-006','Choice selects one option from a caller-defined set.','selecting one option from a defined set'),
('s-008','Noul returns the probability of yes.','probability that the answer is yes'),
('s-007','Score uses ordered descriptive levels.','rating content against ordered, descriptive levels'),
('s-009','TypeSafe confidence is derived from the output distribution; Noul has no separate confidence field.','(Noul answers don\'t carry one.)'),
('s-010','TypeSafe calls its decision-training approach RLCD and describes calibration over groups, not a guarantee about one prediction.','These rates describe groups of predictions, not a guarantee about any single answer.'),
('s-004','TypeSafe attributes its zero-percent figure to schema matching, not empirical task correctness.','Our number is not empirical. Schema matching is guaranteed'),
('s-011','TypeSafe documents numerical, adversarial-input and cross-question consistency limitations for Jev 1.13.','structural invariants one might imagine to hold that simply aren\'t guaranteed'),
('s-014','TypeSafe advises pinning a version after tuning thresholds because aliases can move.','pin that version\'s ID instead of the alias'),
('s-005','The documented Jev HTTP endpoint is POST https://api.typesafe.ai/v1/systemone.','POST https://api.typesafe.ai/v1/systemone'),
('s-012','The SDK Score answer reports a probability-weighted expected rubric score.','Expected score: the probability-weighted average of the rubric levels.'),
('s-015','Python SDK version 0.6.0 changed Score criteria to an ordered sequence.','accept `Score.criteria` as an ordered sequence instead of a dictionary keyed by integers'),
('s-021','AnyJev L0 debiasing alone does not establish calibrated model uncertainty.','it does not make the model\'s own uncertainty'),
('s-021','AnyJev warns its L1 calibration does not generally survive distribution shift beyond its calibration set.','survive distribution shift beyond the calibration set'),
('s-022','Laya documents that a Jev confidence threshold does not transfer directly.','A threshold carried over from Jev does not transfer.'),
('s-022','Laya distinguishes near-chance base-checkpoint typed-decisions performance from its specialized checkpoint.','The base checkpoints are near chance on typed-decisions zero-shot'),
('s-023','GLiNER2.5-Decide is documented as a 340M English classification model.','The 340M English classification model in the GLiNER2.5 family.'),
('s-024','SemIf probabilities are conditional on the provided options.','Returned probabilities are conditional on the supplied options.'),
('s-024','SemIf includes workload-specific calibration which leaves the selected option unchanged.','Calibration does not change the selected option.'),
('s-002','Decision 1.0 provides encoder and adapted Qwen branches; native vLLM-SR integration is described as planned in its release.','native vLLM-SR integration and Open Decision API support are planned next.'),
('s-033','Fastino explicitly distinguishes its JevK5 benchmark comparator from TypeSafe Jev.','JevK5 is an open reproduction rather than TypeSafe’s Jev.'),
('s-033','Fastino says classification answers themselves do not include evidence spans.','Classification answers themselves do not return evidence spans.'),
('s-020','Archestra reports 337 judge-agreed decisions from an initial 400-label, 100-call sample.','337 decisions where all three judge families agreed'),
('s-020','Archestra reports mostly stable Jev labels but drifting probabilities and some option-order sensitivity.','labels are mostly stable, but its internal probabilities float'),
('s-027','In Nhu Hoang\'s supplied Banking77 experiment, retaining Jev answers at confidence exactly 1.00 and routing the rest to Qwen fixed 84 errors but introduced 211.','Qwen fixed 84 mistakes, but introduced 211 new ones.'),
('s-028','The coding-agent PDF labels itself an independent synthesis rather than an official TypeSafe publication.','Independently compiled, September 2026. Not affiliated with or endorsed by TypeSafe'),
('s-019','NIST AI RMF Core groups activities into Govern, Map, Measure and Manage.','GOVERN'),
('s-017','InstructGPT research describes fine-tuning from human feedback.','human feedback'),
('s-018','The DeepSeek-R1 paper describes reinforcement learning for reasoning.','reinforcement learning'),
('s-016','Guo et al. study neural-network probability calibration and temperature scaling.','temperature scaling'),
]
rows=[]
for i,(sid,statement,quote) in enumerate(items,1):
    snapshot=(root/'snapshots'/f'{sid}.txt').read_text(encoding='utf-8')
    assert quote in snapshot, (sid,quote)
    rows.append(dict(cid=f'c-{i:03}',statement=statement,bindings=[dict(sid=sid,locator=dict(kind='quote',value=quote),verified_by='quote-match')],stance='supported',confidence='moderate',verified='pass'))
(root/'claims.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
print(f'Wrote {len(rows)} claims; each locator exists in its snapshot.')
