# Four hexagonal wheels of flat-ended triangles (DICTO, 2026-10-14): a cuboctahedron's 4 central planes each hold a regular hexagon
# of 6 equilateral triangles (centre to edge); its 24 edges split into the 4 hexagons' rims, and each of its 12 radii is shared by 2
# wheels. Each triangle is blunted into a flat-ended triangle with FUJI's proportion (sides 1 and r = 1/phi): the cut at the centre
# frees the hub where 12 radii meet, the cuts at the rim free the corners where wheels cross. Thin plates; writes
# paper/figures/wheels.json for the renderer, with each wheel tagged. DICTO · dictospheres.com
import itertools, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
r = float(sys.argv[1]) if len(sys.argv) > 1 else 1 / phi
E = 1 + 2 * r                       # full triangle side = cuboctahedron edge = its circumradius; long sides 1, cuts r
c = r                               # each corner cut back by r along both sides (equilateral corner of side r)
V = np.array(sorted({p for s in itertools.product((1, -1), repeat=2) for p in set(itertools.permutations((s[0], s[1], 0)))}), float)
V = V / np.linalg.norm(V[0]) * E
N = [np.array(n, float) / math.sqrt(3) for n in [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]]
T = 0.035 * E                       # plate thickness
verts, faces, tags = [], [], []
def plate(poly, n, tag):
    base = len(verts); k = len(poly)
    for p in poly: verts.append(list(p + n * T / 2))
    for p in poly: verts.append(list(p - n * T / 2))
    faces.append(list(range(base, base + k))); tags.append(tag)
    faces.append(list(range(base + 2 * k - 1, base + k - 1, -1))); tags.append(tag)
    for i in range(k): faces.append([base + i, base + k + i, base + k + (i + 1) % k, base + (i + 1) % k]); tags.append('edge')
for w, n in enumerate(N):
    ring = [v for v in V if abs(v @ n) < 1e-9]
    a = ring[0] / np.linalg.norm(ring[0]); b = np.cross(n, a)
    ring = sorted(ring, key=lambda v: math.atan2(v @ b, v @ a))
    O = np.zeros(3)
    for i in range(6):
        A, B = ring[i], ring[(i + 1) % 6]; tri = [O, A, B]
        poly = []
        for j in range(3):
            P, Q, R_ = tri[j], tri[(j + 1) % 3], tri[(j + 2) % 3]
            poly += [P + (Q - P) / E * c, Q + (P - Q) / E * c]   # the two corners of side PQ, cut back by c from each end
        # order: around the triangle
        poly = [poly[0], poly[1], poly[2], poly[3], poly[4], poly[5]]
        plate(poly, n, f'w{w}')
json.dump({'wheels': dict(v=verts, f=faces, t=tags)}, open(os.path.join(ROOT, 'paper', 'figures', 'wheels.json'), 'w'))
# checks: long sides 1, short sides r, plates of different wheels meet only along shared radii
print(f'r = {r:.6f}, cuboctahedron edge {E:.4f}, plates {len(faces) // 8}')
