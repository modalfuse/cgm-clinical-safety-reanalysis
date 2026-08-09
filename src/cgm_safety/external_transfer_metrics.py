"""Evaluation of unchanged source-selected thresholds on target scores."""

from .clinical_safety_metrics import binary_metrics, safe_auc


def evaluate_fixed_threshold(labels, scores, threshold: float) -> dict[str, float]:
    """Evaluate discrimination and an externally fixed operating threshold."""
    alarms = [float(score) >= threshold for score in scores]
    return {"threshold": float(threshold), **binary_metrics(labels, alarms), **safe_auc(labels, scores)}
