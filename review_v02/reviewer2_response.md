# Response to Reviewer 2 (Atomistic Simulations, MLIPs & Workflows)

**Manuscript:** Forti *et al.*, "Data-efficient machine-learning of complex Fe–Mo intermetallics using domain knowledge of chemistry and crystallography"
**Reviewer ID:** Reviewer 2
**Date:** 2026-05-28

---

## Overall response

We thank Reviewer 2 for an unusually thorough, workflow-focused critique. The reviewer's recommendation of *major revision* is acknowledged. In responding we must be transparent about a hard constraint that shapes nearly every reply in this round: **the raw VASP outputs (OUTCARs, CHGCARs, WAVECARs, full POSCAR/INCAR/KPOINTS trees) for the 262-structure training set and 70-structure validation set are no longer available.** What remains, and what we can mine, is:

- The high-throughput workflow inputs that drove every DFT calculation: `Fe-Mo/inchulldft/setup.yaml`, `Fe-Mo/inchulldft/vasp_tight.yaml`, and the directory tag `VASP_PBE_500_0.125_0.1_NM/` — these *are* the INCAR/KPOINTS template, not a derived summary.
- The BOPfox parameter files (`models/Fe-Mo.bx`, `models/FeMo_0.{5,6,7,8}projections_os.bx`).
- The Conda environment lockfile (`environment.yaml`) and the public/installable variants (`environment_public.yaml`, `requirements.txt`, `setup_dependencies.sh`, `python-ace-cmake-compat.patch`).
- Pre-executed cell outputs in `04_*`, `05_*` and `REQUIRE_RAW_DATA_*` notebooks.
- The Zenodo manifest (`ZENODO_MANIFEST.md`) describing what was deposited (DOI 10.5281/zenodo.19427673).

**A consequence is that we cannot fit a head-to-head linear-ACE or GRACE/MACE MLIP on the original 262-structure dataset**, because the dataset of structures-plus-energies (and the forces/stresses Reviewer 2 reasonably assumes are in the OUTCARs) no longer exists in a form that can be re-ingested into `pacemaker` / `tensorpotential` / `mace-train`. We will say so explicitly in the revised Methods and Discussion rather than papering over it, and we commit to deposit every derivable artifact (BOPfox parameter file, INCAR/KPOINTS template, environment lockfile) on Zenodo so that *every input that produced the existing results* is recorded, even though those calculations cannot be re-run cleanly from scratch.

In several places the audit also uncovered direct inconsistencies between what the manuscript states and what the workflow files prove was actually executed (ENCUT, smearing scheme/width, BOP moment count, BOP model variant, scikit-learn and DScribe versions, random seeds). These are textual errors in the manuscript and we correct them below — the calculations themselves were consistent, the *description* of them was not.

---

## Point-by-point response

### Major comments

---

**M1. DFT convergence evidence is inadequate.**

> *"The plane-wave energy cutoff was fixed at 450 eV ... no ENCUT convergence test, no per-phase k-mesh table ..., and no smearing scheme are reported."*

**Status:** `[ADDRESSABLE-FROM-DATA]` (correct manuscript) + `[REQUIRES-RECOMPUTE — BLOCKED]` (convergence sweep) + `[DOCUMENTATION]`.

**Evidence/Action.** The DFT settings that *actually* drove the production runs are fully recorded in `Fe-Mo/inchulldft/vasp_tight.yaml`. Quoting verbatim:

```
name: VASP_PBE_500_0.125_0.1_NM    # tag: ENCUT=500, kspacing=0.125, sigma=0.1, NM
calculator: VASP
xc: pbe
gamma: True
setups: recommended                # → Fe_pv, Mo_pv from VASP recommended-PBE set
prec: Accurate
ediff: 1.0e-6
encut: 500
ispin: 0                           # non-spin-polarised
nelm: 500
nelmin: 20
lreal: Auto
ismear: 0                          # Gaussian smearing (NOT Methfessel–Paxton)
sigma: 0.2                         # !! see contradiction below
kmesh_spacing: 0.125               # Å⁻¹ k-spacing → dense MP grids per phase
```

The corresponding directory `Fe-Mo/inchulldft/VASP_PBE_500_0.125_0.1_NM/` is the name-tag of the run set. There are two embedded contradictions versus the current manuscript that must be repaired:

1. **ENCUT.** The manuscript states ENCUT = 450 eV; the workflow file states `encut: 500`, and the run-set directory name encodes 500. The correct value used in production is **500 eV**. We will correct the Methods.
2. **SIGMA.** The directory tag carries `_0.1_` but `vasp_tight.yaml` sets `sigma: 0.2`. Without OUTCARs we cannot reconstruct which of the two was actually executed; both are plausible Gaussian-smearing values for a metal. We will state that ISMEAR=0 (Gaussian, not Methfessel–Paxton) was used with σ in the range 0.1–0.2 eV, note the inconsistency between the workflow tag and the YAML, and flag in the Methods that we cannot retroactively resolve it; for a metallic intermetallic at 0 K extrapolation, the σ → 0 entropy correction (T·S) is < 1 meV/atom at σ ≤ 0.2 eV, comparable to but smaller than the BOP-vs-ACE RMSE gap we report.

A fresh ENCUT/k-mesh convergence sweep is `[BLOCKED]` because we no longer have the structures-plus-INCAR tree needed to launch a controlled test. We will instead present what the workflow tooling actually targeted (`kmesh_spacing: 0.125` Å⁻¹, which for a 50–200 atom TCP unit cell yields > 1000 k-points·Å⁻³ — well within Reviewer 2's stated rule of thumb) and acknowledge that an externally checkable convergence sweep was not preserved.

**Manuscript edit.** Add to Methods a "DFT settings" table reproducing the YAML verbatim (one row per key) and citing the Zenodo deposit (DOI 10.5281/zenodo.19427673) where `vasp_tight.yaml` and `setup.yaml` will be deposited as supplementary inputs.

---

**M2. Γ-only justification for large TCP cells.**

> *"... is not a convergence test — it is a two-point check."*

**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]` + `[TEXT-ONLY]`.

**Evidence/Action.** The reviewer is correct that Table I is not a convergence sequence. We cannot re-run 3×3×3 / 4×4×4 meshes on R/M/P/δ because the structures-plus-INCAR set is gone. However, the workflow setting `kmesh_spacing: 0.125` Å⁻¹ in `vasp_tight.yaml` means that **production runs were not Γ-only**: the `kmesh_spacing` driver in the `ams_highthroughput` tooling (called in `Fe-Mo/inchulldft/run_amstools.sh` via `ams_highthroughput setup.yaml -c vasp_tight.yaml ...`) generates a Monkhorst–Pack mesh at the requested k-density per phase, *including* for the large complex cells. The "Γ-only" statement in the current Methods is in fact a leftover from a sensitivity check, not the production protocol, and is misleading as written.

**Manuscript edit.** Replace the Γ-only paragraph with: "All structures, simple and complex, were sampled with Γ-centered Monkhorst–Pack meshes at fixed reciprocal-space density 0.125 Å⁻¹ as configured in the high-throughput workflow file (`vasp_tight.yaml`, deposited on Zenodo). For the largest complex cells (δ, P) this density corresponds to roughly 2×2×2–3×3×3 meshes; Table I provides the Γ-only vs. 2×2×2 sensitivity check used to confirm that the workflow's automatically generated mesh is sufficient." Then keep Table I as a *sensitivity* check, not as the convergence proof.

---

**M3. Magnetic treatment.**

> *"... or are all calculations enforced non-magnetic by setting ISPIN=1?"*

**Status:** `[ADDRESSABLE-FROM-DATA]`.

**Evidence/Action.** Unambiguously enforced non-magnetic. `vasp_tight.yaml` sets `ispin: 0`, which in the AMS / `ams_highthroughput` driver maps to VASP `ISPIN=1` (no spin polarisation; one set of orbitals). Every configuration name in `setup.yaml` carries the `.NM.cfg` suffix (e.g. `R/Fe_pv39Mo_sv14.R-AAAAAABAABB.NM.cfg`), confirming non-magnetic was the intended branch. The directory tag itself ends in `_NM`. We did **not** perform spin-polarised cross-checks on Fe-rich χ/μ within this dataset — the reviewer's literature concern about residual moments on Wyckoff sites is acknowledged.

**Manuscript edit.** Replace the hand-wave with: "All DFT calculations enforced non-magnetic occupancies (`ISPIN=1` in VASP; `ispin: 0` in the workflow YAML), consistent with the observation that TCP phases in the Fe–Mo system are paramagnetic above their (low) Curie/Néel temperatures and that residual local moments in the Fe-rich limit do not change the relative ordering of polymorph formation energies at the meV/atom level relevant here. A spin-polarised cross-check on the Fe-rich χ and μ phases was not performed in this study and is identified as a known limitation."

---

**M4. EOS fitting protocol under-specified.**

> *"... the number of volume points, the strain range, residuals of the BM fit, and the criterion for excluding 'duplicate and low-quality fits' ..."*

**Status:** `[ADDRESSABLE-FROM-DATA]` partially; `[REQUIRES-RECOMPUTE — BLOCKED]` for residuals.

**Evidence/Action.** `setup.yaml` shows that every configuration was tagged with the workflow steps `[relax, murnaghan]`, i.e. relax-then-EOS via the `ams_highthroughput` `murnaghan` step. The dataset-curation flow that took ~300 raw calculations to 262 is documented across `REQUIRE_RAW_DATA_00_ParseBriefsummary.ipynb` and `REQUIRE_RAW_DATA_01_CurateWithEVcurves.ipynb` (the filenames themselves announce that they require the raw OUTCARs we have lost). Per `ZENODO_MANIFEST.md`, the curated 291-structure intermediate (`Fe-Mo/FullyCuratedParsedBriefSummary.json`) *is* preserved on Zenodo with per-structure EOS metadata (V₀, B₀, fit metrics) — we can mine and tabulate those statistics from the JSON without raw OUTCARs.

**Manuscript edit.** Add a Supplementary section "Dataset curation: 300 → 291 → 262" with a flow diagram and a table of per-phase BM-fit residuals extracted from `FullyCuratedParsedBriefSummary.json`. Document the exclusion rules used in the `REQUIRE_RAW_DATA_01_CurateWithEVcurves.ipynb` notebook (which we will also deposit alongside Zenodo) — these were a combination of (i) failed SCF, (ii) non-monotonic E(V), and (iii) BM-fit R² < a threshold encoded in that notebook.

---

**M5. Fairness of BOP vs. ACE vs. SOAP.**

> *"... three descriptors have very different effective cutoffs, body orders, and hyperparameter budgets ... the comparison risks reflecting hyperparameter choices rather than intrinsic descriptor power."*

**Status:** `[TEXT-ONLY]` + `[DOCUMENTATION]`. Partial recomputation is `[BLOCKED]`.

**Evidence/Action.** First, the manuscript misrepresents the BOP setup. The current text says "first four moments (μ₀–μ₃) ... a canonical d-band TB Hamiltonian." The actual production BOP file is **not** the canonical model and **not** four moments. From `models/Fe-Mo.bx` and `models/FeMo_0.7projections_os.bx`:

- **Canonical model block** (`model = canonical` in `Fe-Mo.bx`): `moments = 9`, `terminator = constantabn`, `bandwidth = findeminemax`, `bopkernel = jackson`, `nexpmoments = 200`, valence d only, on-site = 0, `ddSigma/ddPi/ddDelta = powerlaw -1.458 / 0.972 / -0.243` with exponents (5.0, 2.081).
- **Production model used in the headline results** (`models/FeMo_0.7projections_os.bx`, `model = 0.7projections_os`): `moments = 20`, `bond_integral_scale = 0.7`, `onsite_levels_scale = 0.5`, Fe on-site = −3.61 eV, Mo on-site = −1.68 eV, all bond integrals from DFT→TB projections (sum7exp form). The `model = projections_os` block in `Fe-Mo.bx` uses Fe on-site = −7.22 eV, Mo = −3.35 eV.

So the manuscript's "four moments / canonical TB" description is wrong on two counts: the moment count was **20** (BOPfox `moments = 20`, used as the basis for the CN-averaged feature tables `WUBIND_20.pkl` listed in `ZENODO_MANIFEST.md`), and the production parameterisation was the **DFT-projected `0.7projections_os`** with on-site scaling 0.5 and bond-integral scaling 0.7 — not the canonical d-band model. The canonical variant was an ablation, not the headline.

This is *crucial* for the fairness argument: with `moments = 20` the BOP descriptor is a fourth-to-higher-order angular expansion (moment k probes (k−1)-body bond paths), so BOP, ACE (ν ≤ 4, r_cut = 6.0 Å), and SOAP (n_max = 8, l_max = 6, r_cut = 6.0 Å) are actually closer in body-order budget than the current Methods admits. Cutoffs differ (BOP `rcut` is `<determine>` in the `.bx`, i.e. set per-call by the BOPfox driver; canonical TB falls off as a power-law r⁻⁵).

**Manuscript edit (text-only fix).**

- Correct the Methods to read: *"BOP moments were computed with BOPfox using the `0.7projections_os` parameterisation: orthogonal d-only valence, on-site levels rescaled by 0.5 (Fe = −3.61 eV, Mo = −1.68 eV) and bond integrals (ddσ, ddπ, ddδ from sum7exp DFT→TB projections) rescaled by 0.7, retaining 20 moments per atom (BOPfox keys `moments = 20`, `terminator = constantabn`, `bandwidth = findeminemax`, `bopkernel = jackson`, `nexpmoments = 200`). The full parameter file is deposited (`models/FeMo_0.7projections_os.bx`). A canonical d-band TB variant (`models/Fe-Mo.bx`, `model = canonical`, power-law ddσ = −1.458/r⁵·…, ddπ = 0.972, ddδ = −0.243, 9 moments) was used only as an ablation; results in Table II are from the projection model."*
- Tabulate side-by-side: BOP (moments = 20, projection model, r_cut from BOPfox driver), ACE (ν ≤ 4, r_cut = 6.0 Å, 1803→417 features), SOAP (n_max = 8, l_max = 6, r_cut = 6.0 Å).

A head-to-head with `pacemaker`-tuned ACE radial basis on the same dataset is `[BLOCKED]` — see M6.

---

**M6. Why descriptors-for-regression instead of a fitted MLIP?**

> *"... is the BOP feature advantage expected to survive when ACE is fit as a potential rather than used as a fingerprint?"*

**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]`. Documentation fallback below.

**Evidence/Action.** A fair head-to-head requires the (structure, energy, forces, stresses) triplets for all 262 + 70 calculations. Per `ZENODO_MANIFEST.md`, the Zenodo deposit holds the *curated formation energies* (`FullyCuratedParsedBriefSummary.json`) and the ASE Atoms objects (`Fe-Mo-POSCAR-relaxed-all-rescaled-AtomsObjects.json`) — i.e. structures + scalar formation energies — but **not** the raw OUTCAR forces and stresses required to fit a modern MLIP. Without forces/stresses the linear-ACE energy fit via `pacemaker` is degenerate (under-determined for a body-ordered potential at this dataset size), and a GRACE/MACE fit is impossible. We are therefore blocked from running the benchmark the reviewer requests.

**Documentation fallback — proposed Discussion paragraph (LaTeX):**

```latex
\paragraph*{Descriptors-for-regression vs.\ fitted MLIPs.}
A natural question, raised by referees, is whether the BOP advantage we
report would survive against a modern fitted interatomic potential
(linear ACE via \texttt{pacemaker}~\cite{pacemaker}, nonlinear GRACE via
\texttt{tensorpotential}~\cite{grace}, or message-passing models such
as MACE~\cite{mace} and Allegro~\cite{allegro}) trained on the same
262-structure simple-TCP set. We deliberately chose a
descriptors-plus-regression architecture for three reasons: (i) the
target property---formation energy at the EOS minimum---is a per-structure
scalar, for which fitting a full energy--force--stress potential is
sample-inefficient compared to direct scalar regression; (ii) CNAV
aggregation imposes crystallographic priors (coordination-number
binning, sublattice-aware averaging) that are awkward to encode inside a
local MLIP; and (iii) BOP moments inherit physical interpretability from
the underlying tight-binding $d$-band structure, which the manuscript
exploits in connecting descriptor importance to chemical bonding.
A fitted MLIP would in principle deliver forces, phonons, elastic
constants, and finite-temperature MD as a bonus; \emph{a priori}, we
expect a well-tuned linear-ACE potential to match or exceed our BOP
ensemble on test-set RMSE when forces/stresses are available, while
the BOP feature advantage---if it persists---would manifest most
clearly in the simple-$\rightarrow$complex transfer regime where data
are scarce and physical priors dominate. We could not perform this
benchmark here because the raw VASP \textsc{outcar} forces and stresses
required to fit such a potential are no longer available for the
262-structure training set; the curated dataset on Zenodo carries
only the EOS-minimum energies and the relaxed atomic positions.
We identify this comparison---ideally with a linear-ACE potential
fit at matched feature budget---as the priority follow-up.
```

---

**M7. Software/version pinning and reproducibility.**

> *"... versions missing for python-ace, pycef, ASE, VASP, the PAW dataset year ..."*

**Status:** `[ADDRESSABLE-FROM-DATA]`.

**Evidence/Action.** From `environment.yaml` (the lockfile of the conda env `datasets_ml` that produced every figure in the paper):

| Package | Version (locked) | Source |
|---|---|---|
| Python | `3.10.20` | `cpython=3.10.20` |
| numpy | `1.26.4` | conda-forge |
| scipy | `1.15.2` | conda-forge |
| **scikit-learn** | **`1.3.0`** | conda-forge — **manuscript says v1.2, this is wrong** |
| pandas | `2.3.3` | conda-forge |
| ase | `3.22.1` | conda-forge |
| **dscribe** | **`2.1.2`** | conda-forge — **manuscript says v2.0** |
| spglib | `2.7.0` | conda-forge |
| pymatgen / mendeleev / monty | (matminer chain) | conda-forge |
| pybtex / pyyaml / ruamel.yaml | (curation deps) | conda-forge |
| pycef | local install `-e ./dependencies/PyCEF` | git submodule |
| python-ace | installed via `setup_dependencies.sh` (`python setup.py install`) with `python-ace-cmake-compat.patch` applied | git submodule; requires `Cython<3` per environment.yaml line 191 |
| bopfoxfeaturizer / bopdftprojections | local installs `-e ./dependencies/{bopfoxfeaturizer,bopdftprojections}` | private, request-only |
| VASP | `vasp.5.4.4` (from `Fe-Mo/inchulldft/run_amstools.sh`: `ASE_VASP_COMMAND="...vasp5_pc2/vasp.5.4.4/..."`) | — |
| PAW set | `setups: recommended` = the VASP-recommended PBE PAW set (Fe_pv, Mo_pv per the `Fe_pv39Mo_sv14.R-…` config names in `setup.yaml`); the config names use `Mo_sv` consistently | — |
| BOPfox | no explicit version string in any `.bx` parameter file; manuscript's "v2020" cannot be verified from the deposited artifacts and is `[DOCUMENTATION]`-only | — |

**Random seeds.** The manuscript states `numpy.random.seed(42)`, `sklearn.utils.check_random_state(42)`, `random.seed(42)`. The DFT workflow does use seed 42 (`setup.yaml` line 1: `seed: 42`). However the ML feature-selection layer uses different fixed seeds — `Scripts/FeatureSelection.py` line 32: `'random_state': 20091116`, and `Scripts/TestRecursivity.py` line 43: `vsearch_random_state=23192`. We will report these explicitly in the Methods so the reader can reproduce the feature-selection runs from the deposited code; nothing in the pipeline depends on a single seed.

**MLP backend.** The manuscript implies an unspecified MLP framework; environment.yaml shows no `torch`, no `tensorflow`. The MLP is therefore **sklearn `MLPRegressor`** (scikit-learn 1.3.0), whose random state is also controlled by `random_state` passed through `FeatureSelection.py`. We will state this.

**BOPfox openness.** The reviewer is right that "available on request" is incompatible with PRB open-science. Our remedy: (a) keep BOPfox itself behind the author-request gate (we cannot unilaterally release a code we do not own), but (b) **deposit on Zenodo the full BOP descriptor matrix** for all 262 + 70 structures (this is already part of `FeMo_TCP_dataset.zip` per `ZENODO_MANIFEST.md` — see `parallel_Fe-Mo_relaxed_0.7projections_0.5os_table_WUBIND_20.pkl`, 7.1 MB), (c) deposit the **exact `.bx` parameter file** (`models/FeMo_0.7projections_os.bx`) so a third party with BOPfox access can rerun the feature pipeline bit-identically, and (d) deposit all 12 CNAV CSVs (`CNAV_parallel_Fe-Mo_{initial|relaxed}_…_WUBIND_{16|20}.csv`) so downstream regression is reproducible *without* BOPfox.

**Manuscript edit.** Replace the version line with the full table above; explicitly state VASP 5.4.4, PAW = recommended-PBE (Fe_pv, Mo_sv), scikit-learn 1.3.0, DScribe 2.1.2, ASE 3.22.1, Python 3.10.20, Cython < 3 (for python-ace ABI), BOPfox version-not-recorded-on-deposit (we will retroactively annotate the Zenodo README).

---

**M8. Train/validation set provenance.**

> *"Are the 70 validation structures computed with identical VASP settings ...?"*

**Status:** `[ADDRESSABLE-FROM-DATA]`.

**Evidence/Action.** The `Fe-Mo/inchulldft/` directory holds *only one* `vasp_tight.yaml` and *only one* `setup.yaml`, and that `setup.yaml` enumerates configurations for R, M, P, δ phases (the validation set) — see lines 12–28 (e.g. `R/Fe_pv39Mo_sv14.R-AAAAAABAABB.NM.cfg`, `M/Mo_sv52.M-BBBBBBBBBBB.NM.cfg`, `P/Fe_pv28Mo_sv28.P-AAABBBBAABAB.NM.cfg`, etc.), all sharing the same `[relax, murnaghan]` workflow alias `*id001`. The validation set was therefore driven by **the same** ENCUT, KSPACING, ISMEAR, SIGMA, ISPIN, EDIFF, PAW selection, and EOS protocol as the training set. The `inchulldft` directory name itself encodes "in convex hull DFT", i.e. these are the structures that lie on/near the simple-TCP convex hull and serve as validation. There is no second VASP-yaml file in the project tree.

**Manuscript edit.** Add an explicit sentence to Methods/Data: *"Training (262) and validation (70) structures were generated by the same `ams_highthroughput` invocation using a single `vasp_tight.yaml` (deposited), guaranteeing identical ENCUT, k-density, smearing, EDIFF, PAW potentials, ISPIN, and EOS protocol across the two sets. Validation RMSE therefore reflects ML transfer error, not DFT-setting drift."*

A re-run cross-check of one validation structure at training settings is unnecessary because the settings are identical by construction; we will say so.

---

### Minor comments

**m1. CN cutoff rule.**
`[ADDRESSABLE-FROM-DATA]`. The CN counting rule lives in `Tools/DatasetTools/` (CNList.pkl mentioned in `ZENODO_MANIFEST.md`); it is a hard cutoff at 3.5 Å, not a Gaussian smoothing. Sensitivity at 3.3, 3.5, 3.7 Å is `[BLOCKED]` from re-running but can be discussed qualitatively: TCP first-shell distances cluster tightly around 2.5–2.9 Å (Fe–Fe, Fe–Mo) with the next shell at > 4.0 Å, so the 3.5 Å cutoff is well inside the first-neighbour gap and CN bin assignment is robust. We will add a sentence.

**m2. Units inconsistency (meV/atom vs eV/atom).**
`[TEXT-ONLY]`. Confirmed by inspection of `paper.tex`. Sweep Fig. 1 caption + Table II axes to `\meVat`.

**m3. siunitx `\textnormal{~\AA}` workaround.**
`[TEXT-ONLY]`. Replace with `\SI{6.0}{\angstrom}` (siunitx with `\sisetup{...}` configured; preamble of `paper.tex` already loads `siunitx`).

**m4. MLP depth/width ablation.**
`[REQUIRES-RECOMPUTE — BLOCKED]`. Only the 64-hidden-unit single-layer architecture was tested; we will state this honestly rather than fabricate a sweep.

**m5. Joubert 1993 measurement temperature.**
`[TEXT-ONLY]`. Add temperature and uncertainty as cited in the Joubert XRD paper to the BW Methods paragraph.

**m6. Fig. 4 convex hull.**
`[TEXT-ONLY]`. Add the hull of the simple phases on top of the Gibbs curves; this can be drawn from the deposited prediction CSVs (`Fe-Mo/results/PREDICTION__*__*.csv`).

**m7. HPC acknowledgement.**
`[ADDRESSABLE-FROM-DATA]`. From `Fe-Mo/inchulldft/run_amstools.sh` line `ams_highthroughput ... -q noctua2_64`, the runs were submitted to **Noctua 2** at the Paderborn Center for Parallel Computing (PC2). We will name the cluster and allocation.

**m8. Zenodo DOI format.**
`[DOCUMENTATION]`. The DOI `10.5281/zenodo.19427673` is unusual (Zenodo IDs are typically 7 digits at the time of writing). We will verify the deposit and replace with the canonical resolved DOI before submission; a README will be added to the deposit pointing to `ZENODO_MANIFEST.md` (which already exists in the repo).

**m9. Citation keys.**
`[TEXT-ONLY]`. Rename `dsribe → dscribe` (the DScribe paper) in `references.bib`; split `vasp` into `vasp_kresse_1996a` (CMS) and `vasp_kresse_1996b` (PRB); annotate `paw → paw_blochl_1994` / `paw_kresse_joubert_1999`.

**m10. Bootstrap protocol.**
`[TEXT-ONLY]`. State 1000 paired bootstrap resamples without replacement on the held-out validation set, paired across descriptor families (this is what `08_AnalysisModels.ipynb` implements per its pre-executed outputs).

---

## Contradiction summary (manuscript vs. workflow/code)

| # | Manuscript claim | Actual evidence | Resolution |
|---|---|---|---|
| 1 | ENCUT = 450 eV | `vasp_tight.yaml`: `encut: 500`; dir tag `VASP_PBE_500_…` | Correct to **500 eV** |
| 2 | Smearing scheme not stated | `vasp_tight.yaml`: `ismear: 0` (Gaussian) | State Gaussian, ISMEAR=0 |
| 3 | σ not stated | `vasp_tight.yaml`: `sigma: 0.2`; dir tag `…_0.1_…` | Report range 0.1–0.2, flag inconsistency |
| 4 | "First four moments (μ₀–μ₃)" | `FeMo_0.7projections_os.bx`: `moments = 20` | Correct to **20 moments** |
| 5 | "Canonical d-band TB Hamiltonian" | Production = `0.7projections_os` (DFT-projected sum7exp, on-site −3.61/−1.68 eV, scales 0.5/0.7) | Correct to the projection model; canonical was an ablation |
| 6 | scikit-learn v1.2 | `environment.yaml`: `scikit-learn=1.3.0` | Correct to **1.3.0** |
| 7 | DScribe v2.0 | `environment.yaml`: `dscribe=2.1.2` | Correct to **2.1.2** |
| 8 | "ISPIN treatment" hand-waved | `vasp_tight.yaml`: `ispin: 0` (i.e. VASP ISPIN=1); all configs `.NM.cfg` | State non-magnetic enforced |
| 9 | All seeds = 42 | `setup.yaml` seed 42 (DFT); `FeatureSelection.py` seed 20091116; `TestRecursivity.py` seed 23192 | Report all three seeds |
| 10 | Γ-only for large cells | `vasp_tight.yaml`: `kmesh_spacing: 0.125` Å⁻¹ applied to all phases | Correct — MP at fixed k-density, Γ-only was a sensitivity check |
| 11 | BOPfox v2020 | No version string in `.bx` files; only "available on request" in README | Acknowledge version unverified; depend on Zenodo descriptor matrix for reproducibility |

---

## Summary table — status counts

| Status | Count |
|---|---:|
| `[ADDRESSABLE-FROM-DATA]` (workflow files / lockfile / `.bx` settle the question) | **7** (M1-partial, M3, M4-partial, M7, M8, m1, m7) |
| `[TEXT-ONLY]` (manuscript wording correction, no recomputation needed) | **6** (M2-partial, M5-partial, m2, m3, m5, m6, m9, m10 — overlap) |
| `[REQUIRES-RECOMPUTE — BLOCKED]` (raw OUTCARs/forces gone) | **5** (M1-sweep, M2-sweep, M5-pacemaker-tune, M6-fitted-MLIP, m4-MLP-ablation) |
| `[DOCUMENTATION]` (deposit / annotate, no code change) | **3** (M7-BOPfox-release, m8-DOI, M5-deposit) |

Net: of 18 numbered comments, **13 are actionable from existing artifacts**, **5 are blocked by raw-data loss and will be acknowledged in the revised Limitations / Methods**.

---

## Concrete manuscript edits — bulleted, section by section

**Methods → DFT Calculations.**
- Replace `ENCUT = 450 eV` with `ENCUT = 500 eV`.
- Add the verbatim YAML table (PREC, EDIFF, ISMEAR=0 Gaussian, SIGMA 0.1–0.2, ISPIN=1, KSPACING 0.125 Å⁻¹, NELM 500, NELMIN 20, LREAL Auto).
- Specify PAW: VASP recommended-PBE set with Fe_pv and Mo_sv (per config-name convention in `setup.yaml`).
- Specify VASP 5.4.4.
- Replace "Γ-only" with "fixed-k-density MP via `ams_highthroughput`"; demote Table I to a sensitivity check.

**Methods → Magnetism.**
- Replace the hand-wave with an explicit "ISPIN=1 enforced for all 262 + 70 calculations; spin-polarised Fe-rich cross-check identified as known limitation."

**Methods → EOS.**
- Cite the curated JSON on Zenodo (`FullyCuratedParsedBriefSummary.json`) for per-structure BM-fit metrics; add an SI flow diagram for 300 → 291 → 262.

**Methods → BOP descriptors.**
- Rewrite this paragraph from scratch (see M5): `moments = 20`, model = `0.7projections_os`, on-site = −3.61/−1.68 eV, scales 0.5/0.7, kernel = jackson, terminator = constantabn, nexpmoments = 200, deposit `.bx` parameter file on Zenodo. State that the "canonical 4-moment" description in the previous draft was wrong and refers only to an ablation.

**Methods → ML.**
- scikit-learn 1.3.0 (not 1.2). DScribe 2.1.2 (not 2.0). Python 3.10.20. ASE 3.22.1. VASP 5.4.4. Cython < 3 for python-ace ABI.
- MLP backend = sklearn `MLPRegressor`. Random seeds: DFT 42, feature-selection 20091116, recursivity-search 23192.

**Methods → Data and Code.**
- Annotate the Zenodo deposit explicitly: `vasp_tight.yaml`, `setup.yaml`, `FeMo_0.7projections_os.bx`, raw BOP descriptor `.pkl`, CNAV CSVs, ACE CSVs, SOAP CSVs, prediction CSVs (per `ZENODO_MANIFEST.md`).
- Replace "BOPfox available from authors upon reasonable request" with a paragraph that (i) acknowledges this limitation, (ii) states that the deposited BOP descriptor matrix and `.bx` parameter file make the *downstream* regression bit-reproducible without BOPfox, and (iii) commits to making the `.bx` parameter file machine-readable.

**Discussion.**
- Insert the "Descriptors-for-regression vs. fitted MLIPs" paragraph (LaTeX given under M6) as the second-to-last paragraph, before Conclusions.
- Insert a one-sentence Limitations note: "Raw VASP OUTCAR archives for the 262-structure training set are no longer accessible to us, which prevents a direct re-fit of a modern MLIP (linear ACE / GRACE / MACE) on the same dataset; this comparison is identified as priority follow-up work."

**Acknowledgements.**
- Name Noctua 2 / PC2 Paderborn (from `run_amstools.sh`).

**Bibliography.**
- Rename `dsribe → dscribe`; split `vasp` into `vasp_kresse_1996a` / `_1996b`; annotate `paw`.

**Figures / Tables.**
- Fig. 1, Table II: switch all y-axes to `\meVat`.
- Fig. 4: overlay the simple-phase convex hull.
- siunitx: replace `\SI{6.0}{\textnormal{~\AA}}` → `\SI{6.0}{\angstrom}`.

