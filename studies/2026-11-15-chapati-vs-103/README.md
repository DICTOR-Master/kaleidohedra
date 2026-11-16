# Chapati & Chapati 2026 compared with #103 The DICTO Yantra (2026-11-15)

**Verdict.** Chapati & Chapati's report is earlier (Zenodo, 6 October 2026) than #103 v1 (8 November 2026), but it is numerical and computational: none of #103's exact results (Theorems 1, 2, 5, 6, 7, 9, 10, Propositions 4, 8, 11–13, the yantras on solids and on spheres) is in it. The one overlapping result is the count of the 43. Both papers get 14, 10, 10, 8, 1 by different rules: Chapati count star points of the circuit outlines, #103 Proposition 3 counts the regions inside an odd number of triangles. #103 v4 already credits them for this and for the sampling. **Two disagreements matter for Version 5.** (1) The two rules **part on Kulaichev's yantra**: there Chapati's own enumerator returns 43 and the odd-region rule returns 45. So #103 v4's sentence "both rules pick out the same 43" holds only for yantras with the traditional pattern. (2) Chapati's split of the 74 regions into "50 triangles, 24 trapezoids" counts the points where a line ends on a side as corners. Counting real corners gives **53 triangles and 21 four-sided regions**, with all 43 odd regions triangles, as #103 certifies. A third point is a difference of claim, not of numbers: Chapati say the system has "no closed-form solution", while #103 Theorem 1 makes the closing step one quadratic in an explicit field, and Theorems 9 and 10 give exact algebraic slopes. #103 v4 already says this. **Palomar:** the #103 candidates (Theorem 2 R1, Theorem 1, Theorem 5 with β* = −y_H) are untouched and still new as far as the sources go.

**Status:** report read in full (45 pp, every page, including Appendices A–C); code zip downloaded (MIT); four yantras checked with Chapati's own enumerator (FINAL ok). This is not a reproduction of Chapati's report. Only the items named below were checked. Their machine-learning, generative, spectral and export results were read but not rerun.

## 1. Dates

| record | Zenodo id | created (UTC) | publication date | notes |
|---|---|---|---|---|
| G. D. Chapati, R. Chapati, *Verified Reconstruction of the Śrī Yantra* | 23188650 (concept 23188649) | 2026-10-06 13:16 | 2026-10-06 | single version "1.0"; PDF title page says "September 2026"; licence CC BY 4.0, code MIT |
| #103 v1 *The DICTO Yantra: Exact Śrī Yantras, a Rational One, and a Perfect Yantra on the …* | 24052634 (concept 24052633) | 2026-11-08 11:26 | 2026-11-08 | |
| #103 v2 / v3 / v4 | 24061031 / 24092662 / 24094699 | 11-08 21:04 / 11-09 20:32 / 11-09 23:38 | 11-09 / 11-10 / 11-10 | v4 adds the credit to Chapati [13] (found through forward citations of Chiodo 2021) |

Sources: the Zenodo API (`/api/records/<id>` and `/versions`), read 15 November 2026; `papers/2026-11-08-dicto-yantra/zenodo-state.json` (id 24094699, version 4 on Zenodo, concept 24052633). Chapati were first, by 33 days. #103 v1 did not know of them. The v4 credit says that the report was "read §1–2 and the closing gate". This study reads all of it.

## 2. Overlap, claim by claim

### #103's results against Chapati

| #103 | in Chapati? | relation |
|---|---|---|
| Model and conditions (i)–(iii): 18 marmas, 6 corner touches, 7 apex-on-base, both great triangles inscribed (after Chiodo 2021 / Huet 2002) | Huet's 31-step construction with 5 starting values and one closing condition, from Huet's paper and his PostScript `Shri.ps` | **same family, different coordinates.** Both stand on Huet. The coordinates agree: Huet's classical inputs in Chapati's code give #103's P, Q, R, S = 0.332, 0.537, 0.602, 0.836, and the kite angles 78.23° and 70.37° of #103 Table 2. Mapped into Chapati's code, #103's DICTO Yantra and Kulaichev's yantra close to 1.5·10⁻¹⁶ and 0 (log). |
| Theorem 1 (every rational choice of u, v, Q, S: all meetings in one quadratic field; admissibility conditions) | no. Chapati solve the closing condition by a numerical root-find and state "no closed-form solution" | **different; Chapati's claim is answered by Theorem 1** (and by Chiodo 2021's constructibility) |
| Theorem 1, admissible region "open"; v4 credits their sampling | 5,000 sampled parameter sets in boxes around Huet's classical point; 24.3% valid; failures: 58.9% close but leave the circle, 11.8% do not close, 5.0% wrong count | **complementary.** Their validity is "closes + every point in the circle + 43 star-point chambers", near #103's admissibility. It is a sample, not a description. |
| Theorem 2 (R1 in whole-number fractions) | no | new in #103 |
| Proposition 3 (the 43 are the odd regions; 14, 10, 10, 8, 1) | **yes, by another rule**: star points, one per convex corner of the āvaraṇa outlines (8, 10, 10, 14, with the trikoṇa); checked at four parameter sets | **same count on traditional-pattern yantras, different method; they differ on the 45-region yantras** (§3) |
| 74 regions of the arrangement (#103: "75 regions with Euler characteristic 2", the outer face included) | "74 regions (50 triangles, 24 trapezoids)" | **total agrees** (74 bounded faces). The split conflicts (§3). |
| Proposition 4, Theorem 5 (viewpoint, β* = −y_H), Theorem 6, Theorem 7, Proposition 8 | no | new in #103 |
| Theorems 9, 10, Proposition 11 (certified counts), Proposition 12 (Rh345), Proposition 13 (u*), §9 yantras, §11 spheres, §12 the choice | no (Chapati do not treat Kulaichev's yantra, extra conditions, rigid yantras or exact forms) | new in #103 |
| Traditional numbers: 18 marmas, 24 sandhis | quote a devotional source: "24 sandhis … and 28 marma-sthānas, points where three lines meet", used "as a hint, not as proof"; not computed | 24 agrees. 28 is not a result of theirs, so it is no conflict. Under #103's conventions there are 18 three-line points off the corners, or 31 with the 6 corner touches and the 7 apex-on-base points. 28 is neither. |

### Chapati's results not in #103

1. The feasibility benchmark (5,000 sets, seed 20260908), the failure-mode table, and the measurement of Huet's "very shallow range".
2. Classifiers (k-NN AUC 0.9574, MLP 0.9754, the F1 gain at the widest stratum), the negative ablation and the learning curve.
3. A generator of valid parameter sets (classifier rejection, 83.4% valid against 15.1% for uniform sampling).
4. The Dirichlet spectrum of the 43 regions by finite elements (λ₁ = 1213.3), the finding that each mode stays inside one region "because the 43 chambers meet one another only at vertices", and the TM cutoffs.
5. Exports (DXF, HFSS/CST scripts, ONNX, C).
6. The source work: the free URL of Huet's paper (`gallium.inria.fr/~huet/PUBLIC/Nivat.pdf`) and the nine triangle definitions from Huet's `Shri.ps`, which #103 v1–v4 could not reach. Also Huet's remark, as they report it, that Bhāskararāya's inside-out instructions place J and Q on the circle only by luck.

Item 4 follows from #103's Proposition 3. Crossing any side changes the number of containing triangles by exactly one. So two odd regions never share a side: they meet only at corners.

## 3. Conflicts, checked

Check: `scripts/cross.py` runs Chapati's own `huet_build.py`, `gate1_complete.py`, `faces.py` and `geometry.py` (MIT, from their Zenodo zip, imported unchanged and not copied here) on four yantras. #103's yantras are mapped into Huet's five parameters: YQ = 1 − b3, YJ = 1 − b7, YP = 1 − b6, XF = t1's leg at depth b3, XA = t3's leg at depth b8. The mapping is checked by rebuilding: |YL − (1 − b9)| ≤ 4·10⁻¹⁶. Log: `data/cross-log.txt`, FINAL ok (a pilot of under 5 minutes on the compute machine).

| yantra | bounded faces | split, Chapati's simplify | split, real corners (turn > 10⁻⁶ rad) | odd regions (#103 rule) | star-point rule (Chapati) |
|---|---|---|---|---|---|
| Huet classical, Chapati's Gate-1 point (YP 0.4627) | 74 | 50 tri + 24 quad | **53 tri + 21 quad** | 43 (14, 10, 10, 8, 1), all triangles | 43 |
| Huet classical (YP 0.463) | 74 | 48 + 26 | 53 + 21 | 43, all triangles | 43 |
| DICTO Yantra (GF1) | 74 | 49 + 25 | 53 + 21 | 43, all triangles (= #103 certified) | 43 |
| Kulaichev–Rao–Pustynski | 78 | 49 + 28 + 1 other | 53 + 25 | **45 (14, 10, 12, 8, 1), 41 triangles + 4 four-sided** (= #103 certified) | **43** |

**Conflict 1: the two rules for the 43 part on Kulaichev's yantra.** On every traditional-pattern yantra tried, both rules give 43. On Kulaichev's yantra, Chapati's enumerator still finds all 8 + 10 + 10 + 14 tips plus the trikoṇa, so 43. The odd regions number 45, and only 41 of them are triangles (#103 Proposition 11, certified, and this run). The star-point rule does not see Pustynski's two tiny triangles or the four regions that lose their tips. Chapati's validity label would therefore call Kulaichev's yantra a valid 43-chamber yantra. Chapati never evaluated that yantra, so this is not a claim of theirs that is wrong. It does make #103 v4's sentence "both rules pick out the same 43" too broad.

**Conflict 2: 50 triangles and 24 trapezoids against 53 and 21.** Chapati's §2.1 counts the vertex where a line only ends on another side (a T-junction, at the corner touches and apex-on-base points) as a corner. Their own §13.1 found three such vertices "collinear to 3·10⁻⁹" in the 43 and removed them from the export. Counting real corners, the 74 regions at their own Gate-1 point are 53 triangles and 21 four-sided regions. #103 does not state this split, so #103 is not affected. Version 5 may state it if it mentions Chapati's 74.

**Not a conflict, a difference of claim:** "no closed-form solution" (Chapati, abstract and §1). In Chiodo's coordinates the closing step is one quadratic (#103 Theorem 1; Chiodo 2021's Apollonius step). The rigid yantras have exact minimal polynomials (Theorems 9, 10). #103 v4 §14 already says so.

**Minor, outside #103:** Chapati attribute their differences from Huet's printed values (up to 0.0011 for YL and YV) "entirely" to Huet's three-decimal rounding. That is larger than a half-unit of the third decimal, though rounded inputs can carry it. This was not checked further, and nothing in #103 depends on it.

**Agreements checked:** Huet's classical inputs give #103's P, Q, R, S and Table 2 angles. The 74 bounded faces agree (#103's 75 includes the outer face). The ring counts 14, 10, 10, 8, 1 agree. Their reproduced YQ = 0.667907682971 is reproduced by their code.

## 4. Credit sentences for #103's next version

To be placed where each result is used. All are drafts for DICTO's read. #103 itself is not edited here.

1. **§2, after Proposition 3** (it replaces v4's last clause "both rules pick out the same 43"):
   > The same five circuits and counts were found earlier by Chapati and Chapati [13] (6 October 2026) by a different rule: the 43 are the star points, one per convex corner of each āvaraṇa outline (8, 10, 10 and 14, with the trikoṇa), each tip capping one region; they verified it at four points of the family. On every yantra with the traditional pattern the two rules pick out the same 43 (checked with Chapati and Chapati's own enumerator, MIT licence, on Huet's classical yantra and the DICTO Yantra). They part on Kulaichev's yantra: every tip still caps a region, so the star-point rule returns 43, while the odd regions number 45 (14, 10, 12, 8, 1), 41 of them triangles. The parity rule sees Pustynski's two tiny triangles; the star-point rule does not.
2. **§2 or §10, where the full arrangement is counted** (after "The result is 75 regions with Euler characteristic 2"):
   > that is, 74 bounded regions and the outer one. Chapati and Chapati [13] also count 74 at Huet's classical yantra; their split, 50 triangles and 24 four-sided, counts as a corner the point where a line ends on a side, and with true corners it is 53 triangles and 21 four-sided, the 43 odd regions all triangles.
3. **§2, after Proposition 3** (new):
   > Chapati and Chapati [13] observed that the 43 regions meet one another only at corners, never along a side, so that each Dirichlet mode of the figure stays inside one region. Proposition 3 explains why: crossing a side changes the number of containing triangles by one, so two odd regions never share a side.
4. **§14, Known, credited** (it replaces v4's Chapati sentence):
   > Chapati and Chapati (2026) [13] reconstructed Huet's construction numerically (residual 1.9·10⁻¹⁴) from Huet's paper and his PostScript drawing, counted the 43 as the star points of the five circuits, sampled 5,000 parameter sets around Huet's classical yantra (24.3% valid; most failures close but leave the circle), trained classifiers and a generator of valid parameter sets, and computed the Dirichlet spectrum of the 43 regions by finite elements; none of the last four is in this paper. They state that the system has no closed-form solution; in Chiodo's coordinates its closing step is one quadratic (Theorem 1), and the rigid yantras have exact algebraic slopes (Theorems 9 and 10).
5. **§14, Sources checked** (it replaces v4's last clause):
   > … G. D. Chapati and R. Chapati, Zenodo 2026 (doi:10.5281/zenodo.23188650; the 45-page report read in full on 15 November 2026, and its code, MIT licence, run on four yantras).
6. **Only if Version 5 reads Huet in full:** (Update 16 November 2026: Huet's author version has now been read, pp. 2–3 checked, study 2026-11-16-palomar-yantra; this item can go ahead.)
   > Huet's paper, not reachable for Version 1, is freely available (gallium.inria.fr/~huet/PUBLIC/Nivat.pdf), with his PostScript drawing Shri.ps; we owe both links to Chapati and Chapati [13].
   Then the "(full text not reachable)" notes in §14 change.

DICTO's results stay as they are. Proposition 3 (the parity rule) remains DICTO's. Chapati's earlier star-point rule is credited beside it, as both are independent works.

## 5. Palomar (studies/2026-11-14-lean-loop-equality, candidates C and C′)

**Still new, as far as the sources go.** Chapati have no exact field, no rational yantra and no viewpoint map: Theorem 2 (R1), Theorem 1 and Theorem 5 with uniqueness β* = −y_H are not in their report. Their statement that the system has "no closed-form solution" is, if anything, a recent statement that Theorem 1 answers. Theorem 1's novelty still rests on its explicit field, beside Chiodo 2021's constructibility, which must be credited. For any entry, add Chapati & Chapati 2026 to the literature-search record as related work: numerical reconstruction, star-point count, sampling. Do not cite it as prior art for the candidate statements. A Lean entry built on Proposition 3 would need the star-point rule credited and the Kulaichev difference stated, but Proposition 3 is not a listed candidate.

## Files

- `scripts/cross.py`: the check. Usage: `python3 -I cross.py <Chapati src dir> <folder holding studies/2026-11-08-sri-yantra/{figures/golden_family.json,data/kulaichev-numeric-data.txt}>`.
- `data/cross-log.txt`: its output (FINAL ok).
- Not stored here: Chapati's PDF (in DICTO's reference library) and code (Zenodo 23188650, MIT).
