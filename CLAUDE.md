# Paper Writing Lab — Instructions for Claude Code

## Project Overview

Agent-based system for collaborative scientific paper writing and simulated journal submission/peer-review. Based on the MLFeMoTCPs repository (Fe–Mo TCP phase formation energy prediction). Targets Physical Review B.

## Directory Layout

| Path | Description |
|------|-------------|
| `agents/` | Agent definitions (orchestrator, author1, author2) |
| `reviewers/` | Reviewer agent definitions + generated feedback files |
| `skills/` | Domain skills (PRB Author Guide) |
| `paper/` | Original npj-format LaTeX manuscript (18 pages) |
| `paper_prb/` | PRB-format REVTeX 4.2 manuscript (8 pages, accepted) |
| `drafts/` | Markdown draft sections |
| `MLFeMoTCPs/` | Source ML repository (notebooks, data, pipeline) |

## Agents

### Orchestrator (editor) — `agents/orchestrator.md`
Coordinator. Manages: outline → author assignment → draft review → LaTeX integration → compilation → submission to PRB → revision management.

### Author 1 — `agents/author1.md`
Lead author (Mariano Forti). ML pipeline, descriptors (BOP/ACE/SOAP), CNAV, VotingRegressor ensemble. Writes Methods + Results in LaTeX.

### Author 2 — `agents/author2.md`
Advisor (Hammerschmidt/Drautz). TCP phase thermodynamics, BOP theory. Writes Introduction + Discussion + Conclusions + Abstract in LaTeX.

### Reviewer 1 — `reviewers/reviewer1.md`
DFT/tight-binding expert. Checks: k-point convergence, EOS fitting, reference states, BOP moments, CNAV physics, Pulay stress.

### Reviewer 2 — `reviewers/reviewer2.md`
ML methods expert. Checks: nested CV, confidence intervals, split robustness, learning curves, hyperparameters, random seeds.

### Reviewer 3 — `reviewers/reviewer3.md`
CALPHAD/thermodynamics expert. Checks: Bragg-Williams SRO, temperature choice, CALPHAD comparison, occupancy metrics, transferability.

## Skill: PRB Author Guide — `skills/prb_author_guide.md`

```
\documentclass[prb,twocolumn]{revtex4-2}
\bibliographystyle{apsrev4-2}
```
- Regular Articles: numbered sections
- Abstract: ≤500 words, single paragraph, no equations/table refs
- Figures: EPS/PDF, online color free
- Tables: booktabs `\toprule`/`\midrule`/`\bottomrule`

## Workflow

1. **Analyze** notebooks → extract findings → `repo_analysis.md`
2. **Outline** → user approval
3. **Draft** (parallel): author1 → Methods+Results, author2 → Introduction+Discussion+Conclusions
4. **Integrate** → LaTeX → `latexmk -pdf`
5. **Submit** → convert to REVTeX 4.2 → cover letter → orchestrator (editor)
6. **Review** → 3 reviewers produce feedback → `reviewers/reviewer*_feedback.md`
7. **Revise** → point-by-point response → update manuscript → resubmit
8. **Iterate** until accepted

## LaTeX Conventions

- Unit macros: `\newcommand{\meV}{\ensuremath{\,\mathrm{meV}}}`, `\meVat`, `\eVat`
- Build: `latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode"`
- Figures: `figures/figXX.pdf`
- All energies in meV/atom
- siunitx for units

## ML Pipeline Summary

- **Training:** 262 DFT structures (simple TCP: A15, C15, C14, C36, σ, χ, μ)
- **Validation:** 70 DFT structures (complex TCP: R, M, P, δ)
- **Target:** $E_f^{nmhcp}$ (NM hcp Fe + hcp Mo reference)
- **Descriptors:** BOP moments (canonical d-band TB), ACE (python-ace), SOAP (DScribe)
- **Aggregation:** CNAV (coordination-number-resolved averaging)
- **Models:** KRR (RBF kernel) + RF (200 trees) + MLP (64 hidden) → VotingRegressor
- **Feature selection:** Forward recursive, nested inside 5-fold CV
- **Best RMSE:** BOP 28±3 meV/at (test), 35-42 meV/at (validation)
- **Software:** scikit-learn v1.2, Python 3.10, Conda env `datasets_ml`

## Key Results

1. BOP > ACE > SOAP for TCP energies (p<0.01, 95% bootstrap CIs)
2. CNAV improves RMSE 20-40% over per-structure averaging
3. Learning curves: BOP advantage persists at all training sizes (N=50-209)
4. R-phase sublattice occupancies: MAD=0.04 vs. XRD (Joubert 1993)
5. BW sensitivity: L=±5 kJ/mol changes occupancies <0.03 (except 6c site: ~0.08)
6. DFT data reduction: ~10× vs. exhaustive sampling

## Important Paths

- **Accepted manuscript:** `paper_prb/paper.pdf` (8 pages, 0 errors)
- **Response to reviewers:** `paper_prb/response_to_reviewers.md`
- **Editorial decision:** `reviewers/editorial_decision.md`
- **Original draft:** `paper/paper.pdf` (18 pages, npj format)
- **Cover letter:** `paper_prb/cover_letter.tex`
- **Report:** `report.md`
