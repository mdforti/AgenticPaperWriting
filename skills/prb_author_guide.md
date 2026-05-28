# Skill: Physical Review B — Author Guide

## Overview
Physical Review B (PRB) is the American Physical Society's premier journal for condensed matter and materials physics. This guide covers preparation and submission for **Regular Articles** (no length limit), which is the appropriate article type for this manuscript.

## Manuscript Formatting

### REVTeX (Required)
- Use **REVTeX 4.2** — the APS-supported LaTeX macro package
- Document class: `\documentclass[prb,twocolumn]{revtex4-2}`
- For Regular Articles, twocolumn format is standard
- A PDF is sufficient for peer review, but REVTeX source is preferred

### Length Calculation
PRB Regular Articles have no strict length limit, but authors should be concise. Length is estimated as:
`Total = Text + Displayed Math + Figures + Tables`
- **Text:** Body text, figure/table captions, footnotes/endnotes (excludes: title, author list, abstract, references, acknowledgments, PhySH keywords)
- **Displayed math:** 16 words/row (single-column), 32 words/row (double-column)
- **Figures:** (150 / aspect_ratio + 20) words for single-column; (300 / (0.5 × aspect_ratio) + 40) for double-column
- **Tables:** 13 + 6.5×lines words (single-column); 26 + 13×lines (double-column)

### Title
- Self-contained, concise, informative
- Avoid: new terminology, quality assessments ("precise", "important"), proper nouns, newly coined words

### Author List & Affiliations
- Use `\author{}` and `\affiliation{}` commands
- For multi-institutional papers, use `\superscriptaddress` option or group by address
- Contact author: `\email{}` and `\homepage{}` available
- Contribution statements as byline footnotes or after Acknowledgments

### Abstract
- Single paragraph, < 500 words, ~5% of article length
- No displayed equations or tables
- No numbered references (spell out citations in text)
- Must be self-contained (reprinted in abstract databases)

### Sectioning
- Regular Articles use numbered sections: 1, 2, 3, ...
- Subsections: 1.1, 1.2, ... (avoid subsubsections if possible)
- Headings: `\section{}`, `\subsection{}`

### Figures
- Submitted separately (PostScript or EPS preferred)
- Online color is free; print color incurs charges
- Ensure figures are legible in both color and grayscale
- Captions should be self-contained

### Tables
- Use `\begin{table}` with `\caption{}`
- PRB prefers ruled tables (`\toprule`, `\midrule`, `\bottomrule` from `booktabs`)

### References
- Numbered consecutively in text as [1], [2], ...
- Use BibTeX with REVTeX's `\bibliographystyle{apsrev4-2}` and `\bibliography{}`
- Include DOIs where available
- Avoid broken links

## Submission Process

### Pre-Submission Checklist
1. Manuscript compiled with REVTeX 4.2, no errors
2. Figures as separate EPS/PDF files
3. Suggested referees (3–5 experts not close collaborators)
4. PhySH classification terms (https://physh.aps.org)
5. Cover letter (optional but recommended)

### Via APS Submission Server
1. Register/login at https://authors.aps.org
2. Select Physical Review B
3. Upload manuscript (PDF or REVTeX source + figure files)
4. Enter metadata (title, authors, abstract, PhySH terms)
5. Suggest referees and mention any excluded referees
6. Submit

### During Review
- Manuscript receives an APS code (e.g., AB12345)
- Status checked via https://status.aps.org
- Typical first decision: 4–8 weeks
- Rebuttal/resubmission with point-by-point response to referee comments

### After Acceptance
- Production team converts to XML
- Author proof correction (48-hour turnaround typical)
- Article published online with DOI; assigned to an issue

## Editorial Criteria (PRB)
1. **Significance:** Advances understanding of condensed matter physics
2. **Quality:** Computational methodology must be sound, properly converged, and reproducible
3. **Novelty:** New physical insight, not merely incremental results
4. **Presentation:** Clear, well-organised, proper referencing

## Open Access
- PRB is a hybrid journal (subscription + open access)
- OA options: CC-BY 4.0 license (article processing charges apply)
- See https://journals.aps.org/open-access

## Key References
- PRB author website: https://journals.aps.org/prb/authors
- REVTeX home: https://journals.aps.org/revtex
- APS Style Guide: https://journals.aps.org/files/styleguide-pr.pdf
- Web submission guidelines: https://journals.aps.org/authors/web-submission-guidelines-physical-review
