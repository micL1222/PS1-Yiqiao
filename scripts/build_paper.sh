#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root/paper"
if ! command -v latexmk >/dev/null 2>&1; then
  echo "BLOCKED: pdfLaTeX/latexmk is not installed; use the Overleaf ZIP import." >&2
  exit 2
fi
if ! command -v pdflatex >/dev/null 2>&1 || ! command -v bibtex >/dev/null 2>&1; then
  echo "BLOCKED: pdfLaTeX or BibTeX is missing." >&2
  exit 2
fi
mkdir -p build
if [ -f "$root/figures/ps1_teaser.pdf" ]; then
  cp "$root/figures/ps1_teaser.pdf" figures/ps1_teaser.pdf
fi
latexmk -silent -pdf -bibtex -interaction=nonstopmode -halt-on-error -file-line-error \
  -output-directory=build -jobname=PS1-v2-draft main.tex
test -s build/PS1-v2-draft.pdf
echo "Local draft: $root/paper/build/PS1-v2-draft.pdf"
