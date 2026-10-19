# EXACT check of the tall PiTet (Kepler–Poinsot) cycle in Q(sqrt5), DICTO 2026-10-19:
#   I (edge 1) -> great stellated dodecahedron (tips 3 x face centre) -> hull D1 -> small stellated dodecahedron (tips sqrt5 x face centre)
#   -> hull I2 = phi^3 I exactly; the stars' spikes; the valleys filled by the Cleo-star pattern (inward pyramids + valley tetrahedra):
#   exact volumes, sum = valley, every piece inside the hull and outside the core, no two pieces overlapping (exact separating planes).
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '2026-10-19-five-fold-octet'))
from exact_cycle import Q5, Fr, PHI, dot
from exact_shells import cross, sub
from exact_inner import hullH, piece, check
z, h = Q5(0), Q5(Fr(1, 2))
I = [v for a, b in ((h, PHI / 2),) for v in [(z, sa * a, sb * b) for sa in (1, -1) for sb in (1, -1)] +
     [(sb * b, z, sa * a) for sa in (1, -1) for sb in (1, -1)] + [(sa * a, sb * b, z) for sa in (1, -1) for sb in (1, -1)]]
cent = lambda P: tuple(sum((p[k] for p in P), Q5(0)) / len(P) for k in range(3))
def star(core, f):
    """spikes on every face of core: tip = f x the face centre (the foot of the centre's perpendicular, the face being regular)"""
    H = hullH(core); out = []
    for o, _ in H['F']:
        F = [H['C'][j] for j in o]; tip = tuple(f * x for x in cent(F)); out.append((F, tip))
    return H, out
log = {'mark': 'DICTO tall PiTet (Kepler-Poinsot), exact, 2026-10-19'}
HI, gsd = star(I, Q5(3)); D1 = [t for _, t in gsd]
HD, ssd = star(D1, Q5(0, 1)); I2 = [t for _, t in ssd]
phi3 = PHI * PHI * PHI
log['I2_is_phi3_I'] = set(I2) == {tuple(phi3 * x for x in v) for v in I}
log['D1_is_a_dodecahedron'] = len(set(D1)) == 20 and len({repr(dot(v, v)) for v in D1}) == 1
print({k: v for k, v in log.items() if k != 'mark'}, flush=True)
def shell(core, Hcore, spikes, hullpts, name):
    sp = [piece(F + [tip]) for F, tip in spikes]; Hh = hullH(hullpts)
    pyr = []
    for o, i in Hh['F']:
        F = [Hh['C'][j] for j in o]; n, d = Hh['H'][i]; c = max(core, key=lambda v: dot(n, v).f()); pyr.append(piece(F + [c]))
    e2 = min(dot(sub(a, b), sub(a, b)).f() for a, b in itertools.combinations(core, 2)); tets = []
    for a, b in itertools.combinations(core, 2):
        if abs(dot(sub(a, b), sub(a, b)).f() - e2) > 1e-9: continue
        two = [tip for F, tip in spikes if a in F and b in F]
        if len(two) == 2: tets.append(piece([a, b] + two))
    # the star = core + spikes, as one inner solid for the valley check: valley pieces must lie outside the core and each spike
    check(f'{name}: spikes (core -> star)', sp, Hcore, Hh, log)
    check(f'{name}: valleys (star -> hull) = {len(pyr)} inward pyramids + {len(tets)} valley tetrahedra', pyr + tets + sp, Hcore, Hh, log)
    log[f'{name}: volumes'] = {'spike': repr(sp[0]['V']), 'inward_pyramid': repr(pyr[0]['V']), 'valley_tet': repr(tets[0]['V']),
                               'one_kind_each': all(len({repr(p['V']) for p in g}) == 1 for g in (sp, pyr, tets))}
    return Hh
HD1 = shell(I, HI, gsd, D1, 'great stellated shell')
shell(D1, HD, ssd, I2, 'small stellated shell')
json.dump(log, open(os.path.join(HERE, 'exact_kp.json'), 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in log.items() if 'volumes' in k}, indent=1, default=str))
