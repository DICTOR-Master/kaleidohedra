# The DICTO OCD Stella in the octet and the gyrated octet, exact in Q(sqrt5) (DICTO 2026-10-19 "what about OCD Stella"; float first look
# in README). Builds the Stella exactly with studies/2026-10-16-ocd-pyrochlore/scripts/stella_cut_exact.py (same frame as the OG in #37:
# octahedron |x|+|y|+|z| <= R, R = 2phi/3), then checks: the Stella lies in the octahedron; its 8 joint triangles lie on the 8 faces;
# its share of the octahedron; the joint triangle's share of a face; its mirror twin in a face = the Stella turned 60 degrees.
import os, sys, io, contextlib, itertools
from fractions import Fraction as Fr
PY = os.path.expanduser('~/kaleidohedra/studies/2026-10-16-ocd-pyrochlore'); os.chdir(PY)
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/stella_cut_exact.py').read())
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True)
R = Q(Fr(1, 3), Fr(1, 3))
# The Stella study's bcc lattice sits in a golden orientation; turn the Stella into the #37 frame first. The cube axes of the bcc lattice are
# its lattice vectors of length c = 4R/3; the rotation with those axes as rows (entries in Q(sqrt5)) is chosen so that the OCD lands exactly
# on the #37 OG (studies/2026-10-18-ocd-octet/data/step1-ocd-exact.json).
c = R * Q(Fr(4, 3)); c2 = c * c; Zq = Q(0)
lat = []
for m in itertools.product(range(-2, 3), repeat=3):
    t = [Zq, Zq, Zq]
    for k, b in zip(m, LB): t = add(t, mul(b, Q(k)))
    if dot(t, t) == c2: lat.append(t)
axes = None
for a, b in itertools.combinations(lat, 2):
    if dot(a, b) == Zq:
        cc = cross(a, b); cc = [x / c for x in cc]
        if any(key(cc) == key(t) for t in lat): axes = [a, b, cc]; break
ok(axes is not None, f'the bcc lattice has three orthogonal cube vectors of length 4R/3 ({len(lat)} of that length)')
import json as _j
OGD = _j.load(open(os.path.expanduser('~/dbt-exact/2026-10-18-ocd-octet/data/step1-ocd-exact.json')))
pq = lambda s_: (lambda a, b: Q(Fr(a), Fr(b)))(*s_.split('|'))
OG = {key([pq(x) for x in v]) for v in OGD['V']}
M = None
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        rows = [[x * Q(sg[i]) / c for x in axes[perm[i]]] for i in range(3)]
        if {key([dot(rw, v) for rw in rows]) for v in OCD} == OG: M = rows; break
    if M: break
ok(M is not None, 'a rotation onto the cube axes carries the Stella study\'s OCD exactly onto the #37 OG')
SV = [[dot(rw, v) for rw in M] for v in S['V']]
signs = [[Q(a), Q(b), Q(c)] for a, b, c in itertools.product((1, -1), repeat=3)]
ok(all(sgn(R - dot(s, v)) >= 0 for s in signs for v in SV),
   f'Stella ({len(SV)} corners) lies in the octahedron |x|+|y|+|z| <= R')
on = {tuple(s[i].a for i in range(3)): [v for v in SV if dot(s, v) == R] for s in signs}
ok(all(len(x) == 3 for x in on.values()), 'each of the 8 octahedron faces holds exactly 3 Stella corners (its joint triangle)')
tri = on[(1, 1, 1)]; s2 = [dot(sub(a, b), sub(a, b)) for a, b in itertools.combinations(tri, 2)]
ok(len({(x.a, x.b) for x in s2}) == 1, f'the joint triangle is equilateral, side^2 = {s2[0]!r}')
octv = Q(Fr(64, 81), Fr(32, 81)); vS = pvol(S)
print(f'      Stella volume {vS!r} = {vS.f():.6f}; octahedron (64 + 32*sqrt5)/81 = {octv.f():.6f}; share {(vS / octv)!r} = {(vS / octv).f():.6f}')
edge2 = R * R * 2; share = s2[0] / edge2
ok(True, f'joint triangle / octahedron face (similar, concentric) = side^2/edge^2 = {share!r} = {share.f():.6f}')
# the mirror twin across x+y+z = R, moved back by t = (2R/3)(1,1,1), against the Stella turned 60 degrees about (1,1,1)
n = [Q(1), Q(1), Q(1)]
mir = lambda v: [v[k] - (dot(n, v) - R) * Q(Fr(2, 3)) for k in range(3)]
t = R * Q(Fr(2, 3))
twin = {key([x - t for x in mir(v)]) for v in SV}
F3 = lambda a: Q(Fr(a, 3)); R60 = [[F3(2), F3(-1), F3(2)], [F3(2), F3(2), F3(-1)], [F3(-1), F3(2), F3(2)]]
rot = lambda v: [R60[i][0] * v[0] + R60[i][1] * v[1] + R60[i][2] * v[2] for i in range(3)]
ok(twin == {key(rot(v)) for v in SV}, 'the mirror twin in a face = the Stella turned 60 degrees about the joint three-fold axis (spinel law, as the OG)')
ok(twin != {key(v) for v in SV}, 'and it is not the Stella itself (a true twin, not a translate)')
mt = {key(mir(v)) for v in SV}
ok({key(v) for v in tri} <= mt, 'twin Stellas meet on the whole joint triangle (the mirror fixes the face)')
import json as _js
_js.dump({'mark': 'DICTO · dictospheres.com', 'note': 'OCD Stella in the #37 frame (float copy of the exact corners)', 'V': [[x.f() for x in v] for v in SV]},
         open(os.path.expanduser('~/dbt-exact/2026-10-19-og-gyrated-octet/stella-37frame.json'), 'w'))
print('wrote stella-37frame.json')
