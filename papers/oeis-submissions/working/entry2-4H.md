# OEIS working page: Entry 2, 4H hexagonal-layer coordination sequence

Prepared 24 Nov 2026 from ENTRIES.md "Entry 2" (rules 0, 0b, 1-15 applied). Data and facts only: DICTO writes the entry.
Nothing submitted. Checks: studies/2026-11-24-oeis-entry2-sweep1 (FINAL ok).

> **BLOCKER: no released home paper contains this sequence.**
> - #74 *Spin Ice and Kagome Magnets on Every Stacking* (DICTO DOI: 10.5281/zenodo.23730421, v2) prints only the shells 3 to 6
>   of diamond (24, 42, 64, 92) and lonsdaleite (25, 44, 67, 96), "with 4H in between (Figure 1a)". Figure 1a plots the 4H
>   *average over all sites* as a percentage against 3C (n = 1..6), not the h-site numbers.
> - HexOct book (DICTO DOI: 10.5281/zenodo.23731359, v11), Chapter 13: the same text and figure (Figure 13.1a).
> - #102 (DICTO DOI: 10.5281/zenodo.24037664, v6): Figure 2a plots shell differences in percent for 686 sites; no terms.
> - No paper names the h/c split or says that the A-bilayer atoms have A008264.
>
> So the prepared %D/%H lines to #74 and HexOct fail rule 13 (the cited work must contain the claim), as the A008264 link
> did on 16 Nov. The entry can go in with no DICTO link (a computed coordination sequence needs none), or after a released
> paper prints the sequence. DICTO decides which.
>
> **Open prior-art point: O'Keeffe 1991** (Chem. Mater. 3, 332-335, "Topological and geometrical characterization of
> sites in silicon carbide polytypes") may print the first terms for the 4H sites. A008264 cites its Eq. (2) for the
> lonsdaleite formula. It is closed access (OpenAlex: closed, no repository copy; Crossref has no abstract) and was not
> opened, so it cannot be cited for any claim (rule 13), and it is not known whether it holds this sequence.

---

## 1. The sequence

- **What it counts.** The 4H stacking of close-packed bilayers, ABAC repeated (4H-SiC network, all atoms alike). In each
  bilayer the lower atom bonds to the upper atom straight above it, and each upper atom bonds to three lower atoms of the
  next bilayer. B and C are the hexagonal (h) bilayers: both neighbours of each sit at A. a(n) = number of atoms exactly n
  bonds from an atom of an h bilayer. All four h-bilayer atoms of the period (B and C; lower and upper) give the same
  sequence (checked to n = 200).
- **Home paper:** none released holds it (blocker above).
- **DATA** (n = 0..57, 260 characters):

```
1,4,12,24,42,66,96,130,170,214,264,318,378,444,516,592,674,760,852,948,1050,1158,1272,1390,1514,1642,1776,1914,2058,2208,2364,2524,2690,2860,3036,3216,3402,3594,3792,3994,4202,4414,4632,4854,5082,5316,5556,5800,6050,6304,6564,6828,7098,7374,7656,7942,8234,8530
```

  (n = 0..56 is 255 characters if the editors want a margin: drop ",8530".)
- **OFFSET:** `0,2`
- **b-file:** working/b-entry2-4H.txt, n = 0..200, format "n a(n)". The two independent methods below agree at every term.

## 2. Facts for the fields

### Terms recomputed two independent ways (24 Nov 2026, FINAL ok)
1. Study scripts rerun: studies/2026-11-07-oeis-candidates/oeis_checks.py (output identical to the stored
   data-oeis-terms.txt; C3 line "4H site (bilayer 1 [B, h], atom 0)" to n = 60), and the ENTRIES.md Entry 2 Python
   program run as written (n = 0..57, and the same function to n = 200).
2. Fresh method, fresh_4H_geometric.py: exact integer coordinates of the ideal crystal; two atoms are bonded if and only if
   their distance is the bond length (72 d^2 = 8(dx^2 + dx*dy + dy^2) + 3 dz^2 = 27). It uses no stacking-direction rule.
   Shell-by-shell search from all four h-site atoms: identical to method 1 for n = 0..200.
3. Same fresh code from the A-bilayer (c) atoms, lower and upper: equal to the OEIS b-file of A008264 for n = 0..200.
4. OEIS searched 24 Nov 2026: `1,4,12,24,42,66,96,130,170,214,264,318` and `24,42,66,96,130,170,214,264,318,378,444`:
   no match; "4H polytype": only A008264 and A400949 (neither holds these terms).

### NAME (two wordings; DICTO picks or writes his own)
- (a) Coordination sequence of an atom of a hexagonal (h) bilayer of the 4H polytype of diamond (4H-SiC network, stacking ABAC).
- (b) Coordination sequence for the atoms of the hexagonal layers of the 4H (ABAC) stacking of the tetrahedral (diamond-type) network.

### FORMULA facts (all empirical: found from the terms and checked to n = 200, not proved)
- G.f., reduced (gcd of numerator and denominator = 1):
  - (a) `Empirical g.f.: (1 + 2*x + 5*x^2 + 4*x^3 + 6*x^4 + 6*x^5 + 6*x^6 + 4*x^7 + 5*x^8 + 2*x^9 + x^10)/((1-x)^2*(1-x^8)).`
  - (b) the same with the denominator expanded: `.../(1 - 2*x + x^2 - x^8 + 2*x^9 - x^10)`.
- Recurrence, from the denominator; it holds for n >= 11 (checked to 200):
  - (a) `a(n) = 2*a(n-1) - a(n-2) + a(n-8) - 2*a(n-9) + a(n-10) for n >= 11.`
  - (b) as an index line: `Index entries for linear recurrences with constant coefficients, signature (2,-1,0,0,0,0,0,1,-2,1).`
- Closed form by residue class, the same shape as A008264's "a(4*m+k) = 42*m^2 + 21*k*m + [2, 4, 12, 25]":
  - (a) `a(8*m+k) = 168*m^2 + 42*k*m + [2, 4, 12, 24, 42, 66, 96, 130], 0 <= k < 8` (for n >= 1; a(0) = 1).
  - (b) `a(n) = 21*(n^2 - k^2)/8 + c(k), k = n mod 8, c = [2, 4, 12, 24, 42, 66, 96, 130]` (for n >= 1).
- Growth: a(n) ~ 21*n^2/8 (42/16 from the g.f. at x = 1), the same leading term as A008264 (lonsdaleite); diamond (A008253) grows as 5*n^2/2.
- Why "empirical": coordination sequences of periodic nets have rational g.f.s in general, but this one was fitted to the
  terms and verified, not derived. Keep the word, as on A301299 (whose g.f. was later "confirmed by" a published proof).

### EXAMPLE facts (numbers only)
- a(1) = 4, a(2) = 12 (as in diamond and lonsdaleite).
- a(3) = 24: diamond (A008253) also 24; lonsdaleite (A008264) and the A-bilayer atoms of the same 4H crystal 25.
- a(5) = 66: diamond 64, lonsdaleite 67.
- First differences: from lonsdaleite at n = 3; from diamond at n = 5. Equal to lonsdaleite again for many larger n (e.g. n = 6..10: 96, 130, 170, 214, 264).

### PROG (both run 24 Nov 2026 and print exactly the DATA)
- (a) Python: the ENTRIES.md Entry 2 program, unchanged; its last line `print(coordseq('ABAC', 1, 0, 57))` prints the
  58 terms (as a Python list). It computes the network itself, so it is not empirical.
- (b) PARI, from the empirical g.f. (prints the same 58 terms; editors may want it marked as from the empirical g.f.):

```
(PARI) Vec((1+2*x+5*x^2+4*x^3+6*x^4+6*x^5+6*x^6+4*x^7+5*x^8+2*x^9+x^10)/((1-x)^2*(1-x^8))+O(x^58))
```

  What each part does: the fraction is the g.f.; `+O(x^58)` cuts the power series after x^57; `Vec` lists its 58 coefficients.

### REFERENCES and LINKS (each checked against rule 13)
| Work | Opened? | Contains the claim? | Use |
|---|---|---|---|
| DICTO, #74 Spin Ice and Kagome Magnets on Every Stacking, DICTO DOI: 10.5281/zenodo.23730421 | yes (v2 PDF) | NO: no 4H site terms (only diamond/lonsdaleite shells 3-6 and a 4H site-average plot) | do not cite for this sequence |
| DICTO, HexOct book, DICTO DOI: 10.5281/zenodo.23731359 | yes (v11 PDF, Ch. 13) | NO: same text as #74 | do not cite for this sequence |
| DICTO, #102 Every Site Hears the Same, DICTO DOI: 10.5281/zenodo.24037664 | yes (v6) | holds only the walk statement (Theorem 1: closed walks and closed non-backtracking walks at every atom of every stacking equal diamond's); no shells | fits only a comment that links the walk counts (A002895, A400949), if DICTO writes one |
| M. O'Keeffe 1991, Chem. Mater. 3, 332-335, doi:10.1021/cm00014a025 | NO (closed access) | unknown | cannot be cited (rule 13); prior-art point open |
| RCSR | not checked: no RCSR net name for the 4H SiC network was looked up | - | optional; A008264 links RCSR "lon" |

If a DICTO paper is cited later: Links only (rule 11, it has a DOI), house format as on A400949:
`DICTO, <a href="https://doi.org/10.5281/zenodo.NNNNNNNN">Title</a>, Zenodo (2026).`

### COMMENTS: facts only (DICTO writes the comment; rule 0b)
- The network: bilayers ABAC repeated; B and C are hexagonal, A cubic (Jagodzinski symbol hc). All atoms of B and C have
  this sequence; all atoms of A have A008264 (checked to n = 200 against the A008264 b-file). Source: the computation only.
- The closed walks (A002895) and closed non-backtracking walks (A400949) are the same at these atoms as in diamond: #102 Theorem 1 (contains it).
- Style models for a comment of this kind: A301299 (its %C), A321019 (its %C, one sentence defining the net).

### CROSSREFS (each fetched from OEIS 24 Nov 2026 and read)
- A008253: coordination sequence of diamond (3C). Fits: same network type, all cubic layers.
- A008264: tridymite, lonsdaleite, wurtzite (2H). Fits: all hexagonal layers; also the A-bilayer atoms of 4H (checked to 200).
- A002895: Domb numbers (closed walks on diamond). Fits: same closed walks at these atoms (#102 Thm 1).
- A400949: closed non-backtracking walks on diamond (DICTO's, approved). Fits: same at these atoms (#102 Thm 1).
- Two wordings:
  - (a) `Cf. A008253 (diamond, 3C), A008264 (lonsdaleite, 2H; also the cubic-layer atoms of 4H), A002895, A400949.`
  - (b) `Cf. A002895, A008253, A008264, A400949.` (A-number order, no notes)
- Later: the 6H entries (3, 4, 5) once they have A-numbers.

### KEYWORDS
- (a) `nonn,easy`: nonn = all terms positive; easy = a short program computes many terms (as on A008264, A301299, A321019).
- (b) `nonn`: if DICTO prefers not to claim "easy".
- Not `walk`: this is a shell count, not a walk count.

## 3. Model entries to follow (all fetched and read 24 Nov 2026)
1. **A008264** (lonsdaleite coordination sequence): look at **%F** for the residue-class form a(4*m+k) = ... and the g.f.,
   and at the **%H Index entries ... signature** line (last in Links). The sister sequence; the 4H formulas copy its shape.
2. **A301299** (node of type V1 in the 2-D "krq" net): look at **%N** (naming one site type of a net with two site types),
   **%Y** (the sibling A301301 named), and the **%C** "g.f. confirmed by" note: how an empirical g.f. is worded.
3. **A321019** (a 3-D net with respect to a 5-valent point): look at **%o** (a one-line PARI `Vec(g.f. + O(x^N))`
   program) and **%F** (g.f., then recurrence, then closed form, each a separate line).

## 4. DICTO's entry
(He writes it from sections 1-3 and pastes it here.)

## 5. Verification
(After his entry: field by field, facts only.)

## 6. Status
- 24 Nov 2026: prepared; BLOCKED on the home-paper question (see top) and the O'Keeffe 1991 prior-art point. Not submitted.
