# Draft: Methods

## Methods

### DFT Calculations
All density-functional theory (DFT) calculations were performed using the Vienna Ab initio Simulation Package (VASP) with the projector augmented wave (PAW) method and the Perdew–Burke–Ernzerhof (PBE) exchange-correlation functional. The plane-wave energy cutoff was set to 400–450 eV, and Monkhorst–Pack k-point meshes were chosen to ensure total energy convergence to within 1 meV/atom. For TCP phases with large unit cells (R, M, P, δ), single k-point calculations at the Γ-centred point were used, while denser meshes were employed for the smaller simple TCP phases.

For each structure, we performed a series of constant-volume calculations spanning a range of volumes around the equilibrium, followed by E–V curve fitting using the Birch–Murnaghan equation of state (EOS) to obtain the equilibrium volume V₀, bulk modulus B₀, and the equilibrium formation energy. This procedure eliminates Pulay stress errors and ensures consistency across structures with different cell sizes and shapes.

The target property for machine learning was the formation energy referenced to non-magnetic (NM) hcp Fe and hcp Mo, denoted $E_f^{nmhcp}$. This reference state was chosen to eliminate magnetic contributions that are not present in the non-magnetic TCP phases, ensuring a clean target for the ML models.

### Descriptor Computation

#### BOP Moments
Bond-order potential (BOP) moments were computed using the BOPfox code[ref]. We employed a canonical d-band tight-binding Hamiltonian with a rectangular d-band model. For each atom, the first four moments of the local density of states (µ₀, µ₁, µ₂, µ₃) were computed from the crystal structure. Two projection schemes were used: (i) **canonical** — moments from the pure tight-binding Hamiltonian, yielding 405-dimensional feature vectors after CNAV; and (ii) **0.7dProjections 0.5OS** — moments projected onto DFT-calculated local densities of states using a scissor operator, yielding 417-dimensional feature vectors. The latter gave consistently better performance.

#### ACE Descriptors
Atomic cluster expansion (ACE) descriptors[ref] were computed using the `python-ace` package. The ACE framework provides a complete linear basis of rotationally invariant many-body functions of the local atomic environment. We used a cutoff radius of 6.0 Å, correlation orders 2–4, and radial basis functions spaced at 0.5 Å intervals. The full ACE basis yielded up to 1803 features per structure. A "canonical" variant using only the dominant radial basis functions reduced this to 417 features while retaining most of the predictive accuracy.

#### SOAP Descriptors
Smooth overlap of atomic positions (SOAP) descriptors[ref] were computed using the DScribe library (v2.0). The SOAP power spectrum was calculated with the following parameters: radial cutoff r_cut = 6.0 Å, n_max = 8 radial basis functions, and l_max = 6 spherical harmonics. Element-specific SOAP vectors (Fe–Fe, Fe–Mo, Mo–Mo, Mo–Fe) were computed for each central atom and then concatenated. The resulting per-atom SOAP vectors had dimension 287 after CNAV aggregation.

#### CNAV Aggregation
For each structure, the per-atom descriptor vectors were averaged within groups sharing the same coordination number (CN). The CN for each atom was determined from the ACE radial function analysis, using a cutoff of 3.5 Å for the first shell. The CN-resolved averages were concatenated into a single structure-level fingerprint, with the number of CN groups varying between 3 and 6 depending on the phase. Feature sets were also computed without CNAV (using a single per-structure average) as a baseline for comparison.

### Model Training and Evaluation
All machine learning models were implemented using scikit-learn (v1.2). The training/test split (209/53) was stratified by phase to ensure that each simple TCP phase was represented in both sets. Features were standardised to zero mean and unit variance using the training set statistics.

#### Model Selection
Three regression algorithms were considered:

1. **Kernel Ridge Regression (KRR):** RBF kernel with α ∈ [10⁻⁴, 10⁻²] and γ ∈ [10⁻⁴, 10⁻¹] optimised via grid search with 5-fold cross-validation (CV).

2. **Random Forest (RF):** 200 trees, max_depth ∈ [10, 50] and min_samples_leaf ∈ [1, 10] optimised via grid search with 5-fold CV.

3. **Multi-Layer Perceptron (MLP):** Single hidden layer with 64 neurons, ReLU activation, trained with Adam optimiser (learning rate 10⁻³) for up to 1000 epochs with early stopping. Regularisation parameter α ∈ [10⁻⁴, 10⁻²] was optimised via 5-fold CV.

#### Ensemble Construction
For each feature set, a VotingRegressor ensemble was constructed by averaging the predictions of the three optimally tuned models (KRR, RF, MLP). This approach consistently outperformed individual models, with the ensemble RMSE being 5–15% lower than the best individual model.

#### Feature Selection
Forward recursive feature selection was performed separately for each model/feature combination. Starting from the full feature set, features were added one at a time based on the improvement in 5-fold CV RMSE. The selection was terminated when the CV RMSE stopped improving by more than 0.5 meV/atom. This procedure reduced the dimensionality by factors of 2–10 depending on the feature set (from ~400–1800 to ~50–300). Feature selection was embarrassingly parallel and was executed on the cluster using 16 cores per job.

#### Evaluation Metrics
Model performance was evaluated using:
- **RMSE:** $\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2}$
- **MAE:** $\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i|$

Both metrics were computed on the test set (53 structures) and the independent validation set (70 structures).

### Thermodynamic Modelling
Finite-temperature thermodynamic properties were computed within the compound energy formalism (CEF) using the Bragg–Williams (BW) approximation, as implemented in the `pycef` code. The Gibbs free energy of each phase is given by:

$G = \sum_i y_i G_i^\circ + RT \sum_s \sum_i y_i^{(s)} \ln y_i^{(s)} + G^E$

where $y_i^{(s)}$ is the site fraction of species i on sublattice s, $G_i^\circ$ is the ML-predicted formation energy of the end-member compound, and $G^E$ is the excess Gibbs free energy (set to zero for the ideal Bragg–Williams approximation).

Sublattice occupancies were obtained by minimising the Gibbs free energy with respect to site fractions at fixed temperature and composition, using a sequential least-squares programming (SLSQP) optimiser.
