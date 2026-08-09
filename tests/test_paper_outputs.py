from pathlib import Path
import subprocess
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "derived"


def row(frame, **criteria):
    selected = frame
    for column, value in criteria.items():
        selected = selected[selected[column] == value]
    assert len(selected) == 1
    return selected.iloc[0]


def test_v54_key_numbers():
    table2 = pd.read_csv(DERIVED / "benchmark-ph60-ood-mae.csv")
    assert row(table2, model="Linear regression").dubosson_mae == 15.85
    assert row(table2, model="N-HiTS").dubosson_mae == 18.72

    table3 = pd.read_csv(DERIVED / "clinical-risk-dubosson-ph60-ood.csv")
    linear, nhits = row(table3, model="Linear regression"), row(table3, model="N-HiTS")
    assert (linear.trajectory_mae, nhits.trajectory_mae) == (15.40, 18.65)
    assert (linear.zone_a_pct, nhits.zone_a_pct) == (67.3, 56.0)
    assert (linear.zone_d_pct, nhits.zone_d_pct) == (0.7, 1.3)

    table4 = pd.read_csv(DERIVED / "event-operating-points.csv")
    logistic = row(table4, ph=60, model="Logistic event classifier", operating_point="default_0.5")
    xgboost = row(table4, ph=60, model="XGBoost event classifier", operating_point="default_0.5")
    trajectory = row(table4, ph=60, model="Linear trajectory")
    assert (logistic.fnr_pct, xgboost.fnr_pct, trajectory.fnr_pct) == (9.0, 8.6, 38.4)

    table5 = pd.read_csv(DERIVED / "matched-specificity.csv")
    assert sorted(table5.pr_auc.unique().tolist()) == [0.85, 0.87, 0.90]
    near90 = table5[table5.threshold_policy.str.contains("0.90")]
    assert near90.fnr_pct.tolist() == [10.2, 9.6, 9.1]

    table6 = pd.read_csv(DERIVED / "external-transfer.csv")
    t1 = row(table6, target="ShanghaiT1DM", model="XGBoost", threshold_policy="source default 0.5")
    t2 = row(table6, target="ShanghaiT2DM", model="XGBoost", threshold_policy="source default 0.5")
    assert (t1.pr_auc, t1.fnr_pct, t2.pr_auc, t2.fnr_pct) == (0.90, 4.0, 0.79, 5.9)


def test_build_script_creates_tables_and_figures():
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_paper_outputs.py")], check=True, cwd=ROOT)
    expected = [*(ROOT / "output" / f"table-{n}.md" for n in range(2, 7)),
                ROOT / "output" / "dts-risk-aggregate.png",
                ROOT / "output" / "matched-specificity-comparison.png",
                ROOT / "output" / "external-transfer.png"]
    assert all(path.exists() and path.stat().st_size > 0 for path in expected)
