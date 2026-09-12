"""Transparent interruption-authority policies for a synthetic 20-minute task.

Online scheduling uses only current report fields and audited historical counts.
Outcome labels are accepted only by :func:`evaluate_decisions`, after routing.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


AGENTS = ("Evidence", "Planning", "Idea")
CURRENT_CLAIM_POLICY = "current_claim"
REPUTATION_POLICY = "reputation_calibrated"
POLICIES = (CURRENT_CLAIM_POLICY, REPUTATION_POLICY)

ALPHA = 0.5
INTERRUPT_THRESHOLD = 0.65
QUEUE_THRESHOLD = 0.35
SESSION_HORIZON = 20
CHECKPOINT_INTERVAL = 5
COLD_START_RELIABILITY = 0.5
IMPORTANT_LATE_LOSS = 7.0
ATTENTION_COSTS = {
    "interrupt": 2.0,
    "queue": 0.2,
    "digest": 0.05,
}


@dataclass(frozen=True)
class Decision:
    """One deterministic online routing decision."""

    id: str
    agent: str
    task_type: str
    arrival_minute: int
    importance: float
    urgency: float
    current_claim_score: float
    historical_reliability: float
    policy: str
    policy_score: float
    route: str
    delivery_minute: int

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a UTF-8 JSON object from ``path``."""

    with Path(path).open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def _unit_interval(value: Any, name: str) -> float:
    """Validate and return a numeric value in the closed unit interval."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    numeric = float(value)
    if not 0.0 <= numeric <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return numeric


def current_claim_score(importance: Any, urgency: Any, alpha: Any = ALPHA) -> float:
    """Calculate ``N = alpha * I + (1 - alpha) * U`` with bounded inputs."""

    importance_value = _unit_interval(importance, "importance")
    urgency_value = _unit_interval(urgency, "urgency")
    alpha_value = _unit_interval(alpha, "alpha")
    return alpha_value * importance_value + (1.0 - alpha_value) * urgency_value


def beta_smoothed_reliability(valid_count: int, audited_count: int) -> float:
    """Estimate reliability using a Beta(1, 1) prior.

    The posterior mean is ``(valid_count + 1) / (audited_count + 2)``.
    """

    if isinstance(valid_count, bool) or isinstance(audited_count, bool):
        raise ValueError("history counts must be integers")
    if not isinstance(valid_count, int) or not isinstance(audited_count, int):
        raise ValueError("history counts must be integers")
    if valid_count < 0 or audited_count < 0 or valid_count > audited_count:
        raise ValueError("history counts require 0 <= valid_count <= audited_count")
    return (valid_count + 1.0) / (audited_count + 2.0)


def build_reliability_lookup(history_document: Mapping[str, Any]) -> dict[tuple[str, str], float]:
    """Build task-specific reliability values keyed by ``(agent, task_type)``."""

    lookup: dict[tuple[str, str], float] = {}
    records = history_document.get("history", [])
    if not isinstance(records, list):
        raise ValueError("history must be a list")
    for record in records:
        key = (str(record["agent"]), str(record["task_type"]))
        if key in lookup:
            raise ValueError(f"duplicate history record for {key}")
        lookup[key] = beta_smoothed_reliability(
            record["valid_count"], record["audited_count"]
        )
    return lookup


def reliability_for(
    report: Mapping[str, Any],
    reliability_lookup: Mapping[tuple[str, str], float],
) -> float:
    """Return task-specific reliability or the transparent 0.50 cold start."""

    key = (str(report["agent"]), str(report["task_type"]))
    return _unit_interval(
        reliability_lookup.get(key, COLD_START_RELIABILITY),
        "historical reliability",
    )


def route_score(score: Any) -> str:
    """Map a score to interrupt, queue, or digest at the exact thresholds."""

    bounded_score = _unit_interval(score, "score")
    if bounded_score >= INTERRUPT_THRESHOLD:
        return "interrupt"
    if bounded_score >= QUEUE_THRESHOLD:
        return "queue"
    return "digest"


def next_checkpoint(
    arrival_minute: int,
    interval: int = CHECKPOINT_INTERVAL,
    horizon: int = SESSION_HORIZON,
) -> int:
    """Return the strictly next checkpoint within the session horizon.

    Reports must arrive before minute 20. Thus an arrival exactly at a checkpoint
    is sent to the following checkpoint: 5 -> 10 and 10 -> 15.
    """

    if isinstance(arrival_minute, bool) or not isinstance(arrival_minute, int):
        raise ValueError("arrival_minute must be an integer")
    if not 0 <= arrival_minute < horizon:
        raise ValueError("arrival_minute must be in [0, session_horizon)")
    checkpoint = (arrival_minute // interval + 1) * interval
    if checkpoint > horizon:
        raise ValueError("no checkpoint remains within the session horizon")
    return checkpoint


def _delivery_minute(route: str, arrival_minute: int) -> int:
    """Calculate delivery time for an online route."""

    if route == "interrupt":
        return arrival_minute
    if route == "queue":
        return next_checkpoint(arrival_minute)
    if route == "digest":
        return SESSION_HORIZON
    raise ValueError(f"unknown route: {route}")


def schedule_report(
    report: Mapping[str, Any],
    policy: str,
    reliability_lookup: Mapping[tuple[str, str], float],
    alpha: float = ALPHA,
) -> Decision:
    """Route one report without reading any evaluation-only outcome label."""

    if policy not in POLICIES:
        raise ValueError(f"policy must be one of {POLICIES}")
    report_id = str(report["id"])
    agent = str(report["agent"])
    task_type = str(report["task_type"])
    if agent not in AGENTS:
        raise ValueError(f"unknown agent: {agent}")

    arrival = report["arrival_minute"]
    if isinstance(arrival, bool) or not isinstance(arrival, int):
        raise ValueError("arrival_minute must be an integer")
    if not 0 <= arrival < SESSION_HORIZON:
        raise ValueError("arrival_minute must be in [0, 20)")

    importance = _unit_interval(report["importance"], "importance")
    urgency = _unit_interval(report["urgency"], "urgency")
    current_score = round(current_claim_score(importance, urgency, alpha), 12)
    reliability = reliability_for(report, reliability_lookup)
    policy_score = round(
        current_score
        if policy == CURRENT_CLAIM_POLICY
        else current_score * reliability,
        12,
    )
    route = route_score(policy_score)

    return Decision(
        id=report_id,
        agent=agent,
        task_type=task_type,
        arrival_minute=arrival,
        importance=importance,
        urgency=urgency,
        current_claim_score=current_score,
        historical_reliability=round(reliability, 12),
        policy=policy,
        policy_score=policy_score,
        route=route,
        delivery_minute=_delivery_minute(route, arrival),
    )


def schedule_reports(
    reports: Iterable[Mapping[str, Any]],
    policy: str,
    reliability_lookup: Mapping[tuple[str, str], float],
    alpha: float = ALPHA,
) -> list[Decision]:
    """Route reports deterministically in the supplied order."""

    return [schedule_report(report, policy, reliability_lookup, alpha) for report in reports]


def _outcome_lookup(outcomes: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    """Index evaluation-only outcomes and reject duplicate identifiers."""

    lookup: dict[str, Mapping[str, Any]] = {}
    for outcome in outcomes:
        report_id = str(outcome["id"])
        if report_id in lookup:
            raise ValueError(f"duplicate outcome for {report_id}")
        lookup[report_id] = outcome
    return lookup


def evaluate_decisions(
    decisions: Iterable[Decision],
    outcomes: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Evaluate already-made decisions against hidden synthetic labels."""

    decision_list = list(decisions)
    outcomes_by_id = _outcome_lookup(outcomes)
    missing = [decision.id for decision in decision_list if decision.id not in outcomes_by_id]
    if missing:
        raise ValueError(f"missing outcomes for: {missing}")

    route_counts = Counter(decision.route for decision in decision_list)
    immediate = route_counts["interrupt"]
    invalid_immediate = 0
    important_count = 0
    important_timely = 0
    late_alert_loss = 0.0

    by_agent: dict[str, Counter[str]] = {agent: Counter() for agent in AGENTS}
    for decision in decision_list:
        outcome = outcomes_by_id[decision.id]
        valid = bool(outcome["valid"])
        late_loss = float(outcome["late_loss"])
        latest_useful = int(outcome["latest_useful_minute"])
        timely = decision.delivery_minute <= latest_useful
        important = valid and late_loss >= IMPORTANT_LATE_LOSS

        if decision.route == "interrupt" and not valid:
            invalid_immediate += 1
        if important:
            important_count += 1
            if timely:
                important_timely += 1
        if valid and not timely:
            late_alert_loss += late_loss

        by_agent[decision.agent]["total"] += 1
        by_agent[decision.agent][decision.route] += 1

    attention_cost = sum(
        route_counts[route] * cost for route, cost in ATTENTION_COSTS.items()
    )
    routing_by_agent: dict[str, dict[str, Any]] = {}
    for agent in AGENTS:
        counts = by_agent[agent]
        total = counts["total"]
        routing_by_agent[agent] = {
            "report_count": total,
            "interrupt_count": counts["interrupt"],
            "queue_count": counts["queue"],
            "digest_count": counts["digest"],
            "interrupt_rate_within_agent": counts["interrupt"] / total if total else 0.0,
            "queue_rate_within_agent": counts["queue"] / total if total else 0.0,
            "digest_rate_within_agent": counts["digest"] / total if total else 0.0,
            "immediate_authority_share": counts["interrupt"] / immediate if immediate else 0.0,
        }

    return {
        "report_count": len(decision_list),
        "immediate_interruptions": immediate,
        "queued_notices": route_counts["queue"],
        "digest_notices": route_counts["digest"],
        "invalid_immediate_notices": invalid_immediate,
        "invalid_interruption_fraction": invalid_immediate / immediate if immediate else 0.0,
        "important_alert_count": important_count,
        "important_alerts_delivered_on_time": important_timely,
        "important_alert_timely_recall": important_timely / important_count if important_count else 0.0,
        "attention_cost": round(attention_cost, 12),
        "late_alert_loss": round(late_alert_loss, 12),
        "synthetic_joint_loss": round(attention_cost + late_alert_loss, 12),
        "routing_by_agent": routing_by_agent,
    }


def swap_agent_reliabilities(
    reliability_lookup: Mapping[tuple[str, str], float],
    first_agent: str,
    second_agent: str,
) -> dict[tuple[str, str], float]:
    """Swap two agents' reliability levels while preserving their task keys."""

    swapped = deepcopy(dict(reliability_lookup))
    first_values = {value for (agent, _), value in swapped.items() if agent == first_agent}
    second_values = {value for (agent, _), value in swapped.items() if agent == second_agent}
    if len(first_values) != 1 or len(second_values) != 1:
        raise ValueError("history swap requires one reliability level per selected agent")
    first_value = next(iter(first_values))
    second_value = next(iter(second_values))
    for key in list(swapped):
        if key[0] == first_agent:
            swapped[key] = second_value
        elif key[0] == second_agent:
            swapped[key] = first_value
    return swapped


def equal_count_ranking(
    reports: Iterable[Mapping[str, Any]],
    policy: str,
    reliability_lookup: Mapping[tuple[str, str], float],
    immediate_count: int,
    alpha: float = ALPHA,
) -> list[Decision]:
    """Run an offline ranking diagnostic with an exact interruption budget.

    The top ``immediate_count`` reports by policy score interrupt. Every other
    report uses the same fallback: queue to the strictly next checkpoint. This
    isolates ranking quality from each policy's online score-to-route mapping.
    It is an offline comparison, not an online deployment policy.
    """

    report_list = list(reports)
    if not 0 <= immediate_count <= len(report_list):
        raise ValueError("immediate_count is outside the report count")
    scored = schedule_reports(report_list, policy, reliability_lookup, alpha)
    ranked = sorted(
        scored,
        key=lambda decision: (
            -decision.policy_score,
            decision.arrival_minute,
            decision.id,
        ),
    )
    selected_ids = {decision.id for decision in ranked[:immediate_count]}

    diagnostic: list[Decision] = []
    for decision in scored:
        if decision.id in selected_ids:
            route = "interrupt"
        else:
            route = "queue"
        diagnostic.append(
            Decision(
                **{
                    **decision.to_dict(),
                    "route": route,
                    "delivery_minute": _delivery_minute(route, decision.arrival_minute),
                }
            )
        )
    return diagnostic
