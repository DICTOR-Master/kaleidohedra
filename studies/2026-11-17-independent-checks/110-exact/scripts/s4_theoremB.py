"""Item 4, exact: Theorem B (a)-(d) in the 120-cell Q.
Copies are found by a complete search over ordered 4-tuples of Q's corners
(no symmetry used): a copy of a template X (A, B or C3 on the 600-cell) is a
set of Q corners that is the image of X under an orthogonal map scaled to
Q's radius; the images of 4 independent template corners fix the map, and
each further corner is the unique Q corner with the required inner products.
All comparisons are exact equalities of cosines (cross-multiplied in Z[phi])."""
import multiprocessing as mp
from common import *

L = Log('logs/s4_theoremB.log')
B = load_base()
P, Q, lab, WQ = B['P'], B['Q'], B['lab'], B['WQ'].astype(np.int64)
RP2 = np.array([50, 50])
RQ2 = B['RQ2']
GQ = gram(Q)
qidx = {canon_point(q): i for i, q in enumerate(Q)}
# cos labels: Q inner products scaled by RP2, template ones by RQ2
uq, LQ = value_labels(zmul(GQ, RP2[None, None]))
keymap = {zkey(u): i for i, u in enumerate(uq)}
IP36 = zmul(RQ2, np.array([0, 1]))            # R^2 * phi
assert np.all(IP36 % 2 == 0)
IP36 = IP36 // 2                              # R^2 cos36 = R^2 phi/2
A36 = zeq(GQ, IP36[None, None])
L.check('(a) each corner of Q has 24 corners at 36 deg', set(A36.sum(1).tolist()), {24})

# ---------------- (a) inscribed 600-cells
def comps(nodes):
    nodes = list(nodes)
    seen, out = set(), []
    for s in nodes:
        if s in seen:
            continue
        st, c = [s], set()
        while st:
            x = st.pop()
            if x in c:
                continue
            c.add(x)
            st += [y for y in nodes if A36[x, y] and y not in c]
        seen |= c
        out.append(frozenset(c))
    return out

icos = {v: comps(np.nonzero(A36[v])[0]) for v in range(600)}
L.check('(a) the 24 split into two sets of 12 with no 36-deg pair between them',
        {tuple(sorted(len(c) for c in icos[v])) for v in range(600)}, {(12, 12)})
cells600 = set()
for v in range(600):
    for ic in icos[v]:
        S = {v} | set(ic)
        nbr = {v: ic}
        queue = list(ic)
        par = {w: v for w in ic}
        while queue:
            w = queue.pop()
            if w in nbr:
                continue
            c = [c for c in icos[w] if par[w] in c]
            assert len(c) == 1
            nbr[w] = c[0]
            for y in c[0]:
                if y not in S:
                    S.add(y)
                if y not in nbr and y not in par:
                    par[y] = w
                    queue.append(y)
        cells600.add(frozenset(S))
Pi = sorted(sorted(s) for s in cells600)
L.check('(a) inscribed 600-cells found from every corner', (len(Pi), sorted({len(s) for s in Pi})), (10, [120]))
# exact: each is closed under reflection in each of its corners, and is a 600-cell
okr = 0
for s in Pi:
    X = Q[s]
    ix = {canon_point(x): i for i, x in enumerate(X)}
    if all(reflect_perm(X, X[k], ix) is not None for k in range(120)):
        okr += 1
L.check('(a) each closed under its own reflections (exact)', okr, 10)
ok12 = all(set(A36[np.ix_(s, s)].sum(1).tolist()) == {12} for s in Pi)
L.check('(a) each has 12 neighbours at 36 deg per corner inside it', ok12, True)
inc = np.zeros((10, 600), bool)
for i, s in enumerate(Pi):
    inc[i, s] = True
L.check('(a) every corner in exactly 2', set(inc.sum(0).tolist()), {2})
M = inc.astype(int) @ inc.T.astype(int)
# states: graph of disjointness
state = [-1] * 10
state[0] = 0
for _ in range(10):
    for i in range(10):
        for j in range(10):
            if i != j and M[i, j] == 0 and state[i] >= 0:
                state[j] = state[i]
            if i != j and M[i, j] > 0 and state[i] >= 0 and state[j] < 0:
                state[j] = 1 - state[i]
L.check('(a) two states of 5', sorted([state.count(0), state.count(1)]), [5, 5])
same = {int(M[i, j]) for i in range(10) for j in range(10) if i != j and state[i] == state[j]}
cross = {int(M[i, j]) for i in range(10) for j in range(10) if state[i] != state[j]}
L.check('(a) same state: disjoint', same, {0})
L.check('(a) different states: meet in 24 corners', cross, {24})
allowed = {zkey(zmul(RQ2, np.array(c))) for c in [(1, 0), (-1, 0), (0, 0)]}
half = zmul(RQ2, np.array([1, 0]))
assert np.all(half % 2 == 0)
allowed |= {zkey(half // 2), zkey(-half // 2)}
is24 = 0
for i in range(10):
    for j in range(10):
        if state[i] == 0 and state[j] == 1:
            T = [x for x in Pi[i] if inc[j, x]]
            vals = {zkey(GQ[a, b]) for a in T for b in T}
            n60 = set((zeq(GQ[np.ix_(T, T)], (half // 2)[None, None])).sum(1).tolist())
            if vals <= allowed and n60 == {8}:
                is24 += 1
L.check('(a) each cross-state meeting is a 24-cell (angles and 8 at 60 deg)', is24, 25)
L.check('(a) the two through a corner are in different states',
        all(len({state[i] for i in np.nonzero(inc[:, v])[0]}) == 2 for v in range(600)), True)

# ---------------- (b) copies
def template(name):
    ids = np.nonzero(lab == name)[0]
    X = P[ids]
    GT = gram(X)
    LT = np.full(GT.shape[:2], -1)
    sc = zmul(GT, RQ2[None, None])
    for a in range(len(X)):
        for b in range(len(X)):
            LT[a, b] = keymap.get(zkey(sc[a, b]), -1)
    # choose 4 independent corners with many small angles (exact Gram det)
    n = len(X)
    order = sorted(itertools.combinations(range(n), 4),
                   key=lambda c: -sum(zfloat(GT[a, b]) for a, b in itertools.combinations(c, 2)))
    for c in order:
        d = zdet4(GT[np.ix_(c, c)][None])[0]
        if np.any(d != 0):
            base = list(c)
            break
    rest = [k for k in range(n) if k not in base]
    return ids, X, LT, base, rest

TPL = {}

def search_q0(args):
    name, q0 = args
    ids, X, LT, base, rest = TPL[name]
    b0, b1, b2, b3 = base
    out = []
    c1 = np.nonzero(LQ[q0] == LT[b0, b1])[0]
    for q1 in c1:
        m2 = (LQ[q0] == LT[b0, b2]) & (LQ[q1] == LT[b1, b2])
        for q2 in np.nonzero(m2)[0]:
            m3 = (LQ[q0] == LT[b0, b3]) & (LQ[q1] == LT[b1, b3]) & (LQ[q2] == LT[b2, b3])
            for q3 in np.nonzero(m3)[0]:
                qs = [q0, q1, q2, q3]
                want = LT[np.ix_(rest, base)]                       # (r,4)
                have = LQ[qs].T                                     # (600,4)
                hit = (have[None, :, :] == want[:, None, :]).all(-1)  # (r,600)
                cnt = hit.sum(1)
                if np.all(cnt == 1):
                    img = np.empty(len(ids), int)
                    img[base] = qs
                    img[rest] = hit.argmax(1)
                    out.append(img)
    return out

for name in ['A', 'B', 'C3']:
    TPL[name] = template(name)
    if (TPL[name][2] < 0).any():
        L(name, 'has an angle not found in Q')

copies = {}
with mp.get_context('fork').Pool(24) as pool:
    for name in ['A', 'B', 'C3']:
        ids, X, LT, base, rest = TPL[name]
        res = pool.map(search_q0, [(name, q) for q in range(600)], chunksize=5)
        sets = {}
        nmap = 0
        for r in res:
            for img in r:
                nmap += 1
                # exact full Gram check of the image
                sets.setdefault(tuple(sorted(img)), img)
        cp = list(sets.values())
        okg = all(np.array_equal(LQ[np.ix_(c, c)], LT) for c in cp)
        L(f'{name}: {nmap} congruent maps found, {len(cp)} distinct copies; full Gram exact: {okg}')
        copies[name] = np.array(cp)
L.check('(b) copies of A (A and -A) in Q', len(copies['A']), 1200)
L.check('(b) copies of B (B and -B) in Q', len(copies['B']), 1200)
L.check('(b) copies of C3 in Q', len(copies['C3']), 600)
host = {}
for name, want in [('A', 120), ('B', 120), ('C3', 60)]:
    h = []
    for c in copies[name]:
        hs = [i for i in range(10) if inc[i, c].all()]
        h.append(hs[0] if len(hs) == 1 else -1 - len(hs))
    h = np.array(h)
    host[name] = h
    L.check(f'(b) every {name} copy inside exactly one P_i', bool((h >= 0).all()), True)
    L.check(f'(b) {name} copies per P_i', sorted(set(np.bincount(h, minlength=10).tolist())), [want])
    through = np.bincount(copies[name].ravel(), minlength=600)
    L(f'    {name} copies through each corner: {sorted(set(through.tolist()))}')
for name, st in [('A', 12), ('B', 12), ('C3', 24)]:
    c0 = np.sort(copies[name][0])
    orb = {tuple(r) for r in np.sort(WQ[:, c0], axis=1)}
    allc = {tuple(sorted(c)) for c in copies[name]}
    L.check(f'(b) {name}: one class under Sym(Q), stabiliser order', (orb == allc, 14400 // len(orb)), (True, st))

# ---------------- (c) walls
Wkeys = {}
mirP, crsP = [], []
for i, s in enumerate(Pi):
    X = Q[s]
    m = {canon_dir(x) for x in X}
    adj = A36[np.ix_(s, s)]
    cl = cliques(adj, 4)
    assert len(cl) == 600
    c = {canon_dir(X[list(t)].sum(0)) for t in cl}
    assert len(m) == 60 and len(c) == 300 and not (m & c)
    mirP.append(m)
    crsP.append(c)
allw = set().union(*mirP, *crsP)
L.check('(c) walls of the ten P_i together', len(allw), 1560)
Mq = {canon_dir(p) for p in P}           # Q's 60 mirrors (normals along P0 corners)
Xq = {canon_dir(q) for q in Q}           # 300 corner-axis walls
Nq = allw - Mq - Xq
L.check('(c) classes M, X, N', (len(Mq & allw), len(Xq & allw), len(Nq)), (60, 300, 1200))
hostM = {(sum(k in mirP[i] for i in range(10)), sum(k in crsP[i] for i in range(10))) for k in Mq}
hostX = {(sum(k in mirP[i] for i in range(10)), sum(k in crsP[i] for i in range(10))) for k in Xq}
hostN = {(sum(k in mirP[i] for i in range(10)), sum(k in crsP[i] for i in range(10))) for k in Nq}
L.check('(c) each M wall: (mirror of, cross wall of) how many P_i', hostM, {(0, 10)})
L.check('(c) each X wall: (mirror of, cross wall of)', hostX, {(2, 0)})
L.check('(c) each N wall: (mirror of, cross wall of)', hostN, {(0, 2)})
okx = all(sum(inc[i, q] for i in range(10) if canon_dir(Q[q]) in mirP[i]) == 2 for q in range(600))
L.check('(c) an X wall is a mirror of exactly the 2 P_i through that corner axis',
        all({i for i in range(10) if canon_dir(Q[q]) in mirP[i]} == set(np.nonzero(inc[:, q])[0]) for q in range(600)), True)
L.check('(c) each P_i: 60 mirrors from X; 300 cross walls = 60 from M + 240 from N',
        {(len(mirP[i] & Xq), len(crsP[i] & Mq), len(crsP[i] & Nq)) for i in range(10)}, {(60, 60, 240)})
wall_list = sorted(allw)
wid = {k: i for i, k in enumerate(wall_list)}
wclass = np.array([0 if k in Mq else (1 if k in Xq else 2) for k in wall_list])

plates = {}
tpl_ridges = {}
for name in ['A', 'B', 'C3']:
    ids, X, LT, base, rest = TPL[name]
    F, Rg, E = face_lattice(X)
    tpl_ridges[name] = Rg
    tri = np.array([r[:3] for r in Rg])
    cp = copies[name]
    pts = Q[cp[:, tri]]                         # (nc, nr, 3, 5, 2)
    nc, nr = pts.shape[:2]
    nv = plate_normals(pts.reshape(nc * nr, 3, 5, 2))
    ks = [wid.get(canon_dir(v), -1) for v in nv]
    pl = np.array(ks).reshape(nc, nr)
    plates[name] = pl
    L(f'{name}: plates per copy {nr}; plates outside the 1560: {(pl < 0).sum()}')
    used = {c: len(set(pl[wclass[np.maximum(pl, 0)] == c].tolist())) for c in range(3)}
    L(f'    distinct walls used by all {name} copies: M {used[0]}, X {used[1]}, N {used[2]}')
    own = all(set(wall_list[k] for k in pl[j]) <= (mirP[host[name][j]] | crsP[host[name][j]]) for j in range(nc))
    inQ = np.array([all(wclass[k] < 2 for k in pl[j]) for j in range(nc)])
    plates[name + '_own'] = own
    plates[name + '_inQ'] = inQ
    plates[name + '_used'] = used
L.check('(c) A: hidden in own P_i', plates['A_own'], True)
L.check('(c) A copies hidden in Q (all plates in W(Q))', int(plates['A_inQ'].sum()), 1200)
L.check('(c) A uses (M, X, N) walls', tuple(plates['A_used'][c] for c in range(3)), (0, 300, 0))
L.check('(c) B: hidden in own P_i', plates['B_own'], True)
L.check('(c) B copies hidden in Q', int(plates['B_inQ'].sum()), 0)
L.check('(c) B uses (M, X, N) walls', tuple(plates['B_used'][c] for c in range(3)), (60, 300, 1200))
L.check('(c) C3: hidden in own P_i', plates['C3_own'], True)
L.check('(c) C3 copies hidden in Q', int(plates['C3_inQ'].sum()), 0)
L.check('(c) C3 uses (M, X, N) walls', tuple(plates['C3_used'][c] for c in range(3)), (60, 0, 1200))

# ---------------- (d) triangle split in each P_i
EDGE_Q = None
okd = []
for i, s in enumerate(Pi):
    adj = A36[np.ix_(s, s)]
    tri_i = {tuple(sorted((s[a], s[b], s[c]))) for a, b, c in cliques(adj, 3)}
    assert len(tri_i) == 1200
    res = []
    for name in ['A', 'B']:
        cnt = {t: 0 for t in tri_i}
        per = set()
        for j in np.nonzero(host[name] == i)[0]:
            n = 0
            for r in tpl_ridges[name]:
                if len(r) == 3:
                    t = tuple(sorted(copies[name][j][list(r)]))
                    if t in cnt:
                        cnt[t] += 1
                        n += 1
            per.add(n)
        res.append((sorted(set(cnt.values())), sorted(per)))
    okd.append(res)
L.check('(d) per P_i: (A: copies per triangle, triangle faces per copy), (B: same)',
        {str(r) for r in okd}, {str([([2], [20]), ([1], [10])])})

np.savez_compressed('data/thmB.npz', Pi=np.array(Pi), state=np.array(state),
                    copiesA=copies['A'], copiesB=copies['B'], copiesC3=copies['C3'],
                    hostA=host['A'], hostB=host['B'], hostC3=host['C3'],
                    platesA=plates['A'], platesB=plates['B'], platesC3=plates['C3'],
                    wclass=wclass)
L.final()
