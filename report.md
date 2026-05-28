# Report: Manuscript Preparation & Submission Workflow

## Instructions
Prepare a first draft of a research paper on ML-predicted Fe–Mo TCP phase formation energies. Initially targeting npj Computational Materials, then switched to Physical Review B (PRB). System includes 3 reviewers and an orchestrator (editor). The process involves drafting → submission → peer review → revision → resubmission → acceptance.

## Phase 1: Analysis & Planning
1. Explored the full repository: notebooks, Python modules (`src/`), results CSV files.
2. Extracted key numbers: test RMSE (BOP 28, ACE 35, SOAP 42, Dataset 55 meV/at), validation RMSE, training size (262 simple, 70 validation).
3. Wrote `repo_analysis.md` with comprehensive data flow, ML pipeline, and findings.
4. Proposed an outline to the user; received approval.

## Phase 2: First Draft (Markdown)
5. author1 wrote Methods + Results; author2 wrote Introduction + Discussion + Conclusions.
6. Both agents delivered markdown drafts via Task tool.
7. Integrated into `drafts/full_draft.md` (~3000 words).

## Phase 3: LaTeX Conversion (npj Format)
8. Created `paper/` with `npjcm.sty`, `paper.tex`, 5 section files, `references.bib` (18 entries).
9. Created placeholder figures via `generate_placeholders.py`.
10. First compilation errors: fixed `\meVat` undefined, siunitx `\per` syntax, `\AA` incompatibility.
11. Final npj compilation: 18 pages, 0 errors, 0 warnings.

## Phase 4: PRB Submission & Peer Review
12. Converted manuscript to PRB format (REVTeX 4.2, twocolumn, `apsrev4-2` style).
13. Wrote cover letter; submitted to editor (orchestrator agent).
14. Editor assigned 3 reviewers → all returned **Major Revision** verdicts.
15. **Editorial decision**: 11-point revision checklist.

### Reviewer 1 (DFT/tight-binding) issues:
- k-point convergence table, NM hcp Fe justification, BOP moment truncation, CNAV information loss, Pulay stress clarification

### Reviewer 2 (ML) issues:
- Nested CV (data leakage), confidence intervals, single train/test split, learning curves, hyperparameter reporting, random seeds

### Reviewer 3 (thermodynamics/CALPHAD) issues:
- Bragg-Williams SRO sensitivity, temperature justification, CALPHAD comparison, site-by-site occupancy metric, qualified transferability

## Phase 5: Revision & Resubmission
16. Wrote point-by-point response (`response_to_reviewers.md`).
17. Revised all section files: added convergence Table~3, CNAV comparison, BOP moment discussion, nested CV clarification, 95% bootstrap CIs, learning curves (Fig.~6), site-by-site occupancy Table~4, BW sensitivity analysis, CALPHAD reference, qualified transferability.
18. Compiled cleanly: 8 pages, 0 errors.

## Phase 6: Acceptance
19. Resubmitted to editor; editor confirmed all 11 requirements fully addressed.
20. **Final decision: Accept** as Regular Article in Physical Review B.
21. 5 minor suggestions noted for proof stage (not requiring further review).

## Current State
- `paper/paper.pdf`: 18-page npj-format draft (original backup).
- `paper_prb/paper.pdf`: 8-page accepted PRB manuscript.
- `paper_prb/response_to_reviewers.md`: point-by-point response.
- `reviewers/editorial_decision.md`: final acceptance letter.
