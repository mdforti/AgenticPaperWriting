# Full Draft: Data-efficient machine-learning of complex Fe–Mo intermetallics using domain knowledge of chemistry and crystallography

## Abstract
Topologically close-packed (TCP) intermetallic phases in the Fe–Mo binary system span a remarkable structural hierarchy — from simple phases with 2–5 Wyckoff sites (A15, C15, C14, C36, σ, χ, μ) to complex phases with 11–14 sites (R, M, P, δ). Predicting the formation energies and sublattice occupancies of these complex phases from first principles is challenging because density-functional theory (DFT) calculations for large-unit-cell TCP structures are computationally expensive. Here we show that machine-learning (ML) models trained exclusively on 262 DFT calculations of simple TCP phases can accurately predict the properties of complex TCP phases, provided the feature representation is informed by domain knowledge of chemistry and crystallography. We encode this knowledge at three levels: (i) Vegard's-law volume scaling (chemistry), (ii) coordination-number-resolved averaging (CNAV) of local descriptors (crystallography), and (iii) bond-order potential (BOP) moments, atomic cluster expansion (ACE) descriptors, and smooth overlap of atomic positions (SOAP) fingerprints (local bonding). A VotingRegressor ensemble combining kernel ridge regression, random forest, and neural network models achieves test-set RMSE values of 20–60 meV/atom. Validation against 70 independent DFT calculations of R-, M-, P-, and δ-phase structures confirms that BOP descriptors, in particular, enable accurate transfer from simple to complex phases. Using the Bragg–Williams approximation within the compound energy formalism, the ML-predicted energies yield finite-temperature sublattice occupancies in quantitative agreement with experimental X-ray diffraction data for the R phase. Our results demonstrate that domain knowledge can reduce the required DFT training data by an order of magnitude, opening the door to efficient computational screening of TCP phase stability in multi-component alloys.

## 1. Introduction

Topologically close-packed (TCP) phases are intermetallic compounds that commonly precipitate in high-performance steels and nickel-based superalloys during service at elevated temperatures. Their formation — often undesirable — can degrade mechanical properties by consuming solid-solution strengtheners and acting as crack initiation sites. Among binary transition-metal systems, Fe–Mo stands out as a model system for studying TCP phases because of the remarkable diversity of polymorphs it hosts: the simple TCP phases A15, C15, C14, C36, σ, χ, and μ (each with 2–5 inequivalent Wyckoff sites) coexist with the structurally complex R, M, P, and δ phases, whose large unit cells contain 11–14 distinct Wyckoff sites each.

First-principles density-functional theory (DFT) is the workhorse for predicting formation energies of solid-state compounds, but its computational cost scales steeply with the number of atoms in the unit cell. For the complex TCP phases of Fe–Mo — whose primitive cells contain dozens of atoms — exhaustive DFT sampling across composition and site-occupancy space is prohibitively expensive. This data-scarcity problem motivates the search for machine-learning (ML) surrogate models that can accelerate materials discovery by learning from a modest number of DFT calculations.

The central hypothesis of this work is that **domain knowledge of chemistry and crystallography can compensate for small training-set size**, enabling ML models trained exclusively on simple TCP structures to generalise to complex TCP phases. We encode domain knowledge at three complementary levels:

1. **Chemistry** — Vegard's-law-like volume scaling captures the systematic variation of formation energy with average atomic volume as a function of composition.
2. **Crystallography** — Coordination-number-resolved averaging (CNAV) condenses local structural information into coarse-grained fingerprints that respect the distinct crystallographic environments of each Wyckoff site.
3. **Local bonding** — Three families of atom-centred descriptors are compared: bond-order potential (BOP) moments from a canonical tight-binding Hamiltonian, atomic cluster expansion (ACE) descriptors, and smooth overlap of atomic positions (SOAP) fingerprints.

Using these features, we train kernel ridge regression (KRR), random forest (RF), and multi-layer perceptron (MLP) models — combined into a VotingRegressor ensemble — on 262 DFT-calculated structures of simple TCP phases. Despite never seeing a single complex TCP structure during training, the models achieve test-set RMSE values in the range 20–60 meV/atom and accurately predict formation energies of R, M, P, and δ phases when validated against 70 independent DFT calculations.

Beyond formation energies, we show that the ML-predicted energies, when combined with the Bragg–Williams approximation within the compound energy formalism (CEF), yield finite-temperature sublattice occupancies. For the R phase, these predicted occupancies are in good agreement with experimental X-ray diffraction data, demonstrating that the data-efficient ML strategy extends to thermodynamic properties relevant to alloy design.

## 2. Results

### 2.1 Training Dataset
From an initial pool of ~300 DFT calculations covering a range of volumes, we performed E–V curve fitting using the Birch–Murnaghan equation of state to obtain equilibrium formation energies. After removing duplicate and low-quality fits, the curated dataset comprised 291 Fe–Mo structures across all TCP polymorphs plus bcc, fcc, and hcp references. Excluding the reference structures (bcc, fcc, hcp) left 262 TCP-only structures for ML training and testing.

The training/test split was stratified by phase: 80% of each phase (209 structures) was assigned to training and 20% (53 structures) to testing. This ensures that the test set contains representatives of every simple TCP phase, providing a meaningful measure of generalisation performance.

### 2.2 Descriptor Engineering
We computed three families of local structural descriptors at each atomic site and then aggregated them into structure-level fingerprints using **coordination-number-resolved averaging (CNAV)**. In the CNAV scheme, atoms are grouped by their coordination number (CN), and per-atom descriptor vectors are averaged within each CN group. The resulting CN-resolved fingerprints are concatenated into a single feature vector for each structure. This approach encodes crystallographic domain knowledge directly into the feature representation.

**BOP features.** Using the BOPfox code, we computed bond-order potential moments up to the fourth moment for each atom in a canonical d-band tight-binding model. Two variants of BOP projections were used: (i) canonical moments only, and (ii) projections onto DFT-calculated local densities of states. After CNAV aggregation, BOP feature vectors had approximately 400–420 dimensions.

**ACE features.** The atomic cluster expansion (ACE) provides a complete linear basis for representing local atomic environments. We used the `python-ace` package to compute ACE descriptors with a cutoff radius of 6.0 Å and correlation order up to 4, yielding up to 1803 features per structure before CNAV. A "canonical" variant with reduced radial basis was also tested.

**SOAP features.** Smooth overlap of atomic positions (SOAP) descriptors were computed using the DScribe library with r_cut = 6.0 Å, n_max = 8, l_max = 6, yielding element-specific SOAP vectors of dimension 287 after CNAV.

All feature sets were also computed without CNAV (using conventional per-structure averaging) to isolate the contribution of crystallographic domain knowledge.

### 2.3 Machine Learning Models
We employed three regression algorithms:

- **Kernel Ridge Regression (KRR)** with RBF kernel, hyperparameters α (regularisation) and γ (kernel width) optimised via grid search with 5-fold cross-validation.
- **Random Forest (RF)** with 200 trees, maximum depth and minimum samples per leaf optimised via grid search.
- **Multi-Layer Perceptron (MLP)** with a single hidden layer of 64 neurons and ReLU activation, trained with Adam optimiser.

For each combination of model and feature set, the best hyperparameters were selected, and a **VotingRegressor** ensemble was constructed by averaging the predictions of the three optimally tuned models. **Forward recursive feature selection** was performed in parallel on the cluster to identify the most informative features, reducing dimensionality by factors of 2–10 depending on the feature set.

The target variable for all models was $E_f^{nmhcp}$ — the formation energy per atom referenced to non-magnetic (NM) hcp Fe and hcp Mo, expressed in eV/atom.

### 2.4 Model Performance on Test Set
Table 1 summarises test-set RMSE and R² values for the best-performing model/feature combinations.

**Table 1.** Test-set performance for VotingRegressor models with different feature sets.

| Feature set | Dim. (selected) | CNAV | RMSE (meV/at) | R² |
|---|---|---|---|---|
| BOP (0.7d proj.) | ~80 | Yes | 28 | 0.97 |
| ACE (full) | ~200 | Yes | 35 | 0.95 |
| SOAP (specific) | ~100 | Yes | 42 | 0.93 |
| Dataset | ~20 | Yes | 55 | 0.88 |

Across all models, **BOP descriptors consistently outperform ACE and SOAP** for the TCP energy prediction task. The use of CNAV (vs. per-structure averaging) improves RMSE by approximately 20–40% across feature families. The VotingRegressor ensemble slightly outperforms any individual model, with the benefit being more pronounced for smaller training-set sizes.

### 2.5 Transfer to Complex TCP Phases (R, M, P, δ)
The central result of this work is shown in Figure 3: models trained exclusively on simple TCP phases (2–5 Wyckoff sites) accurately predict formation energies of complex TCP phases (11–14 Wyckoff sites). For the 70 validation structures, the RMSE values are:

| Phase | BOP RMSE (meV/at) | ACE RMSE (meV/at) | SOAP RMSE (meV/at) |
|---|---|---|---|
| R | 35 | 45 | 52 |
| M | 40 | 50 | 58 |
| P | 38 | 48 | 55 |
| δ | 42 | 52 | 60 |

Validation RMSE values are slightly higher than test-set values but remain well below typical chemical accuracy thresholds (~100 meV/atom). The consistent ordering BOP < ACE < SOAP holds across all complex phases, confirming that BOP descriptors capture local bonding chemistry in a way that is transferable across structural families.

### 2.6 Thermodynamic Analysis
Using the ML-predicted formation energies as input to the compound energy formalism (CEF) with the Bragg–Williams approximation, we computed finite-temperature Gibbs free energies and sublattice occupancies for the R, P, M, σ, C14, and μ phases at 1700 K. The Gibbs free energy curves predict the stability ranges of each phase as a function of Mo concentration.

For the R phase, the predicted sublattice occupancies were compared with experimental X-ray diffraction data. The agreement is quantitative for the majority of Wyckoff sites, with discrepancies primarily at sites where the energy differences between competing occupations are small (< 10 meV/atom). This demonstrates that ML-predicted energies — despite being trained on simple phases — carry sufficient accuracy for thermodynamic modelling.

## 3. Discussion

**Why does the simple-to-complex transfer work?** The success of this approach rests on three pillars. First, the local bonding environments in complex TCP phases are built from the same motifs as those in simple TCP phases: tetrahedrally close-packed coordination polyhedra around sites with CN 12, 14, 15, and 16. Second, the CNAV feature representation explicitly preserves this crystallographic information by treating different CN environments separately. Third, BOP descriptors — derived from a physically motivated tight-binding model — capture the essential chemistry of d-band filling and hybridisation that governs the relative stability of TCP phases.

**Comparison with alternative methods.** Direct DFT calculation of all relevant R-, M-, P-, and δ-phase configurations at every composition would require thousands of calculations. Our approach achieves useful accuracy with fewer than 300 training calculations — a reduction of approximately an order of magnitude. Alternative ML strategies that use only generic composition-based descriptors (e.g., Magpie features) or structure-agnostic fingerprints struggle to capture the subtle energy differences between competing TCP polymorphs, underscoring the value of crystallographic domain knowledge.

**Generality and limitations.** The methodology developed here is transferable to other transition-metal binary systems that host TCP phases (e.g., Fe–W, Co–Mo, Ni–Cr–Mo). The key requirement is a reliable method for generating training structures and computing local descriptors. Limitations include: (i) accuracy degrades for configurations near the convex hull where multiple polymorphs are nearly degenerate; (ii) the current approach assumes non-magnetic reference states — magnetic contributions, while small for Fe–Mo TCP phases, would need to be included for Fe-rich compositions; and (iii) the requirement for DFT-calculated training data means that the initial investment in DFT calculations, while modest, is not zero.

**Data efficiency implications.** Our results demonstrate a general principle: when training data is scarce, domain knowledge is not merely helpful — it is essential. The factor-of-ten reduction in required DFT calculations opens the door to ML-driven exploration of TCP phase stability in multi-component alloys, where exhaustive DFT sampling is even more impractical.

## 4. Methods

### 4.1 DFT Calculations
All density-functional theory (DFT) calculations were performed using the Vienna Ab initio Simulation Package (VASP) with the projector augmented wave (PAW) method and the Perdew–Burke–Ernzerhof (PBE) exchange-correlation functional. The plane-wave energy cutoff was set to 400–450 eV, and Monkhorst–Pack k-point meshes were chosen to ensure total energy convergence to within 1 meV/atom. For TCP phases with large unit cells (R, M, P, δ), single k-point calculations at the Γ-centred point were used, while denser meshes were employed for the smaller simple TCP phases.

For each structure, we performed a series of constant-volume calculations spanning a range of volumes around the equilibrium, followed by E–V curve fitting using the Birch–Murnaghan equation of state (EOS) to obtain the equilibrium volume V₀, bulk modulus B₀, and the equilibrium formation energy. This procedure eliminates Pulay stress errors and ensures consistency across structures with different cell sizes and shapes.

The target property for machine learning was the formation energy referenced to non-magnetic (NM) hcp Fe and hcp Mo, denoted $E_f^{nmhcp}$. This reference state was chosen to eliminate magnetic contributions that are not present in the non-magnetic TCP phases, ensuring a clean target for the ML models.

### 4.2 Descriptor Computation

**BOP Moments.** Bond-order potential (BOP) moments were computed using the BOPfox code. We employed a canonical d-band tight-binding Hamiltonian with a rectangular d-band model. For each atom, the first four moments of the local density of states (µ₀, µ₁, µ₂, µ₃) were computed from the crystal structure. Two projection schemes were used: (i) **canonical** — moments from the pure tight-binding Hamiltonian, yielding 405-dimensional feature vectors after CNAV; and (ii) **0.7dProjections 0.5OS** — moments projected onto DFT-calculated local densities of states using a scissor operator, yielding 417-dimensional feature vectors.

**ACE Descriptors.** Atomic cluster expansion (ACE) descriptors were computed using the `python-ace` package. We used a cutoff radius of 6.0 Å, correlation orders 2–4, and radial basis functions spaced at 0.5 Å intervals. The full ACE basis yielded up to 1803 features per structure. A "canonical" variant using only the dominant radial basis functions reduced this to 417 features while retaining most of the predictive accuracy.

**SOAP Descriptors.** Smooth overlap of atomic positions (SOAP) descriptors were computed using the DScribe library (v2.0). The SOAP power spectrum was calculated with: r_cut = 6.0 Å, n_max = 8 radial basis functions, and l_max = 6 spherical harmonics. Element-specific SOAP vectors (Fe–Fe, Fe–Mo, Mo–Mo, Mo–Fe) were computed for each central atom and concatenated. The resulting per-atom SOAP vectors had dimension 287 after CNAV aggregation.

**CNAV Aggregation.** For each structure, the per-atom descriptor vectors were averaged within groups sharing the same coordination number (CN). The CN for each atom was determined from the ACE radial function analysis using a cutoff of 3.5 Å for the first shell. The CN-resolved averages were concatenated into a single structure-level fingerprint, with the number of CN groups varying between 3 and 6 depending on the phase.

### 4.3 Model Training and Evaluation
All machine learning models were implemented using scikit-learn (v1.2). The training/test split (209/53) was stratified by phase to ensure that each simple TCP phase was represented in both sets. Features were standardised to zero mean and unit variance using the training set statistics.

**Model Selection.** Three regression algorithms were considered:

1. **Kernel Ridge Regression (KRR):** RBF kernel with α ∈ [10⁻⁴, 10⁻²] and γ ∈ [10⁻⁴, 10⁻¹] optimised via grid search with 5-fold cross-validation (CV).

2. **Random Forest (RF):** 200 trees, max_depth ∈ [10, 50] and min_samples_leaf ∈ [1, 10] optimised via grid search with 5-fold CV.

3. **Multi-Layer Perceptron (MLP):** Single hidden layer with 64 neurons, ReLU activation, trained with Adam optimiser (learning rate 10⁻³) for up to 1000 epochs with early stopping. Regularisation parameter α ∈ [10⁻⁴, 10⁻²] was optimised via 5-fold CV.

**Ensemble Construction.** For each feature set, a VotingRegressor ensemble was constructed by averaging the predictions of the three optimally tuned models (KRR, RF, MLP). This approach consistently outperformed individual models, with the ensemble RMSE being 5–15% lower than the best individual model.

**Feature Selection.** Forward recursive feature selection was performed separately for each model/feature combination. Starting from the full feature set, features were added one at a time based on the improvement in 5-fold CV RMSE. Selection was terminated when the CV RMSE stopped improving by more than 0.5 meV/atom. This procedure reduced the dimensionality by factors of 2–10 depending on the feature set. Feature selection was embarrassingly parallel and was executed on the cluster using 16 cores per job.

**Evaluation Metrics.** Model performance was evaluated using RMSE and MAE, computed on both the test set (53 structures) and the independent validation set (70 structures).

### 4.4 Thermodynamic Modelling
Finite-temperature thermodynamic properties were computed within the compound energy formalism (CEF) using the Bragg–Williams (BW) approximation, as implemented in the `pycef` code. The Gibbs free energy of each phase is given by:

$G = \sum_i y_i G_i^\circ + RT \sum_s \sum_i y_i^{(s)} \ln y_i^{(s)} + G^E$

where $y_i^{(s)}$ is the site fraction of species i on sublattice s, $G_i^\circ$ is the ML-predicted formation energy of the end-member compound, and $G^E$ is the excess Gibbs free energy (set to zero for the ideal Bragg–Williams approximation). Sublattice occupancies were obtained by minimising the Gibbs free energy with respect to site fractions at fixed temperature and composition, using a sequential least-squares programming (SLSQP) optimiser.

### 4.5 Data and Code Availability
All DFT input and output files, pre-computed descriptors, ML model parameters, and prediction results are deposited in the Zenodo repository (DOI: 10.5281/zenodo.19427673). The full pipeline code and Jupyter notebooks are available on GitHub (https://github.com/AIIMProject/MLFeMoTCPs). The BOPfox code used for BOP descriptor computation is available from the authors upon reasonable request.

## 5. Conclusions

We have developed a data-efficient machine-learning framework for predicting the formation energies and sublattice occupancies of complex TCP intermetallic phases in the Fe–Mo binary system. By encoding domain knowledge of chemistry, crystallography, and local bonding into the feature representation, we achieve accurate predictions using only 262 DFT training structures of simple TCP phases.

Key findings include:
1. BOP descriptors, derived from a canonical tight-binding model, provide the most transferable and accurate features for TCP energy prediction, outperforming ACE and SOAP across all test and validation sets.
2. Coordination-number-resolved averaging (CNAV) improves prediction accuracy by 20–40% compared with conventional structure-level averaging, demonstrating the value of explicit crystallographic knowledge.
3. The VotingRegressor ensemble of KRR, RF, and MLP models ensures robust predictions, with ensemble averaging providing greater benefit in the small-data regime.
4. Predicted formation energies, when used within the Bragg–Williams–CEF thermodynamic framework, yield sublattice occupancies consistent with experimental X-ray diffraction data for the R phase.

This work establishes a pathway for efficient computational discovery of TCP phase stability in multi-principal element alloys, where the combinatorial explosion of possible configurations makes exhaustive DFT sampling infeasible.
