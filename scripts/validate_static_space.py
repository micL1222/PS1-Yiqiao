"""Compare the deployed Static Space game logic with the trusted Python game."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.information_acquisition_game import (
    interior_mixed_research_probability,
    payoff_matrices,
    pure_nash_equilibria,
)


SOURCE = ROOT / "deployment/huggingface-static/model.js"
CASES = [(4, cost) for cost in range(6)]


def main() -> None:
    assert SOURCE.is_file(), "Static model source missing"
    script = """
const model = require(process.argv[1]);
const cases = JSON.parse(process.argv[2]);
process.stdout.write(JSON.stringify(cases.map(([V,c]) => ({
  V, c, payoffs: model.payoffs(V,c), pure: model.pure(V,c), mixed: model.mixed(V,c)
}))));
"""
    result = subprocess.run(
        ["node", "-e", script, str(SOURCE), json.dumps(CASES)],
        check=True, capture_output=True, text=True,
    )
    actual = json.loads(result.stdout)
    names = ("R", "S")
    for case in actual:
        value, cost = case["V"], case["c"]
        a, b = payoff_matrices(value, cost)
        for row in range(2):
            for col in range(2):
                key = names[row] + names[col]
                assert case["payoffs"][key] == [a[row, col], b[row, col]], (value, cost, key)
        expected_pure = [[left[0], right[0]] for left, right in pure_nash_equilibria(value, cost)]
        assert case["pure"] == expected_pure, (value, cost, "pure")
        if 0 < cost < value:
            assert case["mixed"]["type"] == "interior"
            expected_p = interior_mixed_research_probability(value, cost)
            assert abs(case["mixed"]["pR"] - expected_p) < 1e-12
            assert abs(case["mixed"]["pS"] - (1 - expected_p)) < 1e-12
        else:
            assert case["mixed"]["type"] in {"boundary", "outside"}
        print(f"PASS V={value}, c={cost}: payoffs, pure equilibria, mixed classification")
    assert actual[0]["pure"] == [["R", "R"], ["R", "S"], ["S", "R"]]
    assert actual[2]["payoffs"] == {"RR": [2, 2], "RS": [2, 4], "SR": [4, 2], "SS": [0, 0]}
    assert actual[4]["pure"] == [["R", "S"], ["S", "R"], ["S", "S"]]
    assert actual[5]["pure"] == [["S", "S"]]
    print("Static Space/Python parity: PASS (6 cases, V=4 and c=0..5)")


if __name__ == "__main__":
    main()
