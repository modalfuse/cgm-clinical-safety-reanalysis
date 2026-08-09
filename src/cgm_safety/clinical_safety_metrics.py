"""Clinical-safety metrics for binary event scores and alarms."""

from collections.abc import Iterable

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def safe_auc(labels: Iterable[int], scores: Iterable[float]) -> dict[str, float]:
    """Return PR-AUC and ROC-AUC, using NaN when an AUC is undefined."""
    labels_array = np.asarray(labels, dtype=int)
    scores_array = np.asarray(scores, dtype=float)
    if labels_array.shape != scores_array.shape:
        raise ValueError("labels and scores must have the same shape")
    pr_auc = float(average_precision_score(labels_array, scores_array)) if np.any(labels_array == 1) else np.nan
    roc_auc = float(roc_auc_score(labels_array, scores_array)) if np.unique(labels_array).size == 2 else np.nan
    return {"pr_auc": pr_auc, "roc_auc": roc_auc}


def binary_metrics(labels: Iterable[int], alarms: Iterable[int]) -> dict[str, float]:
    labels_array, alarms_array = np.asarray(labels, dtype=bool), np.asarray(alarms, dtype=bool)
    if labels_array.shape != alarms_array.shape:
        raise ValueError("labels and alarms must have the same shape")
    tp = int(np.sum(labels_array & alarms_array))
    fn = int(np.sum(labels_array & ~alarms_array))
    tn = int(np.sum(~labels_array & ~alarms_array))
    fp = int(np.sum(~labels_array & alarms_array))
    positive, negative = tp + fn, tn + fp
    return {
        "tp": tp, "fn": fn, "tn": tn, "fp": fp,
        "sensitivity": tp / positive if positive else np.nan,
        "fnr": fn / positive if positive else np.nan,
        "specificity": tn / negative if negative else np.nan,
        "precision": tp / (tp + fp) if tp + fp else np.nan,
    }


def count_false_alarm_episodes(
    labels: Iterable[int],
    alarms: Iterable[int],
    minutes: Iterable[float],
    *,
    groups: Iterable[object] | None = None,
    merge_gap_minutes: float = 10.0,
) -> int:
    """Count false-alarm runs within groups using the chosen merge gap."""
    labels_array, alarms_array, minute_array = map(np.asarray, (labels, alarms, minutes))
    if not (labels_array.shape == alarms_array.shape == minute_array.shape):
        raise ValueError("all inputs must have the same shape")
    group_array = np.zeros(labels_array.shape, dtype=int) if groups is None else np.asarray(groups)
    if group_array.shape != labels_array.shape:
        raise ValueError("groups must have the same shape as the other inputs")

    false_alarm = (labels_array == 0) & (alarms_array == 1)
    episodes = 0
    for group in np.unique(group_array[false_alarm]):
        false_minutes = np.sort(minute_array[false_alarm & (group_array == group)].astype(float))
        episodes += 1 + int(np.sum(np.diff(false_minutes) > merge_gap_minutes))
    return episodes


def lead_time_summary(lead_minutes: Iterable[float]) -> dict[str, float]:
    values = np.asarray(list(lead_minutes), dtype=float)
    values = values[np.isfinite(values)]
    if values.size == 0:
        return {"n": 0, "mean": np.nan, "median": np.nan, "q1": np.nan, "q3": np.nan}
    return {
        "n": int(values.size), "mean": float(np.mean(values)), "median": float(np.median(values)),
        "q1": float(np.quantile(values, 0.25)), "q3": float(np.quantile(values, 0.75)),
    }
