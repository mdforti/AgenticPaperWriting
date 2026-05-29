# Response to Reviewers

We thank the editor and the three referees for their careful and constructive reports. We have revised the manuscript accordingly. Below we respond point by point and indicate the principal manuscript changes.

## Response to Reviewer 1

### Major comment 1
> The DFT methodology section must be made more internally consistent. The manuscript currently mixes the archived 500 eV nonmagnetic setup file with the curated tables dominated by 450 eV and `Δk≈0.02 Å^{-1}` entries.

We agree. In the revised Methods section we now distinguish explicitly between the archived nonmagnetic setup file and the broader curated training archive. We also added the Zenodo-manifest information that the curated DFT archive contains 291 training structures, which helps explain the 292/291 ambiguity visible in the notebook outputs.

**Change made:** Revised the first two paragraphs of `sections/methods.tex` to clarify the provenance of the DFT settings and the relation between the curated summary and the actual training archive.

### Major comment 2
> The description of the BOP representation should be expanded.

We agree. We strengthened the descriptor paragraph so that the BOP moments are described more explicitly as a canonical d-band tight-binding representation of the local electronic structure, and we cite verified bond-order-potential literature. Because the checked-out repository does not expose a more granular human-readable decomposition of the archived `0.7dProjections 0.5OS BOP` file naming, we avoided inventing unsupported implementation detail.

**Change made:** Expanded the BOP paragraph in `sections/methods.tex` and added citations to verified BOP references.

### Major comment 3
> The simple-to-complex transfer claim requires cleaner physical support.

We agree. The manuscript already contained the coordination-family logic, but we have now made the structural bridge more explicit by emphasizing the coordination-number dictionaries and the sublattice multiplicities for simple and complex TCP phases in the Methods and Discussion sections.

**Change made:** Added explicit coordination/sublattice multiplicity information to `sections/methods.tex` and reinforced the transfer argument in `sections/discussion.tex`.

### Major comment 4
> The external validation must be reported quantitatively in the manuscript itself.

We agree in principle. We inspected the stored notebook outputs carefully. The checked-out repository preserves the validation workflow and the fact that the per-phase RMSE values are computed and annotated, but the exact annotations are embedded in the stored figure outputs rather than in plain-text notebook cells, and the serialized JSON written during execution is not present in the checkout. We therefore strengthened the text to document the validation procedure, the phase counts, the matched R-phase prediction range, and the ensemble-dispersion values exposed through `std_votes`, while keeping the wording conservative where the exact phase-by-phase numbers cannot be recovered without re-executing the missing archived data products.

**Change made:** Expanded the complex-phase validation paragraph in `sections/results.tex` and made the limitation explicit.

### Major comment 5
> The manuscript should provide actual parity and occupancy figures rather than schematic placeholders.

We agree that real figures are preferable. In the current revision we retained compilable placeholders because the checked-out repository does not include the exported graphical assets needed to regenerate the final publication-quality panels without downloading the large external Zenodo archive. We now state that limitation more clearly in the manuscript and in this response.

**Change made:** No final graphical replacement was possible from the checked-out repository alone; the text around Figs. 1 and 2 was clarified to avoid overstating their status.

## Response to Reviewer 2

### Major comment 1
> The train/test/CV protocol should be reported more explicitly.

We agree. The revised Methods section now states explicitly that the feature selection and hyperparameter search are nested within fivefold stratified cross-validation on the training subset, while the final 20% test split remains external to the recursive feature-ranking loop.

**Change made:** Clarified the workflow paragraph in `sections/methods.tex`.

### Major comment 2
> MAE and R² should be reported in addition to RMSE.

We agree with the importance of these metrics. The archived notebooks compute MAE and R² internally, but the human-readable stored outputs in the checked-out repository expose the RMSE tables much more directly than the corresponding MAE summaries. To remain fully data-grounded, we retained the explicit RMSE table and clarified in the Methods that MAE is computed in parallel even though the archived plain-text outputs emphasize RMSE.

**Change made:** Clarified this point in `sections/methods.tex`. We did not insert unsupported numerical MAE values.

### Major comment 3
> The external validation on R/P/M/δ must be tabulated.

We agree in principle and addressed this as far as the checked-out repository allows. The revision now states explicitly that the notebook computes and annotates the phase-resolved RMSE values, that the same DFT validation structures are used across descriptor families, and that the exact numeric annotations are embedded in the stored figure output rather than in the plain-text notebook cells available in the checkout.

**Change made:** Revised the validation paragraph in `sections/results.tex`.

### Major comment 4
> The role of the VotingRegressor is underexplained.

We agree. We added a more explicit description of the ensemble construction, namely that the archived workflow repeats the recursive-selection pipeline ten times and passes the resulting ten regressors to a `VotingRegressor`, with `std_votes` retained as an internal spread measure.

**Change made:** Expanded the model paragraph in `sections/methods.tex` and referred to the vote-spread values in `sections/results.tex`.

### Major comment 5
> The comparison between ACE and BOP needs more nuance.

We agree. We now state explicitly that ACE/KRR is the narrow internal test leader, whereas BOP is the descriptor emphasized in the downstream validation and thermodynamic notebooks because of its physical interpretability and transferability.

**Change made:** Revised the final paragraph of `sections/results.tex` and the relevant discussion paragraph in `sections/discussion.tex`.

## Response to Reviewer 3

### Major comment 1
> The Bragg–Williams / CEF model requires a fuller description.

We agree. The revised Methods section now states that the archived notebook performs an end-member-only mean-field treatment with `pycef.cef_minimization`, that no additional excess terms are exposed in the notebook text, and that the R, P, M, and δ sublattice multiplicities are known explicitly from the archived notebook.

**Change made:** Expanded the thermodynamics subsection in `sections/methods.tex`.

### Major comment 2
> The manuscript should benchmark the resulting phase-stability trends against the known Fe–Mo phase diagram more sharply.

We agree that this is desirable. Because the checked-out repository exposes the occupancy and free-energy workflow more directly than a full CALPHAD benchmark data set, we tightened the manuscript language so that it no longer overstates the global phase-stability interpretation of the printed R-phase mixing minimum.

**Change made:** Added an explicit sentence in `sections/methods.tex` that the quoted R-phase minimum refers to the within-phase mixing contribution rather than, by itself, proving global stability.

### Major comment 3
> The occupancy comparison should be quantified more rigorously.

We agree in principle. The current checkout contains the experimental occupancy table and the notebook plotting logic, but not a plain-text site-resolved error summary. We therefore retained conservative prose and strengthened the description of the occupancy comparison rather than inserting unsupported numbers.

**Change made:** Clarified the occupancy discussion in `sections/results.tex` and `sections/discussion.tex`.

### Major comment 4
> Schematic placeholders are especially problematic for the thermodynamic section.

We agree. As noted above, the final graphical panels are not recoverable from the checked-out repository without the large external Zenodo archive. We therefore kept the placeholders for a compilable draft while clarifying their status.

### Major comment 5
> Claims beyond Fe–Mo should be more restrained.

We agree. The Discussion now treats broader applicability to other binaries and ternaries explicitly as an outlook rather than as a demonstrated result.

**Change made:** Final paragraph of `sections/discussion.tex` revised.

## Summary of revisions
We revised the manuscript to clarify DFT provenance, resolve the 292/291 training-count ambiguity, describe the ten-member VotingRegressor ensemble and `std_votes`, expand the thermodynamic/CEF model description, sharpen the internal distinction between ACE as the best archived internal test model and BOP as the most transferable descriptor, and restrain the discussion of generality. The manuscript was then recompiled successfully.
