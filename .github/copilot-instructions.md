# Paper Writing Lab — Instructions for Copilot

## Project Overview

This repository implements an agent-based system for collaborative scientific paper writing. It simulates the full journal submission and peer-review process for a research paper on machine-learning-predicted Fe–Mo TCP phase formation energies, targeting Physical Review B.

## Repository Structure

```
.
├── agents/           # Agent definitions (orchestrator, author1, author2)
├── reviewers/        # Reviewer agent definitions + feedback files
├── skills/           # Domain skills (PRB Author Guide)
├── paper/            # Original npj-format LaTeX manuscript
├── paper_prb/        # PRB-format LaTeX manuscript (accepted version)
├── drafts/           # Markdown drafts
├── logs/             # Session archives
├── MLFeMoTCPs/       # Source ML repository (notebooks, data, pipeline code)
└── .github/          # Copilot / CI configuration
```

## Agent System

Six agents collaborate in the paper writing & review workflow:

### Orchestrator (editor)
**File:** `agents/orchestrator.md`
- Role: Workflow coordinator and submission manager
- Manages 5 phases: Outline → Drafting → Integration → Compilation → Iteration
- Assigns sections to author1 and author2
- Reviews consistency, compiles LaTeX, manages submission to PRB

### Author 1 — Lead Author (Mariano Forti)
**File:** `agents/author1.md`
- ML pipeline designer: KRR, RF, MLP, VotingRegressor, BOPfox, ACE, SOAP, CNAV
- Writes Methods (DFT params, descriptors, model training) and Results (RMSE tables, validation, thermodynamics)

### Author 2 — Advisor (Thomas Hammerschmidt / Ralf Drautz)
**File:** `agents/author2.md`
- Atomistic simulations & thermodynamics expert
- Writes Introduction (TCP phases, data scarcity, domain knowledge), Discussion (transferability, limitations), Conclusions, and Abstract

### Reviewer 1 — Computational Materials Physicist
**File:** `reviewers/reviewer1.md`
- DFT, tight-binding, BOP methods expert
- Scrutinizes: DFT convergence, reference states, BOP moment truncation, CNAV information loss, Pulay stress

### Reviewer 2 — Machine Learning for Materials Science
**File:** `reviewers/reviewer2.md`
- Kernel methods, ensemble models, feature engineering expert
- Scrutinizes: nested CV/data leakage, confidence intervals, train/test splits, learning curves, hyperparameters, reproducibility

### Reviewer 3 — Thermodynamics & CALPHAD
**File:** `reviewers/reviewer3.md`
- CEF, Bragg-Williams, TCP phase crystallography expert
- Scrutinizes: BW/SRO approximation, temperature choice, CALPHAD comparison, site-occupancy metrics, transferability

## Skill: Physical Review B Author Guide
**File:** `skills/prb_author_guide.md`

Key formatting rules:
- Document class: `\documentclass[prb,twocolumn]{revtex4-2}`
- Bibliography: `\bibliographystyle{apsrev4-2}`
- Regular Articles: numbered sections (1, 2, 3, ...), subsections (1.1, 1.2, ...)
- Abstract: single paragraph, <500 words, no displayed equations, no numbered refs
- Figures: separate EPS/PDF files, online color free
- Tables: booktabs ruled tables preferred
- References: numbered [1], [2], ... with DOIs

## Workflow

1. Analyze notebooks → extract findings → write `repo_analysis.md`
2. Propose outline → get user approval
3. Draft in parallel: author1 = Methods+Results, author2 = Intro+Discussion+Conclusions
4. Integrate, review for consistency, iterate
5. Submit to PRB (convert to REVTeX 4.2, write cover letter)
6. Peer review by 3 independent reviewers → feedback in `reviewers/`
7. Revise & resubmit based on reviewer comments (point-by-point response)

## LaTeX Conventions

- Figures: `figures/figXX.pdf` (extracted from notebook outputs)
- Tables: inline in section files
- Energies in meV/atom (convert from eV/atom by multiplying by 1000)
- Use `\SI{}{}` from siunitx for units
- Unit macros: `\meV`, `\eVat`, `\meVat`
- Build: `latexmk -pdf paper.tex` (with `bibtex` for bibliography updates)

## ML Pipeline (source repo: MLFeMoTCPs/)

- **Dataset:** 262 DFT structures simple TCP phases (A15, C15, C14, C36, σ, χ, μ)
- **Validation:** 70 DFT structures complex phases (R, M, P, δ)
- **Target:** Formation energy $E_f^{nmhcp}$ (NM hcp Fe + hcp Mo reference)
- **Descriptors:** BOP moments (canonical d-band TB), ACE (python-ace), SOAP (DScribe)
- **Aggregation:** Coordination-number-resolved averaging (CNAV)
- **Models:** KRR + RF + MLP → VotingRegressor ensemble
- **Key result:** BOP RMSE 28 meV/at (test), 35-42 meV/at (validation)
- **Software:** scikit-learn v1.2, Conda env `datasets_ml`, Python 3.10

## Key Findings (from the paper)

1. BOP descriptors outperform ACE and SOAP for TCP energy prediction (p<0.01)
2. CNAV improves RMSE by 20-40% vs. conventional per-structure averaging
3. VotingRegressor ensemble (KRR+RF+MLP) improves RMSE 5-15% over best individual model
4. Predicted energies yield R-phase XRD-validated sublattice occupancies (MAD=0.04)
5. Domain knowledge reduces required DFT data by ~10×
