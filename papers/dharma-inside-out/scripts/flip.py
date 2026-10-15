# Flip test (DICTO, queued 2026-10-13; run 2026-10-16): every piece of each Spheres of Dharma skin turned over through the sphere midway
# between its two solids, as a physical half-turn (DICTO's choice): a half-turn about a line on the midway sphere, at the point on the
# piece's own axis halfway between the inner and outer solid. Symmetric pieces: the line in a mirror plane (= reflection in the midway
# plane). Twisted pieces: the line's angle searched, best fit kept. Measured per skin: overlaps, gaps, new inner/outer extent.
import json, sys, itertools, numpy as np
from scipy.spatial import ConvexHull
D = json.load(open(sys.argv[1]))
SKINS = [('I -> ID', ['npyr5', 'nfru3']), ('ID -> D', ['npyr3']), ('D -> TI', ['nfru5', 'nt1']), ('TI -> Hecatodihedron', ['ncap7']),
         ('Hecatodihedron -> RT', ['ncap6', 'nwedge']), ('RT -> I(phi^2)', ['nedge', 'nface'])]
def role(r, V): return f'ncap{len(V)}' if r == 'ncap' else r
pieces = [(role(r, V), np.array(V, float)) for r, V, *_ in D]
core = [P for r, P in pieces if r == 'core'][0]
H = lambda P: ConvexHull(P)
def ray(hull, u):
    n, d = hull.equations[:, :3], hull.equations[:, 3]; nu = n @ u; m = nu > 1e-12
    return np.min(-d[m] / nu[m])
def mirror_ok(P, u):
    """Is the piece symmetric under some mirror plane containing its axis u? Returns that plane's in-plane direction t."""
    c = P.mean(0)
    for v in P:
        w = v - c; t = w - (w @ u) * u
        if np.linalg.norm(t) < 1e-9: continue
        t /= np.linalg.norm(t); nrm = np.cross(u, t)        # plane spanned by u, t through c
        R = P - 2 * np.outer((P - c) @ nrm, nrm)
        if all(np.min(np.linalg.norm(P - r, axis=1)) < 1e-4 for r in R): return t
    return None
def halfturn(P, p, t):
    return 2 * (p + np.outer((P - p) @ t, t)) - P
def inside(eqs, X): return np.all(X @ eqs[:, :3].T + eqs[:, 3] <= 1e-7, axis=1)
def sep(P, Q):
    hp, hq = ConvexHull(P), ConvexHull(Q); A = [e[:3] for e in hp.equations] + [e[:3] for e in hq.equations]
    E1 = [P[j] - P[i] for s in hp.simplices for i, j in itertools.combinations(s, 2)][:40]; E2 = [Q[j] - Q[i] for s in hq.simplices for i, j in itertools.combinations(s, 2)][:40]
    A += [np.cross(a, b) / np.linalg.norm(np.cross(a, b)) for a in E1 for b in E2 if np.linalg.norm(np.cross(a, b)) > 1e-9]
    return max(max(Q @ n) * 0 + max(min(Q @ n) - max(P @ n), min(P @ n) - max(Q @ n)) for n in A)
rng = np.random.default_rng(7); dirs = rng.normal(size=(240, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
inner_pts = core; out = []
for name, roles in SKINS:
    skin = [P for r, P in pieces if r in roles]
    Hin = H(inner_pts); Hout = H(np.vstack([inner_pts] + skin))
    flipped, kinds = [], {}
    for P in skin:
        u = P.mean(0) / np.linalg.norm(P.mean(0)); rmid = (ray(Hin, u) + ray(Hout, u)) / 2; p = rmid * u
        t = mirror_ok(P, u)
        if t is not None: flipped.append(halfturn(P, p, t)); kinds['mirror'] = kinds.get('mirror', 0) + 1; continue
        # twisted piece: search the line's angle round u, keep the one whose flipped piece sticks out least past the original band
        a = np.cross(u, [0.3, 0.5, 0.8]); a /= np.linalg.norm(a); b = np.cross(u, a); best = None
        for th in np.linspace(0, np.pi, 73)[:-1]:
            tt = np.cos(th) * a + np.sin(th) * b; F = halfturn(P, p, tt)
            score = -min(np.min(F @ e[:3] + e[3]) for e in [np.zeros(4)]) if False else np.max(F @ Hout.equations[:, :3].T + Hout.equations[:, 3])
            if best is None or score < best[0]: best = (score, F)
        flipped.append(best[1]); kinds['twisted'] = kinds.get('twisted', 0) + 1
    # overlaps among flipped pieces (nearby pairs)
    worst, npairs = 0.0, 0
    for P, Q in itertools.combinations(flipped, 2):
        cp, cq = P.mean(0), Q.mean(0)
        if np.linalg.norm(cp - cq) > np.linalg.norm(P - cp, axis=1).max() + np.linalg.norm(Q - cq, axis=1).max(): continue
        npairs += 1; worst = min(worst, sep(P, Q))
    # coverage along rays: gaps and double cover between the flipped skin's first and last covered radius
    E = [ConvexHull(F).equations for F in flipped]
    rmax = max(np.linalg.norm(F, axis=1).max() for F in flipped) * 1.01; rs = np.linspace(0, rmax, 500)
    gaps = dbl = cov = 0; rin, rou = [], []
    for u in dirs:
        X = np.outer(rs, u); k = sum(inside(e, X).astype(int) for e in E)
        idx = np.where(k > 0)[0]
        if not len(idx): continue
        seg = k[idx[0]: idx[-1] + 1]; cov += len(seg); gaps += int((seg == 0).sum()); dbl += int((seg > 1).sum())
        rin.append(rs[idx[0]]); rou.append(rs[idx[-1]])
    oi = [ray(Hin, u) for u in dirs]; oo = [ray(Hout, u) for u in dirs]
    # the midway surface: the original skin covers every point halfway between its two solids; how much do the flipped pieces cover?
    M = np.array([(ray(Hin, u) + ray(Hout, u)) / 2 * u for u in rng.normal(size=(4000, 3)) / 1 for u in [u / np.linalg.norm(u)]])
    km = sum(inside(e, M).astype(int) for e in E); midcov = (km >= 1).mean(); middbl = (km >= 2).mean()
    # how much of the flipped skin's volume lies inside the old inner solid (it would have to give way)
    vin = sum(ConvexHull(F).volume for F in flipped)
    Xs = rng.uniform(-rmax, rmax, size=(60000, 3)); inF = np.zeros(len(Xs), bool)
    for e in E: inF |= inside(e, Xs)
    into_inner = (inF & inside(Hin.equations, Xs)).sum() / max(inF.sum(), 1)
    out.append(f'{name}: {len(skin)} pieces ({kinds}); worst overlap depth {worst:.4f} over {npairs} nearby pairs; along 240 rays: '
               f'midway surface covered {midcov:.1%} (twice {middbl:.1%}); {into_inner:.1%} of the flipped pieces lies inside the old inner solid; radial gaps {gaps / cov:.1%}; inner radius {min(rin):.4f}-{max(rin):.4f} (was {min(oi):.4f}-{max(oi):.4f}), '
               f'outer {min(rou):.4f}-{max(rou):.4f} (was {min(oo):.4f}-{max(oo):.4f})')
    print(out[-1], flush=True)
    inner_pts = np.vstack([inner_pts] + skin)
open('data/flip-dharma.txt', 'w').write('\n'.join(out) + '\n')
