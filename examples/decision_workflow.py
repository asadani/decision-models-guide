"""Offline teaching lab. Synthetic predictions, not a trained model or benchmark.

Run: python examples/decision_workflow.py
"""
from dataclasses import dataclass, asdict
import hashlib
import json
import math

LABELS = ('billing', 'technical', 'other')
POLICY_VERSION = 'triage-demo-1'

@dataclass(frozen=True)
class Prediction:
    probabilities: dict[str, float]
    model: str

    def validate(self):
        if set(self.probabilities) != set(LABELS):
            raise ValueError('Missing or unexpected labels')
        values = list(self.probabilities.values())
        if any(isinstance(v, bool) or not isinstance(v, (int, float))
               or not math.isfinite(v) or not 0 <= v <= 1 for v in values):
            raise ValueError('Invalid probability')
        if not math.isclose(sum(values), 1.0, abs_tol=1e-6):
            raise ValueError('Probabilities must sum to one')

    def winner(self):
        self.validate()
        return max(LABELS, key=self.probabilities.__getitem__)


def policy(prediction, *, evidence_present, action='route', threshold=0.8):
    """Threshold is illustrative. Policy returns a proposal, executes nothing."""
    if not 0 <= threshold <= 1:
        raise ValueError('Invalid threshold')
    try:
        prediction.validate()
    except ValueError:
        return {'status': 'review', 'reason': 'invalid_prediction'}
    if not evidence_present:
        return {'status': 'review', 'reason': 'missing_evidence'}
    if action != 'route':
        return {'status': 'review', 'reason': 'action_outside_auto_policy'}
    label = prediction.winner()
    probs = sorted(prediction.probabilities.values(), reverse=True)
    if probs[0] == probs[1]:
        return {'status': 'review', 'reason': 'tie'}
    if label == 'other' or probs[0] < threshold:
        return {'status': 'review', 'reason': 'uncertain_or_other'}
    return {'status': 'route', 'destination': label, 'reason': 'within_demo_policy'}


def metrics(rows, threshold=0.8, bins=5):
    """Multiclass Brier (sum over K, mean over N); top-label ECE.

    Expects labeled rows with complete probability distributions. No training or
    threshold fitting happens here. ECE is descriptive and depends on binning.
    """
    if not rows or bins < 1 or not 0 <= threshold <= 1:
        raise ValueError('Need labeled rows, positive bins and valid threshold')
    correct, brier, nll = 0, 0.0, 0.0
    accepted = []
    buckets = [[] for _ in range(bins)]
    recalls = []
    for row in rows:
        pred = Prediction(row['p'], 'synthetic-v1')
        winner = pred.winner()
        y = row['label']
        if y not in LABELS:
            raise ValueError('Unknown reference label')
        hit = int(winner == y)
        peak = pred.probabilities[winner]
        correct += hit
        brier += sum((pred.probabilities[k] - int(k == y)) ** 2 for k in LABELS)
        # Clip only inside log for numerical stability; disclose the floor.
        nll -= math.log(max(pred.probabilities[y], 1e-15))
        buckets[min(int(peak * bins), bins - 1)].append((peak, hit))
        result = policy(pred, evidence_present=True, threshold=threshold)
        if result['status'] == 'route':
            accepted.append(hit)
    for label in LABELS:
        subset = [r for r in rows if r['label'] == label]
        if subset:
            recalls.append(sum(Prediction(r['p'], 'synthetic-v1').winner() == label for r in subset) / len(subset))
    reliability = [{'n': len(b), 'mean_top_probability': sum(p for p, _ in b)/len(b),
                    'accuracy': sum(hit for _, hit in b)/len(b)} for b in buckets if b]
    n = len(rows)
    return {
        'n': n, 'accuracy': correct/n,
        'majority_baseline': max(sum(r['label'] == k for r in rows) for k in LABELS)/n,
        'macro_recall_present_classes': sum(recalls)/len(recalls),
        'multiclass_brier': brier/n, 'negative_log_likelihood': nll/n,
        'top_label_ece': sum(b['n']/n * abs(b['mean_top_probability']-b['accuracy']) for b in reliability),
        'policy_coverage': len(accepted)/n,
        'policy_selective_accuracy': sum(accepted)/len(accepted) if accepted else None,
        'reliability_bins': reliability,
    }


def receipt(state, prediction, result, threshold):
    """Minimal teaching receipt. Hash is a fingerprint, NOT an immutable audit log."""
    encoded = json.dumps(state, sort_keys=True, separators=(',', ':')).encode()
    return {'schema_version': 'triage-1', 'policy_version': POLICY_VERSION,
            'state_sha256': hashlib.sha256(encoded).hexdigest(),
            'prediction': asdict(prediction), 'threshold_signal': 'max_probability',
            'threshold': threshold, 'policy_result': result,
            'execution': 'not_executed', 'outcome': None}


SYNTHETIC = [
    {'label':'billing', 'p':{'billing':.9,'technical':.05,'other':.05}},
    {'label':'technical','p':{'billing':.05,'technical':.9,'other':.05}},
    {'label':'technical','p':{'billing':.85,'technical':.1,'other':.05}},
    {'label':'billing','p':{'billing':.5,'technical':.4,'other':.1}},
    {'label':'other','p':{'billing':.1,'technical':.1,'other':.8}},
    {'label':'technical','p':{'billing':.2,'technical':.6,'other':.2}},
]

if __name__ == '__main__':
    state = {'ticket_id':'synthetic-001','message':'I was charged twice.'}
    prediction = Prediction(SYNTHETIC[0]['p'], 'synthetic-v1')
    threshold = .8
    result = policy(prediction, evidence_present=True, threshold=threshold)
    print(json.dumps({'notice':'Synthetic arithmetic demo; no model benchmark',
                      'metrics':metrics(SYNTHETIC,threshold),
                      'receipt':receipt(state,prediction,result,threshold)}, indent=2))
