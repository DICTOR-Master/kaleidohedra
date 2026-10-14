# Six decagonal wheels (DICTO, 2026-10-14): DICTO asked whether adding wheels turns the cuboctahedron's 4 hexagonal wheels into an
# icosahedral network. Regular hexagonal wheels cannot do it: 4 is the most planes that can share their hexagons' diameters
# (each plane meets the others in exactly its 3 diameters only for the cuboctahedron). The icosahedral counterpart has 6 wheels,
# one in each plane perpendicular to a 5-fold axis, and each wheel is a decagon: the icosidodecahedron's 6 great decagons. Its
# centre-to-edge triangles are golden triangles (sides phi, phi, 1, apex 36°), the same triangles as FUJI's short faces. Corners
# blunted as in the hexagonal wheels; thin plates; writes paper/figures/wheels-ico.json. DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
ico = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float)
E = [(a, b) for a, b in itertools.combinations(range(12), 2) if abs(np.linalg.norm(ico[a] - ico[b]) - 2) < 1e-9]
V = np.array([(ico[a] + ico[b]) / 2 for a, b in E]); V /= np.linalg.norm(V[0] - V[[i for i in range(30) if abs(np.linalg.norm(V[0] - V[i]) - min(np.linalg.norm(V[0] - V[j]) for j in range(1, 30))) < 1e-9][0]])
axes = [ico[i] / np.linalg.norm(ico[i]) for i in range(12) if (ico[i] > 0).sum() + (abs(ico[i]) < 1e-9).sum() * 0 >= 0][:]
axes = [a for a in axes if a @ np.array([1e-3, 2e-3, 3e-3]) > 0]
assert len(axes) == 6
cut = 0.18                         # corner cut, as a fraction of the unit edge
T = 0.035 * np.linalg.norm(V[0])
verts, faces, tags = [], [], []
def plate(poly, n, tag):
    b = len(verts); k = len(poly)
    for p in poly: verts.append(list(p + n * T / 2))
    for p in poly: verts.append(list(p - n * T / 2))
    faces.append(list(range(b, b + k))); tags.append(tag); faces.append(list(range(b + 2 * k - 1, b + k - 1, -1))); tags.append(tag)
    for i in range(k): faces.append([b + i, b + k + i, b + k + (i + 1) % k, b + (i + 1) % k]); tags.append('edge')
for w, n in enumerate(axes):
    ring = [v for v in V if abs(v @ n) < 1e-9]; assert len(ring) == 10
    a = ring[0] / np.linalg.norm(ring[0]); bvec = np.cross(n, a); ring = sorted(ring, key=lambda v: math.atan2(v @ bvec, v @ a))
    for i in range(10):
        tri = [np.zeros(3), ring[i], ring[(i + 1) % 10]]; poly = []
        for j in range(3):
            P, Q = tri[j], tri[(j + 1) % 3]; L = np.linalg.norm(Q - P); poly += [P + (Q - P) / L * cut, Q + (P - Q) / L * cut]
        plate(poly, n, f'w{w}')
R = np.linalg.norm(V[0]); print(f'circumradius / edge = {R:.6f} (phi = {phi:.6f}); triangles {6 * 10}')
json.dump({'wheels_ico': dict(v=verts, f=faces, t=tags)}, open(os.path.join(ROOT, 'paper', 'figures', 'wheels-ico.json'), 'w'))
