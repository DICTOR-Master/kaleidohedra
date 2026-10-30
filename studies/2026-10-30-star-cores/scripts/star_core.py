# Star Cores, study 0 (DICTO 2026-10-30: "all new shapes given the star core treatment"). For every new shape of DICTO Solids with a
# D-number and a model, the treatment #78 gave the truncated icosahedron, for t = 2 (mirrored spikes) and t = phi (golden):
#  (1) its own pyramids from the centre (centre = mean of the corners, fixed by every symmetry): valid when every face plane has the
#      centre strictly inside and the pyramids' volumes add up to the solid's (no overlap);
#  (2) spikes: over each face the pyramid to the tip t x the foot of the perpendicular from the centre;
#  (3) the star (solid + spikes), the halo (hull of the tips); star inside the halo?; layer fill: over each corner the piece to the tips of
#      its faces, over each edge the tetrahedron (edge + the 2 tips); volumes add up?; overlaps by the separating-axis test;
#  (4) the core of the turn: the faces grouped into families (number of sides, distance from the centre); the hull of each family's tips;
#      the core = the intersection of the family hulls that are solid; compared with the shape itself;
#  (5) the core's own turn: the core of the core's turn, compared with the shape (period two?);
#  (6) the star chain: period from survey v2 when known.
# Numerical (float64, tolerances 1e-9 relative); exact checks follow for the shapes that close. Usage:
#   star_core.py <dataset dir> <out dir> [jobs]
import csv, json, os, sys, itertools, multiprocessing as mp, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
DS, OUT = sys.argv[1], sys.argv[2]; JOBS = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 8
def load(fn):
    d = json.load(open(os.path.join(DS, fn), encoding='utf8'))
    V = np.array([[float(x) for x in v['decimal']] for v in d['vertices']]); F = d['faces']
    return d, V, F
def faces_info(V, F):
    out = []
    for f in F:
        P = V[f]; n = np.zeros(3)
        for i in range(len(f)): n += np.cross(P[i], P[(i + 1) % len(f)])   # Newell normal (outward for ccw faces)
        n /= np.linalg.norm(n); out.append((f, n, float(n @ P.mean(0))))
    return out
def vol(Q):
    try: return ConvexHull(Q).volume
    except Exception: return 0.0
def polyvol(V, F):
    s = 0.0
    for f in F:
        for i in range(1, len(f) - 1): s += np.linalg.det(np.array([V[f[0]], V[f[i]], V[f[i + 1]]]))
    return s / 6
def pl(Q):
    u = {}
    for eq in ConvexHull(Q).equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
def cut(H):
    try:
        W = HalfspaceIntersection(H, np.zeros(3)).intersections; return W[ConvexHull(W).vertices]
    except Exception: return None
def shape(Q):
    hq = ConvexHull(Q); V = Q[hq.vertices]; V = V / np.linalg.norm(V, axis=1).max(); hq = ConvexHull(V)
    fam = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7)); fam.setdefault(k, [i for i, p in enumerate(V) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    fk = {}
    for ids in fam.values(): fk[len(ids)] = fk.get(len(ids), 0) + 1
    d = np.linalg.norm(V[:, None] - V[None], axis=2)
    E = sorted({round(float(d[a, b]), 5) for ids in fam.values() for a, b in itertools.combinations(ids, 2)
                if sum(1 for j in fam.values() if a in j and b in j) == 2})
    return dict(V=len(V), faces=dict(sorted(fk.items())), edges=E, radii=sorted({round(float(x), 5) for x in np.linalg.norm(V, axis=1)}))
def axes(Q):
    hq = ConvexHull(Q); ed = {tuple(sorted((a, b))) for sm in hq.simplices for a, b in [(sm[0], sm[1]), (sm[1], sm[2]), (sm[0], sm[2])]}
    return [eq[:3] for eq in hq.equations], [Q[b] - Q[a] for a, b in ed]
def overlaps(pieces, limit=None):
    pieces = [Q for Q in pieces if vol(Q) > 1e-12]   # flat pieces (a corner in the plane of its tips) take no space
    AX = [axes(Q) for Q in pieces]; C = [Q.mean(0) for Q in pieces]; R = [np.linalg.norm(Q - Q.mean(0), axis=1).max() for Q in pieces]
    bad = 0
    for i, j in itertools.combinations(range(len(pieces)), 2):
        if np.linalg.norm(C[i] - C[j]) > R[i] + R[j] + 1e-9: continue
        sepd = False
        for ax in AX[i][0] + AX[j][0] + [np.cross(u, v) for u in AX[i][1] for v in AX[j][1]]:
            nn = np.linalg.norm(ax)
            if nn < 1e-12: continue
            pa, pb = pieces[i] @ (ax / nn), pieces[j] @ (ax / nn)
            if pa.max() <= pb.min() + 1e-7 or pb.max() <= pa.min() + 1e-7: sepd = True; break
        if not sepd:
            bad += 1
            if limit and bad >= limit: return bad
    return bad
def core_of(V, F, t):
    FI = faces_info(V, F); tips = [t * c * n for _, n, c in FI]
    fam = {}
    for (f, n, c), tp in zip(FI, tips): fam.setdefault((len(f), round(c, 7)), []).append(tp)
    H = []
    for k, T in fam.items():
        T = np.array(T)
        if len(T) >= 4 and np.linalg.matrix_rank(T - T.mean(0), tol=1e-9) == 3: H.append(pl(T))
    if not H: return None, len(fam)
    return cut(np.vstack(H)), len(fam)
def treat(item):
    try: return treat1(item)
    except Exception as e: return dict(name=item[0], D=item[1], file=item[2], verdict='error: ' + type(e).__name__ + ' ' + str(e).splitlines()[0][:120])
def treat1(item):
    name, dnum, fn = item
    d, V, F = load(fn); V = V - V.mean(0); res = dict(name=name, D=dnum, file=fn, symmetry=d.get('symmetry', {}).get('schoenflies'), convex=d.get('checks', {}).get('convex', True), corners=len(V), faces=len(F))
    FI = faces_info(V, F); res['centre_inside_every_face'] = bool(min(c for _, _, c in FI) > 1e-9)
    VS = polyvol(V, F); pyr = [np.vstack([V[f], np.zeros(3)]) for f, _, _ in FI]
    res['pyramids_add_up'] = bool(res['centre_inside_every_face'] and abs(sum(map(vol, pyr)) - VS) < 1e-7 * VS)
    res['face_families'] = len({(len(f), round(c, 7)) for f, _, c in FI})
    if not res['pyramids_add_up']:
        res['verdict'] = 'no star core: the solid is not made of its pyramids from the centre'; return res
    for tn, t in (('phi', phi), ('2', 2.0)):
        r = {}; tips = np.array([t * c * n for _, n, c in FI])
        spikes = [np.vstack([V[f], tp]) for (f, _, _), tp in zip(FI, tips)]
        star = VS + sum(map(vol, spikes)); r['star_over_solid'] = star / VS
        H = tips[ConvexHull(tips).vertices] if np.linalg.matrix_rank(tips, tol=1e-9) == 3 else None
        r['halo'] = shape(tips); VH = vol(tips); r['halo_over_solid'] = VH / VS
        hp = pl(tips); ins = lambda Q: bool(np.all(Q @ hp[:, :3].T + hp[:, 3] <= 1e-8))
        r['star_inside_halo'] = all(ins(Q) for Q in spikes) and ins(V)
        if res['convex'] and r['star_inside_halo']:
            fa = {v: [i for i, (f, _, _) in enumerate(FI) if v in f] for v in range(len(V))}
            E = sorted({tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f, _, _ in FI for i in range(len(f))})
            L1 = [np.vstack([V[v]] + [tips[i] for i in fa[v]]) for v in range(len(V))] + [np.vstack([V[a], V[b]] + [tips[i] for i in fa[a] if i in fa[b]]) for a, b in E]
            s1 = sum(map(vol, L1)); r['layer_pieces'] = len(L1); r['layer_fills'] = bool(abs(s1 - (VH - star)) < 1e-7 * VH)
            r['overlaps'] = overlaps([V] + spikes + L1, limit=5) if len(L1) < 1500 else None
        C, nf = core_of(V, F, t)
        if C is not None:
            r['core'] = shape(C); r['core_is_shape'] = r['core'] == shape(V) if res['convex'] else None
            CH = ConvexHull(C); CF = []
            for eq in CH.equations:
                ids = [i for i, p in enumerate(C) if abs(eq[:3] @ p + eq[3]) < 1e-8]
                c0 = C[ids].mean(0); u = C[ids[0]] - c0; w = np.cross(eq[:3], u)
                CF.append([i for _, i in sorted((np.arctan2((C[i] - c0) @ w, (C[i] - c0) @ u), i) for i in ids)])
            CF = [list(x) for x in {tuple(sorted(f)): f for f in CF}.values()]
            C2, _ = core_of(C, CF, t)
            r['core_core'] = shape(C2) if C2 is not None else None
            r['core_returns_to_shape'] = (r['core_core'] == shape(V)) if (C2 is not None and res['convex']) else False
        else: r['core'] = None
        res[tn] = r
    p = res['phi']
    res['verdict'] = ('star fills; core returns (period two)' if p.get('core_returns_to_shape') else
                      'star fills; core does not return' if p.get('layer_fills') else
                      'star outside its halo' if not p.get('star_inside_halo') else 'star inside halo, layer does not fill')
    return res
if __name__ == '__main__':
    rows = [r for r in csv.DictReader(l for l in open(os.path.join(DS, 'index.csv'), encoding='utf8') if not l.startswith('#'))]
    items = [(r['name'], r['universal_number'], r['dataset_file']) for r in rows if r['status'] == 'new' and r['in_dataset'] == 'y' and r['kind'] in ('solid', 'piece')]
    os.makedirs(OUT, exist_ok=True); out = []
    with mp.Pool(JOBS) as pool:
        for res in pool.imap_unordered(treat, items):
            out.append(res); print(res['D'], res['name'], '|', res['verdict'], flush=True)
            json.dump(sorted(out, key=lambda r: int(r['D'][1:]) if r['D'][1:].isdigit() else 999), open(os.path.join(OUT, 'star-cores.json'), 'w'), indent=1, default=float)
    print('done', len(out))
