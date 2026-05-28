# Reviewer 1 Feedback

## Summary
This manuscript addresses an important and difficult problem, namely the prediction of TCP-phase energetics in Fe--Mo from a comparatively small DFT data set using physically informed descriptors. I find the general strategy attractive, particularly the attempt to combine local bond-order-potential moments with coordination-number-resolved averaging and then to test the resulting models on more complex phases. The manuscript is readable and already contains several technically useful details. However, in its present form it does not yet meet the standard expected for a Physical Review B article because the electronic-structure provenance is not sufficiently sharp, the descriptor comparison is not always disentangled from differences in archived workflows, and the external-validation evidence is described qualitatively where quantitative reporting is required.

## Major comments
1. The DFT methodology section must be made more internally consistent. The manuscript correctly notes that the repository exposes a nonmagnetic setup file with `ENCUT=500 eV`, `ISMEAR=0`, `SIGMA=0.2 eV`, and `kmesh_spacing=0.125 Å^{-1}`, but it also states that the curated tables are dominated by 450 eV and `Δk≈0.02 Å^{-1}` entries. At present this reads as a mixture of two workflows rather than as a clean production protocol. The authors should identify which settings correspond to the actual training data, which correspond to the later validation workflow, and whether all structures were recomputed consistently before model fitting. A referee cannot assess the reliability of the energetic ranking without this provenance.

2. The description of the BOP representation should be expanded. The manuscript states, correctly in broad terms, that the descriptors are moment-based and physically interpretable, but it does not explain which moments were retained, how the 0.7d projections and 0.5OS settings modify the underlying canonical model, or why this variant should outperform the canonical BOP baseline. Because the manuscript emphasizes physical interpretability, the authors should explain the relationship between the retained moments and the local $d$-band electronic structure in more concrete terms.

3. The simple-to-complex transfer claim requires cleaner physical support. The paper argues that complex TCP phases reuse local environments already present in the simpler prototypes, which is plausible, but the supporting evidence is currently qualitative. I recommend including at least one compact analysis that maps the coordination/site families represented in the simple phases onto those appearing in $R$, $P$, $M$, and $\delta$. Without such a bridge, the transfer argument remains more suggestive than demonstrated.

4. The external validation must be reported quantitatively in the manuscript itself. The text currently says that the notebook parity plots annotate phase-resolved RMSE values but does not list those values because the checked-out repository does not expose them as plain text. That is not sufficient for publication. The authors need to recover the actual $R$, $P$, $M$, and $\delta$ errors for BOP, ACE, and SOAP and tabulate them, even if this requires rerunning or exporting the archived notebook state more carefully.

5. The manuscript should provide at least one genuine parity figure rather than schematic placeholders. For an electronic-structure and descriptor paper, a placeholder box is not adequate evidence. The same concern applies to the occupancy comparison. These figures are central to the claims and should be included in publishable form.

## Minor comments
1. The manuscript should state explicitly whether the formation energies are based on fully relaxed magnetic states for the FM data and on separate nonmagnetic relaxations for the NM data, or whether some reference structures were reused.
2. The Murnaghan fitting is mentioned, but the quality criteria for accepting or rejecting equation-of-state fits are not reported.
3. The introduction and methods still contain `% TODO: CITE` placeholders for core TCP and BOP literature. These must be resolved before submission.
4. It would help the reader to explain why the internal test leader is ACE/KRR whereas the downstream interpretation centers BOP.
5. Please define once, in words, what “0.5OS” means in the BOP feature name.

## Recommendation
Major Revision
