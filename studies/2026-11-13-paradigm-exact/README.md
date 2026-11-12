# The Permutohedron Paradigm: three gaps closed before release (13 Nov 2026)

**Conclusion (13 Nov 2026): all three gaps close. Theorem 4.1 is exact (DICTO's build read in rational coordinates; hull = chamfered
cube, build = Z less six cube pyramids), Theorems 5.3 and 5.4 are proved and certified exactly in Q(sqrt5), and the Chapter 9 Boulder
note is written from checked B1 results, with what is exact, numerical and open. No claim was downgraded.**

DICTO 13 Nov: books first; these gaps close before the book's release. Also done here for the book (DICTO's decisions of 13 Nov):
cover c (Figure 13.1, Plain Bob Minimus) rendered as the cover, and the Permutohedron Family retold as Chapter 14.

## Runs (compute machine, through the job gate)
| job | what | result |
|---|---|---|
| pexact-pilot | hemi_exact.py in full; scutoid_exact.py flip (pilot) | FINAL ok, 4.1 s + 5.5 s |
| pexact | hemi_exact.py; scutoid_exact.py all | FINAL ok, 4 s + 14 s (logs data/hemi-exact.log, data/scutoid-exact.log, data/pexact.log) |
| pcover (print machine) | cover/cover_svg.py, cover_shot.mjs, cover_title.py | FINAL ok on the second run (first run: a missing view-angle variable, fixed) |

`scripts/q5.py`: exact arithmetic in Q(sqrt5) (signs decided exactly), exact facets, volumes, separating-axis test for convex polytopes.

## 1. Chapter 4, Theorem 4.1 (scripts/hemi_exact.py) - EXACT
Input: DICTO's world export (data/dicto-build-worldpoly.json, copied from studies/2026-11-11-hemi-rd-build). Every stored quaternion
gives, to 4.4e-16, a rotation matrix with entries 0, +-1 (orthogonal, det 1, checked exactly); every position is a multiple of 1/10 to
5e-16. Read as these exact values (the export stores floats; the rounding is printed). Then, in rational arithmetic: one Hemi RD has 8
faces and volume 1; all 14 pieces volume 1; 91 pairs separated by exact planes; Z (generators e1, e2, e3 and four half diagonals) has 32
corners, 6 unit squares, 12 hexagons with squared sides 1, 3/4, 3/4, 1, 3/4, 3/4, volume 15; every build corner lies in Z + c,
c = (0, 1/5, 1/5), and every corner of Z + c is a build corner, so conv(build) = Z + c exactly; the six cube pyramids (volume 1/6) lie in
Z + c and are separated from all pieces and each other (99 pairs); 14 + 6/6 = 15 = vol Z, so pieces and pyramids fill Z + c.

## 2. Chapter 5, Theorems 5.3 and 5.4 (scripts/scutoid_exact.py) - PROVED + EXACT CERTIFICATE
Proof of 5.3 written in the chapter: the cell over a rhombus is its cone from the centre between PD and TK; side faces in mirror planes,
so flat; cones fill space, so the cells fill the shell; the group is transitive on rhombi, so congruent. Certificate (Q(sqrt5)):
TI, ID, TD with exact facets (closed surfaces, Euler 2); PD = TI°, RT = ID°, TK = TD° exact, bipolar checks; all 32 polar corners on
the 12 + 20 axes; 30 rhombi (5,3,5,3); PD folds abd, bcd and TK folds abc, acd over every rhombus; every side plane maps the 32 axes to
themselves (a mirror); PD (five-fold radius 1) < TK (1.55) < PD x 155/86 strictly; 120 side faces coplanar with the centre; 30 equal
volumes, one distance multiset, adding to V(TK) - V(PD) (6.4660211935 at radius 1, = the source study's float value); the back shell
likewise; the two flip cells differ.
Proof of 5.4 in the chapter (move and flip are involutions, the square closes through the polars; nested K0 < K1 < lam K0 give onions
filling space but the centre). Certificate: shells S (TI 1 -> ID 1.18 -> TD 1.42, circumradii to six digits) and A (TD -> ID 1.499 ->
TI x 71/45): every half-cell = conv of its two end faces, with facets exactly the construction's faces (flat); each shrunk edge reopens
across; 2016 pairs per shell separated by exact planes; all inside the outer solid and outside the core; volumes add exactly to the shell
(S: 689.7413293355 = 5.6660707968 x R0^3 in the standard scale, the source study's value); TI < TD < TI x 71/45 strictly; four shapes.
Limit (stated in the chapter): the filling of the scutoid shells is certified at these radii; at other radii only flatness is proved.

## 3. Chapter 9: the Boulder note (Section 9.3) - WRITTEN
"The Boulder" = B1 of the gap triage, "walls along the sliders, exactly" (#86, #80/#81, #61). Results found in
studies/2026-11-09-b1-walls/README.md and its logs; the #80/#81 exact chain logs were on the compute machine only and are now kept in
data/b1-logs/ (windows/c-14o25.txt, d-3o4.txt, d-29o20.txt: FINAL ok; b1-cube-exact.log: FINAL ok; b1-edge81.log: numerical edge s*;
b1-windows.log ends FINAL FAIL only because two slow runs were stopped by design, d-13o10 and d-21o20). Status in the note:
#86 exact; #61 = Theorem 9.1; #80 exact on (1/2, 3/5) and (3/4, 1), window numerical; #81 exact on [2/5, 1] and [3 - phi, 3/2], the
(5/4, 3 - phi) closure and s* = 1.08734394 +- 4e-8 numerical, exact form of s* open.

## 4. Cover c and Chapter 14
- cover/: cover_svg.py re-draws Figure 13.1 with the chapter's own drawing code (figs.py of studies/2026-11-12-change-ringing, executed
  from its file) on a 1000 px square; cover_shot.mjs rasterises it at 2.4x (2400 px, vector edges, no blur); cover_title.py adds the
  house title panel (DSEG14 letters as on the other book covers, gold title, red DICTO). Output paradigm-cover-front.png (2400 x 3348).
- Chapter 14 (papers/paradigm-ch14) retold from the Permutohedron Family draft: the family and its cone, Theorem 14.1 (the line to the
  associahedron), Proposition 14.2 (ABHY reproduced), Theorem 14.3 (equal-edged members), the 13-COA and its Vacuus, Proposition 14.4
  (Fedorov's five). Prior art from studies/2026-11-12-permutohedron-equal-edges/PRIOR-ART.md: the 13-COA is the augmented
  cuboctahedron (Stewart 1970), named by DICTO for its role as an atom; 339 H3 atoms new as far as the sources checked show.
