# DICTO #43 Conjecture 1, 2026-11-09 (DICTO: "yes" to the pilot). Can an INTERVAL run replace the exact one beyond D_13?
# Intervals prove strict inequalities, never equalities. So classify every exact coincidence of the family D_0..D_KMAX:
#  - face with >3 polygon corners: FORCED if its members form ONE orbit of the face's stabiliser (rotations fixing its normal),
#    since then they are all at one height on the axis automatically; otherwise UNFORCED (a true coincidence intervals cannot prove);
#  - listed point lying exactly on a face but not a polygon corner: BOUNDARY coincidence (unforced unless noted);
#  - listed point strictly inside: fine for intervals.
# Also the smallest float gap between a face plane and a non-member point (what interval precision would have to resolve).
# usage: python -u coincidence_pilot.py <five-fold-octet dir> <kmax>
import sys, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exact_family.py')).read()
head = src.split("t0 = time.time()")[0]
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], '/dev/null']
exec(head)
W = [tuple(cv(x) for x in v) for v in OG]
NEG = [tuple(tuple(-x for x in row) for row in M) for M in GX]          # central inversion x rotations = the mirrors of I_h
FULL = GX + NEG
def is_reflection(M):                                                     # -R with R a half-turn is a reflection
    tr = M[0][0] + M[1][1] + M[2][2]; return tr == R5(1)
from scipy.spatial import ConvexHull as CH
tot_unforced = 0
for k in range(KMAX + 1):
    t = time.time()
    idx = {v: i for i, v in enumerate(W)}; Wf = np.array([fl(v) for v in W])
    F, ne, _ = exact_faces(W, idx, Wf)
    onface = set(); corners = set(); nontri = forced = unforced = 0; worst = []
    gap = np.inf
    for mem, (n, d, isrep) in F.items():
        mm = sorted(mem); P = Wf[mm]; c0 = P.mean(0); B = np.linalg.svd(P - c0)[2][:2]; Q = (P - c0) @ B.T
        vert = [mm[i] for i in CH(Q).vertices] if len(mm) > 3 else mm
        corners.update(vert); onface.update(mm)
        if isrep:
            nf = fl(n); dd = d.f(); g = np.abs(Wf @ nf - dd) / np.linalg.norm(nf); g[mm] = np.inf; gap = min(gap, g.min())
        if len(mm) > 3 or len(vert) > 3:
            nontri += 1
            stab = [M for M in FULL if app(M, n) == n and app(M, W[mm[0]]) in idx]
            orb = set(idx[app(M, W[mm[0]])] for M in stab)
            refl = [M for M in stab if is_reflection(M)]
            def classes(M): return len(set(frozenset((j, idx[app(M, W[j])])) for j in mm))
            if orb == set(mm) or any(classes(M) <= 2 for M in refl): forced += 1
            else:
                unforced += 1
                if isrep and len(worst) < 3: worst.append((len(mm), len(vert), len(stab)))
    bnd = len(onface) - len(corners); inside = len(W) - len(onface)
    tot_unforced += unforced + bnd
    print(f'D_{k} [rotations+mirrors]: points {len(W)} corners {len(corners)} faces {len(F)} (non-triangle {nontri}: forced {forced}, UNFORCED {unforced}) '
          f'boundary non-corner points {bnd} strictly inside {inside} | min float gap plane-to-nonmember {gap:.2e} | eg unforced (members, corners, |stab|) {worst} ({time.time()-t:.0f} s)', flush=True)
    if k == KMAX: break
    feet = {}
    for n, d, _ in F.values():
        s = d / dot(n, n); feet[tuple(s * x for x in n)] = 1
    W = list(feet)
print('VERDICT: interval route needs no exact help up to D_%d' % KMAX if tot_unforced == 0 else f'VERDICT: {tot_unforced} unforced coincidences up to D_{KMAX}: plain interval route not rigorous')
print('FINAL ok' if k == KMAX else 'FINAL FAIL: did not reach KMAX')
