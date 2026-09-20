"""Plot verified strict-interior mixed probabilities from the saved cost sweep."""

import csv
import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".venv" / "matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SOURCE = ROOT / "outputs" / "cost_sweep.csv"
PDF = ROOT / "figures" / "cost_sweep_mixed_probability.pdf"
PNG = ROOT / "figures" / "cost_sweep_mixed_probability.png"


def read_verified_interior_points():
    with SOURCE.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("Cost sweep is empty")
    values = {float(row["V"]) for row in rows}
    if len(values) != 1:
        raise ValueError("Figure requires one fixed information value V")
    value = values.pop()
    points = []
    boundaries = []
    for row in rows:
        cost = float(row["c"])
        relation = row["relation_to_V"]
        if relation == "interior":
            if not 0 < cost < value:
                raise ValueError(f"Mislabeled interior cost: {cost}")
            if row["interior_analytical_mixed_applies"] != "True" or row["analytical_and_nashpy_mixed_agree"] != "True":
                raise ValueError(f"Interior mixed result is not cross-checked at c={cost}")
            probability = float(row["nashpy_mixed_p_research_agent_a"])
            other = float(row["nashpy_mixed_p_research_agent_b"])
            analytical = float(row["analytical_p_research"])
            candidates = [item for item in json.loads(row["nashpy_equilibria"]) if item["classification"] == "mixed"]
            if len(candidates) != 1 or not all(
                math.isclose(actual, probability, abs_tol=1e-9)
                for actual in (other, analytical, candidates[0]["agent_a"][0], candidates[0]["agent_b"][0])
            ):
                raise ValueError(f"Mixed probabilities disagree in saved output at c={cost}")
            points.append((cost, probability))
        elif relation in ("zero-cost boundary", "equal-value boundary"):
            if row["interior_analytical_mixed_applies"] != "False" or row["analytical_p_research"]:
                raise ValueError(f"Boundary mislabeled as interior at c={cost}")
            boundaries.append((cost, relation))
    if not points or len(boundaries) != 2:
        raise ValueError("Expected interior data and both boundary cases")
    return value, sorted(points), sorted(boundaries), sorted(float(row["c"]) for row in rows)


def main():
    value, points, boundaries, all_costs = read_verified_interior_points()
    costs, probabilities = zip(*points)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f8fafc")
    ax.plot(costs, probabilities, color="#126782", linewidth=2.3, marker="o", markersize=7,
            label="Verified strict-interior mixed equilibrium")
    for cost, relation in boundaries:
        ax.axvline(cost, color="#718096", linestyle="--", linewidth=1.15, alpha=0.85)
        label = "zero-cost boundary" if relation == "zero-cost boundary" else "c = V boundary"
        ax.annotate(label, (cost, 0.96), xytext=(5, 0), textcoords="offset points",
                    fontsize=8, color="#44546a", va="top", rotation=90)
    for cost, probability in points:
        ax.annotate(f"{probability:.2f}", (cost, probability), xytext=(0, 9),
                    textcoords="offset points", ha="center", fontsize=9, color="#083f52")
    ax.set_xlim(min(all_costs) - 0.2, max(all_costs) + 0.2)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(all_costs)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("Research cost c")
    ax.set_ylabel("Mixed-equilibrium probability of Research")
    ax.set_title("Research Probability Falls as Private Research Cost Rises\n"
                 f"Formal equilibrium calculation, V = {value:g}", fontsize=11, pad=12)
    ax.grid(axis="y", color="#d9e2e8", linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower right", fontsize=8, frameon=False)
    fig.text(0.12, 0.015, "Only 0 < c < V has the ordinary interior mixed probability; boundaries are degenerate.",
             fontsize=8, color="#44546a")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    PDF.parent.mkdir(exist_ok=True)
    fig.savefig(PDF, format="pdf", metadata={"Title": "Cost sweep mixed probability"})
    fig.savefig(PNG, format="png", dpi=220)
    plt.close(fig)
    for output in (PDF, PNG):
        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError(f"Figure output missing or empty: {output}")
    print(f"Data source: {SOURCE.relative_to(ROOT)}")
    print(f"Verified interior points: {points}")
    print(f"Wrote {PDF.relative_to(ROOT)} and {PNG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
