# Project Context for Future Codex Sessions

## Identity and status

- **Course:** COMSCI/ECON 206 Computational Microeconomics, Autumn 2026 Session 1.
- **Project:** Revised PS1 v2 research proposal, developed individually.
- **Working title:** Who Pays to Know? Strategic Information Acquisition Before AI Collective Decisions.
- **Status:** Clean project initialized. The model and equilibrium statements below are theoretical. No computational or behavioral verification has been run.
- **Authorship:** The author independently developed the research question and strategic model. AI assistance is limited to implementation, debugging, project organization, drafting assistance, reproducibility checks, and technical verification after that reasoning.

## Motivation and formal baseline

This project studies who privately pays to acquire information before a collective AI decision when everyone shares the resulting benefit. The private cost and shared benefit create an incentive to free-ride.

- **Players:** Agent A and Agent B.
- **Actions:** Research (R) or Skip (S), chosen by each player.
- **Information benefit:** If at least one player researches, each receives value **V**. One research action is sufficient to provide the full benefit in this simplified baseline.
- **Private research cost:** Each researching player pays **c**. A player who skips pays no research cost.
- **No research:** If both skip, each receives 0.
- **Baseline parameters:** **V = 4**, **c = 2**.

Payoffs are ordered (Agent A, Agent B):

| Agent A \ Agent B | Research (R) | Skip (S) |
| --- | --- | --- |
| **Research (R)** | (2, 2) | (2, 4) |
| **Skip (S)** | (4, 2) | (0, 0) |

The author's **theoretical predictions**, awaiting NashPy verification, are the pure-strategy Nash equilibria **(R, S)** and **(S, R)** for the baseline. These follow from the expected incentives to skip when the other researches and to research when the other skips, given 0 < c < V.

## Working research questions

- **Economics:** How do private research costs shape strategic information acquisition and free-riding before a collective AI decision?
- **Computer Science:** Can a reproducible game-theoretic computation recover the predicted equilibria and show how equilibrium behavior changes as research costs or information value vary?
- **Behavioral Science:** Do decision-makers follow equilibrium free-riding incentives, or can bounded strategic reasoning and beliefs about others’ willingness to research produce systematic departures from the equilibrium prediction?
- **Integrated:** When information is costly but collectively valuable, when will AI agents acquire information themselves rather than free-ride on others, and how closely will computational or observed behavior match the game-theoretic prediction?

## Evidence status

Only the theoretical game definition, manual equilibrium predictions, and planned computational verification exist. There is no verified NashPy output, synthetic or simulated result, observed LLM or human behavior, or validated educational outcome. Distinguish **theoretical prediction**, **computationally verified result**, **synthetic or simulated result**, **observed LLM behavior**, **observed human behavior**, **expected result**, and **planned future test** in all future work. See `docs/evidence_status.md`.

## Planned near-term workflow

1. Implement the formal game.
2. Verify the baseline using NashPy.
3. Run a meaningful parameter modification.
4. Create a reproducible notebook.
5. Build a teaser figure.
6. Integrate verified results into the paper.
7. Build or revise a Hugging Face educational demo.

These steps are plans, not completed work.

## Constraints for future work

- Never fabricate results or citations. Separate predicted from computed, simulated, or observed results.
- Do not edit Human-Only peer reviews.
- Preserve reproducibility and keep paper, notebook, demo, and figures aligned to the same research model.
- Do not modify old PS1 v1 materials unless explicitly instructed.
- Do not treat this initialization as authorization to write the final paper or implement the game.
