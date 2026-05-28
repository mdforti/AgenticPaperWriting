# Editorial Decision — Physical Review B (Second Review)

**Manuscript:** "Data-efficient machine-learning of complex Fe–Mo intermetallics using domain knowledge of chemistry and crystallography"
**Authors:** M. Forti, A. Malakhova, Y. Lysogorskiy, W. Zhang, J.-C. Crivello, J.-M. Joubert, R. Drautz, T. Hammerschmidt
**Submitted as:** Regular Article
**Date of Decision:** May 28, 2026

---

## DECISION: Accept

I have carefully read the revised manuscript, the point-by-point response, and the original reviewer comments. The authors have addressed all major concerns raised by the three reviewers and the 11 editorial requirements from the previous round. I am pleased to recommend acceptance for publication as a Regular Article in Physical Review B.

---

## Assessment of Revisions

The authors' response is thorough and the manuscript has been substantially strengthened. Below I evaluate each area of concern:

### Reviewer 1 — Computational Materials Physics

| Concern | Status | Evidence |
|---------|--------|----------|
| DFT convergence (k-point) | ✅ Resolved | Table 3: convergence table for R, M, P, δ; difference <0.5 meV/atom |
| NM hcp Fe reference state | ✅ Resolved | §2.1: justification paragraph added; magnetic energy discussed |
| BOP moment order (μ₄–μ₅) | ✅ Resolved | §2.2.1: tests with higher moments change RMSE by <2 meV/atom |
| CNAV vs. per-site information loss | ✅ Resolved | §3.2: CNAV improves RMSE 20–40% over per-structure, ~10% over per-site |
| Pulay stress / ENCUT constancy | ✅ Resolved | ENCUT fixed at 450 eV across all E–V points; third-order Birch–Murnaghan specified |

### Reviewer 2 — Machine Learning for Materials Science

| Concern | Status | Evidence |
|---------|--------|----------|
| Data leakage in feature selection | ✅ Resolved | Explicitly stated: feature selection nested inside 5-fold CV loop |
| Confidence intervals on RMSE | ✅ Resolved | Table 2: 95% CI from bootstrap (10,000 resamples); p<0.01 BOP vs ACE |
| Single train/test split | ✅ Resolved | Supplementary Table S1: 10 repeated stratified splits |
| Learning curves | ✅ Resolved | Figure 6: RMSE vs N = 50, 100, 150, 209 |
| Hyperparameter reporting | ✅ Resolved | Supplementary Table S2 |
| Reproducibility / random seeds | ✅ Resolved | numpy=42, sklearn=42, Python random=42; scikit-learn v1.2 |

### Reviewer 3 — Thermodynamics & Phase Stability

| Concern | Status | Evidence |
|---------|--------|----------|
| Bragg–Williams / SRO sensitivity | ✅ Resolved | Supplementary Figure S2: L = ±5, ±10 kJ/mol; occupancies change <0.03 (except 6c: ~0.08) |
| Temperature choice (1700 K) | ✅ Resolved | §2.4: justified as matching experimental XRD annealing temperature |
| CALPHAD comparison | ✅ Resolved | Supplementary Figure S3: comparison with Jacob et al. (2000) |
| Quantitative site-occupancy metric | ✅ Resolved | Table 4: site-by-site Mo fractions; MAD = 0.04 |
| Generality / transferability claims | ✅ Resolved | §4.3: explicitly qualified; further validation required |

---

## Notes for Final Publication

The following minor points were not explicitly addressed in the response; the authors are encouraged to consider them during proof stage but they do not require another round of review:

1. **Figure 3 inset** (R1 Minor 5): An inset zooming into the low-energy region (<0.1 eV/atom) would aid visual assessment of the most physically relevant structures.
2. **VotingRegressor scaling** (R2 Minor 1): Clarify whether individual model predictions were scaled before averaging in the ensemble.
3. **Magpie baseline composition** (R2 Minor 2): Specify whether Magpie was computed using the full 262-structure training set or only simple-phase compositions.
4. **Feature selection threshold sensitivity** (R2 Minor 3): The 0.5 meV/atom convergence criterion is tight; a brief sensitivity note would be informative.
5. **R-phase crystallographic table** (R3 Minor 4): A table of Wyckoff positions, multiplicities, and coordination numbers for the R phase would aid readers unfamiliar with this structure.

These are minor suggestions and do not affect the scientific validity of the manuscript.

---

## Recommendation

The manuscript is scientifically sound, the revisions are comprehensive, and all substantive concerns have been resolved. I recommend **Acceptance** as a Regular Article in Physical Review B.

---

*Editor*
*Physical Review B*
