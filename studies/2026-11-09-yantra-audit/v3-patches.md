# Version 3 patch list for paper #103, *The DICTO Yantra: Two Exact Solutions*

These texts are prepared for a Version 3 draft. **None of them has been applied** to paper.html or to the published PDF.
Each patch gives the place, the current text (copied from Version 2), and the replacement. The evidence for the new wording
is in AUDIT_REPORT.md and certificates/.

---

## Patch 1 (task 4): Theorem 1, with its admissibility conditions

**Place.** §2, the statement of Theorem 1, and one sentence after its proof.

**Current.**
> Theorem 1 (the quadratic family). If u, v, Q and S are rational, every corner and every meeting point of the yantra lies in one quadratic field ℚ(√Δ), and all 18 marmas, the 6 corner touches, the 7 apex-on-base points and both inscribed triangles hold exactly. Here Δ(u, v, Q, S) is the discriminant of the construction's closing quadratic; its square-free part has degrees 10, 20, 6, 6 in u, v, Q, S.

**Replacement.**
> Theorem 1 (the quadratic family). Let u, v, Q and S be rational, and let the construction be defined at them: every divisor met along it is nonzero (among them S − P, R − P, Q − P, the leading coefficient of the closing quadratic, and the divisors that follow from b1, such as R − b1 and b8 − Q). Then every corner and every meeting point of the yantra lies in one quadratic field ℚ(√Δ), and all 18 marmas, the 6 corner touches, the 7 apex-on-base points and both inscribed triangles hold exactly. Here Δ(u, v, Q, S) is the discriminant of the closing quadratic; its square-free part has degrees 10, 20, 6, 6 in u, v, Q, S. The figure is real when Δ ≥ 0. It is a Śrī Yantra (admissible) when, in addition, the bases are strictly ordered (b1 < b2 < … < b9), every half-width is positive, every apex lies on the correct side of its base (below it for t1–t5, above it for t6–t9), and every corner lies in the closed disc.

**Add after the proof.**
> The algebraic part of the theorem is one identity. For symbolic u, v, Q, S and b1, every one of the 31 conditions (18 marmas, 6 corner touches, 7 apex-on-base points), together with both inscribed triangles, is either identically zero in the model or a multiple of the closing polynomial. Only the marma (1,4,6) needs the closing equation. This was checked in two computer algebra systems (Singular via Sage, and sympy). Admissibility is a set of strict inequalities, so it holds on an open region of the parameters. Each example in Table 1 was tested against it. A description of the whole admissible region is open.

Note for the draft: the identity covers exactly the generic statement (audit stage 2, case G). The inequality list is the one in model.py's `order_ok`, read with the corners of t3 and t7 exactly on the circle.

---

## Patch 2 (task 5): Proposition 8's heading

**Place.** §8.

**Current.**
> Proposition 8 (no parent solid). (1) No two corners of a Platonic solid …

**Replacement.**
> Proposition 8 (no parent solid among the tested families). (1) No two corners of a Platonic solid …

The rest of the statement and the proof stay as they are. The open items stay as they are and are named once more at the end of the proof:
> Not covered: regular polygons with many sides (angles a rational fraction of a turn) were not searched, and the irrationality of u² for PF2 is not proved (findpoly finds no integer polynomial of degree ≤ 8; this supports it but does not prove it). So (2) is conditional on that irrationality.

In §13 "Open", item (5) stays. Add: "(6) Proposition 8 beyond the tested families: many-sided regular polygons."

---

## Patch 3 (task 6): the proof-status table

**Place.** New table at the start of §13 ("What is closed, what is computed, what is open"), before "Closed and exact".

> Table 4. How each result is established.
>
> | Status | Meaning |
> |---|---|
> | Exact symbolic | proved by algebraic identities (by hand or by computer algebra on symbols) |
> | Exact rational | proved with rational (or exact number-field) arithmetic on specific numbers |
> | Certified algebraic | exact polynomial, with certificates of irreducibility, of real-root isolation and that the geometric solution is the isolated root |
> | Certified computation | a finite combinatorial count in which every sign is certified by interval arithmetic and every zero is proved exactly |
> | High-precision numerical | verified to a stated tolerance; exact form not known |
> | Computational search | established within a stated finite domain |
>
> | Result | Status |
> |---|---|
> | Theorem 1 (quadratic family) | exact symbolic (generic identity, two systems); examples exact in ℚ(√Δ) |
> | Theorem 2 (R1 in fractions) | exact rational (two independent scripts) |
> | Proposition 3 (the 43 are the odd pieces) | certified computation for the DICTO Yantra (43 = 14 + 10 + 10 + 8 + 1, 18 marmas, 24 sandhis); for the other listed yantras a computation on stored 40–60-digit values (figure.py, counts.py), not certified |
> | Proposition 4 (three dimensions) | exact symbolic |
> | Theorem 5 (viewpoint) | exact symbolic |
> | Theorem 6 (natural coordinates) | exact symbolic (G, Q and H in full: Appendix H) |
> | Theorem 7 (one slope) | exact symbolic (linear algebra) |
> | Proposition 8 (1) | computational search (the listed solids and polytopes) |
> | Proposition 8 (2) | exact, conditional on u² irrational for PF2 (open) |
> | §3, Rh345 | exact in a number field of degree 20 (rhombus345_exact.py; not re-audited) |
> | Theorem 9 (DICTO Yantra, degree 160) | certified algebraic |
> | Theorem 10 (Kulaichev's yantra, degree 348) | certified algebraic |
> | Proposition 11 (45 vs 43; 28 vs 24 sandhis) | certified computation for both yantras; degrees certified (Theorems 9, 10) |
> | Table 3, other yantras (K1–K4, V1, PF1, PF2, G1, E1, rhombus yantras) | high-precision numerical (10⁻⁵⁰ at 60 digits) |
> | §9.5 rule for the extra pieces | open |
> | §11 spheres (gnomonic projection keeps every meeting) | exact symbolic; caps and figures computed |

Note for the draft: R1's coordinates are exact fractions, so its count could be certified by the same script fed with point intervals; this audit ran certified_counts.py for the DICTO Yantra and Kulaichev's yantra only.

---

## Patch 4 (task 1 outcome): the proofs of Theorems 9 and 10

**Place.** §10, after each "Proof (computation)" paragraph. Add:

> Certificate. (i) f160 is irreducible over ℚ: modulo 43 it stays irreducible. Two further systems confirm it (PARI polisirreducible; FLINT/NTL via Sage). Its even part g(y) = f160(√y) is irreducible as well (modulo 43, of degree 80). Over ℚ(√5), g splits into two conjugate factors of degree 40 (PARI nffactor; the product was checked exactly in sympy). (ii) The interval [6793185887067746573886503103907545526887, 6793185887067746573886503103907545526888]·10⁻⁴⁰ contains exactly one real root u0 of f160 (PARI polsturm, and an independent Descartes count). (iii) Interval Newton (the Krawczyk test, at 520 digits) proves that the system "(c), closing equation, (d)" in natural coordinates, with uv = 2/φ³, has exactly one solution in a box of radius 10⁻⁴⁸⁰ around the numerical yantra, and encloses it to width 6·10⁻⁴⁹⁸. (iv) At that solution the two resultants vanish. Every factor that the elimination drops is shown to be nonzero there by interval arithmetic. Every factor of the last resultant other than f160 has no real root in the interval of (ii) (exact Sturm counts). So f160(u) = 0 at the exact yantra, and its u is u0. (v) From that solution the whole yantra is rebuilt in interval arithmetic. Every division in the construction has a nonzero divisor; the closing equation, (b), (c) and (d) hold exactly, and with them all of Huet's conditions (Theorem 1's identity); the yantra is admissible, with strict inequalities. The elimination was also recomputed by a second route (Singular resultants, 1 minute instead of 66), which gives the same factor degrees 1^1600, 160, 160, 320.

For Theorem 10, the same certificate applies, with these changes: f348 is irreducible by its factorisation patterns modulo 7, 11, 13 and 19; the isolating interval is [7504385160222140244060846570512345103408, …409]·10⁻⁴⁰; the solution is enclosed to width 1.2·10⁻⁵³⁴; and the new elimination (18 s, natural coordinates with v = u) gives a resultant of degree 1744 whose factors are u (1^178), two other linear factors (1^274, 1^178), a quadratic (2^185), f348 and one factor of degree 396. This is an independent rederivation of f348 by a different route than kulaichev_exact.py.

---

## Patch 5 (task 2 outcome): Propositions 3 and 11, the counts certified

**Place.** The "Check." paragraphs after Proposition 3 and Proposition 11. Add:

> For the DICTO Yantra and Kulaichev's yantra the count is certified (certified_counts.py). The arrangement of the 27 sides is built from the exact solutions of Theorems 9 and 10, enclosed to about 500 digits. Every one of its decisions comes down to one question: do three of the 27 lines pass through one point? Each answer is either certified nonzero by interval arithmetic or proved exactly zero as an identity of the model. For the DICTO Yantra, 31 concurrencies and 36 parallel pairs are exact, and 5 909 other signs are certified; the smallest certified value is 5.2·10⁻⁶ (a near-concurrency of t6's and t8's left legs with t5's right leg). The result is 75 faces with Euler characteristic 2, and 43 odd faces (14, 10, 10, 8, 1), all 43 of them triangles, with 18 marmas and 24 sandhis. For Kulaichev's yantra, 31 concurrencies and 38 parallel pairs are exact (the extra 2 pairs are the opposite sides of the rhombus, u = v), and 5 965 signs are certified; the smallest is 5.8·10⁻⁸ (the doubled area of one of the two tiny pieces). The result is 45 odd faces (14, 10, 12, 8, 1), 41 of them triangles, with 18 marmas and 28 sandhis.

(The "41 of them triangles" sharpens the Version 2 sentence "their third ring holds 12 pieces, not all of them triangles": exactly four of the 45 odd pieces are not triangles.)

---

## Patch 6: Appendix H

**Place.** New appendix after §14 (or as a supplementary file next to the two polynomial files). Its text is appendix_H.md of this audit: G, Q(t), the trivial factors and the full relation H, 43 coefficients cᵢⱼ(u, v) in factored form, plus the one-line machine-readable form.

In Theorem 6's proof add: "The full relation H is given in Appendix H."

---

## Patch 7 (house rule, 9 Nov 2026): authorship wording and credits

DICTO is the author, so the running "DICTO proposed X" sentences become direct statements of X. The credits list becomes two lines. DICTO's names stay (DICTO Yantra, Cleo-Antonius, Cleo-Octangula, Cleo-Icos, Antonius, Julias, DICTO's rhombus). Explicit credit to other people stays (Huet, Chiodo, Kulaichev, Rao, Pustynski, Kavi Mahesh, Tripathi, Gonçalves–Mádr–Stříž, Kaivalyāśrama, Matos, Euclid, Hypsicles, Aristotle, Ennin).

**7a. Credits section.** Replace the whole paragraph under "Credits" (from "DICTO proposed the upright rhombus; …" to "… Computation and drafting with Claude (Anthropic).") by:

> DICTO: ideas, names, constructions and direction.
> Computation, verification and drafting with Claude (Anthropic).

The reference images are credit to another person, so keep that sentence and move it to §1 "Reference images", which already describes them: "H. J. T. Matos's painted yantra (2023, CC BY-SA 4.0), used as a reference only and not reproduced."

**7b. Byline note** (under the author line). Current: "The rhombus, the solids, the viewpoint, the Cleo-Antonius and the names are DICTO's. Computation and drafting with Claude (Anthropic)."
Replacement: the same two lines as 7a.

**7c. Running text.** Each sentence below is replaced as shown. The rest of each paragraph is unchanged.

| § | Current | Replacement |
|---|---|---|
| hook | "…and yantras built on solids that DICTO proposed, and it ends…" | "…and yantras built on solids, and it ends…" |
| Fig. 1 | "…Hypsicles' Book XIV, and DICTO proposed it as the pyramid Aristotle meant in On the Heavens (#44); Antonius is DICTO's space-filling partner for it (#44)." | "…Hypsicles' Book XIV, and the pyramid Aristotle meant in On the Heavens (#44); Antonius is its space-filling partner (#44)." |
| §1 | "Later DICTO compared the exact yantras with H. J. T. Matos's painted yantra (2023, CC BY-SA 4.0), used as a reference only and not reproduced here." | "The exact yantras are also compared with H. J. T. Matos's painted yantra (2023, CC BY-SA 4.0), used as a reference only and not reproduced here." |
| §3 | "DICTO proposed the upright rhombus: the two legs of t7 (from O) and the two legs of t3 (from T), the four longest lines of the yantra, meet at E± = …" | "The upright rhombus: the two legs of t7 (from O) and the two legs of t3 (from T), the four longest lines of the yantra, meet at E± = …" |
| Fig. 4 | "Left: Rh345, DICTO's rhombus made the 3-4-5 rhombus (DICTO proposed it; slope exactly 3/4, exact in a field of degree 20)." | "Left: Rh345, DICTO's rhombus made the 3-4-5 rhombus (slope exactly 3/4, exact in a field of degree 20)." |
| §4 | "DICTO proposed the triangles as tetrahedra in a sphere, the stella octangula as the rhombus's solid, and spinning tetrahedra." | "The triangles become tetrahedra in a sphere, the stella octangula is the rhombus's solid, and the tetrahedra can spin." |
| §5 | "DICTO proposed the viewpoint: a change of perspective that makes one yantra meet every demand." | "The viewpoint: a change of perspective that makes one yantra meet every demand." |
| §6 | "DICTO proposed a simpler formula. Let t1's corner be …" | "A simpler formula: let t1's corner be …" |
| §7 | "DICTO proposed the triangular grid, after the Matos painting, and then the Cleo grid: all nine triangles similar, …" | "The triangular grid, after the Matos painting, and the Cleo grid: all nine triangles similar, …" |
| §8 | "DICTO chose the stella: keep the stella's tetrahedron exact below (v = 1/√2) and free the upper slope." | "Here the stella is kept: its tetrahedron stays exact below (v = 1/√2) and the upper slope is free." |
| §9.1 | "DICTO proposed a side of Antonius in place of the stella. Antonius (D65, …)" | "A side of Antonius takes the place of the stella. Antonius (D65, …)" |
| §9.1 | "DICTO named the pair the Cleo-Antonius: the Cleo-Icos cone above …" | "This pair is the Cleo-Antonius: the Cleo-Icos cone above …" |
| §9.1 | "DICTO named it the DICTO Yantra. Its exact form is Theorem 9." | "This is the DICTO Yantra. Its exact form is Theorem 9." |
| §9.2 | "DICTO proposed the Cleo-Icos as the great pair, then the kite proportion: keep the Cleo but not the rhombus. The Cleo-Octangula is DICTO's name for the pair of a Cleo-Icos above and the stella's tetrahedron below (u = 2/φ², v = 1/√2)." | "Take the Cleo-Icos as the great pair, then the kite proportion: keep the Cleo but not the rhombus. The Cleo-Octangula is the pair of a Cleo-Icos above and the stella's tetrahedron below (u = 2/φ², v = 1/√2)." |
| §9.3 | "DICTO proposed keeping the stella. PF2 keeps …" | "PF2 keeps …" (delete the first sentence) |
| §9.4 | "DICTO proposed a gnomon like his Julias (#54). When the bindu's incircle …" | "A gnomon, like DICTO's Julias (#54): when the bindu's incircle …" |
| §10 | "The check run backwards. DICTO proposed running the check backwards (backwards.py). From each polynomial alone, …" | "The check run backwards (backwards.py). From each polynomial alone, …" |
| §11 | "DICTO proposed the Cleo sphere: twenty yantras (V1), …" and "DICTO then proposed the 81-triangle sphere: each of the twenty faces …" | "The Cleo sphere: twenty yantras (V1), …" and "The 81-triangle sphere: each of the twenty faces …" |

Check before the Version 3 PDF: grep the draft for "DICTO proposed", "DICTO chose", "DICTO named" and "DICTO compared". Each hit must be gone, except inside a quotation.

---

## Patch 8: the status box and version line (when Version 3 is released)

"Version 3 adds certificates for Theorems 9 and 10 (irreducibility, real-root isolation, and interval Newton with the elimination identities); certified piece counts for the DICTO Yantra (43) and Kulaichev's yantra (45); Appendix H (Theorem 6's relation H in full); a proof-status table; admissibility conditions in Theorem 1; and the narrower heading of Proposition 8."
