# Keyed W, Penrose rhombs (DICTO 10-24 picked A): on W's 4 bump faces the FAT rhombs of one Penrose (P3) pattern stand raised, on its 4 dent
# faces they are sunk, so every W is the same and one W's bumps fill its neighbour's dents. Pattern: edge = OG edge / phi, centred on the
# socket (OCD centre A0), one pattern across each join (penrose_keys.py, picture A). Clearances and relief as Fable review 4
# (>= 0.035 from the cell edges, >= 0.025 from the socket shadow, height 0.05, walls 30 degrees). Geometry frame from keyed-W-geometry.json.
import json, math, cmath, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); G = json.load(open(os.path.join(H, 'keyed-W-geometry.json')))
R = G['R']; m = np.array(G['m']); cell = np.array(G['cell']); U, Wv, N = (np.array(G['frame'][k]) for k in ('U', 'W', 'N'))
tri = np.array(G['face1_triangle_uv']); Sh = np.array(G['shadow_uv']); OV = np.array(G['ocd_V'])
HREL, WALL = G['relief']['height'], G['relief']['wall_deg_off_normal']; phi = (1 + 5 ** .5) / 2
OGE = max(np.linalg.norm(OV[i] - OV[j]) for i in range(len(OV)) for j in range(i) if np.linalg.norm(OV[i] - OV[j]) < 0.5)   # OG edge (hexagon side)
L = OGE / phi; xyz = lambda p: p[0] * U + p[1] * Wv
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
# fat rhombs = pairs of thick half-triangles sharing their base b-cc
key = lambda z: (round(z.real, 7), round(z.imag, 7)); pairs = {}
for c, a, b, cc in tris:
    if c == 1: pairs.setdefault(tuple(sorted([key(b), key(cc)])), []).append((a, b, cc))
fat = []
for k_, v in pairs.items():
    if len(v) == 2:
        (a1, b1, c1), (a2, _, _) = v; fat.append(np.array([[z.real, z.imag] for z in (a1, b1, a2, c1)]))
def dseg(p, a, b): t = np.clip((p - a) @ (b - a) / ((b - a) @ (b - a)), 0, 1); return np.linalg.norm(p - a - t * (b - a))
def dpoly(p, P): return min(dseg(p, P[i], P[(i + 1) % len(P)]) for i in range(len(P)))
def inside(p, P):
    cr = lambda a, b: a[0] * b[1] - a[1] * b[0]; s = [cr(P[(i + 1) % len(P)] - P[i], p - P[i]) for i in range(len(P))]
    return all(x >= -1e-12 for x in s) or all(x <= 1e-12 for x in s)
def ok(K):
    pts = np.vstack([K[i] + (K[(i + 1) % 4] - K[i]) * np.linspace(0, 1, 30)[:, None] for i in range(4)])
    return all(inside(p, tri) for p in pts) and min(dpoly(p, tri) for p in pts) >= 0.035 and not any(inside(p, Sh) for p in pts) and min(dpoly(p, Sh) for p in pts) >= 0.025
# wallpaper cut at the frame: allowed area = face triangle shrunk by 0.035, minus the socket shadow grown by 0.025; each fat rhomb is trimmed to it
from shapely.geometry import Polygon
allowed = Polygon(tri).buffer(-0.035, join_style=2).difference(Polygon(Sh).buffer(0.025, join_style=2))
MIN_AREA = 0.15 * (L * L * math.sin(math.radians(72)))          # drop slivers under 15% of a fat rhomb
keys = []
for K in fat:
    piece = Polygon(K).intersection(allowed)
    for g in (getattr(piece, 'geoms', None) or [piece]):
        if g.geom_type == 'Polygon' and g.area >= MIN_AREA: keys.append(np.array(g.exterior.coords[:-1]))
print(f'free area on face 1: {allowed.area:.4f} of the face {Polygon(tri).area:.4f} ({100 * allowed.area / Polygon(tri).area:.0f}%); one fat rhomb {L * L * math.sin(math.radians(72)):.4f}')
print(f'OG edge {OGE:.4f}, rhomb edge {L:.4f}; trimmed fat-rhomb keys on face 1: {len(keys)}, sizes', sorted(round(Polygon(K).area / (L * L * math.sin(math.radians(72))), 2) for K in keys))
t_in = HREL * math.tan(math.radians(WALL))
def frustum(K):
    from shapely.geometry import Polygon as Pg
    top = np.array(Pg(K).buffer(-t_in, join_style=2).exterior.coords[:-1])            # walls 30 degrees: the top is the key shrunk by t_in
    return dict(bottom=np.array([xyz(p) for p in K]).tolist(), top=(np.array([xyz(p) for p in top]) + HREL * N).tolist())
B1 = [frustum(K) for K in keys]
sigma = lambda X: X * np.array([-1, 1, 1]); iota = lambda X: 2 * m - X; ginv = lambda X: X[..., [2, 0, 1]]
TR = lambda B, f: dict(bottom=f(np.array(B['bottom'])).tolist(), top=f(np.array(B['top'])).tolist())
bumps = [TR(B, f) for B in B1 for f in (lambda X: X, sigma, iota, lambda X: iota(sigma(X)))]
dents = [TR(B, lambda X, f=f: f(ginv(X))) for B in B1 for f in (lambda X: X, sigma, iota, lambda X: iota(sigma(X)))]
json.dump(dict(mark='DICTO · dictospheres.com', rhomb_edge=L, og_edge=OGE, face1_keys_uv=[K.tolist() for K in keys], bumps=bumps, dents=dents,
               relief=dict(height=HREL, wall_deg=WALL)), open(os.path.join(H, 'penrose-W-keys.json'), 'w'))
print(f'bumps {len(bumps)} (on 4 faces), dents {len(dents)} (on 4 faces)')
