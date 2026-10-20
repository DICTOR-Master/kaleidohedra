# DICTO 2026-10-20: the OCD Stella with octahedra ("the Stella with holes"), exact in Q(sqrt5). First found 2026-10-16 (float,
# studies/2026-10-16-ocd-pyrochlore, stella_octahedra.py, stella_octa_pyro.py; app: OCD Stella Crystals, partner octahedra, Notches).
# Frame of #37: the OCD's bcc packing has sites (2R/3)(a,b,c), a,b,c all even or all odd, R = 2phi/3; its Voronoi cell is the truncated
# octahedron |x|+|y|+|z| <= R, |x|,|y|,|z| <= 2R/3; the regular octahedron of the 8 joint (hexagon) planes is |x|+|y|+|z| <= R.
# Checks: cell and octahedron; the Stella (built exactly by stella_twin_exact.py) in its cell; which neighbours' octahedra reach a
# Stella (only the 6 square neighbours' tips); the notch of one tip, all 6 equal; octahedra meet face to face across hexagon walls and
# overlap tip to tip across square walls (so no two octahedra may be square neighbours); fills of the pyrochlore (octahedra on one
# diamond network, half the sites) and rock-salt (a quarter) crystals; the notched Stella.
import os, sys, io, contextlib, itertools, json
ME = os.path.dirname(os.path.abspath(__file__)); GY = os.path.join(ME, '..', '2026-10-19-og-gyrated-octet')
sys.path.insert(0, os.path.join(ME, '..', '2026-10-18-ocd-octet', 'scripts'))
import q5
from exactpoly import planes_of, intersect, volume
from q5 import Fr, Z, ONE, qr, qa, qs, qm, qd, qf, qn, dot, vsub, vadd, vmul, qs_
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True)
qstr = lambda x: f'{x[0]} + {x[1]}*sqrt5 = {qf(x):.6f}'
# the exact Stella in this frame, from the gyrated-octet study's script (its own Q numbers -> pairs)
g = {}
here = os.getcwd()
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(GY, 'stella_twin_exact.py')).read(), g)
os.chdir(here)
SV = [[(x.a, x.b) for x in v] for v in g['SV']]
R = (Fr(1, 3), Fr(1, 3)); TR = qm(R, qr(Fr(2, 3)))
cellv = qm(qr(Fr(32, 27)), qm(R, qm(R, R))); octv = qm(qr(Fr(4, 3)), qm(R, qm(R, R)))
ok(cellv == (Fr(512, 729), Fr(256, 729)), f'cell (truncated octahedron) {qstr(cellv)} = #31a\'s cell')
ok(qd(octv, cellv) == qr(Fr(9, 8)), 'the octahedron of the 8 joint planes is 9/8 of the cell')
signs = list(itertools.product((1, -1), repeat=3))
OCTP = [([qr(a), qr(b), qr(c)], R) for a, b, c in signs]
CELLP = OCTP + [([qr(s) if i == k else Z for i in range(3)], TR) for k in range(3) for s in (1, -1)]
ok(volume(intersect(CELLP)) == cellv, 'the cell is the octahedron cut by the 6 square walls |x_i| <= 2R/3')
SP = planes_of(SV); vS = volume(SV)
ok(vS == (Fr(-4064, 729), Fr(2240, 729)), f'OCD Stella {qstr(vS)} (#31a)')
ok(volume(intersect(SP + CELLP)) == vS, 'the Stella lies in its cell')
sh = lambda P, t: [(n, qa(d, dot(n, t))) for n, d in P]
site = lambda a, b, c: [qm(TR, qr(a)), qm(TR, qr(b)), qm(TR, qr(c))]
nbrs = [(a, b, c) for a, b, c in itertools.product(range(-4, 5), repeat=3) if (a % 2 == b % 2 == c % 2) and (a, b, c) != (0, 0, 0) and a * a + b * b + c * c <= 16]
reach = {}
for m in nbrs:
    x = volume(intersect(SP + sh(OCTP, site(*m))))
    if x != Z: reach[m] = x
sq = {m for m in nbrs if sorted(map(abs, m)) == [0, 0, 2]}
ok(set(reach) == sq and len(set(reach.values())) == 1, f'only the 6 square neighbours\' octahedra reach a Stella, each tip taking the same notch')
n = next(iter(reach.values())); print(f'      one notch {qstr(n)} ({qf(n) / qf(vS):.4%} of the Stella); six {qstr(qm(qr(6), n))} ({6 * qf(n) / qf(vS):.4%})')
tipv = volume(intersect(OCTP + [([qn(ONE), Z, Z], qn(TR))]))   # a tip beyond a square wall: x >= 2R/3
ok(tipv == qm(cellv, qr(Fr(1, 48))), f'each octahedron tip beyond a square wall is 1/48 of the cell, {qstr(tipv)}; the Stella takes {qf(n) / qf(tipv):.2%} of it into its notch')
# octahedron against octahedron: hexagon (nearest) neighbours face to face; square neighbours overlap tip to tip
hexn = [m for m in nbrs if sorted(map(abs, m)) == [1, 1, 1]]
ok(all(volume(intersect(OCTP + sh(OCTP, site(*m)))) == Z for m in hexn), 'octahedra on hexagon neighbours meet face to face (no overlap)')
oo = volume(intersect(OCTP + sh(OCTP, site(2, 0, 0))))
ok(qf(oo) > 0, f'octahedra on square neighbours would overlap tip to tip ({qstr(oo)}), so no two octahedra may be square neighbours')
others = [m for m in nbrs if m not in hexn and m not in sq]
ok(all(volume(intersect(OCTP + sh(OCTP, site(*m)))) == Z for m in others), 'farther octahedra never overlap')
# the crystals. Square neighbours change (a+b+c)/2 (even sites) or (a+b+c-1)/2 (odd sites) by one, so the classes mod 2 of each parity
# give four fcc sublattices; octahedra on one even and one odd class (one diamond network) are never square neighbours: pyrochlore.
# Every Stella then has all 6 square neighbours octahedra (6 notches); rock salt: octahedra on one class (a quarter), Stellas notched
# by the octahedra around them, on average 6 * (1/4) / (3/4) = 2 notches each.
pyro = qd(qs(qa(octv, vS), qm(qr(6), n)), qm(qr(2), cellv))
rock = qd(qs(qa(octv, qm(qr(3), vS)), qm(qr(6), n)), qm(qr(4), cellv))
alone = qd(vS, cellv)
print(f'      pyrochlore (octahedra on one diamond network, every Stella notched 6 times): fill {qstr(pyro)} ({qf(pyro):.4%})')
print(f'      rock salt (octahedra on a quarter of the sites): fill {qstr(rock)} ({qf(rock):.4%})')
print(f'      OCD Stellas alone: {qstr(alone)} ({qf(alone):.4%})')
ok(abs(qf(pyro) - 0.9633) < 5e-5 and abs(qf(rock) - 0.9172) < 5e-5, 'the float fills of 2026-10-16 (96.33%, 91.72%) agree')
gap = qs(ONE, pyro); print(f'      pyrochlore gap {qstr(gap)} ({qf(gap):.4%}): the cell outside the Stella and the 6 tips, per Stella cell; octahedra fill their own cells whole')
# octahedron's own cell: is the octahedron less its tips the whole cell? (octahedron & cell = cell, i.e. the cell lies in the octahedron)
ok(volume(intersect(OCTP + CELLP)) == cellv, 'the octahedron covers its whole cell (the cell lies in it); its 6 tips are the excess, 6/48 = 1/8 of a cell')
notched = qs(vS, qm(qr(6), n)); print(f'      notched OCD Stella (6 notches) {qstr(notched)}')
json.dump(dict(mark='DICTO · dictospheres.com', cell=qs_(cellv), octahedron=qs_(octv), stella=qs_(vS), notch=qs_(n), tip=qs_(tipv), notched_stella=qs_(notched),
               fill_pyrochlore=qs_(pyro), fill_rock_salt=qs_(rock), fill_alone=qs_(alone), stella_V=[[qs_(x) for x in v] for v in SV]),
          open(os.path.join(ME, 'stella-octa-exact.json'), 'w'), indent=1, ensure_ascii=False)
print('saved stella-octa-exact.json')
