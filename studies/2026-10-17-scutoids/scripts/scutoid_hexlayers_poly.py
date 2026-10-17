# DICTO 2026-10-17: "go ahead with the scutoids" — after the voxel run (scutoid_hexlayers.py): pin the best stacked-tile setting without
# voxel error, then reshape the weakest piece (the outer piece over a pentagon). Same construction as scutoid_hexlayers.py, except (DICTO 10-17) each layer is a flat slab and bundles meet only sideways: bundles (core TI +
# strict scutoid layer, sweep continuing outward) on a hexagonal-prism lattice, x to the bundle that reaches it first, inside a bundle to the
# plane that reaches it last. Here every piece is computed as a polyhedron: its sweep cell (convex) minus each neighbour's "got there first"
# region (convex), i.e. a union of convex parts. Volume from the parts; surface = all part faces minus the faces shared between two parts of
# the same piece (coplanar overlap, 2D clipping). Float arithmetic (not exact rational): labelled "polyhedral (float)".
# build() keeps a stacking offset (s1, s2) for reference only; DICTO rejected shifted layers 10-17, so the search uses s1 = s2 = 0. -> data/scutoid-hexlayers-poly.txt
import sys, json, itertools, numpy as np
from scipy.optimize import linprog, minimize
from scipy.spatial import HalfspaceIntersection, ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(p): return [p, [p[1], p[2], p[0]], [p[2], p[0], p[1]]]
ICO = np.array([c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1, s2 * phi])], float)
DOD = np.array([[a, b, c] for a in (1, -1) for b in (1, -1) for c in (1, -1)] + [c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1 * phi, s2 / phi])], float)
diag = np.array([abs(abs(v[0]) - abs(v[1])) < 1e-9 and abs(abs(v[1]) - abs(v[2])) < 1e-9 for v in DOD])
N = np.vstack([ICO, DOD[diag], DOD[~diag]]); G = ['P'] * 12 + ['Hd'] * 8 + ['Ho'] * 12
TI = []
for b in ([0, 1, 3 * phi], [1, 2 + phi, 2 * phi], [phi, 2, phi ** 3]):
    for c in cyc(b):
        for s in itertools.product((1, -1), repeat=3): TI.append([c[k] * s[k] for k in range(3)])
TI = np.unique(np.round(TI, 9), axis=0); dA = (TI @ N.T).max(0)
EPS = 1e-9

def tau_rows(D, c):
    # tau_k(x) = (n_k·x - n_k·c - dA_k)/D_k = a_k·x + b_k
    return N / D[:, None], -(N @ c + dA) / D

def clean(A, b):
    k = np.linalg.norm(A, axis=1) > 1e-12
    if (b[~k] < -1e-12).any(): return A[:0], b[:0], False
    return A[k], b[k], True

def cheb(A, b):
    # largest ball inside {A x <= b}; returns (centre, radius) or None
    A, b, ok = clean(A, b)
    if not ok: return None
    nr = np.linalg.norm(A, axis=1)
    r = linprog(np.r_[np.zeros(3), -1], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    if r.status != 0 or r.x[3] < 1e-7: return None
    return r.x[:3], r.x[3]

def poly(A, b):
    A, b, ok = clean(A, b)
    cc = cheb(A, b) if ok else None
    if cc is None: return None
    hs = HalfspaceIntersection(np.c_[A, -b], cc[0]); V = hs.intersections; H = ConvexHull(V)
    faces = []
    for i in range(len(A)):
        on = np.abs(V @ A[i] - b[i]) < 1e-7 * max(1, np.linalg.norm(A[i]))
        if on.sum() < 3: continue
        P = V[on]; n = A[i] / np.linalg.norm(A[i]); o = P.mean(0); u = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(n, u)
        ang = np.arctan2((P - o) @ w, (P - o) @ u); P = P[np.argsort(ang)]
        faces.append((n, float(n @ P[0]), P))
    return dict(V=V, vol=H.volume, faces=faces)

def area3(P):
    s = np.zeros(3)
    for i in range(len(P)): s += np.cross(P[i], P[(i + 1) % len(P)])
    return np.linalg.norm(s) / 2

def clip2(p, q):
    # convex polygon p ∩ convex polygon q (both CCW 2D); Sutherland–Hodgman
    out = p
    for i in range(len(q)):
        a, b = q[i], q[(i + 1) % len(q)]; inp = out; out = []
        if not len(inp): break
        def side(x): return (b[0] - a[0]) * (x[1] - a[1]) - (b[1] - a[1]) * (x[0] - a[0])
        for j in range(len(inp)):
            cur, prv = inp[j], inp[j - 1]; sc, sp = side(cur), side(prv)
            if sc >= -1e-12:
                if sp < -1e-12: out.append(prv + (cur - prv) * sp / (sp - sc))
                out.append(cur)
            elif sp >= -1e-12: out.append(prv + (cur - prv) * sp / (sp - sc))
        out = np.array(out)
    return out

def a2(P):
    return 0.5 * abs(sum(P[i][0] * P[i - 1][1] - P[i - 1][0] * P[i][1] for i in range(len(P)))) if len(P) >= 3 else 0.0

def shared_area(f, g):
    # f, g on the same plane with opposite normals: project both into f's plane basis, order CCW, clip
    n = f[0]; u = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(n, u)
    def ccw(P):
        Q = np.c_[P @ u, P @ w]; o = Q.mean(0); return Q[np.argsort(np.arctan2(Q[:, 1] - o[1], Q[:, 0] - o[0]))]
    return a2(clip2(ccw(f[2]), ccw(g[2])))

def union_measure(parts):
    vol = sum(p['vol'] for p in parts); A = sum(area3(f[2]) for p in parts for f in p['faces'])
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            for f in parts[i]['faces']:
                for g in parts[j]['faces']:
                    if f[0] @ g[0] < -1 + 1e-9 and abs(f[1] + g[1]) < 1e-7: A -= 2 * shared_area(f, g)
    return vol, A

def psi(vol, A): return np.pi ** (1 / 3) * (6 * vol) ** (2 / 3) / A

def subtract(pieces, S):
    # pieces: list of (A,b) convex; S: (A,b) convex. returns pieces \ S
    out = []
    for A, b in pieces:
        if cheb(np.r_[A, S[0]], np.r_[b, S[1]]) is None: out.append((A, b)); continue
        AA, bb = A, b
        for i in range(len(S[0])):
            na, nb = np.r_[AA, -S[0][i:i + 1]], np.r_[bb, -S[1][i]]
            if cheb(na, nb) is not None: out.append((na, nb))
            AA, bb = np.r_[AA, S[0][i:i + 1]], np.r_[bb, S[1][i]]
            if cheb(AA, bb) is None: break
    return out

def build(gP, gHd, gHo, af, cf, s1=0.0, s2=0.0, slab=True):
    g = np.array([{'P': gP, 'Hd': gHd, 'Ho': gHo}[x] for x in G]); D = dA * (g - 1)
    rB = max(dA * g / np.linalg.norm(N, axis=1)); a, c = af * 2 * rB, cf * 2 * rB
    A1 = a * np.array([1, -1, 0]) / 2 ** .5; A2 = a * np.array([1, 0, -1]) / 2 ** .5; A3 = c * np.ones(3) / 3 ** .5 + s1 * A1 + s2 * A2
    cell = abs(np.dot(A1, np.cross(A2, A3)))
    imgs = [i * A1 + j * A2 + k * A3 for i in range(-4, 5) for j in range(-4, 5) for k in range(-3, 4)]
    imgs = [p for p in imgs if 1e-9 < np.linalg.norm(p) < 2.2 * (2 * rB) * max(af, cf, 1)]
    a0, b0 = tau_rows(D, np.zeros(3)); box = 3 * max(a, c)
    BOX = (np.vstack([np.eye(3), -np.eye(3)]), np.full(6, box))
    if slab:
        # DICTO 10-17: "outwards at the sides is okay if they still tile space, but up or down is a no-no": each layer a slab with flat top
        # and bottom (planes ⊥ (1,1,1) at ±c/2); bundles meet only their own layer's neighbours
        u = np.ones(3) / 3 ** .5; BOX = (np.vstack([BOX[0], u, -u]), np.r_[BOX[1], c / 2, c / 2])
        imgs = [p for p in imgs if abs(p @ u) < 1e-9]
    res = {'cell': cell, 'pieces': {}, 'touch_box': False}
    Ttot = 0.0
    for zone in ('core', 'layer', 'outer'):
        for j in (range(32) if zone != 'core' else [None]):
            if zone == 'core': A, b = a0, -b0                     # tau_k <= 0
            else:
                A = a0 - a0[j]; b = b0[j] - b0                     # tau_k <= tau_j
                if zone == 'layer': A = np.r_[A, -a0[j:j + 1], a0[j:j + 1]]; b = np.r_[b, b0[j], 1 - b0[j]]
                else: A = np.r_[A, -a0[j:j + 1]]; b = np.r_[b, b0[j] - 1]
            A = np.r_[A, BOX[0]]; b = np.r_[b, BOX[1]]
            pcs = [(A, b)]; full = None
            if zone != 'outer': full = poly(A, b)
            for cimg in imgs:
                ac, bc = tau_rows(D, cimg)
                # neighbour got there first: tau^c_k < tau^0_j for all k   (core: T^c < T^0 is not convex; core must be untouched: T^c >= 0)
                if zone == 'core': S = (ac, -bc)
                else: S = (ac - a0[j], b0[j] - bc)
                pcs = subtract(pcs, S)
                if not pcs: break
            parts = [p for p in (poly(A_, b_) for A_, b_ in pcs) if p is not None]
            if not parts: continue
            if any(np.abs(p['V']).max() > box * (1 - 1e-6) for p in parts): res['touch_box'] = True
            vol, ar = union_measure(parts)
            Ttot += vol
            key = zone if zone == 'core' else f'{zone} {G[j]}{j}'
            res['pieces'][key] = dict(vol=vol, area=ar, psi=psi(vol, ar), parts=len(parts), lost=(full['vol'] - vol) if full else 0.0)
    res['sum_vs_cell'] = Ttot / cell
    return res

def score(res):
    ps = res['pieces']; lost = sum(v['lost'] for k, v in ps.items() if not k.startswith('outer'))
    lay = min(v['psi'] for k, v in ps.items() if k.startswith('layer')); out = min(v['psi'] for k, v in ps.items() if k.startswith('outer'))
    return dict(least_layer=lay, least_outer=out, lost_rel=lost / res['cell'], sum_vs_cell=res['sum_vs_cell'], touch_box=res['touch_box'])

def kinds(res):
    out = {}
    for k, v in res['pieces'].items():
        kk = k.rstrip('0123456789')
        out.setdefault(kk, []).append(round(v['psi'], 3))
    return {k: (min(v), max(v)) for k, v in out.items()}

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'pin'
    lines = ['DICTO · dictospheres.com', 'Stacked hexagonal-prism tiles of scutoid bundles — polyhedral (float), not voxel']
    if mode == 'pin':
        for prm in ((1.85, 1.95, 2.10, 1.4, 1.1), (1.85, 1.95, 2.10, 1.25, 1.1), (1.6, 1.7, 1.85, 1.4, 1.1)):
            r = build(*prm); s = score(r)
            lines.append(f'  voxel best {prm}: least scutoid {s["least_layer"]:.3f}, least outer {s["least_outer"]:.3f}, layer lost {s["lost_rel"]:.2e} of a cell, pieces sum {s["sum_vs_cell"]:.6f} of a cell, box {s["touch_box"]}')
            lines.append(f'     by kind (min, max ψ): {kinds(r)}'); print(lines[-2]); print(lines[-1], flush=True)
        open('data/scutoid-hexlayers-poly-pin.txt', 'w').write('\n'.join(lines) + '\n')
    else:
        # search: maximise min(least scutoid, least outer) with the layer intact; x = (gP, gHd, gHo, af, cf)
        best = [None, -1]
        def f(x):
            try: r = build(*x); s = score(r)
            except Exception as e: return 1.0
            if s['lost_rel'] > 1e-6 or abs(s['sum_vs_cell'] - 1) > 1e-6 or s['touch_box']: return 1.0
            v = min(s['least_layer'], s['least_outer'])
            if v > best[1]: best[0], best[1] = (list(map(float, x)), s, kinds(r)), v; print(json.dumps(dict(x=best[0][0], **{k: float(w) for k, w in s.items()}, kinds=best[0][2])), flush=True)
            return -v
        # DICTO 10-17: no stacking shift ("they won't stand up and be equal by themselves"): layers straight, s1 = s2 = 0
        starts = [(1.85, 1.95, 2.10, 1.4, 1.1), (1.6, 1.7, 1.85, 1.4, 1.1), (1.85, 1.95, 2.10, 1.25, 1.1), (2.0, 2.0, 2.0, 1.3, 1.0)]
        for x0 in starts:
            minimize(f, x0, method='Nelder-Mead', options=dict(maxfev=int(sys.argv[2]) if len(sys.argv) > 2 else 150, xatol=1e-3, fatol=1e-4, initial_simplex=None))
        x, s, k = best[0]
        lines += [f'  best found: least of scutoids and outer pieces {best[1]:.3f}', f'  settings (gP, gHd, gHo, in-layer spacing, layer height): {[round(v, 4) for v in x]}',
                  f'  {s}', f'  by kind (min, max ψ): {k}', '  comparison: voxel best 0.697 (≈0.67); RD closing 0.578; hex prism closing 0.586; cube 0.806']
        print('\n'.join(lines)); open('data/scutoid-hexlayers-poly.txt', 'w').write('\n'.join(lines) + '\n')
