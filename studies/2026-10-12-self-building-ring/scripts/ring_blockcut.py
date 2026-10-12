# Is a side ring (J2 or FUJI, at a golden size, in a frame turn) an exact union of whole pieces of an existing exact kit complex?
# Complexes: the Chain of Karma steps 1 and 2 (113 and 1,569 pieces: icosahedra, AXE, FUJI, CLEO at several sizes).
# A ring placement is "clean" if every complex piece near it lies wholly inside the ring (inside the band, interior-disjoint from
# the hole) or wholly outside (interior-disjoint from the band, or inside the hole), and the inside pieces' volumes add up to the
# ring's volume. Tests are exact for these solids (separating axes over the full frame axis set).
import sys, os, json, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
from kit_exact import KIT
from scipy.spatial import ConvexHull, cKDTree
rc.KIT.update(KIT); PHI = rc.PHI
src = open(os.path.join(rc.HERE, 'local_cover.py')).read()
exec(src[src.index('# the 120 frame symmetries'):src.index('pieces = {k')])
CHAIN = os.path.expanduser('~/kaleidohedra/studies/2026-10-11-chain-of-karma/chain-of-karma-steps-1-2.json')
if not os.path.exists(CHAIN): CHAIN = os.path.join(rc.HERE, '../data/chain-of-karma-steps-1-2.json')
STEP = sys.argv[1] if len(sys.argv) > 1 else '2'
B = json.load(open(CHAIN))[STEP]
# the complex in the frame of ring_core: the step's vertices are centred on the Lotus centre like the kit file? align by the big icosahedron
def _snapc(x):
    for den in (2, 4):
        for q in range(-40, 41):
            p = x * den - q * PHI
            if abs(p - round(p)) < 3e-5 * den: return (round(p) + q * PHI) / den
    raise ValueError(x)
PVs = [np.vectorize(_snapc)(np.array(p['v'], float)) for p in B]
allv = np.vstack(PVs); cen = allv.mean(0); PVs = [V - cen for V in PVs]
# turn the complex into the kit's frame: its 12 outermost corners (the big icosahedron) onto the kit icosahedron's directions
_A = np.vstack(PVs); _d = np.linalg.norm(_A, axis=1); _O = np.unique(np.round(_A[_d > _d.max() - 1e-6], 9), axis=0)
_O = _O / np.linalg.norm(_O, axis=1)[:, None]; _K = KIT['I'] - KIT['I'].mean(0); _K = _K / np.linalg.norm(_K, axis=1)[:, None]
assert len(_O) == 12
_e = min(np.linalg.norm(_O[0] - w) for w in _O[1:]); _nb = [m for m in range(12) if abs(np.linalg.norm(_O[m] - _O[0]) - _e) < 1e-6]
_b = _nb[0]; _c = [m for m in _nb if abs(np.linalg.norm(_O[m] - _O[_b]) - _e) < 1e-6][0]
_Ai = np.linalg.inv(np.array([_O[0], _O[_b], _O[_c]]).T); _ROT = None
for i, j, k in itertools.permutations(range(12), 3):
    R_ = np.array([_K[i], _K[j], _K[k]]).T @ _Ai
    if np.allclose(R_ @ R_.T, np.eye(3), atol=1e-4) and all(np.min(np.linalg.norm(_K - y, axis=1)) < 1e-4 for y in _O @ R_.T):
        _ROT = R_; break
assert _ROT is not None
_ROT = np.vectorize(lambda x: _snapc(x) if abs(x) > 1e-9 else 0.0)(_ROT); assert np.allclose(_ROT @ _ROT.T, np.eye(3), atol=1e-12)
PVs = [V @ _ROT.T for V in PVs]; allv     # snapped to the golden module (data had 5 decimals); exact to 1e-12 now = np.vstack(PVs); cen = np.zeros(3)
n = len(B); VOL = np.array([ConvexHull(V).volume for V in PVs]); PC = np.array([V.mean(0) for V in PVs])
PR = np.array([np.linalg.norm(V - V.mean(0), axis=1).max() for V in PVs])
print(f'step {STEP}: {n} pieces, total volume {VOL.sum():.6f}', flush=True)
# check that the complex's pieces are in the kit's frame: their edges must run along two-fold axes of KIT's icosahedron
Ic = KIT['I'] - KIT['I'].mean(0)
U2 = np.array([Ic[i] - Ic[j] for i, j in itertools.permutations(range(12), 2) if abs(np.linalg.norm(Ic[i] - Ic[j]) - 1) < 1e-9])
def two_fold(d): return np.any(np.abs(np.abs(U2 @ (d / np.linalg.norm(d))) - 1) < 1e-9)
okframe = all(two_fold(V[i] - V[j]) for V in PVs[:200] for i, j, l, d in rc.convex_edges(V))
print(f'complex edges on the kit frame two-fold axes: {okframe}', flush=True)
# frame axes for exact separation
AX = []
for V in [KIT[k] for k in ('I', 'AXE', 'FUJI', 'CLEO', 'J2')]:
    for g in G: AX += list(rc.planes(V @ g.T)[:, :3])
dirs = U2 / np.linalg.norm(U2, axis=1)[:, None]
for a, b in itertools.combinations(dirs, 2):
    c = np.cross(a, b)
    if np.linalg.norm(c) > 1e-9: AX.append(c / np.linalg.norm(c))
AX = np.array(AX); AX *= np.sign(AX @ np.array([.31, .57, .73]))[:, None]; AX = np.unique(np.round(AX, 8), axis=0)
maxv = max(len(V) for V in PVs); PV = np.stack([np.vstack([V, np.repeat(V[:1], maxv - len(V), 0)]) for V in PVs])
PLO, PHI_ = (PV @ AX.T).min(1), (PV @ AX.T).max(1)
tree = cKDTree(PC)
_, _ui = np.unique(np.round(allv - cen, 6), axis=0, return_index=True); pts = (allv - cen)[_ui]     # exact values, deduplicated
found = []
TARGETS = os.environ.get('TARGETS', 'ring-J2,ring-FUJI').split(',')
for RING in TARGETS:
    kindT, P_ = RING.split('-')
    if P_ == 'I':                                                      # positive control: whole icosahedra
        r = {'floor': KIT['I'][:1]}; band0 = KIT['I'] - KIT['I'].mean(0); hole0 = None; kindT = 'control'
    else:
        r = rc.ring(P_); band0, hole0 = r['band'] - r['c1'], r['hole'] - r['c1']
    if kindT == 'band': hole0 = None                                   # the frustum below the tip, no hole
    if kindT == 'control': pass
    elif kindT == 'whole':                                             # phi*P itself
        band0 = np.vstack([r['floor'], r['apex'][None]]) - r['c1']; hole0 = None
    rvol = rc.vol(band0) - (rc.vol(hole0) if hole0 is not None else 0)
    if hole0 is None: hole0 = np.zeros((4, 3)) + 1e6 * np.array([[1, 0, 0], [1.1, 0, 0], [1, .1, 0], [1, 0, .1]])   # far away dummy
    for m in range(-1, 5):
        s = PHI ** m; tv = rvol * s ** 3
        if tv > VOL.sum(): continue
        shapes, seen = [], set()
        for g in G:
            bd, hl = s * band0 @ g.T, (s * hole0 @ g.T if hole0[0, 0] < 1e5 else hole0); key = tuple(sorted(map(tuple, np.round(bd, 5))))
            if key in seen: continue
            seen.add(key); shapes.append((bd, hl))
        hits = 0; tried = 0
        for bd, hl in shapes:
            Fb = rc.planes(bd); rad = np.linalg.norm(bd, axis=1).max()
            for j in [0]:                                       # a floor corner of the band is a convex corner of the ring: some piece has a corner there
                T = pts - bd[j]                                         # put band corner j on every complex vertex
                for t in T:
                    tried += 1
                    near = tree.query_ball_point(t, rad + PR.max())
                    if len(near) < 2: continue
                    near = np.array(near); W = PV[near]
                    BL, BH = ((bd + t) @ AX.T).min(0), ((bd + t) @ AX.T).max(0)
                    HL, HH = ((hl + t) @ AX.T).min(0), ((hl + t) @ AX.T).max(0)
                    lo, hi = PLO[near], PHI_[near]
                    out_band = np.any((hi <= BL + 1e-5) | (lo >= BH - 1e-5), axis=1)
                    sF = np.einsum('nvk,fk->nvf', W, Fb[:, :3]) + (Fb[:, 3] - Fb[:, :3] @ t)
                    in_band = np.all(sF <= 1e-5, axis=(1, 2))
                    Fh = rc.planes(hl + t); sH = np.einsum('nvk,fk->nvf', W, Fh[:, :3]) + Fh[:, 3]
                    in_hole = np.all(sH <= 1e-5, axis=(1, 2))
                    off_hole = np.any((hi <= HL + 1e-5) | (lo >= HH - 1e-5), axis=1)
                    inside = in_band & off_hole; outside = out_band | in_hole
                    if not np.all(inside | outside) or inside.sum() < 2: continue
                    v = VOL[near[inside]].sum()
                    if abs(v - tv) < 1e-5 * max(1, tv):
                        hits += 1
                        found.append({'ring': RING, 'scale_k': m, 'pieces': [{'r': B[i]['r'], 'v': (PVs[i]).tolist()} for i in near[inside]],
                                      'band': (bd + t).tolist(), 'hole': (hl + t).tolist()})
        print(f'{RING} ring at phi^{m} (volume {tv:.6f}): {len(shapes)} turns, {tried} placements tried, clean cuts {hits}', flush=True)
json.dump(found, open(os.path.join(rc.HERE, f'../data/ring-blockcut-step{STEP}.json'), 'w'))
print(f'clean cuts found: {len(found)}')
