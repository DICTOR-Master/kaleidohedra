# DICTO 2026-10-18 bcc golden kit -- STEP 3: (a) the envelope overlaps given to one side as keys (the octet's trick), exactly; (b) as DICTO
# says "cant see the minimal solution without penrose": where the five-fold corners of neighbouring envelopes face each other in the bcc
# packing, and whether those corners are free (in G') or buried -- the places a Penrose link could go. -> data/step3-keys.json
import itertools
from exactpoly import *
G = json.load(open(os.path.join(HERE, '..', '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json')))
RT = [[q(x) for x in v] for v in G['RT']]; LB = [[q(x) for x in v] for v in G['LB']]
PR = planes_of(RT)
def lat(c):
    o = [Z, Z, Z]
    for k, Lv in zip(c, LB): o = vadd(o, vmul(Lv, qr(k)))
    return o
nbs = [lat(c) for c in itertools.product(range(-3, 4), repeat=3) if c != (0, 0, 0)]
d2 = sorted({qs_(dot(o, o)) for o in nbs}, key=lambda s: qf(q(s)))
shell = lambda k: [o for o in nbs if qs_(dot(o, o)) == d2[k]]
first, second, third = shell(0), shell(1), shell(2)
# (a) overlaps with first neighbours
ov = []
for t in first:
    c = intersect(PR + shift(PR, t)); ov.append((t, c, volume(c)))
vols = {qs_(v) for _, _, v in ov}
corner_counts = {len(c) for _, c, _ in ov}
# is each overlap a golden rhombohedron? 8 corners, 12 equal edges along five-fold axes
def is_rhombohedron(c):
    if len(c) != 8: return False
    cf = np.array([[qf(x) for x in p] for p in c]); h = ConvexHull(cf)
    E = set()
    for s in h.simplices:
        for i, j in ((s[0], s[1]), (s[1], s[2]), (s[0], s[2])): E.add((min(i, j), max(i, j)))
    lens = sorted({qs_(dot(vsub(c[i], c[j]), vsub(c[i], c[j]))) for i, j in E}, key=lambda s: qf(q(s)))
    return lens[0]
edge_info = is_rhombohedron(ov[0][1])
# no point in three envelopes: pairwise overlaps of overlaps (from the same RT) have zero volume
triple = max((qf(volume(intersect(PR + shift(PR, a) + shift(PR, b)))) for a, b in itertools.combinations(first + second, 2)), default=0)
# the key rule: OCD at 0 keeps the overlap towards t when t is in the tetrahedral class + (sign product of t's coordinates > 0)
cls = lambda t: (1 if sgn(t[0]) * sgn(t[1]) * sgn(t[2]) > 0 else -1)
kept = [t for t in first if cls(t) > 0]; given = [t for t in first if cls(t) < 0]
consistent = all(cls([qn(x) for x in t]) < 0 for t in kept)   # the neighbour at t sees the same overlap at -t, class -: does not claim it
RTvol = volume(intersect(PR)); ovol = q(next(iter(vols)))
keyed_env = qs(RTvol, qm(qr(4), ovol))
cell = det3(*LB); cell = cell if sgn(cell) > 0 else qn(cell)
# (b) five-fold corners: RT corners at the largest radius are the 12 five-fold ones? (RT: 12 five-fold, 20 three-fold)
r2 = [dot(v, v) for v in RT]; radii = sorted({qs_(x) for x in r2}, key=lambda s: qf(q(s)))
by_r = {s: [v for v, x in zip(RT, r2) if qs_(x) == s] for s in radii}
five = [v for v in RT if len([w for w in RT if dot(vsub(v, w), vsub(v, w)) == min((dot(vsub(v, u), vsub(v, u)) for u in RT if u != v), key=qf)]) == 5]
inside_other = lambda p: any(all(sgn(qs(dd, dot(n, vsub(p, t)))) > 0 for n, dd in PR) for t in first + second + third)
facing = []
for v in five:
    for t in nbs:
        w = vsub(t, v)                         # the neighbour's antiparallel five-fold corner
        if not any(all(a == b for a, b in zip(w, vsub(t, u))) for u in five): continue
        dv = vsub(w, v); along = qd(dot(dv, v), dot(v, v)); side = vsub(dv, vmul(v, along))
        if qf(dot(dv, dv)) < 1.0: facing.append(dict(t=[qs_(x) for x in t], t_dist2=qs_(dot(t, t)), gap2=qs_(dot(dv, dv)), gap=qf(dot(dv, dv)) ** .5,
                                                along=qf(along) * qf(dot(v, v)) ** .5, sideways=qf(dot(side, side)) ** .5))
free = [not inside_other(v) for v in five]
checks = dict(radii2=radii, five_fold_corners=len(five), five_fold_corners_free_in_Gprime=sum(free),
              first_overlaps=len(ov), overlap_volumes=sorted(vols), overlap_corners=sorted(corner_counts), overlap_shortest_edge2=edge_info,
              max_triple_overlap=triple, key_rule_consistent=consistent, RT_volume=qs_(RTvol), keyed_envelope=qs_(keyed_env), keyed_envelope_float=qf(keyed_env),
              cell=qs_(cell), envelopes_per_cell=1, envelopes_fill=qs_(qd(keyed_env, cell)), envelopes_fill_float=qf(qd(keyed_env, cell)), Gprime_share=qs_(qs(ONE, qd(keyed_env, cell))), Gprime_share_float=1 - qf(qd(keyed_env, cell)), facing_fivefold_pairs=sorted(facing, key=lambda f: f['gap'])[:6])
print(json.dumps(checks, indent=1)); save('step3-keys.json', dict(mark=MARK, step=3, checks=checks))
