# Builds src/krp-core/src/polyhedra/tetoktjiru.js (DICTO 2026-10-21): DICTO Tetoktjiru, bodies and legs, DICTO's coral jacks that fill
# space on the octet truss (corners: integer points of even sum; octahedra centred on the odd ones; tetrahedral holes centred on the
# half-integer points):
#   - DICTO Oktjiru at every octahedron centre: six slim tapering legs to the octahedron's corners (the legs);
#   - DICTO Tetjiru at every tetrahedral hole: four thick legs out through the tetrahedron's faces into the Oktjiru's hollows (the bodies).
# The legs are drawn first as a skeleton and every point of space goes to the piece whose legs it is nearest (DICTO: "form the lattice
# in the structure you want the legs to be"), so the pieces fill space. Two tones (DICTO: the Tetjiru are the bodies, the Oktjiru the
# legs): the up bodies and the side of every leg facing them in deep coral, the down bodies and the side facing them in pale coral.
# One Oktjiru shape (all translates); the Tetjiru in its two turns. Meshed coarser than the study's figures, for the app.
# Study: kaleidohedra research branch, studies/2026-10-20-double-octet/jacks_octet.py + jacks_twotone_figs.py (args 0.14 0.05 0.24 0.08,
# TET_LEN 0.72). Needs manifold3d, scikit-image, scipy, pyfqmr (run on dicto-node).
# Usage: python3 scripts/build-tetoktjiru.py [repo root]
import itertools, json, os, sys
import numpy as np, manifold3d as m3
from skimage.measure import marching_cubes
from scipy.ndimage import gaussian_filter
import pyfqmr
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
RHO_OKT, TIP_OKT, RHO_TET, TIP_TET, TET_LEN, K, STEP = 0.14, 0.05, 0.24, 0.08, 0.72, 0.04, 0.04
DEEP, PALE = 0xb8452f, 0xeea58c
TRIS = {6: 3000, 4: 1400}                           # triangles kept: Oktjiru, Tetjiru
AX = np.vstack([np.eye(3), -np.eye(3)])
def tet_legs(t):                                    # unit directions from a tetrahedral hole to its 4 corners
    t = np.array(t, float); C = np.array([t + .5 * np.array(s) for s in itertools.product((1, -1), repeat=3)])
    C = C[[int(round(p.sum())) % 2 == 0 for p in C]]; L = C - t; return L / np.linalg.norm(L, axis=1)[:, None]
def sites_near(c, rad):
    c = np.array(c, float); out = []; lo = np.floor(c - rad).astype(int); hi = np.ceil(c + rad).astype(int)
    for p in itertools.product(*[range(a, b + 1) for a, b in zip(lo, hi)]):
        p = np.array(p, float)
        if int(p.sum()) % 2 and np.linalg.norm(p - c) <= rad: out.append((p, AX, RHO_OKT, TIP_OKT, 1.0))
        q = p + .5
        if np.linalg.norm(q - c) <= rad: out.append((q, -tet_legs(q), RHO_TET, TIP_TET, TET_LEN))
    return out
def field(X, c, L, R0, R1, LEN):                    # distance to c's tapering legs, legs blended (soft minimum, width K)
    D = X - c; ds = []
    for l in L:
        t = np.clip(D @ l / LEN, 0, 1); ds.append(np.linalg.norm(D - np.outer(t * LEN, l), axis=1) - (R0 * (1 - t) + R1 * t))
    ds = np.array(ds); m = ds.min(0); return m - K * np.log(np.exp(-(ds - m) / K).sum(0))
def piece(site, half=1.35):
    c = site[0]; n = int(round(2 * half / STEP)) + 1; ax = np.linspace(-half, half, n)
    G = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3) + c
    m = np.full(len(G), np.inf)
    for s in sites_near(c, 2 * half + .2):
        if np.linalg.norm(s[0] - c) > 1e-9: m = np.minimum(m, field(G, *s))
    g = gaussian_filter((field(G, *site) - m).reshape(n, n, n), 0.6)
    g[0], g[-1], g[:, 0], g[:, -1], g[:, :, 0], g[:, :, -1] = 1, 1, 1, 1, 1, 1
    V, F, _, _ = marching_cubes(g, 0.0, spacing=(STEP,) * 3); V = V - half
    sim = pyfqmr.Simplify(); sim.setMesh(V, F); sim.simplify_mesh(target_count=TRIS[len(site[1])], aggressiveness=5, preserve_border=True, verbose=False)
    V, F, _ = sim.getMesh()                          # simplified for the app (the study keeps the full mesh)
    mf = m3.Manifold(m3.Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(F, np.uint32)))
    if mf.volume() < 0 or mf.status() != m3.Error.NoError:
        mf = m3.Manifold(m3.Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(F[:, ::-1], np.uint32)))
    return mf
def creases(V, T, deg=40):                           # outline only where the surface folds sharply, not every mesh edge
    N = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); N /= np.linalg.norm(N, axis=1)[:, None] + 1e-12; by = {}
    for f, tri in enumerate(T):
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])): by.setdefault((min(a, b), max(a, b)), []).append(f)
    return [[int(a), int(b)] for (a, b), fs in by.items() if len(fs) == 2 and N[fs[0]] @ N[fs[1]] < np.cos(np.radians(deg))]
turn = lambda t: 'UP' if int(round(np.array(t).sum() - 1.5)) % 2 == 0 else 'DOWN'
RAW, VOL = {}, {}
def add(pid, name, site):
    mf = piece(site); me = mf.to_mesh(); V = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts)
    if pid == 'TETOKTJIRU_OKTJIRU':                   # each leg split lengthwise: the tone of the body in that octant
        X = V[T].mean(1); s = np.where(X >= 0, 1.0, -1.0); fc = [DEEP if turn(site[0] + .5 * v) == 'UP' else PALE for v in s]
    else: fc = [DEEP if pid.endswith('UP') else PALE] * len(T)
    RAW[pid] = {'name': name, 'vertices': np.round(V, 4).tolist(), 'faces': T.tolist(), 'faceColours': fc, 'edges': creases(V, T)}; VOL[pid] = round(mf.volume(), 5)
okt = np.array([1., 0, 0]); tu, td = np.full(3, .5), np.array([1.5, .5, .5])
add('TETOKTJIRU_OKTJIRU', 'DICTO Oktjiru (Tetoktjiru, the legs)', (okt, AX, RHO_OKT, TIP_OKT, 1.0))
add('TETOKTJIRU_TETJIRU_UP', 'DICTO Tetjiru (Tetoktjiru, a body, up)', (tu, -tet_legs(tu), RHO_TET, TIP_TET, TET_LEN))
add('TETOKTJIRU_TETJIRU_DOWN', 'DICTO Tetjiru (Tetoktjiru, a body, down)', (td, -tet_legs(td), RHO_TET, TIP_TET, TET_LEN))
entry = lambda pid, p: {'shape': pid, 'position': [round(float(x), 9) for x in p], 'quaternion': [0, 0, 0, 1]}
tet_entry = lambda t: entry('TETOKTJIRU_TETJIRU_' + turn(t), t)
kit1 = [entry('TETOKTJIRU_OKTJIRU', okt)] + [tet_entry(okt + .5 * np.array(s)) for s in itertools.product((1, -1), repeat=3)]
kit2 = [tet_entry(np.array(b, float) + .5) for b in itertools.product((0, 1), repeat=3)]
kit2 += [entry('TETOKTJIRU_OKTJIRU', c) for c in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (2, 1, 0), (2, 0, 1), (1, 2, 0), (0, 2, 1), (1, 0, 2), (0, 1, 2), (2, 1, 2), (1, 2, 2), (2, 2, 1)]]
KITS = {'tetoktjiru': {'label': 'DICTO Tetoktjiru · one Oktjiru (legs) among 8 Tetjiru (bodies)', 'group': 'sets', 'entries': kit1},
        'tetoktjiru.block': {'label': 'DICTO Tetoktjiru · a block (8 Tetjiru + 13 Oktjiru): two coral creatures woven together', 'group': 'sets', 'entries': kit2}}
out = f"""// Generated by scripts/build-tetoktjiru.py (DICTO 2026-10-21). Do not edit.
// DICTO Tetoktjiru, bodies and legs: DICTO's coral jacks (Tibetan byi ru, coral). Oktjiru (six slim legs, the legs) and Tetjiru (four thick
// legs, the bodies) fill space together on the octet truss; up bodies and the legs facing them deep coral, down bodies and theirs pale.
import {{ specOf }} from './stellaJewel.js';
const RAW = {json.dumps(RAW, separators=(',', ':'))};
export const TETOKTJIRU_ADDITIONS = Object.fromEntries(Object.entries(RAW).map(([id, p]) => [id, {{ ...specOf(id, p.name, p.vertices, p.faces, true, 1), faceColours: p.faceColours, edges: p.edges }}]));
export const TETOKTJIRU_ADDITION_IDS = Object.keys(TETOKTJIRU_ADDITIONS);
export const TETOKTJIRU_KITS = {json.dumps(KITS, separators=(',', ':'))};
export const TETOKTJIRU_VOLUMES = {json.dumps(VOL)};
"""
open(os.path.join(ROOT, 'src/krp-core/src/polyhedra/tetoktjiru.js'), 'w').write(out)
print({k: len(v['faces']) for k, v in RAW.items()}, VOL, 'Oktjiru + 2 Tetjiru =', round(sum(VOL.values()), 4), '(2)', 'bytes', len(out))
