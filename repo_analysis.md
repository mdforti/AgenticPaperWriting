# Repository Analysis — MLFeMoTCPs

## Paper Metadata
- **Title:** "Data-efficient machine-learning of complex Fe–Mo intermetallics using domain knowledge of chemistry and crystallography"
- **Authors:** Mariano Forti, Alesya Malakhova, Yury Lysogorskiy, Wenhao Zhang, Jean-Claude Crivello, Jean-Marc Joubert, Ralf Drautz, Thomas Hammerschmidt
- **Affiliations:** ICAMS (Ruhr-Universität Bochum), CNRS-Saint-Gobain-NIMS (Tsukuba), ICMPE (Thiais)
- **Published in:** npj Computational Materials (2026)
- **DOI:** 10.1038/s41524-026-02070-5
- **Data DOI:** 10.5281/zenodo.19427673

## Scientific Objective
Predict **formation energies** and **sublattice occupancies** of complex topologically close-packed (TCP) intermetallic phases in the **Fe–Mo binary system** using machine learning. The core challenge: complex TCP phases (R, M, P, d with 11–14 Wyckoff sites) are predicted from models trained only on simple TCP phases (A15, C15, C14, C36, s, c, µ with 2–5 Wyckoff sites) using fewer than 300 DFT calculations.

## Domain-Knowledge Strategy
The methodology exploits **three levels of domain knowledge**:

| Level | Knowledge Type | Implementation |
|---|---|---|
| **Chemistry** | Vegard's law volume scaling | Atomic features based on elemental fractions |
| **Crystallography** | Coordination-number-resolved averaging (CNAV) | CN-dependent per-site features aggregated into structure-level fingerprints |
| **Local Bonding** | BOP / ACE / SOAP descriptors | 3 complementary local structural representations |

## Data
- **291 DFT training structures** (curated from ~300 raw DFT runs via E–V curve fitting)
- **262 TCP-only structures** used for ML (bcc/fcc/hcp removed)
- **70 validation structures** for M, P, d, R phases (from separate DFT calculations)
- DFT code: VASP with PBE-PAW pseudopotentials, ENCUT = 400–450 eV

## Feature Sets (18 total variants)

| Feature Family | Dim. (max) | CNAV? | Description |
|---|---|---|---|
| atomic | 135 | Yes | Elemental fractions, volume, Mag |
| dataset | 32 | Yes | Per-atom stats, structure encoding |
| SOAP_specific_small | 287 | Yes | DScribe SOAP, element-specific |
| ACE | 1803 | Yes | Atomic Cluster Expansion, full |
| Canonical ACE | 417 | Yes | ACE with canonical weights |
| Canonical BOP | 405 | Yes | BOPfox, canonical TB params |
| 0.7dProjections 0.5OS BOP | 417 | Yes | BOPfox, DFT projections |
| *(All above also exist as "no CNAV" variants)* | — | No | Same features, no CN averaging |

## ML Models & Training
- **Models:** Kernel Ridge Regression (KRR), Random Forest (RF), Multi-Layer Perceptron (MLP)
- **Ensemble:** VotingRegressor combining optimally-tuned pipelines
- **Feature selection:** Forward recursive feature selection (cluster-parallel)
- **Target variable:** $E_f^{nmhcp}$ (formation energy, non-magnetic hcp reference)
- **Train/Test split:** 209 train / 53 test (stratified by phase, 80/20)
- **Hyperparameter optimization:** Grid search with cross-validation for each model/feature combination

## Key Findings

### 1. Model Performance
- **Kernel Ridge** with BOP features achieves best overall accuracy
- **BOP descriptors** consistently outperform ACE and SOAP for this system
- Test RMSE in the range of ~20–60 meV/atom depending on feature/model combination

### 2. Validation Results
- Independent DFT validation for 70 structures across R, M, P, d phases
- RMSE values (meV/atom) for each descriptor class:
  - BOP: ~X meV/atom (best)
  - ACE: ~Y meV/atom
  - SOAP: ~Z meV/atom

### 3. Transfer Learning Success
- Models trained exclusively on simple TCP phases generalize to complex TCP phases
- This data-efficiency is the core claim of the paper

### 4. Thermodynamic Analysis (Notebook 15A)
- Bragg–Williams approximation using CEF (Compound Energy Formalism)
- Finite-temperature sublattice occupancies computed from ML predictions
- R-phase occupancy compared with experimental XRD data
- Gibbs free energy curves computed for R, P, M, C14, mu, sigma phases at 1700 K

## Notebook Pipeline

| Notebook | Purpose |
|---|---|
| 00 | Parse raw DFT output (requires NOMAD data) |
| 01 | Curate dataset via E–V curve fits |
| 02 | Dataset characterization statistics |
| 03 | Prepare ASE Atoms objects and dataset splits |
| 04a | Compute ACE descriptors |
| 04b | Compute SOAP, Magpie/matminer descriptors |
| 05 | Compute BOP moment descriptors (requires BOPfox) |
| 07 | Feature selection analysis and model building |
| 07b | Model selection (VotingRegressor ensemble) |
| 08 | Model analysis and comparison figures |
| 09 | Generate R,P,M,d configurations, compute descriptors, predict |
| 10 | Validate format for DFT validation data |
| 11 | Final prediction validation (main paper figures) |
| 15A | Thermodynamic analysis (Bragg–Williams) |

## Software Dependencies
- ASE (Atomic Simulation Environment)
- DScribe (SOAP descriptors)
- python-ace (ACE descriptors)
- scikit-learn (ML models)
- pymatgen (structure handling)
- BOPfox (closed-source, available on request)
- pycef (Compound Energy Formalism thermodynamics)

## Reproducibility
- **Without BOPfox:** Run notebooks 07 → 08 → 09 → 10 → 11 after downloading Zenodo data
- **Full reproduction:** Run notebooks 03 → 04 → 05, then Scripts/FeatureSelection.py on cluster, then 07 → 11
- Zenodo archive (~1.4 GB) contains all pre-computed descriptors and prediction outputs
