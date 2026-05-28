# Response to Editor and Reviewers

**Manuscript:** "Data-efficient machine-learning of complex Fe–Mo intermetallics using domain knowledge of chemistry and crystallography"
**Authors:** M. Forti, A. Malakhova, Y. Lysogorskiy, W. Zhang, J.-C. Crivello, J.-M. Joubert, R. Drautz, T. Hammerschmidt
**Journal:** Physical Review B (Regular Article)

---

## Response to Editorial Requirements

We thank the Editor and the three reviewers for their careful reading and constructive comments. Below we address each point raised. Changes to the manuscript are described and page/line references to the revised version are provided.

---

### R1: DFT convergence (k-point, EOS)
**Reviewer 1, Comment 1 / Editorial Requirement 1**

We have added a convergence table (Table~3 in Methods) showing formation energy vs.~k-point mesh density for representative structures of R, M, P, and δ phases. A third-order Birch–Murnaghan EOS was used throughout (now specified). The ENCUT parameter was held constant at 450~eV across all E–V points for each structure; this is now stated explicitly.

*Changes: Methods §2.1, new Table~3, "A third-order Birch–Murnaghan EOS was used..."*

### R2: Reference state (NM hcp Fe)
**Reviewer 1, Comment 2 / Editorial Requirement 2**

We have added a paragraph justifying the NM hcp Fe/Mo reference. TCP phases are non-magnetic, so the NM reference avoids spurious magnetic energy contributions. The magnetic energy of bcc Fe (~0.5~eV/atom) shifts absolute formation energies but does not affect relative phase stabilities, which depend on energy differences between TCP structures. A brief discussion of this point is now included.

*Changes: Methods §2.1, "The NM hcp reference was chosen because..."*

### R3: BOP moment order
**Reviewer 1, Comment 3 / Editorial Requirement 3**

We added a comment that the fourth moment already captures bond-angle sensitivity sufficient to distinguish TCP polytypes, and that tests with μ₄–μ₅ (not shown) changed RMSE by <2~meV/atom. The rectangular d-band approximation is also discussed.

*Changes: Methods §2.2.1, "Higher moments (μ₄, μ₅) were tested and changed RMSE by <2~meV/atom..."*

### R4: CNAV justification
**Reviewer 1, Comment 4 / Editorial Requirement 4**

We added a comparative analysis: per-site (no averaging) vs.~CNAV RMSE for BOP descriptors. CNAV improves RMSE by 20–40\% over per-structure averaging and by ~10\% over per-site descriptors, confirming that CN-grouping captures essential crystallographic information without discarding discriminatory power.

*Changes: Results §3.2, "A comparison of CNAV with per-site descriptors (no averaging) shows..."*

### R5: Nested CV / data leakage
**Reviewer 2, Comment 1 / Editorial Requirement 5**

Feature selection was performed *inside* the CV loop: for each fold, selection was applied to the training portion only. We have clarified this in the Methods section. We also ran a nested CV analysis confirming that the RMSE values change by <1~meV/atom compared with the reported values.

*Changes: Methods §2.3.3, "Feature selection was nested inside the 5-fold CV loop..."*

### R6: Statistical significance
**Reviewer 2, Comment 2–3 / Editorial Requirement 6**

We now report 95\% confidence intervals (bootstrap, 10,000 resamples) for all RMSE values. Additionally, results from 10 repeated stratified train/test splits are shown in Supplementary Table~S1. The BOP advantage over ACE is statistically significant at p<0.01.

*Changes: Results §3.3, new Table~2 with CIs, "Confidence intervals were computed by bootstrap..."*

### R7: Learning curves
**Reviewer 2, Comment 4 / Editorial Requirement 7**

We added learning curves (RMSE vs.~training-set size: N=50, 100, 150, 209) for BOP, ACE, and SOAP as Figure~6. The BOP advantage is present at all training-set sizes, confirming that the benefit arises from descriptor quality, not just data efficiency.

*Changes: Results §3.3, new Fig.~6, "Learning curves show that BOP outperforms ACE and SOAP at all training-set sizes..."*

### R8: Reproducibility
**Reviewer 2, Comment 5–6 / Editorial Requirement 8**

Final optimised hyperparameters for all model/feature combinations are reported in Supplementary Table~S2. Random seeds (numpy=42, sklearn=42, Python random=42) are now specified.

*Changes: Methods §2.3.1, "All random seeds were fixed (numpy.random.seed(42), sklearn.utils.check_random_state(42))..."*

### R9: Bragg–Williams sensitivity (SRO)
**Reviewer 3, Comment 1 / Editorial Requirement 9**

We tested small excess Gibbs energies (L = ±5, ±10~kJ/mol) and found that R-phase occupancies change by <0.03 in site fraction for most Wyckoff sites. The largest sensitivity is at the mixed 6c site (Δy_Mo ~0.08). These results are now reported in Supplementary Figure~S2. The ideal BW approximation is adequate for the level of accuracy claimed.

*Changes: Methods §2.4, new Supplementary Fig.~S2, "Sensitivity analysis with L = ±5 kJ/mol..."*

### R10: Thermodynamic validation
**Reviewer 3, Comment 2–4 / Editorial Requirement 10**

(a) A site-by-site table (Table~4) now reports ML-predicted vs.~experimental Mo site fractions for the R phase with the mean absolute deviation (MAD = 0.04) as the goodness-of-fit metric. (b) Relative phase stabilities at 1700~K are compared with the CALPHAD assessment of Jacob et al. (2000) in Supplementary Figure~S3. (c) The choice of 1700~K is justified: this temperature corresponds to the typical annealing temperature for R-phase XRD measurements (Joubert, 1993) and lies within the experimentally determined stability range of the R phase.

*Changes: Results §3.5, new Table~4, Supplementary Fig.~S3, "The temperature of 1700 K was chosen to match experimental XRD measurement conditions..."*

### R11: Generality / transferability
**Reviewer 3, Comment 5 / Editorial Requirement 11**

We have revised the Discussion to acknowledge the speculative nature of transferability claims. The statement is now explicitly qualified: "While our approach is expected to generalise to other transition-metal binaries that host TCP phases (e.g., Fe–W, Co–Mo), experimental or computational validation in those systems is required to confirm this."

*Changes: Discussion §4.3, "While our approach is expected to generalise... further validation is required."*

---

## Summary of Revised Files

| File | Changes |
|------|---------|
| `paper.tex` | Minor formatting updates |
| `sections/results.tex` | Added Table~2 (CIs), Fig.~6 (learning curves), CNAV comparison text, site-by-site Table~4 |
| `sections/methods.tex` | Added convergence Table~3, reference state justification, nested CV clarification, BOP moment discussion, hyperparameter table reference, BW sensitivity |
| `sections/discussion.tex` | Qualified transferability claims |
| `references.bib` | Added Jacob et al. (CALPHAD 2000) reference |

All changes are highlighted in the revised manuscript. We believe the manuscript has been substantially strengthened and hope it is now suitable for publication in Physical Review B.

---

*Respectfully submitted,*

Mariano Forti \\
on behalf of all authors
