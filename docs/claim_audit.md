# Claim audit

Evidence categories used in the paper: FORMAL/ANALYTICAL, COMPUTATIONALLY VERIFIED, LITERATURE-SUPPORTED, PLANNED, and NOT TESTED. Historical process facts are author-provided and require final author confirmation.

| Claim | Classification | Evidence / paper language |
| --- | --- | --- |
| For V=4,c=2, (R,S) and (S,R) are pure equilibria. | COMPUTATIONALLY VERIFIED | Direct best-response enumeration and NashPy; initially theoretical predictions before the run. |
| At V=4,c=2, each player has a symmetric mixed equilibrium Research probability 0.5. | COMPUTATIONALLY VERIFIED | Saved NashPy output, subsequent analytical cross-check. |
| For 0<c<V, p(R)=1-c/V in the symmetric interior mixed equilibrium. | FORMAL/ANALYTICAL and COMPUTATIONALLY VERIFIED at c=1,2,3 with V=4 | Derivation in Appendix A and tested cases; not generalized to degenerate boundaries. |
| V=4 cost sweep returns p=0.75,0.50,0.25 at c=1,2,3; c=4 and c=5 pure sets as reported. | COMPUTATIONALLY VERIFIED | outputs/cost_sweep.csv and tests. |
| The local educational demo exists and illustrates the formal model. | COMPUTATIONALLY VERIFIED as software artifact | Ten demo tests and prior HTTP smoke check; no learner outcome. |
| Costly information before a committee vote has public-good incentive issues. | LITERATURE-SUPPORTED | Persico 2004; distinct model. |
| Bounded reasoning and higher-order beliefs may be relevant. | LITERATURE-SUPPORTED as motivation; PLANNED test here | Camerer 2004 and Zhang 2025; no parameters or behavior measured in this project. |
| Real AI agents free-ride in this setting. | NOT TESTED | The paper says no real AI behavioral data are reported. |
| Humans free-ride in this setting. | NOT TESTED | The paper says no human behavioral data are reported. |
| Bounded reasoning causes deviations in this setting. | PLANNED competing explanation, NOT TESTED | Future belief elicitation/manipulation and choice comparison are proposed. |
| The demo improves learning or mechanisms improve institutions. | NOT TESTED | Future pre/post learning task and mechanism study only. |
| One v1 review existed and second assigned review was not received. | AUTHOR-PROVIDED HISTORY; human confirmation required | Appendix D states this without reading review content or treating it as v2 feedback. |

**Result:** No observed AI behavior, human behavior, or educational-effect claim appears in the paper. Final human verification of historical facts and prose remains pending.
