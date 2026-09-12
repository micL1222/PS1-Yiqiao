---
title: Who Gets to Interrupt
emoji: 🔔
colorFrom: blue
colorTo: indigo
sdk: static
app_file: index.html
pinned: false
---

# Who Gets to Interrupt?

Interactive companion for **Reputation-Calibrated Deference in Multi-Agent AI**, a COMSCI/ECON 206 research proposal by Yiqiao Liu.

The static interface compares two transparent interruption-authority rules:

- current claim: `S = 0.5I + 0.5U`
- history calibrated: `S = (0.5I + 0.5U) × R`

It runs entirely in the browser. There are no API calls, secrets, analytics, stored responses, backend services, or build dependencies. For local inspection, open `index.html` or serve this directory with `python -m http.server`.

The included examples are authored synthetic diagnostic cases from the project data. They are not participant data, real LLM outputs, field observations, deployment evidence, or safety validation. The multiplicative rule is a proposed, inspectable heuristic—not a proven optimal, safer, or fairer policy. Yiqiao Liu selected the research direction and central model idea; AI/Codex assisted with implementation and interface construction.

To deploy after review, create a Hugging Face Space using the Static SDK and upload this directory at the Space root. Official documentation: https://huggingface.co/docs/hub/spaces-sdks-static
