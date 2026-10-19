# Export the DICTO Belted Triacontahedron (DBT), its OG, the octahedron and the two removed corners for the 3D page (float).
import json, sys, numpy as np
exec(open('belted.py').read().split("faces = {}")[0])
def polys(P, H):
    out = []
    for eq in H:
        on = np.where(np.abs(P @ eq[:3] + eq[3]) < 1e-8)[0]
        if len(on) < 3: continue
        c = P[on].mean(0); nrm = eq[:3]; a = P[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(nrm, a)
        on = sorted(on, key=lambda i: np.arctan2((P[i] - c) @ b, (P[i] - c) @ a)); out.append([int(i) for i in on])
    return out
dbt = polys(P, H)
RT = np.unique(np.round(HalfspaceIntersection(H[:30], np.zeros(3)).intersections, 10), axis=0)
top = RT[np.argmax(RT @ n3)]; bot = RT[np.argmin(RT @ n3)]
cut = [p for p in P if abs(abs(p @ n3) - R / 3 ** .5) < 1e-8]
keys = []
for pole in (top, bot):
    base = [p for p in cut if np.sign(p @ n3) == np.sign(pole @ n3)]; keys.append([pole.tolist()] + [b.tolist() for b in base])
og = ConvexHull(V); ogeq = []
for e in og.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in ogeq): ogeq.append(e)
ogf = polys(V, np.array(ogeq))
O6 = [[R, 0, 0], [-R, 0, 0], [0, R, 0], [0, -R, 0], [0, 0, R], [0, 0, -R]]
# rotate so the belt axis (1,1,1) points up (y)
z = n3; x = np.cross([0, 1, 0], z); x /= np.linalg.norm(x); y = np.cross(z, x); M = np.array([x, z, -y])
rot = lambda A: (np.asarray(A) @ M.T).round(6).tolist()
json.dump({'mark': 'DICTO · dictospheres.com', 'dbt': {'v': rot(P), 'f': dbt}, 'og': {'v': rot(V), 'f': ogf}, 'octa': rot(O6),
           'keys': [rot(k) for k in keys], 'volume': round(h.volume, 6)}, open(sys.argv[1], 'w'))
print('DBT faces', len(dbt), 'sizes', sorted(len(f) for f in dbt)[:3], '...', '| OG faces', len(ogf))
