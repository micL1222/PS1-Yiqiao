"""Unit checks for the independently enumerated and NashPy equilibria."""

import unittest

import numpy as np

from src.information_acquisition_game import (
    ACTIONS,
    create_game,
    interior_mixed_research_probability,
    payoff_matrices,
    pure_nash_equilibria,
    support_enumeration_results,
)


class InformationAcquisitionGameTests(unittest.TestCase):
    def test_action_order(self):
        self.assertEqual(ACTIONS, ("Research", "Skip"))

    def test_baseline_payoff_matrices(self):
        a, b = payoff_matrices(4, 2)
        np.testing.assert_array_equal(a, [[2, 2], [4, 0]])
        np.testing.assert_array_equal(b, [[2, 4], [2, 0]])
        game = create_game(4, 2)
        np.testing.assert_array_equal(game.payoff_matrices[0], a)
        np.testing.assert_array_equal(game.payoff_matrices[1], b)

    def test_baseline_pure_equilibria(self):
        self.assertEqual(
            set(pure_nash_equilibria(4, 2)),
            {("Research", "Skip"), ("Skip", "Research")},
        )

    def test_baseline_nashpy_pure_equilibria(self):
        result = support_enumeration_results(4, 2)
        actual = {
            tuple(item["pure_profile"])
            for item in result["equilibria"]
            if item["classification"] == "pure"
        }
        self.assertEqual(actual, {("Research", "Skip"), ("Skip", "Research")})

    def test_baseline_nashpy_mixed_equilibrium(self):
        mixed = [
            item for item in support_enumeration_results(4, 2)["equilibria"]
            if item["classification"] == "mixed"
        ]
        self.assertEqual(len(mixed), 1)
        np.testing.assert_allclose(mixed[0]["agent_a"], [0.5, 0.5], atol=1e-9)
        np.testing.assert_allclose(mixed[0]["agent_b"], [0.5, 0.5], atol=1e-9)

    def test_baseline_analytical_mixed_probability(self):
        self.assertEqual(interior_mixed_research_probability(4, 2), 0.5)

    def test_low_interior_cost_mixed_probability(self):
        self._assert_interior_mixed(4, 1, 0.75)

    def test_higher_interior_cost_mixed_probability(self):
        self._assert_interior_mixed(4, 3, 0.25)

    def _assert_interior_mixed(self, value, cost, expected):
        self.assertEqual(interior_mixed_research_probability(value, cost), expected)
        mixed = [
            item for item in support_enumeration_results(value, cost)["equilibria"]
            if item["classification"] == "mixed"
        ]
        self.assertEqual(len(mixed), 1)
        np.testing.assert_allclose(mixed[0]["agent_a"], [expected, 1 - expected], atol=1e-9)
        np.testing.assert_allclose(mixed[0]["agent_b"], [expected, 1 - expected], atol=1e-9)

    def test_equal_value_boundary_pure_equilibria(self):
        # When c = V, indifference adds (Skip, Skip) to the pure equilibria.
        self.assertEqual(
            set(pure_nash_equilibria(4, 4)),
            {("Research", "Skip"), ("Skip", "Research"), ("Skip", "Skip")},
        )

    def test_high_cost_unique_pure_equilibrium(self):
        self.assertEqual(pure_nash_equilibria(4, 5), [("Skip", "Skip")])

    def test_zero_cost_boundary_pure_equilibria(self):
        # This lists pure profiles only, not the full degenerate mixed correspondence.
        self.assertEqual(
            set(pure_nash_equilibria(4, 0)),
            {("Research", "Research"), ("Research", "Skip"), ("Skip", "Research")},
        )

    def test_negative_cost_is_invalid(self):
        with self.assertRaises(ValueError):
            payoff_matrices(4, -1)

    def test_nonpositive_value_is_invalid(self):
        for value in (0, -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                payoff_matrices(value, 2)

    def test_formula_rejects_boundary_and_high_cost(self):
        for cost in (0, 4, 5):
            with self.subTest(cost=cost), self.assertRaises(ValueError):
                interior_mixed_research_probability(4, cost)


if __name__ == "__main__":
    unittest.main()
