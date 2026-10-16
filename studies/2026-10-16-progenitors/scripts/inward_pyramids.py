# Progenitors step 10 (DICTO 2026-10-16: "how about the 12 five-sided pyramids of Hypsicles pointing inwards"): on each pentagonal face of D'
# (the Cleo star's hull) a pentagonal pyramid pointing inward, apex at the icosahedron corner below it. Exact in Q(sqrt5): do the 12 overlap the
# Cleo spikes or I? their volume, height, apex angle; what is left of the star–D' gap; and how they compare with D's central (Hypsicles) pyramids.
# -> data/inward-pyramids.txt
exec(open('scripts/cleo_star_station.py').read().split("print('\\n'.join(out))")[0])
from scipy.spatial import Delaunay
plD = planes_exact(Dp)
pyr = []                                                           # (apex = I corner, base = D' face corners)
for n, d in plD:
    base = [v for v in Dp if dot(n, v) == d]
    apex = max(I, key=lambda v: dot(n, v).f())
    pyr.append((apex, base))
# overlap test (float, robust margins): sample interior points of each pyramid; none may lie inside I or inside a spike
If = np.array([[x.f() for x in v] for v in I]); hI = ConvexHull(If)
spk = []
for s in hI.simplices:
    c = If[s].mean(0); spk.append(Delaunay(np.vstack([If[s], 2 * c])))
inI = Delaunay(If)
rng = np.random.default_rng(1); bad = 0
for apex, base in pyr:
    P = np.array([[x.f() for x in v] for v in [apex] + base])
    for _ in range(4000):
        w = rng.dirichlet(np.ones(len(P))); p = w @ P
        if inI.find_simplex(p) >= 0 or any(sp.find_simplex(p) >= 0 for sp in spk): bad += 1
out.append(f'  12 inward pentagonal pyramids (base a face of D\', apex the I corner below): interior points inside I or a spike: {bad} of 48000')
# exact: is each pyramid's side face in the plane of a spike face? (apex, t_i, t_i+1) vs spike faces through apex
apex, base = pyr[0]
vols = [volume([apex] + base, np.array([[x.f() for x in v] for v in [apex] + base])) for apex, base in pyr]
n0, d0 = plD[0]; _hh = d0 - dot(n0, apex); h2 = _hh * _hh / dot(n0, n0)
out.append(f'  each: volume {vols[0]!r} = {vols[0].f():.6f} (all equal: {len(set((v.a, v.b) for v in vols)) == 1}), height² {h2!r} = {h2.f():.6f}')
tot = vols[0] * 12; rest = gap - tot
out.append(f'  12 pyramids = {tot!r} = {tot.f():.6f} of the gap {gap.f():.6f}; left: {rest!r} = {rest.f():.6f} ({rest.f() / gap.f() * 100:.1f}%), the valleys along the 30 edges of I')
# Hypsicles: D's own central pyramid (apex at the centre) on the same face, height = inradius of D'
r2in = d0 * d0 / dot(n0, n0); out.append(f'  D\'s central (Hypsicles) pyramid on that face: height² {r2in!r} = {r2in.f():.6f}; inward pyramid height / Hypsicles height = {(h2.f() / r2in.f()) ** .5:.6f}')
print('\n'.join(out[-5:])); open('data/inward-pyramids.txt', 'w').write('\n'.join(out) + '\n')
