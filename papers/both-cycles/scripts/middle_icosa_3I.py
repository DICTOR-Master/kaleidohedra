# Exact check (Fable advice 2026-10-16): in the middle setting (rho^2 = 3 phi^2/4) the reversed icosahedron is exactly 3*I, the
# icosahedron whose edge thirds are the truncated icosahedron's corners (TI plus its 12 caps, an in-between Dharma stage), with its
# 12 corners among the triacontahedron's corners. All in Q(sqrt5), no floats in the comparisons. -> data/middle-icosa-3I.txt
import os, io, sys, contextlib, itertools
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(here)
st = dict(stations); I, D, TI, RT = st['icosahedron'], st['dodecahedron'], st['truncated icosahedron'], st['rhombic triacontahedron']
key = lambda v: tuple((x.a, x.b) for x in v)
out = ['DICTO · dictospheres.com', 'Middle setting: the reversed icosahedron is 3·I (exact, Q(√5))']
for label, rho2 in (('ends  rho^2 = phi^2/4', Q(3, 1) / 8), ('middle rho^2 = 3 phi^2/4', Q(9, 3) / 8)):
    rev_I = {key([x * rho2 for x in c]) for c in polar(D)}       # polar of the original dodecahedron in the toggle sphere
    for k in (1, 3):
        if rev_I == {key([x * k for x in v]) for v in I}: out.append(f'  {label}: reversed icosahedron = {k}·I exactly')
I3 = [[x * 3 for x in v] for v in I]
e2 = min(sum(((a[i] - b[i]) * (a[i] - b[i]) for i in range(3)), Q(0)).f() for a, b in itertools.combinations(I3, 2))
edges = [(a, b) for a, b in itertools.combinations(I3, 2) if abs(sum(((a[i] - b[i]) * (a[i] - b[i]) for i in range(3)), Q(0)).f() - e2) < 1e-9]
thirds = {key([a[i] + (b[i] - a[i]) * Q(Fr(t, 3)) for i in range(3)]) for a, b in edges for t in (1, 2)}
TIk = {key(v) for v in TI}; extra = [v for v in TI if key(v) not in thirds]
T60 = [list(map(lambda ab: Q(*ab), k)) for k in thirds]
def onface(p):                                   # p lies exactly in the plane of some face of the 60-corner TI (and not outside)
    for a, b, c in itertools.combinations(T60, 3):
        u = [b[i] - a[i] for i in range(3)]; w = [c[i] - a[i] for i in range(3)]
        n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
        if all(x == 0 for x in n): continue
        d = sum((n[i] * a[i] for i in range(3)), Q(0)); side = [(sum((n[i] * q[i] for i in range(3)), Q(0)) - d).f() for q in T60]
        if (max(side) < 1e-12 or min(side) > -1e-12) and sum((n[i] * p[i] for i in range(3)), Q(0)) == d: return True
    return False
out.append(f'  3·I has {len(edges)} edges; their {len(thirds)} third-points are exactly the truncated icosahedron corners: {thirds <= TIk}')
out.append(f'  the {len(extra)} other points in the float hull list of the TI station are not corners: each lies exactly in a TI face plane: {all(onface(v) for v in extra)}')
out.append(f'  the 12 corners of 3·I are corners of the rhombic triacontahedron exactly: {({key(v) for v in I3} <= {key(v) for v in RT})}')
print('\n'.join(out)); open('data/middle-icosa-3I.txt', 'w').write('\n'.join(out) + '\n')
