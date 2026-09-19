# Evidence Status

This ledger distinguishes the author's theoretical specifications and predictions from results that require a verified run or observation. It should be updated only when actual evidence exists.

| Claim | Status | Evidence Type | Current Evidence | Next Verification Step |
| --- | --- | --- | --- | --- |
| Baseline game is defined. | Completed. | Analytical model specification. | Payoff rules and V = 4, c = 2 matrix documented in `research_model.md`. | Check implementation against the specification when code is written. |
| (R, S) and (S, R) are Nash equilibria for V = 4, c = 2. | Predicted, not yet computationally verified. | Theoretical prediction. | Manual best-response reasoning. | Verify with NashPy and preserve actual output. |
| Equilibrium changes when c crosses V. | Predicted. | Theoretical boundary expectation. | Comparison of V − c with 0 in the manual model. | Run a parameter sweep and verify boundary cases. |
| Real AI agents free-ride. | Not tested. | Planned future test; no observed LLM behavior. | None. | Define and run an LLM behavior study before making an observed claim. |
| Humans free-ride in this setting. | Not tested. | Planned future test; no observed human behavior. | None. | Design an appropriate human study before making an observed claim. |
| Hugging Face tool improves learning. | Not tested. | Planned future test; no validated educational outcome. | None. | Define learning measures and evaluate the future tool before making an outcome claim. |

No computationally verified, synthetic or simulated, observed LLM, or observed human result is available at initialization. An expected result or planned future test must never be described as an observation.
