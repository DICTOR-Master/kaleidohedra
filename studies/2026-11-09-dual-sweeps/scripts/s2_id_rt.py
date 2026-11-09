"""Second dual sweep ID ∩ mu·RT, exact in Q(sqrt5). ID = edge midpoints of the icosahedron I with corners the cyclic
permutations of (0, ±1, ±phi); its faces: pentagons normal to I's corners, triangles normal to I's face centres.
RT = polar of ID in the unit sphere = {m.x <= 1 : m a corner of ID}. Birds 1, 2 on this line."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweeplib as L
from sweeplib import F, Q, ZERO, ONE, dot
import drive
import sympy as sp
L.set_field(5)
logf = open(os.path.join(os.path.dirname(__file__), '..', 'data', 's2_id_rt.log'), 'w')
def log(s): print(s); logf.write(s + '\n'); logf.flush()
phi = F(Q(1, 2), Q(1, 2))
I = []
for s1, s2 in itertools.product((1, -1), repeat=2):
    base = [F(0), F(s1), phi * s2]
    for r in range(3):
        I.append(base[r:] + base[:r])
sub = lambda u, v: [a - b for a, b in zip(u, v)]
Iedges = [(i, j) for i, j in itertools.combinations(range(12), 2) if dot(sub(I[i], I[j]), sub(I[i], I[j])) == F(4)]
assert len(Iedges) == 30
ID = [[(a + b) * Q(1, 2) for a, b in zip(I[i], I[j])] for i, j in Iedges]
Ifaces = [t for t in itertools.combinations(range(12), 3) if all(tuple(sorted(p)) in set(Iedges) for p in itertools.combinations(t, 2))]
assert len(Ifaces) == 20
cent = [[I[t[0]][k] + I[t[1]][k] + I[t[2]][k] for k in range(3)] for t in Ifaces]
pl = []
for u in I:
    pl.append((u, max((dot(u, m) for m in ID), key=float), ZERO, 'pent'))
for c in cent:
    pl.append((c, max((dot(c, m) for m in ID), key=float), ZERO, 'tri'))
for m in ID:
    pl.append((m, ZERO, ONE, 'rhomb'))
sw = L.Sweep(pl)
checks = []
# the ID itself (mu large) and the RT (mu small)
stP = sw.structure(F(10)); stS = sw.structure(F(1))
log(f'mu=10: {sw.census(stP)}, {len(stP["V"])} corners; mu=1: {sw.census(stS)}, {len(stS["V"])} corners')
checks.append(('mu=10 is the ID (30 corners, 12 pentagons, 20 triangles)', len(stP['V']) == 30 and sw.census(stP) == {('pent', 5): 12, ('tri', 3): 20}))
checks.append(('mu=1 is a scaled RT (32 corners, 30 rhombi)', len(stS['V']) == 32 and sw.census(stS) == {('rhomb', 4): 30}))
# squared flag radii of the ID
R2 = dot(ID[0], ID[0])
IDedges = [(i, j) for i, j in itertools.combinations(range(30), 2)
           if dot(sub(ID[i], ID[j]), sub(ID[i], ID[j])) == min((dot(sub(ID[0], ID[k]), sub(ID[0], ID[k])) for k in range(1, 30)), key=float)]
assert len(IDedges) == 60
mid = [(a + b) * Q(1, 2) for a, b in zip(ID[IDedges[0][0]], ID[IDedges[0][1]])]
rho2 = dot(mid, mid)
h5 = pl[0][1] * pl[0][1] / dot(pl[0][0], pl[0][0]); h3 = pl[12][1] * pl[12][1] / dot(pl[12][0], pl[12][0])
flags = sorted([h5, h3, rho2, R2], key=float)
log(f'squared flag radii of the ID: pentagon centre {h5} (~{float(h5):.10f}), triangle centre {h3} (~{float(h3):.10f}), '
    f'edge midpoint {rho2} (~{float(rho2):.10f}), corner {R2} (~{float(R2):.10f})')
R = drive.run_line(sw, Q(1), log, 'ID-RT')
ws = [w['mu'] for w in R['walls']]
fw = [f['mu'] for f in R['feet']]
checks.append(('walls = squared flag radii of the ID', ws == flags))
checks.append(('every wall determinant linear in mu, root at the wall', all(w['dets_ok'] for w in R['walls'])))
checks.append(('Euler 2 on both sides of every wall', all(w['kind']['euler'] == (2, 2) for w in R['walls'])))
c = ws[0] * ws[-1]
sym = drive.symmetric_under(ws, c)
log(f'turn test: c = first*last = {c}; walls symmetric under mu -> c/mu: {sym}; products of mirrored pairs: {ws[0]*ws[3]} vs {ws[1]*ws[2]}')
ev = sorted(set(ws) | set(fw), key=float)
log(f'all events (S walls + foot walls): {ev} ~ {[round(float(x), 10) for x in ev]}')
for cc in [ev[0] * ev[-1]]:
    log(f'  all events symmetric under {cc}/mu: {drive.symmetric_under(ev, cc)}')
checks.append(('no turn: walls not symmetric under first*last', not sym))
# antipol is off the line
on_line = []
for mu in [ws[1] + (ws[2] - ws[1]) * Q(1, 2), ws[2] + (ws[3] - ws[2]) * Q(1, 3)]:
    st = sw.structure(mu)
    Sv = L.Sweep(sw.antipol_planes(st, mu))
    fams = Sv.census(Sv.structure(ZERO))
    # S^v has pentagon planes at 1/h5, triangle planes at 1/h3: ratio of distances inverted, so not ID's ratio
    log(f'antipol at mu ~ {float(mu):.6f}: census {fams}')
ratio = (h3 / h5)
log(f'h3^2/h5^2 = {ratio} (~{float(ratio):.10f}); antipol inverts it to {ONE / ratio}: the antipol line has a different pentagon:triangle ratio, so it is not this line')
checks.append(('antipol leaves the line (h3 != h5)', ratio != ONE))
res = drive.tmin_envelope(sw, ev, log, 'ID-RT')
best = max(res, key=lambda r: r['fvalue'])
inter = [r for r in res if r['interior']]
log(f'sup t_min on the open line: {best["value"]} (~{best["fvalue"]:.12f}) at mu = {best["argmax"]} (~{float(best["argmax"]):.12f})')
for r in inter:
    a, b = r['interval']
    gm = sp.sqrt(a.sym() * b.sym())
    log(f'interior max on ({a}, {b}) at {sp.simplify(r["argmax"])}; geometric mean of the interval ends {sp.simplify(gm)} (~{float(gm):.10f}); equal: {sp.simplify(r["argmax"] - gm) == 0}')
for mu in [F(1), F(10)]:
    t, _, _ = sw.tmin(mu); log(f't_min({mu}) = {t} (~{float(t):.10f})')
for n, ok in checks: log(('ok   ' if ok else 'FAIL ') + n)
allok = all(ok for _, ok in checks)
log('FINAL ok' if allok else 'FINAL FAIL: ' + '; '.join(n for n, ok in checks if not ok))
