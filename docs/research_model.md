# Working Research Model

This document preserves the author's initial theoretical model and records subsequent computational verification separately. It does not report observed behavior.

## Players, actions, and parameters

- Players: **i ∈ {A, B}**.
- Actions: **aᵢ ∈ {R, S}**, where R = Research and S = Skip.
- **V** is the value to each player of having useful information.
- **c** is the private research cost paid by each player who researches.
- Baseline: **V = 4**, **c = 2**.

If at least one player researches, both obtain the full information benefit V. The researching player pays c, giving that player **uᵢ = V − c**. A player who skips while the other researches receives **uᵢ = V**. If both skip, each receives **uᵢ = 0**. The simplified baseline assumes that one research action is sufficient to create the full information benefit; this assumption may later be modified.

## Baseline payoff matrix

Payoffs are ordered (Agent A, Agent B):

| Agent A \ Agent B | Research (R) | Skip (S) |
| --- | --- | --- |
| **Research (R)** | (2, 2) | (2, 4) |
| **Skip (S)** | (4, 2) | (0, 0) |

## Theoretical best-response reasoning

If the other agent researches, Skip yields V while Research yields V − c. Thus, for **c > 0**, Skip is preferred. If the other agent skips, Research yields V − c while Skip yields 0. Thus, for **0 < c < V**, Research is preferred.

Therefore, for **0 < c < V**, the author initially **theoretically predicted** the pure-strategy Nash equilibria **(R, S)** and **(S, R)**. For baseline V = 4 and c = 2, these were the initial verification targets; the results of the later code run are recorded below.

## Theoretical boundary expectations

- If **c > V**, research is individually unattractive when the other skips, so **(S, S)** is expected to become an equilibrium.
- If **c = V**, indifference creates a boundary case. The later discrete computational check is recorded below; its finite support-enumeration output does not characterize every possible mixed profile.
- **c < 0** is not economically meaningful under the current interpretation; later implementation should treat it as invalid input unless the model is explicitly redefined.

## Computational Verification

The implemented matrices for V = 4, c = 2 are Agent A `[[2, 2], [4, 0]]` and Agent B `[[2, 4], [2, 0]]`. The independent four-profile best-response checker and NashPy support enumeration both returned the author's initially predicted **pure** equilibria (R, S) and (S, R).

NashPy also returned a **mixed** equilibrium with Agent A = [0.5, 0.5] and Agent B = [0.5, 0.5], in [Research, Skip] order. The initial reasoning had identified only the two pure equilibria. After the NashPy result, let p be the other agent’s probability of Research. Research gives V - c, while Skip gives pV. Indifference gives `p(Research) = (V - c)/V = 1 - c/V = 0.5`, agreeing with the returned probabilities. This formula applies for 0 < c < V and does not fully characterize degenerate boundaries.

With V = 4 fixed, the computational sweep checked c = 0, 1, 2, 3, 4, 5. The two methods agreed on every **pure** equilibrium set. The interior mixed probabilities were 0.75, 0.5, and 0.25 for c = 1, 2, and 3, respectively, and agreed with the formula. At c = 0 the pure equilibria are (R, R), (R, S), (S, R); at c = V = 4 they are (R, S), (S, R), (S, S); at c = 5 only (S, S) is pure. Boundary support-enumeration output is finite and is not a complete claim about any mixed-equilibrium continuum. See `../outputs/verification_summary.md` and the machine-readable outputs for the executed results.

These formal equilibrium calculations provide no observed LLM or human behavior evidence.
