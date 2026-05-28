# General description of the project

# DatasetsML — Fe-Mo TCP Phase Stability from Machine Learning
**Paper**: *Data-efficient machine-learning of complex Fe–Mo intermetallics using domain knowledge of chemistry and crystallography*  
---

## Overview
The project describes the machine-learning pipeline used to predict the formation energies and sublattice occupancies of complex TCP (topologically close-packed) intermetallic phases in the Fe–Mo binary system.

The motodology exploits **domain knowledge** at three levels — chemistry (Vegard's law volume scaling), crystallography (coordination-number-resolved averaging, CNavg), and local bonding (BOP, ACE, SOAP descriptors) — enables data-efficient predictions for complex TCP phases (R, M, P, δ with 11–14 Wyckoff sites) from models trained on only simple TCP phases (A15, C15, C14, C36, σ, χ, μ with 2–5 Wyckoff sites) using fewer than 300 DFT calculations.

---

## Repository Structure

```
DatasetsML_2.0/
├── Fe-Mo/
│   ├── CuratedParsedBriefSummary.json   # Curated DFT dataset @ Zenodo archive
│   ├── Atomsobjects/Fe-Mo-POSCAR.initial-rescaled-AtomsObjects.json #  ASE Atoms objects, initial guess structures
│   ├── Atomsobjects/Fe-Mo-POSCAR.initial-rescaled-AtomsObjects.json #  ASE Atoms objects, optimized structures
│   ├── Descriptors/                         # Pre-computed BOP feature files, 
│   ├── results/                             # Feature selection results, predictions
│   ├── graphs/                              # Generated figures
│   └── data/Validation/                     # DFT validation data
├── Tools/                                   # datasetsml-tools Python package
├── Scripts/                                 # Standalone scripts (feature selection)
├── dependencies/                            # External packages (see below)
├── environment.yaml                         # Full conda environment
└── environment_public.yaml                  # Environment without private packages
```

---

## Notebook Workflow

Notebooks are numbered to indicate execution order. The main publishable pipeline starts at **notebook 03**. Notebooks 00–02 require raw DFT output data and are preserved for future integration with the [NOMAD repository](https://nomad-lab.eu/).

| Notebook | Purpose | Prerequisites |
|----------|---------|---------------|
| `REQUIRE_RAW_DATA_00_ParseBriefsummary.ipynb` | Parse raw DFT output | Raw DFT data (not included; NOMAD planned) |
| `REQUIRE_RAW_DATA_01_CurateWithEVcurves.ipynb` | Curate dataset via E–V curve fits | Notebook 00 output |
| `REQUIRE_RAW_DATA_02_CharacterizeDataset.ipynb` | Dataset statistics | Notebook 01 output |
| `03_PrepareDataset.ipynb` | Prepare ASE Atoms objects and dataset splits | `FullyCuratedParsedBriefSummary.pkl` |
| `04_ComputeACEFeatures.ipynb` | Compute ACE descriptors | Atoms objects, `python-ace` |
| `04_ComputeLibraryFeatures.ipynb` | Compute SOAP, Magpie/matminer descriptors | Atoms objects, DScribe |
| `05_ComputeBOPFeatures.ipynb` | Compute BOP moment descriptors | Atoms objects, **BOPfox** (see below) |
| `07_MachineLearn-ModelSelection.ipynb` | Build ensemble ML models from feature selection results | Descriptor files, `concatenation_results_*.pkl` |
| `08_AnalysisModels.ipynb` | Analyse and compare fitted models | Model outputs |
| `09_PrepareFeaturesPrediction.ipynb` | Generates R,P,M, $\delta$ configurations, computes descriptors, predicts formation enthalpies, generates validation data | Fitted ensamble models |
| `10_ValidateValidationData.ipynb` | Checks existence of DFT for validation data, formats for final model validation | Validation data + model predictions |
| `11_ValidatePredictions.ipynb` | Final prediction validation | Predictions + DFT validation |
| `15_A_Thermodynamics.ipynb` | Thermodynamic analysis (Bragg–Williams) | Model predictions |

Legacy and experimental notebooks are in the `legacy/` folder.

---
## Dependencies & Software

### Public packages (included in `environment_public.yaml`)
- [ASE](https://wiki.fysik.dtu.dk/ase/) — atomic simulation environment
- [DScribe](https://singroup.github.io/dscribe/) — SOAP descriptor generation
- [python-ace](https://github.com/ICAMS/python-ace) — ACE descriptor generation
- [scikit-learn](https://scikit-learn.org/) — machine learning
- [pymatgen](https://pymatgen.org/) — structure handling

### BOPfox (available on request)
Notebooks `05_ComputeBOPFeatures.ipynb` and `09_PrepareFeaturesPrediction.ipynb` require the **BOPfox** software and associated Python wrappers (`bopfoxfeaturizer`, `bopdftprojections`).  
BOPfox is not openly distributed. Please contact the authors to request access.  
Pre-computed BOP descriptor files for the complex TCP phases are provided in the Zenodo archive so that notebooks 09–11 can be run without BOPfox.

---

## Data Availability

- **Curated DFT dataset** (`FullyCuratedParsedBriefSummary.pkl`): included in this repository and in the Zenodo archive.
- **Pre-computed BOP descriptors** for complex TCP phases (R, M, P, δ): available in the Zenodo archive (see `ZENODO_MANIFEST.md`).
- **Raw DFT calculation data**: to be deposited in the [NOMAD repository](https://nomad-lab.eu/) (in preparation). This repository will be updated with NOMAD integration once available.

---
## License

MIT License — see [LICENSE](LICENSE).


# Instructions for the Agentic Paper Writing Workflow

This file defines the shared rules that govern all agents and the sequential steps of the paper-writing workflow. Individual responsibilities, writing requirements, and domain-specific criteria for each agent are defined exclusively in the corresponding agent files under `agents/` and `reviewers/`. The target journal is **Physical Review B** (REVTeX 4.2, two-column format).

## General Rules (all agents)

These rules apply to every agent without exception.

**Integrity.** Never fabricate data, numbers, figures, or references. Use only values that appear in the repository notebooks and data files. If a citation is needed and the exact reference is unknown, insert a `% TODO: CITE [description]` placeholder. Never invent a DOI, author name, or journal title.

**No bullet points.** All scientific content must be written in connected, fluent prose. Bullet lists, dashes, and enumerated lists are prohibited in the manuscript text. When a sequence of items must be presented — parameters, steps, findings — integrate them into paragraphs using appropriate transitional phrases such as "first", "furthermore", "in addition", and "finally".

**Scientific method.** Every result must be accompanied by (1) the scientific question or hypothesis being tested, (2) a description of the computational experiment including inputs, model, and parameters, (3) the quantitative outcome with numerical values and units, and (4) an interpretation that connects the result to the broader argument. Claims without numbers are not acceptable.

**LaTeX format.** The manuscript uses `\documentclass[prb,twocolumn]{revtex4-2}`. Units are typeset with `\SI{}{}` from the siunitx package. All energies are reported in meV/atom (multiply eV/atom values by 1000). The bibliography uses `\bibliographystyle{apsrev4-2}`. Cross-references use `\ref{}` and `\label{}`.

**Build command.** Compile from the `drafts/prb_draft/` directory using:
```
latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" paper.tex
```
Run `bibtex paper` after any bibliography change.

---

## Workflow

The workflow consists of two nested iteration loops. The inner loop (Phases 1–3) is the authors' internal writing and review cycle. The outer loop (Phases 4–8) is the external editorial and peer-review cycle. The outer loop repeats until the Editor issues a final acceptance or rejection.

### Phase 1 — Manuscript Preparation

Author 1 reads the complete repository — all notebooks from 03 to 15A, the curated DFT dataset, the pre-computed descriptor files, and the figures in `Backbone/` — and performs a literature survey on machine learning for intermetallic phase stability and TCP phases in transition-metal alloys. Based on this study, Author 1 writes the first complete manuscript draft covering every section: Abstract, Introduction, Methods, Results, Discussion, and Conclusions, together with all required figures extracted from the notebooks. The full writing responsibilities, section requirements, figure checklist, and literature constraints for this phase are defined in `agents/author1.md`.

### Phase 2 — Internal Review and Revision

Author 1 sends the completed draft to Author 2. Author 2 reads it immediately and in full, then provides detailed written feedback identifying every scientific, methodological, and presentational problem found. Author 1 addresses every comment and returns a revised draft. This exchange continues iteratively — with no fixed limit on rounds — until Author 2 is genuinely satisfied with the scientific rigour and communicative quality of the manuscript and explicitly approves it for submission. The review standards, feedback process, and approval conditions are defined in `agents/author2.md`.

### Phase 3 — Compilation and Submission

The Orchestrator receives the draft that Author 2 has approved, runs the pre-submission checklist, and compiles the manuscript to PDF using `latexmk -pdf paper.tex` from `drafts/prb_draft/`. If any checklist item fails, the Orchestrator returns the draft to the responsible author with specific instructions and does not proceed until all items pass. Once the PDF is clean, Author 1 submits it to the Editor. The compilation procedure and checklist are defined in `agents/orchestrator.md`.

### Phase 4 — Editorial Assessment

The Editor reads the submitted manuscript and performs a desk review. If the manuscript fails on formatting, scope, or abstract requirements, the Editor issues a desk rejection and returns it to the authors with specific instructions; the workflow returns to Phase 2. If the manuscript passes, the Editor assigns it to all three referees with individual covering notes and waits for their reports. The desk-review criteria and referee assignment procedure are defined in `agents/editor.md`.

### Phase 5 — Peer Review

Reviewer 1, Reviewer 2, and Reviewer 3 each read the manuscript independently and write a structured referee report saved as `reviewers/reviewer{N}_feedback_r{round}.md`. Reviewer 1 evaluates the machine-learning methodology and model validation. Reviewer 2 evaluates the metallurgical soundness and DFT setup. Reviewer 3 evaluates the thermodynamic analysis and connection to experiment. Each reviewer's scope and mandatory checks are defined in `reviewers/reviewer1.md`, `reviewers/reviewer2.md`, and `reviewers/reviewer3.md` respectively.

### Phase 6 — Editorial Decision

The Editor reads all three referee reports and synthesises them into a written decision letter saved as `reviewers/editorial_decision_r{round}.md`. The letter states the decision (Accept, Minor Revision, Major Revision, or Reject), explains the reasoning in connected prose, and lists every change required before the next round. The decision letter and the full referee reports are sent to the authors. Decision types and letter format are defined in `agents/editor.md`.

### Phase 7 — Revision and Response

Author 1 and Author 2 read the decision letter and all referee reports together. They discuss each point raised and agree on a response strategy: which criticisms are valid and must be fully addressed, which can be contested with scientific argument, and which fall outside the scope of the manuscript. Author 1 then revises the manuscript accordingly and writes a point-by-point response letter — saved as `drafts/prb_draft/responses/response_r{round}.md` — that addresses every comment from every referee in the order they appear in the decision letter. Author 2 reads both the revised manuscript and the response letter, checks that every referee comment has been addressed or argued against, and approves both before resubmission. If either is unsatisfactory, the revision continues. The full procedure for this phase is defined in `agents/author1.md` and `agents/author2.md`.

### Phase 8 — Resubmission

The Orchestrator compiles the revised manuscript to PDF, verifies that the response letter is complete, and resubmits both to the Editor. The workflow returns to Phase 4. This outer loop continues until the Editor issues a final acceptance or a rejection that the authors choose not to appeal.

---

## File Layout Reference

```
agents/
  author1.md              # Author 1 full agent definition
  author2.md              # Author 2 / Advisor full agent definition
  orchestrator.md         # Orchestrator full agent definition
  editor.md               # Editor (PRB handling editor) full agent definition
reviewers/
  reviewer1.md            # Reviewer 1: ML for materials properties
  reviewer2.md            # Reviewer 2: Metallurgy and computational materials science
  reviewer3.md            # Reviewer 3: Senior metallurgist, TCP phases
  reviewer{N}_feedback_r{round}.md  # Referee reports (one per reviewer per round)
  editorial_decision_r{round}.md    # Editor decision letters
drafts/prb_draft/
  paper.tex               # Current manuscript (always the latest version)
  references.bib          # Bibliography
  figures/                # Extracted PDF figures
  responses/
    response_r{round}.md  # Point-by-point response to reviewers
skills/
  prb_author_guide.md     # Physical Review B formatting reference
INSTRUCTIONS.md           # Workflow overview and general rules
```