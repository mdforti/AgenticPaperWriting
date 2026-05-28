# Review by Reviewer 2 — Machine Learning for Materials Science

## (i) Summary

This paper proposes a domain-knowledge-informed machine-learning pipeline to predict formation energies of complex Fe–Mo TCP intermetallics using only 262 DFT training structures of simple phases. The authors compare BOP, ACE, and SOAP descriptors, aggregated via coordination-number-resolved averaging (CNAV), and use a VotingRegressor ensemble (KRR + RF + MLP). The best model achieves test RMSE of 28 meV/atom and validation RMSE of 35–42 meV/atom for complex phases. The predicted energies are then used in a CEF/Bragg–Williams thermodynamic framework to compute R-phase sublattice occupancies that agree with XRD experiments.

The paper addresses a genuinely hard problem (small-data regime, transfer across structural families) and the domain-knowledge encoding strategy is principled. I have several concerns regarding the rigour of the ML evaluation, particularly around statistical significance, data leakage, and uncertainty quantification.

## (ii) Major Comments

**1. Data leakage in feature selection.**
The Methods section states that forward recursive feature selection was "performed separately for each model/feature combination" and terminated when CV RMSE stopped improving. However, the authors do not specify whether feature selection was nested *inside* the cross-validation loop or performed on the full training set before cross-validation. If feature selection was performed on the full 209-structure training set and then evaluated via 5-fold CV, this constitutes data leakage — the feature selector has seen all training data, and the CV estimate will be optimistically biased. The authors must clarify and, if the latter case applies, re-run the analysis with nested CV.

**2. Statistical significance of descriptor ranking.**
The central claim is BOP > ACE > SOAP. Table I shows RMSE values of 28, 35, and 42 meV/atom for BOP, ACE, and SOAP, respectively. No confidence intervals or error bars are provided for these values. Given the small test set (53 structures), the uncertainty on the RMSE estimate is non-trivial. I request that the authors report 95% confidence intervals for all RMSE values (e.g., via bootstrap or the standard formula assuming normality of residuals). Without this, the reader cannot assess whether the BOP advantage over ACE is statistically significant.

**3. Single train/test split.**
The reported results rely on a single stratified 80/20 split (209/53). With only 262 total structures, the results may be sensitive to the specific split. The authors should report results from at least 10 repeated random stratified splits, or use leave-one-phase-out cross-validation to demonstrate robustness. The current single-split evaluation is a weakness for a paper where the key claim is about generalisation.

**4. Learning curves.**
For a paper emphasising data efficiency, the absence of learning curves is a surprising omission. The claim that "domain knowledge compensates for small training-set size" would be strongly supported by showing RMSE as a function of training-set size (e.g., N = 50, 100, 150, 209). This would also demonstrate whether the advantage of BOP over ACE/SOAP persists across all data regimes or emerges only at larger training set sizes.

**5. Hyperparameter optimisation details.**
The hyperparameter ranges are given only sparsely (e.g., α ∈ [10⁻⁴, 10⁻²], γ ∈ [10⁻⁴, 10⁻¹]). Were these ranges determined by preliminary experiments? Were the optimised hyperparameters stable across cross-validation folds? The authors should report the chosen hyperparameters for each model/feature combination and discuss whether they differ systematically across descriptor families.

**6. Reproducibility.**
The scikit-learn version is given (v1.2), but random seeds are not reported. For ensemble methods (RF) and neural networks (MLP), determinism requires fixing multiple random seeds (numpy, sklearn, Python random). The authors should specify all random seeds used and confirm that the results are reproducible.

## (iii) Minor Comments

1. The VotingRegressor averages predictions of KRR, RF, and MLP. Were the individual models' predictions on a common scale before averaging? If RMSE values differ substantially between models, a simple average may not be optimal — a weighted ensemble could perform better.
2. The Magpie baseline is labelled "Dataset (magpie)" in Table I. Was Magpie computed using the full 262-structure composition information or only the simple-phase training set? Please clarify.
3. Feature selection termination criterion: "when CV RMSE stopped improving by more than 0.5 meV/atom" — 0.5 meV/atom seems tight given the overall RMSE values. How sensitive are the results to this threshold? A sensitivity analysis would be informative.
4. The CNAV approach reduces dimensionality but also changes the feature space qualitatively. The claim that CNAV "improves RMSE by 20–40%" is based on a supplementary figure that was not included in the review. Please include the non-CNAV baseline RMSE in the main text for completeness.
5. The paper would benefit from a parity plot with colour-coding by phase to visually assess systematic biases (e.g., all σ-phase points above the diagonal).

## (iv) Recommendation

**Major Revision.** The core ML approach is well-motivated and the results are promising, but the evaluation methodology needs strengthening in several critical areas: nested CV, confidence intervals, multiple train/test splits, and learning curves. These are standard expectations for ML in materials science publications. Once addressed, the paper would be suitable for PRB.
