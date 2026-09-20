# Import the PS1 v2 draft into Overleaf

The final submission PDF is compiled and visually checked in Overleaf. This repository creates a local pre-Overleaf draft only. Complete the blocking items in MANUAL_INPUTS_REQUIRED.md before final submission.

1. Confirm the author-approved vector PDF in figures/ps1_teaser.pdf matches paper/figures/ps1_teaser.pdf, and keep the matching editable .drawio master in paper/figures/.
2. From the project root, run ./scripts/verify_all.sh. Resolve any failure. Run ./scripts/build_paper.sh and confirm Figure 1 appears and the main sections end by page 2.
3. Review unresolved workshop and Human-Only requirements in `MANUAL_INPUTS_REQUIRED.md`, along with any publication status. Author identity, field-trip metadata, and Figure 1 are filled. Check citations and claims yourself.
4. Zip **the contents of paper/**, excluding paper/build/, .gitkeep, and local temporary files, so main.tex is at the ZIP root. For example, from the project root: cd paper && zip -r build/PS1-v2-overleaf-source.zip main.tex references.bib acmart.cls ACM-Reference-Format.bst sections appendices figures field_trip. The build/ directory is local and excluded from the ZIP.
5. In Overleaf, choose **New Project → Upload Project**, then upload that ZIP. No account or project is created by this local work.
6. Set **Main Document** to main.tex and **Compiler** to **pdfLaTeX**. Compile. Recompile once more if citations need a BibTeX refresh.
7. Confirm every citation resolves in the reference list. Check Figure 1's vector sharpness, caption, and accessibility description.
8. Check that the title, metadata, Figure 1, and all five numbered main sections fit by the end of page 2. References, Author Notes, and appendices may continue afterward. Verify the complete PDF visually and confirm no clipped tables or unfilled placeholders.
9. Use Overleaf's **Download PDF** action for the final PDF. Use **Download → Source** for the final Overleaf source ZIP. Preserve both for Canvas submission.

If Overleaf's TeX Live version differs, address actual compile errors without changing the required ACM class format or silently dropping content. A GitHub sync route is optional and has not been configured.
