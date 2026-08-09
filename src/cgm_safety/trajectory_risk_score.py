"""Continuous risk score derived from forecast trajectories."""

import numpy as np


def trajectory_risk_score(predicted_trajectory) -> np.ndarray:
    """Return negative minimum forecast glucose for each trajectory."""
    values = np.asarray(predicted_trajectory, dtype=float)
    if values.ndim == 1:
        values = values.reshape(1, -1)
    if values.ndim != 2 or values.shape[1] == 0:
        raise ValueError("predicted_trajectory must be a non-empty vector or matrix")
    return -np.nanmin(values, axis=1)
