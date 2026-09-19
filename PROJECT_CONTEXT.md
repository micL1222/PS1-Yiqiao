# Project Context for Future Codex Sessions

## Identity and status

- **Course:** COMSCI/ECON 206 Computational Microeconomics, Autumn 2026 Session 1.
- **Project:** Revised PS1 v2 research proposal, developed individually.
- **Working title:** Who Pays to Know? Strategic Information Acquisition Before AI Collective Decisions.
- **Status:** Formal Python implementation, automated tests, six-case cost sweep, saved computational outputs, and a freshly executed notebook exist. The baseline equilibrium claims below were computationally verified; no behavioral verification has been run.
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

The author's initial **theoretical predictions** were the pure-strategy Nash equilibria **(R, S)** and **(S, R)** for the baseline. They follow from incentives to skip when the other researches and to research when the other skips, given 0 < c < V. Direct best-response enumeration and NashPy have now verified both. NashPy additionally returned a symmetric mixed equilibrium with A = [0.5, 0.5] and B = [0.5, 0.5] in [Research, Skip] order; an analytical calculation made after that result agrees.

## Working research questions

- **Economics:** How do private research costs shape strategic information acquisition and free-riding before a collective AI decision?
- **Computer Science:** Can a reproducible game-theoretic computation recover the predicted equilibria and show how equilibrium behavior changes as research costs or information value vary?
- **Behavioral Science:** Do decision-makers follow equilibrium free-riding incentives, or can bounded strategic reasoning and beliefs about others’ willingness to research produce systematic departures from the equilibrium prediction?
- **Integrated:** When information is costly but collectively valuable, when will AI agents acquire information themselves rather than free-ride on others, and how closely will computational or observed behavior match the game-theoretic prediction?

## Evidence status

The theoretical model, computational verification, executed notebook, and generated JSON/CSV/Markdown outputs now exist. The baseline has two verified pure equilibria and one verified interior mixed equilibrium; the discrete V = 4 cost sweep checks c = 0 through 5. There is still no synthetic or simulated agent-behavior result, observed LLM or human behavior, or validated educational outcome. Distinguish **theoretical prediction**, **computationally verified result**, **synthetic or simulated result**, **observed LLM behavior**, **observed human behavior**, **expected result**, and **planned future test** in all future work. See `docs/evidence_status.md`.

## Workflow state

1. **Completed:** Implement the formal game in `src/information_acquisition_game.py`.
2. **Completed:** Verify the baseline using NashPy and an independent pure best-response checker.
3. **Completed:** Check V = 4 at c = 0, 1, 2, 3, 4, 5.
4. **Completed:** Create and execute `notebooks/information_acquisition_baseline.ipynb`; save actual outputs in `outputs/`.
5. **Next likely stage, not started:** Design the research teaser and integrate the verified baseline into the PS1 paper.
6. **Later, not started:** Build or revise a Hugging Face educational demo.

The code uses [Research, Skip] action order. Boundary c = 0 and c = V cases are degenerate; direct enumeration lists all pure equilibria, while finite support enumeration does not establish a complete boundary mixed-equilibrium correspondence.

## Constraints for future work

- Never fabricate results or citations. Separate predicted from computed, simulated, or observed results.
- Do not edit Human-Only peer reviews.
- Preserve reproducibility and keep paper, notebook, demo, and figures aligned to the same research model.
- Do not modify old PS1 v1 materials unless explicitly instructed.
- Do not treat computational verification as authorization to write the final paper, publish an artifact, or make behavioral claims.
