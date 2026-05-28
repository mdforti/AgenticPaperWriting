# Review by Reviewer 1 — Computational Materials Physicist (DFT & Tight-Binding)

## (i) Summary

This manuscript presents a machine-learning framework for predicting formation energies and sublattice occupancies of topologically close-packed (TCP) intermetallic phases in the Fe–Mo binary system. The authors train models on 262 DFT calculations of simple TCP phases (A15, C15, C14, C36, σ, χ, μ) and demonstrate transferability to structurally complex phases (R, M, P, δ) with 11–14 Wyckoff sites. A key methodological contribution is coordination-number-resolved averaging (CNAV) of local structural descriptors. Three descriptor families are compared: bond-order potential (BOP) moments, atomic cluster expansion (ACE), and smooth overlap of atomic positions (SOAP). The BOP descriptors, derived from a canonical d-band tight-binding Hamiltonian, are found to consistently outperform ACE and SOAP.

The topic is relevant and the experimental-theoretical cross-validation (XRD sublattice occupancies) is commendable. However, several aspects of the DFT methodology and the physical interpretation of descriptor transferability require clarification before I can recommend publication.

## (ii) Major Comments

**1. DFT convergence and EOS fitting protocol.**
The Methods section states that plane-wave energy cutoffs of 400–450 eV and Monkhorst–Pack meshes were used. For large-unit-cell phases (R, M, P, δ), single Γ-point calculations were employed. The convergence of total energy differences with respect to k-point sampling for these large cells should be explicitly demonstrated, not merely asserted. A single Γ-point may be insufficient for metallic systems with sharp features at the Fermi level, particularly for formation energy differences that require sub-10 meV/atom resolution. I recommend the authors provide a convergence table showing formation energy vs. k-point density for at least one representative structure of each complex phase (R, M, P, δ).

**2. Reference state choice.**
The formation energy reference is non-magnetic (NM) hcp Fe and hcp Mo. The choice of NM hcp Fe is unusual — ground-state Fe is ferromagnetic bcc. The authors should justify why the NM hcp reference is appropriate for TCP phases and demonstrate that the relative energetics are insensitive to this reference choice. In particular, the magnetic energy of bcc Fe (bcc–NM) is approximately 0.5 eV/atom — how does this affect the formation energy scale?

**3. BOP moment interpretability.**
The BOP moments (μ₀–μ₃) are computed from a canonical d-band tight-binding Hamiltonian. The authors claim that BOP descriptors "capture the essential chemistry of d-band filling and hybridisation." However, only the first four moments are used. In canonical band theory, the fourth moment already introduces sensitivity to bond angles and topology, but higher moments (μ₅, μ₆) are needed to distinguish certain TCP polytypes. Was there any systematic convergence test with respect to moment order? This is especially relevant because BOP outperforms ACE and SOAP — the physical reason for this should be explored more quantitatively.

**4. CNAV: crystallographic justification vs. circularity.**
The CNAV scheme groups atoms by coordination number and averages descriptors within each CN group. For simple TCP phases, CN values are 12, 14, 15, 16 (the Kasper polyhedra). For complex phases, the same CN values appear. However, two sites with the same CN can have very different local environments (e.g., a CN-12 site in A15 vs. a CN-12 site in χ). How does CNAV distinguish these? The authors should discuss whether the averaging within CN groups discards the very information needed to discriminate between phases. If BOP moments are already site-specific, why is the additional CNAV averaging necessary?

**5. Pulay stress correction.**
The authors state that E–V curve fitting eliminates Pulay stress errors. This is true only if the cell shape and volume are varied consistently. For the constant-volume calculations, did the authors use the same energy cutoff and ENCUT parameter across all volumes? Pulay stress arises from the basis-set incompleteness with respect to volume changes in plane-wave codes. Please confirm that no ENCUT variation is present across the E–V curve.

## (iii) Minor Comments

1. Line 5 of Methods: "single k-point calculations at the Γ-centred point" — typo, should be "Γ-centred" or "Γ-only".
2. The Birch–Murnaghan EOS fitting: was a third-order or second-order EOS used? Please specify.
3. The authors mention "BOPfox code" and "BOP moments" but do not provide the version or the specific DFT→BOP projection parameters (scissor operator shift value, smearing, etc.). These details are essential for reproducibility.
4. The canonical tight-binding Hamiltonian assumes a rectangular d-band. Have the authors considered the effect of the d-band shape (e.g., elliptic vs. rectangular) on the predicted moments?
5. Figure 3 would benefit from an inset zooming into the low-energy region (< 0.1 eV/atom), where the most physically relevant structures lie.

## (iv) Recommendation

**Major Revision.** The DFT convergence documentation and the physical interpretability of the BOP/CNAV comparison need to be strengthened. The core methodology is sound and the results are promising, but the paper would benefit from addressing the above points before publication in Physical Review B.
