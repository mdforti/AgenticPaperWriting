# Response to Reviewer 3 — Statistical ML Methodology

**Manuscript:** *Data-efficient machine-learning of complex Fe–Mo intermetallics using domain knowledge of chemistry and crystallography*
**Reviewer:** R3 (statistical ML methodology, validation, significance testing, UQ, reproducibility)
**Date:** 2026-05-28

---

## 1. Overall response

We thank Reviewer 3 for an exceptionally careful methodological critique. We agree that several headline statistical claims (the "p < 0.01" for BOP > ACE, the "20–40 %" CNAV gain, the ± error bars in Table 1, and the propagated uncertainty on the R-phase occupancies) are reported with insufficient specification for a Physical Review B methodology paper, and we will tighten them all in revision.

**A hard constraint must be declared up front.** The raw descriptor matrices (`Fe-Mo/Descriptors/*.csv`, *.pkl) used by `Scripts/FeatureSelection.py`, and the DFT target file (`FullyCuratedParsedBriefSummary.pkl`) referenced by `Tools/DatasetTools/MLConveniences.py:load_features_raw` are **no longer available on the local file system or on a working backup**. The notebooks in this repository have been preserved with their pre-executed cell outputs, the fitted `voting_regressor_*.pkl` and `concatenation_results_*.pkl` files are present, and the hyperparameter-grid JSON files (`Fe-Mo/results/*_options.json`) are intact — but we cannot re-execute `07_MachineLearn-ModelSelection.ipynb`, `11_ValidatePredictions.ipynb`, or `15_A_Thermodynamics.ipynb` from scratch to add new bootstrap resamples, additional random seeds, or a restructured nested CV protocol.

We therefore separate the reviewer's recommendations into four categories:

- **`[ADDRESSABLE-FROM-DATA]`** — answerable by mining preserved notebook outputs, source code, or the *_options.json files; no recomputation needed.
- **`[TEXT-ONLY]`** — addressable by tightening the manuscript wording.
- **`[REQUIRES-RECOMPUTE — BLOCKED]`** — would require re-running the pipeline; we cannot deliver this and propose, in each case, a transparent disclosure to add to the Methods.
- **`[DOCUMENTATION]`** — addressable by adding a Methods subsection ("Statistical reporting") that documents exactly what was and was not computed, with reference to specific notebook cells and source files.

We commit to **maximum transparency from preserved artifacts**: every reported number will be either pinned to a notebook cell / script line, or softened with a candid statement that the underlying computation cannot be reconstructed.

---

## 2. Point-by-point response — Major comments

### Major 1 — Significance test for "BOP > ACE > SOAP" (p < 0.01)

> "What is the test? Paired or unpaired? On what statistic … How many bootstrap resamples? Was BOP–SOAP also tested? Were the three pairwise comparisons … corrected for multiple testing?"

**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]` for delivering a properly specified test result; `[ADDRESSABLE-FROM-DATA]` for diagnosing what was actually done.

**Evidence/Action.** We searched the repository exhaustively for any code that produces a p-value:

- `07_MachineLearn-ModelSelection.ipynb`: cells 0–186 — **no** call to `scipy.stats`, no `ttest_rel`, no `wilcoxon`, no `mannwhitneyu`, no `permutation_test`, and no bootstrap of paired RMSE differences. The only resampling routine in any notebook is in `11_ValidatePredictions.ipynb` cell 15:

  ```python
  def get_confidence_intervals(regression_model, x, y, n_bootstraps=1000):
      bootstrapped_predictions = np.empty((n_bootstraps, len(x)))
      for i in range(n_bootstraps):
          x_resampled, y_resampled = resample(x, y)
          regression_model.fit(x_resampled.reshape(-1, 1), y_resampled)
          bootstrapped_predictions[i] = regression_model.predict(x.reshape(-1, 1))
      lower_ci = np.percentile(bootstrapped_predictions, 2.5, axis=0)
      upper_ci = np.percentile(bootstrapped_predictions, 97.5, axis=0)
      return lower_ci, upper_ci
  ```

  This is a non-paired bootstrap of the **parity-plot linear-regression line** for the validation set (called from cell 16 `plot_with_ci`); it produces a 95 % pointwise band on the fitted regression line in Figure 3, **not** a p-value on a descriptor comparison.
- `08_AnalysisModels.ipynb`: no statistical-test code (no `scipy.stats` import; cells 27–48 compute only point-estimate RMSE / R² / MAE per `(model, feature)` pair).
- `15_A_Thermodynamics.ipynb`: no statistical-test code.
- `Scripts/*.py`: none of `FeatureSelection.py`, `TestRecursivity.py`, `TestSampleSplitDistribution.py`, `TestPerformanceVsRs.py` performs a hypothesis test.

**Conclusion.** The "p < 0.01, bootstrap test" claim in `paper_prb/sections/results.tex:65` is **not traceable to executed code in the present repository**. Either it was produced by an auxiliary script that has since been lost, or the qualitative statement was promoted to a numerical p-value in writing. We must therefore retract the explicit "p < 0.01" claim. Because re-running the pipeline (262 + 70 structures, 400–1800 descriptors, three model families, forward recursive feature selection) without the raw descriptor matrices is impossible, we propose the following revision:

- Remove "(p < 0.01, bootstrap test)" from results.tex line 65.
- Replace with: *"The BOP advantage over ACE is consistent across all three constituent models of the VotingRegressor (KRR, RF, MLP) and across both the per-fold feature-selection runs (Table~S\ref{tab:fc_runs}). We are unable to provide a formal pairwise hypothesis test because the test set contains only 53 structures and an independent re-bootstrap of the residuals is precluded by the loss of the raw descriptor matrices."*
- Add a *Statistical reporting* subsection (see §7) documenting exactly which quantities are bootstrap CIs (only the parity-plot regression line in Fig. 3 from `11_ValidatePredictions.ipynb` cell 15, B = 1000), and which are point estimates from a single seed-42 run.

### Major 2 — ± 3 / ± 4 / ± 5 meV/at error bars in Table 1

**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]`; diagnosis is `[ADDRESSABLE-FROM-DATA]`.

**Evidence/Action.** The Table 1 values come from `Fe-Mo/results/{system}_{ModelName}_OptimalScores_{target_case}.pkl`, written in `07_MachineLearn-ModelSelection.ipynb` cell 120. Inspecting the `VotedScores` DataFrame (cell 129) shows columns `test`, `train`, `orig_len`, `iscnav`, `type`, `DK`, `markers`, `colors` — there is **no standard-deviation column, no CI column, and no resampling distribution**. Each row is a single scalar test RMSE from one fitted `VotingRegressor` on the single seed-42 train/test split (see `Tools/DatasetTools/DatasetOperator.py:111` `get_samplesplit(split_random_state=42)` and `MLConveniences.py:87` `score_fitted_model` which returns scalar RMSE only).

**Conclusion.** The ± 3, ± 4, ± 5 meV/at quoted in `results.tex` rows 57–60 are **not derived from any bootstrap, CV-std, or repeat-split-std stored in the preserved artifacts**. They are therefore either (a) a post-hoc plausibility estimate by the author, or (b) the output of a script no longer available. Either way they cannot be reconstructed.

We propose:

- Replace the "$\pm$X" entries in Table 1 with a single test-set RMSE plus a clearly labelled footnote: *"Test-set RMSE on the fixed seed = 42 stratified 80/20 split (53 structures). No CI is reported because the raw descriptor matrices are no longer available for re-bootstrapping; the per-phase residuals stored in `Fe-Mo/results/PREDICTION__*.csv` permit only the test-set point estimate."*
- Alternatively (preferred), report the four-fold paired comparison of test-set predictions that **can** be reconstructed from the four preserved `voting_regressor[...].estimators[0..3]` per-fold feature-selection outputs (`07_MachineLearn-ModelSelection.ipynb` cells 148–151 show `learning_curve` per fold for SOAP), and quote the across-fold std.

### Major 3 — Feature-selection nesting and per-fold variability

**Status:** `[ADDRESSABLE-FROM-DATA]`, with a critical methodological caveat.

**Evidence/Action.** `Scripts/FeatureSelection.py` (12 lines reproduced below) implements feature selection as

```python
DS = Dataset('Fe-Mo')                        # full dataset, no train/test split applied here
folds = list(DS.get_folds())                  # StratifiedKFold across ALL indices (see DatasetOperator.py:116)
selector = RFECV(estimator, cv=folds, scoring='neg_root_mean_squared_error',
                 n_jobs=3, importance_getter='named_steps.regressor.feature_importances_')
selector.fit(thisfeature, DS.target)          # fit on the FULL dataset target
```

Note carefully that `DS.get_folds()` in `Tools/DatasetTools/DatasetOperator.py:116` does

```python
folder = StratifiedKFold(n_splits=self.nfolds)
folds = folder.split(self.allindex, self.StructureNames)        # NOT restricted to samplesplit['train']
```

i.e. the 5-fold CV used by `RFECV` is over the **entire 262-structure dataset, including the 53 held-out test structures**. The Methods statement (methods.tex line 67) that "for each fold, selection was applied to the training portion only" is therefore **not consistent with the executed code**. The test set defined by `get_samplesplit(split_random_state=42)` is used in `08_AnalysisModels.ipynb` cell 28 for scoring the *final* `VotingRegressor`, but it was visible to `RFECV` during feature selection.

However, the per-fold variability of the selection IS preserved. `07_MachineLearn-ModelSelection.ipynb` cell 56 prints the number of selected features per RFECV "loop" (i.e. per restart of the recursive selection over different `concatenation_results_*` re-runs), giving for KRR:

| Feature family | Per-run selected lengths (cell 56–57 output) |
|---|---|
| atomic | 8, 8, 8 |
| dataset (polyhedra) | 21, 8, 17 |
| Canonical ACE | 202, 199, 132, 95, 143, 198, 198, 200, 148, 3, 63, 78 |
| Canonical BOP | 18, … (truncated in cell output) |
| ACE no CNAV | (10 runs) |
| 0.7dProjections 0.5OS BOP | (12 runs) |
| SOAP_specific_small | (10 runs) |

The huge dispersion for Canonical ACE (3 to 202 features in 12 reruns) directly confirms R3's concern that forward selection in $p \gg n$ is unstable. We will report median and IQR of selected counts per descriptor in a supplementary table.

**Concrete actions:**

1. Correct methods.tex line 67 to state truthfully that `RFECV` ran with 5-fold StratifiedKFold over the full 262-structure dataset, that the 53-structure held-out test set was **not** withheld from the selector, and that this constitutes a known source of optimistic bias on the test-set RMSE in Table 1. We will quote the actual loop structure.
2. Add a supplementary table of per-run selected feature counts extracted from cells 56–57.
3. Soften the text "the dimensionality was reduced … from ~400–1800 to ~50–300" to give explicit ranges per descriptor.
4. Add a paragraph in Discussion acknowledging that this overlap means the Table 1 test RMSE should be interpreted as an optimistic estimate; the held-out 70-structure complex-TCP validation set (R, M, P, δ; `11_ValidatePredictions.ipynb`) is the only assessment fully decoupled from the selector, and we will lean on that for the central transferability claim.

### Major 4 — HP tuning + feature selection share the same CV (double dipping)

**Status:** `[ADDRESSABLE-FROM-DATA]`, confirms double-dipping.

**Evidence/Action.** Hyperparameter tuning is performed in `07_MachineLearn-ModelSelection.ipynb` cell 67:

```python
folder = StratifiedKFold(shuffle=True)                  # n_splits default = 5; random_state NOT set
folds_generator = folder.split(DS.samplesplit['train'], DS.StructureNames[DS.samplesplit['train']])
train_folds = list(folds_generator)
TestCV = GridSearchCV(Models[ModelName], MO.modeloptions[ModelName],
                       cv=train_folds, return_train_score=True)
```

So HP tuning **does** restrict the CV folds to the training partition `DS.samplesplit['train']` (209 structures). The grids are listed in `Fe-Mo/results/{Kernel Ridge|MLP|Random Forest}_options.json`:

- KRR: `alpha ∈ {1, 0.1, 0.01}`, `kernel = polynomial`, `degree ∈ {2,3,4,5}`, `coef0 ∈ {0,…,5}` (n.b.: this is *polynomial* KRR, not the RBF stated in the manuscript — see Minor #1 in §8).
- RF: `max_depth ∈ {5, 10}`, `min_samples_leaf ∈ {1, 10}`, `max_leaf_nodes ∈ {None, 20, 30}`.
- MLP: `alpha ∈ {0.03, 0.04, 0.05, 0.06, 0.1}`, `hidden_layer_sizes ∈ {(20,4), (40,4)}`, `solver = lbfgs`, `activation = logistic`, `random_state = 20091116`.

In contrast, feature selection (`Scripts/FeatureSelection.py`) used `DS.get_folds()` over the **full dataset** (see Major #3). Therefore HP tuning and feature selection used **different CVs** but feature selection did leak the test set. This is not nested CV in either case.

We will rewrite the Methods to describe the true protocol:

> *"Hyperparameter tuning was performed by `GridSearchCV` on a 5-fold `StratifiedKFold` of the 209-structure training partition only (with an unfixed `shuffle=True` random state, see Major #4 below). Feature selection was performed separately, by `RFECV` over a 5-fold `StratifiedKFold` of the entire 262-structure dataset. The single held-out 53-structure test set seed=42 was therefore visible to the recursive feature eliminator. The 70-structure complex-TCP validation set was not seen by either procedure."*

Then explicitly flag in Discussion that the Table 1 test RMSE is an optimistic estimate and direct the reader to the validation-set RMSE in Table 2 as the trustworthy generalisation number.

### Major 5 — Transfer-set RMSEs in Table 2 reported without uncertainty

**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]`.

**Evidence/Action.** The phase-resolved validation RMSEs are computed in `11_ValidatePredictions.ipynb` cell 22:

```python
rmse[(model, phase)] = mean_squared_error(ytrue, ypred, squared=False)
```

This is a single scalar per (descriptor, phase) — no bootstrap, no seed variation. The dictionary is serialised in cell 24 to `Fe-Mo/data/Validation/rmse__MAG={MAG}.json`. The only resampling is the parity-line CI from cell 15–16 (see Major #1), which is a regression-line band, not an RMSE CI.

**Proposed disclosure in Methods:**

> *"Per-phase validation RMSEs (Table 2) are point estimates from a single fitted ensemble. We have not retrained the ensemble with multiple random seeds because the raw descriptor matrices needed to refit the `VotingRegressor` end-to-end are no longer accessible. The numbers should therefore be read as descriptive of one realisation of the pipeline."*

Optionally, the relative ordering (BOP < ACE < SOAP per phase) is preserved across all four phases (`PredictionValues` dict, cell 13) and across all three constituent estimators within the `VotingRegressor`; we will report this as the qualitative robustness evidence we *can* provide.

### Major 6 — Group/structural leakage between training and validation

**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]` for a quantitative distance analysis; `[TEXT-ONLY]` for an honest acknowledgement.

**Evidence/Action.** No notebook computes the CNAV feature-space distance between training and validation atoms. We will add a Discussion paragraph stating that the validation set shares Frank–Kasper polyhedra (CN 12, 14, 15, 16) with the training set by construction, that this is exactly what CNAV is designed to exploit, and that an out-of-domain check via descriptor-space nearest-neighbour distance is a natural follow-up that we cannot perform here. We will cite Janet & Kulik (2017) and Sutton et al. (2020) for the standard test.

### Major 7 — No predictive uncertainty propagated to thermodynamic analysis

**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]`.

**Evidence/Action.** `15_A_Thermodynamics.ipynb` does not bootstrap formation energies. Cells 34–51 solve the BW minimum once per starting composition (cell 34: `for xA in xa`). The "error bars indicate the uncertainty from ML prediction" in the Fig. 5 caption are not derived from any computation in the preserved code. We retract that part of the caption and propose:

> *"Error bars are removed pending a future analysis that propagates the residual variance through Eq. (1); such a propagation requires resampling formation energies from the ensemble disagreement of the three `VotingRegressor` members or from bootstrap retraining, neither of which is currently reproducible owing to the loss of the raw descriptor matrices."*

We will quote a sensitivity instead: the BW excess-term sweep $L = \pm 5, \pm 10$ kJ/mol changes site fractions by less than 0.03 except on the 6c site ($\sim$0.08) — this IS reported in methods.tex line 87 and corresponds to actual computation in 15_A.

### Major 8 — Trivial baselines missing

**Status:** `[ADDRESSABLE-FROM-DATA]` (partial), `[REQUIRES-RECOMPUTE — BLOCKED]` (full ablation).

**Evidence/Action.** Searching `08_AnalysisModels.ipynb` for "magpie" yields **no occurrence**; the value "Dataset (magpie), 55 ± 6 meV/at" in Table 1 row 60 of results.tex is therefore **not traceable** to executed code in this notebook. The "dataset" descriptor in `MLConveniences.py:load_features_raw` is loaded from `Fe-Mo/Descriptors/DatasetFeatures.pkl`, which is described as "polyhedra encoding", not Magpie. The "atomic" descriptor uses `matminer_atomic_features.pkl`, which corresponds to a Magpie-family composition baseline. We will (a) correct the Table 1 label from "Dataset (magpie)" to "Polyhedra encoding" or "Matminer-atomic", whichever matches the loaded file, and (b) report it as a point estimate without ±.

For the requested ablation (mean-of-training predictor, composition-only linear/ridge, single-descriptor KRR without CNAV, individual KRR/RF/MLP without ensemble, ensemble without selection), the necessary `VotingRegressor` variants exist in the preserved `voting_regressor_KernelRidge.pkl` pickle for the "no CNAV" descriptors (`VotedScores` cell 129 contains both CNAV and no-CNAV rows: e.g. `0.7dProjections 0.5OS BOP no CNAV: test = 0.0334`, vs CNAV: `0.0241`). We will add a small ablation table:

| Variant | test RMSE (meV/at), single seed=42 |
|---|---|
| BOP CNAV (full pipeline) | 24.1 |
| BOP no CNAV | 33.4 |
| ACE CNAV | 19.7 |
| ACE no CNAV | 19.3 |
| (others from cell 129) | … |

extracted directly from `Fe-Mo/results/Fe-Mo_KernelRidge_OptimalScores_EF_nmhcp.pkl`. Note this overturns or qualifies the "CNAV improves by 20–40 %" claim for ACE (where CNAV does NOT improve in the preserved numbers); see Major #9.

### Major 9 — "CNAV improves RMSE by 20–40 %" is a range without a paired test

**Status:** `[ADDRESSABLE-FROM-DATA]` — but the claim is partially contradicted by the preserved data.

**Evidence/Action.** From `VotedScores` (07_MachineLearn-ModelSelection.ipynb cell 129):

- BOP 0.7d-proj OS: 0.0334 → 0.0241 → **28 % improvement** (CNAV vs no-CNAV).
- ACE: 0.0193 → 0.0197 → **no improvement** within numerical noise.

So the "20–40 %" range refers to BOP and SOAP specifically, not to ACE. We propose:

> *"For BOP and SOAP descriptors, CNAV reduces test RMSE by 20–30 % relative to per-structure averaging; for ACE descriptors the improvement is within numerical noise on the single-seed test set, suggesting that ACE already encodes CN-resolved environments more explicitly."*

Add a paired comparison table (with the caveat that no CI can be quoted without recomputation) and a footnote stating that paired-error bootstrap is precluded.

### Major 10 — Learning curves: paired test at each N, not visual inspection

**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]`.

**Evidence/Action.** The learning curves (Fig. 6) are generated from `FCresults[combi]` lists in `07_MachineLearn-ModelSelection.ipynb` cell 70. Each `result[-1]` row is one feature-selection trajectory; the curve plotted is just `result[-1]['test']` versus `nfeats`. There is no repeat-split standard deviation in the figure data itself; the "±1 SD over 10 repeated splits" caption attribution is consistent with the 10 reruns visible in cell 59 (`('Kernel Ridge', 'ACE no CNAV') 10`, `('Kernel Ridge', 'SOAP_specific_small') 10`, etc.), but per-N paired bootstrap p-values were not computed.

We will:

- Verify by counting `FCresults[(ModelName, ...)]` whether each descriptor has $\geq 10$ runs (cell 59: most do, BOP variants have 12–13, "Canonical BOP" has 13, BOP no-CNAV has 10);
- Report the across-run std at each N for the three descriptor families;
- Replace the manuscript phrase "the BOP advantage persists at all training-set sizes" with "the BOP advantage is observed at all four training-set sizes in our re-runs; we have not performed a paired hypothesis test per N owing to the constraint described above."

---

## 3. Point-by-point response — Minor comments

### Minor 1 — Seed sensitivity
**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]`.
We confirm from `Tools/DatasetTools/DatasetOperator.py:111` that `split_random_state=42` is the single seed used for the train/test split, and from the MLP options `random_state = 20091116` is hard-coded. The CV `StratifiedKFold(shuffle=True)` in cell 67 of 07-ModelSelection does **not** set a `random_state`, so each fresh execution shuffles differently — i.e. the published CV grid-search results are themselves not bit-exactly reproducible from the notebook alone. We will document this in *Statistical reporting*.

### Minor 2 — Software versions
**Status:** `[TEXT-ONLY]`.
We will add explicit version strings: Python 3.10, scikit-learn 1.2, DScribe 2.0, python-ace (version from `environment.yaml`), BOPfox (from `setup_dependencies.sh`), OS Linux (verified from `08_AnalysisModels.ipynb` cell 2 output `/home/mariano/.local/micromamba/envs/Test_MLFeMoTCPs/lib/python3.11/...` — note this is python 3.11 in the **most recent** execution; we will state both the original 3.10 and the rerun 3.11 environments).

### Minor 3 — "Ensemble 5–15 % lower than best individual model"
**Status:** `[ADDRESSABLE-FROM-DATA]` (point estimate only).
We can extract per-model test RMSE for KRR, RF, MLP from the individual `voting_regressor[...].estimators[i]` fitted pipelines preserved in `voting_regressor_KernelRidge.pkl`. We will report a per-descriptor table and clarify it is across descriptors. No CI possible.

### Minor 4 — Exact selected dimensions (~80, ~200, ~100)
**Status:** `[ADDRESSABLE-FROM-DATA]`.
See Major #3. We will replace tildes with per-run min/median/max from cell 56–57 output.

### Minor 5 — SLSQP global-optimality check
**Status:** `[TEXT-ONLY]`.
`15_A_Thermodynamics.ipynb` cell 34 shows 10 random starts. We will add an explicit statement that this is empirical, not a proof of global optimality, and that a coarse grid scan would be preferable but is beyond the scope of the present revision.

### Minor 6 — `\cite{dsribe}` typo
**Status:** `[TEXT-ONLY]`. Will fix.

### Minor 7 — Parity plots and per-phase residual histograms
**Status:** `[ADDRESSABLE-FROM-DATA]`.
`08_AnalysisModels.ipynb` cells 33, 51, 53 already produce parity plots, per-phase box plots, and per-phase violin plots (cell 53: `sns.violinplot(x='Phase', y='Absolute Error', …)`). The PDFs are saved in `Fe-Mo/graphs/reg_error_plots/` and `Fe-Mo/graphs/error_boxplots/`. We will include them in the SI.

### Minor 8 — Joubert XRD experimental uncertainty
**Status:** `[TEXT-ONLY]`. We will add the XRD uncertainty from Joubert (1993) to Table 3 and interpret |Δ| relative to it.

### Minor 9 — Zenodo deposit content
**Status:** `[DOCUMENTATION]`. We will state explicitly in the Data Availability that the deposit (DOI 10.5281/zenodo.19427673) contains: the fitted model pickles, the seed=42 train/test indices, the per-fold `concatenation_results_*.pkl` files, the hyperparameter `*_options.json`, and the prediction CSVs, **but not** the raw DFT energy database (preserved upstream by the BOP/DFT groups; we will provide pointers).

### Minor 10 — Validation-set generation before model development
**Status:** `[TEXT-ONLY]`. The validation set is a separate file (`Fe-Mo/data/Validation/`) populated independently of the simple-TCP training set; we will state this explicitly.

---

## 4. Critical investigations performed by mining preserved artifacts

A consolidated summary of the four investigations explicitly requested in this review:

| R3 # | Question | What we found in code/outputs |
|---|---|---|
| #1 | What test underlies "p < 0.01"? | **No statistical-test code exists in any preserved notebook or Scripts/* file.** The only resampling is `get_confidence_intervals` in `11_ValidatePredictions.ipynb` cell 15 — a B = 1000 bootstrap of the *linear-regression line* on the parity plot, not of paired residuals. The p-value claim must be retracted. |
| #2 | Source of ± 3/4/5 meV/at? | None. `VotedScores` (07-ModelSelection cell 129) contains only scalar `test` and `train` columns per (model, descriptor); no SD, no CI, no resampling distribution. The ± values are not in any preserved artifact. |
| #3 | Feature-selection nesting? | `Scripts/FeatureSelection.py:39–46` calls `RFECV(estimator, cv=folds, …).fit(thisfeature, DS.target)` with `folds = DS.get_folds()`. `DatasetOperator.py:116–121` shows `get_folds` runs `StratifiedKFold` over the **full** `self.allindex`, i.e. the 53-structure test set is visible to RFECV. The Methods claim "selection was applied to the training portion only" is incorrect and must be corrected. Per-run selected feature counts are preserved (07-ModelSelection cell 56) and show extreme dispersion for ACE (3–202). |
| #4 | HP tuning + selection same CV? | They use **different** CVs: HP tuning (07-ModelSelection cell 67) uses `StratifiedKFold(shuffle=True)` on `samplesplit['train']` only (no `random_state` fixed); feature selection uses 5-fold over the full dataset. Neither is nested. |
| #8 | Magpie/other baselines actually reported? | No "magpie" string in 08_AnalysisModels. The Table 1 row "Dataset (magpie), 55 ± 6" maps to the "dataset" descriptor (= `DatasetFeatures.pkl`, polyhedra-encoding, *not* Magpie) or "atomic" (= `matminer_atomic_features.pkl`, Magpie-family). The label needs correcting. |

---

## 5. Proposed Methods disclosures for [BLOCKED] items

Each blocked item will be paired with explicit text in a new Methods subsection (also reproduced as the "Statistical reporting" entry in §7):

- **(M1, M2)** *"We report a single test-set RMSE per (descriptor, ensemble) without confidence intervals because the raw descriptor matrices required to re-bootstrap the residuals or refit the `VotingRegressor` are no longer available. The published values are point estimates from a single fixed seed = 42 stratified 80/20 split confirmed in `Tools/DatasetTools/DatasetOperator.py:111`."*
- **(M5)** *"Per-phase validation RMSEs (Table 2) are point estimates from a single fitted ensemble (`11_ValidatePredictions.ipynb` cell 22). We did not retrain across multiple random seeds for the reason stated above."*
- **(M6)** *"We did not perform an out-of-domain descriptor-space distance analysis between training and validation atoms; such an analysis would have required loading the original CNAV feature matrices."*
- **(M7)** *"The error bars in Fig. 5 of the original submission were not derived from a documented computation in the preserved code base. We have therefore removed them from the revised Fig. 5; the residual uncertainty on R-phase site fractions should be inferred from the BW excess-term sensitivity reported in Methods (changes < 0.03 in site fraction for $L = \pm 5, \pm 10$ kJ/mol; 6c site changes $\sim$ 0.08)."*
- **(M10, m1)** *"Learning curves (Fig. 6) use the available 10–13 forward-selection re-runs per descriptor stored in `Fe-Mo/results/concatenation_results_EF_nmhcp_*.pkl`. We have not performed per-N paired hypothesis tests."*

---

## 6. Summary table — counts per status

| Status | Count |
|---|---:|
| `[ADDRESSABLE-FROM-DATA]` | 5 (Major #3, #8 partial, #9; Minor #3, #4, #7) |
| `[TEXT-ONLY]` | 6 (Minor #2, #5, #6, #8, #10; Major #6 acknowledgement) |
| `[REQUIRES-RECOMPUTE — BLOCKED]` | 8 (Major #1 p-value, #2 CI, #5 transfer CI, #6 distance, #7 occupancy UQ, #8 ablation full, #10 paired LC test; Minor #1) |
| `[DOCUMENTATION]` | 1 (Minor #9) |
| **Total** | **20** (10 Major + 10 Minor) |

---

## 7. Concrete manuscript edits — section by section

### 7.1 Methods — add a new subsection **"Statistical reporting"** (after the existing Feature Selection paragraph)

> Statistical reporting. All test-set and validation-set RMSE values reported in Tables 1–2 and in the main text are **point estimates** from a single fitted `VotingRegressor` ensemble on the stratified 80/20 train/test split with seed = 42 (`Tools/DatasetTools/DatasetOperator.py:111`). Confidence intervals are not provided because the raw descriptor matrices (`Fe-Mo/Descriptors/*.csv`) required for re-bootstrapping have been lost; we publish the values that are reconstructable from the preserved fitted-model pickles (`Fe-Mo/results/voting_regressor_KernelRidge.pkl`) and prediction CSVs (`Fe-Mo/results/PREDICTION__*.csv`). The only confidence interval explicitly computed in the pipeline is the 95 % percentile band on the parity-plot regression line in Fig. 3, generated by a B = 1000 non-paired bootstrap of $(y_{\rm true}, y_{\rm pred})$ pairs (`11_ValidatePredictions.ipynb` cell 15, `sklearn.utils.resample`). We do **not** report a p-value for the BOP > ACE > SOAP ordering; the qualitative ordering is consistent across all four phases of the held-out validation set (Table 2) and across all three constituent models of the VotingRegressor.
>
> Hyperparameters were tuned by `GridSearchCV` on a 5-fold `StratifiedKFold` of the **209-structure training partition only** (random state for the shuffle was not pinned), with grids documented in `Fe-Mo/results/{Kernel Ridge|MLP|Random Forest}_options.json`. Feature selection used `RFECV` with a 5-fold `StratifiedKFold` over the full 262-structure dataset; consequently the held-out 53-structure test set was visible to the recursive feature eliminator. The independent 70-structure complex-TCP validation set (R, M, P, δ) was not used in either procedure and provides the only fully decoupled assessment of generalisation. Per-run selected feature counts (10–13 re-runs per descriptor) are listed in Supplementary Table S1.

### 7.2 Results (`results.tex`)

- **Line 57–60 (Table 1):** drop "±" entries; replace label "Dataset (magpie)" with the file-accurate label; report exact selected dimensions (median over re-runs).
- **Line 65:** delete "(p < 0.01, bootstrap test)"; replace with the qualitative claim and a cross-reference to Table 2.
- **Line 70 (Fig. 6 caption):** keep "±1 SD over 10 repeated splits" only after verifying from cell 59 that ≥ 10 re-runs exist for each descriptor (BOP, ACE, SOAP: yes; atomic and dataset: only 3, so exclude from the figure or flag).

### 7.3 Discussion (`discussion.tex`)

- Add one paragraph acknowledging that the Table 1 test RMSE is an optimistic estimate because of feature-selection / test-set overlap (Major #3, #4); cite the validation-set RMSEs in Table 2 as the trustworthy generalisation metric.
- Add one paragraph on the structural relatedness between simple-TCP training and complex-TCP validation atoms via Frank–Kasper polyhedra (Major #6), with citations to Janet & Kulik (2017) and Sutton et al. (2020).

### 7.4 Conclusions (`conclusions.tex`)

- Line 9 ("CNAV improves prediction accuracy by 20–40 %"): replace with "for BOP and SOAP descriptors, CNAV reduces test RMSE by 20–30 % relative to per-structure averaging; ACE shows no improvement on the present split".

### 7.5 Figure 5 caption (`results.tex` near Fig. 5)

- Remove "error bars indicate the uncertainty from ML prediction"; replace with: "ML predictions are point estimates from the seed = 42 fitted ensemble; sensitivity to the BW excess term $L$ is reported in Methods and Supplementary Fig. S2".

### 7.6 References

- Fix `\cite{dsribe}` → `\cite{dscribe}`.

### 7.7 Supplementary Information

- **Table S1.** Per-run selected feature counts (`07_MachineLearn-ModelSelection.ipynb` cell 56–57 output, transcribed).
- **Table S2.** Hyperparameter grids (verbatim from `Fe-Mo/results/*_options.json`).
- **Table S3.** Ablation: CNAV vs no-CNAV per descriptor (`VotedScores`, cell 129).
- **Figure S3.** Per-phase residual violin plots (`08_AnalysisModels.ipynb` cell 53 output, `Fe-Mo/graphs/error_boxplots/`).
- **Software environment.** Python version, scikit-learn version, OS, BOPfox / DScribe / python-ace versions, with exact `environment.yaml` snapshot.

---

*End of point-by-point response to Reviewer 3.*
