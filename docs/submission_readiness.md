# Submission readiness — 2026-09-20

Research-artifact verification and final-submission readiness are separate. The local paper compiles with the approved Figure 1, author identity, author-confirmed field-trip images, and five numbered sections ending on page 2. This is a local candidate, not the authoritative Overleaf PDF.

| Requirement | Status | Evidence | Remaining action |
| --- | --- | --- | --- |
| Formal model, cost sweep, outputs, tests | COMPLETE | 24 model/demo tests, fresh six-cell notebook, 16/16 project checks | Preserve the verified snapshot. |
| Paper source, citations, claim boundaries | COMPLETE LOCALLY | 13/13 paper checks; seven documented citations; claim audit | Final author read-through and Overleaf compile. |
| Figure 1 and editable master | COMPLETE | Author-approved PDF and Draw.io source in root and paper-local figures | Inspect after Overleaf import. |
| Author Notes | COMPLETE FOR VERIFIED FACTS | Name, NetID, email, individual contribution, instructor and workshop officials, Session B | Confirm any course-required role, teammate, or acknowledgement details. |
| Field-trip photographs | COMPLETE FOR AUTHOR-CONFIRMED FACTS | Both unchanged photos; author confirms attendance, sites, September 4 date, and photographer | Author reviews captions; no reuse license is asserted. |
| Appendix B and E | COMPLETE LOCALLY | Author-supplied topic-change reasoning, verified pure and mixed model development | Author read-through. |
| Appendix D | COMPLETE FOR AVAILABLE FACTS | One accessible v1 review and another assigned review currently inaccessible; no substantive review content used | Human-Only response or instructor clarification if required. |
| Human-Only workshop/reflection | COURSE/REVIEW STATUS UNAVAILABLE | No workshop comments or reflection invented | Author completes personally if required. |
| Verified local Git commit/tag | COMPLETE AFTER FREEZE | `ps1-v2-verified` tag; use `git rev-parse` for full SHA | Preserve tag and report hash externally. |
| GitHub publication | PUBLISHED AND VERIFIED | Public `micL1222/PS1-Yiqiao` v2 branch, verified commit, tag, README, notebook, demo, outputs, paper source checked via GitHub API | Preserve v1 `main`; no force push. |
| Google Colab URL | PUBLISHED AND VERIFIED AT LINK LEVEL | GitHub notebook and Colab URL returned HTTP 200; six notebook code cells fresh-ran locally | Hosted Google Colab execution remains unverified. |
| Hugging Face Space | PUBLISHED AND RUNNING | The author manually uploaded the [Static Space in the official course organization](https://huggingface.co/spaces/dku-comsci-econ206-2026/who-pays-to-know); five source files match `deployment/huggingface-static/`, and Python/JavaScript parity passes. | Keep the source and deployed artifact aligned. |
| Code snapshot and Overleaf source ZIP | COMPLETE LOCALLY AFTER PACKAGING | `submission/` archives are local and excluded from Git | Verify ZIPs and upload only the paper ZIP to Overleaf. |
| Final Overleaf PDF and source | MANUAL OVERLEAF STEP REMAINING | Local candidate PDF only | Import paper source ZIP, compile with pdfLaTeX, inspect, download PDF and source. |
| Canvas submission | MANUAL STEP REMAINING | No submission made | Submit authoritative files after final review. |
| v1/review record preservation | COMPLETE LOCALLY | Week3 project inspected read-only; no review file opened | Author preserves private historical records. |

The Hugging Face Static Space is released. The earlier Gradio plan restrictions are historical. No behavioral experiment or educational-effectiveness evaluation has been conducted. Final Overleaf and Human-Only/course-process steps remain before submission.
