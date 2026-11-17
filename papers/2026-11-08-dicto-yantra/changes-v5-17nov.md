# #103 Version 5 draft: changes of 17 November 2026

Source: consolidation-ledger.md (the four #103 lines of 17 Nov) and the draft's status box (pending E1 wording).

1. Palomar (PALOMAR-2026-11-17-000006)
   - §10.1, new paragraph after Theorem 14 ("What Theorem 14 says"): the Lean 4 proof by a separate, kernel-checked route; exactly one admissible figure; slope in an interval of width 2^-21 holding Theorem 10's value; registered on Palomar [18].
   - §10.1, after the census: "The certificate is not yet checked in a proof assistant" became "This certificate is not itself checked …", plus "The statement of Theorem 14 is proved in Lean 4 by the separate route registered on Palomar [18]."
   - End of §10.2: Theorem 15 has no Lean proof yet (said so, since Theorem 14 now has one).
   - Table 5, Theorem 14 row: "the statement also proved in Lean 4 by a separate route (Palomar … [18])".
   - §13 Closed and exact: "(Theorem 14, computer-assisted, and proved in Lean 4 [18])".
   - Reference [18]: Palomar registry entry, 17 Nov 2026, with its URL. The repository commit is not cited: the paper does not link kulaichev-yantra-lean.
2. Headline point (DICTO, 17 Nov)
   - Abstract, second sentence: Kulaichev's own conditions force exactly one figure; it is not the traditional yantra (45 regions, 41 triangles + 4 four-sided, 28 sandhis; not 43 triangles and 24 sandhis); the DICTO Yantra is (Theorems 14 and 15).
   - Abstract: removed the later repeat "so no yantra meeting Kulaichev's conditions has the traditional 43 triangles and 24 sandhis".
   - §10.1, the same point in the new paragraph beside Theorem 14.
3. Why nine
   - New §10.3 "Why nine" (starts on a new page, so its heading does not sit alone at the foot of page 33): Proposition 16 (1) one removal order only, 3/5/7/9 triangles with 7, 16, 29, 43 odd regions (rings 6,1 / 12,3,1 / 14,7,7,1 / 14,10,10,8,1) on R1 and the DICTO Yantra; (2) the 7→9 step cannot be repeated (corner touch (2,6,6) puts the new base on t6's base line; 6 conditions for 4 unknowns), so nine is the largest member of the family grown by that step. Proof sketch; exact checks on R1 and Q3 (step_check.py, FINAL ok).
   - One paragraph: a 4-condition step (as 5→7) could repeat; at nine the counts are 43, 45 (three ring patterns), 47, 49 (1500 exact rational samples, computed); walls open.
   - Table 5: rows for Proposition 16 and the §10.3 counts. §13 Open: item (7). §14 New here: Proposition 16. Data and code: study 2026-11-17-yantra-sequence.
4. E1 sandhis (status-box wording, now applied)
   - Proposition 3: "except E1 (28)" became "except E1, which has 22 sandhis and two points where four sides meet (§9.6)".
   - Table 3, E1 row: sandhis 28 became "22 + two 4-line points"; caption notes the exact-edge count.
   - §9.6: "E1 keeps 43 regions and 18 marmas; it has 22 sandhis and two points where four sides meet (t4's leg through the corner touch (5,5,6), and its mirror image)".
   - Data and code: e1_sandhi.py (study 2026-11-12-yantra-regions-45).
   - Figure 11 (overlay-E1.png): red note "28 sandhis, not 24" became "on its edge 22 sandhis and two points where four sides meet, not 24 sandhis"; one line in studies/2026-11-08-sri-yantra/scripts/overlay.py, re-run on the compute host (FINAL ok); only overlay-E1.png copied into figures/.
5. Status box: new "Newest in this draft (17 November 2026)" list of items 1–4; the old pending E1 note is marked as applied.

At publication: update the data-link commit to one holding studies 2026-11-17-yantra-sequence (and the Figure 13 scripts); the Version 5 line names items 1–4.
