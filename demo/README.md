# Who Pays to Know? Local Interactive Prototype

This local Gradio app teaches the formal information-acquisition game implemented in `src/information_acquisition_game.py`. It is **not deployed**. The app illustrates a game-theoretic model and does not simulate or measure actual LLM or human behavior.

## Run locally

From the project root, use an installed Python 3.9 compatible with the isolated demo environment:

```sh
python3 -m venv .venv-demo
PIP_CACHE_DIR="$PWD/.venv-demo/pip-cache" .venv-demo/bin/python -m pip install -r demo/requirements.txt
.venv-demo/bin/python -m demo.app
```

The app binds to `127.0.0.1:7860` by default and uses no public share link. Set `DEMO_PORT` to use another local port. The current tested environment uses Python 3.9.6 and Gradio 4.44.1. The `huggingface_hub<1.0` constraint is required because this Gradio release imports `HfFolder`.

## Educational pathway and evidence limits

- **Audience:** Students learning introductory game theory or computational economics.
- **Interaction:** Change V and c, choose Research or Skip, inspect unilateral best responses, payoff matrices, and equilibrium output.
- **Learning goal:** Understand how a privately borne research cost can create free-riding incentives when information benefits are shared.
- **Observable future indicator:** In a later evaluation, compare whether learners identify best responses or equilibria correctly before and after using the tool.

The educational **tool exists**, but improved learning has **not been evaluated**. No demonstrated SDG 4 impact is claimed. Hugging Face deployment is pending.
