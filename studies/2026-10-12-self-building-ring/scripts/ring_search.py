# Symmetric exact-cover search for the side ring (2026-10-12), built to finish where the 2026-10-11 brute force stalled:
#  - the forced corner pieces (local_cover.py: a J2 corner at every floor corner of the J2 ring, a FUJI corner at every floor corner
#    of the FUJI ring) are fixed at their largest size (apex at the band's top corner) when FIX=1;
#  - kit pieces in the 120 frame turns at sizes phi^k (SIZES), placed with a corner on a candidate point (ROUNDS of closure);
#  - every test is vectorised: all solids here have faces and edges along frame directions, so one precomputed axis set (all face
#    normals and edge-pair cross products of every kit piece and the ring, in all 120 turns) makes separating-axis tests exact;
#  - placements are grouped into orbits of the ring's own turns (5-fold or 3-fold) and the MILP covers sample points of one sector.
# Any MILP solution is then checked exactly (pairwise separating axes on the full piece list, volume to 1e-9).
import sys, os, itertools, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
from kit_exact import KIT
from scipy.spatial import ConvexHull, cKDTree
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
rc.KIT.update(KIT); PHI = rc.PHI
src = open(os.path.join(rc.HERE, 'local_cover.py')).read()
exec(src[src.index('# the 120 frame symmetries'):src.index('pieces = {k')])
RING = sys.argv[1] if len(sys.argv) > 1 else 'J2'
SIZES = [int(s) for s in os.environ.get('SIZES', '-1,-2,-3').split(',')]
TYPES = os.environ.get('TYPES', 'AXE,CLEO,FUJI,J2,t1,t2,t3,t4,t5,t6,T2,I,J11').split(',')
ROUNDS = int(os.environ.get('ROUNDS', '2')); NS = int(os.environ.get('NS', '20000')); FIX = os.environ.get('FIX', '1') == '1'
TLIM = float(os.environ.get('TLIM', '3000')); TAG = os.environ.get('TAG', '')
t00 = time.time()
r = rc.ring(RING); band, hole = r['band'], r['hole']; Fb, Fh = rc.planes(band), rc.planes(hole)
RV = rc.vol(band) - rc.vol(hole)
NF = 5 if RING == 'J2' else 3
axis = r['apex'] - r['c1']; axis /= np.linalg.norm(axis); c1 = r['c1']
def rot(k):
    a = 2 * np.pi * k / NF; K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
RT = [rot(k) for k in range(NF)]
for Rk in RT: assert all(np.min(np.linalg.norm(band - (c1 + (y - c1) @ Rk.T), axis=1)) < 1e-9 for y in band)
assert any(np.allclose(Rk, g) for g in G for Rk in RT[1:2]), 'ring turn not in the frame group'
# axis set
def dirs(V):
    H = rc.planes(V); out = list(H[:, :3])
    E = [V[i] - V[j] for i, j, l, d in rc.convex_edges(V)]
    return out, E
FN, ED = [], []
for nm in TYPES + ['__band', '__hole']:
    V = band if nm == '__band' else hole if nm == '__hole' else KIT[nm]
    n, e = dirs(V)
    for g in G: FN += list(np.array(n) @ g.T); ED += list(np.array(e) @ g.T)
def uniq_dirs(X):
    X = np.array(X); X /= np.linalg.norm(X, axis=1)[:, None]; X *= np.sign(X @ np.array([0.123, 0.456, 0.789]))[:, None]
    return np.unique(np.round(X, 8), axis=0)
EDu = uniq_dirs(ED); cr = [np.cross(a, b) for a, b in itertools.combinations(EDu, 2)]
cr = [c for c in cr if np.linalg.norm(c) > 1e-9]
AX = uniq_dirs(list(FN) + cr)
print(f'{RING} ring: volume {RV:.9f}; {len(AX)} separating axes; types {TYPES}; sizes {SIZES}; rounds {ROUNDS}', flush=True)
def rng_of(W): p = W @ AX.T; return p.min(-2), p.max(-2)
BLO, BHI = rng_of(band); HLO, HHI = rng_of(hole)
fixed = []
if FIX:
    big = np.vstack([r['floor'], r['apex'][None]])
    for B in r['floor']: fixed.append(B + (big - B) / PHI ** 2)
FR = [rng_of(W) for W in fixed]
FE = [rc.planes(W) for W in fixed]
vleft = RV - sum(rc.vol(W) for W in fixed)
# shapes
shapes = []
for nm in TYPES:
    V0 = KIT[nm] - KIT[nm].mean(0); v0 = rc.vol(V0)
    for k in SIZES:
        seen = set()
        for g in G:
            V = PHI ** k * V0 @ g.T; key = tuple(sorted(map(tuple, np.round(V, 6))))
            if key in seen: continue
            seen.add(key); shapes.append((nm, k, V, PHI ** (3 * k) * v0))
print(f'{len(shapes)} shapes (type x size x turn)', flush=True)
P = np.unique(np.round(np.vstack([band, hole] + fixed), 9), axis=0)
place = {}
for rnd in range(ROUNDS):
    new = []
    for si, (nm, k, V, v) in enumerate(shapes):
        if v > vleft + 1e-9: continue
        T = (P[:, None, :] - V[None, :, :]).reshape(-1, 3)
        T = np.unique(np.round(T, 9), axis=0)
        # cheap prefilter: inside the band (corner test), then the axis tests in chunks
        W = T[:, None, :] + V[None, :, :]
        ok = np.all(np.einsum('tvi,fi->tvf', W, Fb[:, :3]) + Fb[:, 3] <= 1e-9, axis=(1, 2))
        if not ok.any(): continue
        T, W = T[ok], W[ok]
        oks = []
        for c0 in range(0, len(W), 1500):
            lo, hi = rng_of(W[c0:c0 + 1500])
            o = np.any((hi <= HLO + 1e-9) | (lo >= HHI - 1e-9), axis=1)
            for (flo, fhi) in FR: o &= np.any((hi <= flo + 1e-9) | (lo >= fhi - 1e-9), axis=1)
            oks.append(o)
        ok = np.concatenate(oks)
        for t, w in zip(T[ok], W[ok]):
            key = (si, tuple(np.round(t, 7)))
            if key not in place: place[key] = w; new.append(w)
    if new: P = np.unique(np.round(np.vstack([P] + new), 9), axis=0)
    print(f'round {rnd}: {len(place)} placements, {len(P)} points ({time.time() - t00:.0f}s)', flush=True)
keys = list(place)
# orbits under the ring's turns
canon = lambda W: tuple(sorted(map(tuple, np.round(W, 6))))
bykey = {canon(place[k]): i for i, k in enumerate(keys)}
orbits, seen = [], set()
for i, k in enumerate(keys):
    if i in seen: continue
    mem = []
    for Rk in RT:
        j = bykey.get(canon(c1 + (place[k] - c1) @ Rk.T))
        if j is None: mem = None; break
        mem.append(j)
    if mem is None: continue
    mem = sorted(set(mem)); seen.update(mem)
    if len(mem) < NF: continue                      # a piece fixed by a turn would contain the axis, which lies in the hole
    lo_, hi_ = rng_of(np.array([place[keys[j]] for j in mem]))
    if all(np.any((hi_[a] <= lo_[b] + 1e-9) | (hi_[b] <= lo_[a] + 1e-9)) for a, b in itertools.combinations(range(len(mem)), 2)):
        orbits.append(mem)
print(f'{len(orbits)} orbits of {NF}', flush=True)
# samples in one sector: angle about the axis in [0, 2pi/NF)
ref = np.cross(axis, [1, 0, 0] if abs(axis[0]) < .9 else [0, 1, 0]); ref /= np.linalg.norm(ref); ref2 = np.cross(axis, ref)
rng = np.random.default_rng(11); lo, hi = band.min(0), band.max(0)
S = rng.uniform(lo, hi, (NS * 40, 3))
S = S[np.all(S @ Fb[:, :3].T + Fb[:, 3] < -1e-9, axis=1) & ~np.all(S @ Fh[:, :3].T + Fh[:, 3] <= 1e-9, axis=1)]
for E in FE: S = S[~np.all(S @ E[:, :3].T + E[:, 3] <= 1e-9, axis=1)]
ang = np.mod(np.arctan2((S - c1) @ ref2, (S - c1) @ ref), 2 * np.pi); S = S[ang < 2 * np.pi / NF][:NS]
print(f'{len(S)} sample points in one sector; volume to fill {vleft:.9f}', flush=True)
rows, cols = [], []; vols = np.zeros(len(orbits))
for c, mem in enumerate(orbits):
    for i in mem:
        W = place[keys[i]]; E = rc.planes(W); vols[c] += shapes[keys[i][0]][3]
        hit = np.where(np.all(S @ E[:, :3].T + E[:, 3] < -1e-9, axis=1))[0]
        rows += list(hit); cols += [c] * len(hit)
M = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(S), len(orbits))).tocsr()
cov = np.asarray(M.sum(1)).ravel()
print(f'sample points no orbit covers: {int((cov == 0).sum())} (max multiplicity {M.max() if M.nnz else 0})', flush=True)
if (cov == 0).any():
    U = S[cov == 0]; z = (U - c1) @ axis; rr = np.linalg.norm((U - c1) - np.outer(z, axis), axis=1)
    print(f'  uncovered: height {z.min():.3f}..{z.max():.3f}, radius {rr.min():.3f}..{rr.max():.3f}', flush=True)
t0 = time.time()
res = milp(np.ones(len(orbits)), constraints=[LinearConstraint(M, 1, 1), LinearConstraint(vols[None, :], vleft - 1e-7, vleft + 1e-7)],
           integrality=np.ones(len(orbits)), bounds=Bounds(0, 1), options={'time_limit': TLIM})
print('MILP:', res.status, res.message, f'{time.time() - t0:.0f}s', flush=True)
if res.x is None: sys.exit()
chosen = [keys[i] for c in np.where(res.x > .5)[0] for i in orbits[c]]
allW = fixed + [place[k] for k in chosen]; names = [f'{RING if False else ("J2" if RING == "J2" else "FUJI")}@phi^-1 (corner)'] * len(fixed) + [f'{shapes[k[0]][0]}@phi^{shapes[k[0]][1]}' for k in chosen]
lo_, hi_ = zip(*[rng_of(W) for W in allW]); lo_, hi_ = np.array(lo_), np.array(hi_)
bad = 0
for i, j in itertools.combinations(range(len(allW)), 2):
    if not np.any((hi_[i] <= lo_[j] + 1e-9) | (hi_[j] <= lo_[i] + 1e-9)): bad += 1
badh = sum(not np.any((h <= HLO + 1e-9) | (l >= HHI - 1e-9)) for l, h in zip(lo_, hi_))
tot = sum(rc.vol(W) for W in allW)
from collections import Counter
print('pieces:', dict(Counter(names)))
print(f'ring volume {RV:.12f}; pieces {tot:.12f}; overlapping pairs {bad}; overlapping the hole {badh}', flush=True)
json.dump([{'name': n, 'vertices': W.tolist()} for n, W in zip(names, allW)], open(os.path.join(rc.HERE, f'../data/ring-{RING}{TAG}-solution.json'), 'w'))
