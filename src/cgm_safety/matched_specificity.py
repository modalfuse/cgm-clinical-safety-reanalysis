"""Operating-point selection at a requested specificity."""

import numpy as np

from .clinical_safety_metrics import binary_metrics


def select_matched_specificity(labels, scores, target_specificity: float) -> dict[str, float]:
    """Select the threshold minimizing absolute specificity mismatch.

    Ties favor lower FNR and then the higher threshold.
    """
    labels_array, scores_array = np.asarray(labels, dtype=int), np.asarray(scores, dtype=float)
    if labels_array.shape != scores_array.shape:
        raise ValueError("labels and scores must have the same shape")
    if not 0 <= target_specificity <= 1:
        raise ValueError("target_specificity must be between zero and one")
    thresholds = np.r_[np.inf, np.unique(scores_array)[::-1], -np.inf]
    candidates = []
    for threshold in thresholds:
        metrics = binary_metrics(labels_array, scores_array >= threshold)
        candidates.append((abs(metrics["specificity"] - target_specificity), metrics["fnr"], -threshold, threshold, metrics))
    _, _, _, threshold, metrics = min(candidates, key=lambda item: item[:3])
    return {"threshold": float(threshold), "target_specificity": target_specificity, **metrics}
