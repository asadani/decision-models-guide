"""Meaningful boundary and arithmetic checks for the teaching lab."""
import math
import unittest
from decision_workflow import Prediction, policy, metrics

class WorkflowTests(unittest.TestCase):
    def test_high_probability_does_not_authorize_refund(self):
        p=Prediction({'billing':1.,'technical':0.,'other':0.},'test')
        self.assertEqual(policy(p,evidence_present=True,action='refund')['status'],'review')

    def test_missing_evidence_overrides_high_probability(self):
        p=Prediction({'billing':1.,'technical':0.,'other':0.},'test')
        self.assertEqual(policy(p,evidence_present=False)['reason'],'missing_evidence')

    def test_invalid_distributions_fail_closed(self):
        for probs in [{'billing':float('nan'),'technical':0.,'other':0.},
                      {'billing':.9,'technical':.9,'other':0.},
                      {'billing':1.}, {'billing':True,'technical':0.,'other':0.}]:
            with self.subTest(probs=probs):
                self.assertEqual(policy(Prediction(probs,'test'),evidence_present=True)['reason'],'invalid_prediction')

    def test_tie_does_not_auto_route(self):
        p=Prediction({'billing':.5,'technical':.5,'other':0.},'test')
        self.assertEqual(policy(p,evidence_present=True,threshold=.4)['reason'],'tie')

    def test_metrics_against_hand_calculation(self):
        rows=[{'label':'billing','p':{'billing':.8,'technical':.1,'other':.1}},
              {'label':'technical','p':{'billing':.8,'technical':.1,'other':.1}}]
        m=metrics(rows)
        self.assertAlmostEqual(m['accuracy'],.5)
        self.assertAlmostEqual(m['multiclass_brier'],.76)
        self.assertAlmostEqual(m['negative_log_likelihood'],-(math.log(.8)+math.log(.1))/2)
        self.assertAlmostEqual(m['top_label_ece'],.3)
        self.assertAlmostEqual(m['policy_coverage'],1.)

    def test_zero_coverage_has_no_accuracy_estimate(self):
        rows=[{'label':'billing','p':{'billing':.5,'technical':.4,'other':.1}}]
        self.assertIsNone(metrics(rows,threshold=.99)['policy_selective_accuracy'])

if __name__ == '__main__':
    unittest.main()
