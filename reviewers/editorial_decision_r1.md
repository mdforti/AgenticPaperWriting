# Editorial Decision Letter — Round 1

**Manuscript number:** PRB-2025-XXXXX  
**Title:** "Data-efficient machine learning of complex Fe–Mo topologically close-packed intermetallics using domain knowledge of chemistry and crystallography"  
**Date:** [Submission date + handling period]  
**To:** Corresponding Author  

---

## Decision: Major Revision

The manuscript has been reviewed by three referees with complementary expertise in machine-learning methods for materials, computational metallurgy and DFT methodology, and TCP phase metallurgy. I have read all three reports in full and have formed an independent assessment. While the referees agree that the subject matter is appropriate for PRB and that the core scientific contribution — the coordination-number-resolved averaging (CNAV) scheme and its demonstrated effect on prediction accuracy, together with the sublattice occupancy comparison with experiment — is original and meritorious, they have collectively identified concerns that require substantive revision before the manuscript can be accepted. I am therefore requesting a major revision.

The revision deadline is three months from the date of this letter. The revised manuscript must be accompanied by a point-by-point response document addressing every comment raised by each referee. Revised text should be clearly identified (e.g., with a colour-change or markup annotation in a companion version). The response document must quote each referee comment in full and state specifically what change was made and where, or explain clearly why the authors believe the change is unnecessary.

---

## Summary of Referee Opinions and Editorial Assessment

**On the overall merit of the contribution.** All three referees recognise that the paper addresses an important problem. The CNAV scheme receives positive remarks from both Reviewer 1 and Reviewer 3 for connecting the crystallographic hierarchy of TCP phases to a physically motivated descriptor design. Reviewer 2 commends the thermodynamic post-processing via the compound energy formalism. No referee suggests rejection or recommends that the manuscript be redirected to a different journal. The work therefore passes the significance and novelty filters of PRB's editorial criteria.

**On machine-learning methodology (Reviewer 1, Major).** Reviewer 1 identifies the absence of a parity plot for the 20% hold-out test set as a major deficiency. The manuscript reports test-set RMSE values in Table 2 but provides no scatter plot of predicted versus DFT formation energies for the test set. Reviewer 1's concern is well-founded and represents a standard expectation for ML materials science papers at PRB: a parity plot reveals systematic biases, high-energy outlier structures, and composition-dependent model failure that a scalar RMSE conceals. The existing Fig. 5 addresses only the external validation set; it does not substitute for a test-set parity plot. I require the authors to add a parity plot (at minimum for the three best-performing KRR models — BOP+CNAV, ACE+CNAV, and SOAP+CNAV) as a new or revised figure. Reviewer 1 also raises questions about whether feature selection, if any, was performed outside the cross-validation loop. If feature selection was not applied, a single sentence in the Methods to that effect will suffice. If feature selection was applied, the authors must confirm that it was nested within the CV loop. I share the referee's concern: data leakage through improperly nested feature selection is a common and consequential error in ML materials papers, and the absence of documentation on this point is not acceptable.

Reviewer 1's minor comments on the SOAP cutoff radius and the VotingRegressor performance are also substantive. The authors should either provide evidence that 4.0 Å is equivalent to a larger cutoff for SOAP in this system, or acknowledge the choice as a potential limitation in the text. The VotingRegressor ensemble performance relative to the best individual model should be reported explicitly. These are not blocking but must be addressed in the revision.

**On DFT methodology (Reviewer 2, Major).** Reviewer 2 identifies the absence of the electronic smearing method and smearing width as a major omission. The DFT setup section states the pseudopotentials, plane-wave cutoff, and k-point density but does not describe the Fermi-level broadening scheme. For metallic systems with Fe this is not a footnote: the Methfessel–Paxton order and width affect absolute total energies and, through differential cancellation, formation enthalpies at the meV/atom level. Given that the paper makes quantitative claims about energy differences of 20–50 meV/atom, the smearing parameters must be documented. I require this information to be added to the Methods section.

Reviewer 2's comment on k-point convergence for large-unit-cell TCP phases is an important minor concern. For the R phase with 53 atoms per cell, a Δk = 0.020 Å⁻¹ mesh may correspond to a very sparse or even gamma-point sampling depending on the cell geometry. The authors should state whether convergence was verified, ideally with a quantitative bound on the energy error. Reviewer 2's additional minor comments — on the NM-hcp reference choice, the E–V sampling protocol, and the temperature context for the 1700 K analysis — are scientifically well-motivated and should be addressed in the revised text. I note that Reviewer 2's major concern about the NM versus FM reference state, while worth addressing, is less urgent than the smearing documentation; the authors may choose to respond to it primarily in the Discussion rather than by repeating calculations.

**On crystallographic description and TCP phase context (Reviewer 3, Major).** Reviewer 3 raises two major concerns. First, the manuscript identifies the eleven TCP phases by conventional name and atom count but provides no space groups or Pearson symbols. This information is standard in any PRB paper on TCP intermetallics and is necessary for reproducibility: a reader cannot recover the crystal structure from the name alone, particularly for phases like M and δ which have ambiguous naming in different sub-fields. I require the authors to add space groups and Pearson symbols, at minimum in a revised Table 1 or in a new supplementary table. Second, Reviewer 3 notes that the CEF-based thermodynamic analysis at 1700 K is not compared with the assessed Fe–Mo CALPHAD phase diagram, making it impossible for the reader to determine whether the computed stable phase assemblage is physically correct. I agree that this comparison — even a qualitative statement citing the Joubert–Crivello assessed diagram — is essential to establish that the thermodynamic model is producing physically reasonable results.

Reviewer 3's minor comments are collectively important for a senior materials science audience. The Wyckoff site labelling inconsistency (internal labels B1/B2/D1/D2 versus standard Wyckoff letters) must be resolved or explained. The absence of any reference to structure-map approaches to TCP phase stability (Pettifor, Villars et al.) represents a gap in the contextualisation of the work that should be corrected with one or two additional references. The discussion of the technological motivation — specifically the Mo content range relevant to deleterious TCP precipitation in engineering steels versus high-Mo refractory alloys — should be clarified so that readers understand which industrial context the work primarily addresses.

**Where referees agree.** All three referees and I agree that the CNAV scheme is the most original and impactful part of the paper, and all three accept the thermodynamic and occupancy comparison as scientifically relevant. The concerns raised by Reviewers 1–3 are specific and addressable without repeating the core DFT calculations (with the possible exception of verifying k-point convergence for the R phase, which the authors may have data for already). I therefore expect that a careful and thorough response will bring the manuscript to an acceptable state for publication.

---

## Required Changes

The following items are mandatory and must be addressed in the revision. I have grouped them by origin, but the authors should treat every item with equal seriousness.

**From Reviewer 1:**
(R1-M1) Add a parity plot for the 20% hold-out test set for the three best KRR models (BOP+CNAV, ACE+CNAV, SOAP+CNAV).
(R1-M2) State explicitly whether feature selection was performed, and if so confirm that it was nested inside the cross-validation loop.
(R1-m1) Justify the SOAP cutoff radius of 4.0 Å or acknowledge it as a limitation.
(R1-m2) Report the VotingRegressor test-set RMSE and compare it with the best individual model.
(R1-m3) Include cross-validation RMSE alongside test-set RMSE in Table 2 or state why this would be redundant.
(R1-m4) Complete the ACE descriptor documentation (radial cutoff, number of radial basis functions, body-order truncation).

**From Reviewer 2:**
(R2-M1) Document the electronic smearing method (Methfessel–Paxton, Gaussian, or tetrahedron) and the smearing width in the DFT Methods section.
(R2-m1) Address k-point convergence for the R phase specifically; a brief statement on whether convergence was verified will suffice.
(R2-m2) Describe the E–V curve sampling (number of volume points, range relative to estimated equilibrium volume).
(R2-m3) Acknowledge that the NM-hcp reference choice merges structural and magnetic contributions and discuss whether RMSE rankings are expected to be reference-state dependent.
(R2-m4) Place the 1700 K thermodynamic analysis in the context of the Fe–Mo phase diagram stability range for the R phase.
(R2-m5) Confirm that the experimental XRD occupancy data are from Joubert and Crivello (2012) and state the measurement temperature.

**From Reviewer 3:**
(R3-M1) Add space groups and Pearson symbols for all eleven TCP phases discussed; a revised or expanded Table 1 is the appropriate location.
(R3-M2) Compare the computed CEF phase-stability topology at 1700 K (or the nearest stable-phase composition window) with the assessed Fe–Mo phase diagram, citing the CALPHAD literature.
(R3-m1) Clarify the Wyckoff site labelling in Fig. 6 and provide a mapping to the standard crystallographic notation for the R-phase space group.
(R3-m2) Add one or two references to structure-map approaches (Pettifor or Villars et al.) and one or two sentences contextualising the present approach relative to those methods.
(R3-m3) Clarify the technological motivation: identify whether the primary application context is TCP precipitation in low-Mo engineering steels or TCP-matrix high-Mo refractory alloys.
(R3-m4) Add a brief discussion bounding the expected short-range-order correction to the CEF thermodynamics.

---

## Formatting Requirements for Revision

The revised manuscript must continue to compile cleanly with `latexmk -pdf paper.tex` (REVTeX 4.2, `prb,twocolumn`). If the new parity plot or the crystallographic table require a third column or additional page, an appropriate REVTeX layout adjustment is acceptable. All new figures must follow the `\caption{}`/`\label{fig:...}` convention and must be referenced in the text. Any newly cited references must be added to `references.bib` using established BibTeX keys consistent with those already present.

---

## Closing

I appreciate the significant effort that has gone into this manuscript. The core contribution — a domain-knowledge-informed descriptor scheme that improves TCP phase prediction accuracy and transfers from simple to complex phases — is timely and well-executed. The concerns raised by the referees are specific and largely technical in nature; none of them challenge the central scientific claim. I look forward to receiving the revised manuscript.

Yours sincerely,  
**Handling Editor, Physical Review B**

---

## Appendices: Full Referee Reports

The complete text of the three referee reports is appended below. The reports are identified as Report A (Reviewer 1 — ML methodology), Report B (Reviewer 2 — metallurgy and DFT), and Report C (Reviewer 3 — TCP phase metallurgy). The authors are required to respond to every comment in all three reports in their point-by-point response document.

---

### Report A — Reviewer 1 (Machine Learning for Materials Properties)

*[See `reviewers/reviewer1_feedback_r1.md` for full text.]*

**Recommendation:** Major revision  
**Key blocking issue:** Missing test-set parity plot; missing documentation of feature selection procedures.

---

### Report B — Reviewer 2 (Metallurgy and Computational Materials Science)

*[See `reviewers/reviewer2_feedback_r1.md` for full text.]*

**Recommendation:** Major revision  
**Key blocking issue:** Electronic smearing method and width not documented in DFT Methods section.

---

### Report C — Reviewer 3 (TCP Phase Metallurgy, Senior Reviewer)

*[See `reviewers/reviewer3_feedback_r1.md` for full text.]*

**Recommendation:** Major revision  
**Key blocking issues:** Space groups and Pearson symbols absent for all TCP phases; no comparison of CEF-predicted phase stability with the assessed Fe–Mo phase diagram.
