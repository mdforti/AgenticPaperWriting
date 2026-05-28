# Referee Report — Reviewer 1 (Machine Learning for Materials Properties)

**Manuscript:** "Data-efficient machine learning of complex Fe–Mo topologically close-packed intermetallics using domain knowledge of chemistry and crystallography"  
**Report round:** 1

---

## Summary

The manuscript describes a machine-learning workflow for predicting formation enthalpies of Fe–Mo topologically close-packed intermetallic phases using three families of site-resolved descriptors — bond-order-potential (BOP) moments, atomic cluster expansion (ACE), and species-resolved SOAP — combined with a coordination-number-resolved averaging (CNAV) scheme designed to capture the Frank–Kasper site hierarchy. Models are trained on 209 simple and R-phase TCP structures and tested on a 53-structure hold-out set and a separately held-out 70-structure external validation set covering R, M, P, and δ phases. The central quantitative claim is that CNAV reduces the BOP test error by 32% and that kernel ridge regression reaches 19–24 meV/atom test errors. The work is technically detailed and the thermodynamic post-processing section adds physical relevance. However, the manuscript has one major methodological gap that must be addressed before publication: the absence of a parity plot for the 20% test-set predictions.

---

## Major Comments

**1. Missing test-set parity plot.** The manuscript reports test-set RMSE values in Table 2 for eleven descriptor–model combinations, but provides no scatter plot of predicted versus DFT formation energies for the 20% hold-out test set. The validation parity plots (Fig. 5) cover only the external complex-phase validation set. A parity plot for the internal test set is essential in a PRB manuscript for two reasons: it reveals systematic biases or outlier structures that a scalar RMSE conceals, and it allows the reader to assess whether the RMSE is dominated by a small number of high-energy outliers or is representative of the full energy range. The figure `Fe-Mo_OptimalRegresorComparison.pdf` shows a bar chart of RMSE values across models but does not contain the required scatter plot. The authors must add a parity plot of predicted versus DFT formation energies for the test set (at minimum for the three best KRR models — BOP+CNAV, ACE+CNAV, SOAP+CNAV) before the manuscript can be accepted.

**2. Missing description of error distribution and outlier analysis.** Related to the above, the repository appears to contain an error-distribution figure (`Figure_Result_ErrorDistribution.png`) that was not included in the manuscript. Given that the energy range spans from −42.8 to 720.5 meV/atom — a very wide window — the reader cannot determine from RMSE alone whether the model performs uniformly or is substantially better in the near-hull region than in the high-energy tail. The authors should either include the error distribution figure or discuss the composition- and energy-resolved error structure in the text.

**3. Feature selection and data-leakage risk.** The manuscript does not describe whether any feature selection or dimensionality reduction was applied to the descriptor vectors before regression, nor does it state whether the number of features reported for each descriptor family reflects post-selection dimensions. If any forward recursive feature selection or PCA pre-processing was performed, it is critical that this step was nested inside the cross-validation loop and not applied to the full training set before splitting. The omission of this information prevents the reader from ruling out data leakage. The Methods section should explicitly state whether feature selection was performed and, if so, how it was controlled.

---

## Minor Comments

**1. SOAP cutoff radius justification.** The SOAP descriptor is computed with a cutoff radius of 4.0 Å, a value that is at the lower end of what is typically used for TCP phases. The R phase, for example, has coordination shells extending to 16-fold environments; at 4.0 Å the descriptor may capture only the nearest-neighbour shell for some Wyckoff sites. The authors should either justify this choice by comparison with a larger cutoff (e.g., by stating that 4.0 Å and 6.0 Å give equivalent CV errors) or acknowledge it as a potential limitation.

**2. VotingRegressor performance not quantified in the text.** The Methods section introduces the VotingRegressor ensemble of KRR, MLP, and RF but the Results section focuses exclusively on KRR. The paper does not report whether the VotingRegressor outperforms KRR alone and by how much, nor does it present a figure or table showing the ensemble test-set RMSE. If the ensemble was evaluated and found not to outperform the best individual model, this should be stated explicitly so that the reader understands why the paper focuses on KRR.

**3. Cross-validation versus test-set RMSE comparison.** Table 2 reports only test-set RMSE. Including the cross-validation RMSE for each representation would help the reader assess whether any models are overfitting or whether the training–test gap is unexpectedly large. The learning-curve figure (Fig. 2) provides partial information for KRR but not for MLP and RF.

**4. ACE hyperparameter documentation.** The ACE descriptor is documented as "lmax=321, corresponding to lmax=3 for pair terms, lmax=2 for three-body terms, and lmax=1 for four-body terms." While this notation is internally consistent, it does not specify the radial cutoff, the number of radial basis functions, or the body-order truncation for the ACE expansion. These parameters materially affect the descriptor quality and should be reported in the Methods.

---

## Recommendation

I recommend publication in Physical Review B after major revision. The work is scientifically sound, the CNAV concept is well-motivated and convincingly demonstrated, and the thermodynamic post-processing adds genuine value. The requirement for a test-set parity plot and the clarification of feature selection procedures are necessary for this to constitute a fully reproducible and rigorous ML study at PRB standards. Once these items are addressed, I expect the manuscript to be suitable for publication.
