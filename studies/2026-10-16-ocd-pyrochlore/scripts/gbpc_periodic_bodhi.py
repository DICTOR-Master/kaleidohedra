# Fable, GBPC pass 4 (2026-10-16): the periodic count with Bodhi pieces (exact in Q(sqrt5)).
# Any piece of edge scale r*phi|v| (r rational) has volume r^3 * phi^3 * dO * (X + Y*phi), X, Y rational. In a periodic fill the sums over one
# cell must give G' = phi^3 dO (X + Y phi) with X = -10/243, Y = 22/243 (gbpc_periodic_count.py). Oblate: X = 1, Y = 0; prolate: X = 0, Y = 1.
# Bodhi pieces: block coordinates x = s a + t b + u c with a, b, c = r*phi times three adjacent five-fold vectors; block cube = prolate.
import os, json, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
q = lambda s: tuple(Fr(x) for x in s.split('|'))
qa = lambda x, y: (x[0] + y[0], x[1] + y[1]); qs = lambda x, y: (x[0] - y[0], x[1] - y[1])
qm = lambda x, y: (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
def qinv(x): n = x[0] * x[0] - 5 * x[1] * x[1]; return (x[0] / n, -x[1] / n)
qf = lambda x: float(x[0]) + float(x[1]) * 5 ** 0.5
def qsgn(x):
    a, b = x
    if a == 0 and b == 0: return 0
    if a >= 0 and b >= 0: return 1
    if a <= 0 and b <= 0: return -1
    return (1 if a > 0 else -1) if a * a - 5 * b * b > 0 else (1 if b > 0 else -1)
Z = (Fr(0), Fr(0)); absq = lambda x: x if qsgn(x) >= 0 else qs(Z, x)
dot = lambda u, v: qa(qa(qm(u[0], v[0]), qm(u[1], v[1])), qm(u[2], v[2]))
cross = lambda u, w: [qs(qm(u[1], w[2]), qm(u[2], w[1])), qs(qm(u[2], w[0]), qm(u[0], w[2])), qs(qm(u[0], w[1]), qm(u[1], w[0]))]
det3 = lambda a, b, c: dot(a, cross(b, c))
vsub = lambda u, v: [qs(a, b) for a, b in zip(u, v)]
G = json.load(open(os.path.join(STUDY, 'data', 'gbpc-geom-exact.json')))
AX5 = [[q(x) for x in v] for v in G['AX5']]
dets = sorted({tuple(absq(det3(*t))) for t in itertools.combinations(AX5, 3)}, key=qf); dO, dP = dets
phi = (Fr(1, 2), Fr(1, 2)); phi3 = qm(qm(phi, phi), phi)
face = [[q(x) for x in v] for v in G['faces'][0]]; fd = absq(det3(*face))
lines = ['DICTO · dictospheres.com', f'oblate det {dO}, prolate det {dP}; block frame (three adjacent five-fold vectors) det {fd}: equals prolate {fd == dP}']
def XY(v):   # v = volume / (r^3 dO) -> divide by phi^3, write as X + Y phi
    x = qm(v, qinv(phi3)); return x[0] - x[1], 2 * x[1]
rows = []
for b, B in G['bodhi'].items():
    blk = [[q(x) for x in c] for c in B['block']]
    cm = [(sum(c[t][0] for c in blk) / len(blk), sum(c[t][1] for c in blk) / len(blk)) for t in range(3)]
    vb = Z
    for fc in B['faces']:
        for t in range(1, len(fc) - 1): vb = qa(vb, absq(det3(vsub(blk[fc[0]], cm), vsub(blk[fc[t]], cm), vsub(blk[fc[t + 1]], cm))))
    vb = qm(vb, (Fr(1, 6), Fr(0)))                 # in block-cube (prolate) units
    v = qm(qm(vb, phi3), qm(fd, qinv(dO)))         # piece at edge scale r*phi|v|: vol / (r^3 dO) = vb * phi^3 * dP / dO
    X, Y = XY(v); rows.append((b, B['name'], vb, X, Y))
    lines.append(f"{b} {B['name']}: volume {vb[0]} + {vb[1]}*sqrt5 prolate blocks; per r^3 phi^3 dO: X = {X}, Y = {Y}" + ('   <- negative X' if X < 0 else ''))
lines.append('periodic fill needs sum r^3 X = -10/243 per cell. Rhombohedra give X >= 0, so pieces with X < 0 are required; at edge scale r = 1/9 (lam):')
for b, nm, vb, X, Y in rows:
    if X < 0: lines.append(f'  {nm} alone: at least {Fr(10, 243) / (-X * Fr(1, 729))} per cell')
print('\n'.join(lines)); open(os.path.join(STUDY, 'data', 'gbpc-periodic-bodhi.txt'), 'w').write('\n'.join(lines) + '\n')
