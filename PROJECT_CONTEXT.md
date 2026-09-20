# Project Context for Future Codex Sessions

## Identity and status

- **Course:** COMSCI/ECON 206 Computational Microeconomics, Autumn 2026 Session 1.
- **Project:** Revised PS1 v2 research proposal, developed individually.
- **Working title:** Who Pays to Know? Strategic Information Acquisition Before AI Collective Decisions.
- **Status:** Formal model, sweep, approved Figure 1, author-confirmed field-trip metadata, five-section ACM paper, appendices, local PDF build, and validators are complete locally. The verified snapshot is public on the separate `v2-information-acquisition` branch of `micL1222/PS1-Yiqiao`; the Colab link is available, although hosted Colab execution is unverified. The author manually deployed the final [Hugging Face Static Space](https://huggingface.co/spaces/dku-comsci-econ206-2026/who-pays-to-know) to the official course organization; it is public and running. Final Overleaf compilation and Human-Only/course-process work remain. No behavioral or educational-outcome evaluation has been run.
- **Authorship:** The author supplied the original reassessment, strategic idea, model decisions, and interpretation. OpenAI Codex provided substantial implementation, debugging, artifact construction, drafting, source checking, and verification assistance. The author retains final responsibility.

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

The theoretical model, computational verification, executed notebook, generated JSON/CSV/Markdown outputs, public Static Space, historical local Gradio demo, vector cost-sweep figure, and editable Draw.io teaser now exist. The baseline has two verified pure equilibria and one verified interior mixed equilibrium; the discrete V = 4 cost sweep checks c = 0 through 5. The Static Space illustrates the formal game only, and its JavaScript model is checked against the trusted Python model by `scripts/validate_static_space.py`. There is still no synthetic or simulated agent-behavior result, observed LLM or human behavior, or validated educational outcome. Distinguish **theoretical prediction**, **computationally verified result**, **synthetic or simulated result**, **observed LLM behavior**, **observed human behavior**, **expected result**, and **planned future test** in all future work. See `docs/evidence_status.md`.

## Workflow state

- **Completed Step 2:** Implement the formal game, independently check pure equilibria, verify NashPy baseline and c = 0 through 5 sweep, and execute the notebook.
- **Completed Step 3:** Build the local Gradio prototype in `demo/`, generate a vector cost-sweep PDF and PNG from `outputs/cost_sweep.csv`, create the editable `figures/ps1_teaser.drawio` master, add demo tests and `scripts/validate_project.py`, and run `./scripts/verify_all.sh`. The workflow passed 14 original model tests, 10 demo logic tests, fresh notebook execution, and 16/16 validator checks. A localhost HTTP smoke test returned 200 and the server was stopped.
- **Resolved Figure 1 follow-up:** The author reviewed the Draw.io master and exported `figures/ps1_teaser.pdf` as a vector PDF. The real figure is integrated into the local paper, whose five main sections still end on page 2.
- **Completed Step 4 local draft:** Retrieved the official public course template, retained ACM class/BibTeX style, verified seven sources against primary or official pages, and drafted exactly five main sections and Appendices A–E. No peer-review file was accessed or represented as direct feedback on v2.
- **Step 5A/5B local context:** The author supplied verified individual identity and the reason for changing topics. Session B was recovered from the author's own v1 `main.tex`; title, role, and teammate names remain unverified and omitted from the paper. The author confirmed September 4 attendance at both field-trip sites and personally taking both copied photographs. No week3 file was changed. One accessible review concerns v1 only; another assigned review is inaccessible, and neither review's substantive file was accessed. Remaining Human-Only inputs are in `paper/MANUAL_INPUTS_REQUIRED.md`.

The code uses [Research, Skip] action order. Boundary c = 0 and c = V cases are degenerate; direct enumeration lists all pure equilibria, while finite support enumeration does not establish a complete boundary mixed-equilibrium correspondence. The Static Space is deployed; educational effectiveness has not been evaluated.

## Remaining stages

1. Author review and completion of remaining Human-Only and workshop details, if required.
2. Keep the public v2 GitHub branch and Colab notebook consistent with the verified artifact tag; do not rewrite v1 `main`.
3. Keep `deployment/huggingface-static/` aligned with the manually deployed Static Space. `deployment/huggingface/` records an unsuccessful historical Gradio approach.
4. Final Overleaf compilation, visual check, source ZIP, and cross-artifact submission audit.

## Constraints for future work

- Never fabricate results or citations. Separate predicted from computed, simulated, or observed results.
- Do not edit Human-Only peer reviews.
- Preserve reproducibility and keep paper, notebook, demo, and figures aligned to the same research model.
- Do not modify old PS1 v1 materials unless explicitly instructed.
- Publication and deployment were authorized for Step 5B when authenticated access is available. Do not invent URLs or observed behavior.
