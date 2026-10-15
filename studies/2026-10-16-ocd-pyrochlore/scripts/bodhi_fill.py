# Step 18 (DICTO: "Bodhi check" -> fill test with Bodhi pieces). The Bodhi pieces (and golden rhombohedra) are golden zonotopes:
# every face is perpendicular to one of the 15 two-fold axes, so they can fill exactly regions walled by golden planes.
# Golden envelope of the OCD: push the 30 golden planes in until they touch it -> a circumscribed rhombic triacontahedron (RT).
# Envelope minus OCD = the non-golden shell (Cleo-Ico adapters / resin); outside the envelopes = Bodhi-fillable, if envelopes of
# neighbouring copies do not overlap. Checked in the bcc packing and in the densest packing. Float.
import json, itertools, numpy as np, sys
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
sys.path.insert(0, '../_lib'); import geomcheck as gc
N = json.load(open('data/network.json')); O = np.array(N['ocd']); T = np.array(N['T']); r = np.linalg.norm(O, axis=1)
ax = gc.icosa_axes(O[np.abs(r - r.max()) < 1e-9]); D2 = np.vstack([ax['2'], -ax['2']])
hs = np.array([np.r_[u, -np.max(O @ u)] for u in D2])                    # u.x <= support of the OCD along u
RT = np.unique(np.round(HalfspaceIntersection(hs, np.zeros(3)).intersections, 10), axis=0); hR = ConvexHull(RT)
vO, vR = ConvexHull(O).volume, hR.volume
ER = hR.equations
def overlap(E1, E2):
    A = np.vstack([E1, E2]); nrm = np.linalg.norm(A[:, :3], axis=1)
    rr = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], nrm], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)]); return rr.status == 0 and rr.x[3] > 1e-8
sh = lambda E, c: E - np.c_[np.zeros((len(E), 3)), E[:, :3] @ c]
out = [f'golden envelope of the OCD: {len(RT)} corners, {len({tuple(np.round(e, 6)) for e in ER})} faces (a rhombic triacontahedron: {len(RT) == 32}); volume {vR:.6f} (OCD {vO:.6f})',
       f'non-golden shell (envelope - OCD) = {vR - vO:.6f} = {100 * (vR - vO) / vR:.1f}% of the envelope']
for name, B in [('bcc packing', np.array([T[0] + T[1], T[0] + T[2], T[0]]).T), ('densest packing', np.array(json.load(open('data/densest.json'))['B']))]:
    det = abs(np.linalg.det(B)); L = [B @ np.array(m, float) for m in itertools.product(range(-2, 3), repeat=3) if any(m)]
    hits = sum(overlap(ER, sh(ER, c)) for c in L)
    golden = det - vR
    out.append(f'{name}: cell {det:.6f}; envelopes of neighbouring copies overlap: {hits // 2} pairs per copy; '
               + (f'Bodhi-fillable (outside the envelopes) {golden:.6f} = {100 * golden / det:.1f}% of space, non-golden shell {100 * (vR - vO) / det:.1f}%, OCD {100 * vO / det:.1f}%' if hits == 0
                  else 'the envelopes collide, so the golden region is not walled off as a whole'))
print('\n'.join(out)); open('data/bodhi-fill.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'envelope': RT.tolist()}, open('data/bodhi-envelope.json', 'w'))

# Fix: cut each envelope flat at its joint planes (the contact hexagon planes). Joined neighbours' cut faces coincide (both
# envelopes are centrally symmetric about the joint), so the cuts face each other, never the gap; what faces the gap stays golden.
for name, B, joints in [('bcc packing', np.array([T[0] + T[1], T[0] + T[2], T[0]]).T, list(T) + list(-T))]:
    cut = np.vstack([hs] + [np.r_[t / np.linalg.norm(t), -np.linalg.norm(t) / 2] for t in joints])
    Ec = np.unique(np.round(HalfspaceIntersection(cut, np.zeros(3)).intersections, 10), axis=0); hc = ConvexHull(Ec); EC = hc.equations
    det = abs(np.linalg.det(B)); L = [B @ np.array(m, float) for m in itertools.product(range(-2, 3), repeat=3) if any(m)]
    hits = sum(overlap(EC, sh(EC, c)) for c in L)
    # are the joint cut faces of two joined envelopes identical (flush)?
    t = joints[0]; n = t / np.linalg.norm(t)
    A = Ec[np.abs(Ec @ n - np.linalg.norm(t) / 2) < 1e-7]; Bf = (Ec + t)[np.abs((Ec + t) @ n - np.linalg.norm(t) / 2) < 1e-7]
    flush = len(A) == len(Bf) and all(np.min(np.linalg.norm(Bf - a, axis=1)) < 1e-7 for a in A)
    out2 = [f'{name}, envelopes cut at the 8 joint planes: volume {hc.volume:.6f}; overlaps with neighbours {hits // 2}; joined cut faces flush: {flush} ({len(A)}-gons)']
    if hits == 0:
        out2.append(f'   space: OCD {100 * vO / det:.1f}%, non-golden shell (cut envelope - OCD) {100 * (hc.volume - vO) / det:.1f}%, '
                    f'Bodhi-fillable (outside the envelopes, walled only by golden planes) {100 * (det - hc.volume) / det:.1f}%')
    print('\n'.join(out2)); open('data/bodhi-fill.txt', 'a').write('\n'.join(out2) + '\n')
    json.dump({'envelope_cut': Ec.tolist()}, open('data/bodhi-envelope-cut.json', 'w'))
