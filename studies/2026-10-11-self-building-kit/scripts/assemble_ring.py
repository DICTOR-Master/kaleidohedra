# Outer layer of the side ring (2026-10-11): take the collision-free covers of one sloping face (face_cover.py), turn them round
# the ring's axis onto every sloping face (5-fold for the pentagonal pyramid, 3-fold for FUJI; these turns are in the kit's
# icosahedral frame), and keep the combinations in which no two pieces overlap. Writes the outer layers found, and the volume
# left to fill inside the ring.
import sys, os, glob, itertools, numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'selfbuild_sides.py')).read()
exec(src[:src.index('place = {}')])
N = 5 if TARGET == 'jsides' else 3
axis = apex - base.mean(0); axis /= np.linalg.norm(axis); c1 = base.mean(0)
def rot(k):
    a = 2 * np.pi * k / N; K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
R = [rot(k) for k in range(N)]
turn = lambda W, k: c1 + (W - c1) @ R[k].T
# sanity: the turns map the band and the small pyramid onto themselves
for k in range(N):
    for X in (TV, HV):
        Y = turn(X, k); assert all(np.min(np.linalg.norm(X - y, axis=1)) < 1e-6 for y in Y), 'turn is not a symmetry'
print(f'{TARGET}: {N}-fold turns check out')
covers = {}
for f in sorted(glob.glob(f'face-cover-{TARGET}-facetype*-*.npy')):
    t = f.split('facetype')[1].split('-')[0]
    covers.setdefault(t, []).append([np.array(w, float) for w in np.load(f, allow_pickle=True)])
print({t: len(v) for t, v in covers.items()}, 'covers per face type')
def ok_together(A, B):
    return not any(overlap(a, b) for a in A for b in B)
def around(C):
    return [turn(W, k) for k in range(N) for W in C]
def self_ok(C):            # a cover and its own turned copies
    T = [[turn(W, k) for W in C] for k in range(N)]
    return all(ok_together(T[i], T[j]) for i in range(N) for j in range(i))
types = sorted(covers)
good = {t: [C for C in covers[t] if self_ok(C)] for t in types}
print({t: len(v) for t, v in good.items()}, 'covers that also fit their turned copies')
layers = []
if len(types) == 1:
    layers = [around(C) for C in good[types[0]]]
else:
    for C0 in good[types[0]]:
        A0 = around(C0)
        for C1 in good[types[1]]:
            A1 = around(C1)
            if ok_together(A0, A1): layers.append(A0 + A1)
            if len(layers) >= 50: break
        if len(layers) >= 50: break
print(f'{len(layers)} complete outer layer(s) with no overlaps')
vol = lambda W: hull(W)[1]
for i, L in enumerate(layers[:50]):
    np.save(f'outer-layer-{TARGET}-{i + 1}.npy', np.array(L, dtype=object), allow_pickle=True)
if layers:
    L = layers[0]; vfill = sum(vol(W) for W in L)
    print(f'first layer: {len(L)} pieces, volume {vfill:.6f} of the ring\'s {TVOL:.6f} ({vfill / TVOL:.1%}); left inside {TVOL - vfill:.6f}')
