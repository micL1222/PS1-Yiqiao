# Research Development Log

## 2026-09-20 — PS1 v2 initialization

- Previous PS1 direction is being replaced by a strategic information-acquisition direction in this new project.
- New project created separately to preserve v1.
- Two-player Research/Skip baseline formalized from the author's research idea.
- No computational verification has yet been run.
- Next task: NashPy implementation and verification, subject to a separate instruction.

## 2026-09-20 — Computational baseline implementation and verification

- Added the formal Python game, an independent pure best-response checker, NashPy support enumeration, and strict-interior analytical mixed-probability calculation.
- Ran automated tests and verified the V = 4, c = 2 payoff matrices and initially predicted pure equilibria.
- NashPy additionally identified the symmetric mixed equilibrium A = [0.5, 0.5], B = [0.5, 0.5]; the subsequent analytical calculation agreed. The initial reasoning had identified the two pure equilibria only.
- Ran the V = 4 cost sweep for c = 0 through 5, checking every pure-equilibrium set against NashPy and the interior mixed cases against the analytical formula.
- Executed the notebook from a fresh process and saved actual JSON, CSV, and Markdown outputs.
- Boundary c = 0 and c = V cases are degenerate; no exhaustive mixed-boundary claim is made.
- Real AI behavior, human behavior, and educational outcomes remain untested. Next likely stage is the research teaser and integration of verified results into the PS1 paper; that stage has not begun.

## 2026-09-20 — Local artifact integration

- Kept the original payoff model and 14 baseline tests semantically unchanged; re-running Step 2 generated identical baseline JSON, CSV, and summary bytes before new work.
- Built a local Gradio 4.44.1 prototype in an isolated Python 3.9.6 `.venv-demo`. A `huggingface_hub<1.0` constraint resolved an import incompatibility. Ten demo logic tests, app instantiation, and a localhost HTTP 200 smoke test passed; the server was terminated and no public share link was used.
- Generated the vector cost-sweep PDF and PNG from the actual `outputs/cost_sweep.csv` interior points only. The PDF was rendered and visually checked; no raster-image object was embedded.
- Created the editable Draw.io teaser master, caption, and accessibility description. The XML contains 14 editable shapes and 9 connectors and passed structural validation. No local Draw.io export mechanism was found, so the optional teaser PDF awaits manual vector export.
- Added the project-wide consistency validator and `./scripts/verify_all.sh`. The full workflow passed the 14 original tests, 10 demo tests, fresh six-cell notebook execution, and 16/16 objective validator checks.
- Formal-model computations are distinct from real AI or human observations. No behavioral experiment or educational effectiveness evaluation was conducted.
