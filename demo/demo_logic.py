"""Presentation-facing calculations that reuse the verified source model."""

from src.information_acquisition_game import ACTIONS, payoff_matrices
from src.run_baseline_analysis import analyze_case


def _action_index(action):
    if action not in ACTIONS:
        raise ValueError(f"Action must be one of {ACTIONS}")
    return ACTIONS.index(action)


def evaluate_choice(value, cost, agent_b_action, agent_a_action):
    """Evaluate Agent A's selected action against the other available action."""
    a, b = payoff_matrices(value, cost)
    row = _action_index(agent_a_action)
    col = _action_index(agent_b_action)
    alternative_row = 1 - row
    selected_payoff = float(a[row, col])
    alternative_payoff = float(a[alternative_row, col])
    best_value = max(float(a[0, col]), float(a[1, col]))
    best_responses = tuple(ACTIONS[i] for i in (0, 1) if float(a[i, col]) == best_value)
    if cost == 0:
        if agent_b_action == "Research":
            interpretation = "Zero-cost boundary: both actions tie because the information is already shared and Research costs nothing."
        else:
            interpretation = "Zero-cost boundary: when B skips, free Research obtains the shared information value."
    elif cost == value and agent_b_action == "Skip":
        interpretation = "Equal-value boundary: Research and Skip tie for A when B skips, since V - c = 0."
    elif cost > value and agent_b_action == "Skip":
        interpretation = "High-cost case: Research yields a negative payoff while Skip yields zero, so private research is unattractive."
    elif agent_b_action == "Research":
        interpretation = "In this payoff model, A can obtain the shared information while avoiding the private research cost by choosing Skip."
    else:
        interpretation = "In this payoff model, A gains by researching when B skips because V - c is positive."
    return {
        "V": float(value),
        "c": float(cost),
        "agent_a_action": agent_a_action,
        "agent_b_action": agent_b_action,
        "agent_a_payoff": selected_payoff,
        "agent_b_payoff": float(b[row, col]),
        "alternative_action": ACTIONS[alternative_row],
        "alternative_payoff": alternative_payoff,
        "best_responses": best_responses,
        "selected_is_best_response": agent_a_action in best_responses,
        "unilateral_deviation_improves": alternative_payoff > selected_payoff,
        "interpretation": interpretation,
    }


def analyze_game(value, cost):
    """Provide the complete verified-model analysis for the selected parameters."""
    return analyze_case(value, cost)


def _number(value):
    return f"{value:g}"


def render_choice(value, cost, agent_b_action, agent_a_action):
    result = evaluate_choice(value, cost, agent_b_action, agent_a_action)
    return "\n".join([
        "### Choice evaluation",
        f"- **Selected profile (A, B):** ({result['agent_a_action']}, {result['agent_b_action']})",
        f"- **Agent A payoff:** {_number(result['agent_a_payoff'])}",
        f"- **Agent B payoff:** {_number(result['agent_b_payoff'])}",
        f"- **A's alternative action and payoff:** {result['alternative_action']} → {_number(result['alternative_payoff'])}",
        f"- **A's best responses to B:** {', '.join(result['best_responses'])}",
        f"- **Selected action is a best response:** {'Yes' if result['selected_is_best_response'] else 'No'}",
        f"- **Unilateral deviation improves A's payoff:** {'Yes' if result['unilateral_deviation_improves'] else 'No'}",
        "",
        f"**Interpretation:** {result['interpretation']}",
    ])


def render_game(value, cost):
    result = analyze_game(value, cost)
    a = result["agent_a_payoffs"]
    b = result["agent_b_payoffs"]
    pure = ", ".join(f"({x}, {y})" for x, y in result["independent_pure_equilibria"])
    nashpy_lines = [
        f"- {item['classification'].capitalize()}: A = {item['agent_a']}; B = {item['agent_b']}"
        for item in result["nashpy_support_enumeration"]
    ]
    lines = [
        "### Full game analysis",
        f"**Parameters:** V = {_number(value)}, c = {_number(cost)}. Action order: [Research, Skip].",
        f"**Case:** {result['relation_to_V']}.",
        "",
        "| Agent A / Agent B | Research | Skip |",
        "| --- | --- | --- |",
        f"| **Research** | ({_number(a[0][0])}, {_number(b[0][0])}) | ({_number(a[0][1])}, {_number(b[0][1])}) |",
        f"| **Skip** | ({_number(a[1][0])}, {_number(b[1][0])}) | ({_number(a[1][1])}, {_number(b[1][1])}) |",
        "",
        f"**Pure Nash equilibria:** {pure}.",
        "",
        "**NashPy support-enumeration output:**",
        *nashpy_lines,
        "",
    ]
    if result["relation_to_V"] == "interior":
        lines.append(
            f"**Analytical interior mixed equilibrium:** p(Research) = 1 - c/V = {result['analytical_p_research']:.3f} "
            "for each agent. NashPy agrees within numerical tolerance."
        )
    elif result["relation_to_V"] == "zero-cost boundary":
        lines.append("**Boundary note:** c = 0 creates indifference. This finite support-enumeration output is not a complete characterization of any equilibrium continuum.")
    elif result["relation_to_V"] == "equal-value boundary":
        lines.append("**Boundary note:** c = V creates indifference. The interior mixed formula is not used to characterize this degenerate case.")
    else:
        lines.append("**High-cost note:** c > V makes Research privately unattractive when the other agent skips.")
    lines.extend(["", "This is a formal-game calculation, not observed AI or human behavior."])
    return "\n".join(lines)
