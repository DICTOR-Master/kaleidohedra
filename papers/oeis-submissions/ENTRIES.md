# OEIS submissions prepared for DICTO (7 November 2026)

Nothing has been submitted. DICTO submits these himself from his own OEIS account.

## How to submit

1. Register: oeis.org → "Register" (an OEIS wiki account). The OEIS asks contributors to register under their real full name; the %A line then carries that name ("_First Last_"). Decide how DICTO appears before registering (see "Open points").
2. Log in, then open oeis.org/Submit.html ("Contribute a new sequence"). The form has one box per field below (%N name, data, %O offset, %C comments, %D references, %H links, %F formulas, %e example, %p/%o programs, %Y cross-references, %K keywords). Paste the text after the tag, without the "%X A??????" prefix.
3. Submit ONE entry first (recommended: entry 1). The draft gets its A-number at once; the editors then comment on the draft's page.
4. Answer the editors on the draft page ("Discussion"), and edit the draft there; do not resubmit a changed copy.
5. When entry 1 is approved, submit the next one, replacing the placeholder A?????? numbers in %Y and %C by the real A-numbers.
6. The comments on existing entries (section C) are added with "edit" on that entry's page; each also goes through the editors.
7. New contributors are asked to keep only a few drafts open at a time; one at a time is safest.
8. Links (%H) must be stable: use the Zenodo DOIs; entry 1 and the comments on A002895/A002899 should wait until #102 is released and has its DOI.
9. The editors may shorten names, ask for a PARI/Mathematica program, or move text between fields; that is normal.
10. Each program below runs in python3 in under one second and prints exactly the data shown.

Order suggested: 1 (after #102 is out), 2, 3, 4, 5, 6, then the comments, then 7 (optional).

All terms below were recomputed on 7 November 2026: `studies/2026-11-07-oeis-candidates/oeis_checks.py` rerun (output identical to `data-oeis-terms.txt`, FINAL ok); the coordination sequences extended to n = 100 by breadth-first search on all atoms of one period; and every program printed in this file was run as written and compared term by term with the data lines.

---

## A. New entries

### Entry 1. Closed non-backtracking walks per atom of diamond

```
%I A??????
%S A?????? 0,0,24,48,480,3432,25704,194256,1509072,11820000,93722376,750276792,6056400480,
%T A?????? 49241424120,402912569544,3315331754256,27416593190640,227742362372496,
%U A?????? 1899436965599880,15899758239277008,133535586308211888,1124913591689189016,9502705513658774712
%N A?????? Number of closed non-backtracking walks of length 2n (cyclically non-backtracking, i.e., tailless) starting and ending at a fixed atom of the diamond network.
%C A?????? A walk v_0, v_1, ..., v_{2n} = v_0 along bonds is non-backtracking if v_{i+1} != v_{i-1} for all i, including v_1 != v_{2n-1}. a(n) = (1/|V|) trace(B^(2n)) for the Hashimoto (non-backtracking edge) matrix B of the diamond network; walks of odd length do not exist since the network is bipartite.
%C A?????? a(1) = a(2) = 0 because the shortest cycles of diamond are its six-rings.
%C A?????? The same numbers hold at every atom of lonsdaleite (hexagonal diamond, 2H) and of the tetrahedral network of every close-packed stacking (polytypes 4H, 6H, 9R, ..., periodic or not), although their coordination sequences differ (A008253, A008264, A??????): this is DICTO's Loop Equality, found in #74 for lengths 6 to 34 on five stackings and proved for all lengths in #102 (Theorem 1). The corresponding statement for all closed walks (A002895) is due to Nagle (1966, ice) and Thorpe (1972, periodic polytypes).
%D A?????? DICTO, Spin Ice and Kagome Magnets on Every Stacking (#74), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23730421, Section 3.
%D A?????? DICTO, Every Site Hears the Same: the Loop Equality Is a Theorem (#102), Zenodo, 2026 (DOI at release).
%D A?????? DICTO, HexOct: The Hexagonality Law, with the Window Law, the Rule of Halves & the Swap Rule (book), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23731359, Chapter 13.
%D A?????? J. F. Nagle, Lattice statistics of hydrogen bonded crystals. I. The residual entropy of ice, J. Math. Phys. 7 (1966), 1484-1491.
%D A?????? M. F. Thorpe, Random walks in polytype structures, J. Math. Phys. 13 (1972), 294-299.
%D A?????? H. Bass, The Ihara-Selberg zeta function of a tree lattice, Internat. J. Math. 3 (1992), 717-797.
%H A?????? DICTO, <a href="https://doi.org/10.5281/zenodo.23730421">Spin Ice and Kagome Magnets on Every Stacking</a>, Zenodo (2026).
%H A?????? DICTO, <a href="https://doi.org/10.5281/zenodo.XXXXXXXX">Every Site Hears the Same: the Loop Equality Is a Theorem</a>, Zenodo (2026).
%H A?????? DICTO, <a href="https://doi.org/10.5281/zenodo.23731359">HexOct: The Hexagonality Law</a>, Zenodo (2026).
%H A?????? M. F. Thorpe, <a href="https://doi.org/10.1063/1.1665973">Random walks in polytype structures</a>, J. Math. Phys. 13 (1972), 294-299.
%F A?????? Sum_{n>=1} a(n)*x^n/n = -2*log((1-x)*(1+3*x)) + Sum_{k>=1} A002895(k)*(x/(1+3*x)^2)^k/k (Ihara-Bass formula for a 4-regular net).
%F A?????? G.f.: 2*x/(1-x) - 6*x/(1+3*x) + ((1-3*x)/(1+3*x))*(D(x/(1+3*x)^2) - 1), where D(x) = Sum_{k>=0} A002895(k)*x^k.
%e A?????? a(3) = 24: each atom of diamond lies on 12 six-rings, and each can be walked round in 2 directions.
%o A?????? (Python)
%o A?????? from math import comb
%o A?????? from fractions import Fraction
%o A?????? def domb(n):  # A002895
%o A??????     return sum(comb(n,k)**2*comb(2*k,k)*comb(2*n-2*k,n-k) for k in range(n+1))
%o A?????? def loops(W, q):  # Ihara-Bass per vertex of a (q+1)-regular net; W[i] = closed i-step walks
%o A??????     M = len(W)-1; c = [Fraction(0)]*(M+1)
%o A??????     for k in range(1, M//2+1): c[2*k] += Fraction(q-1, 2*k)
%o A??????     for j in range(1, M+1):
%o A??????         for i in range(j+1):
%o A??????             if 2*j-i <= M: c[2*j-i] += Fraction(comb(j,i)*W[i]*(-q)**(j-i), j)
%o A??????     return [int(m*c[m]) for m in range(1, M+1)]   # lengths 1..M
%o A?????? t = loops([domb(i//2) if i%2 == 0 else 0 for i in range(47)], 3)
%o A?????? print([t[2*n-1] for n in range(1, 24)])
%Y A?????? Cf. A002895 (all closed walks), A008253, A008264, A002899, A??????(entry 7, fcc analog), A??????(entries 2-5).
%K A?????? nonn,walk
%O A?????? 1,3
%A A?????? DICTO, Nov 07 2026
```

Checked: the formula terms equal DICTO's direct count (loops2.py, five stackings) for lengths 6..34 (oeis_checks.py C1), and the g.f. form was expanded and compared for n = 1..30. #102 checked the loops at 686 sites of 42 stackings to length 24.

---

### Entry 2. Coordination sequence of the hexagonal-layer atoms of the 4H polytype

```
%I A??????
%S A?????? 1,4,12,24,42,66,96,130,170,214,264,318,378,444,516,592,674,760,852,948,1050,1158,1272,
%T A?????? 1390,1514,1642,1776,1914,2058,2208,2364,2524,2690,2860,3036,3216,3402,3594,3792,3994,
%U A?????? 4202,4414,4632,4854,5082,5316,5556,5800,6050,6304,6564,6828,7098,7374,7656,7942,8234,8530
%N A?????? Coordination sequence of an atom of a hexagonal (h) bilayer of the 4H polytype of diamond (4H-SiC network, stacking ABAC).
%C A?????? The network: close-packed bilayers stacked ABAC repeated (= ABCB, Jagodzinski symbol hc); each atom is bonded to the atom directly above or below it in its bilayer and to three atoms of the neighbouring bilayer, as in 4H silicon carbide with all atoms alike. The B and C bilayers are hexagonal (their two neighbours sit in the same position A); all their atoms have this sequence. The atoms of the cubic A bilayers have the sequence A008264 of lonsdaleite instead (checked for n <= 100).
%C A?????? The sequence first differs from diamond (A008253) at n = 5 and from lonsdaleite (A008264) at n = 3.
%C A?????? Although the shells differ, the numbers of closed walks (A002895) and of closed non-backtracking walks (A??????, entry 1) of every length at this atom are those of diamond (DICTO, #102, Theorem 1).
%D A?????? DICTO, Spin Ice and Kagome Magnets on Every Stacking (#74), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23730421, Figure 1a.
%D A?????? DICTO, HexOct: The Hexagonality Law, with the Window Law, the Rule of Halves & the Swap Rule (book), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23731359.
%D A?????? M. O'Keeffe, Topological and geometrical characterization of sites in silicon carbide polytypes, Chemistry of Materials 3 (1991), 332-335.
%H A?????? DICTO, <a href="https://doi.org/10.5281/zenodo.23730421">Spin Ice and Kagome Magnets on Every Stacking</a>, Zenodo (2026).
%H A?????? M. O'Keeffe, <a href="https://doi.org/10.1021/cm00014a025">Topological and geometrical characterization of sites in silicon carbide polytypes</a>, Chem. Mater. 3 (1991), 332-335.
%F A?????? Empirical g.f.: (1 + 2*x + 5*x^2 + 4*x^3 + 6*x^4 + 6*x^5 + 6*x^6 + 4*x^7 + 5*x^8 + 2*x^9 + x^10)/((1-x)^2*(1-x^8)) (checked for n <= 100).
%e A?????? a(3) = 24: in diamond also 24, in lonsdaleite and at the A-bilayer atoms of the same 4H crystal 25.
%o A?????? (Python)
%o A?????? def coordseq(stack, k0, u0, N):
%o A??????     # tetrahedral (SiC-type) net on the periodic stacking `stack` of close-packed bilayers.
%o A??????     # Atom (k,x,y,u): bilayer k, in-plane point (x*a1+y*a2)/3, u = 0 lower / 1 upper atom.
%o A??????     p = len(stack); L = ['ABC'.index(c) for c in stack]
%o A??????     D = [(1,1), (-2,1), (1,-2)]          # the 3 shortest vectors from a point of A to B
%o A??????     eps = lambda k: 1 if (L[(k+1)%p]-L[k%p]) % 3 == 1 else -1
%o A??????     def nbrs(v):
%o A??????         k, x, y, u = v
%o A??????         if u: e = eps(k);  return [(k,x,y,0)] + [(k+1,x+e*a,y+e*b,0) for a,b in D]
%o A??????         e = eps(k-1);      return [(k,x,y,1)] + [(k-1,x-e*a,y-e*b,1) for a,b in D]
%o A??????     v0 = (k0, L[k0], L[k0], u0); seen = {v0}; front = {v0}; out = [1]
%o A??????     for _ in range(N):
%o A??????         front = {w for v in front for w in nbrs(v) if w not in seen}
%o A??????         seen |= front; out.append(len(front))
%o A??????     return out
%o A?????? print(coordseq('ABAC', 1, 0, 57))
%Y A?????? Cf. A008253 (diamond, 3C), A008264 (lonsdaleite, 2H; also the A-bilayer atoms of 4H), A??????, A??????, A?????? (6H sites), A002895.
%K A?????? nonn,easy
%O A?????? 0,2
%A A?????? DICTO, Nov 07 2026
```

The same program checks itself: `coordseq('ABC',0,0,n)` gives A008253 and `coordseq('AB',0,0,n)` gives A008264 (all 48 listed terms), as does `coordseq('ABAC',0,1,n)`.

---

### Entry 3. Coordination sequence of the hexagonal-layer atoms of the 6H polytype

```
%I A??????
%S A?????? 1,4,12,24,42,64,92,127,168,213,264,319,380,445,516,591,672,757,848,946,1050,1158,1272,
%T A?????? 1390,1514,1642,1776,1914,2058,2206,2360,2521,2688,2859,3036,3217,3404,3595,3792,3993,
%U A?????? 4200,4411,4628,4852,5082,5316,5556,5800,6050,6304,6564,6828,7098,7372,7652,7939,8232,8529
%N A?????? Coordination sequence of an atom of a hexagonal (h) bilayer of the 6H polytype of diamond (6H-SiC network, stacking ABCACB).
%C A?????? The network: close-packed bilayers stacked ABCACB repeated (Jagodzinski symbol hcc), bonded as in 6H silicon carbide with all atoms alike. The two A bilayers of the period are hexagonal (both neighbours in position B, resp. C); all their atoms have this sequence. The four cubic bilayers carry two other sequences, A?????? (entry 4) and A?????? (entry 5), each at half of their atoms.
%C A?????? Although the shells differ, the numbers of closed walks (A002895) and of closed non-backtracking walks (A??????, entry 1) of every length at this atom are those of diamond (DICTO, #102, Theorem 1).
%D A?????? DICTO, Spin Ice and Kagome Magnets on Every Stacking (#74), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23730421.
%D A?????? DICTO, HexOct: The Hexagonality Law, with the Window Law, the Rule of Halves & the Swap Rule (book), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23731359.
%D A?????? M. O'Keeffe, Topological and geometrical characterization of sites in silicon carbide polytypes, Chemistry of Materials 3 (1991), 332-335.
%H A?????? DICTO, <a href="https://doi.org/10.5281/zenodo.23730421">Spin Ice and Kagome Magnets on Every Stacking</a>, Zenodo (2026).
%H A?????? M. O'Keeffe, <a href="https://doi.org/10.1021/cm00014a025">Topological and geometrical characterization of sites in silicon carbide polytypes</a>, Chem. Mater. 3 (1991), 332-335.
%F A?????? Empirical g.f.: (1 + 2*x + 5*x^2 + 4*x^3 + 6*x^4 + 4*x^5 + 6*x^6 + 7*x^7 + 6*x^8 + 4*x^9 + 6*x^10 + 4*x^11 + 5*x^12 + 2*x^13 + x^14)/((1-x)^2*(1-x^12)) (checked for n <= 100).
%e A?????? a(5) = 64 as in diamond, against 66 at the hexagonal atoms of 4H and 67 in lonsdaleite.
%o A?????? (Python) # coordseq() as in A?????? (entry 2)
%o A?????? print(coordseq('ABCACB', 0, 0, 57))
%Y A?????? Cf. A008253, A008264, A??????(entry 2), A??????(entry 4), A??????(entry 5), A002895.
%K A?????? nonn,easy
%O A?????? 0,2
%A A?????? DICTO, Nov 07 2026
```

(When submitting, paste the full coordseq() function from entry 2 into %o; the editors prefer self-contained programs.)

---

### Entry 4. 6H polytype, cubic-layer atoms bonded to the hexagonal layer

```
%I A??????
%S A?????? 1,4,12,25,43,66,96,129,169,214,264,319,380,445,516,592,673,759,852,948,1051,1159,1272,
%T A?????? 1390,1514,1642,1776,1915,2059,2208,2364,2523,2689,2860,3036,3217,3404,3595,3792,3994,
%U A?????? 4201,4413,4632,4854,5083,5317,5556,5800,6050,6304,6564,6829,7099,7374,7656,7941,8233,8530
%N A?????? Coordination sequence of an atom of a cubic (c) bilayer of the 6H polytype of diamond (6H-SiC network, stacking ABCACB) whose three interlayer bonds go to the neighbouring hexagonal bilayer.
%C A?????? In the period ABCACB the bilayers B, C, C, B (positions 1, 2, 4, 5) are cubic and each lies next to one hexagonal A bilayer. Each atom of a cubic bilayer has its three interlayer bonds either towards that A bilayer (this sequence: the lower atoms of bilayers 1 and 4, the upper atoms of bilayers 2 and 5) or towards the other cubic bilayer (A??????, entry 5).
%C A?????? Although the shells differ, the numbers of closed walks (A002895) and of closed non-backtracking walks (A??????, entry 1) of every length at this atom are those of diamond (DICTO, #102, Theorem 1).
%D A?????? DICTO, Spin Ice and Kagome Magnets on Every Stacking (#74), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23730421.
%D A?????? DICTO, HexOct: The Hexagonality Law, with the Window Law, the Rule of Halves & the Swap Rule (book), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23731359.
%D A?????? M. O'Keeffe, Topological and geometrical characterization of sites in silicon carbide polytypes, Chemistry of Materials 3 (1991), 332-335.
%H A?????? DICTO, <a href="https://doi.org/10.5281/zenodo.23730421">Spin Ice and Kagome Magnets on Every Stacking</a>, Zenodo (2026).
%H A?????? M. O'Keeffe, <a href="https://doi.org/10.1021/cm00014a025">Topological and geometrical characterization of sites in silicon carbide polytypes</a>, Chem. Mater. 3 (1991), 332-335.
%F A?????? Empirical g.f.: (1 + 2*x + 5*x^2 + 5*x^3 + 5*x^4 + 5*x^5 + 7*x^6 + 3*x^7 + 7*x^8 + 5*x^9 + 5*x^10 + 5*x^11 + 5*x^12 + 2*x^13 + x^14)/((1-x)^2*(1-x^12)) (checked for n <= 100).
%e A?????? a(4) = 43, between diamond's 42 and lonsdaleite's 44.
%o A?????? (Python) # coordseq() as in A?????? (entry 2)
%o A?????? print(coordseq('ABCACB', 1, 0, 57))
%Y A?????? Cf. A008253, A008264, A??????(entry 2), A??????(entry 3), A??????(entry 5), A002895.
%K A?????? nonn,easy
%O A?????? 0,2
%A A?????? DICTO, Nov 07 2026
```

---

### Entry 5. 6H polytype, cubic-layer atoms bonded to the other cubic layer

```
%I A??????
%S A?????? 1,4,12,24,43,67,96,130,169,213,264,319,380,445,516,591,673,760,852,949,1051,1158,1272,
%T A?????? 1390,1514,1642,1776,1914,2059,2209,2364,2524,2689,2859,3036,3217,3404,3595,3792,3993,
%U A?????? 4201,4414,4632,4855,5083,5316,5556,5800,6050,6304,6564,6828,7099,7375,7656,7942,8233,8529
%N A?????? Coordination sequence of an atom of a cubic (c) bilayer of the 6H polytype of diamond (6H-SiC network, stacking ABCACB) whose three interlayer bonds go to the neighbouring cubic bilayer.
%C A?????? These are the upper atoms of bilayers 1 and 4 and the lower atoms of bilayers 2 and 5 of the period ABCACB (positions 0..5); the other atoms of these cubic bilayers have A?????? (entry 4), the atoms of the hexagonal A bilayers A?????? (entry 3).
%C A?????? Although the shells differ, the numbers of closed walks (A002895) and of closed non-backtracking walks (A??????, entry 1) of every length at this atom are those of diamond (DICTO, #102, Theorem 1).
%D A?????? DICTO, Spin Ice and Kagome Magnets on Every Stacking (#74), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23730421.
%D A?????? DICTO, HexOct: The Hexagonality Law, with the Window Law, the Rule of Halves & the Swap Rule (book), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23731359.
%D A?????? M. O'Keeffe, Topological and geometrical characterization of sites in silicon carbide polytypes, Chemistry of Materials 3 (1991), 332-335.
%H A?????? DICTO, <a href="https://doi.org/10.5281/zenodo.23730421">Spin Ice and Kagome Magnets on Every Stacking</a>, Zenodo (2026).
%H A?????? M. O'Keeffe, <a href="https://doi.org/10.1021/cm00014a025">Topological and geometrical characterization of sites in silicon carbide polytypes</a>, Chem. Mater. 3 (1991), 332-335.
%F A?????? Empirical g.f.: (1 + 2*x + 5*x^2 + 4*x^3 + 7*x^4 + 5*x^5 + 5*x^6 + 5*x^7 + 5*x^8 + 5*x^9 + 7*x^10 + 4*x^11 + 5*x^12 + 2*x^13 + x^14)/((1-x)^2*(1-x^12)) (checked for n <= 100).
%e A?????? a(3) = 24 as in diamond, while the other atoms of the same bilayer (entry 4) have a(3) = 25.
%o A?????? (Python) # coordseq() as in A?????? (entry 2)
%o A?????? print(coordseq('ABCACB', 1, 1, 57))
%Y A?????? Cf. A008253, A008264, A??????(entry 2), A??????(entry 3), A??????(entry 4), A002895.
%K A?????? nonn,easy
%O A?????? 0,2
%A A?????? DICTO, Nov 07 2026
```

---

### Entry 6. The Fibonacci stacking of close-packed layers as letters A, B, C = 0, 1, 2

```
%I A??????
%S A?????? 0,1,0,2,1,2,0,2,1,0,1,2,0,2,1,2,0,1,0,2,0,1,2,1,0,2,0,1,0,2,1,2,0,1,0,2,0,1,2,1,0,1,2,0,
%T A?????? 2,1,0,1,2,1,0,2,0,1,0,2,1,2,0,1,0,2,0,1,2,1,0,2,0,1,0,2,1,2,0,2,1,0,1,2,0,2,1,2,0,1,0,2,
%U A?????? 1,2,0,2,1,0,1,2,1,0,2,0,1,2,1,0,1,2,0,2,1,2,0,1,0,2,1,2,0,2,1,0,1,2,0,2,1,2,0,1,0,2
%N A?????? Position (A, B, C = 0, 1, 2) of layer n in the Fibonacci stacking of close-packed layers: the layer types (c, h) follow the Fibonacci word, a(0) = 0, a(1) = 1.
%C A?????? A layer is hexagonal (h) if its two neighbours have the same position and cubic (c) otherwise (Jagodzinski). Here layer n >= 1 is h exactly when A003849(n) = 1, i.e., the types follow the Fibonacci word c -> ch, h -> c started from c. Steps between layers are +1 or -1 mod 3; a cubic layer repeats the previous step and a hexagonal layer reverses it.
%C A?????? Convention: first layer A, first step forward (A -> B). The other three choices give the same sequence up to a permutation of 0, 1, 2.
%C A?????? Hexagonal layers never touch and their share is 1/phi^2 (DICTO, #69). The first 16 terms read ABACBCACBABCACBC, the 16-layer periodic approximant of #69.
%F A?????? a(n) = (2*Sum_{k=2..n+1} A085002(k) - n) mod 3, i.e., the step from layer k to layer k+1 is 2*A085002(k+2) - 1.
%e A?????? Layers 0..8 are A, B, A, C, B, C, A, C, B; layer types from layer 1 on: h, c, c, h, c, h, c, c (the Fibonacci word).
%o A?????? (Python)
%o A?????? def fib_stacking(N):   # a(0..N-1)
%o A??????     w = 'c'
%o A??????     while len(w) < N: w = ''.join('ch' if t == 'c' else 'c' for t in w)   # Fibonacci word
%o A??????     a = [0, 1]; s = 1
%o A??????     for k in range(1, N-1):
%o A??????         if w[k] == 'h': s = -s          # a hexagonal layer reverses the step
%o A??????         a.append((a[-1] + s) % 3)
%o A??????     return a[:N]
%o A?????? print(fib_stacking(130))
%D A?????? DICTO, The Hexagonality Law and the Fibonacci Stacking (#69), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23721038.
%D A?????? DICTO, HexOct: The Hexagonality Law, with the Window Law, the Rule of Halves & the Swap Rule (book), Zenodo, 2026, DICTO DOI 10.5281/zenodo.23731359.
%H A?????? DICTO, <a href="https://doi.org/10.5281/zenodo.23721038">The Hexagonality Law and the Fibonacci Stacking</a>, Zenodo (2026).
%Y A?????? Cf. A003849 (Fibonacci word, the layer types), A085002 (the steps), A005614, A000201.
%K A?????? nonn,easy
%O A?????? 0,4
%A A?????? DICTO, Nov 07 2026
```

Checked: the Jagodzinski types recovered from the letters for 390 layers (oeis_checks.py C5); the A085002 formula checked for n < 2000 (assert in the test copy of the program); "layer n is h iff A003849(n) = 1" is the same rule as w[n] = 'h'.

---

### Entry 7 (optional). Closed non-backtracking walks per sphere of fcc

Extension; not yet the subject of a DICTO paper beyond #102 Corollary 3 (lengths 3 to 12 printed there).

```
%I A??????
%S A?????? 0,0,48,264,1680,17016,151872,1401720,13238400,126357120,1221557040,11927724720,
%T A?????? 117462513168,1165493695464,11640248292288,116929064980056,1180626550585152,
%U A?????? 11975554917588624,121975042856240112,1246999597381941864,12791835532462832208,131625892179685049256
%N A?????? Number of closed non-backtracking walks of length n (cyclically non-backtracking, i.e., tailless) starting and ending at a fixed vertex of the face-centered cubic lattice (12 nearest neighbours).
%C A?????? The same numbers hold at every sphere of the hexagonal close packing and of every close-packed stacking (dhcp, ..., periodic or not), DICTO #102 Corollary 3; the corresponding statement for all closed walks (A002899) is Thorpe (1972) for periodic stackings.
%C A?????? a(3) = 48: each vertex lies on 24 triangles (the 24 edges of its cuboctahedron of neighbours), walked in 2 directions.
%D A?????? DICTO, Every Site Hears the Same: the Loop Equality Is a Theorem (#102), Zenodo, 2026 (DOI at release), Corollary 3.
%D A?????? M. F. Thorpe, Random walks in polytype structures, J. Math. Phys. 13 (1972), 294-299.
%H A?????? DICTO, <a href="https://doi.org/10.5281/zenodo.XXXXXXXX">Every Site Hears the Same: the Loop Equality Is a Theorem</a>, Zenodo (2026).
%F A?????? G.f.: 10*x^2/(1-x^2) - 22*x^2/(1+11*x^2) + ((1-11*x^2)/(1+11*x^2))*(F(x/(1+11*x^2)) - 1), where F(x) = Sum_{k>=0} A002899(k)*x^k (Ihara-Bass formula for a 12-regular net).
%e A?????? a(3) = 48, a(4) = 264.
%o A?????? (Python)
%o A?????? from math import comb
%o A?????? from fractions import Fraction
%o A?????? def domb(n):  # A002895
%o A??????     return sum(comb(n,k)**2*comb(2*k,k)*comb(2*n-2*k,n-k) for k in range(n+1))
%o A?????? def fcc(n):   # A002899
%o A??????     return sum(comb(n,k)*(-4)**(n-k)*domb(k) for k in range(n+1))
%o A?????? def loops(W, q):  # Ihara-Bass per vertex of a (q+1)-regular net; W[i] = closed i-step walks
%o A??????     M = len(W)-1; c = [Fraction(0)]*(M+1)
%o A??????     for k in range(1, M//2+1): c[2*k] += Fraction(q-1, 2*k)
%o A??????     for j in range(1, M+1):
%o A??????         for i in range(j+1):
%o A??????             if 2*j-i <= M: c[2*j-i] += Fraction(comb(j,i)*W[i]*(-q)**(j-i), j)
%o A??????     return [int(m*c[m]) for m in range(1, M+1)]   # lengths 1..M
%o A?????? print(loops([fcc(i) for i in range(23)], 11))
%Y A?????? Cf. A002899, A002895, A??????(entry 1, diamond analog), A293237.
%K A?????? nonn,walk
%O A?????? 1,3
%A A?????? DICTO, Nov 07 2026
```

Checked: lengths 3..24 equal oeis_checks.py C1b (fcc closed walks by direct propagation, then Ihara-Bass); the A002899 sum formula used in the program is David Broadhurst's PARI program on A002899; the g.f. form expanded and compared for lengths 1..40.

---

## B. Comments for existing entries

Add with "edit" on each entry. Signature at the end: "- _DICTO_, Nov 07 2026" (or the registered real name).

**A002895** (Domb numbers; wait for #102's DOI):
```
%C A002895 Also the number of closed 2n-step walks from any atom of lonsdaleite (A008264) and of the tetrahedral network of every close-packed stacking (polytypes 4H, 6H, 9R, ..., periodic or not), although the coordination sequences of these atoms differ. For periodic polytypes this is Thorpe (1972); for every atom of every stacking, including aperiodic ones, see DICTO (2026, #102, Lemma 2). Via the Ihara-Bass formula the same holds for the closed non-backtracking walks A??????.
%D A002895 M. F. Thorpe, Random walks in polytype structures, J. Math. Phys. 13 (1972), 294-299.
%H A002895 DICTO, <a href="https://doi.org/10.5281/zenodo.XXXXXXXX">Every Site Hears the Same: the Loop Equality Is a Theorem</a>, Zenodo (2026).
%Y A002895 Cf. A008264, A??????(entry 1).
```

**A002899** (fcc polygons; wait for #102's DOI):
```
%C A002899 Also the number of closed n-step walks from any sphere of the hexagonal close packing and of every close-packed stacking of equal spheres (dhcp, ..., periodic or not). For periodic stackings this is Thorpe (1972); every sphere of every stacking: DICTO (2026, #102, Corollary 3). Compare A293237 (equal escape probabilities of fcc and hcp).
%D A002899 M. F. Thorpe, Random walks in polytype structures, J. Math. Phys. 13 (1972), 294-299.
%H A002899 DICTO, <a href="https://doi.org/10.5281/zenodo.XXXXXXXX">Every Site Hears the Same: the Loop Equality Is a Theorem</a>, Zenodo (2026).
%Y A002899 Cf. A293237, A??????(entry 7, if submitted).
```

**A008264** (lonsdaleite coordination sequence):
```
%C A008264 Empirically also the coordination sequence of every atom of the cubic (A) bilayers of the 4H polytype (stacking ABAC, network of 4H-SiC with all atoms alike); checked for n <= 100. The atoms of the hexagonal bilayers of 4H have A??????(entry 2). - _DICTO_, Nov 07 2026
%H A008264 DICTO, <a href="https://doi.org/10.5281/zenodo.23730421">Spin Ice and Kagome Magnets on Every Stacking</a>, Zenodo (2026).
%Y A008264 Cf. A??????(entries 2-5).
```

**A085002** (floor(n*phi) mod 2):
```
%C A085002 2*a(n+2) - 1, n >= 0, is the sequence of steps (+1 forward A -> B -> C -> A, -1 backward) of the Fibonacci stacking of close-packed layers, whose layer types follow the Fibonacci word (A003849); its partial sums mod 3 give the layer positions A??????(entry 6). Checked for n < 2000; see DICTO (#69). - _DICTO_, Nov 07 2026
%H A085002 DICTO, <a href="https://doi.org/10.5281/zenodo.23721038">The Hexagonality Law and the Fibonacci Stacking</a>, Zenodo (2026).
%Y A085002 Cf. A003849, A??????(entry 6).
```

---

## C. Open points before submitting

1. **Name.** The OEIS asks for real names on accounts and in %A lines; "DICTO" as the author name may be questioned by the editors. DICTO decides how to register.
2. **O'Keeffe 1991** (Chem. Mater. 3, 332-335) characterized the sites of SiC polytypes topologically and is cited on A008264 for a formula; it very probably lists the first coordination-sequence terms of the 4H and 6H sites. It was not read (paywalled; Crossref has no abstract). Entries 2-5 credit it in %D; if the paper prints these sequences, the %N/%C should say "computed independently, extending O'Keeffe (1991)". The OEIS has no hits for any of the four sequences (searched 7 November 2026).
3. **The 4H "c" atoms equal lonsdaleite** (A008264) to n = 100 with the same g.f.: computed, not proved; therefore "Empirically" in the A008264 comment. The g.f.s of entries 2-5 are fitted (Berlekamp-Massey, order <= 14 from 100 terms) and verified to n = 100; rationality is known in general for periodic nets, the exact forms are marked "Empirical".
4. **Site names.** The script output labelled the sites "4H B" and "6H A, B atom 0, B atom 1". The entries name them by structure instead (hexagonal bilayers of 4H, which include both B and C; hexagonal A bilayers of 6H; the two halves of the cubic bilayers of 6H by the direction of their three interlayer bonds), since the letter alone does not fix the site.
5. **#102 DOI.** Replace zenodo.XXXXXXXX in entries 1, 7 and the A002895/A002899 comments once #102 is released.
