# Review by Reviewer 3 — Thermodynamics & Phase Stability (CALPHAD / TCP Phases)

## (i) Summary

This manuscript combines machine-learning-predicted formation energies with the compound energy formalism (CEF) and Bragg–Williams (BW) approximation to predict finite-temperature sublattice occupancies of Fe–Mo TCP phases. The central result is that ML models trained only on simple TCP phase energies can reproduce experimental X-ray diffraction data for the R-phase site occupancies. The thermodynamic analysis is a welcome addition to what would otherwise be a purely computational ML study, and the connection to experiment strengthens the paper considerably.

However, several aspects of the thermodynamic modelling require closer scrutiny. The Bragg–Williams approximation has known limitations for ordered intermetallics, and the comparison with the known Fe–Mo phase diagram raises questions about the quantitative reliability of the predicted free energy curves.

## (ii) Major Comments

**1. Bragg–Williams approximation vs. experimental reality.**
The authors use the ideal Bragg–Williams (BW) approximation (Gᴱ = 0), which assumes random mixing on each sublattice and neglects short-range order (SRO). For TCP phases with large unit cells and strong site preferences, SRO effects can be significant. The R phase, in particular, has 11 distinct Wyckoff sites with well-documented occupancies. The approximation Gᴱ = 0 should be justified explicitly. At minimum, the authors should estimate the magnitude of the SRO contribution (e.g., via a cluster variation method calculation or by comparing with a CALPHAD assessment that includes excess terms). How sensitive are the predicted occupancies to small positive or negative excess Gibbs energies?

**2. Temperature choice.**
The thermodynamic analysis is performed at 1700 K. The Fe–Mo phase diagram shows that TCP phases are stable over a range of temperatures, with some phases (e.g., μ, σ) having stability down to lower temperatures. Why was 1700 K chosen? Is this the temperature at which the experimental XRD data were collected? If not, the temperature dependence of the site occupancies should be discussed. The experimental R-phase XRD data cited for validation — at what temperature were these measurements performed?

**3. Consistency with the Fe–Mo phase diagram.**
Figure 4 shows Gibbs free energy curves at 1700 K. The relative ordering of phase stabilities from the ML-predicted energies should be compared with the experimentally assessed Fe–Mo phase diagram (e.g., from the CALPHAD assessment by Jacob et al. or from the ASM phase diagram database). Specifically:
- Is the predicted stability range of each phase consistent with the known composition range?
- Are the relative stabilities (which phase is most stable at a given composition) consistent with experiment?
- The ML models were trained on formation energies referenced to NM hcp elements — does this produce consistent absolute Gibbs energies for phase diagram construction?

A direct comparison with an established CALPHAD assessment of the Fe–Mo system would significantly strengthen the thermodynamic validation.

**4. Site-occupancy prediction: quantitative agreement vs. qualitative agreement.**
The authors state that predicted sublattice occupancies are "in quantitative agreement with experimental XRD data." However, no quantitative goodness-of-fit metric is reported (e.g., R-factor, weighted R-factor, or mean absolute deviation in site fractions). The reader needs to know: which sites agree within experimental uncertainty, and which do not? The error bars in Figure 5 need explicit definition — are they ML prediction uncertainty, experimental uncertainty, or both? A site-by-site table with ML-predicted vs. experimental Mo fractions would be more informative than a qualitative statement.

**5. Only one phase (R) is validated against experiment.**
The thermodynamic validation is limited to the R phase, because XRD data are only available for this phase. The authors should discuss whether the approach is expected to work equally well for M, P, and δ phases, and what experimental data would be needed to test this. The claims about "transferability to other binary systems" in the Discussion are speculative without experimental or computational validation in at least one additional system (e.g., Fe–W or Co–Mo).

## (iii) Minor Comments

1. The SLSQP optimiser is mentioned but no convergence criteria or starting-point sensitivity is reported. Site-occupancy optimisation in a high-dimensional CEF space can have multiple local minima. Please report whether the optimisation was run from multiple starting points and whether the same minimum was found consistently.
2. Equation (1): The site-fraction notation yᵢ⁽ˢ⁾ is standard but the relationship between the end-member energies Gᵢ° and the ML-predicted formation energies could be clarified. Are the end-member energies taken directly as the ML-predicted E_f^{nmhcp} values? How are end-members with mixed occupancy handled?
3. The excess Gibbs energy Gᴱ is set to zero (ideal BW). In standard CALPHAD practice, the excess term includes binary interaction parameters L_{ij} that are fitted to experimental data. Could the authors provide a sensitivity analysis showing whether small non-zero interaction parameters (e.g., L = ±5 kJ/mol) significantly alter the predicted occupancies?
4. The paper mentions "R-phase sublattice occupancies" but does not specify the site definitions (Wyckoff positions, multiplicity) for the R phase. A table of the R-phase crystal structure (space group, lattice parameters, Wyckoff sites, coordination numbers) would aid reproducibility.
5. References to prior CALPHAD assessments of Fe–Mo: the authors should cite and discuss the work of Jacob et al. (CALPHAD 2000) or similar assessments.

## (iv) Recommendation

**Major Revision.** The connection between ML-predicted energies and thermodynamic modelling is one of the most interesting aspects of this work, but several technical details need to be clarified and the validation against experiment needs to be placed on a more quantitative footing. In particular, the sensitivity of the site-occupancy predictions to the Bragg–Williams approximation should be assessed. With these additions, the paper would make a solid contribution to PRB.
