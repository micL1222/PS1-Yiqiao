# Import the PS1 v2 draft into Overleaf

The final submission PDF is compiled and visually checked in Overleaf. This repository creates a local pre-Overleaf draft only. Complete the blocking items in MANUAL_INPUTS_REQUIRED.md before final submission.

1. Open figures/ps1_teaser.drawio in diagrams.net, review it, and export a **vector PDF** named figures/ps1_teaser.pdf. Place the same PDF in paper/figures/ps1_teaser.pdf; the local build script copies it there automatically when run. Keep the editable .drawio master in paper/figures/.
2. From the project root, run ./scripts/verify_all.sh. Resolve any failure. Run ./scripts/build_paper.sh and confirm the final Figure 1 appears, not the visible placeholder. Recheck that the main sections end by page 2 with the actual export.
3. Review all manual placeholders and complete the required author, workshop, Human-Only, field-trip, and publication fields. Check citations and claims yourself.
4. Zip **the contents of paper/**, excluding paper/build/, .gitkeep, and local temporary files, so main.tex is at the ZIP root. For example, from the project root: cd paper && zip -r build/PS1-v2-overleaf-source.zip main.tex references.bib acmart.cls ACM-Reference-Format.bst sections appendices figures field_trip. The build/ directory is local and excluded from the ZIP.
5. In Overleaf, choose **New Project → Upload Project**, then upload that ZIP. No account or project is created by this local work.
6. Set **Main Document** to main.tex and **Compiler** to **pdfLaTeX**. Compile. Recompile once more if citations need a BibTeX refresh.
7. Confirm every citation resolves in the reference list. Check Figure 1's vector sharpness, caption, and accessibility description. There must be no “pending manual Draw.io export” box.
8. Check the title, metadata, Figure 1, all five numbered sections, and the contribution statements end by page 2. References, Author Notes, and appendices may continue afterward. Verify the complete PDF visually and confirm no clipped tables or unfilled placeholders.
9. Use Overleaf's **Download PDF** action for the final PDF. Use **Download → Source** for the final Overleaf source ZIP. Preserve both for Canvas submission.

If Overleaf's TeX Live version differs, address actual compile errors without changing the required ACM class format or silently dropping content. A GitHub sync route is optional and has not been configured.
