# Project Context for Future Codex Sessions

## Identity and status

- **Course:** COMSCI/ECON 206 Computational Microeconomics, Autumn 2026 Session 1.
- **Project:** Revised PS1 v2 research proposal, developed individually.
- **Working title:** Who Pays to Know? Strategic Information Acquisition Before AI Collective Decisions.
- **Status:** Step 4 scholarly integration and local ACM LaTeX draft completed: verified formal model and sweep, isolated Gradio demo, vector cost-sweep figure, editable Draw.io teaser master, citation/claim audits, five-section paper and appendices, local PDF build, and project/paper validators. Final teaser export, author inputs, publication, and Overleaf final compilation remain pending. No behavioral or educational-outcome evaluation has been run.
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
- **Computer Science:** Can a reproducible game-theoretic computation recover the predicted equilibria and show how equilibrium behavior changes as research costs vary?
- **Behavioral Science:** Do decision-makers follow equilibrium free-riding incentives, or can bounded strategic reasoning and beliefs about others’ willingness to research produce systematic departures from the equilibrium prediction?
- **Integrated:** When information is costly but collectively valuable, when will AI agents acquire information themselves rather than free-ride on others, and how closely will observed behavior match the formal game-theoretic prediction? The observed-behavior part is unanswered.

## Evidence status

The theoretical model, computational verification, executed notebook, generated JSON/CSV/Markdown outputs, local Gradio demo, vector cost-sweep figure, and editable Draw.io teaser now exist. The baseline has two verified pure equilibria and one verified interior mixed equilibrium; the discrete V = 4 cost sweep checks c = 0 through 5. The demo illustrates the formal game only. There is still no synthetic or simulated agent-behavior result, observed LLM or human behavior, or validated educational outcome. Distinguish **theoretical prediction**, **computationally verified result**, **synthetic or simulated result**, **observed LLM behavior**, **observed human behavior**, **expected result**, and **planned future test** in all future work. See `docs/evidence_status.md`.

## Workflow state

- **Completed Step 2:** Implement the formal game, independently check pure equilibria, verify NashPy baseline and c = 0 through 5 sweep, and execute the notebook.
- **Completed Step 3:** Build the local Gradio prototype in `demo/`, generate a vector cost-sweep PDF and PNG from `outputs/cost_sweep.csv`, create the editable `figures/ps1_teaser.drawio` master, add demo tests and `scripts/validate_project.py`, and run `./scripts/verify_all.sh`. The workflow passed 14 original model tests, 10 demo logic tests, fresh notebook execution, and 16/16 validator checks. A localhost HTTP smoke test returned 200 and the server was stopped.
- **Manual Step 3 follow-up:** No local Draw.io export mechanism was available. Open the master in diagrams.net, review its layout, and export `figures/ps1_teaser.pdf` as a vector PDF before using it in a paper.
- **Completed Step 4 local draft:** Retrieved the official public course template, retained ACM class/BibTeX style, verified seven sources against primary or official pages, drafted exactly five main sections and Appendices A–E, compiled a local PDF, and checked that the main text ends on page 2 with an approximately full-size visible teaser placeholder. Human-only fields and final submission items are in paper/MANUAL_INPUTS_REQUIRED.md. The old v1 review was not accessed; it is not represented as feedback on v2. Second assigned peer review: not received.

The code uses [Research, Skip] action order. Boundary c = 0 and c = V cases are degenerate; direct enumeration lists all pure equilibria, while finite support enumeration does not establish a complete boundary mixed-equilibrium correspondence. The app has not been deployed, and educational effectiveness has not been evaluated.

## Future stages — not begun

1. Author review and completion of Human-Only, identity, workshop, and field-trip inputs; manual vector teaser export.
2. Publication of GitHub and Google Colab artifacts.
3. Hugging Face deployment.
4. Final Overleaf compilation, two-page visual check, source ZIP, and cross-artifact submission audit.

## Constraints for future work

- Never fabricate results or citations. Separate predicted from computed, simulated, or observed results.
- Do not edit Human-Only peer reviews.
- Preserve reproducibility and keep paper, notebook, demo, and figures aligned to the same research model.
- Do not modify old PS1 v1 materials unless explicitly instructed.
- Paper drafting was explicitly authorized for Step 4; publication, deployment, and behavioral claims remain separate future work.
