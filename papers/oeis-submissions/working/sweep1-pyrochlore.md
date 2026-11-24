# OEIS working page: Sweep 1, closed walks per site of the pyrochlore network

Prepared 24 Nov 2026 from ENTRIES.md QUEUE item 2 and studies/2026-11-18-oeis-sweep (candidate 1); rules 0, 0b, 1-15
applied. Data and facts only: DICTO writes the entry. Nothing submitted. Checks: studies/2026-11-24-oeis-entry2-sweep1 (FINAL ok).

## 1. The sequence

- **What it counts.** The pyrochlore network: the sites are the corners of corner-sharing tetrahedra (the spin-ice
  lattice); each site is joined to 6 others, 3 in each of its 2 tetrahedra. It is the line graph of the diamond network
  (one site at the midpoint of each bond; two sites joined when their bonds share an atom). a(n) = number of closed walks
  of n steps that start and end at a fixed site. All sites are alike.
- **Home paper:** #102, DICTO, *Every Site Hears the Same: the Loop Equality Is a Theorem*, DICTO DOI: 10.5281/zenodo.24037664
  (v6, released 15 Nov 2026). **Corollary 2** (spin ice), opened and read: "On the pyrochlore network of every stacking, at
  every site and for every length, the numbers of closed walks ... equal those of the pyrochlore network of diamond
  (lengths 1 to 14: walks 0, 6, 12, 78, 300, 1512, ...)". Its proof sets up the incidence-matrix identities used in the
  formula below, and the paper defines the pyrochlore network as the line graph of the stacking's network. #102 does NOT print the Domb-number formula.
- **DATA** (n = 0..25, 246 characters):

```
1,0,6,12,78,300,1512,7056,35214,176124,902496,4679136,24590208,130560768,699729792,3779987712,20562988878,112547448924,619346672208,3424664011776,19018122975768,106021551258096,593110987716000,3328539189498432,18733818892838688,105717847936756800
```

- **OFFSET:** `0,3` (a(0) = 1, as in A002895, A002899 and A338672; the first term above 1 is the third).
- **b-file:** working/b-sweep1-pyrochlore.txt, n = 0..40 (the stated range), format "n a(n)". The formula below is proved,
  so a longer b-file could come from it if DICTO wants one; 0..40 is what the two independent methods checked.

## 2. Facts for the fields

### Terms recomputed two independent ways (24 Nov 2026, FINAL ok)
1. Study scripts rerun: studies/2026-11-18-oeis-sweep/scripts/pyrochlore.py (formula, n = 0..40; its own check against
   the direct count passes, FINAL ok) and studies/2026-11-08-pyrochlore-walks/walks.py (direct count on the network from
   pyrochlore coordinates, n = 0..30, FINAL ok).
2. Fresh method, fresh_pyrochlore_linegraph.py: builds diamond's atoms and bonds, makes the sites the bonds and joins
   bonds that share an atom, then counts closed walks by dynamic programming over all 14431 sites within 20 steps, n = 0..40.
   It uses no formula and none of walks.py's code. Equal to method 1 at every n = 0..40.
3. The two PARI programs below (run with PARI/GP 2.19) give the same 41 terms.
4. OEIS searched 24 Nov 2026: `1,0,6,12,78,300,1512,7056,35214,176124`, `6,12,78,300,1512,7056,35214` and the halved
   `3,6,39,150,756,3528`: no match; the word "pyrochlore" appears nowhere in the OEIS.

### NAME (two wordings; DICTO picks or writes his own)
- (a) Number of n-step closed walks on the pyrochlore lattice.  (the form of A338672, "... on kagome lattice")
- (b) Number of closed walks of length n starting and ending at a fixed site of the pyrochlore network (corner-sharing tetrahedra).

### FORMULA facts
- **Exact formula (proved):**
  - (a) `a(n) = ((-2)^n + Sum_{k=0..floor(n/2)} binomial(n,2*k)*2^(n-2*k)*A002895(k))/2.`  (the form of A338672's second %F)
  - (b) `a(n) = (1/2)*Sum_{i=0..n} binomial(n,i)*2^(n-i)*w(i) + (1/2)*(-2)^n, where w(i) = A002895(i/2) for even i and 0 for odd i.`
- **G.f. (follows from the formula):**
  - (a) `G.f.: (1/(1+2*x) + D(x^2/(1-2*x)^2)/(1-2*x))/2, where D(x) = Sum_{k>=0} A002895(k)*x^k.`
  - (b) the same with D(x) written out by van Hoeij's hypergeometric g.f. on A002895 (longer; only if DICTO wants it closed).
- **Proof (exact, every n).** Let S be the atom-bond incidence matrix of diamond. Then S*S^T = A + 4I (A = diamond's
  adjacency; 4 bonds per atom) and S^T*S = P + 2I (P = the pyrochlore adjacency; each bond has 2 atoms). Both identities are
  in #102, proof of Corollary 2. For j >= 1, trace((S^T*S)^j) = trace((S*S^T)^j). Count on a periodic piece large
  enough that no walk of length n wraps round, with V atoms and E = 2V bonds:
  trace(P^n) = trace((S^T*S - 2I)^n) = (E - V)*(-2)^n + trace((A + 2I)^n), and trace((A + 2I)^n) = V*Sum_i C(n,i)*2^(n-i)*w(i).
  So E*a(n) = V*Sum_i C(n,i)*2^(n-i)*w(i) + (E - V)*(-2)^n; dividing by E = 2V gives the formula.
  Checked numerically against the direct counts for n = 0..40.
- **Same numbers on every stacking:** #102 Corollary 2 (contains it): every site of the pyrochlore network of every
  close-packed stacking, periodic or not, has these closed-walk numbers.
- Kagome analog: A338672's formula a(n) = ((-2)^n + 2*Sum ... A002893 ...)/3 has the same shape (kagome is the line graph
  of the honeycomb net, 3-regular, E/V = 3/2; here 4-regular, E/V = 2). Checked by hand: the general line-graph formula
  gives A338672's a(2) = 4 and a(3) = 4.

### EXAMPLE facts (numbers only)
- a(1) = 0 (no step returns at once).
- a(2) = 6: out and back along each of the 6 bonds.
- a(3) = 12: the site is a corner of 2 tetrahedra; in each, 3 triangles pass through it; each walked 2 ways: 2*3*2 = 12.
- a(4) = 78 (printed in #102 Corollary 2).

### PROG (all run 24 Nov 2026; each prints exactly the DATA, n = 0..25)
- (a) PARI, function form (the form of A338672's %o):

```
(PARI) D(m)=sum(k=0,m,binomial(m,k)^2*binomial(2*k,k)*binomial(2*m-2*k,m-k));
a(n)=(sum(i=0,n\2,binomial(n,2*i)*2^(n-2*i)*D(i))+(-2)^n)/2;
vector(26,n,a(n-1))
```

  What each line does: D(m) is the Domb number (A002895's own formula); a(n) is the exact formula; `n\2` is floor(n/2);
  the last line lists a(0..25). (Tested as three separate gp lines: in gp a function body runs to the end of its line.)
- (b) PARI, g.f. form:

```
(PARI) my(N=25,G=sum(m=0,N\2,sum(k=0,m,binomial(m,k)^2*binomial(2*k,k)*binomial(2*m-2*k,m-k))*x^(2*m))+O(x^(N+1))); Vec((subst(G,x,x/(1-2*x))/(1-2*x)+1/(1+2*x))/2)
```

  G is the diamond walk series Sum A002895(m)*x^(2m); `subst(G,x,x/(1-2*x))/(1-2*x)` shifts every eigenvalue by 2;
  `1/(1+2*x)` adds the (-2)^n part; `Vec` lists the coefficients.
- (c) Python:

```
(Python)
from math import comb
def domb(m):  # A002895
    return sum(comb(m,k)**2*comb(2*k,k)*comb(2*m-2*k,m-k) for k in range(m+1))
def a(n):
    return (sum(comb(n,2*i)*2**(n-2*i)*domb(i) for i in range(n//2+1)) + (-2)**n)//2
print([a(n) for n in range(26)])
```

### REFERENCES and LINKS (each checked against rule 13)
| Work | Opened? | Contains the claim? | Field |
|---|---|---|---|
| DICTO, #102 *Every Site Hears the Same: the Loop Equality Is a Theorem*, DICTO DOI: 10.5281/zenodo.24037664 | yes (v6 PDF and Zenodo record) | yes: Corollary 2 (terms for lengths 1-6, every site of every stacking; S*S^T = A + 4I and S^T*S - 2I in its proof) | Links only (it has a DOI, rule 11) |
| DICTO, #60 *DICTO Janus c/h Pyrochlore*, DICTO DOI: 10.5281/zenodo.23678750 | no (only cited in #102 for the network) | not checked | leave out unless opened and checked |
| Line-graph spectrum theorem (Sachs 1967) | no free copy opened | - | not cited; the proof above stands alone |

Links line in the house format of DICTO's approved A400949 (two wordings):
- (a) `DICTO, <a href="https://doi.org/10.5281/zenodo.24037664">Every Site Hears the Same: the Loop Equality Is a Theorem</a>, Zenodo (2026). See Corollary 2.`
- (b) the same without "See Corollary 2." (as A400949 has it for #102)

### COMMENTS: facts only (DICTO writes the comment; rule 0b)
- The pyrochlore network is the network of spin ice (corner-sharing tetrahedra); it is the line graph of diamond.
- The same numbers hold at every site of the pyrochlore network of every close-packed stacking, periodic or not: #102 Corollary 2.
- The formula is not printed in #102. It follows from #102's incidence identities (proof above), so a comment or formula
  line should not say "#102 gives the formula".
- Style models for the comment: A002899 and A338672 (their %C/%F wording on a lattice's closed walks).

### CROSSREFS (each fetched from OEIS 24 Nov 2026 and read)
- A002895: Domb numbers, closed 2n-step walks on diamond. Fits: the formula is built from it.
- A338672: n-step closed walks on the kagome lattice. Fits: the 2-D analog (line graph of the honeycomb), same formula shape.
- A002899: n-step closed walks on fcc. Fits: the sphere-packing case of the same "every stacking" result (#102 Cor 3).
- A400949: closed non-backtracking walks on diamond (DICTO's, approved). Fits: same family.
- A402231: closed non-backtracking walks on fcc (DICTO's, approved). Fits: same family.
- Two wordings:
  - (a) `Cf. A002895 (diamond), A338672 (kagome), A002899 (fcc), A400949, A402231.`
  - (b) `Cf. A002895, A002899, A338672, A400949, A402231.` (A-number order, no notes)
- Later: sweep 2 (closed tailless walks on the pyrochlore network) once it has an A-number.

### KEYWORDS
- (a) `nonn,walk`: nonn = no negative terms; walk = counts walks on a lattice (as on A338672 and A002899).
- (b) `nonn,walk,easy`: easy if DICTO counts the one-line formula as an easy program.

## 3. Model entries to follow (all fetched and read 24 Nov 2026)
1. **A338672** (n-step closed walks on the kagome lattice): look at **%F** (the formula with (-2)^n and a binomial sum
   over the honeycomb walk numbers, divided by 3), **%o** (one-line PARI a(n)), **%K** nonn,walk and
   **%O** 0,3. It is the same kind of sequence, one dimension down.
2. **A002899** (n-step polygons on fcc): look at **%O** (0,3, a(0) = 1) and **%Y**. It is the closed-walk entry that #102's
   stacking result also covers, and the one DICTO's planned comment goes on.
3. **A400949** (DICTO's own, approved): look at **%H**, the exact form the editors accepted for the #102 link, and
   **%D/%H**, where each work goes into one field only (rule 11).

## 4. DICTO's entry
(He writes it from sections 1-3 and pastes it here.)

## 5. Verification
(After his entry: field by field, facts only.)

## 6. Status
- 24 Nov 2026: prepared, READY. Not submitted. Sequence places free: two (STATUS 24 Nov: A400949, A402231 and A402191
  approved; only the A008264 comment open). One in, one out (rule 14).
