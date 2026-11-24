# OEIS working page: Sweep 2, closed tailless walks per site of the pyrochlore network

Prepared 24 Nov 2026 from ENTRIES.md QUEUE item 3 (rules 0, 0b, 1-15 applied). Data and facts only: DICTO writes the entry.
Nothing submitted. Checks: studies/2026-11-24-oeis-sweep2-pyrochlore-tailless (each script prints FINAL ok).
Place: this is the third open item (the A008264 comment, Sweep 1, this), the most allowed by rule 14.

## 1. The sequence

- **What it counts.** Closed walks of n steps that start and end at a fixed site of the pyrochlore network (the spin-ice
  network: corner-sharing tetrahedra), never step straight back, and do not step back across the start either
  (cyclically non-backtracking, "tailless"). All sites are alike. It is the pyrochlore partner of A400949 (diamond) and
  A402231 (fcc), and the non-backtracking partner of Sweep 1 (closed walks, submitted).
- **Home paper:** DICTO, #102 *Every Site Hears the Same: the Loop Equality Is a Theorem*, DICTO DOI: 10.5281/zenodo.24037664.
  Corollary 2 prints the terms "loops 0, 0, 12, 12, 0, 276, 756, 2988, …" (lengths 1 to 8). It also states that the same
  numbers hold at every site of the pyrochlore network of every stacking. Read in the released PDF on 24 Nov.
- **DATA** (n = 1..27, 246 characters):

```
0,0,12,12,0,276,756,2988,16104,64800,278916,1286352,5738928,25845036,118098612,540178572,2482501704,11470845192,53186644596,247472898972,1155354197016,5409675441324,25398322598892,119545910744592,563987677987800,2666471876270592,12632008967689620
```

- **OFFSET:** `1,3` (a(3) = 12 is the first term greater than 1).
- **b-file:** studies/2026-11-24-oeis-sweep2-pyrochlore-tailless/data/b-sweep2.txt, n = 1..40, format "n a(n)".

## 2. Facts for the fields

### Terms computed two independent ways (24 Nov 2026, FINAL ok, n = 1..40)
1. **Direct count** (`scripts/direct_count.py`). The network is built as the line graph of diamond. Walks are counted by
   dynamic programming over (site, previous site), with no formula at all. Run time 20 s.
2. **Formula** (`scripts/formula_check.py`, exact rational series). Both formulas below agree with method 1 at every term.
   The Python program below also agrees (`scripts/prog_check.py`).
3. The 2026-11-18 sweep's Ihara–Bass terms agree too, as does its separate Hashimoto count to n = 30.
4. OEIS searched 24 Nov 2026: `12,12,0,276,756,2988,16104,64800` and `276,756,2988,16104,64800,278916,1286352` gave no
   match.

### NAME (two wordings; DICTO picks or writes his own)
- (a) Number of closed non-backtracking walks of length n (cyclically non-backtracking, i.e., tailless) starting and ending at a fixed site of the pyrochlore network.
- (b) Number of closed tailless non-backtracking walks of length n at a site of the pyrochlore network.

(a) has the same shape as A400949's name.

### FORMULA facts (proved: the Ihara–Bass formula with the pyrochlore spectrum; checked exactly to n = 40)
- **Logarithmic form,** as on A400949:
  - (a) `Sum_{n>=1} a(n)*x^n/n = -2*log(1-x^2) - (1/2)*log(1+6*x^2+25*x^4) + Sum_{k>=1} A002895(k)*(x/(1-2*x+5*x^2))^(2*k)/(4*k) (Ihara-Bass formula for a 6-regular net).`
  - Why it holds: the network is 6-regular (q = 5). Half of its spectrum is −2, and the other half is 2 + μ, with μ running
    over diamond's spectrum, whose even moments are A002895. Then 1 + 2x + 5x^2 times 1 − 2x + 5x^2 is 1 + 6x^2 + 25x^4.
- **Ordinary g.f.,** in the shape of A402231's G.f. line:
  - (b) `G.f.: 4*x^2/(1-x^2) - 10*x^2/(1+5*x^2) + ((1-5*x^2)/(1+5*x^2))*(P(x/(1+5*x^2)) - 1), where P(x) is the g.f. for A?????? (Sweep 1).`
  - Put in Sweep 1's A-number once known.

### EXAMPLE facts (numbers only)
- a(1) = a(2) = 0.
- a(3) = 12: the site lies on 2 tetrahedra and on 3 triangles in each, so 6 triangles, each walked in 2 directions. This is
  the same count as Sweep 1's a(3).
- a(4) = 12: each tetrahedron has 3 four-cycles through the site, walked in 2 directions, and there are 2 tetrahedra.
- a(5) = 0. This was computed, not derived by hand.

### PROG (run 24 Nov 2026; it prints the 40 terms equal to the direct count)

```
(Python)
from math import comb
from fractions import Fraction
def domb(m):  # A002895
    return sum(comb(m,k)**2*comb(2*k,k)*comb(2*m-2*k,m-k) for k in range(m+1))
def w(n):  # closed n-step walks per pyrochlore site
    return (sum(comb(n,2*i)*2**(n-2*i)*domb(i) for i in range(n//2+1)) + (-2)**n)//2
def loops(W, q):  # Ihara-Bass per vertex of a (q+1)-regular net; W[i] = closed i-step walks
    M = len(W)-1; c = [Fraction(0)]*(M+1)
    for k in range(1, M//2+1): c[2*k] += Fraction(q-1, 2*k)
    for j in range(1, M+1):
        for i in range(j+1):
            if 2*j-i <= M: c[2*j-i] += Fraction(comb(j,i)*W[i]*(-q)**(j-i), j)
    return [int(m*c[m]) for m in range(1, M+1)]   # lengths 1..M
print(loops([w(i) for i in range(28)], 5))
```

`loops` is A400949's own function, unchanged. `w` is the program of Sweep 1, and `range(28)` prints the 27 DATA terms.

### REFERENCES and LINKS (rule 13: the cited work must contain the claim; rule 11: Links only)
| Work | Opened? | Contains the claim? | Use |
|---|---|---|---|
| DICTO, #102 Every Site Hears the Same, DICTO DOI: 10.5281/zenodo.24037664 | yes (released PDF) | YES: Corollary 2 prints a(1..8) and the every-stacking statement | %H |
| Bramwell and Gingras, Spin Ice State in Frustrated Magnetic Pyrochlore Materials (arXiv:cond-mat/0201427) | as on Sweep 1 | the network only | optional, as in Sweep 1 |

House format: `DICTO, <a href="https://doi.org/10.5281/zenodo.24037664">Every Site Hears the Same: the Loop Equality Is a Theorem</a>, Zenodo (2026).`

### COMMENTS: facts only (DICTO writes the comment; rule 0b)
- The same numbers hold at every site of the pyrochlore network of every stacking (#102, Corollary 2; contains it).
- The pyrochlore network is the line graph of the diamond network, as in Sweep 1's comment.

### CROSSREFS (each fetched from OEIS 24 Nov 2026 and read)
- A400949: closed tailless walks on diamond (DICTO's, approved). This is its pyrochlore analog.
- A402231: the same for fcc (DICTO's, approved).
- A002895: Domb numbers, used in the formula.
- A?????? (Sweep 1): all closed walks on pyrochlore.
- Two wordings:
  - (a) `Cf. A002895, A400949 (diamond analog), A402231 (fcc analog), A??????.`
  - (b) `Cf. A002895, A400949, A402231.` Use this one if Sweep 1 has no number yet; add it later.

### KEYWORDS
- `nonn,walk`. nonn: all terms are ≥ 0. walk: it counts walks. These are the same keywords as A400949 and A402231.

## 3. Model entries to follow
1. **A400949**: look at its **%N** (the tailless wording), its **%F** (the log form, "Ihara-Bass formula for a 4-regular
   net"), and its **%o** (the `loops` program).
2. **A402231**: look at its **%F** G.f. line (P(x/(1+q*x^2)) shape), its **%e** (the triangle count) and its **%C** (the
   every-stacking statement in one sentence).

## 4. DICTO's entry
(He writes it from sections 1-3 and pastes it here.)

## 5. Verification
(After his entry: field by field, facts only.)

## 6. Status
- 24 Nov 2026: prepared, checks FINAL ok. Not submitted. Waits on DICTO's wording.
