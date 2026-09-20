# Evidence Status

This ledger separates the author’s initial theoretical predictions, subsequent computations, and untested behavioral claims.

| Claim | Status | Evidence Type | Current Evidence | Next Verification Step |
| --- | --- | --- | --- | --- |
| Baseline game is defined. | Completed. | Analytical model specification plus implemented matrices. | `research_model.md` and `src/information_acquisition_game.py` agree on V = 4, c = 2 and the four payoffs. | Maintain consistency if the model changes. |
| (R, S) and (S, R) are pure Nash equilibria for V = 4, c = 2. | Computationally verified. | Independent four-profile best-response enumeration plus NashPy support enumeration. | Executed tests, notebook, and `outputs/baseline_equilibria.json`; both methods return the same two pure profiles. | Re-run tests and analysis after any source change. |
| A symmetric mixed equilibrium exists for V = 4, c = 2, with p(R) = 0.5 for each agent. | Computationally verified and analytically cross-checked. | NashPy support enumeration plus subsequent indifference calculation. | Both agents’ probability vectors are [0.5, 0.5] in the generated baseline JSON and executed notebook; `1 - c/V = 0.5`. | Re-run after any model or dependency change. |
| Pure-equilibrium structure changes at and beyond c = V. | Checked on the discrete V = 4 sweep; analytical boundary reasoning retained. | Direct pure best responses plus NashPy for c = 0, 1, 2, 3, 4, 5. | At c = 4 the pure set includes (S, S); at c = 5 only (S, S) is pure. The c = 0 and c = 4 games are degenerate. | Analyze boundary mixed correspondences separately if needed. |
| Interactive formal-model demo exists. | Completed and locally verified. | Software artifact and local checks. | Gradio app instantiated, 10 demo logic tests passed, and a localhost HTTP request returned 200; `demo/` files are present. | Re-run local verification after changes; future deployment remains pending. |
| Demo demonstrates educational effectiveness. | Not tested. | No educational outcome evidence. | The educational tool exists, but no learner evaluation has been conducted. | Define and evaluate a learning indicator before making an effectiveness claim. |
| Computational cost-sweep figure depicts the verified formal output. | Generated and locally checked. | Reproducible visualization of formal-model results. | `figures/cost_sweep_mixed_probability.pdf` and PNG were generated from `outputs/cost_sweep.csv`; the PDF has no embedded raster-image object. | Re-run figure generation after CSV or plotting changes. |
| Research teaser exists as an editable Draw.io master. | Created and structurally validated. | Editable diagram artifact. | `figures/ps1_teaser.drawio` parses as XML with 14 editable shapes and 9 connectors. | Manually open and vector-export in diagrams.net; review final layout. |
| Real AI agents free-ride. | Not tested. | Planned future test; no observed LLM behavior. | None. | Define and run an LLM behavior study before making an observed claim. |
| Humans free-ride in this setting. | Not tested. | Planned future test; no observed human behavior. | None. | Design an appropriate human study before making an observed claim. |
| Hugging Face tool improves learning. | Not tested. | Planned future test; no validated educational outcome. | None. | Define learning measures and evaluate the future tool before making an outcome claim. |

The computed outcomes are formal-model equilibria. No synthetic agent-behavior result, observed LLM behavior, observed human behavior, or validated educational outcome has been produced.
