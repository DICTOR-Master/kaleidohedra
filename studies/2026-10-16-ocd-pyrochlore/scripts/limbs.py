# Step 7 (DICTO: "hexagonal prisms of different angles as limbs"). Exploratory, float.
# All copies share one orientation and are centrally symmetric, so the copy at lattice point c has a hexagon exactly parallel,
# opposite and equally turned to our free hexagon H (centre p): it is -H + c = H + v with v = c - 2p. Sweeping H along v gives a
# hexagonal prism, the limb: right only for the existing joints (v = 0), oblique otherwise. Its six side faces are parallelograms
# with sides s (hexagon edge) and |v|: rhombi when |v| = s. For every free hexagon and nearby c: length, tilt, collisions with
# other OCDs; then which limbs can coexist.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
N = json.load(open('data/network.json')); O = np.array(N['ocd']); T = np.array(N['T'])
EO = ConvexHull(O).equations
hexes = []
for e in EO:
    idx = np.abs(O @ e[:3] + e[3]) < 1e-7
    if idx.sum() == 6 and not any(np.allclose(e, h[0]) for h in hexes): hexes.append((e, O[idx]))
free = [h for h in hexes if not any(abs(h[0][:3] @ (t / np.linalg.norm(t)) - 1) < 1e-9 for t in np.vstack([T, -T]))]
s_edge = min(np.linalg.norm(a - b) for a, b in itertools.combinations(free[0][1], 2))
lat = []
for m in itertools.product(range(-3, 4), repeat=4):
    p = sum(k * t for k, t in zip(m, T))
    if 1e-9 < np.linalg.norm(p) < 3.2 and not any(np.allclose(p, c) for c in lat): lat.append(p)
cells = [np.zeros(3)] + lat
def overlap(H1, H2):
    A = np.vstack([H1, H2]); nrm = np.linalg.norm(A[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], nrm], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)]); return r.status == 0 and r.x[3] > 1e-7
shift = lambda E, c: E - np.c_[np.zeros((len(E), 3)), E[:, :3] @ c]
limbs = []
for hi, (e, H) in enumerate(free):
    p = H.mean(0); n = e[:3]
    for c in lat:
        v = c - 2 * p
        if v @ n <= 1e-9 or np.linalg.norm(v) > 1.2: continue            # the limb must leave through the outside of the hexagon
        P = np.vstack([H, H + v]); EP = ConvexHull(P).equations
        hit = [tuple(np.round(q, 3)) for q in cells if not (np.allclose(q, 0) or np.allclose(q, c)) and overlap(EP, shift(EO, q))]
        tilt = np.degrees(np.arccos(np.clip(v @ n / np.linalg.norm(v), -1, 1)))
        limbs.append({'hex': hi, 'c': c, 'v': v, 'len': np.linalg.norm(v), 'tilt': tilt, 'hits': len(hit), 'P': P})
ok = sorted([L for L in limbs if L['hits'] == 0], key=lambda L: L['len'])
out = [f'hexagon edge s = {s_edge:.6f}; {len(limbs)} candidate limbs up to length 1.2, {len(ok)} hit no other OCD']
for L in ok[:12]:
    out.append(f'   from free hexagon {L["hex"]:2d}: length {L["len"]:.6f} (= {L["len"] / s_edge:.4f} s), tilt {L["tilt"]:.3f} deg from the hexagon normal; '
               f'side faces: parallelograms {s_edge:.4f} x {L["len"]:.4f}' + (' = RHOMBI' if abs(L['len'] - s_edge) < 1e-6 else ''))
# the shortest collision-free limb on every free hexagon at once: do the limbs hit each other?
short = {}
for L in ok:
    if L['hex'] not in short: short[L['hex']] = L
sets = [L for L in short.values()]
pairs = 0
for A, B in itertools.combinations(sets, 2):
    for qa in [np.zeros(3)]:
        pass
# limbs of all copies are translates of these; test our limbs against translates of every limb by nearby lattice vectors
clash = 0
for A in sets:
    EA = ConvexHull(A['P']).equations
    for B in sets:
        for q in cells:
            if A is B and np.allclose(q, 0): continue
            # the same limb seen from its other end is the same solid: skip that duplicate
            if A['hex'] != B['hex'] and False: pass
            PB = B['P'] + q
            if np.allclose(np.sort(PB, axis=0), np.sort(A['P'], axis=0), atol=1e-9): continue
            if overlap(EA, ConvexHull(PB).equations): clash += 1
out.append(f'all {len(sets)} shortest collision-free limbs used together on every copy: limb-limb collisions {clash}')
print('\n'.join(out)); open('data/limbs.txt', 'w').write('\n'.join(out) + '\n')
json.dump([{'hex': L['hex'], 'len': L['len'], 'tilt': L['tilt'], 'c': L['c'].tolist(), 'P': L['P'].tolist()} for L in ok], open('data/limbs.json', 'w'))

# Limb classes: a limb from hexagon n to the copy at c is the same solid as the limb from the opposite hexagon -n of the copy at c,
# so the 12 free hexagons give 6 limbs per copy. Which classes collide (with any translate)? Keep a collision-free set of classes.
nrm_of = {L['hex']: free[L['hex']][0][:3] for L in sets}
classes = []
for L in sets:
    if not any(np.allclose(nrm_of[L['hex']], -nrm_of[M['hex']]) for M in classes): classes.append(L)
def clash(A, B):
    EA = ConvexHull(A['P']).equations
    for q in cells:
        PB = B['P'] + q
        if np.allclose(np.sort(PB, axis=0), np.sort(A['P'], axis=0), atol=1e-9): continue
        if overlap(EA, ConvexHull(PB).equations): return True
    return False
C = [[clash(A, B) for B in classes] for A in classes]
best = []
for r in range(len(classes), 0, -1):
    for sub in itertools.combinations(range(len(classes)), r):
        if not any(C[a][b] for a in sub for b in sub): best.append(sub)
    if best: break
vol_limb = ConvexHull(sets[0]['P']).volume
out2 = [f'{len(classes)} limb classes per copy (each limb joins two copies, using 2 of the 12 free hexagons in all); '
        f'classes that collide with each other: {[(a, b) for a in range(len(classes)) for b in range(a + 1, len(classes)) if C[a][b]]}; self-collisions: {[a for a in range(len(classes)) if C[a][a]]}',
        f'largest collision-free set: {len(best[0])} limbs per copy ({len(best)} ways), using {2 * len(best[0])} of the 12 free hexagons; '
        f'limb volume {vol_limb:.6f}; they fill {len(best[0]) * vol_limb:.6f} of the gap 0.335695 per copy ({100 * len(best[0]) * vol_limb / 0.335695:.1f}%)']
print('\n'.join(out2)); open('data/limbs.txt', 'a').write('\n'.join(out2) + '\n')
json.dump({'classes': [{'hex': L['hex'], 'P': L['P'].tolist(), 'c': L['c'].tolist()} for L in classes], 'best': [list(b) for b in best]}, open('data/limb-sets.json', 'w'))
