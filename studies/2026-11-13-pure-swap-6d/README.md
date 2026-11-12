# The pure swap in six dimensions (13 Nov 2026; lead 3 of studies/2026-11-13-swaps-and-fixed-points)

**Conclusion (13 Nov 2026): the self-reverse class i = 3 of the 6-permutohedron (2416 corners) balances exactly, class by class (10 pairs, 20/20 up to 272/272), in every direction and on every tilted copy tested; but it is not an exchange of a pair of contacts: it trades one 3-face (three facets meeting) for another, and no contact is lost or made. The balance is PROVED for every simple polytope whose facets are coloured one of each kind at every corner (Theorem 2); it is a known identity (Stanley's balanced Dehn–Sommerville relations, the descent-set symmetry), not a new law.**

Script `scripts/pure_swap.py` (logs `data/pure-swap-pilot.log`, `data/pure-swap-full.log`; data `data/pure-swap-pilot.json`,
`data/pure-swap-full.json`). Compute node through the job gate (jobs pure6-pilot, 11 s, 44 checks; pure6, 96 s, 468 checks), one
process, FINAL ok both. **Exact arithmetic throughout** (rationals); no floating point decides anything.

## 1. Setting and words
The permutohedron of order n (dimension d = n − 1) has the orderings of 1..n as its corners and the proper subsets S of {1..n} as its facets;
the **type** of a facet is |S| (= the node of its Wythoff type, 1..d). At each corner there is exactly one facet of each type (the
prefix sets of the ordering), and edge k is the edge opposite the facet of type k. Sweep by a generic height u; D = the down edges at
a corner, written as the set of the types opposite them; U = the up edges; i = |D|. The face spanned by an edge set E lies in the
facets opposite the edges not in E; it is **lost** at the corner (its top) iff E ⊆ D and **made** (its bottom) iff E ⊆ U. The **event
class** is D; its **reverse** is U (sweeping by −u). For d = 6 the class i = 3 is the only self-reverse value of i (#104 Theorem 1:
it exists only in even dimension).

## 2. Results

**Observation 1 (what the i = 3 event exchanges; computed and immediate).** At an i = 3 corner of a simple 6-polytope the faces lost
are 3 edges, 3 two-faces and ONE 3-face; the faces made are the same in number. No 4-face (a **contact**, the meeting of two facets)
and no facet is lost or made: a contact is lost only where i ≥ 4 and made only where i ≤ 2. So the six-dimensional pure swap is not
an exchange of a pair of contacts: **it trades one 3-face, where three facets meet (types U), for another (types D)**. In 4D the same
rule gives the scutoid swap (i = 2: one contact, the meeting of two cells, for another); in d dimensions the self-reverse event
trades a d/2-face (the meeting of d/2 facets) for another.

**The ledger of the regular 6-permutohedron (exact; identical in all 92 six-dimensional sweeps: 12 regular, 80 tilted).** h-vector
(1, 120, 1191, 2416, 1191, 120, 1) (Eulerian numbers). The i = 3 class, lost 3-face on the facets of types U, made on types D:

| D (made on) | corners | U = reverse (made on) | corners |
|---|---|---|---|
| 1 2 3 | 20 | 4 5 6 | 20 |
| 1 2 4 | 90 | 3 5 6 | 90 |
| 1 2 5 | 111 | 3 4 6 | 111 |
| 1 2 6 | 55 | 3 4 5 | 55 |
| 1 3 4 | 111 | 2 5 6 | 111 |
| 1 3 5 | 272 | 2 4 6 | 272 |
| 1 3 6 | 181 | 2 4 5 | 181 |
| 1 4 5 | 132 | 2 3 6 | 132 |
| 1 4 6 | 181 | 2 3 5 | 181 |
| 1 5 6 | 55 | 2 3 4 | 55 |

Total 2 × 1208 = 2416. **Balanced: every class equals its reverse.** Each count is β₇(D), the number of orderings of 7 with descent
set D (for u in the fundamental chamber the down edges at an ordering are its descents; checked: the 64 class counts are exactly the
64 descent-set numbers). Every other i balances too (i = 2 against i = 4, 1191 each, class by class).

**Theorem 2 (balance for every properly coloured simple polytope; PROVED).** Let P be a simple d-polytope whose facets carry colours
1..d so that every corner meets one facet of each colour. For a generic height u let N_u(S) be the number of corners whose down
edges are opposite the facets of colour set S. Then N_u(S) = N_u(complement of S) for every S, and N_u(S) does not depend on u.
*Proof.* Each face G of P has exactly one lowest corner v; at v, G is spanned by the edges at v lying in G, which all go up; so G is the
intersection of a set T of facets at v containing every facet opposite a down edge. With one facet of each colour at v, the faces
with lowest corner v and colour set T number 1 if colour(D at v) ⊆ T and 0 otherwise. Hence f_T (faces of P lying exactly in facets
of colours T) = Σ over S ⊆ T of N_u(S), and by inversion N_u(S) = Σ over T ⊆ S of (−1)^|S − T| f_T, the same for every u. Sweeping
by −u turns D into U: N_{−u}(S) = N_u(complement of S). ∎
This is Stanley's symmetry of the flag h-vector of a balanced simplicial sphere (the polar of P is one), in its sweep form; for the
permutohedron it is the classical β_n(S) = β_n(complement of S) (reverse the ordering). For the regular 6-permutohedron it was also
already implied by rosette-balance Lemma 1 and Theorem 2 (every Wythoff polytope, any dimension). What the theorem adds: the
balance needs no symmetry, only the colouring, and the counts are the same on every polytope with the same coloured face lattice.

**Tilted 6-permutohedra (the test that could have failed; exact).** Facet normals 1_S tilted by independent random rationals
(8 copies at ±1/400 per entry, 4 at ±1/100; 4D: 10 copies at ±1/200): corners re-solved exactly, every corner checked tight on exactly
its 6 facets and strictly inside the other 120 (same face lattice, simple), each swap-neighbour checked to lie on the edge line.
These polytopes have no symmetry and their edges are no longer parallel to roots (tilting only the offsets b_S would keep the edges
parallel to roots and the ledger trivially identical, so offsets were not used). Result: on all 12 tilted 6D copies × 4 to 8 directions
and all 10 tilted 4D copies × 10 directions, every class balances and the class counts equal the regular ones exactly, as Theorem 2
predicts.

## 3. Controls (468 checks, all ok)
SHOULD PASS (and did): the Eulerian h-vectors (1, 26, 66, 26, 1) and (1, 120, 1191, 2416, 1191, 120, 1) in every sweep; the 64 class
counts = descent-set numbers β₇(D); the 4D permutohedron swaps 6 / 16 / 11 each way (rosette-balance and #108); the i = 3 class has
2416 corners (swaps study K8); i = 2 and i = 4 both 1191; ledger identical in every direction; the moved 16-cell's heights
−30, −4, −3, −2, 1, 2, 12, 31 (rosette-balance Theorem 4).
SHOULD FAIL (and did): (a) the same tilted polytopes with facet labels drawn at random (no longer one of each kind per corner): kinds
X → Y against Y → X unbalanced (4D: 54 unbalanced kinds, pilot 62; 6D: 2341 and 2268, pilot 2266), so Theorem 2's colouring hypothesis is needed;
(b) the i = 2 classes paired with a wrong partner (types shifted by one): 12 mismatches; (c) the moved 16-cell (non-simple, rosette
tissue): 2 corners with one edge down against 1 with five down, unbalanced.

## 4. Answers to the lead
"Sweep it (5040 corners) and classify the i = 3 events: is each one exchange of a pair of contacts, and does the balance law
X → Y = Y → X hold there?" — Classified: 20 classes in 10 reverse pairs (table). Not an exchange of contacts: each i = 3 event
trades one 3-face (three facets meeting) for another; contacts are untouched. Balance: yes, exactly, in every class; proved for every
properly coloured simple polytope (Theorem 2), so it holds with or without symmetry; known in substance (Stanley 1979; descent sets).

## LEADS
1. Uncoloured simple polytopes: #108 Theorem 1 balances 4D contacts by kinds for every simple 4-polytope with any typing. Does a kind
   balance (multisets of facet types) hold for simple 6-polytopes whose typing is not a proper colouring but comes from a Wythoff
   construction with repeated types at a corner (e.g. A6 seeds with unringed nodes that stay simple)? The random-label control says
   it fails for arbitrary labels; the Wythoff typings sit in between.
2. The 3-face trade in pictures: the i = 3 corner of class 135 ↔ 246 (272 corners each, the largest) as a 3D slice, the six-dimensional
   counterpart of the scutoid.
3. 8D: the i = 4 class of the 8-permutohedron (A(9,4) = 156190 corners): same theorem; only a figure or a count is left.

## Sources checked
studies/2026-11-13-swaps-and-fixed-points (README rows 4 and 5, LEAD 3, K8); studies/2026-11-13-rosette-balance (README: Lemma 1,
Theorem 2, Proposition 3, Theorem 4, the 4D permutohedron control; rosette_balance.py function list only, not run: this study uses
its own engine); studies/2026-11-13-near-but-never-on (README, for the form). The #104 and #108 scripts were not run; their counts
enter only as controls. Classical results named: Eulerian numbers; descent-set numbers β_n(S) and their complement symmetry
(MacMahon); the sweep proof of the Dehn–Sommerville relations (h-vector of a simple polytope); Stanley, "Balanced Cohen–Macaulay
complexes", Trans. Amer. Math. Soc. 249 (1979) (flag h-vector of balanced spheres, symmetric). The reference library was not searched.

## Ledger line (for the parent session)
2026-11-13, question "pure swap in 6D (i = 3 class of the 6-permutohedron)": classified (3-face trade, no contact), balanced 10/10
pairs, PROVED for properly coloured simple polytopes (known: Stanley 1979), tilted copies agree; status SETTLED.

DICTO · dictospheres.com
