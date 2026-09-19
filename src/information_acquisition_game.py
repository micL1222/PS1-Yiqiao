"""Two-agent public-information game with private research costs.

Rows are Agent A's actions and columns are Agent B's actions. In both
matrices, index 0 means Research and index 1 means Skip.
"""

from math import isfinite
from numbers import Real
import warnings

import nashpy as nash
import numpy as np

ACTIONS = ("Research", "Skip")
RESEARCH = 0
SKIP = 1


def validate_parameters(value, cost):
    """Return finite numeric (V, c), requiring V > 0 and c >= 0."""
    for name, number in (("V", value), ("c", cost)):
        if isinstance(number, bool) or not isinstance(number, Real):
            raise ValueError(f"{name} must be a finite real number")
        if not isfinite(number):
            raise ValueError(f"{name} must be finite")
    if value <= 0:
        raise ValueError("V must be greater than zero")
    if cost < 0:
        raise ValueError("c must be nonnegative")
    return float(value), float(cost)


def payoff_matrices(value, cost):
    """Construct A and B payoff matrices in Research, Skip action order."""
    value, cost = validate_parameters(value, cost)
    a = np.array([[value - cost, value - cost], [value, 0.0]])
    b = np.array([[value - cost, value], [value - cost, 0.0]])
    return a, b


def create_game(value, cost):
    """Return a NashPy game for validated parameters."""
    a, b = payoff_matrices(value, cost)
    return nash.Game(a, b)


def pure_nash_equilibria(value, cost):
    """Enumerate all four profiles; ties count as best responses."""
    a, b = payoff_matrices(value, cost)
    equilibria = []
    for row in (RESEARCH, SKIP):
        for col in (RESEARCH, SKIP):
            a_best = a[row, col] >= max(a[:, col])
            b_best = b[row, col] >= max(b[row, :])
            if a_best and b_best:
                equilibria.append((ACTIONS[row], ACTIONS[col]))
    return equilibria


def _describe_equilibrium(agent_a, agent_b, tolerance):
    """Preserve NashPy probabilities while classifying a returned profile."""
    agent_a = np.asarray(agent_a, dtype=float)
    agent_b = np.asarray(agent_b, dtype=float)
    if agent_a.shape != (2,) or agent_b.shape != (2,):
        raise ValueError("Expected two probabilities for each player")
    for strategy in (agent_a, agent_b):
        if not np.all(np.isfinite(strategy)) or not np.isclose(
            strategy.sum(), 1.0, atol=tolerance, rtol=0.0
        ):
            raise ValueError("NashPy returned an invalid probability vector")
        if np.any(strategy < -tolerance) or np.any(strategy > 1.0 + tolerance):
            raise ValueError("NashPy returned a probability outside [0, 1]")

    a_pure = (
        np.allclose(agent_a, [1.0, 0.0], atol=tolerance, rtol=0.0)
        or np.allclose(agent_a, [0.0, 1.0], atol=tolerance, rtol=0.0)
    )
    b_pure = (
        np.allclose(agent_b, [1.0, 0.0], atol=tolerance, rtol=0.0)
        or np.allclose(agent_b, [0.0, 1.0], atol=tolerance, rtol=0.0)
    )
    is_pure = bool(a_pure and b_pure)
    profile = (
        [ACTIONS[int(np.argmax(agent_a))], ACTIONS[int(np.argmax(agent_b))]]
        if is_pure
        else None
    )
    return {
        "agent_a": agent_a.tolist(),
        "agent_b": agent_b.tolist(),
        "classification": "pure" if is_pure else "mixed",
        "pure_profile": profile,
    }


def support_enumeration_results(value, cost, tolerance=1e-9):
    """Return NashPy support-enumeration output and any emitted warnings.

    Boundary games can be degenerate. This finite output must not be treated
    as an exhaustive description of a continuous equilibrium correspondence.
    """
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    game = create_game(value, cost)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        equilibria = [
            _describe_equilibrium(agent_a, agent_b, tolerance)
            for agent_a, agent_b in game.support_enumeration()
        ]
    return {
        "equilibria": equilibria,
        "warnings": [f"{item.category.__name__}: {item.message}" for item in caught],
    }


def interior_mixed_research_probability(value, cost):
    """Analytical symmetric interior prediction, defined only for 0 < c < V."""
    value, cost = validate_parameters(value, cost)
    if not 0 < cost < value:
        raise ValueError("interior mixed formula requires 0 < c < V")
    return (value - cost) / value
