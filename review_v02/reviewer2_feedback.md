# Referee Report — Phys. Rev. B

**Manuscript:** "Data-efficient machine-learning of complex Fe–Mo intermetallics using domain knowledge of chemistry and crystallography" (Forti *et al.*)

**Reviewer:** Reviewer 2 — Atomistic simulations, MLIPs & simulation workflows

---

## (i) Summary

The authors present an ML framework that predicts formation energies of complex Fe–Mo TCP phases (R, M, P, δ) from models trained exclusively on simple TCP phases (A15, C15, C14, C36, σ, χ, μ). The approach combines three structural descriptor families (BOP moments via BOPfox, ACE via `python-ace`, SOAP via DScribe), aggregated through a coordination-number-resolved averaging (CNAV) scheme, and fed into a VotingRegressor ensemble (KRR + RF + MLP). The central physical claim is that BOP descriptors deliver the best simple→complex transfer, with test-set RMSE of 28 ± 3 meV/atom and validation RMSE of 35–42 meV/atom. ML-predicted energies are subsequently used inside a Bragg–Williams/CEF model to obtain R-phase sublattice occupancies, in reasonable agreement with Joubert (1993) XRD data.

The scientific question—whether physically motivated descriptors plus a small DFT budget can outperform black-box featurisation for thermodynamic transferability—is timely and well posed. The narrative is clear and the BOP vs. ACE vs. SOAP comparison is, in principle, valuable to the community. However, from the perspective of DFT-protocol rigour, dataset provenance, and fair benchmarking against modern fitted MLIPs, the manuscript is significantly under-documented. I recommend **major revision** before the paper can be accepted at PRB.

---

## (ii) Major Comments

**1. DFT convergence evidence is inadequate for a metallic intermetallic study.**
Methods §"DFT Calculations" states *"The plane-wave energy cutoff was fixed at 450 eV"* and *"Monkhorst–Pack k-point meshes were chosen to ensure total energy convergence to within 1 meV/atom"*, but no ENCUT convergence test, no per-phase k-mesh table (density per Å⁻¹), and no smearing scheme (Methfessel–Paxton order, σ value, tetrahedron+Blöchl?) are reported. For Fermi-surface-sensitive metallic systems like Fe–Mo, the choice between MP smearing and tetrahedron sampling can shift formation energies by several meV/atom—comparable to the differences the authors are trying to resolve. Please add a supplementary table giving ENCUT, k-point density, smearing type and width, EDIFF/EDIFFG, ISMEAR/SIGMA, ISPIN, and PAW potential identifiers (e.g., `Fe_pv`, `Mo_pv`, `Mo_sv`) per phase.

**2. The Γ-only justification for the large TCP cells is unconvincing as presented.**
Table I (Methods) compares Γ-only with a single 2×2×2 mesh and reports differences < 0.5 meV/atom. For unit cells of R, M, P, δ this is *not* a convergence test—it is a two-point check. Please provide a proper convergence sequence (e.g., Γ, 2×2×2, 3×3×3, 4×4×4) for at least one representative complex phase, *and* report total k-point density (number of k-points × volume) so the reader can compare to standard practice for intermetallic metals (typically ≥ 1000 k-points·Å⁻³).

**3. Magnetic treatment is hand-waved.**
The statement *"TCP phases are non-magnetic, so the NM reference avoids spurious magnetic contributions"* needs evidence. Have the authors actually performed spin-polarised (ISPIN=2) calculations on Fe-rich TCP cells to confirm that the magnetic moments collapse to zero, or are all calculations enforced non-magnetic by setting ISPIN=1? In Fe-rich χ and μ phases, residual local moments on certain Wyckoff sites have been reported in the literature. A supplementary table of magnetic moments per Wyckoff site (or a clear statement that ISPIN=1 was enforced) is needed.

**4. EOS fitting protocol is under-specified.**
The Methods state *"a series of constant-volume calculations spanning a range of volumes around the equilibrium, followed by E–V curve fitting using a third-order Birch–Murnaghan equation of state"*, but the number of volume points, the strain range, residuals of the BM fit, and the criterion for excluding *"duplicate and low-quality fits"* (Results §"Training Dataset", which mentions ~300→291→262 structures) are missing. Reproducibility requires that the data-curation pipeline that took ~300 raw calculations down to 262 ML inputs be fully documented, ideally as a flow diagram or notebook in the Zenodo deposition.

**5. Fairness of the BOP vs. ACE vs. SOAP comparison is not established.**
The headline claim is *"BOP descriptors consistently outperform ACE and SOAP"*, with BOP using 4 moments at fixed canonical d-band TB parameters, ACE at cutoff 6.0 Å and ν ≤ 4, and SOAP at r_cut = 6.0 Å, n_max = 8, l_max = 6. These three descriptors have very different effective cutoffs, body orders, and hyperparameter budgets. BOP moments encode bond-angle information via products of two-centre integrals up to fourth moment, which is implicitly a ν = 4 expansion *with a TB-fitted radial dependence*. ACE and SOAP are evaluated with generic radial bases. A truly fair comparison would either (i) tune ACE radial basis on the Fe–Mo dataset (e.g., via `pacemaker` with optimised radial functions and a similarly sized active feature set), or (ii) compare at matched feature count after selection. As reported, the comparison risks reflecting hyperparameter choices rather than intrinsic descriptor power.

**6. Why descriptors-for-regression instead of a fitted MLIP?**
A central methodological gap: with 262 DFT structures (energies, presumably also forces and stresses available in the OUTCARs), the authors are in the size regime where a fitted MLIP—linear ACE via `pacemaker`, nonlinear ACE/GRACE via `tensorpotential`, or a graph-based MACE/Allegro—would deliver not just formation energies but forces, phonons, elastic constants, and finite-T MD. The manuscript never discusses why a fixed-descriptor + scalar regression was chosen over fitting a true potential. Please add a paragraph in the Discussion that explicitly addresses this: is the BOP feature advantage expected to survive when ACE is fit as a *potential* rather than used as a *fingerprint*? A small companion benchmark fitting a linear ACE (pacemaker, default settings, ν ≤ 4, cutoff 6 Å) on the same 262 structures and evaluating on the 70-structure validation set would substantially strengthen the paper. As written, the comparison is unfair to ACE.

**7. Software/version pinning and reproducibility are incomplete.**
Versions are given for some packages (`BOPfox v2020`, `DScribe v2.0`, `scikit-learn v1.2`) but missing for `python-ace`, `pycef`, ASE, VASP, the PAW dataset year, and the Python interpreter. Random seeds are fixed for NumPy/sklearn but not for the MLP training (PyTorch/TensorFlow? sklearn MLPRegressor?). The statement *"The BOPfox code used for BOP descriptor computation is available from the authors upon reasonable request"* is incompatible with PRB's open-science expectations: BOPfox is not openly distributed, so the BOP feature pipeline is in practice unreproducible. At minimum the authors must (a) deposit the pre-computed BOP descriptor matrix at Zenodo (DOI 10.5281/zenodo.19427673), (b) state the exact BOPfox parameter file (canonical d-band TB hopping integrals, on-site levels, cutoff), and (c) verify that the deposited Zenodo entry contains POSCAR/INCAR/KPOINTS/OUTCAR for all 291 (or 262) calculations, not only the descriptors.

**8. Train/validation set provenance.**
Are the 70 validation structures (R, M, P, δ) computed with *identical* VASP settings, PAW potentials, smearing, k-point density, and EOS protocol as the 262 training structures? If not, a fraction of the validation RMSE may be DFT-setting noise rather than ML error. Please add an explicit statement and, ideally, a cross-check where one validation structure is recomputed at the training-set settings.

---

## (iii) Minor Comments

1. The Methods state that CN is determined *"from the ACE radial function analysis using a cutoff of 3.5 Å"*. Please give the actual rule (e.g., counting neighbours within 3.5 Å, or a smoothed Gaussian-weighted count) and discuss sensitivity of CNAV bins to this cutoff (3.3, 3.5, 3.7 Å).

2. Units inconsistency: the abstract and main text use meV/atom, but Table II (test performance) and Fig. 1 caption use eV/atom for the y-axis. Please harmonise to meV/atom throughout, consistent with the PRB unit convention and the macro `\meVat` defined in the preamble.

3. siunitx usage `\SI{6.0}{\textnormal{~\AA}}` is unusual; the conventional `\SI{6.0}{\angstrom}` (with `\usepackage{siunitx}` configured for `\angstrom`) renders correctly without the manual `\textnormal{~...}` workaround.

4. The MLP architecture *"single hidden layer with 64 neurons"* is shallow even by 2020 standards; please report whether deeper or wider variants were tested and report the impact on RMSE.

5. The 1700 K choice for the BW analysis is justified by *"the typical annealing temperature of the experimental XRD measurements"* but the original Joubert (1993) measurement temperature should be cited explicitly with its uncertainty.

6. Figure 4 (Gibbs free energy curves) would benefit from showing the convex hull of the simple phases to allow the reader to judge phase competition; at present the curves are shown but the tangent construction / hull is absent.

7. The acknowledgement of computational resources is generic. PRB requires identification of the HPC system (cluster name, allocation).

8. The Zenodo DOI `10.5281/zenodo.19427673` should be verified—the seven-digit-then-eight-digit format is unusual; please confirm the link resolves and provide a README in the deposit.

9. Several citation keys (`dsribe`, `vasp`, `paw`) need expansion in `references.bib` — `dsribe` should be `dscribe`; `vasp` should distinguish Kresse–Furthmüller 1996a vs. 1996b.

10. The claim *"BOP advantage over ACE is statistically significant (p<0.01, bootstrap test)"* is a statistical-ML question better assessed by Reviewer 3, but the bootstrap protocol (number of resamples, with/without replacement, paired or unpaired) should still be stated in Methods.

---

## (iv) Recommendation

**Major revision.** The physical question is well chosen and the BOP/CNAV idea has merit, but the manuscript as written under-documents the DFT protocol, presents an unfair descriptor comparison versus modern fitted MLIPs (pacemaker/ACE, GRACE, MACE), and falls short of current reproducibility expectations for a method-oriented PRB paper. A revised version that adds the convergence tables, deposits all DFT and descriptor inputs, and ideally includes a head-to-head against a fitted linear ACE potential on the same dataset would be a strong candidate for publication.
