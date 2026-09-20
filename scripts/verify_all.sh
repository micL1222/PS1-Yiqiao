#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

export MPLCONFIGDIR="$PWD/.venv/matplotlib"
export XDG_CACHE_HOME="$PWD/.venv/cache"
export GRADIO_ANALYTICS_ENABLED=False

.venv/bin/python -m unittest discover -s tests -p 'test_information_acquisition_game.py' -v
if [ -d demo ]; then
  .venv-demo/bin/python -m unittest discover -s tests -p 'test_demo_logic.py' -v
  .venv-demo/bin/python -c 'from demo.app import build_app; assert len(build_app().get_config_file()["dependencies"]) == 2; print("Gradio app instantiation: PASS")'
fi
.venv/bin/python -m src.run_baseline_analysis
.venv/bin/python scripts/generate_cost_sweep_figure.py
mkdir -p .venv/verification
PATH="$PWD/.venv/bin:$PATH" JUPYTER_CONFIG_DIR="$PWD/.venv/jupyter_config" JUPYTER_DATA_DIR="$PWD/.venv/jupyter_data" IPYTHONDIR="$PWD/.venv/ipython" .venv/bin/jupyter nbconvert --to notebook --execute notebooks/information_acquisition_baseline.ipynb --output information_acquisition_baseline_verified.ipynb --output-dir .venv/verification
.venv/bin/python - <<'PY'
import json
from pathlib import Path
notebook=json.loads(Path('.venv/verification/information_acquisition_baseline_verified.ipynb').read_text())
code=[cell for cell in notebook['cells'] if cell['cell_type']=='code']
assert code and all(cell.get('execution_count') is not None for cell in code)
assert not any(out['output_type']=='error' for cell in code for out in cell.get('outputs',[]))
print(f'Fresh notebook execution: PASS ({len(code)} code cells)')
PY
.venv/bin/python scripts/validate_project.py
