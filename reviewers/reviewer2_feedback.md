# Reviewer 2 Feedback

## Summary
The manuscript presents a thoughtful small-data learning workflow for complex Fe--Mo TCP phases and contains several good methodological ingredients, including stratified splitting, recursive feature selection, a comparison across descriptor families, and a downstream thermodynamic use case. The topic is appropriate for Physical Review B and of clear interest to the materials-ML community. My main concern is not the overall direction but the level of quantitative reporting. Several claims are presently easier to infer from the repository notebooks than to verify directly from the manuscript. In particular, the external-validation metrics, the mean-absolute-error reporting, and the details of the ensemble construction should be documented more fully.

## Major comments
1. The train/test/CV protocol is promising but needs to be reported more explicitly. The manuscript states that a phase-stratified 80/20 split is used and that recursive feature selection is nested inside fivefold stratified cross-validation on the training subset. This is good practice. However, the paper should say plainly whether the final test set remains untouched during feature ranking, hyperparameter optimization, and voting-regressor construction for every descriptor family. A concise workflow diagram or paragraph with the exact order of operations would eliminate any concern about leakage.

2. The manuscript currently reports a strong RMSE table for the internal test split but does not provide the corresponding MAE and $R^2$ values, although the notebooks compute them. For a small-data benchmark paper, these additional metrics are not optional. The authors should add a supplementary table, or expand Table I, to include MAE and ideally $R^2$ for the principal models.

3. The external validation on $R$, $P$, $M$, and $\delta$ must be tabulated. Right now the text says that the parity notebook computes and annotates phase-resolved RMSE values, but the manuscript leaves them qualitative. This is the central transfer-learning result and must be shown numerically for each descriptor family and phase.

4. The role of the VotingRegressor is underexplained. The paper states that it combines independently fitted pipelines, but it does not say how many constituent estimators are used, whether they differ by random seed, feature subsets, or folds, and how the reported uncertainty proxy `std_votes` should be interpreted. Since the validation notebook exposes this quantity explicitly, the manuscript should explain it.

5. The comparison between ACE and BOP needs more nuance. The internal test table shows ACE/KRR with the lowest RMSE, while the Discussion emphasizes BOP as the preferred descriptor. That may be justified by external transfer and physical interpretability, but the manuscript should make the distinction explicit rather than implying that one descriptor wins uniformly across all criteria.

## Minor comments
1. Please report the exact scikit-learn version used for the archived models.
2. The manuscript would benefit from a short paragraph on why the archived MLP grid uses logistic activations and `lbfgs`, which differs from more common modern choices.
3. The starting feature counts are useful; please also state the final retained feature counts for the best ACE, BOP, and SOAP pipelines.
4. If possible, include confidence intervals or repeated-split variability for the internal benchmark, especially because the data set is modest in size.
5. The manuscript should distinguish clearly between the curated 292-structure count and the 261 structures actually scored in the downstream analysis.

## Recommendation
Major Revision
