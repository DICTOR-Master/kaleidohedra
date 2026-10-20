# DICTO 2026-10-20 (float): how many of the Jewel's 96 edges lie on the 15 two-fold axes of the icosahedral group of its dodecahedron
# (the edge condition of every independent claim of Lalvani, US 4,723,382).  python3 lalvani_edges.py <studies/2026-10-19-og-gyrated-octet>
import sys, os, itertools, numpy as np
exec(open(os.path.join(sys.argv[1], 'jewel_twin.py')).read().split("V = np.array(verts)")[0])
V = np.array(verts); E = {tuple(sorted((o[i], o[(i + 1) % len(o)]))) for o in faces for i in range(len(o))}
D = np.array([c for c in itertools.product((1, -1), repeat=3)] + [[0, a / PHI, b * PHI] for a in (1, -1) for b in (1, -1)]
             + [[a / PHI, b * PHI, 0] for a in (1, -1) for b in (1, -1)] + [[b * PHI, 0, a / PHI] for a in (1, -1) for b in (1, -1)], float)
el = min(np.linalg.norm(a - b) for a, b in itertools.combinations(D, 2)); ax = []
for a, b in itertools.combinations(D, 2):
    if abs(np.linalg.norm(a - b) - el) < 1e-9:
        u = (a + b) / np.linalg.norm(a + b)
        if not any(abs(abs(u @ w) - 1) < 1e-9 for w in ax): ax.append(u)
rh = {tuple(sorted((o[i], o[(i + 1) % 4]))) for o in faces if len(o) == 4 for i in range(4)}
on = lambda e: any(abs(abs((V[e[0]] - V[e[1]]) / np.linalg.norm(V[e[0]] - V[e[1]]) @ w) - 1) < 1e-9 for w in ax)
print(f'two-fold axes {len(ax)}; edges {len(E)}; window edges on axes {sum(on(e) for e in E if e in rh)}/{len(rh)}; other edges on axes {sum(on(e) for e in E if e not in rh)}/{len(E) - len(rh)}')
