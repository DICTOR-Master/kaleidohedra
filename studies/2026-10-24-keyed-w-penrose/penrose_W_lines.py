# Keyed W, option 2 (DICTO 10-24): the Penrose rhomb pattern (picture A, edge OG/phi, centred on the socket) as LINES: each rhomb edge
# inside the free band becomes a ridge on W's 4 bump faces and the same line a groove on its 4 dent faces (Fable review 4 pairing and
# symmetry), so every W is identical and the ridges of one W seat in the grooves of its neighbour. Built exactly with manifold3d.
import json, math, cmath, os, numpy as np, manifold3d as m3
from shapely.geometry import Polygon, LineString
from scipy.spatial import ConvexHull
H = os.path.dirname(os.path.abspath(__file__)); G = json.load(open(os.path.join(H, 'keyed-W-geometry.json')))
R = G['R']; m = np.array(G['m']); cell = np.array(G['cell']); U, Wv, N = (np.array(G['frame'][k]) for k in ('U', 'W', 'N'))
tri = np.array(G['face1_triangle_uv']); Sh = np.array(G['shadow_uv']); OV = np.array(G['ocd_V']); phi = (1 + 5 ** .5) / 2
OGE = max(np.linalg.norm(OV[i] - OV[j]) for i in range(len(OV)) for j in range(i) if np.linalg.norm(OV[i] - OV[j]) < 0.5); L = OGE / phi
HR, WIDTH, WALL = 0.025, 0.045, 30.0            # ridge height (about 1 mm at print scale), base width, wall angle off the normal
xyz = lambda p: p[0] * U + p[1] * Wv
def subdivide(tris):
    out = []
    for c, a, b, cc in tris:
        if c == 0: p = a + (b - a) / phi; out += [(0, cc, p, b), (1, p, cc, a)]
        else: q = b + (a - b) / phi; r = b + (cc - b) / phi; out += [(1, r, cc, a), (1, q, r, b), (0, r, q, a)]
    return out
LEV = 7; tris = []
for i in range(10):
    b = cmath.rect(L * phi ** LEV, (2 * i - 1) * math.pi / 10); c = cmath.rect(L * phi ** LEV, (2 * i + 1) * math.pi / 10)
    if i % 2 == 0: b, c = c, b
    tris.append((0, 0j, b, c))
for _ in range(LEV): tris = subdivide(tris)
k = lambda z: (round(z.real, 7), round(z.imag, 7)); segs = set()
for c, a, b, cc in tris:                        # rhomb edges are each half-triangle's two short sides (a-b, a-cc); the base b-cc is the rhomb's diagonal
    for p, q in ((a, b), (a, cc)): segs.add(tuple(sorted([k(p), k(q)])))
allowed = Polygon(tri).buffer(-0.035, join_style=2).difference(Polygon(Sh).buffer(0.025, join_style=2))
lines = []
for p, q in segs:
    piece = LineString([p, q]).intersection(allowed.buffer(-WIDTH / 2, join_style=2))
    for g in (getattr(piece, 'geoms', None) or [piece]):
        if g.geom_type == 'LineString' and g.length >= 0.06: lines.append(np.array(g.coords))
print(f'OG edge {OGE:.4f}, rhomb edge {L:.4f}; rhomb edges in the pattern {len(segs)}; ridge lines on face 1: {len(lines)}, total length {sum(np.linalg.norm(l[1] - l[0]) for l in lines):.3f}')
def ridge(p, q, sign):                          # trapezoid prism along p-q in face 1's plane, raised (+N) or sunk (-N)
    d = (q - p) / np.linalg.norm(q - p); n2 = np.array([-d[1], d[0]]); top = WIDTH / 2 - HR * math.tan(math.radians(WALL))
    base = [p + n2 * WIDTH / 2, p - n2 * WIDTH / 2, q - n2 * WIDTH / 2, q + n2 * WIDTH / 2]; up = [p + n2 * top, p - n2 * top, q - n2 * top, q + n2 * top]
    lift = sign * HR; pts = [xyz(x) - sign * 0.002 * N for x in base] + [xyz(x) + lift * N for x in up]   # 0.002 overlap into the face so the union welds
    return np.array(pts)
sigma = lambda X: X * np.array([-1, 1, 1]); iota = lambda X: 2 * m - X; ginv = lambda X: X[..., [2, 0, 1]]
OWN = [lambda X: X, sigma, iota, lambda X: iota(sigma(X))]
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, dtype=np.float64))
ocd = lambda c: hull(OV + c)
W = hull(cell) - ocd(np.zeros(3)) - ocd(np.array([0, R, R]))
print(f'W (plain): volume {W.volume():.6f}, genus {W.genus()}')
ridges = [hull(f(ridge(l[0], l[1], +1))) for l in lines for f in OWN]
grooves = [hull(f(ginv(ridge(l[0], l[1], +1)))) for l in lines for f in OWN]   # the bump-face ridge carried by g^-1 onto the dent faces = the neighbour's ridge
KW = W
for r_ in ridges: KW = KW + r_
for g_ in grooves: KW = KW - g_
print(f'keyed W: volume {KW.volume():.6f} (plain {W.volume():.6f}; ridges add {sum(r.volume() for r in ridges):.6f}, grooves remove up to the same)')
# fit check: this W and its neighbour across face 1 (the neighbour = g(W)) must not overlap
g = lambda X: X[..., [1, 2, 0]]
mesh = KW.to_mesh(); V = np.array(mesh.vert_properties)[:, :3]; Fc = np.array(mesh.tri_verts)
NB = m3.Manifold(m3.Mesh(vert_properties=np.asarray(g(V), dtype=np.float32), tri_verts=np.asarray(Fc, dtype=np.uint32)))
ov = (KW ^ NB).volume(); print(f'overlap between a keyed W and its neighbour: {ov:.2e} (should be ~0)')
json.dump(dict(mark='DICTO · dictospheres.com', ridge=dict(height=HR, width=WIDTH, wall_deg=WALL), rhomb_edge=L, lines_face1_uv=[l.tolist() for l in lines],
               W_plain_volume=W.volume(), W_keyed_volume=KW.volume(), overlap_with_neighbour=ov), open(os.path.join(H, 'penrose-W-lines.json'), 'w'), indent=1)
np.save(os.path.join(H, 'keyedW-V.npy'), V); np.save(os.path.join(H, 'keyedW-F.npy'), Fc)
with open(os.path.join(H, 'keyed-W-penrose-lines.off'), 'w') as f:
    f.write(f'OFF\n{len(V)} {len(Fc)} 0\n' + ''.join(f'{x:.6f} {y:.6f} {z:.6f}\n' for x, y, z in V) + ''.join(f'3 {a} {b} {c}\n' for a, b, c in Fc))
print('saved mesh', len(V), 'corners', len(Fc), 'triangles')
