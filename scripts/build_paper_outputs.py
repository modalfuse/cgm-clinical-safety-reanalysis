"""Rebuild manuscript Tables 2–6 and aggregate-data figures."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "derived"
OUTPUT = ROOT / "output"

SOURCES = {
    2: "benchmark-ph60-ood-mae.csv",
    3: "clinical-risk-dubosson-ph60-ood.csv",
    4: "event-operating-points.csv",
    5: "matched-specificity.csv",
    6: "external-transfer.csv",
}


def markdown_table(frame: pd.DataFrame, title: str) -> str:
    display = frame.fillna("n/a")
    headers = [str(column) for column in display.columns]
    lines = [f"# {title}", "", "| " + " | ".join(headers) + " |",
             "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in display.itertuples(index=False, name=None):
        values = [str(value) for value in row]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def build_tables() -> None:
    for number, filename in SOURCES.items():
        frame = pd.read_csv(DERIVED / filename)
        text = markdown_table(frame, f"Table {number}")
        (OUTPUT / f"table-{number}.md").write_text(text, encoding="utf-8")


def build_dts_figure() -> None:
    frame = pd.read_csv(DERIVED / SOURCES[3])
    x = range(len(frame))
    width = 0.35
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.bar([i - width / 2 for i in x], frame["zone_a_pct"], width, label="Zone A")
    ax.bar([i + width / 2 for i in x], frame["zone_d_pct"], width, label="Zone D")
    ax.set_xticks(list(x), frame["model"])
    ax.set_ylabel("Endpoint pairs (%)")
    ax.set_title("Dubosson PH60 OOD DTS risk profile")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT / "dts-risk-aggregate.png", dpi=180)
    plt.close(fig)


def build_matched_figure() -> None:
    frame = pd.read_csv(DERIVED / SOURCES[5])
    frame = frame[frame["threshold_policy"].str.contains("0.90")]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.bar(frame["method"], frame["fnr_pct"], color=["#648FFF", "#DC267F", "#FFB000"])
    ax.set_ylabel("FNR (%)")
    ax.set_title("Matched specificity near 0.90")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(OUTPUT / "matched-specificity-comparison.png", dpi=180)
    plt.close(fig)


def build_external_figure() -> None:
    frame = pd.read_csv(DERIVED / SOURCES[6])
    frame = frame[(frame["model"] == "XGBoost") & (frame["threshold_policy"] == "source default 0.5")]
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    axes[0].bar(frame["target"], frame["pr_auc"], color="#785EF0")
    axes[0].set_ylim(0, 1)
    axes[0].set_title("PR-AUC")
    axes[1].bar(frame["target"], frame["fnr_pct"], color="#FE6100")
    axes[1].set_title("FNR (%)")
    fig.suptitle("External transfer: fixed source threshold")
    fig.tight_layout()
    fig.savefig(OUTPUT / "external-transfer.png", dpi=180)
    plt.close(fig)


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    build_tables()
    build_dts_figure()
    build_matched_figure()
    build_external_figure()


if __name__ == "__main__":
    main()
