"""Unit tests for the deterministic interruption-authority scheduler."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest


COMPANION_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COMPANION_ROOT))

from src.scheduler import (  # noqa: E402
    CURRENT_CLAIM_POLICY,
    REPUTATION_POLICY,
    beta_smoothed_reliability,
    build_reliability_lookup,
    current_claim_score,
    equal_count_ranking,
    evaluate_decisions,
    load_json,
    next_checkpoint,
    reliability_for,
    route_score,
    schedule_report,
    schedule_reports,
    swap_agent_reliabilities,
)


class SchedulerTests(unittest.TestCase):
    """Check scores, boundaries, information separation, and determinism."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.reports_document = load_json(COMPANION_ROOT / "data" / "reports.json")
        cls.history_document = load_json(COMPANION_ROOT / "data" / "history.json")
        cls.outcomes_document = load_json(COMPANION_ROOT / "data" / "outcomes.json")
        cls.reports = cls.reports_document["reports"]
        cls.outcomes = cls.outcomes_document["outcomes"]
        cls.reliabilities = build_reliability_lookup(cls.history_document)

    def test_dataset_has_exactly_eighteen_synthetic_reports(self) -> None:
        self.assertTrue(self.reports_document["metadata"]["synthetic"])
        self.assertEqual(len(self.reports), 18)
        self.assertEqual({report["agent"] for report in self.reports}, {"Evidence", "Planning", "Idea"})

    def test_score_bounds(self) -> None:
        self.assertEqual(current_claim_score(0, 0), 0.0)
        self.assertEqual(current_claim_score(1, 1), 1.0)
        for args in ((-0.01, 0.5), (1.01, 0.5), (0.5, -0.01), (0.5, 1.01)):
            with self.assertRaises(ValueError):
                current_claim_score(*args)

    def test_alpha_calculation(self) -> None:
        self.assertAlmostEqual(current_claim_score(0.8, 0.2, alpha=0.5), 0.5)
        self.assertAlmostEqual(current_claim_score(0.8, 0.2, alpha=0.25), 0.35)

    def test_beta_smoothed_reliability(self) -> None:
        self.assertAlmostEqual(beta_smoothed_reliability(7, 10), 8 / 12)
        with self.assertRaises(ValueError):
            beta_smoothed_reliability(11, 10)

    def test_expected_agent_reliabilities(self) -> None:
        self.assertAlmostEqual(self.reliabilities[("Evidence", "evidence_check")], 0.90)
        self.assertAlmostEqual(self.reliabilities[("Planning", "planning_risk")], 0.50)
        self.assertAlmostEqual(self.reliabilities[("Idea", "idea_suggestion")], 0.20)

    def test_cold_start_reliability(self) -> None:
        unknown = {"agent": "Evidence", "task_type": "new_task_type"}
        self.assertAlmostEqual(reliability_for(unknown, self.reliabilities), 0.50)

    def test_interrupt_threshold_exactly(self) -> None:
        self.assertEqual(route_score(0.65), "interrupt")

        boundary_report = next(report for report in self.reports if report["id"] == "E02")
        decision = schedule_report(
            boundary_report, CURRENT_CLAIM_POLICY, self.reliabilities
        )
        self.assertEqual(decision.current_claim_score, 0.65)
        self.assertEqual(decision.route, "interrupt")

    def test_just_below_interrupt_threshold(self) -> None:
        self.assertEqual(route_score(0.649999999), "queue")

    def test_queue_threshold_exactly(self) -> None:
        self.assertEqual(route_score(0.35), "queue")

    def test_just_below_queue_threshold(self) -> None:
        self.assertEqual(route_score(0.349999999), "digest")

    def test_strictly_next_checkpoint_behavior(self) -> None:
        expected = {4: 5, 5: 10, 9: 10, 10: 15, 19: 20}
        self.assertEqual({minute: next_checkpoint(minute) for minute in expected}, expected)

    def test_horizon_boundary_is_explicit(self) -> None:
        with self.assertRaises(ValueError):
            next_checkpoint(20)

    def test_outcome_labels_do_not_affect_online_scheduling(self) -> None:
        clean_report = deepcopy(self.reports[0])
        contaminated_report = {
            **clean_report,
            "valid": False,
            "late_loss": 999,
            "latest_useful_minute": 0,
        }
        clean_decision = schedule_report(
            clean_report, REPUTATION_POLICY, self.reliabilities
        )
        contaminated_decision = schedule_report(
            contaminated_report, REPUTATION_POLICY, self.reliabilities
        )
        self.assertEqual(clean_decision, contaminated_decision)

    def test_repeated_runs_are_deterministic(self) -> None:
        first = schedule_reports(self.reports, REPUTATION_POLICY, self.reliabilities)
        second = schedule_reports(self.reports, REPUTATION_POLICY, self.reliabilities)
        self.assertEqual(first, second)

    def test_history_swap_changes_only_reputation_policy(self) -> None:
        swapped = swap_agent_reliabilities(self.reliabilities, "Evidence", "Idea")
        current_original = schedule_reports(
            self.reports, CURRENT_CLAIM_POLICY, self.reliabilities
        )
        current_swapped = schedule_reports(
            self.reports, CURRENT_CLAIM_POLICY, swapped
        )
        reputation_original = schedule_reports(
            self.reports, REPUTATION_POLICY, self.reliabilities
        )
        reputation_swapped = schedule_reports(
            self.reports, REPUTATION_POLICY, swapped
        )
        def operational_results(decisions):
            return [
                (
                    decision.id,
                    decision.policy_score,
                    decision.route,
                    decision.delivery_minute,
                )
                for decision in decisions
            ]

        self.assertEqual(
            operational_results(current_original), operational_results(current_swapped)
        )
        self.assertNotEqual(
            operational_results(reputation_original),
            operational_results(reputation_swapped),
        )

    def test_equal_count_has_same_budget_and_no_digest(self) -> None:
        immediate_budget = 10
        for policy in (CURRENT_CLAIM_POLICY, REPUTATION_POLICY):
            decisions = equal_count_ranking(
                self.reports, policy, self.reliabilities, immediate_budget
            )
            routes = [decision.route for decision in decisions]
            self.assertEqual(routes.count("interrupt"), immediate_budget)
            self.assertEqual(routes.count("queue"), len(self.reports) - immediate_budget)
            self.assertNotIn("digest", routes)

    def test_equal_count_uniform_fallback_and_distinct_rankings(self) -> None:
        immediate_budget = 10
        by_policy = {
            policy: equal_count_ranking(
                self.reports, policy, self.reliabilities, immediate_budget
            )
            for policy in (CURRENT_CLAIM_POLICY, REPUTATION_POLICY)
        }
        selected = {
            policy: {
                decision.id for decision in decisions if decision.route == "interrupt"
            }
            for policy, decisions in by_policy.items()
        }
        self.assertNotEqual(
            selected[CURRENT_CLAIM_POLICY], selected[REPUTATION_POLICY]
        )

        for policy, decisions in by_policy.items():
            fallback = {
                decision.id: decision.delivery_minute
                for decision in decisions
                if decision.id not in selected[policy]
            }
            expected = {
                report["id"]: next_checkpoint(report["arrival_minute"])
                for report in self.reports
                if report["id"] not in selected[policy]
            }
            self.assertEqual(fallback, expected)

    def test_online_policy_results_remain_unchanged(self) -> None:
        current_metrics = evaluate_decisions(
            schedule_reports(
                self.reports, CURRENT_CLAIM_POLICY, self.reliabilities
            ),
            self.outcomes,
        )
        reputation_metrics = evaluate_decisions(
            schedule_reports(
                self.reports, REPUTATION_POLICY, self.reliabilities
            ),
            self.outcomes,
        )
        self.assertEqual(
            (
                current_metrics["immediate_interruptions"],
                current_metrics["queued_notices"],
                current_metrics["digest_notices"],
                current_metrics["late_alert_loss"],
                current_metrics["synthetic_joint_loss"],
            ),
            (10, 5, 3, 0.0, 21.15),
        )
        self.assertEqual(
            (
                reputation_metrics["immediate_interruptions"],
                reputation_metrics["queued_notices"],
                reputation_metrics["digest_notices"],
                reputation_metrics["late_alert_loss"],
                reputation_metrics["synthetic_joint_loss"],
            ),
            (2, 4, 12, 49.0, 54.4),
        )


if __name__ == "__main__":
    unittest.main()
