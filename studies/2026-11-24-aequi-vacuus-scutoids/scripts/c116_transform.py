"""DICTO's Hollow-straw as he means it (27 Nov 2026): a TRANSFORMATION with both ends fixed. With Claude (Anthropic).
DICTO: "start and end shapes fixed, a balloon-like drinking straw between each pair of faces, all straws pumped up together until
they meet"; "I have never wanted or asked for the core to be the same as the outer... it is a transformation!!!"; "yes build it".
Ends: C116 in its OWN shape (the floating-resin placement, data/cells/stand/amber_c116-layer0float_*.json: solid_V, solid_faces) and
Minana #377 fixed around it (same frame: Minana scaled by the layer's s). Pairing sigma (onefloor_float.json): C116 face k -> Minana face
sigma(k). Every plane written a . x = 1 (O inside both). Motion: a_k(lam) = (1 - lam) a_k + lam m_sigma(k), lam 0 -> 1, all faces
together (straight-line motion of each face's polar point: the face turns and moves at once). P(lam) = {x : a_k(lam) . x <= 1 all k}.
Straw k = the region swept by face k of P(lam). Checks along a fine lam grid:
  (1) ends: P(0) has C116's face pattern, P(1) Minana's (combinatorially, under sigma);
  (2) every face present at every lam (each straw joins its two faces);
  (3) NESTING: P(lam) grows (every face moves outward at every corner: (m - a_k) . x <= 0 on face k), so the straws do not overlap
      and fill the shell exactly;
  (4) the pattern changes = swaps: each a lost neighbour pair and a gained one at one lam; expect the 18 swaps of the floor, no others.
Numerical first (floats, grid + bisection on each change); exact form only if it holds. Output data/c116/transform.json."""
import os, sys, json
import numpy as np
from scipy.spatial import HalfspaceIntersection
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
R = json.load(open(os.path.join(ROOT, 'data/cells/stand/amber_c116-layer0float_layer_6-5_cen.json')))
sig = {int(k): int(v) for k, v in json.load(open(os.path.join(ROOT, 'data/c116/onefloor_float.json')))['pairing'].items()}
C116f = json.load(open(os.path.join(ROOT, 'data/c116/pairing.json')))['faces']
S = A.build("aequus-377"); s = float(R['s'])
MV = np.array([[float(c) for c in v] for v in S['V']]) * s
M = []
for u, c in S['planes']:
    uf = np.array([float(x) for x in u]); M.append(uf / (float(c) * s))
M = np.array(M)
assert np.allclose(np.abs(M @ MV.T).max(axis=1), 1, atol=1e-9) and (M @ MV.T <= 1 + 1e-9).all(), 'Minana planes in the layer frame'
CV = np.array(R['solid_V']); CF = R['solid_faces']
Ak = []
for f in CF:
    X = CV[f]; c0 = X.mean(0); n = np.linalg.svd(X - c0)[2][2]; n = n if n @ c0 > 0 else -n; Ak.append(n / (n @ c0))
Ak = np.array(Ak)
assert (Ak @ CV.T <= 1 + 1e-7).all(), 'core planes'
assert all(len(CF[k]) == len(C116f[k]) for k in range(60))
Mk = np.array([M[sig[k]] for k in range(60)])
print('core radius', np.linalg.norm(CV, axis=1).min(), np.linalg.norm(CV, axis=1).max(), '; Minana radius', np.linalg.norm(MV, axis=1).min(), np.linalg.norm(MV, axis=1).max(), flush=True)
def state(lam):
    A_ = (1 - lam) * Ak + lam * Mk
    H = HalfspaceIntersection(np.hstack([A_, -np.ones((60, 1))]), np.zeros(3)); P = H.intersections
    sc = np.abs(P).max(); pts = []
    for p in P:
        if not any(np.linalg.norm(p - q) < 1e-9 * sc for q in pts): pts.append(p)
    P = np.array(pts); tight = np.abs(A_ @ P.T - 1) < 1e-8
    faces = [set(np.where(tight[k])[0]) for k in range(60)]
    pairs = {(k, l) for k in range(60) for l in range(k + 1, 60) if len(faces[k] & faces[l]) >= 2}
    present = all(len(f) >= 3 for f in faces)
    out = True                                    # nesting: face k moves outward at all its corners
    for k in range(60):
        if faces[k] and ((Mk[k] - Ak[k]) @ P[list(faces[k])].T).max() > 1e-9: out = False
    deg4 = int((tight.sum(0) >= 4).sum())
    return pairs, present, out, deg4, len(P)
def pairs_of(fl):
    at = {}
    for k, F in enumerate(fl):
        for v in F: at.setdefault(v, set()).add(k)
    return {(a, b) for S_ in at.values() for a in S_ for b in S_ if a < b}
inv = {v: k for k, v in sig.items()}
want0 = pairs_of(C116f)
want1 = {tuple(sorted((inv[a], inv[b]))) for a, b in pairs_of([vs for vs, kk in S['faces']])}
NG = int(os.environ.get('NG', 2000)); lams = np.linspace(0, 1, NG + 1)
prev = None; events = []; all_present = True; all_out = True; bad_lam = []
for i, lam in enumerate(lams):
    pairs, present, out, deg4, nv = state(lam)
    if i == 0: print('start pattern = C116 under the pairing:', pairs == want0, '; corners', nv, flush=True)
    if i == NG: print('end pattern = Minana #377 under the pairing:', pairs == want1, '; corners', nv, flush=True)
    all_present &= present; all_out &= out
    if not out: bad_lam.append(float(lam))
    if prev is not None and pairs != prev:
        events.append(dict(lam=float(lam), lost=sorted(prev - pairs), gained=sorted(pairs - prev)))
    prev = pairs
    if i % (NG // 10) == 0: print(f'PROGRESS {i / NG:.2f} lam {lam:.3f} corners {nv} pairs {len(pairs)} all faces {present} growing {out}', flush=True)
# refine every change between its two grid points (the S6 symmetry makes a swap's 6 images happen at one lam)
fine = []
for e in events:
    lo = e['lam'] - 1.0 / NG; sub = np.linspace(lo, e['lam'], 801); pv = state(lo)[0]
    for lam in sub[1:]:
        pr = state(lam)[0]
        if pr != pv: fine.append(dict(lam=float(lam), lost=sorted(pv - pr), gained=sorted(pr - pv)))
        pv = pr
events = fine
FL = json.load(open(os.path.join(ROOT, 'data/c116/onefloor_float.json')))['swaps']     # [gained pair, lost pair] per swap
floor = {(tuple(sorted(g)), tuple(sorted(l))) for g, l in FL if l}
def as_swaps(e):   # pair each lost pair with the gained pair on the same four faces
    out = []
    for l in e['lost']:
        g = [g for g in e['gained'] if len(set(l) | set(g)) == 4 and all(tuple(sorted(q)) in (want0 | want1) for q in [(l[0], g[0]), (l[0], g[1]), (l[1], g[0]), (l[1], g[1])])]
        out.append((tuple(g[0]) if len(g) == 1 else None, tuple(l)))
    return out
matched = [(g, l) for e in events for g, l in as_swaps(e)]
print('swap times (lam) and counts:', sorted({(round(e['lam'], 5), len(e['lost'])) for e in events}), flush=True)
print('every change is a set of single swaps of the floor:', all(g is not None and (tuple(sorted(g)), tuple(sorted(l))) in floor for g, l in matched), '; swaps', len(matched), flush=True)
swaps = [e for e in events if len(e['lost']) == len(e['gained'])]
other = [e for e in events if len(e['lost']) != len(e['gained'])]
lost = sorted({p for e in events for p in e['lost']}); gained = sorted({p for e in events for p in e['gained']})
print('pattern changes:', len(events), '; single swaps', len(swaps), '; other changes', len(other), flush=True)
print('pairs lost overall', len(set(map(tuple, lost)) - want1), 'gained overall', len(set(map(tuple, gained)) - want0), '(the floor has 18 and 18)', flush=True)
print('every face present throughout:', all_present, '; nested (every face moves outward everywhere):', all_out, flush=True)
if bad_lam: print('not growing at lam in', min(bad_lam), '..', max(bad_lam), '(', len(bad_lam), 'grid points )', flush=True)
for e in other[:10]: print('  other change at lam', round(e['lam'], 4), 'lost', e['lost'], 'gained', e['gained'], flush=True)
json.dump(dict(events=events, all_present=all_present, nested=all_out, bad_lam=bad_lam[:200]), open(os.path.join(ROOT, 'data/c116/transform.json'), 'w'))
ok_run = len(events) > 0
good = all_out and all_present and len(matched) == 18 and all(g is not None and (tuple(sorted(g)), tuple(sorted(l))) in floor for g, l in matched)
print('RESULT:', "DICTO's transformation WORKS (numerically): nested, every face throughout, exactly the 18 swaps of the floor" if good else 'not yet: see the checks above')
print('FINAL ok' if ok_run else 'FINAL FAIL (no pattern change seen)')
