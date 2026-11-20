# Gaps batch C, item 3 (L36): is the EKP cell (#8: Pm-3, 1b + 12j (0, y, z), y = 1/(2φ), z = 1/(2φ²)) the same structure as the AFLOW
# prototype A12B_cP13_200_j_b-001 (theoretical LiH12: Li 1b, H 12j)? Same Wyckoff set; compare the free parameters under every
# setting change that keeps 1b at 1b and 12j at 12j (sign changes, y <-> z by the quarter turn of the Euclidean normaliser Im-3m,
# lattice translations y -> y + 1, z -> z + 1). -> logs/item3.log
import os, itertools, math
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = []
def log(s=''): print(s); L.append(s)
phi = (1 + 5 ** 0.5) / 2
ekp = (1 / (2 * phi), 1 / (2 * phi ** 2))
cif = open(os.path.join(here, 'data/aflow_A12B_cP13_200_j_b-001.cif')).read().split('\n')
h = [l.split() for l in cif if l.startswith('H2')][0]; li = [l.split() for l in cif if l.startswith('Li1')][0]
a = float([l.split()[1] for l in cif if l.startswith('_cell_length_a')][0])
y2, z2 = float(h[3]), float(h[4])
log(f'AFLOW A12B_cP13_200_j_b-001 (LiH12, theoretical): a = {a} Å, Li {li[-2]}{li[-1]} at ({li[2]}, {li[3]}, {li[4]}), H 12j (0, {y2}, {z2})')
log(f'EKP cell (#8): 12j (0, {ekp[0]:.6f}, {ekp[1]:.6f}), 1b at (1/2, 1/2, 1/2)')
def reduce(y, z):     # canonical form: |values| folded into [0, 1/2], unordered pair
    f = lambda t: min(t % 1, 1 - t % 1)
    return tuple(sorted((f(y), f(z))))
ra, re_ = reduce(y2, z2), reduce(*ekp)
log(f'canonical |y|, |z| (mod 1, folded, unordered): AFLOW {ra[0]:.6f}, {ra[1]:.6f};  EKP {re_[0]:.6f}, {re_[1]:.6f}')
same = all(abs(u - v) < 1e-4 for u, v in zip(ra, re_))
log(f'same parameters: {same}')
# shape of the 12-point cluster around the empty 1a site: regular icosahedron needs |z|/|y| = 1/φ = 0.618034
def cluster(y, z):
    P = []
    for s1, s2 in itertools.product((1, -1), repeat=2):
        for p in [(0, s1 * y, s2 * z), (s2 * z, 0, s1 * y), (s1 * y, s2 * z, 0)]: P.append(p)
    d = sorted(math.dist(p, q) for p, q in itertools.combinations(P, 2))
    return P, d
for nm, (y, z) in (('AFLOW', (y2, z2 - round(z2))), ('EKP', ekp)):
    P, d = cluster(y, z); ratio = min(abs(y), abs(z)) / max(abs(y), abs(z))
    log(f'  {nm}: 12 points (0, {y:.5f}, {z:.5f}) about 1a; small/large = {ratio:.6f}; 30 shortest distances span {d[0]:.5f}..{d[29]:.5f} (a = 1)'
        f' -> {"regular icosahedron" if abs(ratio - 1 / phi) < 1e-6 and abs(d[29] - d[0]) < 1e-9 else "not a regular icosahedron"}')
# controls: the EKP parameters against themselves under y <-> z and sign changes must give same = True; LiH12 against a shifted copy must not change
close = lambda u, v: all(abs(x - w) < 1e-12 for x, w in zip(u, v))
assert close(reduce(-ekp[1], ekp[0] + 1), re_) and close(reduce(z2, -y2), ra) and not close(ra, re_)
log('control: canonical form invariant under y <-> z, sign changes, lattice translations (pass); and it separates AFLOW from EKP (fail case): True')
log('VERDICT: the Wyckoff set 1b + 12j of Pm-3 is in AFLOW as the theoretical LiH12 prototype A12B_cP13_200_j_b-001, '
    'with different free parameters (a distorted 12-point cluster, not a regular icosahedron); the EKP parameters y = 1/(2φ), z = 1/(2φ²) were not found.')
log('FINAL ok')
open(os.path.join(here, 'logs/item3.log'), 'w').write('\n'.join(L) + '\n')
