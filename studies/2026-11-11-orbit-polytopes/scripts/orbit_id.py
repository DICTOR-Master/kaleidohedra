"""Orbit polytopes from one corner (DICTO 11 Nov: "identify / chase down the remainder of reflection-group orbit polytopes by seeing one
corner and discerning the hyper-cube"). Given a solid's corners (any dimension, centred), find:
  1. its full symmetry group (orthogonal maps permuting the corners), its order;
  2. the reflections among them and the group W they generate (identified by order: A3 24, B3 48, H3 120; A4 120, B4 384, F4 1152,
     H4 14400; products allowed);
  3. whether the corners are ONE W-orbit; if so, the seed labels: the corner moved into W's fundamental chamber, its inner products
     with W's simple roots (zero = that mirror is not used).
Float geometry (tolerance 1e-7), labels recognised exactly where simple. Controls first (CONTROLS); then the solids given in a JSON file."""
import itertools, json, sys
import numpy as np
TOL = 1e-7
HULL = '--hull' in sys.argv
sys.argv = [a for a in sys.argv if a != '--hull']
def centred(V): V = np.array(V, float); return V - V.mean(0)
def sym_group(V):
    """all orthogonal maps (as permutation of corners + matrix) preserving V; built from images of a frame of corners"""
    n, d = V.shape
    # frame: d linearly independent corners of the smallest norm class
    norms = np.round(np.linalg.norm(V, axis=1), 6)
    frame = []
    for i in np.argsort(norms):
        cand = frame + [i]
        if np.linalg.matrix_rank(V[cand], tol=1e-6) == len(cand): frame = cand
        if len(frame) == d: break
    F = V[frame]; G = F @ F.T
    mats = []
    by_norm = {}
    for i, nr in enumerate(norms): by_norm.setdefault(nr, []).append(i)
    pools = [by_norm[norms[f]] for f in frame]
    def rec(k, chosen):
        if k == d:
            Img = V[chosen]
            if not np.allclose(Img @ Img.T, G, atol=1e-6): return
            M = np.linalg.solve(F, Img).T            # M @ F[i] = Img[i]
            if not np.allclose(M @ M.T, np.eye(d), atol=1e-6): return
            W = V @ M.T
            # every image must be a corner
            from scipy.spatial import cKDTree
            t = cKDTree(V); dd, _ = t.query(W)
            if np.all(dd < 1e-6): mats.append(M)
            return
        for j in pools[k]:
            if j in chosen: continue
            ok = all(abs(V[j] @ V[chosen[i]] - G[k, i]) < 1e-6 for i in range(k))
            if ok: rec(k + 1, chosen + [j])
    rec(0, [])
    return mats
def reflections(mats):
    R = []
    for M in mats:
        w = np.linalg.eigvalsh((M + M.T) / 2)
        if np.isclose(np.linalg.det(M), -1) and np.allclose(M, M.T, atol=1e-7) and np.sum(np.isclose(w, -1, atol=1e-6)) == 1:
            ev, vec = np.linalg.eigh(M); r = vec[:, np.argmin(ev)]; R.append(r / np.linalg.norm(r))
    return R
def generated(R, d, cap=20000):
    I = np.eye(d); gens = [I - 2 * np.outer(r, r) for r in R]; G = [I]; seen = {tuple(np.round(I, 6).ravel())}; frontier = [I]
    while frontier and len(G) < cap:
        nf = []
        for A in frontier:
            for S in gens:
                B = S @ A; k = tuple(np.round(B, 6).ravel())
                if k not in seen: seen.add(k); G.append(B); nf.append(B)
        frontier = nf
    return G
def identify(name, V, expect=None):
    V = centred(V); n, d = V.shape
    mats = sym_group(V); R = reflections(mats); W = generated(R, d) if R else [np.eye(d)]
    orbit = {tuple(np.round(M @ V[0], 6)) for M in W}; single = len(orbit) == n
    # seed labels: choose a generic point to fix a chamber; simple roots = reflections whose mirror bounds the chamber of that point
    labels = None
    if single and R:
        Rs = []
        for r in R:
            if not any(np.allclose(r, s, atol=1e-6) or np.allclose(r, -s, atol=1e-6) for s in Rs): Rs.append(r)
        p = np.array([1.0, 0.31, 0.073, 0.0119][:d]) + 1e-3
        Rs = [r if r @ p > 0 else -r for r in Rs]
        # simple roots: positive roots not a positive combination of two others (bounding walls): keep r if the chamber point's nearest mirror set
        # practical: move V[0] into the chamber by reflections, then labels = inner products with walls that bound the chamber
        x = V[0].copy()
        for _ in range(200):
            bad = [r for r in Rs if r @ x < -1e-9]
            if not bad: break
            r = bad[0]; x = x - 2 * (r @ x) * r
        # walls of the chamber {y: r.y >= 0 for all r}: those r for which the chamber has a facet on r.y = 0 (LP-free test via generic interior pts)
        from scipy.optimize import linprog
        simple = []
        for r in Rs:
            A = [-(s) for s in Rs if not np.allclose(s, r)]
            res = linprog(c=-np.zeros(d), A_ub=np.array(A) if A else None, b_ub=np.zeros(len(A)) if A else None, A_eq=r.reshape(1, -1), b_eq=[0], bounds=[(-1, 1)] * d)
            # r bounds the chamber if there is a point on r.y = 0 strictly inside the other half-spaces: maximise slack
            Aub = np.hstack([np.array(A), np.ones((len(A), 1))]) if A else None
            res = linprog(c=np.r_[np.zeros(d), -1], A_ub=Aub, b_ub=np.zeros(len(A)) if A else None, A_eq=np.r_[r, 0].reshape(1, -1), b_eq=[0], bounds=[(-1, 1)] * d + [(0, 1)])
            if res.success and -res.fun > 1e-7: simple.append(r)
        labels = [round(float(r @ x), 6) for r in simple]
    verdict = f'ORBIT of a reflection group of order {len(W)} ({len(R)} mirrors), seed labels {labels}' if single and R else ('NOT an orbit of its reflections' + (f' (symmetry group {len(mats)}, reflections {len(R)}, one reflection-orbit has {len(orbit)} of {n} corners)'))
    ok = '' if expect is None else ('  [control PASS]' if (expect == bool(single and R)) else '  [control FAIL]')
    print(f'{name}: {n} corners, symmetry group {len(mats)}: {verdict}{ok}', flush=True)
    return {'name': name, 'corners': n, 'sym': len(mats), 'mirrors': len(R), 'W': len(W), 'orbit': bool(single and R), 'labels': labels}, (expect is None or expect == bool(single and R))
def signed_perms(t): return sorted({tuple(s * c for s, c in zip(sg, p)) for p in itertools.permutations(t) for sg in itertools.product((1, -1), repeat=3)})
def even_perms(t):
    return [p for p in itertools.permutations(t) if sum(1 for i in range(3) for j in range(i + 1, 3) if p.index(t[i]) > p.index(t[j])) % 2 == 0]
def cyc_signed(t):
    out = set()
    for k in range(3):
        c = t[k:] + t[:k]
        for sg in itertools.product((1, -1), repeat=3): out.add(tuple(s * x for s, x in zip(sg, c)))
    return sorted(out)
tau = (1 + 5 ** .5) / 2
snub_xi = 1.839286755214161
CONTROLS = [
 ('cube', signed_perms((1, 1, 1)), True), ('octahedron', signed_perms((1, 0, 0)), True), ('cuboctahedron', signed_perms((1, 1, 0)), True),
 ('truncated octahedron', signed_perms((2, 1, 0)), True), ('truncated cube', signed_perms((1, 1, 2 ** .5 - 1)), True),
 ('rhombicuboctahedron', signed_perms((1 + 2 ** .5, 1, 1)), True), ('truncated cuboctahedron', signed_perms((1 + 2 * 2 ** .5, 1 + 2 ** .5, 1)), True),
 ('icosahedron', cyc_signed((0, 1, tau)), True), ('icosidodecahedron', sorted(set(signed_perms((tau, 0, 0))[:0]) | set(cyc_signed((0, 0, tau))) | set(cyc_signed((0.5, tau / 2, tau * tau / 2)))), True),
 ('snub cube (chiral: mirrors absent)', sorted({tuple(s * c for s, c in zip(sg, p)) for p in [(1, 1 / snub_xi, snub_xi), (1 / snub_xi, snub_xi, 1), (snub_xi, 1, 1 / snub_xi)] for sg in itertools.product((1, -1), repeat=3) if (sg[0] * sg[1] * sg[2]) == 1} | {tuple(s * c for s, c in zip(sg, p)) for p in [(1 / snub_xi, 1, snub_xi), (1, snub_xi, 1 / snub_xi), (snub_xi, 1 / snub_xi, 1)] for sg in itertools.product((1, -1), repeat=3) if (sg[0] * sg[1] * sg[2]) == -1}), False),
 ('rhombic dodecahedron (two kinds of corner)', signed_perms((1, 1, 1)) + signed_perms((2, 0, 0)), False),
]
if __name__ == '__main__':
    out = []; ok = True
    print('CONTROLS', flush=True)
    for name, V, exp in CONTROLS:
        r, good = identify(name, V, exp); out.append(r); ok &= good
    if len(sys.argv) > 1:
        print('SOLIDS', flush=True)
        S = [s for s in json.load(open(sys.argv[1]))]
        for k, s in enumerate(S):
            V = np.unique(np.round(np.array(s['corners'], float), 9), axis=0)
            if HULL:
                from scipy.spatial import ConvexHull
                try: hv = np.unique(np.round(V[ConvexHull(V).vertices], 9), axis=0)
                except Exception: hv = V
                convex = len(hv) == len(V); V = hv
            else: convex = None
            if len(V) > 120 or len(V) < 4 or np.linalg.matrix_rank(V - V.mean(0), tol=1e-7) < 3: print(f"skip {s['id']} ({len(V)} corners)", flush=True); continue
            try: r, _ = identify(f"{s['id']} | {s['name']}", V); r['id'] = s['id']; r['convex'] = convex; out.append(r)
            except Exception as e: print(f"error {s['id']}: {e}", flush=True)
            print(f'PROGRESS {(k + 1) / len(S):.3f} {k + 1}/{len(S)}', flush=True)
    json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else 'orbit_results.json', 'w'), indent=1)
    print('FINAL ok' if ok else 'FINAL FAIL (a control failed)')
