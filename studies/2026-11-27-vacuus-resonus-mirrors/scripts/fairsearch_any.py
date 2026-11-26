"""Step 10 (generic version of step 7, any dual pair; PAIR env, e.g. 'icosidodecahedron|rhombic triacontahedron').
Step 7 (27 Nov 2026; DICTO: "keep going with the fair dice search"): fair dice from the pieces of DICTO's pair conjecture,
cube + octahedron planes (13 planes through O: 9 mirrors + x +- y +- z = 0). With Claude (Anthropic).
Exact rule (angles.py / relations.py): every piece is of kind A (1/16 - theta/8 of the sphere) or B (-1/24 + theta/8), theta =
arccos(1/3)/pi irrational; so a union of pieces has solid angle (#A + #B ... ) and a face is FAIR-SIZED iff #A = #B = a, its share is
a/48, and a die of such faces has N = 48/a faces. Search, for a = 1 (N = 48), 2 (N = 24), 3 (N = 16):
1. all 96 pieces on the sphere, exactly (octants split by the other 10 planes); kind by solid angle; adjacency by shared edges;
2. candidate faces: connected unions of a A's and a B's whose outline is a convex spherical polygon (exact signs);
3. every partition of the sphere into candidate faces (CP-SAT exact cover, all solutions up to a cap);
4. each partition kept only if it is the face pattern (seen from O) of a convex polyhedron: face k = {x : n_k . x >= n_j . x for
   all j}, an LP: for adjacent faces k, j on the great circle with normal m (pointing into k), n_k - n_j = lam m with lam >= 1;
5. symmetry group (of the 48 signed permutations, those mapping the partition to itself) and duplicates removed up to O_h.
Output fairdice.json; each die: N, faces as piece lists, symmetry order, face side counts, plane normals (floats)."""
import os, sys, json, itertools
import numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'angles.py')).read()
exec(src[:src.index('PAIRS5 = ')])
from scipy.optimize import linprog
SD = dict(SOL); PA, PB = os.environ.get('PAIR', 'cube|octahedron').split('|'); Vc, Vo = SD[PA], SD[PB]
pa, pb = planes_of(Vc), planes_of(Vo); ALLP = []
for p in pa[0] + pa[1] + pb[0] + pb[1]: add(ALLP, p)
one = Vc[0][0] * 0 + 1; z = one * 0
MIR = mirrors_of(Vc); GO = {6: 24, 9: 48, 15: 120}[len(MIR)]
# 1. pieces: start from the 8 octant triangles, split by every non-coordinate plane
E = [(one, z, z), (z, one, z), (z, z, one)]
polys = []
for sx, sy, sz in itertools.product((1, -1), repeat=3):
    tri = [scl(sx, E[0]), scl(sy, E[1]), scl(sz, E[2])]
    if sg(dot(cross(sub(tri[1], tri[0]), sub(tri[2], tri[0])), tri[0])) < 0: tri = [tri[0], tri[2], tri[1]]
    polys.append(tri)
for p in ALLP:
    if sum(1 for c in p if not c.iszero()) == 1: continue
    polys = [q for P in polys for q in split(P, p)]
polys = [P for P in polys if len(P) >= 3]
NP = len(polys)
ang = [float(solid_angle(P) / (4 * mp.pi)) for P in polys]
vals = sorted(set(round(a, 12) for a in ang)); KINDS = len(vals)
kind = [vals.index(round(a, 12)) for a in ang]
from collections import Counter as _C
print('piece kinds (fraction of sphere : count):', [(v, c) for v, c in sorted(_C(round(a, 12) for a in ang).items())], flush=True)
assert all(c == GO for c in _C(kind).values()), 'every kind once per chamber expected'
def vkey(v):
    f = np.array([float(x) for x in v]); f /= np.linalg.norm(f); return tuple(np.round(f, 9))
VK = [[vkey(v) for v in P] for P in polys]
edges = {}
for i, P in enumerate(VK):
    for k in range(len(P)): edges.setdefault(frozenset((P[k], P[(k + 1) % len(P)])), []).append(i)
adj = {i: set() for i in range(NP)}
for e, L in edges.items():
    if len(L) == 2: a, b = L; adj[a].add(b); adj[b].add(a)
print('pieces', len(polys), 'kinds', KINDS, 'shared edges', sum(1 for L in edges.values() if len(L) == 2), flush=True)
# exact outline of a union: boundary edges (edges used once), chained; convex iff every corner turns the same way (exact)
EX = {}
for i, P in enumerate(polys):
    for v, k in zip(P, VK[i]): EX[k] = v
def outline(S):
    cnt = {}
    for i in S:
        P = VK[i]
        for k in range(len(P)):
            e = (P[k], P[(k + 1) % len(P)]); r = (e[1], e[0])
            if r in cnt: del cnt[r]
            else: cnt[e] = 1
    nxt = {}
    for a, b in cnt:
        if a in nxt: return None
        nxt[a] = b
    start = next(iter(nxt)); loop = [start]
    while True:
        b = nxt[loop[-1]]
        if b == start: break
        loop.append(b)
        if len(loop) > len(nxt): return None
    if len(loop) != len(nxt): return None   # not a single disc
    # drop straight-through corners (on one great circle), then test convexity exactly
    pts = [EX[k] for k in loop]; corners = []
    for k in range(len(pts)):
        u, v, w = pts[k - 1], pts[k], pts[(k + 1) % len(pts)]
        s = sg(dot(cross(u, v), w))
        if s < 0: return None
        if s > 0: corners.append(v)
    return corners
def connected(S):
    S = set(S); seen = {next(iter(S))}; st = list(seen)
    while st:
        x = st.pop()
        for y in adj[x]:
            if y in S and y not in seen: seen.add(y); st.append(y)
    return len(seen) == len(S)
def candidates(a):
    out = set(); frontier = {frozenset([i]) for i in range(NP)}
    for size in range(2, KINDS * a + 1):
        nf = set()
        for S in frontier:
            for x in S:
                for y in adj[x]:
                    if y not in S:
                        T = S | {y}
                        cnt = _C(kind[i] for i in T)
                        if all(c <= a for c in cnt.values()): nf.add(T)
        frontier = nf
        print(f'      size {size}: {len(frontier)} partial unions', flush=True)
    for S in frontier:
        if outline(S) is not None: out.add(S)
    return sorted(out, key=sorted)
# symmetry: the 48 signed permutation matrices acting on piece centroids
cen = []
for P in polys:
    c = np.mean([np.array([float(x) for x in v]) / np.linalg.norm([float(x) for x in v]) for v in P], axis=0); cen.append(c / np.linalg.norm(c))
cen = np.array(cen); G = []
refl = []
for m in MIR:
    u = np.array([float(x) for x in m]); u /= np.linalg.norm(u); refl.append(np.eye(3) - 2 * np.outer(u, u))
mats = [np.eye(3)]
while True:
    new = [R @ M for R in refl for M in mats]; added = False
    for M in new:
        if not any(np.allclose(M, X) for X in mats): mats.append(M); added = True
    if not added: break
assert len(mats) == GO, (len(mats), GO)
for M in mats:
    img = [int(np.argmin(np.linalg.norm(cen - M @ c, axis=1))) for c in cen]
    assert sorted(img) == list(range(NP)); G.append(img)
def realise(faces):
    # LP: n_k - n_j = lam * m (m = normal of the shared great circle, pointing into k), lam >= 1
    N = len(faces); owner = {}
    for k, F in enumerate(faces):
        for i in F: owner[i] = k
    rows, rhs = [], []; lamv = []
    seen = set()
    for e, L in edges.items():
        if len(L) != 2: continue
        i, j = L; k, l = owner[i], owner[j]
        if k == l or (k, l) in seen: continue
        a, b = tuple(e); m = np.cross(np.array(a), np.array(b)); m /= np.linalg.norm(m)
        cj = np.mean([np.array(v) for v in VK[i]], axis=0)
        if m @ cj < 0: m = -m                      # m points into face k (piece i's side)
        seen.add((k, l)); seen.add((l, k)); lamv.append((k, l, m))
    nv = 3 * N + len(lamv)
    Aeq, beq = [], []
    for t, (k, l, m) in enumerate(lamv):
        for q in range(3):
            r = np.zeros(nv); r[3 * k + q] = 1; r[3 * l + q] = -1; r[3 * N + t] = -m[q]; Aeq.append(r); beq.append(0)
    r = np.zeros(nv); r[0:3 * N] = 0
    bounds = [(None, None)] * (3 * N) + [(1, None)] * len(lamv)
    # fix the free translation n_k -> n_k + c (O inside: sum of face normals direction free): pin n_0 = 0 offset via sum n_k = 0
    for q in range(3):
        r = np.zeros(nv); r[q:3 * N:3] = 1; Aeq.append(r); beq.append(0)
    res = linprog(np.zeros(nv), A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=bounds, method='highs')
    return res.status == 0
from ortools.sat.python import cp_model
results = []
for a in [int(x) for x in os.environ.get('AS', '1,2,3').split(',')]:
    C = candidates(a); N = GO // a
    print(f'a = {a} (N = {N}): candidate fair-sized convex faces {len(C)}', flush=True)
    m = cp_model.CpModel(); x = [m.NewBoolVar(f'c{t}') for t in range(len(C))]
    cover = {i: [] for i in range(NP)}
    for t, S in enumerate(C):
        for i in S: cover[i].append(x[t])
    for i in range(NP): m.AddExactlyOne(cover[i])
    # no T-junctions (a convex polyhedron cannot have them): if face t passes straight through a vertex v of the arrangement,
    # all pieces at v outside t belong to ONE face
    around = {}
    for i, P in enumerate(VK):
        for k in P: around.setdefault(k, set()).add(i)
    ncon = 0
    for tt, S in enumerate(C):
        cor = {vkey(v) for v in outline(S)}
        bverts = set()
        for i in S:
            for k in VK[i]:
                if not around[k] <= S: bverts.add(k)
        for v in bverts - cor:
            out = sorted(around[v] - S)
            for p_ in out:
                for q_ in out:
                    if p_ < q_:
                        for s2 in range(len(C)):
                            if p_ in C[s2] and q_ not in C[s2]:
                                m.AddBoolOr([x[tt].Not(), x[s2].Not()]); ncon += 1
    print(f'   T-junction constraints {ncon}', flush=True)
    sols = []
    class CB(cp_model.CpSolverSolutionCallback):
        def __init__(s): super().__init__()
        def on_solution_callback(s):
            sols.append([t for t in range(len(C)) if s.Value(x[t])])
            if len(sols) % 100000 == 0: print(f'PROGRESS partitions {len(sols)}', flush=True)
            if len(sols) >= int(os.environ.get('CAP', 200000)): s.StopSearch()
    so = cp_model.CpSolver(); so.parameters.enumerate_all_solutions = True; so.parameters.num_workers = 1
    so.parameters.max_time_in_seconds = float(os.environ.get('TLIM', 1800))
    st = so.Solve(m, CB())
    print(f'   partitions found {len(sols)} (status {so.StatusName(st)})', flush=True)
    canon_seen = set(); kept = 0
    for sol in sols:
        faces = [sorted(C[t]) for t in sol]
        key = min(tuple(sorted(tuple(sorted(g[i] for i in F)) for F in faces)) for g in G)
        if key in canon_seen: continue
        canon_seen.add(key)
        if not realise(faces): continue
        fs = set(tuple(F) for F in faces)
        sym = sum(1 for g in G if set(tuple(sorted(g[i] for i in F)) for F in faces) == fs)
        sides = sorted(len(outline(set(F))) for F in faces)
        results.append(dict(N=N, a=a, symmetry_order=sym, side_counts=sides, faces=faces)); kept += 1
    print(f'   distinct up to O_h: {len(canon_seen)}; realised as convex polyhedra: {kept}', flush=True)
    for r in [r for r in results if r['N'] == N][:40]:
        from collections import Counter
        print(f'      N {N}: symmetry {r["symmetry_order"]}, faces by sides {dict(Counter(r["side_counts"]))}', flush=True)
json.dump(results, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../fairdice_' + PA.replace(' ', '-') + '.json'), 'w'))
full = [r for r in results if r['symmetry_order'] == GO]
print('full-symmetry dice found (controls, Catalan-type):', [(r['N'], dict(_C(r['side_counts']))) for r in full])
print('FINAL ok' if full else 'FINAL FAIL (no full-symmetry control found)')
