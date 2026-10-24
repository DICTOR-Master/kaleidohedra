# Delian Ball set, step 2: keep the rounded tetrahedron's corner balls as in Ball set 1 and grow only its 4 face bumps (face-ball offset and
# radius times k), so the extra volume goes into the octahedra, where there is room. Find k with tet = 2/3 = ball, and check no overlaps
# (neighbouring tetrahedra, and the pieces of a 2x2x2 block summing to 8 with no overlap).
import itertools, sys, numpy as np, manifold3d as m3
sys.argv = ['x']; src = open('roundtet_octet.py').read().split("if __name__ == '__main__':")[0]; exec(src)
def filler_b(V, k, kr):
    V = np.array(V, float); t = V.mean(0); P = []
    for j in range(4):
        P.append(balls(t + S_CORNER * (V[j] - t), R_CORNER))
        n = t - V[j]; n /= np.linalg.norm(n); P.append(balls(t + k * D_FACE * n, kr * R_FACE))
    return hull(np.vstack(P))
t0 = np.array([.5, .5, .5]); V0 = tet_around(t0); neigh = [t0 + np.array(d) for d in itertools.product((-1, 0, 1), repeat=3) if any(d)]
def row(k, kr):
    F0 = filler_b(V0, k, kr); return F0.volume(), max((F0 ^ filler_b(tet_around(t), k, kr)).volume() for t in neigh)
best = None
for kr in [1.0, 1.5, 2.0, 2.5, 3.0]:
    lo, hi = 1.0, 4.0
    if row(hi, kr)[0] < 2 / 3: print(f'radius x{kr}: cannot reach 2/3'); continue
    for _ in range(34):
        mid = (lo + hi) / 2
        if row(mid, kr)[0] < 2 / 3: lo = mid
        else: hi = mid
    v, ov = row(lo, kr); print(f'bump radius x{kr}: offset x{lo:.4f} gives tet {v:.6f} (2/3); worst neighbour overlap {ov:.2e}')
    if ov < 1e-6 and best is None: best = (lo, kr)
if best:
    k, kr = best; F = lambda V: filler_b(V, k, kr)
    def ball(c):
        c = np.array(c, float); m = rd(c)
        for s in itertools.product((1, -1), repeat=3): m = m - F(tet_around(c + .5 * np.array(s)))
        return m
    pieces = [('ball', ball((x, y, z))) for x, y, z in itertools.product(range(-1, 4), repeat=3) if (x + y + z) % 2] + [('tet', F(V)) for _, V in tets_in(range(-1, 3))]
    box = m3.Manifold.cube([2, 2, 2]); inb = [(n_, p ^ box) for n_, p in pieces]; inb = [(n_, p) for n_, p in inb if p.volume() > 1e-9]
    tot = sum(p.volume() for _, p in inb); over = sum((a ^ b).volume() for (_, a), (_, b) in itertools.combinations(inb, 2))
    B = ball((1, 0, 0)); T = F(V0)
    print(f'\nDELIAN BALL SET: bump offset x{k:.4f}, radius x{kr}: ball {B.volume():.6f}, tet {T.volume():.6f}, ball genus {B.genus()}; 2x2x2 box {tot:.5f} (8), overlap {over:.2e} ->', 'PASS' if abs(tot - 8) < 2e-3 and over < 2e-3 else 'FAIL')
    import json; json.dump(dict(k_offset=k, k_radius=kr, ball=B.volume(), tet=T.volume(), box=tot, overlap=over), open('delian-ball.json', 'w'), indent=1)
    for nm, M in (('ball', B), ('tet', T)):
        me = M.to_mesh(); np.save(f'delian-{nm}-V.npy', np.asarray(me.vert_properties)[:, :3]); np.save(f'delian-{nm}-F.npy', np.asarray(me.tri_verts))
