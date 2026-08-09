import math

import numpy as np

from cgm_safety.clinical_safety_metrics import (
    binary_metrics,
    count_false_alarm_episodes,
    lead_time_summary,
    safe_auc,
)
from cgm_safety.external_transfer_metrics import evaluate_fixed_threshold
from cgm_safety.matched_specificity import select_matched_specificity
from cgm_safety.trajectory_risk_score import trajectory_risk_score


def test_binary_auc_and_undefined_auc_are_safe():
    metrics = binary_metrics([1, 1, 0, 0], [1, 0, 0, 1])
    assert metrics["sensitivity"] == metrics["specificity"] == 0.5
    auc = safe_auc([0, 1, 0, 1], [0.1, 0.9, 0.2, 0.8])
    assert auc["pr_auc"] == auc["roc_auc"] == 1.0
    undefined = safe_auc([0, 0], [0.1, 0.2])
    assert math.isnan(undefined["pr_auc"]) and math.isnan(undefined["roc_auc"])


def test_false_alarm_merging_and_lead_time():
    assert count_false_alarm_episodes([0] * 4, [1] * 4, [0, 5, 15, 31], merge_gap_minutes=10) == 2
    assert count_false_alarm_episodes(
        [0] * 4,
        [1] * 4,
        [0, 5, 0, 5],
        groups=["day-1", "day-1", "day-2", "day-2"],
        merge_gap_minutes=10,
    ) == 2
    summary = lead_time_summary([5, 10, 15, np.nan])
    assert summary["n"] == 3 and summary["median"] == 10


def test_risk_matched_specificity_and_fixed_threshold():
    assert trajectory_risk_score([[100, 80, 65], [120, 110, 90]]).tolist() == [-65, -90]
    labels = [0, 0, 0, 1, 1]
    scores = [0.1, 0.2, 0.3, 0.8, 0.9]
    matched = select_matched_specificity(labels, scores, 1.0)
    assert matched["specificity"] == 1.0 and matched["fnr"] == 0.0
    fixed = evaluate_fixed_threshold(labels, scores, 0.5)
    assert fixed["threshold"] == 0.5 and fixed["fnr"] == 0.0
