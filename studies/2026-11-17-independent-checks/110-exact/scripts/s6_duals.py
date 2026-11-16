"""Item 6 (part 1), exact: which pentagons and edges of the 120-cell Q are
covered by the fins of the polar duals A*, B*, C3* of the copies of A, B, C3
in the 600-cell P dual to Q.

Polarity about the centre: X* = {y : x.y <= r^2 for all corners x of X}.
The ridges of X* are dual to the edges ab of X; the fin over that ridge is
the cone from the centre over it, which is the set of directions d in which
a and b both attain max_x x.d (the normal cone of the edge).  This cone does
not depend on r^2 or on the scale of P, so the coverage is computed with the
corners of P0 (P is a positive multiple of P0, its corners lying along the
cell centres of Q).  A pentagon F of Q is covered whole by X* iff for some
edge ab of X every corner of F lies in the normal cone of ab (the cone is
convex), tested exactly with ranks of exactly sorted Z[phi] values."""
import json, os, time
from scipy.optimize import linprog
from common import *

FAMS = sys.argv[1:] or ['A', 'B', 'C3']
L = Log('logs/s6_duals_' + '_'.join(FAMS) + '.log')
B = load_base()
P, Q, lab, W = B['P'], B['Q'], B['lab'], B['W'].astype(np.int64)
pent, qedges, edges = B['pent'], B['qedges'], B['edges']
Dv = gram(P, Q)                                    # (120,600,2) exact
uniq, inv = value_labels(Dv)
order = np.argsort(zfloat(uniq), kind='stable')
su = uniq[order]
diffs = zsign(su[1:] - su[:-1])
L.check('distinct values x.q sorted exactly (strictly increasing)', bool((diffs > 0).all()), True)
rank_of = np.empty(len(uniq), int)
rank_of[order] = np.arange(len(uniq))
RK = rank_of[inv]                                  # (120,600) exact order
mir = {canon_dir(p) for p in P}

fam = {}
for name in FAMS:
    ids = np.nonzero(lab == name)[0]
    F, Rg, E = face_lattice(P[ids])
    tE = np.array([(ids[a], ids[b]) for a, b in E])
    imgs = {}
    for g in W:
        key = tuple(sorted(g[ids]))
        if key not in imgs:
            imgs[key] = g
    copies = sorted(imgs)
    want = {'A': 120, 'B': 120, 'C3': 60}[name]
    L.check(f'{name}: copies in the 600-cell (orbit under W(H4), exact)', len(copies), want)
    sets, esets, platesok = [], [], True
    nplates = set()
    for key in copies:
        g = imgs[key]
        cE = g[tE]                                  # edges of the copy
        X = np.array(key)
        mx = RK[X].max(0)                           # (600,)
        top = np.zeros((120, 600), bool)
        top[X] = RK[X] == mx[None]
        cov_q = top[cE[:, 0]] & top[cE[:, 1]]       # (nE,600): q in normal cone of edge
        pc = cov_q[:, pent].all(2).any(0)           # (720,)
        ec = cov_q[:, qedges].all(2).any(0)         # (1200,)
        sets.append(np.nonzero(pc)[0].tolist())
        esets.append(np.nonzero(ec)[0].tolist())
        pk = {canon_dir(P[a] - P[b]) for a, b in cE}
        platesok &= pk <= mir
        nplates.add(len(pk))
    sizes = sorted({len(s) for s in sets})
    cnt = np.zeros(720, int)
    for s in sets:
        cnt[s] += 1
    ecnt = np.zeros(1200, int)
    for s in esets:
        ecnt[s] += 1
    L(f'    {name}*: pentagons inside a single fin, per copy: {sizes}; copies per pentagon {sorted(set(cnt.tolist()))}')
    L.check(f'{name}*: every edge of Q lies whole in a single fin of some copy', bool((ecnt > 0).all()), True)
    L(f'    {name}*: copies per edge (single fin) {sorted(set(ecnt.tolist()))}')
    L.check(f'{name}*: every plate of every copy on one of Q\'s 60 mirrors; plates per copy',
            (bool(platesok), sorted(nplates)), (True, [10]))
    fam[name] = dict(copies=[list(map(int, k)) for k in copies], sets=sets, edge_sets=esets,
                     edges=[cE.tolist() for cE in [imgs[k][tE] for k in copies]])

# ---- union of fins.  A pentagon F (plate H) can only be met in positive area
# by fins whose plate is H.  For d in H let M(d) be the corners of X that
# maximise x.d.  The regions C_a = {d in H : a maximises}, a a corner of X,
# cover H.  In the relative interior of C_a, M(d) is {a} or {a, b_a}, b_a the
# other corner of X on the line through a perpendicular to H; d lies in a fin
# exactly when {a, b_a} is an edge of X ("good" a).  So F is covered whole iff
# every a whose region meets F in positive area is good, and not at all iff
# every such a is bad.  Positive area: float LP, then an exact rational
# witness point checked in Z[phi]; zero area: float LP only (stated).
import multiprocessing as mp
from fractions import Fraction
pkeys = [canon_dir(P[a] - P[b]) for a, b in edges]   # plate of pentagon k (dual to P0 edge k)
Pf, Qf = zfloat(P), zfloat(Q)

def region_lp(a, b, X, F):
    V = Qf[F]
    others = [x for x in X if x != a and x != b]
    A_ub = []
    for x in others:
        w = (Pf[x] - Pf[a]) @ V.T
        A_ub.append(list(w / np.linalg.norm(Pf[x] - Pf[a]) / np.linalg.norm(V[0])) + [1.0])
    for i in range(5):
        r = [0.0] * 6; r[i] = -1.0; r[5] = 1.0
        A_ub.append(r)
    res = linprog([0] * 5 + [-1], A_ub=A_ub, b_ub=[0.0] * len(A_ub), A_eq=[[1] * 5 + [0]], b_eq=[1],
                  bounds=[(0, None)] * 5 + [(None, 1)], method='highs')
    if res.status != 0:
        raise RuntimeError(f'LP status {res.status} {res.message}')
    s = -res.fun
    if s <= 1e-9:
        return False, None
    w = [int(round(v * 10 ** 6)) for v in res.x[:5]]   # integer weights: exact point of F's cone
    if min(w) <= 0:
        return True, False
    d = sum(wi * Q[f] for wi, f in zip(w, F))
    vals = zdot(P[np.array(others)] - P[a][None], d[None])
    return True, bool((zsign(vals) < 0).all())

def cover_one(args):
    name, ci = args
    X = FAM[name]['copies'][ci]
    E = {frozenset(e) for e in FAM[name]['edges'][ci]}
    pairs = {}
    for a, x in itertools.permutations(X, 2):
        pairs.setdefault(canon_dir(P[x] - P[a]), {})[a] = x
    finkeys = {canon_dir(P[min(e)] - P[max(e)]) for e in E}
    cov, part, unver, nlp = [], [], 0, 0
    for k in range(720):
        if pkeys[k] not in finkeys:
            continue
        F = pent[k]
        bmap = pairs.get(pkeys[k], {})
        good_present = bad_present = False
        Fr = RK[:, F]                                   # exact ranks of x.f
        for a in X:
            b = bmap.get(a, -1)
            # exact prune: if some x beats a at all five corners of F, C_a misses F
            if any((Fr[x] > Fr[a]).all() for x in X if x != a and x != b):
                continue
            nlp += 1
            present, ok = region_lp(a, b, X, F)
            if not present:
                continue
            if ok is not True:
                unver += 1
            if b >= 0 and frozenset((a, b)) in E:
                good_present = True
            else:
                bad_present = True
        if good_present and not bad_present:
            cov.append(k)
        elif good_present and bad_present:
            part.append(k)
    return cov, part, unver, nlp

FAM = {nm: {'copies': fam[nm]['copies'], 'edges': fam[nm]['edges']} for nm in fam}
with mp.get_context('fork').Pool(24) as pool:
    for name in FAMS:
        NC = int(os.environ.get('LIMIT', len(FAM[name]['copies'])))
        t1 = time.time()
        res = pool.map(cover_one, [(name, c) for c in range(NC)], chunksize=1)
        L(f'{name}: union stage {time.time() - t1:.1f} s for {NC} copies')
        sets = [r[0] for r in res]
        fam[name]['single'] = fam[name]['sets']
        fam[name]['sets'] = sets
        npart = sum(len(r[1]) for r in res)
        unver = sum(r[2] for r in res)
        nlp = sum(r[3] for r in res)
        cnt = np.zeros(720, int)
        for s_ in sets:
            cnt[s_] += 1
        L(f'{name}*: union-of-fins coverage: {nlp} region LPs, positive-area regions without an exact witness: {unver}')
        L.check(f'{name}*: pentagons covered whole per copy (union of its fins)', sorted({len(s_) for s_ in sets}), [60])
        L.check(f'{name}*: copies covering each pentagon', sorted(set(cnt.tolist())),
                [{'A': 10, 'B': 10, 'C3': 5}[name]])
        L.check(f'{name}*: (copy, pentagon) pairs covered only in part', npart, 0)
        single_in = all(set(a) <= set(b) for a, b in zip(fam[name]['single'], sets))
        L(f'    {name}*: covered by a single fin: {sorted({len(s_) for s_ in fam[name]["single"]})} per copy; '
          f'subset of union coverage: {single_in}')

for name in FAMS:
    json.dump({'family': name, 'copies_600cell_corner_ids': fam[name]['copies'], 'sets': fam[name]['sets'],
               'single_fin_sets': fam[name]['single'], 'edge_sets_single_fin': fam[name]['edge_sets'],
               'note': 'pentagon k of Q is dual to edge k of the 600-cell (edges_of_600cell in '
                       'dual_cover_instance.json); sets[c] = pentagons covered whole by the fins of copy c'},
              open(f'data/dual_sets_{name}.json', 'w'))
    L(f'wrote data/dual_sets_{name}.json')
L.final()
