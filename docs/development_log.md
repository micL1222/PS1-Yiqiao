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

## 2026-09-20 — Scholarly integration and local paper draft

- The author's own reassessment of the earlier attention/interruption project led to the v2 costly-information game; the topic change is not attributed to peer review.
- Re-ran the existing workflow before drafting: 14 model tests, 10 demo tests, six freshly executed notebook code cells, and 16/16 project checks passed.
- Retrieved the official public PS1 Overleaf template into an ignored directory, retained its ACM class and BibTeX style, and drafted a five-section paper with Author Notes and Appendices A–E. No actual peer-review file was accessed. The accessible old-topic review is historical only; the other assigned review's status was later clarified as currently inaccessible to the author.
- Verified seven narrow literature/official-source claims, created a paper argument map, citation and claim audits, and a submission-readiness ledger.
- Built an initial six-page ACM draft whose five main sections ended by page 2. It used a visible teaser placeholder at that stage; the real vector teaser and author identity were integrated later. Workshop and field-trip confirmations, Human-Only response/reflection, public URLs, and final Overleaf compilation remain pending.
- No AI or human behavioral experiment or educational effectiveness evaluation was conducted.

## 2026-09-20 — Step 5A author context and field-trip recovery

- Filled verified individual-author identity and recovered the earlier workshop's Session B designation from the author's own v1 main.tex. Role, teammate names, and Human-Only reflection remain for author confirmation.
- Documented the author's own reason for changing from attention scheduling to a direct two-player Research/Skip game; neither peer review is credited with causing that decision. Corrected Appendix D to record one accessible old-topic review and one assigned review currently inaccessible to the author. No substantive peer-review file was accessed.
- Copied the two author-owned v1 field-trip JPEGs unchanged into paper/field_trip/, recorded source-file names and hashes, and separated visible observations from interpretations. The author subsequently confirmed photographer, visit date, both sites, and attendance. No week3 file was modified.
- Rebuilt the local paper with the approved vector teaser and both photographs. The five numbered main sections still end on page 2; final author review and Overleaf compilation remain pending.

## 2026-09-20 — Step 5B verified local release preparation

- Replaced unverified workshop title, role, and teammate placeholders in the rendered paper with factual Session B status; retained unresolved course details in `paper/MANUAL_INPUTS_REQUIRED.md`. Safely inspected author-owned v1 `main.tex`, README, and proposal title matches only. No peer-review or classmate file was opened.
- Added author-confirmed September 4 attendance and photographer metadata for both field-trip images. Public provenance now uses repository-relative paths; no reuse license for the photos is asserted.
- Polished the author's own topic-change reasoning and removed blank reviewer-response fields. Appendix D now states only the accessible v1-review and inaccessible assigned-review facts.
- Rebuilt the seven-page local PDF, visually inspected the rendered pages, and verified the five main sections end on page 2. The 24 model/demo tests, fresh notebook execution, 16/16 research checks, 13/13 paper checks, seven citations, and claim audit passed.
- GitHub CLI had no saved login, but the existing macOS Git credential authenticated to the GitHub API as `micL1222`. The personal `PS1-Yiqiao` repository had only a `main` branch, leaving `v2-information-acquisition` free. Hugging Face reported no login. No public URL was invented before publication.
- Froze the locally verified snapshot as `b986771d1e79979825cd375c8ed663994bdc67ec` and tagged it `ps1-v2-verified`. Pushed it to a new public `v2-information-acquisition` branch of the author's personal `PS1-Yiqiao` repository without force; remote v1 `main` remained at its prior commit.
- Added the actual public-repository bootstrap to the notebook, fresh-executed its six code cells locally, and pushed that notebook update separately. The GitHub notebook page and constructed Colab URL returned HTTP 200. Google's hosted runtime was not executed.
- Hugging Face CLI and Git credential lookups found no authentication. The minimal Space staging package passed source parity, app instantiation, model logic, and localhost HTTP 200; no public Space was created.

## 2026-09-20 — Hugging Face hosting-plan checks

- Hugging Face authentication was completed and confirmed as `mickeystk`, with membership in `dku-comsci-econ206-2026`. The preferred course-organization Gradio Space creation returned HTTP 402: free `cpu-basic` Gradio/Docker hosting required an organization Team or Enterprise plan. No organization Space or setting was changed.
- The author explicitly approved a public personal-namespace deployment as a fallback. The target `mickeystk/who-pays-to-know` did not previously exist. Its Gradio Space creation also returned HTTP 402: personal free `cpu-basic` Gradio/Docker hosting required PRO. No personal Space was created and no files were uploaded. These were hosting-plan restrictions, not app-code failures.
- The seven-file staging package remained byte-identical to the trusted model/demo sources, except for synchronized display-only wording that states the full project title, formal-model status, and unevaluated educational effectiveness. Offline imports, V=4/c=2 payoffs, pure and mixed equilibria, `share=False`, and local HTTP 200 passed. The verified economic model was not changed.

## 2026-09-20 — Final Static Space and personal-fork source

- The author adapted the prototype to a free HTML/CSS/JavaScript Static Space and manually uploaded the final five source files to the official course organization. Codex assisted with source preparation and verification; Codex did not perform the successful upload.
- The [public Space](https://huggingface.co/spaces/dku-comsci-econ206-2026/who-pays-to-know) reports SDK `static`, is running, and displays the V = 4, c = 2 baseline. At remote Space revision `ad074311cb3320eb525f10734c7b4de702a517f8`, the five application files copied into `deployment/huggingface-static/` matched the live source byte for byte. Extra uploaded ZIP files are not included in the personal repository source package.
- The earlier course-organization and personal Gradio attempts were blocked by plan restrictions and remain historical notes only. `deployment/huggingface/` is retained as historical staging, while `deployment/huggingface-static/` is the final source.
- The JavaScript game was compared with the trusted Python model for V = 4 and c = 0 through 5, including all payoff cells, pure equilibria, and interior mixed probabilities. No observed human/LLM behavior or educational-effectiveness study was conducted.
