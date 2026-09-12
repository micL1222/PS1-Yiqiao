#!/usr/bin/env python3
"""Run the fixed synthetic interruption-authority evaluation.

This script has no network access, randomness, participant data, or API calls.
It writes deterministic JSON metrics and a decision-level CSV under outputs/.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping


COMPANION_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COMPANION_ROOT))

from src.scheduler import (  # noqa: E402
    ALPHA,
    ATTENTION_COSTS,
    CHECKPOINT_INTERVAL,
    CURRENT_CLAIM_POLICY,
    IMPORTANT_LATE_LOSS,
    INTERRUPT_THRESHOLD,
    QUEUE_THRESHOLD,
    REPUTATION_POLICY,
    SESSION_HORIZON,
    Decision,
    build_reliability_lookup,
    equal_count_ranking,
    evaluate_decisions,
    load_json,
    schedule_reports,
    swap_agent_reliabilities,
)


DATA_DIR = COMPANION_ROOT / "data"
OUTPUT_DIR = COMPANION_ROOT / "outputs"
RESULTS_PATH = OUTPUT_DIR / "interruption_authority_results.json"
DECISIONS_PATH = OUTPUT_DIR / "interruption_authority_decisions.csv"


def _decision_dicts(decisions: Iterable[Decision]) -> list[dict[str, Any]]:
    """Convert decisions to serializable dictionaries."""

    return [decision.to_dict() for decision in decisions]


def _bundle(
    decisions: list[Decision], outcomes: list[Mapping[str, Any]]
) -> dict[str, Any]:
    """Pair decisions with their synthetic evaluation metrics."""

    return {
        "metrics": evaluate_decisions(decisions, outcomes),
        "decisions": _decision_dicts(decisions),
    }


def _labeled_reliabilities(
    lookup: Mapping[tuple[str, str], float]
) -> dict[str, float]:
    """Format tuple-keyed reliabilities for JSON output."""

    return {
        f"{agent}:{task_type}": reliability
        for (agent, task_type), reliability in sorted(lookup.items())
    }


def _operational_results(decisions: Iterable[Decision]) -> list[tuple[Any, ...]]:
    """Return fields that determine observable routing, excluding audit metadata."""

    return [
        (
            decision.id,
            decision.policy_score,
            decision.route,
            decision.delivery_minute,
        )
        for decision in decisions
    ]


def _selected_interruption_ids(decisions: Iterable[Decision]) -> list[str]:
    """Return interruption IDs in deterministic rank-independent report order."""

    return [decision.id for decision in decisions if decision.route == "interrupt"]


def _write_decisions_csv(
    bundles: Iterable[tuple[str, str, list[Decision]]],
    outcomes: list[Mapping[str, Any]],
) -> None:
    """Write one auditable table covering online and offline decisions."""

    outcomes_by_id = {str(outcome["id"]): outcome for outcome in outcomes}
    fieldnames = [
        "scenario",
        "policy",
        "id",
        "agent",
        "task_type",
        "arrival_minute",
        "importance",
        "urgency",
        "current_claim_score",
        "historical_reliability",
        "policy_score",
        "route",
        "delivery_minute",
        "synthetic_valid",
        "synthetic_late_loss",
        "synthetic_latest_useful_minute",
        "synthetic_important_alert",
        "synthetic_delivered_on_time",
        "synthetic_late_loss_incurred",
    ]
    with DECISIONS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario, policy_label, decisions in bundles:
            for decision in decisions:
                outcome = outcomes_by_id[decision.id]
                valid = bool(outcome["valid"])
                late_loss = float(outcome["late_loss"])
                latest_useful = int(outcome["latest_useful_minute"])
                timely = decision.delivery_minute <= latest_useful
                writer.writerow(
                    {
                        "scenario": scenario,
                        "policy": policy_label,
                        **{
                            key: value
                            for key, value in decision.to_dict().items()
                            if key != "policy"
                        },
                        "synthetic_valid": valid,
                        "synthetic_late_loss": late_loss,
                        "synthetic_latest_useful_minute": latest_useful,
                        "synthetic_important_alert": valid
                        and late_loss >= IMPORTANT_LATE_LOSS,
                        "synthetic_delivered_on_time": timely,
                        "synthetic_late_loss_incurred": late_loss
                        if valid and not timely
                        else 0.0,
                    }
                )


def main() -> None:
    """Run all deterministic synthetic policies and diagnostics."""

    reports_document = load_json(DATA_DIR / "reports.json")
    history_document = load_json(DATA_DIR / "history.json")
    outcomes_document = load_json(DATA_DIR / "outcomes.json")
    reports = reports_document["reports"]
    outcomes = outcomes_document["outcomes"]
    if len(reports) != 18:
        raise ValueError("the diagnostic dataset must contain exactly 18 reports")

    reliabilities = build_reliability_lookup(history_document)
    baseline_decisions = schedule_reports(
        reports, CURRENT_CLAIM_POLICY, reliabilities
    )
    reputation_decisions = schedule_reports(
        reports, REPUTATION_POLICY, reliabilities
    )

    swapped_reliabilities = swap_agent_reliabilities(
        reliabilities, "Evidence", "Idea"
    )
    swapped_baseline_decisions = schedule_reports(
        reports, CURRENT_CLAIM_POLICY, swapped_reliabilities
    )
    swapped_reputation_decisions = schedule_reports(
        reports, REPUTATION_POLICY, swapped_reliabilities
    )
    baseline_unchanged = _operational_results(
        baseline_decisions
    ) == _operational_results(swapped_baseline_decisions)
    if not baseline_unchanged:
        raise AssertionError("history affected the current-claim-only policy")

    immediate_budget = evaluate_decisions(
        baseline_decisions, outcomes
    )["immediate_interruptions"]
    equal_baseline_decisions = equal_count_ranking(
        reports,
        CURRENT_CLAIM_POLICY,
        reliabilities,
        immediate_budget,
    )
    equal_reputation_decisions = equal_count_ranking(
        reports,
        REPUTATION_POLICY,
        reliabilities,
        immediate_budget,
    )

    result = {
        "metadata": {
            "synthetic": True,
            "research_direction": "Yiqiao Liu",
            "implementation_note": "Implemented with Codex assistance.",
            "evidence_boundary": (
                "Diagnostic construction only; not human data, real LLM output, "
                "field evidence, deployment evidence, or safety validation."
            ),
            "deterministic": True,
        },
        "parameters": {
            "alpha": ALPHA,
            "current_claim_score": "N = alpha * I + (1 - alpha) * U",
            "baseline_score": "S = N",
            "reputation_score": "S = N * R",
            "reliability_estimator": "R = (valid_count + 1) / (audited_count + 2)",
            "interrupt_threshold": INTERRUPT_THRESHOLD,
            "queue_threshold": QUEUE_THRESHOLD,
            "session_horizon": SESSION_HORIZON,
            "checkpoint_interval": CHECKPOINT_INTERVAL,
            "queue_rule": "strictly next 5-minute checkpoint",
            "important_alert_definition": "valid and late_loss >= 7",
            "attention_costs": ATTENTION_COSTS,
            "joint_loss": "attention_cost + late_alert_loss",
        },
        "historical_reliability": _labeled_reliabilities(reliabilities),
        "online": {
            CURRENT_CLAIM_POLICY: _bundle(baseline_decisions, outcomes),
            REPUTATION_POLICY: _bundle(reputation_decisions, outcomes),
        },
        "history_swap_stress_test": {
            "label": "OFFLINE SYNTHETIC STRESS TEST",
            "description": (
                "Evidence and Idea historical reliability are swapped while "
                "current claims and hidden outcomes remain fixed."
            ),
            "swapped_historical_reliability": _labeled_reliabilities(
                swapped_reliabilities
            ),
            "current_claim_decisions_unchanged": baseline_unchanged,
            CURRENT_CLAIM_POLICY: _bundle(swapped_baseline_decisions, outcomes),
            REPUTATION_POLICY: _bundle(swapped_reputation_decisions, outcomes),
        },
        "equal_count_ranking_diagnostic": {
            "label": "OFFLINE RANKING DIAGNOSTIC - NOT AN ONLINE DEPLOYMENT POLICY",
            "description": (
                "Both rankings receive the same immediate-interruption count, "
                "set to the online current-claim policy's threshold-based count. "
                "Every non-selected report uses an identical strictly-next-"
                "checkpoint queue fallback, independent of policy score."
            ),
            "immediate_interruption_budget": immediate_budget,
            CURRENT_CLAIM_POLICY: {
                **_bundle(equal_baseline_decisions, outcomes),
                "selected_interruption_ids": _selected_interruption_ids(
                    equal_baseline_decisions
                ),
            },
            REPUTATION_POLICY: {
                **_bundle(equal_reputation_decisions, outcomes),
                "selected_interruption_ids": _selected_interruption_ids(
                    equal_reputation_decisions
                ),
            },
        },
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")

    _write_decisions_csv(
        [
            ("online", CURRENT_CLAIM_POLICY, baseline_decisions),
            ("online", REPUTATION_POLICY, reputation_decisions),
            ("history_swap", CURRENT_CLAIM_POLICY, swapped_baseline_decisions),
            ("history_swap", REPUTATION_POLICY, swapped_reputation_decisions),
            ("equal_count_offline", CURRENT_CLAIM_POLICY, equal_baseline_decisions),
            ("equal_count_offline", REPUTATION_POLICY, equal_reputation_decisions),
        ],
        outcomes,
    )

    summary = {
        "outputs": [str(RESULTS_PATH), str(DECISIONS_PATH)],
        "online_current_claim": result["online"][CURRENT_CLAIM_POLICY]["metrics"],
        "online_reputation_calibrated": result["online"][REPUTATION_POLICY]["metrics"],
        "history_swap_reputation_calibrated": result["history_swap_stress_test"][
            REPUTATION_POLICY
        ]["metrics"],
        "equal_count_current_claim": result["equal_count_ranking_diagnostic"][
            CURRENT_CLAIM_POLICY
        ]["metrics"],
        "equal_count_reputation_calibrated": result[
            "equal_count_ranking_diagnostic"
        ][REPUTATION_POLICY]["metrics"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
