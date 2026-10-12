# Bodhi seed kit, independent check and data (2026-10-12). Loads the pieces found by pieces.py (data/pieces-*.pkl), then:
#  - every piece convex, inside the outer RT(phi^2), clear of all 13 solids (separating axes), no two pieces overlap;
#  - total volume = gap exactly (so with the above, the pieces + 13 solids fill RT(phi^2) exactly);
#  - a sampled cover check (every sample point of the outer form lies in exactly one solid or piece);
#  - the whole kit is invariant under all 120 symmetries; pieces in one type are congruent;
#  - exact corners: in block coordinates x = s e_a + t e_b + u e_c (e = 5-fold unit vectors of an icosahedron face) every corner
#    coordinate is p + q phi with p, q rational; written to data/*.json with unit edge forms and checks.
import sys, os, json, pickle, itertools, numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bodhi_core import *
D = os.path.join(HERE, '../data')
KIT = sys.argv[1] if len(sys.argv) > 1 else 'A'      # A: outer split by copy a's face t + u/phi = phi first (B2, B3); B: by s/phi + t + u = 2 phi first (B4, B5)
res = {}
with open(os.path.join(D, 'pieces-inner.pkl'), 'rb') as fh: res.update(pickle.load(fh))
with open(os.path.join(D, 'pieces-outer.pkl' if KIT == 'A' else 'pieces-outer-H2FIRST.pkl'), 'rb') as fh: res.update(pickle.load(fh))
kit = []   # (label, pocket, list of corner arrays)
labels = ['B1', 'B2', 'B3'] if KIT == 'A' else ['B1', 'B4', 'B5']
order = [('inner', 0), ('outer', 0), ('outer', 1)]
if KIT == 'B':   # put the 3-fold piece first
    o = res['outer']; o.sort(key=lambda t: len(t[1]))
for lab, (pocket, k) in zip(labels, order):
    orb, Ws = res[pocket][k]; kit.append((lab, pocket, [hull_corners(W) for W in Ws]))
print(f'kit {KIT}')
allp = [(lab, W) for lab, _, Ws in kit for W in Ws]
print(f'pieces: ' + ', '.join(f'{lab} x{len(Ws)}' for lab, _, Ws in kit) + f'; total {len(allp)}')
# containment / clearance / pairwise
for lab, W in allp:
    assert all(np.all(W @ e[:3] + e[3] <= 1e-9) for e in F_OUTER), lab
    for S in SOLIDS: assert sat_separated_general(W, S), lab
bad = 0
for (la, A), (lb, B) in itertools.combinations(allp, 2):
    if not sat_separated_general(A, B): bad += 1
print(f'all inside RT(phi^2), clear of the 12 copies and the centre (separating axes); overlapping piece pairs: {bad}')
tv = sum(vol(W) for _, W in allp)
print(f'piece volume {tv:.12f}; gap {GAP_VOL:.12f}; difference {tv - GAP_VOL:.2e}')
# congruence inside each type (sorted distances) and symmetry of the kit
for lab, _, Ws in kit:
    sig = {congruence_sig(W, 7) for W in Ws}; assert len(sig) == 1, lab
can = {canon(W) for _, W in allp}
assert all(canon(W @ g.T) in can for _, W in allp for g in GROUP)
print('each type: all copies congruent (corner count, volume, all distances to 1e-7); kit invariant under all 120 symmetries')
# chirality: is each piece congruent to its mirror image by a rotation? (it has a mirror symmetry if so)
for lab, _, Ws in kit:
    W = Ws[0]; imgs = {canon(W @ g.T) for g in GROUP}
    print(f'  {lab}: {len(Ws)} copies = 120 / {120 // len(Ws)}; the {120 // len(Ws)} symmetries fixing one copy include a mirror: '
          f'{any(np.linalg.det(g) < 0 and canon(W @ g.T) == canon(W) for g in GROUP)}')
# sampled cover
rng = np.random.default_rng(7); Rm = np.abs(OUTER).max()
S = rng.uniform(-Rm, Rm, (400000, 3)); S = S[np.all(S @ np.array(F_OUTER)[:, :3].T + np.array(F_OUTER)[:, 3] < -1e-9, axis=1)]
cnt = np.zeros(len(S), int)
for F in F_SOLIDS + [planes_of(W) for _, W in allp]:
    F = np.array(F); cnt += np.all(S @ F[:, :3].T + F[:, 3] < 0, axis=1)
print(f'sample cover: {len(S)} points in RT(phi^2): in exactly one solid/piece {np.sum(cnt == 1)}, none {np.sum(cnt == 0)}, two+ {np.sum(cnt > 1)}')
print(f'volume shares: 12 copies {12 * RT_VOL:.6f}, centre {vol(CENTRE):.6f}, ' + ', '.join(f'{lab} x{len(Ws)} {len(Ws) * vol(Ws[0]):.6f}' for lab, _, Ws in kit)
      + f'; sum {12 * RT_VOL + vol(CENTRE) + tv:.9f} = RT(phi^2) {vol(OUTER):.9f}')

# exact corners in block coordinates
t0 = TRIANGLES[np.argmax(U20 @ chamber()[1])]; M = np.array(U12[list(t0)]).T; Mi = np.linalg.inv(M)
def golden(x, den=(1, 2, 4, 5, 10, 20)):
    for d in den:
        for q in range(-200, 201):
            p = x * d - q * PHI
            if abs(p - round(p)) < 1e-7: return Fraction(int(round(p)), d), Fraction(q, d)
    return None
def gstr(pq):
    p, q = pq
    if q == 0: return str(p)
    if p == 0: return f'{q}φ' if q not in (1, -1) else ('φ' if q == 1 else '-φ')
    return f'{p}{"+" if q > 0 else "-"}{abs(q) if abs(q) != 1 else ""}φ'
# choose for each type the copy whose centroid is nearest the chamber's middle, express in (s,t,u)
u5, u3, u2, cone = chamber(); mid = (u5 + u3 + u2); mid /= np.linalg.norm(mid)
def exact_len(x):
    g = golden(x * x)
    return f'√({gstr(g)})' if g else f'{x:.9f}'
out = {}
for lab, pocket, Ws in kit:
    W = max(Ws, key=lambda W: (W.mean(0) / np.linalg.norm(W.mean(0))) @ mid)
    stu = W @ Mi.T
    ex = [[golden(x) for x in r] for r in stu]
    assert all(e is not None for r in ex for e in r), lab
    back = np.array([[float(p) + float(q) * PHI for p, q in r] for r in ex]) @ M.T
    assert np.max(np.abs(back - W)) < 1e-9
    F = faces_of(W); ds = dihedrals(W)
    edges = sorted(ds)
    print(f'\n{lab} ({pocket} pocket), {len(Ws)} copies')
    print(describe(W, lab))
    for i, (r, v) in enumerate(zip(ex, W)):
        print(f'   corner {i}: (s,t,u) = ({", ".join(gstr(e) for e in r)}), |x| = {np.linalg.norm(v):.9f}, '
              f'on: ' + ', '.join(n for n, P in [('outer', F_OUTER)] + [(f'copy{j}', F_SOLIDS[j]) for j in range(12)] + [('centre', F_SOLIDS[12])]
                                  if any(abs(v @ e[:3] + e[3]) < 1e-9 for e in P) and all(v @ e[:3] + e[3] < 1e-9 for e in P)))
    print('   edges: ' + '; '.join(f'{i}-{j} {np.linalg.norm(W[i] - W[j]):.6f} = {exact_len(np.linalg.norm(W[i] - W[j]))} at {ds[(i, j)]:.4f}°' for i, j in edges))
    # which solid each face lies on
    for e, f in F:
        on = [n for n, P, sg in [('outer RT(φ²)', F_OUTER, 1)] + [(f'copy {j}', F_SOLIDS[j], -1) for j in range(12)] + [('centre RT(1/φ)', F_SOLIDS[12], -1)]
              if any(np.linalg.norm(e - sg * q) < 1e-7 for q in P) and all(W[f].mean(0) @ q[:3] + q[3] < 1e-9 for q in P)]
        print(f'   face {f}: {len(f)}-gon, area {0.5 * np.linalg.norm(sum(np.cross(W[f[k]], W[f[(k + 1) % len(f)]]) for k in range(len(f)))):.6f}, '
              f'lies on {on[0] if on else "a cut between pieces"}')
    out[lab] = {'credit': 'DICTO (Bodhi seed, discovery #24); gap pieces study 2026-10-12', 'label': lab, 'pocket': pocket, 'count': len(Ws),
                'scale': 'rhombic triacontahedron edge 1 (the 12 copies); outer RT edge φ², centre RT edge 1/φ',
                'volume': vol(W), 'volumeInProlateUnits': vol(W) / P_VOL,
                'vertices': W.tolist(), 'blockCoordinates': [[gstr(e) for e in r] for r in ex],
                'blockBasis': M.T.tolist(),
                'faces': [f for _, f in F], 'dihedralDegrees': {f'{i}-{j}': a for (i, j), a in ds.items()},
                'allCopies': [w.tolist() for w in Ws],
                'checks': ['convex (hull)', 'inside RT(φ²)', 'clear of all 13 solids (separating axes)', 'no overlap with any other piece',
                           'all copies congruent', 'kit invariant under the 120 symmetries', 'total volume = gap to 1e-12', 'block coordinates exact in Q(φ)']}
    with open(os.path.join(D, f'bodhi-{lab}-raw.json'), 'w') as fh: json.dump(out[lab], fh, indent=1)
    unit = dict(out[lab]); e1 = min(np.linalg.norm(W[i] - W[j]) for i, j in edges)
    unit['scale'] = f'shortest edge 1 (raw scale x {1 / e1:.9f})'; unit['vertices'] = (W / e1).tolist(); unit['volume'] = vol(W / e1)
    unit.pop('allCopies'); unit.pop('blockCoordinates'); unit.pop('blockBasis')
    with open(os.path.join(D, f'bodhi-{lab}-unit.json'), 'w') as fh: json.dump(unit, fh, indent=1)
with open(os.path.join(D, f'bodhi-kit-{KIT}-all-pieces.json'), 'w') as fh:
    json.dump({lab: [W.tolist() for W in Ws] for lab, _, Ws in kit}, fh)
with open(os.path.join(D, 'bodhi-seed-solids.json'), 'w') as fh:
    json.dump({'outer': OUTER.tolist(), 'copies': [c.tolist() for c in COPIES], 'centre': CENTRE.tolist()}, fh)
print(f'\nkit {KIT}: wrote data/bodhi-B*-raw.json, data/bodhi-B*-unit.json, data/bodhi-seed-solids.json')
