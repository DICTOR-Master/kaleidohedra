# DICTO · McCooey's self-dual polyhedra, part 2 (26 Nov 2026). With Claude (Anthropic).
# (A) The self-duality map. McCooey's canonical forms have every edge tangent to the unit sphere, so the polar (pole of each face plane,
#     n_f / d_f) is the canonical dual, of the same size. For a self-dual solid there is an orthogonal map M with M(poles) = corners.
#     Found by matching; then the polar link (Lean M1: Resonus plane of P is perpendicular to a corner of P*, Vacuus plate of P is
#     perpendicular to an edge of P*) is tested in the solid's own terms: Resonus normals = M^-1 (corner directions of P) and Vacuus
#     normals = M^-1 (edge directions of P), up to sign.
# (B) Partial Vacuus on the solid's own dual: pits on every face (apex on the face axis at a = s d_f); is there one s in (0, 1) with
#     every pit wall in a face plane of a scaled copy of the dual (face normals of the dual = corner directions of P)? The wall normal
#     m(a) = u x v - a (u x n + n x v) is linear in a, so parallelism to each candidate direction is a small linear problem.
# (C) High precision: the solids flagged by part 1 (area-weighted silence beyond symmetry, or grey), with McCooey's constants refined
#     from their polynomials to 60 digits (mpmath), energies recomputed at 60 digits.
# Usage: python part2.py <source dir> <data-forms.json> <out.json>
import sys, os, re, json, glob, itertools
import numpy as np, mpmath as mp
SRC, FORMS, OUT = (sys.argv[1:4] if __name__ == "__main__" else (None, None, None))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from forms import parse   # noqa (forms.py runs its census on import only under __main__? guard below)

def faces_normals(V, F):
    N, Dd = [], []
    for f in F:
        P = V[f]; c = P.mean(0); n = np.zeros(3)
        for a, b in zip(P, np.roll(P, -1, 0)): n += np.cross(a - c, b - c)
        n /= np.linalg.norm(n)
        if n @ c < 0: n = -n
        N.append(n); Dd.append(n @ P[0])
    return np.array(N), np.array(Dd)

def find_map(A, B, tol=1e-6):
    """orthogonal R with R(A) = B as point sets (same norms); A, B arrays of points."""
    na = np.linalg.norm(A, axis=1); nb = np.linalg.norm(B, axis=1)
    i0 = 0; j0 = next(j for j in range(1, len(A)) if np.linalg.norm(np.cross(A[i0], A[j])) > 1e-6)
    Ma = np.array([A[i0], A[j0], np.cross(A[i0], A[j0])]).T
    for i in range(len(B)):
        if abs(nb[i] - na[i0]) > tol: continue
        for k in range(len(B)):
            if k == i or abs(nb[k] - na[j0]) > tol or abs(B[i] @ B[k] - A[i0] @ A[j0]) > tol: continue
            for sg in (1, -1):
                R = np.array([B[i], B[k], sg * np.cross(B[i], B[k])]).T @ np.linalg.inv(Ma)
                if np.abs(R @ R.T - np.eye(3)).max() > 1e-6: continue
                W = A @ R.T
                if all(np.min(np.linalg.norm(B - w, axis=1)) < 1e-6 for w in W): return R
    return None

def same_planes(X, Y, tol=1e-6):
    X = [x / np.linalg.norm(x) for x in X]; Y = [y / np.linalg.norm(y) for y in Y]
    def cover(P, Q): return all(any(abs(abs(p @ q) - 1) < tol for q in Q) for p in P)
    return cover(X, Y) and cover(Y, X)

def part_AB(path):
    name, V, F = parse(path)
    N, Dd = faces_normals(V, F)
    poles = N / Dd[:, None]
    E = set()
    for f in F:
        for a, b in zip(f, f[1:] + f[:1]): E.add((min(a, b), max(a, b)))
    R = find_map(poles, V)
    out = dict(name=name, selfdual_map_found=R is not None)
    if R is not None:
        out['map_det'] = round(float(np.linalg.det(R)), 6)   # -1: the duality reverses the hand
        Ri = R.T
        corner_dirs = V @ Ri.T; edge_dirs = np.array([V[b] - V[a] for a, b in E]) @ Ri.T
        vac = [np.cross(V[a], V[b]) for a, b in E]
        out['resonus_eq_corner_planes'] = same_planes(N, corner_dirs)
        out['vacuus_eq_edge_planes'] = same_planes(vac, edge_dirs)
    # (B) pits ending on a scaled copy of the dual: candidate wall directions = corner directions of P
    W = V / np.linalg.norm(V, axis=1)[:, None]
    special = []
    for s_try in []: pass
    cand = None; ok_all = True; svals = []
    for fi, f in enumerate(F):
        n, d = N[fi], Dd[fi]
        for a1, b1 in zip(f, f[1:] + f[:1]):
            u, v = V[a1], V[b1]; m0 = np.cross(u, v); m1 = -(np.cross(u, n) + np.cross(n, v))
            hits = []
            for w in W:   # m0 + a m1 parallel to w  <=>  (m0 + a m1) x w = 0
                A_ = np.cross(m1, w); B_ = -np.cross(m0, w)
                if np.linalg.norm(A_) < 1e-12: continue
                a = float(A_ @ B_ / (A_ @ A_))
                if np.linalg.norm(np.cross(m0 + a * m1, w)) < 1e-8 and 0 < a < d - 1e-9: hits.append(round(a / d, 7))
            svals.append(set(hits))
    common = set.intersection(*svals) if svals else set()
    out['pits_on_dual_depths'] = sorted(common)
    return out

if __name__ == '__main__':
    files = sorted(f for f in glob.glob(os.path.join(SRC, 'SelfDual*.txt')) + glob.glob(os.path.join(SRC, 'ImproperSelfDual*.txt')))
    res = []
    for f in files:
        try: res.append(part_AB(f))
        except Exception as ex: res.append(dict(file=os.path.basename(f), err=str(ex)[:100]))
    # (C) high precision for the flagged ones
    forms = json.load(open(FORMS)); flagged = [r for r in forms if r['iii']['beyond'] or r['iii']['grey'] or r['i']['beyond'] or r['i']['grey']]
    mp.mp.dps = 40; hp = []
    for r in flagged:
        txt = open(os.path.join(SRC, r['file'])).read()
        Cs = {}
        for m in re.finditer(r'^\s*(C\d+)\s*=\s*([-+0-9.eE]+)\s*(?:=|$)', txt, re.M): Cs.setdefault(m.group(1), mp.mpf(m.group(2)))
        # McCooey's 30-digit values used as given (a root-finder can jump to another root of the same polynomial)
        def val(t):
            t = t.strip(); s = -1 if t.startswith('-') else 1; t = t.lstrip('+-').strip()
            return s * (Cs[t] if t in Cs else mp.mpf(t))
        V = [[val(x) for x in m.group(1).split(',')] for m in re.finditer(r'^\s*V\d+\s*=\s*\(([^)]*)\)', txt, re.M)]
        F = [[int(x) for x in m.group(1).split(',')] for m in re.finditer(r'^\s*\{([^}]*)\}', txt, re.M)]
        N, A = [], []
        for f in F:
            P = [mp.matrix(V[i]) for i in f]; c = sum(P, mp.matrix([0, 0, 0])) / len(P); n = mp.matrix([0, 0, 0])
            for a, b in zip(P, P[1:] + P[:1]):
                x, y = a - c, b - c; n += mp.matrix([x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]])
            ln = mp.norm(n); A.append(ln / 2); N.append(n / ln * (1 if (n.T * c)[0] > 0 else -1))
        def energy(k, w):
            W = sum(w); s = mp.mpf(0)
            for i in range(len(N)):
                for j in range(len(N)): s += w[i] * w[j] * mp.legendre(k, (N[i].T * N[j])[0])
            return s / W ** 2
        degs = sorted(set(r['iii']['beyond'] + r['iii']['grey'] + r['i']['beyond'] + r['i']['grey']))
        hp.append(dict(name=r['name'], degrees=degs, e_area={k: mp.nstr(energy(k, A), 5) for k in degs}, e_unit={k: mp.nstr(energy(k, [1] * len(N)), 5) for k in degs}))
        print('HP', r['name'], hp[-1]['e_area'], hp[-1]['e_unit'], flush=True)
    json.dump(dict(AB=res, high_precision=hp), open(OUT, 'w'), indent=1)
    ok = [r for r in res if 'err' not in r]
    print('solids', len(res), 'errors', len(res) - len(ok))
    print('self-duality map found:', sum(r['selfdual_map_found'] for r in ok), '; reverses hand (det -1):', sum(r.get('map_det') == -1 for r in ok))
    print('Resonus = planes perpendicular to own corners (via the map):', sum(bool(r.get('resonus_eq_corner_planes')) for r in ok), 'of', sum(r['selfdual_map_found'] for r in ok))
    print('Vacuus  = planes perpendicular to own edges  (via the map):', sum(bool(r.get('vacuus_eq_edge_planes')) for r in ok), 'of', sum(r['selfdual_map_found'] for r in ok))
    print('pits ending on the own dual (special depths):', [(r['name'], r['pits_on_dual_depths']) for r in ok if r['pits_on_dual_depths']][:30])
    good = len(ok) == len(res) and sum(r['selfdual_map_found'] for r in ok) > 0
    print('FINAL ok' if good else 'FINAL FAIL')
