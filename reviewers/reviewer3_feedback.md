# Reviewer 3 Feedback

## Summary
This is an interesting manuscript that goes beyond standard regression benchmarking by attempting to use machine-learned TCP energies in a finite-temperature Bragg--Williams analysis and by comparing the resulting $R$-phase occupancies with experiment. That thermodynamic ambition is welcome and, in my view, constitutes one of the most compelling aspects of the work. The manuscript is also commendably cautious in not overclaiming the precision of the archived repository. Nevertheless, the current version needs revision before it can be considered for publication because the thermodynamic model is described too briefly, the connection to the known Fe--Mo phase stability is not benchmarked sharply enough, and the occupancy comparison is not quantified as rigorously as it should be.

## Major comments
1. The Bragg--Williams / CEF model requires a fuller description. The manuscript states that `pycef.cef_minimization` is used at 1700 K and that end-member energies are taken from machine-learned phase energies, but it does not spell out the sublattice model for the $R$ phase, the optimization variables, or whether any excess interaction terms beyond end-member energies are included. For a reader coming from CALPHAD or CEF, this level of detail is insufficient.

2. The manuscript should benchmark the resulting phase-stability trends against the known Fe--Mo phase diagram or prior CALPHAD assessments. At present I only learn that the $R$-phase mixing term reaches about -53 meV/atom near one composition and that occupancy curves are compared with experiment. I would like to see a clearer statement of which phases are predicted to be thermodynamically competitive at 1700 K and whether those trends are physically plausible for Fe--Mo.

3. The occupancy comparison is potentially a highlight, but it is not yet analyzed quantitatively enough. The paper states that the notebook overlays ML+CEF and experimental site fractions over $x_{\mathrm{Mo}}=0.27958$--0.37978, yet it does not report a site-resolved error measure or identify which sublattices agree best and which disagree most. A mean absolute deviation across all reported site fractions, together with a brief site-by-site discussion, would substantially strengthen this part.

4. The use of schematic figure placeholders is especially problematic for the thermodynamic section. The reader must see the actual free-energy and occupancy curves to judge the physics. Please replace the placeholders with the notebook-generated figures.

5. The manuscript should be more restrained when discussing generalization beyond Fe--Mo. The present repository demonstrates one binary system with a specific family of TCP phases. Extension to other binaries or ternaries is plausible, but it remains an outlook rather than a demonstrated result.

## Minor comments
1. Please state explicitly whether the Bragg--Williams calculations were also attempted for $P$, $M$, and $\delta$, and if so what level of numerical robustness was obtained.
2. The experimental comparison should identify the underlying diffraction study explicitly rather than leaving a citation placeholder.
3. It would help to explain why the occupancy plot is presented as $y_{\mathrm{Mo}}$ versus $x_{\mathrm{Mo}}$ and how this maps onto the sublattice labels used in the notebook.
4. If short-range order is neglected, that limitation should be stated already in the Methods rather than only in the Discussion.
5. The text should clarify whether the reported $R$-phase mixing minimum corresponds to a global thermodynamic preference or only to the mixing contribution within that phase.

## Recommendation
Major Revision
