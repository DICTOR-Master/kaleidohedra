# Bodhi seed gap pieces, built from the block coordinates (2026-10-12).
# Block coordinates: x = s e_a + t e_b + u e_c for the icosahedron face (a, b, c); the rhombic hexecontahedron block is the unit cube,
# the chamber (fundamental cone) is {s >= t >= u >= 0}. In these coordinates (h = inradius of RT(1/phi) as the unit of the 15 slab
# forms, see logs/slabs.log):
#   centre RT(1/phi) in the 3-fold sector = {s+t+u/phi <= 1, s+t/phi+u <= 1, s/phi+t+u <= 1}      (bipyramid 0, e_a, e_b, e_c, F/phi^2)
#   outer RT(phi^2) in the sector         = the same with phi^3 on the right                      (bipyramid 0, phi^3 e_a, ..., phi F)
#   copy a in the chamber                  = {s >= 1, t + u/phi <= phi, s/phi + t + u <= 2 phi, s + t + u/phi <= phi^3}
#   copies b, c do not enter the chamber's interior (they need t >= s, u >= s); no other copy enters the sector.
# So, per chamber:  inner pocket = {1 >= s >= t >= u >= 0, s + t + u/phi >= 1}                       (one convex cell)
#                   outer pocket = {s >= 1, s >= t >= u >= 0, s+t+u/phi <= phi^3} minus copy a
#                                = R ∩ ({t + u/phi >= phi} ∪ {s/phi + t + u >= 2 phi})                (two convex cells)
# This script builds these cells, checks them against the solids (inside the outer form, outside every solid, exact volumes), then
# looks for the coarsest symmetric convex decomposition: all convex unions of cells (merging across chamber walls), orbits under the
# 120 symmetries, and an exact cover with the fewest congruence classes, then the fewest pieces (MILP).
import sys, os, itertools, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bodhi_core import *
from scipy.spatial import ConvexHull
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix
MODE = sys.argv[1] if len(sys.argv) > 1 else 'both'          # inner | outer | both
EXTRA = os.environ.get('EXTRA', '')                           # extra cut planes for the outer pocket: 'H3' adds u + s/phi = phi (copy b's face)

t0 = TRIANGLES[np.argmax(U20 @ chamber()[1])]; a, b, c = U12[list(t0)]; M = np.array([a, b, c]).T
def X(stu): return M @ np.asarray(stu, float)
def plane(cf, rhs, sense):
    """halfspace cf.(s,t,u) <= rhs (sense +1) or >= rhs (-1), as n.x + d <= 0 in real coordinates"""

    n = np.linalg.inv(M).T @ np.asarray(cf, float)
    e = np.r_[n, -rhs] if sense > 0 else np.r_[-n, rhs]
    k = np.linalg.norm(e[:3]); return e / k
f = 1 / PHI
CH = [plane((1, -1, 0), 0, -1), plane((0, 1, -1), 0, -1), plane((0, 0, 1), 0, -1)]              # s>=t, t>=u, u>=0
OUT = plane((1, 1, f), PHI ** 3, +1)
INNER = [verts(CH + [plane((1, 0, 0), 1, +1), plane((1, 1, f), 1, -1)])]
R = CH + [plane((1, 0, 0), 1, -1), OUT]
H1, H2 = plane((0, 1, f), PHI, -1), plane((f, 1, 1), 2 * PHI, -1)
OUTER = [verts(R + [H1]), verts(R + [H2, -H1])]
if 'H2FIRST' in EXTRA: OUTER = [verts(R + [H2]), verts(R + [H1, -H2])]
if 'H3' in EXTRA:
    H3 = plane((f, 0, 1), PHI, -1)
    OUTER = [verts(R + [H1, H3]), verts(R + [H1, -H3]), verts(R + [H2, -H1, H3]), verts(R + [H2, -H1, -H3])]
    OUTER = [W for W in OUTER if W is not None and len(W) >= 4 and vol(W) > 1e-9]

def check_cells(cells, name):
    tot = 0
    for W in cells:
        assert all(np.all(W @ e[:3] + e[3] <= 1e-7) for e in F_OUTER), 'pokes out of the outer form'
        for S in SOLIDS: assert sat_separated(W, S), 'overlaps a solid'
        tot += vol(W)
    for A, B in itertools.combinations(cells, 2): assert sat_separated(A, B)
    print(f'{name}: {len(cells)} convex cells per chamber, volume x120 = {120 * tot:.9f}')
    return tot
if MODE in ('inner', 'both'):
    vi = check_cells(INNER, 'inner pocket'); print(f'  = {120 * vi / P_VOL:.6f} P; RT(1) = {RT_VOL:.9f}; 10P + 10O = {10 * (P_VOL + O_VOL):.9f}')
if MODE in ('outer', 'both'):
    vo = check_cells(OUTER, 'outer pocket'); print(f'  = {120 * vo / P_VOL:.6f} P; 70P + 10O = {70 * P_VOL + 10 * O_VOL:.9f}; gap - RT(1) = {GAP_VOL - RT_VOL:.9f}')

def search(cells0, name, maxk=12):
    # all 120 images of the chamber cells, deduplicated
    cells = {}
    for W in cells0:
        for g in GROUP:
            V = W @ g.T; k = canon(V)
            if k not in cells: cells[k] = V
    ids = list(cells); C = [cells[k] for k in ids]; n = len(C)
    print(f'\n[{name}] {n} cells in the whole seed')
    vmap = {}
    for i, V in enumerate(C):
        for v in V: vmap.setdefault(key(v, 5), set()).add(i)
    adj = {i: set() for i in range(n)}
    for i, V in enumerate(C):
        for j in set().union(*[vmap[key(v, 5)] for v in V]) - {i}:
            if len({key(v, 5) for v in V} & {key(w, 5) for w in C[j]}) >= 3: adj[i].add(j)
    vols = np.array([vol(V) for V in C])
    # convex unions by pairwise merging (every convex union of arrangement cells splits into two smaller convex unions)
    unions = {frozenset([i]): C[i] for i in range(n)}
    frontier = list(unions)
    while frontier:
        new = []
        for S in frontier:
            nb = set().union(*[adj[i] for i in S]) - S
            for j in nb:
                T = S | {j}
                if T in unions or len(T) > maxk: continue
                U = np.vstack([unions[S], C[j]]); H = ConvexHull(U)
                if abs(H.volume - vols[list(T)].sum()) < 1e-8:
                    unions[T] = U[H.vertices]; new.append(T)
        # also merge pairs of multi-cell unions that touch (needed when neither grows by one cell)
        frontier = new
        print(f'   unions of up to {max(len(S) for S in unions)} cells: {len(unions)}', flush=True)
    # pair merges of existing unions (closure)
    changed = True
    while changed:
        changed = False
        keys = list(unions)
        for S, T in itertools.combinations(keys, 2):
            if S & T or len(S | T) > maxk or not any(j in adj[i] for i in S for j in T): continue
            if (S | T) in unions: continue
            U = np.vstack([unions[S], unions[T]]); H = ConvexHull(U)
            if abs(H.volume - vols[list(S | T)].sum()) < 1e-8:
                unions[S | T] = U[H.vertices]; changed = True
    print(f'   convex unions (all sizes <= {maxk}): {len(unions)}; sizes {sorted(set(len(S) for S in unions))}')
    # orbits under the group
    cid = {canon(V): i for i, V in enumerate(C)}
    orbits, seen = [], set()
    for S in unions:
        if S in seen: continue
        orb = set()
        for g in GROUP:
            img = frozenset(cid[canon(C[i] @ g.T)] for i in S); orb.add(img)
        for T in orb: seen.add(T)
        if all(T in unions for T in orb): orbits.append((sorted(orb), congruence_sig(unions[S])))
        else: print('   (orbit not closed under the group?!)', len(S))
    types = {}
    for oi, (orb, sig) in enumerate(orbits): types.setdefault(sig, []).append(oi)
    print(f'   orbits {len(orbits)}, congruence types {len(types)}')
    # MILP: exact cover of cells by orbits; minimise 1000*types + pieces
    T = list(types); tid = {sig: k for k, sig in enumerate(T)}
    nv = len(orbits) + len(T)
    A = lil_matrix((n, nv))
    for oi, (orb, sig) in enumerate(orbits):
        for S in orb:
            for i in S: A[i, oi] += 1
    cons = [LinearConstraint(csr_matrix(A), 1, 1)]
    B = lil_matrix((len(orbits), nv))
    for oi, (orb, sig) in enumerate(orbits): B[oi, oi] = 1; B[oi, len(orbits) + tid[sig]] = -1
    cons.append(LinearConstraint(csr_matrix(B), -np.inf, 0))
    cost = np.r_[[len(orb) for orb, _ in orbits], [1000.0] * len(T)]
    res = milp(cost, constraints=cons, integrality=np.ones(nv), bounds=Bounds(0, 1), options={'time_limit': 1200})
    print(f'   MILP: {res.message}')
    if res.x is None: return None
    chosen = [oi for oi in range(len(orbits)) if res.x[oi] > .5]
    out = []
    for oi in chosen:
        orb, sig = orbits[oi]; W = unions[orb[0]]
        stab = 120 // len(orb)
        print(f'   piece orbit: {len(orb)} copies, {len(orb[0])} chamber cells each, stabiliser order {stab}, volume {sig[1]:.6f} = {sig[1] / P_VOL:.6f} P')
        out.append((orb, [unions[S] for S in orb]))
    print(f'   total pieces {sum(len(o) for o, _ in out)}, types {len(set(orbits[oi][1] for oi in chosen))}')
    # also: the minimum number of pieces regardless of types
    res2 = milp(np.r_[[len(orb) for orb, _ in orbits], [0.0] * len(T)], constraints=cons[:1], integrality=np.ones(nv), bounds=Bounds(0, 1), options={'time_limit': 1200})
    if res2.x is not None:
        ch2 = [oi for oi in range(len(orbits)) if res2.x[oi] > .5]
        print(f'   fewest pieces regardless of types: {sum(len(orbits[oi][0]) for oi in ch2)} pieces, {len(set(orbits[oi][1] for oi in ch2))} types')
    return out

results = {}
if MODE in ('inner', 'both'): results['inner'] = search(INNER, 'inner')
if MODE in ('outer', 'both'): results['outer'] = search(OUTER, 'outer' + ('+' + EXTRA if EXTRA else ''))
import pickle
with open(os.path.join(HERE, f'../data/pieces-{MODE}{"-" + EXTRA if EXTRA else ""}.pkl'), 'wb') as fh: pickle.dump(results, fh)
for nm, out in results.items():
    if not out: continue
    for k, (orb, Ws) in enumerate(out):
        print(f'\n== {nm} piece type {k + 1}: {len(Ws)} copies')
        print(describe(Ws[0], f'{nm}-{k + 1}'))
