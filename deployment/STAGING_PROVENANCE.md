# Staging provenance

`demo/app.py`, `demo/demo_logic.py`, `src/information_acquisition_game.py`, and `src/run_baseline_analysis.py` are byte-for-byte copies of their same-named paths in the project root. `requirements.txt` is a copy of `demo/requirements.txt`. The root `app.py` only creates and launches the verified Gradio interface with `share=False`.

Before deployment, compare each copy with its root source using `cmp`, run the demo tests from this directory, and perform a localhost HTTP smoke test. This package is not a separate economic model.
