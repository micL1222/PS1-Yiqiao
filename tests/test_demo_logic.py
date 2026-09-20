"""Behavioral checks of the demo's model-backed calculations, not UI text alone."""

import unittest

from demo.demo_logic import analyze_game, evaluate_choice


class DemoLogicTests(unittest.TestCase):
    def test_baseline_skip_best_when_b_researches(self):
        result = evaluate_choice(4, 2, "Research", "Skip")
        self.assertEqual(result["best_responses"], ("Skip",))
        self.assertTrue(result["selected_is_best_response"])
        self.assertEqual((result["agent_a_payoff"], result["agent_b_payoff"]), (4, 2))
        self.assertFalse(result["unilateral_deviation_improves"])

    def test_baseline_research_best_when_b_skips(self):
        result = evaluate_choice(4, 2, "Skip", "Research")
        self.assertEqual(result["best_responses"], ("Research",))
        self.assertTrue(result["selected_is_best_response"])
        self.assertEqual((result["agent_a_payoff"], result["agent_b_payoff"]), (2, 4))

    def test_high_cost_skip_unique(self):
        result = evaluate_choice(4, 5, "Skip", "Skip")
        self.assertEqual(result["best_responses"], ("Skip",))
        self.assertEqual(result["alternative_payoff"], -1)
        self.assertTrue(result["selected_is_best_response"])

    def test_equal_value_tie(self):
        result = evaluate_choice(4, 4, "Skip", "Research")
        self.assertEqual(result["best_responses"], ("Research", "Skip"))
        self.assertTrue(result["selected_is_best_response"])
        self.assertEqual(result["alternative_payoff"], 0)

    def test_zero_cost_tie_when_b_researches(self):
        result = evaluate_choice(4, 0, "Research", "Skip")
        self.assertEqual(result["best_responses"], ("Research", "Skip"))
        self.assertEqual(result["alternative_payoff"], 4)

    def test_baseline_pure_equilibria_from_source(self):
        result = analyze_game(4, 2)
        self.assertEqual(
            {tuple(profile) for profile in result["independent_pure_equilibria"]},
            {("Research", "Skip"), ("Skip", "Research")},
        )
        self.assertEqual(result["agent_a_payoffs"], [[2, 2], [4, 0]])
        self.assertEqual(result["agent_b_payoffs"], [[2, 4], [2, 0]])

    def test_baseline_mixed_equilibrium_from_source(self):
        result = analyze_game(4, 2)
        mixed = [e for e in result["nashpy_support_enumeration"] if e["classification"] == "mixed"]
        self.assertEqual(len(mixed), 1)
        self.assertEqual(mixed[0]["agent_a"], [0.5, 0.5])
        self.assertEqual(mixed[0]["agent_b"], [0.5, 0.5])
        self.assertEqual(result["analytical_p_research"], 0.5)

    def test_invalid_information_value(self):
        for value in (0, -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                evaluate_choice(value, 2, "Research", "Skip")

    def test_negative_research_cost(self):
        with self.assertRaises(ValueError):
            evaluate_choice(4, -1, "Research", "Skip")

    def test_unilateral_deviation_improves_if_wrong_choice(self):
        result = evaluate_choice(4, 2, "Research", "Research")
        self.assertFalse(result["selected_is_best_response"])
        self.assertTrue(result["unilateral_deviation_improves"])
        self.assertEqual(result["alternative_payoff"], 4)


if __name__ == "__main__":
    unittest.main()
