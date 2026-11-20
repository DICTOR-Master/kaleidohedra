"""Part 2: the five cell sets, the tip 600-cell and the caps, put against the earlier 600-cell work
(#63, #65, #76, #104/#107, #109, #110, Alicia ch. 9-11).
Exact Q(sqrt5) arithmetic and exact quaternion products, reusing dehn600.py (imported; its checks rerun silently).
After the import every step is exact: Q(sqrt5) numbers, or integer index tables built from exact products."""
import io, contextlib, time
t0 = time.time()
with contextlib.redirect_stdout(io.StringIO()):
    import dehn600 as D
from itertools import combinations, permutations
from fractions import Fraction as F
from collections import Counter
import sympy as sp

Q5, V, C, cen, dot, idx, qmul, tri_cells, N = D.Q5, D.V, D.C, D.cen, D.dot, D.idx, D.qmul, D.tri_cells, D.N
phi = D.phi
ok = True
def check(name, c):
    global ok; ok &= bool(c); print(("PASS " if c else "FAIL ") + name)
def info(*a): print("   ", *a)
def pos(q):  # exact sign of a + b sqrt5 > 0
    a, b = q.a, q.b
    if a >= 0 and b >= 0: return a > 0 or b > 0
    if a <= 0 and b <= 0: return False
    return a*a > 5*b*b if a > 0 else 5*b*b > a*a
Z0 = Q5(0)
conj = lambda v: (v[0], -v[1], -v[2], -v[3])
scal = lambda s, v: tuple(s*x for x in v)
ONE = idx[(Q5(1), Z0, Z0, Z0)]
M = [[idx[qmul(V[i], V[j])] for j in range(N)] for i in range(N)]      # exact multiplication table of 2I
CJ = [idx[conj(v)] for v in V]
Cset = {frozenset(c): k for k, c in enumerate(C)}
def act(l, r, k):   # rotation x -> V[l] x conj(V[r]) applied to cell k
    return Cset[frozenset(M[l][M[i][CJ[r]]] for i in C[k])]
cc = dot(cen[0], cen[0])                       # |centroid|^2, the same for all 600
cenidx = {c: k for k, c in enumerate(cen)}
check("all 600 centroids have the same norm^2 cc = (%s)" % cc, all(dot(c, c) == cc for c in cen))

# ---------------------------------------------------------------- Q1: the five sets
Lsets = [set(o) for o in D.orbits]
Rsets = []; seen = set()
for k in range(600):
    if k in seen: continue
    o = {act(ONE, CJ[g], k) for g in range(N)}   # x -> x V[g]
    Rsets.append(o); seen |= o
labL = {k: i for i, s in enumerate(Lsets) for k in s}
labR = {k: j for j, s in enumerate(Rsets) for k in s}
check("left multiplication: 5 sets of 120 cells; right multiplication: 5 sets of 120; each cell in one of each",
      sorted(map(len, Lsets)) == [120]*5 and sorted(map(len, Rsets)) == [120]*5 and len(labL) == 600 == len(labR))
LR = Counter((labL[k], labR[k]) for k in range(600))
check("every left set meets every right set in exactly 24 cells", len(LR) == 25 and set(LR.values()) == {24})
check("the ten sets are distinct (no left set is a right set)", all(Lsets[i] != Rsets[j] for i in range(5) for j in range(5)))

# the centres form the 120-cell of #65 (corners = cell centres, joined when the cells share a triangle)
nbr = {k: set() for k in range(600)}
for t, (x, y) in tri_cells.items(): nbr[x].add(y); nbr[y].add(x)
ip_tri = {dot(cen[x], cen[y]) for (x, y) in tri_cells.values()}
maxip = max((dot(cen[0], cen[k]) for k in range(1, 600)), key=lambda q: q.f())
near0 = {k for k in range(1, 600) if dot(cen[0], cen[k]) == maxip}
check("the 600 centres: nearest neighbours are exactly the cells sharing a triangle (4 each, 1200 edges): the 120-cell of #65",
      len(ip_tri) == 1 and ip_tri == {maxip} and near0 == nbr[0] and all(len(s) == 4 for s in nbr.values()))
vset = {dot(V[ONE], V[j]) for j in range(N) if j != ONE}
def gram_set(S):
    S = sorted(S); a = S[0]
    return {dot(cen[a], cen[b])/cc for b in S if b != a}
def is600(S):
    if gram_set(S) != vset: return False
    return all(sum(1 for b in S if dot(cen[a], cen[b])/cc == phi*Q5(F(1, 2))) == 12 for a in S)
check("each of the ten sets has its 120 centres on a regular 600-cell (Gram values and 12 neighbours at cos 36 deg)",
      all(is600(S) for S in Lsets + Rsets))
g24 = {Q5(-1), Q5(F(1, 2)), Q5(F(-1, 2)), Q5(0)}
check("each left set meets each right set in 24 centres forming a 24-cell (Gram values {-1, +-1/2, 0})",
      all(gram_set(Lsets[i] & Rsets[j]) == g24 for i in range(5) for j in range(5)))
info("so the ten sets are Coxeter's compound of ten 600-cells in the 120-cell of the centres, two states of five, as in #110 Theorem B(a)")

# right stabilisers of the left sets, left stabilisers of the right sets
def rstab(S): return frozenset(r for r in range(N) if {act(ONE, CJ[r], k) for k in S} == S)
def lstab(S): return frozenset(l for l in range(N) if {act(l, ONE, k) for k in S} == S)
RS = [rstab(S) for S in Lsets]; LS = [lstab(S) for S in Rsets]
def is2T(G):
    G = set(G)
    closed = all(M[a][b] in G for a in G for b in G)
    re = Counter(V[g][0] for g in G)
    return len(G) == 24 and closed and re == Counter({Q5(1): 1, Q5(-1): 1, Q5(0): 6, Q5(F(1, 2)): 8, Q5(F(-1, 2)): 8})
check("the right symmetries of each left set form a binary tetrahedral group 2T (order 24, real parts 1,-1,0^6,(1/2)^8,(-1/2)^8)",
      all(is2T(G) for G in RS))
check("the five left sets have five different 2T's; the right sets have the same five as left stabilisers",
      len(set(RS)) == 5 and set(RS) == set(LS))
check("the five 2T's are conjugate in 2I (g T g^-1 runs over all five)",
      {frozenset(M[M[g][t]][CJ[g]] for t in RS[0]) for g in range(N)} == set(RS))
pair = {i: LS.index(RS[i]) for i in range(5)}
info("left set i and right set j share a 2T for (i,j) =", sorted(pair.items()), "; they still meet in 24 cells, like every pair")
# symmetry group of a left set: x -> l x conj(r), l in 2I, r in its 2T: 120*24/2 = 1440 rotations
check("rotations x -> l x r^-1 with l in 2I and r in the set's 2T keep the set: 120*24/2 = 1440 = the study's count, so the group is +-[I x T] (Conway-Smith)",
      all({act(l, r, k) for k in Lsets[0]} == Lsets[0] for l in range(0, N, 11) for r in RS[0]) and 120*24//2 == 1440)
# coset reading: fix a centre c0 (cell k0 in left set 0); the centre c0 * conj(r) lies in a left set that depends only on r T0
k0 = sorted(Lsets[0])[0]; c0 = cen[k0]
T0 = RS[labL[k0]]
lab_of_r = [labL[cenidx[qmul(c0, conj(V[r]))]] for r in range(N)]
cos_T0 = {frozenset(M[r][t] for t in T0) for r in range(N)}
check("the left set of the centre c0 r^-1 depends exactly on the coset r T0: the five sets are the five cosets of 2T in 2I",
      all(len({lab_of_r[r] for r in cs}) == 1 for cs in cos_T0) and len({lab_of_r[next(iter(cs))] for cs in cos_T0}) == 5 and len(cos_T0) == 5)
# the 25 24-cells and the 10 splits (#110 Theorem B'(f))
splitsL = [frozenset(frozenset(M[g][t] for t in T) for g in range(N)) for T in RS]   # left cosets g T
splitsR = [frozenset(frozenset(M[t][g] for t in T) for g in range(N)) for T in RS]   # right cosets T g
all24 = Counter(c for s in splitsL + splitsR for c in s)
def vgram(S):
    S = sorted(S); a = S[0]; return {dot(V[a], V[b]) for b in S if b != a}
check("the 2T cosets give 10 splits of the 600-cell into 5 disjoint 24-cells, 25 different 24-cells, each in exactly 2 splits (one left, one right): #110 B'(f)",
      all(len(s) == 5 and len(set().union(*s)) == 120 for s in splitsL + splitsR) and len(all24) == 25 and set(all24.values()) == {2}
      and all(vgram(c) == g24 | {Q5(F(1, 2))} for c in all24) and all(len(set(s) & set(t)) == 1 for s in splitsL for t in splitsR))
# how a capped cell meets a split: the coset it misses
def missed(k, split):
    hit = [sum(1 for v in C[k] if v in cs) for cs in split]
    return hit.count(1) == 4 and hit.count(0) == 1
check("a capped cell has its 4 corners in 4 different 24-cells of every split, missing one (adjacent corners are never in one 24-cell)",
      all(missed(k, list(spl)) for k in range(600) for spl in splitsL + splitsR))

# ---------------------------------------------------------------- Q1/Q4: the 5-cell group S5 (A, B, C3)
def refl(a):   # reflection in the root a (a unit vertex): x -> x - 2(x.a)a, as a permutation of V
    return tuple(idx[tuple(x - Q5(2)*dot(V[j], V[a])*y for x, y in zip(V[j], V[a]))] for j in range(N))
a1 = ONE
cand = lambda S, cond: [b for b in range(N) if cond(b)]
h = Q5(F(-1, 2))
A4roots = None
for a2 in range(N):
    if dot(V[a1], V[a2]) != h: continue
    for a3 in range(N):
        if dot(V[a2], V[a3]) != h or dot(V[a1], V[a3]) != Z0: continue
        for a4 in range(N):
            if dot(V[a3], V[a4]) == h and dot(V[a1], V[a4]) == Z0 and dot(V[a2], V[a4]) == Z0:
                A4roots = (a1, a2, a3, a4); break
        if A4roots: break
    if A4roots: break
gens = [refl(a) for a in A4roots]
ident = tuple(range(N))
comp = lambda p, q: tuple(p[q[j]] for j in range(N))   # p after q
G = {ident: 0}; frontier = [ident]
while frontier:
    nf = []
    for g in frontier:
        for s in gens:
            x = comp(s, g)
            if x not in G: G[x] = G[g] ^ 1; nf.append(x)
    frontier = nf
check("four roots of the 600-cell at 120/90 degrees (an A4 diagram) generate the 5-cell's group S5: 120 elements", len(G) == 120)
orbV = []; seen = set()
for j in range(N):
    if j in seen: continue
    o = {g[j] for g in G}; orbV.append(o); seen |= o
check("S5 splits the 120 corners into orbits 20,20,20,30,30 (Koca et al.)", sorted(map(len, orbV)) == [20, 20, 20, 30, 30])
C3 = next(o for o in orbV if a1 in o)
# identify A by its Gram multiset against #110's A: permutations of (phi^2,phi^2,phi^2,phi,0), centred, radius phi*sqrt2
p2 = phi*phi
Apts = set(permutations([p2, p2, p2, phi, Q5(0)])); mA = sum((x for x in next(iter(Apts))), Q5(0))/Q5(5)
Apts = [tuple(x - mA for x in p) for p in Apts]
d5 = lambda u, w: sum((x*y for x, y in zip(u, w)), Q5(0))
rA2 = d5(Apts[0], Apts[0])
gramA110 = Counter(d5(Apts[0], q)/rA2 for q in Apts)
twenty = [o for o in orbV if len(o) == 20 and o is not C3]
gram_q = lambda o: Counter(dot(V[min(o)], V[j]) for j in o)
check("#110's A (perms of (phi^2,phi^2,phi^2,phi,0)) has the same Gram values as the two non-root 20-orbits (A and -A); not as C3",
      all(gram_q(o) == gramA110 for o in twenty) and gram_q(C3) != gramA110 and rA2 == Q5(2)*p2)
Aset = twenty[0]; mAset = twenty[1]
check("-A is the antipode of A", {idx[scal(Q5(-1), V[j])] for j in Aset} == mAset)
gcell = lambda g, k: Cset[frozenset(g[v] for v in C[k])]
sets10 = [frozenset(S) for S in Lsets] + [frozenset(S) for S in Rsets]
def set_image(g, S): return frozenset(gcell(g, k) for k in S)
perm10 = {g: tuple(sets10.index(set_image(g, S)) for S in sets10) for g in G}
check("every element of S5 maps each of the ten sets onto one of the ten", all(len(set(p)) == 10 for p in perm10.values()))
check("rotations (even) keep left sets left; odd elements swap left and right sets",
      all((all(p[i] < 5 for i in range(5)) if G[g] == 0 else all(p[i] >= 5 for i in range(5))) for g, p in perm10.items()))
evenperms = {tuple(p[:5]) for g, p in perm10.items() if G[g] == 0}
check("the 60 rotations of S5 act on the five left sets as the full alternating group A5 (faithful, transitive)", len(evenperms) == 60)
stabL = [[g for g in G if perm10[g][i] == i] for i in range(5)]
check("S5 meets the symmetry group of each left set in exactly 12 rotations (an A4), no reflections: S5 is not inside it, nor it in S5",
      all(len(s) == 12 and all(G[g] == 0 for g in s) for s in stabL))
fixed = [[k for k in range(600) if all(gcell(g, k) == k for g in s)] for s in stabL]
Atet = [k for k in range(600) if all(v in Aset for v in C[k])]; mAtet = [k for k in range(600) if all(v in mAset for v in C[k])]
check("A has exactly 5 tetrahedral cells that are cells of the 600-cell, and so does -A", len(Atet) == 5 and len(mAtet) == 5)
check("the A4 fixing left set i fixes exactly 2 cells: one tetrahedron of A and the opposite one of -A, both in left set i",
      all(len(f) == 2 and len([k for k in f if k in Atet]) == 1 and len([k for k in f if k in mAtet]) == 1 and all(labL[k] == i for k in f)
          for i, f in enumerate(fixed)))
check("A's five tetrahedra lie one in each left set and one in each right set (and the same for -A)",
      sorted(labL[k] for k in Atet) == list(range(5)) and sorted(labR[k] for k in Atet) == list(range(5))
      and sorted(labL[k] for k in mAtet) == list(range(5)) and sorted(labR[k] for k in mAtet) == list(range(5)))
# the axis of A's tetrahedron k is the normal of C3's cross wall "coordinate k = mean": 12 of C3's 20 corners on it
check("the centre axis of each such tetrahedron is a cross wall normal carrying 12 of C3's 20 corners (C3's walls x_k = mean, #110 Table 1)",
      all(sum(1 for v in C3 if dot(cen[k], V[v]) == Z0) == 12 for k in Atet))
# all 120 A copies in the 600-cell (images of A's 5 tetrahedra under the 7200 rotations)
Acopies = set()
base = frozenset(Atet)
for l in range(N):
    for r in range(N):
        Acopies.add(frozenset(act(l, r, k) for k in base))
check("the 120 A copies of the 600-cell (A and -A for its 60 S5's) have 600 tetrahedra: every cell exactly once (dual of #110 B'(f))",
      len(Acopies) == 120 and Counter(k for s in Acopies for k in s) == Counter({k: 1 for k in range(600)}))
check("every one of the 120 A copies takes one tetrahedron from each left set and one from each right set",
      all(sorted(labL[k] for k in s) == list(range(5)) and sorted(labR[k] for k in s) == list(range(5)) for s in Acopies))
info("so each A copy is a transversal of both states; the 24 cells of a left-right meeting are the tetrahedra of 24 A copies")

# ---------------------------------------------------------------- Q2: the tip 600-cell
c = cen[k0]
cos2 = max((cen[k][0]*cen[k][0]/cc for k in Lsets[0]), key=lambda q: q.f())
info("tip 600-cell = sqrt2 * (2I c)/|c| = sqrt2 * P * c^ : P turned by right multiplication by a unit quaternion; smallest turn cos^2 =", cos2, "=", round(cos2.f(), 6))
check("the unit tip 600-cell is P * c^ (right multiplication), and NOT u * P for any u: c^-1 2I c is not 2I",
      {cenidx[qmul(V[g], c)] for g in range(N)} == Lsets[0] and any(scal(Q5(1)/cc, qmul(qmul(conj(c), V[g]), c)) not in idx for g in range(N)))
# the tip 600-cell's own cell centres: c' c  (c' in the centres), unit after division by cc
Zc = {scal(Q5(1)/cc, qmul(cp, c)) for cp in cen}
check("the cell centres of the tip 600-cell, at unit radius, are 600 points that contain all 120 corners of P: P is inscribed in the tip 600-cell's dual 120-cell",
      len(Zc) == 600 and all(dot(z, z) == 1 for z in Zc) and all(v in Zc for v in V))
duals = []
for S in Lsets:
    cs = cen[sorted(S)[0]]; duals.append(frozenset(scal(Q5(1)/cc, qmul(cp, cs)) for cp in cen))
for S in Rsets:
    cs = cen[sorted(S)[0]]; duals.append(frozenset(scal(Q5(1)/cc, qmul(cs, cp)) for cp in cen))
check("the ten tip 600-cells (5 left choices, 5 mirror choices) have ten different dual 120-cells, each holding P as an inscribed 600-cell",
      len(set(duals)) == 10 and all(all(v in Z for v in V) for Z in duals))
check("in each, P is a left orbit (left choices) or a right orbit (mirror choices) of 2I: one state or the other",
      all(all(scal(Q5(1), qmul(V[g], z)) in Z for g in range(0, N, 7) for z in list(Z)[:40]) for Z in duals[:5])
      and all(all(qmul(z, V[g]) in Z for g in range(0, N, 7) for z in list(Z)[:40]) for Z in duals[5:]))
info("count: a 600-cell lies in exactly 10 of the 120-cells of its size (both groups have order 14400; #110 B(a) read the other way), so these are all of them")
inr2 = cc/Q5(16)
check("P lies strictly inside the tip 600-cell (P's radius 1 < tip inradius sqrt2 * r_in, r_in^2 = cc/16): the hull of the capped solid is the tip 600-cell",
      pos(Q5(2)*inr2 - Q5(1)))
s5 = sp.sqrt(5); ph = (1+s5)/2
check("volume of the capped solid / volume of its hull = 5 sqrt5 phi^2 / (4 * 25/4 phi^3) = 1/(sqrt5 phi)",
      sp.simplify(5*s5*ph**2/(25*ph**3) - 1/(s5*ph)) == 0)
info("ratio = %.6f" % float(1/(s5*ph)))

# ---------------------------------------------------------------- Q3: walls
def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
def normal(p, q, r):
    rows = [p, q, r]; n = []
    for col in range(4):
        m = [[row[j] for j in range(4) if j != col] for row in rows]
        n.append(det3(m) * (1 if col % 2 == 0 else -1))
    return tuple(n)
def canon(n):
    f = next(x for x in n if not (x == Z0)); return tuple(x/f for x in n)
MIR = {canon(v) for v in V}; CROSS = {canon(x) for x in cen}
check("60 mirror normals (corners) and 300 cross-wall normals (cell centres), no overlap", len(MIR) == 60 and len(CROSS) == 300 and not (MIR & CROSS))
S0 = Lsets[0]
plates = Counter(); plate_ridges = {}
def addr(key, ridge):
    plates[key] += 1; plate_ridges.setdefault(key, []).append(ridge)
for t in tri_cells:
    addr(canon(normal(V[t[0]], V[t[1]], V[t[2]])), ('old', t))
side_ok = True; pent_ok = True
for k in S0:
    cell = C[k]
    for u, v in combinations(cell, 2):
        w, x = [z for z in cell if z not in (u, v)]
        n = canon(normal(cen[k], V[u], V[v]))
        addr(n, ('side', k, u, v))
        ewx = tuple(a - b for a, b in zip(V[w], V[x]))
        side_ok &= (n == canon(ewx))
        # pentagon of the 120-cell dual to edge wx: centres of the 5 cells round wx, all on this plate
        ring = [kk for kk in range(600) if w in C[kk] and x in C[kk]]
        pent_ok &= len(ring) == 5 and k in ring and all(dot(cen[kk], ewx) == Z0 for kk in ring)
check("every ridge plate of the capped solid (1200 old triangles, 720 cap sides) is one of the 60 mirrors; none is a cross wall",
      set(plates) <= MIR and len(set(plates)) == 60)
check("each cap side triangle (tip, u, v) lies on the mirror perpendicular to the opposite edge wx of its cell", side_ok)
check("that mirror also carries the 120-cell pentagon dual to wx (#107 Cor. 2), and the tip lies on the ray through one of its corners", pent_ok)
per = Counter((key, r[0]) for key, rs in plate_ridges.items() for r in rs)
check("each mirror carries 20 old triangles and 12 cap sides: its 12 pentagons (#107) and its 12 cap sides pair off one to one",
      {per[(m, 'old')] for m in MIR} == {20} and {per[(m, 'side')] for m in MIR} == {12})
neg = lambda v: tuple(-x for x in v)
def rpts(r):
    if r[0] == 'old': return frozenset(V[i] for i in r[1])
    k, u, v = r[1], r[2], r[3]; return frozenset([cen[k], V[u], V[v]])
full = all({frozenset(neg(p) for p in rpts(r)) for r in rs} == {rpts(r) for r in rs} for rs in plate_ridges.values())
check("every plate carries each ridge together with its opposite (the solid is centrally symmetric): heart kind (#110 Lemma 1)", full)
capok = True
for k in S0:
    ps = {canon(normal(V[a], V[b], V[d])) for a, b, d in combinations(C[k], 3)} | {canon(normal(cen[k], V[u], V[v])) for u, v in combinations(C[k], 2)}
    capok &= ps <= MIR and len(ps) == 10
check("each cap (a 5-cell) has its 10 two-face plates, about P's centre, on 10 different mirrors: every cap is hidden in P's mirrors", capok)
tipM = Counter(sum(1 for v in V if dot(cen[k], v) == Z0)//2 for k in S0)
tipX = Counter(sum(1 for x in cen if dot(cen[k], x) == Z0)//2 for k in S0)
info("each tip lies on", dict(tipM), "mirrors and", dict(tipX), "cross walls (as a point)")
check("every tip lies on the same number of mirrors, and of cross walls (as printed)", len(tipM) == 1 and len(tipX) == 1)
# the tip 600-cell's own triangles: their plates are its own mirrors = P's cross walls through its corners
Tc = sorted(S0); cosn = phi*Q5(F(1, 2))*cc
adjT = {a: {b for b in Tc if b != a and dot(cen[a], cen[b]) == cosn} for a in Tc}
Ttri = [t for t in combinations(Tc, 3) if t[1] in adjT[t[0]] and t[2] in adjT[t[0]] and t[2] in adjT[t[1]]]
Tpl = Counter(canon(normal(cen[a], cen[b], cen[d])) for a, b, d in Ttri)
check("the tip 600-cell's 1200 triangles lie on 60 of P's 300 cross walls, 20 on each (its own mirrors); none on P's mirrors",
      len(Ttri) == 1200 and set(Tpl) <= CROSS and len(Tpl) == 60 and set(Tpl.values()) == {20})
check("conversely P's 60 mirrors are cross walls of the tip 600-cell (its cell centres include P's corners)",
      all(canon(v) in {canon(z) for z in duals[0]} for v in V))

# ---------------------------------------------------------------- Q5: vertex figure, octahedron, shells, designs
at1 = [k for k in range(600) if ONE in C[k]]
def imag(k): return (Z0,) + cen[k][1:]
def regtet(ks):
    ims = [imag(k) for k in ks]; n2 = dot(ims[0], ims[0])
    return all(dot(a, a) == n2 for a in ims) and all(dot(a, b) == Q5(F(-1, 3))*n2 for a, b in combinations(ims, 2))
tL = [frozenset(k for k in at1 if labL[k] == i) for i in range(5)]
tR = [frozenset(k for k in at1 if labR[k] == j) for j in range(5)]
check("at a corner the 20 cells (faces of the icosahedral vertex figure) split by left set into 5 sets of 4 whose face centres form 5 regular tetrahedra",
      len(at1) == 20 and all(len(s) == 4 and regtet(s) for s in tL) and all(len(s) == 4 and regtet(s) for s in tR))
check("the left tetrahedra and the right tetrahedra are different (no tetrahedron in both): the two chiral compounds of five tetrahedra in the dodecahedron of face centres",
      not (set(tL) & set(tR)))
check("each set of 4 faces at a corner meets all 12 neighbours once (edge cover once, read at a corner)",
      all(Counter(v for k in s for v in C[k] if v != ONE) == Counter({v: 1 for v in set(v for k in s for v in C[k] if v != ONE)}) and len(set(v for k in s for v in C[k] if v != ONE)) == 12 for s in tL))
# octahedron analogue (exact integers)
O = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
faces = [f for f in combinations(range(6), 3) if all(sum(a*b for a, b in zip(O[i], O[j])) == 0 for i, j in combinations(f, 2))]
alt = [f for f in faces if (O[f[0]][0]+O[f[0]][1]+O[f[0]][2])*(O[f[1]][0]+O[f[1]][1]+O[f[1]][2])*(O[f[2]][0]+O[f[2]][1]+O[f[2]][2]) > 0]
tips3 = [tuple(sum(O[i][d] for i in f) for d in range(3)) for f in alt]
ecount = Counter(e for f in alt for e in combinations(f, 2))
check("3D: the octahedron's 4 alternate faces cover its 12 edges once; tetrahedra on them have tips (1,1,1)-type: a regular tetrahedron of twice the edge, convex",
      len(faces) == 8 and len(alt) == 4 and len(ecount) == 12 and set(ecount.values()) == {1}
      and all(sum((a-b)**2 for a, b in zip(p, q)) == 8 for p, q in combinations(tips3, 2)))
# Cleo shells of #63: cells by height of the centre over one corner
shells = {}
for k in range(600): shells.setdefault(dot(cen[k], V[ONE]), []).append(k)
check("#63's 15 shells round one corner: every shell splits equally among the five left sets (and the five right sets)",
      len(shells) == 15 and all(len(set(Counter(labL[k] for k in s).values())) == 1 and len(Counter(labL[k] for k in s)) == 5 for s in shells.values())
      and all(len(Counter(labR[k] for k in s)) == 5 and len(set(Counter(labR[k] for k in s).values())) == 1 for s in shells.values()))
info("shell sizes from the corner outward:", [len(shells[hh]) for hh in sorted(shells, key=lambda q: -q.f())])
# designs: P and the unit tip 600-cell together, degrees up to 12 (odd degrees vanish by central symmetry)
x = sp.Symbol('x')
def Upoly(n):
    p = sp.Poly(sp.chebyshevu(n, x), x); return [F(int(sp.numer(cf)), int(sp.denom(cf))) for cf in reversed(p.all_coeffs())]
def zonal(n, svals):   # sum of U_n(t) over pairs, U_n even: in s = t^2
    cf = Upoly(n); tot = Q5(0)
    for s, m in svals.items():
        acc = Q5(0); sp_ = Q5(1)
        for d in range(0, n+1, 2):
            if cf[d] != 0: acc = acc + Q5(cf[d])*sp_
            sp_ = sp_*s
        tot = tot + acc*Q5(m)
    return tot
sv = Counter()
for i in range(N):
    for j in range(N): d_ = dot(V[i], V[j]); sv[d_*d_] += 1
Tu = [cen[k] for k in Tc]
for a in Tu:
    for b in Tu: d_ = dot(a, b); sv[d_*d_/(cc*cc)] += 1
for v in V:
    for b in Tu: d_ = dot(v, b); sv[d_*d_/cc] += 2
zs = {n: zonal(n, sv) for n in (2, 4, 6, 8, 10, 12)}
check("P together with the unit tip 600-cell (240 points) is an 11-design (both parts are) but not a 12-design: no new design from the pair",
      all(zs[n] == Q5(0) for n in (2, 4, 6, 8, 10)) and not (zs[12] == Q5(0)))
info("degree-12 zonal sum =", zs[12])
info("run time %.0f s" % (time.time() - t0))
print("FINAL ok" if ok else "FINAL MISMATCH")
