#!/usr/bin/env python3
"""LQG bridge (DICTO 4 Nov, "Zeptoverse"): a loop-quantum-gravity quantum of space is a polyhedron fixed by its face normals and areas (Minkowski;
Bianchi–Doná–Speziale 2011). For our fixed-normal families, place every member in LQG's area space (area of each normal class / total area) and
mark which members can tile flat space: Dehn zero (necessary, dehn.py v2) and the local edge-angle count (every dihedral closes round an edge with
the solid's own dihedrals: sum k_i θ_i = 2π, or = π beside a face, k >= 0 integers, k_own >= 1). Known tilers are checked as calibration.
Expected (today's results): tilers are isolated points in the area space."""
import sys, json, math, itertools, numpy as np
from collections import Counter
from scipy.spatial import ConvexHull, HalfspaceIntersection
sys.argv = [sys.argv[0], 'x', '8', '300']; exec(open('scripts/dehn.py').read().split("if __name__")[0])
CUBE = [np.eye(3)[i]*s for i in range(3) for s in (1, -1)]; OCT = [np.array(s, float) for s in itertools.product((1, -1), repeat=3)]
RDN = [np.array(p, float) for p in {tuple(s*x for s, x in zip(sg, q)) for q in itertools.permutations((1, 1, 0)) for sg in itertools.product((1, -1), repeat=3)}]
TET = [np.array(v, float) for v in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
def solid(pl):
    H = np.array([[*n, -c] for n, c in pl]); return np.unique(np.round(HalfspaceIntersection(H, np.zeros(3)).intersections, 10), axis=0)
def classify(n, classes):
    for name, ns in classes:
        if any(np.allclose(n/np.linalg.norm(n), m/np.linalg.norm(m), atol=1e-6) for m in ns): return name
    return '?'
def angle_ok(angs):
    """local count: every dihedral appears in a closure k·θ = 2π (or π) with nonneg integers, own coefficient >= 1"""
    A = sorted(set(round(a, 9) for a in angs)); ok = True
    for i, a in enumerate(A):
        found = False
        for ks in itertools.product(range(0, 7), repeat=len(A)):
            if ks[i] == 0: continue
            s = sum(k*x for k, x in zip(ks, A))
            if abs(s - 2*math.pi) < 1e-7 or abs(s - math.pi) < 1e-7: found = True; break
        ok &= found
        if not ok: break
    return ok
def analyse(pl, classes):
    P = solid(pl); h = ConvexHull(P); X, F = hull_faces(P[h.vertices])
    area = Counter()
    for f in F:
        V = X[f]; n = np.cross(V[1] - V[0], V[2] - V[0]); n /= np.linalg.norm(n); c = V.mean(0)
        a = 0.5*abs(sum(np.dot(np.cross(V[i] - c, V[(i + 1) % len(V)] - c), n) for i in range(len(V))))
        area[classify(n, classes)] += a
    tot = sum(area.values()); rows = dehn(X, F, rows_only=True); angs = [t for L, t in rows]
    return {'area_share': {k: round(v/tot, 6) for k, v in sorted(area.items())}, 'dehn0': dehn(X, F)['dehn_zero'], 'angle_count_ok': angle_ok(angs),
            'IQ': 36*math.pi*h.volume**2/h.area**3, 'corners': int(len(h.vertices))}
FAM = {
 'cube ∩ μ·octahedron': (lambda m: [(n, 1.0) for n in CUBE] + [(n, m) for n in OCT], np.linspace(1.01, 2.99, 199), [('square', CUBE), ('triangle', OCT)], {1.5: 'TO (tiles)', 3.0: 'cube (tiles)'}),
 'CO ∩ μ·RD': (lambda m: [(n, 1.0) for n in CUBE] + [(n, 2.0) for n in OCT] + [(n, m) for n in RDN], np.linspace(1.001, 1.999, 200), [('square', CUBE), ('triangle', OCT), ('rhombus', RDN)], {1.0: 'RD (tiles)'}),
 'tetrahedron ∩ μ·(−tetrahedron)': (lambda m: [(-n, 1.0) for n in TET] + [(n, m) for n in TET], np.linspace(1.01, 2.99, 199), [('T face', [-n for n in TET]), ('−T face', TET)], {2.0: 'T(4) minus corners (tiles)'}),
}
out = {}
for name, (fam, rng, classes, known) in FAM.items():
    rows = []
    for m in rng:
        try: r = analyse(fam(float(m)), classes); r['mu'] = float(m); rows.append(r)
        except Exception as e: pass
    pas = [r for r in rows if r['dehn0'] and r['angle_count_ok']]
    print(f"{name}: {len(rows)} members; Dehn 0: {sum(r['dehn0'] for r in rows)}; angle count ok: {sum(r['angle_count_ok'] for r in rows)}; both: {len(pas)} at μ = {[round(r['mu'], 3) for r in pas][:12]}", flush=True)
    for km, lab in known.items():
        try: r = analyse(fam(km), classes); print(f"   calibration {lab} μ={km}: Dehn0 {r['dehn0']}, angle ok {r['angle_count_ok']}, area share {r['area_share']}", flush=True)
        except Exception as e: print('   calibration', lab, 'err', e)
    out[name] = {'rows': rows, 'pass': pas}
json.dump(out, open('data/bridge.json', 'w'), indent=1)
