"""Structural and evidence-boundary checks for the PS1 v2 LaTeX draft."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
MAIN = PAPER / "main.tex"
SECTION_FILES = [
    ("section1_questions.tex", "Three Connected Research Questions"),
    ("section2_economics.tex", "Answer to Q1: Incentives and Intellectual Lineage"),
    ("section3_computation.tex", "Answer to Q2: Method and Evaluation"),
    ("section4_behavior.tex", "Answer to Q3: Behavior and Competing Explanations"),
    ("section5_future.tex", "Advanced Development and Future Directions"),
]
APPENDICES = [
    "appendix_a_technical.tex", "appendix_a1_ai_use.tex",
    "appendix_b_development.tex", "appendix_c_field_trip.tex",
    "appendix_d_review_revision.tex", "appendix_e_structured_abstract.tex",
]
ABSTRACT_ROWS = [
    "Background", "Motivation and application", "Three connected questions",
    "Method and model assumptions", "Results or expected results",
    "Intellectual merits", "Practical impacts", "Feedback received and revision made",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"Missing: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def all_tex() -> str:
    files = [MAIN]
    files += [PAPER / "sections" / name for name, _ in SECTION_FILES]
    files += [PAPER / "appendices" / name for name in APPENDICES]
    return "\n".join(read(p) for p in files)


def check_template() -> None:
    for name in ("acmart.cls", "ACM-Reference-Format.bst"):
        require((PAPER / name).is_file(), f"Template file missing: {name}")
    main = read(MAIN)
    require(r"\documentclass[sigconf,nonacm]{acmart}" in main, "Official ACM class options changed")
    require(r"\bibliographystyle{ACM-Reference-Format}" in main, "Template BibTeX style missing")


def check_sections() -> None:
    main = read(MAIN)
    for name, title in SECTION_FILES:
        body = read(PAPER / "sections" / name)
        require(re.findall(r"\\section\{([^}]+)\}", body) == [title], f"Wrong section title: {name}")
        require(r"\input{sections/" + name[:-4] + "}" in main, f"Section not included: {name}")
    require(not re.search(r"\\section\{", main.split(r"\appendix")[0]), "Unexpected numbered main section")


def check_figure() -> None:
    main = read(MAIN)
    require(r"\begin{teaserfigure}" in main and r"\label{fig:teaser}" in main, "Figure 1 missing")
    require(r"\ref{fig:teaser}" in read(PAPER / "sections/section1_questions.tex"), "Figure 1 reference missing")
    require(r"\Description{" in main and r"\caption{" in main, "Caption/Description missing")
    require(r"\includegraphics[width=\textwidth]{figures/ps1_teaser.pdf}" in main, "Real Figure 1 include missing")
    require("Figure 1 vector PDF pending manual Draw.io export." not in main, "Teaser placeholder remains")
    for rel in ("figures/ps1_teaser.drawio", "figures/ps1_teaser.pdf", "paper/figures/ps1_teaser.drawio", "paper/figures/cost_sweep_mixed_probability.pdf"):
        require((ROOT / rel).is_file(), f"Figure artifact missing: {rel}")


def check_metadata() -> None:
    main = read(MAIN)
    for value in ("COMSCI/ECON 206", "Computational Microeconomics", "Autumn 2026 Session 1", "Luyao Zhang", "Yiqiao Liu (Mickey)", "yl1081@duke.edu", "NetID:} yl1081", "Session B"):
        require(value in main, f"Metadata missing: {value}")
    for placeholder in ("[AUTHOR NAME]", "[NETID]", "[EMAIL]", "[SESSION]"):
        require(placeholder not in main, f"Resolved metadata placeholder remains: {placeholder}")


def check_citations() -> None:
    require(r"\bibliography{references}" in read(MAIN), "Bibliography missing")
    keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", read(PAPER / "references.bib")))
    cites = {
        key.strip()
        for field in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", all_tex())
        for key in field.split(",")
    }
    require(keys == cites, f"Bibliography mismatch: bib-only={keys-cites}; missing={cites-keys}")
    literature = read(ROOT / "docs/literature_verified.md")
    audit = read(ROOT / "docs/citation_audit.md")
    for key in keys:
        require(key in literature and key in audit, f"Unaudited citation: {key}")
    print(f"Citation audit: PASS ({len(keys)}/{len(cites)} matched and documented)")


def check_statements() -> None:
    section5 = read(PAPER / "sections/section5_future.tex")
    for phrase in ("Open Science Statement", "public GitHub v2 branch", "Google Colab notebook", "b986771", "Statement of Contribution to the UN's SDGs", "Hugging Face Static Space", "Educational effectiveness has not been evaluated.", "SDG 4", "By 2056, I aspire to"):
        require(phrase in section5, f"Statement missing: {phrase}")
    for url in (
        "https://github.com/micL1222/PS1-Yiqiao/tree/v2-information-acquisition",
        "https://colab.research.google.com/github/micL1222/PS1-Yiqiao/blob/v2-information-acquisition/notebooks/information_acquisition_baseline.ipynb",
        "https://github.com/micL1222/PS1-Yiqiao/commit/b986771d1e79979825cd375c8ed663994bdc67ec",
        "https://huggingface.co/spaces/dku-comsci-econ206-2026/who-pays-to-know",
    ):
        require(url in section5, f"Verified public URL missing: {url}")
    for stale in ("[pending publication]", "[pending deployment]", "awaits authentication", "not yet available", "Hugging Face unavailable", "PLACEHOLDER", "TBD"):
        require(stale not in all_tex(), f"Obsolete publication placeholder remains: {stale}")


def check_claims() -> None:
    tex = all_tex()
    require("No real AI or human behavioral data are reported in PS1." in tex, "Behavioral non-result missing")
    require("Educational effectiveness has not been evaluated." in tex, "Learning non-result missing")
    require("No real LLM or human choices" in tex, "Technical evidence limit missing")
    require("not empirical frequencies" in tex, "Cost figure evidence label missing")
    audit = read(ROOT / "docs/claim_audit.md")
    for phrase in ("FORMAL/ANALYTICAL", "COMPUTATIONALLY VERIFIED", "LITERATURE-SUPPORTED", "PLANNED", "NOT TESTED", "Real AI agents free-ride", "Humans free-ride", "The demo improves learning"):
        require(phrase in audit, f"Claim-audit item missing: {phrase}")
    print("Claim audit: PASS (formal, computed, literature, planned, and untested separated)")


def check_author_notes() -> None:
    main = read(MAIN)
    for phrase in ("Author Notes", "Acknowledgements", "Individual Contribution", "Codex is not a coauthor", "Human verification of this draft is pending"):
        require(phrase in main, f"Author Notes missing: {phrase}")


def check_appendices() -> None:
    main = read(MAIN)
    require(r"\appendix" in main, "Appendix switch missing")
    for name in APPENDICES:
        require(r"\input{appendices/" + name[:-4] + "}" in main, f"Appendix not included: {name}")
        read(PAPER / "appendices" / name)
    require(r"\subsection{AI-Use Disclosure}" in read(PAPER / "appendices/appendix_a1_ai_use.tex"), "A.1 AI disclosure missing")
    for name in APPENDICES:
        if name != "appendix_a1_ai_use.tex":
            require(len(re.findall(r"\\section\{", read(PAPER / "appendices" / name))) == 1, f"Appendix section missing: {name}")
    field = read(PAPER / "appendices/appendix_c_field_trip.tex")
    for name in ("tencent_shanghai_office.jpg", "shanghai_science_technology_museum.jpg"):
        require((PAPER / "field_trip" / name).is_file(), f"Field-trip photo missing: {name}")
        require(name in field, f"Field-trip photo not included: {name}")


def check_review() -> None:
    review = read(PAPER / "appendices/appendix_d_review_revision.tex")
    for phrase in ("One accessible peer review concerns that earlier topic", "One assigned peer review is currently inaccessible to the author.", "Its substantive content has not been incorporated into this v2 revision.", "not treated as direct evaluation of the v2", "author's own research decision", "Review-process status", "Major revision decision", "Objective v1-to-v2 revision record", "Response status", "no substantive response to unavailable content is claimed"):
        require(phrase in review, f"Review boundary missing: {phrase}")
    require("not received" not in review.lower(), "Unsupported peer-review status remains")


def check_abstract() -> None:
    body = read(PAPER / "appendices/appendix_e_structured_abstract.tex")
    rows = [line.split(" &", 1)[0] for line in body.splitlines() if " &" in line]
    rows = [row for row in rows if row in ABSTRACT_ROWS]
    require(rows == ABSTRACT_ROWS, f"Appendix E requires exactly eight ordered rows: {rows}")


def check_guidance() -> None:
    for name in ("TEMPLATE_PROVENANCE.md", "MANUAL_INPUTS_REQUIRED.md", "OVERLEAF_IMPORT_INSTRUCTIONS.md", "field_trip/PROVENANCE.md"):
        read(PAPER / name)
    manual = read(PAPER / "MANUAL_INPUTS_REQUIRED.md")
    require("BLOCKING" in manual and "NON-BLOCKING" in manual, "Manual checklists incomplete")
    require("Research-artifact verification" in read(ROOT / "docs/submission_readiness.md"), "Readiness distinction missing")


def check_pdf() -> None:
    pdf = PAPER / "build/PS1-v2-draft.pdf"
    aux = PAPER / "build/PS1-v2-draft.aux"
    require(pdf.is_file() and pdf.stat().st_size > 10000, "Local draft PDF missing or small")
    require(pdf.read_bytes().startswith(b"%PDF-"), "Local draft is not PDF")
    require((PAPER / "figures/ps1_teaser.pdf").read_bytes() == (ROOT / "figures/ps1_teaser.pdf").read_bytes(), "Compiled paper teaser differs from approved PDF")
    match = re.search(r"\\newlabel\{main:end\}\{\{5\}\{(\d+)\}", read(aux))
    require(match is not None and int(match.group(1)) <= 2, "Main text extends beyond page 2")
    log = read(PAPER / "build/PS1-v2-draft.log")
    require("undefined on input line" not in log and "undefined references" not in log, "Unresolved citation/reference")
    newest = max(p.stat().st_mtime for p in [MAIN, ROOT / "figures/ps1_teaser.pdf"] + list((PAPER / "sections").glob("*.tex")) + list((PAPER / "appendices").glob("*.tex")))
    require(pdf.stat().st_mtime >= newest, "Draft PDF predates source")
    try:
        result = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True)
        pages = re.search(r"^Pages:\s+(\d+)", result.stdout, re.M)
        print(f"Local PDF: PASS ({pages.group(1) if pages else 'unknown'} pages; main ends on page {match.group(1)})")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"Local PDF: PASS (main ends on page {match.group(1)})")


CHECKS = [
    ("Official template files and class", check_template),
    ("Exactly five titled main sections", check_sections),
    ("Figure 1, Draw.io, and accessibility", check_figure),
    ("Course and placeholder metadata", check_metadata),
    ("Bibliography and citation audit", check_citations),
    ("Open science, SDG 4, and 2056", check_statements),
    ("Behavioral and learning evidence limits", check_claims),
    ("Author Notes and contribution", check_author_notes),
    ("Appendices A, A.1, B, C, D, E", check_appendices),
    ("Historical-review boundary", check_review),
    ("Eight Appendix E rows", check_abstract),
    ("Manual-input and provenance documents", check_guidance),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-pdf", action="store_true")
    args = parser.parse_args()
    checks = CHECKS + ([("Local PDF and two-page main paper", check_pdf)] if args.check_pdf else [])
    failures = 0
    for name, check in checks:
        try:
            check()
            print(f"PASS {name}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {name}: {exc}")
    print(f"Paper validator: {len(checks)-failures}/{len(checks)} checks passed")
    teaser = ROOT / "figures/ps1_teaser.pdf"
    print("Final teaser PDF: READY" if teaser.is_file() else "Final teaser PDF: BLOCKING manual export remains")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
