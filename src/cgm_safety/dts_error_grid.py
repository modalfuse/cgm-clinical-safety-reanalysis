"""DTS point-accuracy Error Grid geometry.

Coordinates follow Supplemental Appendix 2, Table A1, of Klonoff et al.
(2024), DOI 10.1177/19322968241275701. The x-axis is reference glucose and
the y-axis is monitor or forecast glucose, both in mg/dL.
"""

from math import sqrt
from typing import Iterable

import numpy as np

ZONES = ("A", "B", "C", "D", "E")
LOWER = {"B": (62.5, 480.0), "C": (97.5, 307.0), "D": (153.0, 197.0), "E": (238.0, 126.0)}
UPPER = {"B": (60.0, 500.0), "C": (86.5, 347.0), "D": (124.0, 241.0), "E": (179.0, 167.0)}


def _line(x, x1, y1, x2, y2):
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)


def lower_boundary(reference: Iterable[float], boundary: str) -> np.ndarray:
    x = np.asarray(reference, dtype=float)
    x0, y600 = LOWER[boundary]
    return np.where(x <= x0, 0.0, _line(x, x0, 50.0, 600.0, y600))


def upper_boundary(reference: Iterable[float], boundary: str) -> np.ndarray:
    x = np.asarray(reference, dtype=float)
    y0, x600 = UPPER[boundary]
    sloped = _line(x, 50.0, y0, x600, 600.0)
    return np.where(x <= 50.0, y0, np.where(x >= x600, 600.0, sloped))


def dts_zones(reference: Iterable[float], monitor: Iterable[float], *, invalid: str = "raise") -> np.ndarray:
    ref, mon = np.asarray(reference, dtype=float), np.asarray(monitor, dtype=float)
    if ref.shape != mon.shape:
        raise ValueError("reference and monitor must have the same shape")
    if invalid not in {"raise", "mask"}:
        raise ValueError("invalid must be 'raise' or 'mask'")
    valid = np.isfinite(ref) & np.isfinite(mon) & (ref >= 0) & (ref <= 600) & (mon >= 0) & (mon <= 600)
    if invalid == "raise" and not np.all(valid):
        raise ValueError("glucose pair is non-finite or outside 0-600 mg/dL")
    zones = np.full(ref.shape, "", dtype="<U1")
    x, y = ref[valid], mon[valid]
    current = np.full(x.shape, "E", dtype="<U1")
    double_low = (x <= 50) & (y <= 50)
    current[double_low] = "A"
    for is_upper in (True, False):
        choose = ((y >= x) if is_upper else (y < x)) & ~double_low
        xx, yy = x[choose], y[choose]
        part = np.full(xx.shape, "E", dtype="<U1")
        boundaries = UPPER if is_upper else LOWER
        values = {
            name: (upper_boundary(xx, name) if is_upper else lower_boundary(xx, name))
            for name in boundaries
        }
        tests = [(yy <= values[z]) if is_upper else (yy >= values[z]) for z in ("E", "D", "C", "B")]
        for test, assigned in zip(tests, ("D", "C", "B", "A")):
            part[test] = assigned
        current[choose] = part
    zones[valid] = current
    return zones


def wilson_interval(count: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n <= 0:
        return np.nan, np.nan
    p = count / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z / denom * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return center - half, center + half


def dts_zone_summary(reference: Iterable[float], monitor: Iterable[float]) -> dict[str, float]:
    zones = dts_zones(reference, monitor, invalid="mask")
    n = int(np.sum(zones != ""))
    result: dict[str, float] = {"n_points": n, "n_invalid": int(np.sum(zones == ""))}
    for zone in ZONES:
        count = int(np.sum(zones == zone))
        low, high = wilson_interval(count, n)
        result.update({f"n_{zone}": count, f"pct_{zone}": 100 * count / n if n else np.nan,
                       f"pct_{zone}_ci_low": 100 * low, f"pct_{zone}_ci_high": 100 * high})
    return result
