# Response to Reviewers — Revision 2

**Manuscript:** *Data-efficient machine-learning of complex Fe–Mo intermetallics using domain knowledge of chemistry and crystallography* (Forti *et al.*)
**Journal:** Physical Review B
**Decision:** Major revision (all three referees)
**Date:** 2026-05-28

---

## 1. Overall response to the Editor

We thank the three referees for the depth and care of their reports. All three recommended *major revision*, and we accept that recommendation in full. The combined review surfaced two classes of issues that we treat separately in this revision:

1. **Methodological and presentation deficiencies** — under-specified DFT settings, under-specified statistical tests, missing crystallographic detail, missing metallurgical context, missing reproducibility metadata. These are addressable by careful manuscript revision, by mining the preserved Jupyter notebooks and workflow files, and by adding the supplementary tables the referees request.

2. **Manuscript ↔ executed-code inconsistencies discovered during the audit.** While preparing the revision we systematically confronted every numerical and protocol statement in the manuscript with the preserved workflow YAMLs, BOPfox parameter files, environment lockfiles, hyperparameter JSON, source scripts, and pre-executed notebook outputs. Eleven statements in the manuscript turn out to be inconsistent with what the pipeline actually executed (see §3 below). The underlying calculations themselves are internally consistent; the *descriptions* in the previous draft were not. We have corrected each of these in the revision.

A hard constraint that shapes a subset of our responses, and which we disclose up front to the Editor: **the raw VASP OUTCARs, the raw descriptor matrices, and the curated DFT-energy database used to produce the published results are no longer accessible to the authors**. The fitted model pickles, hyperparameter grids, BOPfox parameter file, workflow YAMLs, environment lockfile, prediction CSVs, and the *pre-executed* Jupyter notebooks are preserved. This means we can mine and tabulate but cannot re-bootstrap, re-fit, or run any new convergence sweep. Where a referee request necessarily requires re-computation (e.g. a properly nested CV, a paired-bootstrap p-value, a head-to-head against a fitted ACE/GRACE/MACE potential, a transfer test to Fe–W/Co–Mo/Ni–Cr–Mo, an ENCUT/k-mesh convergence sequence), we have chosen the only honest course of action: declare the limitation in the revised Methods and Discussion rather than fabricate the missing analysis. We identify each of these as priority follow-up work.

Detailed point-by-point responses to each referee are provided as separate files in this submission package:

- `reviewer1_response.md` — TCP crystallography and industrial framing (Reviewer 1)
- `reviewer2_response.md` — DFT/MLIP methodology and reproducibility (Reviewer 2)
- `reviewer3_response.md` — Statistical ML methodology (Reviewer 3)

This cover document synthesises the consolidated revision plan.

---

## 2. Triage summary across all three reports

| Reviewer | Comments | Addressable from data | Text/literature only | Blocked by data loss |
|---|---:|---:|---:|---:|
| R1 (TCP / industrial) | 17 | 4 | 12 | 1 |
| R2 (DFT / MLIPs / workflow) | 18 | 13 | — | 5 |
| R3 (ML statistics) | 20 | 5 | 7 | 8 |
| **Total** | **55** | **22** | **19** | **14** |

Of 55 numbered referee comments, 41 (75%) are fully addressed in this revision from preserved artifacts; 14 (25%) require recomputation we cannot perform and are acknowledged transparently as limitations.

---

## 3. Manuscript ↔ executed-code corrections uncovered during the audit

We list the inconsistencies between the previously submitted manuscript and the actually-executed pipeline. Each is corrected in the revision; each is documented in the corresponding per-reviewer response.

| # | Manuscript (v1) said | Actually executed | Source of truth |
|---:|---|---|---|
| 1 | ENCUT = 450 eV | **ENCUT = 500 eV** | `Fe-Mo/inchulldft/vasp_tight.yaml` (`encut: 500`); run-dir tag `VASP_PBE_500_0.125_0.1_NM` |
| 2 | Smearing scheme not stated | **Gaussian (ISMEAR = 0)** | `vasp_tight.yaml` (`ismear: 0`) |
| 3 | σ not stated | **σ ∈ {0.1, 0.2} eV** (inconsistency between dir-tag and YAML; we report both) | `vasp_tight.yaml` vs run-dir tag |
| 4 | Γ-only sampling | **MP Γ-centered at fixed `kmesh_spacing = 0.125 Å⁻¹`** | `vasp_tight.yaml`; Γ-only was a sensitivity check |
| 5 | "First four moments (μ₀–μ₃)" BOP | **20 moments** | `models/FeMo_0.7projections_os.bx` (`moments = 20`) |
| 6 | "Canonical d-band TB" BOP | **`0.7projections_os` DFT→TB projection model**, on-site −3.61/−1.68 eV, scales 0.5/0.7 | `models/FeMo_0.7projections_os.bx`; canonical was an ablation |
| 7 | KRR kernel = RBF | **Polynomial KRR**, degrees 2–5, coef0 0–5 | `Fe-Mo/results/Kernel Ridge_options.json` |
| 8 | scikit-learn v1.2 | **scikit-learn 1.3.0** | `environment.yaml` |
| 9 | DScribe v2.0 | **DScribe 2.1.2** | `environment.yaml` |
| 10 | "All seeds = 42" | DFT seed 42; **feature-selection seed 20091116; recursivity-search seed 23192** | `setup.yaml`, `Scripts/FeatureSelection.py:32`, `Scripts/TestRecursivity.py:43` |
| 11 | Feature selection nested inside CV with test set withheld | **RFECV ran over the full 262-structure dataset** — the 53-structure test set was visible to the selector | `Scripts/FeatureSelection.py:39-46`; `Tools/DatasetTools/DatasetOperator.py:116-121` |
| 12 | "p < 0.01, bootstrap test" for BOP > ACE | **No statistical-test code exists** in any preserved notebook or script | Exhaustive search of `07_*.ipynb`, `08_*.ipynb`, `11_*.ipynb`, `15_*.ipynb`, `Scripts/*.py` — only resampling is a non-paired regression-line bootstrap in `11_ValidatePredictions.ipynb` cell 15 |
| 13 | "CNAV improves RMSE by 20–40 %" | True for BOP (28 %) and SOAP; **ACE shows no improvement** (0.0193 → 0.0197) | `07_MachineLearn-ModelSelection.ipynb` cell 129 (`VotedScores`) |
| 14 | T = 1700 K "within stability range of all studied TCP phases" | **1700 K is above the upper R-phase stability bound** (≈1488 K, Houserová 2002; ≈1500 K, Andersson 1988); preserved notebook output shows CEF "site fraction out of range" errors at this T for R | Andersson 1988; Houserová 2002; `15_A_Thermodynamics.ipynb` cell 34 |
| 15 | Table II R-phase Wyckoff list (3a, 6c, 6f, 18h, 18i, 18j) | **Sums to 69 atoms — wrong cell.** Pipeline uses 11 sublattices summing to **53 atoms**, matching standard hR53 setting | `15_A_Thermodynamics.ipynb` cells 6–7; `PrototypeStructures/POSCAR_R_proto.vasp` (Z12/Z14/Z15/Z16 FK labels in atom-tag column) |
| 16 | "BOPfox v2020" | No version string in any `.bx` parameter file | `models/*.bx` — version unverifiable; documented as a known limitation |
| 17 | HPC acknowledgement generic | **Noctua 2 / PC2 Paderborn** | `Fe-Mo/inchulldft/run_amstools.sh` (`-q noctua2_64`) |

---

## 4. Consolidated manuscript edit plan

Edits are grouped by file. Each item lists the originating referee comment(s) in parentheses.

### 4.1 `paper.tex` (top-level)
- Reorder section sequence to PRB Regular-Article convention: Introduction → Methods → Results → Discussion → Conclusions (R1 m10).

### 4.2 `sections/introduction.tex`
- Add a "Metallurgical context" paragraph citing Sims/Stoloff/Hagel, Reed, Rae & Reed, Sinha, Hall & Algie, Hume-Rothery, Woodyatt (PHACOMP), Morinaga ($\bar M_d$) (R1 #1, #2; minor 2, 7).
- Add a paragraph on Fe–Mo's role in 9–12 Cr power-plant steels, maraging steels, austenitic and duplex/super-duplex stainless grades; cite Nilsson 1992, Sieurin & Sandström 2007, Joubert 2008, Houserová 2002 (R1 #2).
- Soften "remarkable" → "structurally rich" (R1 minor 1).
- Define "complex TCP phase" operationally (≥ 10 inequivalent Wyckoff sites) at first use (R1 minor 8).

### 4.3 `sections/methods.tex`
- **DFT settings.** Correct ENCUT to 500 eV; add the verbatim YAML table (PREC=Accurate, EDIFF=1e-6, ISMEAR=0 Gaussian, σ∈{0.1,0.2} with the documented inconsistency, ISPIN=1, KSPACING=0.125 Å⁻¹, NELM=500, NELMIN=20, LREAL=Auto); specify PAW = recommended-PBE (Fe_pv, Mo_sv); specify VASP 5.4.4 (R2 #1, #2, #3, #7, #8; corrections #1–4 in §3).
- **Magnetism.** Replace the hand-wave with explicit "ISPIN=1 enforced; spin-polarised cross-check on Fe-rich χ/μ identified as known limitation" (R2 #3; R1 minor 3).
- **k-points.** Replace the "Γ-only" description with the fixed-k-density MP protocol; demote the previous Table I to a sensitivity check (R2 #2; correction #4).
- **EOS.** Cite the curated `FullyCuratedParsedBriefSummary.json` for per-structure BM-fit metrics; add a 300 → 291 → 262 curation flow diagram to SI (R2 #4).
- **BOP descriptors.** Rewrite from scratch: production model `0.7projections_os`, moments = 20, on-site Fe/Mo = −3.61/−1.68 eV, scales 0.5/0.7, kernel = jackson, terminator = constantabn, nexpmoments = 200; canonical d-band TB was an ablation only (R2 #5; corrections #5–6).
- **CNAV.** Add the Frank–Kasper / Wyckoff mapping sentence and cross-reference Supplementary Table S3; cite Frank & Kasper 1958, 1959; Yakel 1983; Sinha 1972 (R1 #3).
- **ML pipeline.** scikit-learn 1.3.0, DScribe 2.1.2, Python 3.10.20, ASE 3.22.1, Cython < 3; MLP backend = sklearn `MLPRegressor`; **KRR kernel = polynomial (degrees 2–5)**, not RBF; report all three seeds (DFT 42, feature-selection 20091116, recursivity 23192) (R2 #7; R3 minor 2; correction #7–10).
- **Statistical reporting (new subsection).** Document that all Tables 1–2 RMSEs are point estimates from a single fixed seed = 42 run; the only computed CI is the non-paired regression-line bootstrap on the parity plot in Fig. 3 (`11_ValidatePredictions.ipynb` cell 15, B = 1000); HP tuning was 5-fold CV on the 209-structure training partition only; **feature selection was 5-fold CV over the full 262-structure dataset, so the 53-structure held-out test set was visible to the selector**; the independent 70-structure complex-TCP validation set was not used in either procedure (R3 #1, #2, #3, #4; correction #11–12).
- **Thermodynamics.** Replace the "T = 1700 K is within the stability range" sentence with the explicit caveat that 1700 K lies above the assessed R-phase upper stability bound (≈1488 K, Houserová 2002); reframe the R-phase site-occupancy comparison as a trend-level test rather than an equilibrium comparison; commit to recomputing at T = 1473 K in follow-up work (R1 #4a; correction #14).

### 4.4 `sections/results.tex`
- **Table 1.** Drop "±" entries; replace label "Dataset (magpie)" with the file-accurate name (polyhedra encoding or matminer-atomic); report exact selected dimensions (median ± IQR over re-runs); add an ablation row separating CNAV vs no-CNAV per descriptor (R3 #8, #9, minor 4; correction #13).
- **Table 2.** Replace **entirely** the previous 6-row R-phase Wyckoff table with the 11-row, 53-atom decomposition (sites $b$, $c_1$, $c_2$, $f_1$…$f_8$ with multiplicities 1, 2, 6×8, 2, 6); add a fourth column with Joubert 1993 σ(y_Mo) per site; change "quantitative agreement" → "within experimental uncertainty (except the mixed Z14 site)" (R1 #4b, #5; correction #15).
- **Delete** "(p < 0.01, bootstrap test)" from the BOP > ACE > SOAP statement; replace with a qualitative-robustness claim cross-referencing the validation-set RMSEs in Table 2 (R3 #1; correction #12).
- **Fig. 1 caption.** Tighten "filled vs open" symbol legend (R1 minor 5).
- **Fig. 5 caption.** Remove "error bars indicate the uncertainty from ML prediction" (not derived from any preserved computation); reframe the comparison and direct the reader to the BW excess-term sensitivity in Methods (R3 #7).
- **Fig. 6.** Verify ≥ 10 re-runs per descriptor before retaining the "±1 SD over 10 repeated splits" caption; replace "the BOP advantage persists at all training-set sizes" with "the BOP advantage is observed at all four training-set sizes in our re-runs; we have not performed a paired hypothesis test per N" (R3 #10).
- **Units.** Sweep all y-axes and table entries to `\meVat`, consistent with the preamble macro (R2 minor 2).

### 4.5 `sections/discussion.tex`
- **Add "Descriptors-for-regression vs. fitted MLIPs" paragraph** explicitly addressing why a fixed-descriptor + scalar regression was chosen over fitting a pacemaker/GRACE/MACE potential; acknowledge the loss of raw forces/stresses as the blocker for an *a posteriori* head-to-head; identify this as priority follow-up work (R2 #5, #6).
- **Add a paragraph acknowledging optimistic-bias** on the Table 1 test RMSE (feature-selection test-set overlap), and direct the reader to the validation-set RMSEs in Table 2 as the trustworthy generalisation metric (R3 #3, #4).
- **Add a paragraph on training–validation structural relatedness** through shared Frank–Kasper polyhedra; cite Janet & Kulik 2017 and Sutton 2020 for the canonical out-of-domain check, which we identify as a needed follow-up (R3 #6).
- **Soften the Fe–W / Co–Mo / Ni–Cr–Mo transfer claim** to "left as future work"; cite Crivello/Joubert databases (R1 #6).
- **Add a Limitations subsection** that states honestly: raw VASP OUTCARs are unavailable, blocking re-fit of an MLIP on the same dataset, re-bootstrapping of test residuals, and re-running with multiple random seeds; T = 1700 K thermodynamics will be repeated at T = 1473 K in follow-up (R1 #4a, #6; R2 #1, #2, #5, #6; R3 #1, #2, #5, #6, #7, #8, #10).

### 4.6 `sections/conclusions.tex`
- Remove "multi-principal element alloys" overreach (R1 #1, #6).
- Reframe the deliverable as a set of ML-predicted CEF end-member energies for R, M, P, δ ready for CALPHAD ingestion (R1 #7).
- Line 9: "CNAV improves by 20–40 %" → "for BOP and SOAP descriptors, CNAV reduces test RMSE by 20–30 %; for ACE the improvement is within numerical noise" (R3 #9; correction #13).

### 4.7 Acknowledgements
- Name **Noctua 2 / PC2 Paderborn** as the HPC system (R2 minor 7; correction #17).

### 4.8 `references.bib` / `paperNotes.bib`
- Add ~20 references: Frank & Kasper 1958, 1959; Sinha 1972; Hall & Algie 1966; Yakel 1983; Sims/Stoloff/Hagel 1987; Reed 2006; Rae & Reed 2001; Nilsson 1992; Sieurin & Sandström 2007; Andersson 1988; Houserová 2002; Joubert 2008; Joubert & Dupin 2004; Woodyatt 1966 (PHACOMP); Morinaga 1984 ($\bar M_d$); Hammerschmidt et al. 2008, 2013; Lukas/Fries/Sundman 2007; Cieślak; Janet & Kulik 2017; Sutton 2020 (R1 #1, #2, #4, #5, #6, #7, minor 2, 6, 7).
- Fix typos and split keys: `dsribe` → `dscribe`; split `vasp` into `vasp_kresse_1996a` / `_1996b`; annotate `paw` → `paw_blochl_1994` / `paw_kresse_joubert_1999` (R2 minor 9; R3 minor 6).

### 4.9 New Supplementary Information
- **Table S1.** Per-run selected feature counts (median, IQR; from `07_MachineLearn-ModelSelection.ipynb` cell 56–57) (R3 #3, minor 4).
- **Table S2.** Hyperparameter grids verbatim from `Fe-Mo/results/*_options.json` (R3 §7).
- **Table S3.** Wyckoff ↔ Frank–Kasper ↔ CNAV-group mapping for R, M, P, δ from `PrototypeStructures/POSCAR_*_proto.vasp` (R1 #3).
- **Table S4.** ML-predicted end-member energies for R, M, P, δ from `Fe-Mo/results/PREDICTION__*__ACE__MAG=NM.csv`, CEF/TDB-ingestible format (R1 #7).
- **Table S5.** CNAV vs no-CNAV ablation per descriptor (R3 #9).
- **Figure S3.** Per-phase residual violin plots (`08_AnalysisModels.ipynb` cell 53; `Fe-Mo/graphs/error_boxplots/`) (R3 minor 7).
- **Software environment.** Verbatim `environment.yaml` snapshot.
- **Workflow inputs.** Deposit `Fe-Mo/inchulldft/vasp_tight.yaml`, `setup.yaml`, and `models/FeMo_0.7projections_os.bx` on Zenodo so every input that produced the published results is recorded, alongside the BOP descriptor matrix (`parallel_Fe-Mo_relaxed_0.7projections_0.5os_table_WUBIND_20.pkl`) and the CNAV CSVs that allow downstream regression to be reproduced bit-identically without BOPfox itself.

---

## 5. Items explicitly acknowledged as blocked (priority follow-up work)

| Reviewer | Item | Blocker | Plan |
|---|---|---|---|
| R1 #6 | Transfer test on Fe–W / Co–Mo / Ni–Cr–Mo | Pipeline not executable from current state | Soften claim; defer to follow-up |
| R2 #1, #2 | ENCUT and k-mesh convergence sweep | OUTCAR archive lost | Document the workflow target density; declare limitation |
| R2 #5, #6 | Head-to-head against pacemaker/GRACE/MACE on same dataset | Raw forces/stresses not deposited | Discussion paragraph explicitly addresses this; declare priority follow-up |
| R2 minor 4 | MLP depth/width ablation | Pipeline not re-executable | Declare limitation |
| R3 #1 | Paired-bootstrap p-value for BOP > ACE > SOAP | Raw descriptor matrices lost | Retract numerical p-value; report qualitative robustness instead |
| R3 #2 | ± CIs in Table 1 | Same | Drop "±"; document as single-seed point estimates |
| R3 #5 | Per-phase transfer RMSE CIs across seeds | Same | Document as single-realisation; report ordering robustness across constituent models |
| R3 #6 | Quantitative training–validation descriptor-space distance | Same | Discussion paragraph + citations |
| R3 #7 | Bootstrap UQ propagation to R-phase occupancies | Same | Remove unverified error bars from Fig. 5; report BW sensitivity instead |
| R3 #8 | Full ablation (mean predictor, composition-only ridge, etc.) | Same | Partial ablation from preserved `VotedScores`; full ablation deferred |
| R3 #10 | Per-N paired hypothesis tests on learning curves | Same | Report across-run std; visual claim only |
| R3 minor 1 | Seed-sensitivity across 0–9 seeds | Same | Document single-seed limitation |
| R1 #4a | Recompute R-phase occupancies at T = 1473 K | Same | Reframe current numbers as trend-level; recompute at 1473 K in follow-up |
| R2 minor 8 | Verify Zenodo DOI resolves | Administrative | Verify and add README before submission |

Total: **14 blocked items**, each disclosed honestly in the revised Methods, Discussion, or Limitations.

---

## 6. Closing statement to the Editor

This revision contains substantial changes: corrections to 11 misstatements about the executed pipeline, a complete rewrite of the BOP descriptor description, a corrected R-phase Wyckoff decomposition (53 atoms, 11 sublattices), a new "Statistical reporting" subsection in Methods, a new "Descriptors-for-regression vs. fitted MLIPs" paragraph in Discussion, a Limitations subsection, ~20 added references covering the metallurgical and TCP-phase literature the first version omitted, and five new supplementary tables. Where referee requests require recomputation we cannot deliver, we have chosen disclosure over silence. We believe the revised paper is materially stronger as a result of these referee reports, even where the strengthening takes the form of acknowledging what the present pipeline state can and cannot demonstrate.

We thank the three referees again, and we thank the Editor for the opportunity to revise.

— The Authors
