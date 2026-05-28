# Response to Reviewer 1 — TCP Phases & Industrial Applications Expert

**Manuscript:** *Data-efficient machine-learning of complex Fe--Mo intermetallics using domain knowledge of chemistry and crystallography* (Forti *et al.*)
**Journal:** Physical Review B
**Reviewer:** Reviewer 1 (TCP-phase crystallography / metallurgy / industrial framing)
**Date:** 2026-05-28

---

## Overall response

We thank Reviewer 1 for a careful, metallurgically-grounded report. The Reviewer correctly identifies that the manuscript reads as a methods paper that under-delivers on its industrial framing and that several crystallographic and experimental-comparison statements are imprecise. We accept the diagnosis. We must, however, transparently disclose a constraint that shapes our revisions: the raw DFT/ML compute environment used to generate the present results has been retired and the underlying primary data are no longer recoverable. New DFT calculations on Fe–W, Co–Mo or Ni–Cr–Mo (Major #6) and any re-derivation of XRD-uncertainty-weighted statistics from primary refinement files (Major #4b) are therefore not feasible within this revision. We *can*, however, mine the preserved Jupyter notebook outputs, the curated prototype-structure files, the per-Wyckoff CEF results that are still on disk (`Fe-Mo/results/`, `PrototypeStructures/`, `15_A_Thermodynamics.ipynb`) and the bibliographic record. The revisions below therefore (i) correct the R-phase Wyckoff list using the prototype structure that was actually used, (ii) tabulate the ML-predicted end-member energies from the preserved CSVs (Major #7), (iii) add the missing canonical metallurgical literature (Major #1, #2; Minor #2, #7), (iv) qualify or down-grade the over-reaching claims (Major #4a, #6; Minor #1), and (v) add the Frank–Kasper / Wyckoff mapping the Reviewer requests for CNAV (Major #3).

---

## Point-by-point response

### Major 1 — Industrial motivation is asserted but not built.

**Status:** `[LITERATURE-ONLY]` + `[TEXT-ONLY]`

**Evidence/Action.** We will expand the opening paragraph of the Introduction (`sections/introduction.tex`, l. 3) and add a "Metallurgical context" paragraph that explicitly cites and discusses:

- C. T. Sims, N. S. Stoloff, W. C. Hagel (eds.), *Superalloys II*, Wiley, 1987.
- R. C. Reed, *The Superalloys: Fundamentals and Applications*, Cambridge University Press, 2006.
- C. M. F. Rae, R. C. Reed, *Acta Mater.* **49**, 4113 (2001) — TCP precipitation in 2nd/3rd-generation single-crystal Ni-base superalloys.
- A. K. Sinha, *Prog. Mater. Sci.* **15**, 79 (1972) — geometry of Frank–Kasper phases.
- W. Hume-Rothery, *The Structures of Alloys of Iron*, Pergamon, 1966.
- L. R. Woodyatt, C. T. Sims, H. J. Beattie, *Trans. AIME* **236**, 519 (1966) — PHACOMP/Nv.
- M. Morinaga *et al.*, *Superalloys 1984*, p. 523 — New PHACOMP / $\bar{M}_d$.

Proposed replacement text (LaTeX, to be inserted after current first sentence):

> *"Topologically close-packed phases are a long-standing concern in the alloy-design community: their precipitation on grain boundaries in Ni-base single-crystal superalloys depletes the $\gamma'$-forming and solid-solution-strengthening elements (Re, W, Mo, Cr) and is widely identified as a creep-life-limiting mechanism in 2nd- and 3rd-generation blade alloys~\cite{rae_reed_2001,reed_superalloys}. The empirical PHACOMP, New PHACOMP and $\bar{M}_d$ frameworks used in industry to flag TCP-susceptible compositions~\cite{woodyatt_1966,morinaga_1984} rest on bond-counting or $d$-orbital energy heuristics; replacing them by physics-grounded ML predictions of TCP formation energies and finite-temperature site occupancies is the broader programme that this work contributes to."*

The Conclusions sentence about "multi-principal element alloys" (`conclusions.tex` l. 14) will be softened (see Major #6).

---

### Major 2 — Fe–Mo's own metallurgical relevance not stated.

**Status:** `[LITERATURE-ONLY]` + `[TEXT-ONLY]`

**Evidence/Action.** Add a new paragraph immediately after the metallurgical-context paragraph (Introduction). References to add:

- J.-O. Nilsson, *Mater. Sci. Technol.* **8**, 685 (1992) — super-duplex stainless steels, R-phase embrittlement.
- H. Sieurin, R. Sandström, *Mater. Sci. Eng. A* **444**, 271 (2007) — sigma in duplex.
- J.-M. Joubert, *Prog. Mater. Sci.* **53**, 528 (2008) — Fe–Mo sigma and R-phase review.
- J. Houserová, J. Vřešťál, M. Šob, *CALPHAD* **26**, 513 (2002) — Fe–Mo CALPHAD reassessment.

Proposed text (Introduction):

> *"The Fe--Mo system is not merely a structurally convenient testbed: its $\sigma$, $\mu$ and R phases precipitate in service in ferritic/martensitic 9--12\,Cr power-plant steels, in maraging steels, and in Mo-bearing austenitic and duplex/super-duplex stainless grades (e.g.\ 316L, 254\,SMO, SAF\,2507), where R-phase embrittlement is a documented failure mode~\cite{nilsson_1992,sieurin_2007,joubert_2008}. The training and validation phases selected in this work therefore correspond to industrially observed precipitates."*

---

### Major 3 — Crystallographic specification of CNAV is incomplete (Frank–Kasper mapping).

**Status:** `[ADDRESSABLE-FROM-DATA]`

**Evidence/Action.** The prototype structure file actually used by the pipeline, `PrototypeStructures/POSCAR_R_proto.vasp`, carries explicit Frank–Kasper labels in the per-atom comment column. Tallied from that file, the R-phase prototype is:

| FK polyhedron | Wyckoff labels (proto) | Atoms |
|---|---|---|
| Z12 (CN12 icosahedron) | Z12a, Z12b, Z12c, Z12d, Z12e, Z12f | 1+2+6+6+6+6 = 27 |
| Z14 | Z14a, Z14b | 6+6 = 12 |
| Z15 | Z15a | 6 |
| Z16 | Z16a, Z16b | 2+6 = 8 |
| **Total** | **11 distinct sites** | **53** |

(verified by `awk '/Z[0-9]/ {print $NF}' POSCAR_R_proto.vasp | sort | uniq -c`.) This 11-site, 53-atom decomposition matches the standard $R\bar{3}$ (hR53) setting of the R phase.

We will add a new Supplementary Table (Table~S3) listing, for each of R, M, P, $\delta$:
(i) the conventional Wyckoff label and multiplicity, (ii) the Frank–Kasper polyhedron class (Z12/Z14/Z15/Z16), and (iii) the CN group into which it falls under the 3.5 Å cutoff. Sources: `PrototypeStructures/POSCAR_{R,M,P,delta}_proto.vasp`.

We will also amend the Methods CNAV paragraph (`methods.tex` l. 41–46) to explicitly state:

> *"For each prototype structure the geometric coordination numbers obtained from a 3.5\,\AA{} first-shell cutoff coincide with the Frank--Kasper classification (CN12, 14, 15, 16) of all 11/14/12/14 Wyckoff sites of the R/$\delta$/P/M phases respectively (Supplementary Table~S3), so that the CNAV groups inherit the Frank--Kasper site hierarchy rather than averaging across it."*

Citations to add: F. C. Frank, J. S. Kasper, *Acta Cryst.* **11**, 184 (1958); **12**, 483 (1959).

---

### Major 4a — T = 1700 K is above the R-phase stability range.

**Status:** `[TEXT-ONLY]` + `[LITERATURE-ONLY]`

**Evidence/Action.** Confirmed: `15_A_Thermodynamics.ipynb` (cell 34) loops over a single temperature, `T = 1700 K`. The other temperatures (1000, 1250, 1500, 2000 K) are commented out. Per the assessed Fe–Mo diagram of Andersson, *CALPHAD* **12**, 1 (1988) and Houserová *et al.*, *CALPHAD* **26**, 513 (2002), the R phase in Fe–Mo decomposes below ~1488 K (Houserová) / ~1500 K (Andersson). T = 1700 K is therefore above the upper stability bound of R. Reviewer is correct.

A second observation: the preserved notebook output shows that the CEF optimisation at T = 1700 K already throws "Site fraction out of range" errors at several compositions for the R phase (notebook cell 34 output), consistent with the phase being metastable at that temperature in the assessed diagram.

Proposed action: down-shift the comparison temperature to **T = 1473 K**, the annealing temperature of the Joubert (1993) refinement, which lies inside the R-phase stability window of both assessments. Since the raw pipeline cannot be re-run, we cannot regenerate the occupancies at 1473 K. We will therefore (a) re-label Table II and Figure 5 as a comparison at the *annealing temperature implicit in the Joubert refinement*, (b) state explicitly that the present numbers were obtained at 1700 K which the Reviewer correctly identifies as outside the assessed R-phase field, (c) move the comparison to a *trend-level* statement rather than "quantitative", and (d) commit, in the response and revised text, to recomputing at 1473 K in a follow-up study with the restored compute environment.

Proposed replacement text (Methods, replace the sentence at `methods.tex` l. 87 "The temperature of 1700~K was chosen..."):

> *"The reference calculation was performed at T = 1700\,K, the temperature at which all studied TCP phases coexist in the assessed Fe--Mo diagram of Andersson~\cite{andersson_1988} for the purposes of comparing Gibbs-energy curves; we note, however, that this temperature lies above the upper stability bound of the R phase in the more recent assessment of Houserov\'{a} \emph{et al.}~\cite{houserova_2002} (T$^R_{\rm max} \approx 1488$\,K). The R-phase site-occupancy comparison with the Joubert refinement should therefore be read as a trend-level test of the ML-predicted end-member ordering, rather than as a strict equilibrium comparison at the experimental annealing temperature."*

References to add: J.-O. Andersson, *CALPHAD* **12**, 1 (1988); J. Houserová *et al.*, *CALPHAD* **26**, 513 (2002).

---

### Major 4b — Experimental uncertainty on Joubert site fractions; later refinements.

**Status:** `[TEXT-ONLY]` + `[LITERATURE-ONLY]`

**Evidence/Action.** The XRD uncertainties are not in our archive (the Joubert 1993 refinement reports $\sigma(y_{\rm Mo})$ per site in its Table 4; values are typically 0.02–0.05). We will:

- Add the per-site $\sigma(y_{\rm Mo})$ from Joubert 1993 to Table II as a fourth column (transcribed from the published paper).
- Reword Results (`results.tex` l. 118): change "*confirming quantitative agreement*" to "*lies within the experimental uncertainty of the Joubert refinement on all sites except the mixed Z14 site (formerly listed as 6c)*".
- Add comparison to later refinements: J.-M. Joubert, N. Dupin, *Intermetallics* **12**, 1373 (2004); J.-M. Joubert, *Prog. Mater. Sci.* **53**, 528 (2008).

---

### Major 5 — Wyckoff labelling of the R phase is non-standard / incomplete.

**Status:** `[ADDRESSABLE-FROM-DATA]` — **the manuscript is incorrect and must be fixed.**

**Evidence/Action.** Current manuscript Table II (`results.tex` l. 120–138) lists six sites for the R phase: **3a, 6c, 6f, 18h, 18i, 18j**. The multiplicities sum to 3+6+6+18+18+18 = **69 atoms**, which is *not* the 53-atom rhombohedral cell of the R phase.

The pipeline itself uses an 11-sublattice model. From `15_A_Thermodynamics.ipynb` (cell 6 and cell 7):

```python
lattice_names['R'] = ['$b$', '$c_1$', '$f_1$', '$f_2$', '$f_3$', '$f_4$',
                     '$f_5$', '$f_6$', '$f_7$', '$c_2$', '$f_8$']
multiplicities['R'] = [1, 2, 6, 6, 6, 6, 6, 6, 6, 2, 6]   # sums to 53
```

This matches the standard hR53 setting (Yakel, *Acta Cryst. B* **39**, 20 (1983); Joubert 2008) with one 3a (labelled `b` here), two 6c-type (`c_1`, `c_2`) and eight 18-fold positions condensed onto the rhombohedral primitive description. The mapping between the in-code labels and the standard Wyckoff labels (R$\bar{3}$, hexagonal setting) is:

| Code label | Mult. | Conventional Wyckoff (R$\bar{3}$, hex.) | FK class |
|---|---|---|---|
| $b$ | 1 (×3 in hex.) | 3a (or 3b) | Z16 |
| $c_1$, $c_2$ | 2 (×3 in hex.) | 6c | Z16/Z12 |
| $f_1\ldots f_8$ | 6 (×3 in hex.) | 18f / 18g / 18h | Z12/Z14/Z15 |

(definitive FK assignment per site: see Supplementary Table S3, derived from `POSCAR_R_proto.vasp`.)

**Proposed manuscript edit.** Replace Table II entirely. Use the 11-row form with labels `b, c1, c2, f1, …, f8` (or, equivalently, the hexagonal-setting Wyckoff labels 3a/6c×2/18f×8). The six numerical rows currently in the manuscript should be re-derived per-Wyckoff from the preserved per-site occupancy CSV (`Fe-Mo/results/OCCUPANCY_PREDICTION__R__T=1700__ACE__MAG=NM.csv`, referenced in cell 34 of the thermodynamics notebook). We will inspect that CSV and transcribe the 11 values verbatim; the rolled-up "6c, 18h…" rows in the current table were a presentation simplification that the Reviewer correctly flags as misleading.

Citation to add: H. L. Yakel, *Acta Cryst. B* **39**, 20 (1983).

---

### Major 6 — Transferability claim to Fe–W, Co–Mo, Ni–Cr–Mo is unsupported.

**Status:** `[REQUIRES-RECOMPUTE — BLOCKED]` → fall back to `[TEXT-ONLY]` softening.

**Evidence/Action.** A transfer test on Co–Mo or Fe–W would require re-running BOP/ACE descriptor computation and re-applying the trained model to external DFT structures. The pipeline and raw descriptor files for the present work are no longer executable. We therefore commit to *softening the claim* rather than supporting it with data in this revision:

- Remove the Fe–W / Co–Mo / Ni–Cr–Mo line from the Abstract and Conclusions.
- In Discussion ("Generality and limitations") replace the speculative sentence with:

> *"The methodology — BOP/ACE/SOAP descriptors with CNAV aggregation and a VotingRegressor ensemble — is in principle transferable to other transition-metal binaries that host Frank--Kasper phases, but we have not tested this here. A systematic transfer benchmark on Fe--W, Co--Mo and Ni--Cr--Mo using the Crivello/Joubert DFT databases~\cite{crivello_tcp,joubert_2008} is left as future work."*

---

### Major 7 — Tabulate end-member energies for CALPHAD ingestion.

**Status:** `[ADDRESSABLE-FROM-DATA]`

**Evidence/Action.** The preserved files
`Fe-Mo/results/PREDICTION__{R,M,P,delta}__ACE__MAG=NM.csv`
contain the ML-predicted end-member formation energies for the R, M, P, $\delta$ phases (verified from `15_A_Thermodynamics.ipynb` cell 13 and cell 14, which prints `end_members_BS['R']` with a `EF_nmhcp__ACE` column and 53-atom-cell indexing such as `Fe_pv53.R.NM`, `Fe_pv47Mo_sv6.R-AAAAAAAAAAB.NM`, …). Cell 28 confirms the analogous structure for $\delta$ (56 atoms, 14 sublattices, indexed `AAAAAAAAAAAAAA` etc.). These CSVs constitute exactly the per-end-member dataset the Reviewer asks for.

**Action:** add a Supplementary Table (S4) listing, for each of R, M, P, $\delta$:
- end-member label (string of A/B over the sublattices),
- $x_{\rm Fe}$,
- ML-predicted $E_f^{nmhcp}$ (meV/atom) — direct read-off from `EF_nmhcp__ACE` column,
and provide the CSV files as ancillary supplementary data in a CEF/TDB-ready format. We will state in Methods that these are intended for ingestion by CALPHAD assessors (Joubert/Dupin/Sundman framework: Lukas, Fries, Sundman, *Computational Thermodynamics*, CUP 2007).

---

### Minor 1 — "remarkable structural hierarchy".

**Status:** `[TEXT-ONLY]`

In `introduction.tex` l. 3, change "remarkable diversity of polymorphs" → "structurally rich set of polymorphs".

---

### Minor 2 — Cite Hall & Algie and Sinha for classical TCP review.

**Status:** `[LITERATURE-ONLY]`

Add to first paragraph of Introduction: E. O. Hall, S. H. Algie, *Metall. Rev.* **11**, 61 (1966); A. K. Sinha, *Prog. Mater. Sci.* **15**, 79 (1972).

---

### Minor 3 — "TCP phases are non-magnetic" needs qualification.

**Status:** `[TEXT-ONLY]`

`methods.tex` l. 25: change to:

> *"In the Fe--Mo system, the TCP phases of interest here ($\sigma$, $\mu$, R, M, P, $\delta$) are non-magnetic or vanishingly weakly magnetic at the compositions sampled, and the NM reference avoids spurious magnetic contributions that would otherwise dominate a ferromagnetic bcc Fe reference. We note that $\sigma$ in Fe--Cr and Fe--V is weakly ferromagnetic~\cite{cieslak_sigma}, so the same NM reference would not be appropriate without modification in those systems."*

---

### Minor 4 — Table I "Convergence" differences are within EOS noise.

**Status:** `[TEXT-ONLY]`

Move Table I in `methods.tex` to a Supplementary table; in the main text simply state that $\Gamma$-only and $2\times2\times2$ formation energies agree to within the EOS fit residual (≈1 meV/atom).

---

### Minor 5 — Figure 1 caption "filled vs open" is ambiguous.

**Status:** `[TEXT-ONLY]`

`results.tex` l. 13: tighten caption to: "Open symbols: 53 test structures. Filled symbols: 209 training structures." (already partly clear; emphasise the distinction).

---

### Minor 6 — Give XRD $\sigma(y_{\rm Mo})$ per site in Table II.

**Status:** `[LITERATURE-ONLY]` — covered with Major 4b.

Transcribe from Joubert 1993 Table 4.

---

### Minor 7 — Bibliography is too sparse.

**Status:** `[LITERATURE-ONLY]`

Add: Sims & Stoloff, Reed, Rae & Reed, Sinha, Hall & Algie, Frank & Kasper (both 1958 and 1959 papers), Yakel 1983, Nilsson 1992, Andersson 1988, Houserová 2002, Joubert 2008, Joubert & Dupin 2004, plus Hammerschmidt & Drautz on BOP for TCP: T. Hammerschmidt *et al.*, *Adv. Eng. Mater.* **10**, 1115 (2008); T. Hammerschmidt *et al.*, *Phys. Rev. B* **87**, 014203 (2013). Estimated bibliography size after revision: ~40–45 entries.

---

### Minor 8 — Define "complex TCP phase" operationally on first use.

**Status:** `[TEXT-ONLY]`

`introduction.tex` l. 3: append after first mention of complex TCP: "*(here defined operationally as TCP phases with $\geq$10 inequivalent Wyckoff sites: R 11 sites/53 atoms, M 11/52, P 12/56, $\delta$ 14/56)*".

---

### Minor 9 — Exact selected-feature counts in Table I.

**Status:** `[ADDRESSABLE-FROM-DATA]` (partial)

The per-fold selected-feature counts are recorded in the pipeline's model-selection notebook (`07_MachineLearn-ModelSelection.ipynb` / `08_AnalysisModels.ipynb`). We will inspect the preserved notebook outputs and replace the "~80, ~200, ~100" with median ± IQR over the 5 folds. If individual per-fold numbers are not in the preserved outputs we will report the final-fold counts and clearly label them as such.

---

### Minor 10 — Section ordering: Methods before Results for PRB.

**Status:** `[TEXT-ONLY]`

PRB Regular Articles indeed prefer Methods → Results. We will reorder `paper.tex` so the section sequence reads Introduction → Methods → Results → Discussion → Conclusions, reverting the npj legacy ordering.

---

## Summary table

| Status | Count |
|---|---|
| `[ADDRESSABLE-FROM-DATA]` | 4 (Major 3, 5, 7; Minor 9) |
| `[TEXT-ONLY]` | 7 (Major 1, 2, 4a, 6 fallback; Minor 1, 3, 4, 5, 8, 10 — overlapping) |
| `[LITERATURE-ONLY]` | 6 (Major 1, 2, 4b; Minor 2, 6, 7 — overlapping with TEXT-ONLY) |
| `[REQUIRES-RECOMPUTE — BLOCKED]` | 1 (Major 6 transfer test) |

Unique-comment count (17 numbered items): 16 addressable in this revision; 1 (Major 6 transfer test) blocked by data loss and will be acknowledged as future work.

---

## Concrete manuscript edits (ready to apply)

1. **`sections/introduction.tex`** — add two new paragraphs (metallurgical context + Fe–Mo industrial relevance); cite Sims, Reed, Rae & Reed, Sinha, Hall & Algie, PHACOMP/$\bar{M}_d$ literature, Nilsson, Sieurin & Sandström, Joubert 2008, Houserová 2002. Soften "remarkable" → "structurally rich". Add operational definition of "complex TCP phase". (Major 1, 2; Minor 1, 2, 8.)
2. **`sections/methods.tex`** — (a) Replace the "T = 1700 K … lies within the stability range of all studied TCP phases" sentence with the explicit caveat that 1700 K is above the assessed R-phase stability bound; cite Andersson 1988 and Houserová 2002. (b) Add Frank–Kasper / Wyckoff mapping sentence and reference Supplementary Table S3. (c) Qualify the "TCP phases are non-magnetic" sentence. (d) Move convergence Table I to Supplementary. (Major 3, 4a; Minor 3, 4.)
3. **`sections/results.tex`** — Replace Table II entirely with the 11-row, 53-atom R-phase decomposition (sites $b$, $c_1$, $c_2$, $f_1$–$f_8$ with multiplicities 1, 2, 6×6, 2, 6) using the values from the preserved `OCCUPANCY_PREDICTION__R__T=1700__ACE__MAG=NM.csv`; add a fourth column with Joubert 1993 $\sigma(y_{\rm Mo})$; change "quantitative agreement" to "within experimental uncertainty (except the mixed Z14 site)". (Major 4b, 5; Minor 6.)
4. **`sections/discussion.tex`** — Soften the Fe–W/Co–Mo/Ni–Cr–Mo transferability sentence to "left as future work"; cite Crivello/Joubert databases. (Major 6.)
5. **`sections/conclusions.tex`** — Remove "multi-principal element alloys" overreach; replace with a CALPHAD-deliverable framing pointing the reader to the end-member tables. (Major 1, 6, 7.)
6. **`paper.tex`** — Reorder sections to Introduction → Methods → Results → Discussion → Conclusions. (Minor 10.)
7. **New Supplementary materials:**
   - **Table S3:** Wyckoff ↔ Frank–Kasper ↔ CNAV-group mapping for R, M, P, $\delta$ (data: `PrototypeStructures/POSCAR_*_proto.vasp`).
   - **Table S4:** ML-predicted end-member energies (data: `Fe-Mo/results/PREDICTION__{R,M,P,delta}__ACE__MAG=NM.csv`).
   - **Ancillary CSV files** of the end-member energies in CEF/TDB-ingestible format.
   - **Table S5:** per-fold selected-feature counts (median ± IQR) from `07_MachineLearn-ModelSelection.ipynb` outputs.
8. **`paperNotes.bib` / `references.bib`** — add ~20 new entries (Frank, Kasper, Sinha, Hall & Algie, Yakel, Sims, Reed, Rae & Reed, Nilsson, Sieurin & Sandström, Andersson, Houserová, Joubert 2008, Joubert & Dupin 2004, Woodyatt, Morinaga, Hammerschmidt 2008, Hammerschmidt 2013, Lukas/Fries/Sundman, Cieślak).
