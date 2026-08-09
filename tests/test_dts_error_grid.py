import numpy as np
import pytest

from cgm_safety.dts_error_grid import dts_zone_summary, dts_zones, lower_boundary, upper_boundary


def test_table_a1_boundaries():
    assert np.allclose(lower_boundary([62.5, 600], "B"), [0, 480])
    assert np.allclose(lower_boundary([97.5, 600], "C"), [0, 307])
    assert np.allclose(lower_boundary([153, 600], "D"), [0, 197])
    assert np.allclose(lower_boundary([238, 600], "E"), [0, 126])
    assert np.allclose(upper_boundary([0, 50, 500], "B"), [60, 60, 600])
    assert np.allclose(upper_boundary([0, 50, 347], "C"), [86.5, 86.5, 600])
    assert np.allclose(upper_boundary([0, 50, 241], "D"), [124, 124, 600])
    assert np.allclose(upper_boundary([0, 50, 167], "E"), [179, 179, 600])


def test_double_low_and_representative_zones():
    assert dts_zones([0, 25, 50], [50, 10, 0]).tolist() == ["A", "A", "A"]
    assert dts_zones([100] * 5, [110, 130, 220, 300, 400]).tolist() == list("ABCDE")
    assert dts_zones([100, 100, 200, 200, 300], [90, 70, 80, 50, 1]).tolist() == list("ABCDE")


def test_invalid_values_raise_or_are_audited():
    with pytest.raises(ValueError, match="outside 0-600"):
        dts_zones([-1, 100], [10, 100])
    summary = dts_zone_summary([-1, 100], [10, 100])
    assert summary["n_points"] == 1
    assert summary["n_invalid"] == 1
    assert summary["n_A"] == 1
