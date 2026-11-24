# Referee report: Sweep 1, closed walks per site of the pyrochlore network

24 Nov 2026. Independent check of working/sweep1-pyrochlore.md (the HTML copy carries the same data, formula,
g.f., crossrefs and all three programs, compared character by character after stripping tags). Rules: ENTRIES.md 0-15.

## Verdict: READY

No error found in the data, offset, formula, proof, g.f., programs, links or crossrefs. Three small points to
tidy (findings 1-3) and one check that could not be made from here (finding 4). None changes a number.

## Findings, in order of severity

1. **Proof: one step is used but not said (clarity, not an error).** The line "E*a(n) = trace(P^n)" needs two
   things the proof does not state at that point: (i) every site of the pyrochlore network is alike (true: the
   symmetries of diamond carry every bond to every other; the worksheet says it in section 1 only), and (ii) the
   periodic piece must be large enough that neither the diamond walks of length <= n nor the pyrochlore walks of
   length n wrap round. With these said, the proof is complete for every n >= 0.
2. **The proof text is prepared prose (rule 0 / 0b).** If the proof goes into the entry (as a %C or as a note on
   the %F line), DICTO writes it in his own words; the worksheet paragraph is the list of steps, not text to
   paste. Everything else is in the agreed form: two wordings for name, formula, g.f., links, crossrefs and
   keywords; comments as facts only; no text in sections 4-5; one sequence, not a bulk submission.
3. **"See Corollary 2." on a concept DOI (minor).** 10.5281/zenodo.24037664 is the all-versions DOI, so it will
   follow later versions; if a later version renumbers the corollaries the pointer goes stale. Wording (b)
   (no "See ...", as on approved A400949) avoids this; wording (a) is correct for Version 6.
4. **Zenodo page not opened by this check.** Zenodo answered 403 (traffic restriction) to one request from each
   of two machines; no further requests were made. Checked instead: the published Version 6 PDF kept in the
   repository (sha256 073ee846605f80ea..., commit "#102 Version 6 published", 20 pages, header "Paper #102,
   Version 6, 15 November 2026, DICTO DOI: 10.5281/zenodo.24037664"), and the stored record state
   (version record 24241321, concept record 24037664, published). The worksheet's own author reports having
   opened the Zenodo record; a one-glance look at the live page by DICTO closes this.

## What was checked, point by point

**(1) DATA: correct.** Own method: the pyrochlore sites built from coordinates (four-site basis on the
face-centred cubic translations, neighbours at squared distance 2, every site checked to have 6 neighbours),
closed walks counted by exact integer propagation with no cut-off, from each of the 4 basis sites, n = 0..40.
The four sites agree. a(0..25) equals the DATA line character for character (246 characters); a(0..40) equals
b-sweep1-pyrochlore.txt (41 lines). This used neither the line-graph construction nor any formula, so it is
independent of both worksheet methods.

**(2) OFFSET 0,3: correct.** a(0) = 1, a(1) = 0, a(2) = 6; the first term greater than 1 in absolute value is the
third term (positions counted from 1). Same as A338672 and A002899 (both %O 0,3, read today).

**(3) FORMULA, proof and g.f.: correct, proved for every n.**
- S*S^T = A + 4I and S^T*S = P + 2I: both hold (4 bonds per atom, 2 atoms per bond, two bonds share at most
  one atom); both are in #102, proof of Corollary 2 ("adjacency matrix S^T S - 2I ... S S^T = A + 4I").
- Trace identity: trace((S^T S)^j) = trace((S S^T)^j) for j >= 1; for j = 0 the traces are E and V. Expanding
  (S^T S - 2I)^n by the binomial theorem, only the j = 0 term differs, by (E - V)*(-2)^n. So
  trace(P^n) = (E - V)*(-2)^n + trace((A + 2I)^n). Correct.
- E/V = 2 (every atom has 4 bonds, each bond shared by 2). Correct. Dividing by E = 2V gives formula (a)/(b).
- n = 0 gives 1; the bracket is even for every n tested to 200, as the proof requires.
- Formula against my direct count: equal for n = 0..40.
- G.f.: Sum_n binomial(n,m)*2^(n-m)*x^n = x^m/(1-2x)^(m+1), so the sum is D(x^2/(1-2x)^2)/(1-2x), and the
  (-2)^n part is 1/(1+2x). The g.f. as worded, expanded in PARI to x^60, equals the formula term by term.
- Kagome hand-check repeated: the same argument with degree 3 and E/V = 3/2 gives A338672's second %F exactly,
  and a(2) = 4, a(3) = 4.
- van Hoeij's hypergeometric g.f. is on A002895 as stated (wording (b) of the g.f. was not expanded here).

**(4) Programs: all three print exactly the DATA.** Run as written, extracted from the worksheet by script:
PARI (a) as three gp lines, PARI (b) as one line (PARI 2.19 through cypari2), Python under python3. Each gives
26 terms equal to the DATA line.

**(5) Links: #102 Corollary 2 contains the claim.** Version 6 text: "Corollary 2 (spin ice). On the pyrochlore
network of every stacking, at every site and for every length, the numbers of closed walks and of closed
non-backtracking loops equal those of the pyrochlore network of diamond (lengths 1 to 14: walks 0, 6, 12, 78,
300, 1512, ...; loops ...)". So the terms a(1..6) and the every-stacking statement are both there; "periodic or
not" is in the abstract; the line-graph definition is in section 1; the check table lists the pyrochlore walks
on 19 stackings, lengths 1 to 14. #102 does not print the Domb-number formula, as the worksheet says. The link
line matches the approved A400949 %H line for #102 exactly. See findings 3 and 4.

**(6) CROSSREFS and novelty: fit; not in the OEIS.** All five A-numbers fetched today and read: A002895 (Domb
numbers, diamond polygons), A338672 (kagome closed walks, %O 0,3, nonn,walk), A002899 (fcc polygons, %O 0,3),
A400949 and A402231 (both live, author James Baker). Searches today, all "No results": the first ten terms;
6,12,78,300,1512,7056,35214; 78,300,1512,7056; the halved 3,6,39,150,756,3528; and the word "pyrochlore".

**(7) Rules.** Rule 11: #102 is in Links only; nothing proposed for References; #60 and Sachs are left out
because they were not opened (rule 13). Rule 12: worked cases are under EXAMPLE. Rule 15: with a b-file, the
"Table of n, a(n)" line comes first, then DICTO. Rule 0: DATA 246 characters, ASCII only; each program has a
line-by-line explanation for the author; AI is not named as author; see finding 2 for the proof text.
Example facts checked: a(2) = 6, a(3) = 2*3*2 = 12, a(4) = 78 (printed in Corollary 2).
