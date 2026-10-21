# DICTO 2026-10-21: the B1NR partner, staggered ("yes try that; an ideal would be a similarly proportioned unit"). The same honeycomb
# floor as b1nr_partner.py, but each layer shifted so its domes sink into the floor corners of the layer below (three positions,
# ABC). The layers are lowered until they touch. Then the space left is checked for closed pockets: a pocket that does not reach the
# edge of the test block is a natural partner, shaped only by the B1NRs (no cutting rule).
import os, itertools, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'b1nr_partner.py')).read(); exec(src[:src.index('# no overlaps among neighbours')])
s = -2 * d * n0                                             # layer shift: a floor corner
def layer(k, r):
    return [(p + k * s + np.array([0, 0, k * Z]), t) for p, t in sites(r, (0,))]
def over(z):
    global Z; Z = z
    low = [place(p, t) for p, t in layer(0, 2)]; tot = 0.0
    for p, t in layer(1, 2):
        if np.linalg.norm(p[:2]) < 2 * d + 1: u = place(p, t); tot += sum((u ^ l).volume() for l in low)
    return tot
lo, hi = 0.3 * H, H
for _ in range(30):
    mid = (lo + hi) / 2; lo, hi = (mid, hi) if over(mid) > 1e-7 else (lo, mid)
Z = hi; print(f'layer step {Z:.5f} (straight stacking {H:.5f}); overlap at that step {over(Z):.1e}')
AREA = abs(np.cross(a1, a2)[2]); print(f'B1NRs fill {2 * VOL / (AREA * Z) * 100:.2f}% of space')
# pockets: complement in a block, components that stay clear of the block's edge
R = 3.2 * 2 * d; box = m3.Manifold.cylinder(6 * Z, R, R, 48).translate([0, 0, -0.5 * Z])
allb = [place(p, t) for k in range(-1, 7) for p, t in layer(k, 5) if np.linalg.norm(p[:2] - 3 * (k * s)[:2] * 0) < R + 3]
U = m3.Manifold.batch_boolean(allb, m3.OpType.Add); rest = (box - U).decompose()
inner = []
for c in rest:
    b = np.asarray(c.bounding_box()); lo3, hi3 = b[:3], b[3:]
    if np.linalg.norm(lo3[:2]) < R - .3 and np.linalg.norm(hi3[:2]) < R - .3 and lo3[2] > -0.5 * Z + .2 and hi3[2] < 5.5 * Z - .2: inner.append(c)
vols = sorted(round(c.volume(), 4) for c in inner)
print(f'space left: {len(rest)} pieces, {len(inner)} closed pockets; pocket volumes {sorted(set(vols))[:8]} (count {len(vols)})')
print(f'per cell: space left {AREA * Z - 2 * VOL:.4f}; B1NR {VOL:.4f}')
np.save(os.path.join(HERE, 'stagger-step.npy'), np.array([Z]))
