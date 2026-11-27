import json, numpy as np, mpmath as mp
mp.mp.dps = 30
A = json.load(open('/tmp/all_stars.json'))
sh = next(s for s in A if s['D'] == 'D71' and s['t'] == '2'); T = sh['turns'][2]
V = np.array(T['solid']['vertices']); V -= V.mean(0); F = T['solid']['faces']
tri = [f for f in F if len(f) == 3]; hexa = [f for f in F if len(f) == 6]
lt = np.mean([np.linalg.norm(V[f[i]] - V[f[(i + 1) % 3]]) for f in tri for i in range(3)])
tri_e = {tuple(sorted((f[i], f[(i + 1) % 3]))) for f in tri for i in range(3)}
lh = np.mean([np.linalg.norm(V[f[i]] - V[f[(i + 1) % 6]]) for f in hexa for i in range(6) if tuple(sorted((f[i], f[(i + 1) % 6]))) not in tri_e])
# truncation depth along the edge of the parent tetrahedron: parent edge L = lh + 2 lt; cut fraction u = lt / L
L = lh + 2 * lt; u = lt / L; ratio = lh / lt
# distances of the triangle and hexagon planes from the centre
dt = np.mean([abs(np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]) / np.linalg.norm(np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]])) @ V[f[0]]) for f in tri])
dh = np.mean([abs(np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]) / np.linalg.norm(np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]])) @ V[f[0]]) for f in hexa])
for name, x in (('hexagon side / triangle side', ratio), ('cut fraction of the parent edge', u), ('triangle plane / hexagon plane distance', dt / dh)):
    x = mp.mpf(float(x))
    print(name, mp.nstr(x, 15), '| identify:', mp.identify(x, ['sqrt(2)', 'sqrt(3)', 'sqrt(5)', 'sqrt(6)'], tol=1e-11),
          '| polynomial (deg <= 4):', mp.findpoly(x, 4, maxcoeff=2000, tol=1e-11))
