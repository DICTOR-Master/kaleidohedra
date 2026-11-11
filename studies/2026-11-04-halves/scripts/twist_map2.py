"""Rerun of twist_map.py with the corrections of 4 Nov: twist Dehn = solid Dehn (additivity); the deciding necessary test for a convex twist is the
edge-angle count with coplanar faces merged (angle_hybrids.py). Candidates = twist convex & solid Dehn zero & twist angle count passes."""
import math, json, itertools, numpy as np
exec(open('scripts/twist_map.py').read().split("phi = (1")[0])
src = open('~/study-runs/2026-11-04-lqg-bridge/scripts/angle_hybrids.py').read()
exec(src[src.index('def dihedrals'):src.index('N = np.array')])
phi = (1 + 5**.5)/2
rows = []; cand = []
for mu in np.round(np.linspace(1.02, 2.98, 50), 4):
    for nu in np.round(np.linspace(1.0, 1.98, 50), 4):
        try:
            P = solid(float(mu), float(nu)); h = ConvexHull(P); P = P[h.vertices]; h = ConvexHull(P)
            def half(top):
                Hs = np.vstack([h.equations, [0, 0, -1 if top else 1, 0]]); return HalfspaceIntersection(Hs, np.array([0, 0, 1e-3 if top else -1e-3])).intersections
            T, B = half(True), half(False); U = np.unique(np.round(np.vstack([T, B @ rz(math.pi/3).T]), 7), axis=0); hu = ConvexHull(U)
            conv = abs(hu.volume - h.volume) < 1e-6*h.volume
            if not conv: continue
            X, F = hull_faces(P); d0 = dehn(X, F)['dehn_zero']
            angs, nf = dihedrals(U); ok, bad = closes(angs)
            r = {'mu': float(mu), 'nu': float(nu), 'dehn0': bool(d0), 'twist_angle_ok': bool(ok), 'twist_faces': nf, 'twist_dihedrals': angs}
            rows.append(r)
            if d0 and ok: cand.append(r); print('CANDIDATE', json.dumps(r), flush=True)
        except Exception: pass
print('twist-convex members', len(rows), '| Dehn zero', sum(r['dehn0'] for r in rows), '| angle count ok', sum(r['twist_angle_ok'] for r in rows), '| candidates', len(cand))
json.dump({'rows': rows, 'candidates': cand}, open('data/twist-map2.json', 'w'), indent=1)
