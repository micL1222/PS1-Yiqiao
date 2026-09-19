# Working Research Model

This document records the author's theoretical model. It does not report computational verification or observed behavior.

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

Therefore, for **0 < c < V**, the **theoretically predicted** pure-strategy Nash equilibria are **(R, S)** and **(S, R)**. For baseline V = 4 and c = 2, these remain theoretical predictions awaiting NashPy verification.

## Theoretical boundary expectations

- If **c > V**, research is individually unattractive when the other skips, so **(S, S)** is expected to become an equilibrium.
- If **c = V**, indifference creates a boundary case requiring explicit analysis and later computational verification.
- **c < 0** is not economically meaningful under the current interpretation; later implementation should treat it as invalid input unless the model is explicitly redefined.

No NashPy computation, parameter sweep, or simulation has been run for this project.
