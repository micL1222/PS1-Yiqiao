"""Check objective consistency of the local PS1 v2 artifacts; not research quality."""

import csv
import json
import math
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def baseline():
    return json.loads((ROOT / "outputs/baseline_equilibria.json").read_text())["baseline"]


def sweep():
    with (ROOT / "outputs/cost_sweep.csv").open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def by_cost():
    return {int(row["c"]): row for row in sweep()}


def check_core_files():
    required = [
        "README.md", "PROJECT_CONTEXT.md", "AI_USE_LOG.md", "requirements.txt",
        "src/information_acquisition_game.py", "src/run_baseline_analysis.py",
        "tests/test_information_acquisition_game.py", "notebooks/information_acquisition_baseline.ipynb",
        "outputs/verification_summary.md", "scripts/generate_cost_sweep_figure.py",
        "scripts/validate_project.py", "scripts/verify_all.sh",
        "figures/cost_sweep_figure_notes.md", "figures/ps1_teaser_caption.md",
        "figures/ps1_teaser_description.md",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    require(not missing, f"Missing core files: {missing}")


def check_baseline_json():
    require((ROOT / "outputs/baseline_equilibria.json").is_file(), "Baseline JSON missing")
    require(bool(baseline()), "Baseline JSON empty")


def check_parameters():
    require(baseline()["parameters"] == {"V": 4, "c": 2}, "Baseline parameters changed")
    require(baseline()["action_order"] == ["Research", "Skip"], "Action order changed")


def check_matrices():
    data = baseline()
    require(data["agent_a_payoffs"] == [[2, 2], [4, 0]], "Agent A matrix changed")
    require(data["agent_b_payoffs"] == [[2, 4], [2, 0]], "Agent B matrix changed")


def check_pure():
    expected = {("Research", "Skip"), ("Skip", "Research")}
    data = baseline()
    direct = {tuple(x) for x in data["independent_pure_equilibria"]}
    from_nashpy = {
        tuple(x["pure_profile"]) for x in data["nashpy_support_enumeration"]
        if x["classification"] == "pure"
    }
    require(direct == from_nashpy == expected, "Baseline pure equilibria disagree")


def check_mixed():
    mixed = [x for x in baseline()["nashpy_support_enumeration"] if x["classification"] == "mixed"]
    require(len(mixed) == 1, "Expected one baseline mixed result")
    for player in ("agent_a", "agent_b"):
        require(len(mixed[0][player]) == 2, f"{player} probability vector length changed")
        require(all(math.isclose(x, 0.5, abs_tol=1e-9) for x in mixed[0][player]), f"{player} mixed result changed")
    require(math.isclose(baseline()["analytical_p_research"], 0.5, abs_tol=1e-9), "Analytical baseline result changed")
    require(baseline()["analytical_and_nashpy_mixed_agree"] is True, "Mixed cross-check not marked true")


def check_costs():
    rows = sweep()
    require(len(rows) == 6, "Cost sweep must contain six rows")
    require([int(row["c"]) for row in rows] == list(range(6)), "Cost sweep must be ordered c=0..5")
    require(all(float(row["V"]) == 4 for row in rows), "Cost sweep V changed")
    require(all(row["pure_methods_agree"] == "True" for row in rows), "Pure methods disagree in sweep")


def check_interior():
    rows = by_cost()
    for cost, expected in ((1, 0.75), (2, 0.50), (3, 0.25)):
        row = rows[cost]
        require(row["relation_to_V"] == "interior", f"c={cost} relation changed")
        require(row["interior_analytical_mixed_applies"] == "True", f"c={cost} formula not marked applicable")
        require(row["analytical_and_nashpy_mixed_agree"] == "True", f"c={cost} cross-check failed")
        for field in ("analytical_p_research", "nashpy_mixed_p_research_agent_a", "nashpy_mixed_p_research_agent_b"):
            require(math.isclose(float(row[field]), expected, abs_tol=1e-9), f"c={cost} {field} changed")


def check_boundaries():
    rows = by_cost()
    for cost in (0, 4):
        row = rows[cost]
        require("boundary" in row["relation_to_V"], f"c={cost} boundary label missing")
        require(row["interior_analytical_mixed_applies"] == "False", f"c={cost} marked interior")
        for field in ("analytical_p_research", "nashpy_mixed_p_research_agent_a", "nashpy_mixed_p_research_agent_b"):
            require(row[field] == "", f"c={cost} has ordinary interior probability")


def check_high_cost():
    row = by_cost()[5]
    require(row["relation_to_V"] == "high-cost", "c=5 relation changed")
    require(row["number_of_pure_equilibria"] == "1", "c=5 pure count changed")
    nashpy = json.loads(row["nashpy_equilibria"])
    pure = {tuple(x["pure_profile"]) for x in nashpy if x["classification"] == "pure"}
    require(pure == {("Skip", "Skip")}, "c=5 high-cost pure equilibrium changed")


def check_notebook():
    path = ROOT / "notebooks/information_acquisition_baseline.ipynb"
    require(path.is_file(), "Notebook missing")
    notebook = json.loads(path.read_text())
    code = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    require(bool(code), "Notebook has no code cells")
    require(all(cell.get("execution_count") is not None for cell in code), "Notebook outputs are not saved")
    require(not any(o["output_type"] == "error" for cell in code for o in cell.get("outputs", [])), "Notebook contains cell errors")


def check_figure_pdf():
    path = ROOT / "figures/cost_sweep_mixed_probability.pdf"
    require(path.is_file() and path.stat().st_size > 1000, "Computational figure PDF missing/empty")
    content = path.read_bytes()
    require(content.startswith(b"%PDF-"), "Computational figure is not a PDF")
    require(b"/Subtype /Image" not in content, "Computational figure contains a raster image object")


def check_drawio():
    path = ROOT / "figures/ps1_teaser.drawio"
    require(path.is_file(), "Draw.io master missing")
    document = ET.parse(path).getroot()
    require(document.tag == "mxfile", "Draw.io root must be mxfile")
    cells = document.findall(".//mxCell")
    vertices = [cell for cell in cells if cell.get("vertex") == "1"]
    edges = [cell for cell in cells if cell.get("edge") == "1"]
    require(len(vertices) > 1 and bool(edges), "Draw.io shapes/connectors missing")
    require(not any("image=" in cell.get("style", "") for cell in vertices), "Raster image object found")
    labels = " ".join(cell.get("value", "") for cell in vertices)
    for token in ("AGENT A", "AGENT B", "Research / Skip", "SHARED INFORMATION", "COLLECTIVE DECISION", "ECONOMICS", "COMPUTATION", "BEHAVIOR", "VERIFIED COMPUTATIONALLY", "NOT YET TESTED"):
        require(token in labels, f"Draw.io label missing: {token}")
    require(any("dashed=1" in edge.get("style", "") for edge in edges), "Planned dashed connector missing")
    require(any("dashed=1" not in edge.get("style", "") for edge in edges), "Modeled solid connector missing")


def check_optional_teaser_pdf():
    path = ROOT / "figures/ps1_teaser.pdf"
    if path.exists():
        require(path.is_file() and path.stat().st_size > 1000, "Teaser PDF is empty")
        require(path.read_bytes().startswith(b"%PDF-"), "Teaser PDF is not a PDF")


def check_demo():
    path = ROOT / "demo"
    if path.exists():
        required = ("app.py", "README.md", "requirements.txt", "demo_logic.py")
        require(all((path / name).is_file() for name in required), "Demo source file missing")
        require((ROOT / "tests/test_demo_logic.py").is_file(), "Demo tests missing")
        app = (path / "app.py").read_text()
        require("share=False" in app and "server_name=\"127.0.0.1\"" in app, "Demo must stay local")


def check_evidence_docs():
    evidence = (ROOT / "docs/evidence_status.md").read_text()
    require("Real AI agents free-ride. | Not tested." in evidence, "Untested real LLM behavior label missing")
    require("Humans free-ride in this setting. | Not tested." in evidence, "Untested human behavior label missing")
    require("Demo demonstrates educational effectiveness. | Not tested." in evidence, "Untested educational effectiveness label missing")
    readme = (ROOT / "README.md").read_text()
    require("Behavioral experiment: not conducted" in readme, "README behavioral status missing")
    require("educational effectiveness has not been evaluated" in readme.lower(), "README educational status missing")


CHECKS = [
    ("A required core files", check_core_files),
    ("B baseline JSON", check_baseline_json),
    ("C baseline parameters and action order", check_parameters),
    ("D payoff matrices", check_matrices),
    ("E pure equilibria", check_pure),
    ("F mixed equilibrium", check_mixed),
    ("G six cost rows", check_costs),
    ("H interior probabilities", check_interior),
    ("I boundary labels", check_boundaries),
    ("J high-cost equilibrium", check_high_cost),
    ("K executed notebook", check_notebook),
    ("L vector computational PDF", check_figure_pdf),
    ("M editable Draw.io XML", check_drawio),
    ("N optional teaser PDF", check_optional_teaser_pdf),
    ("O local demo files", check_demo),
    ("P evidence-status documentation", check_evidence_docs),
]


def main():
    failures = 0
    for name, check in CHECKS:
        try:
            check()
            print(f"PASS {name}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {name}: {exc}")
    print(f"Summary: {len(CHECKS)-failures}/{len(CHECKS)} checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
