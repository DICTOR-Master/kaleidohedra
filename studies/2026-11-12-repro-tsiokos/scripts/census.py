# census.py: independent recount (our own code) of the lattice-registered contact census of Tsiokos, "A Strongly Aperiodic Monotile in
# Three Dimensions" (Chair44 / R44; aiXiv 2609.02383, arXiv 2609.19214): 2388 candidate contact poses, of which exactly 44 are legal
# for the solid's pyramid features. From the paper (§2): chair P = union of a + [0,1]^3, a in {0,1}^3 minus (1,1,1); 24 panels, each
# with 8 square-pyramid features at offsets (+-1/8, +-1/4), (+-1/4, +-1/8) from the panel centre (in-panel axes = the other two axes in
# increasing order), signed height a/10000 along the outward normal; "when two panels meet face to face ... at each point where
# features coincide a bump must meet a dent of the same magnitude". Input: his panel table solid/native_panels.csv (data; read, not run).
# Poses: x -> g x + t, g any of the 48 signed permutations (reflections allowed in his theorem), t integer.
# Checks: (1) our feature apexes = the 192 apexes of his exact solid file r44_solid.json; (2) 2388 touching poses; (3) legal = 44;
# (4) the legal ones are all proper rotations (his theorem: every tiling homochiral); (5) negative control: with one coefficient's sign
# flipped, the legal count must change.
# usage: census.py <native_panels.csv> <r44_solid.json>
import sys, csv, json, itertools
from fractions import Fraction as Q
rows = list(csv.DictReader(open(sys.argv[1])))
OFF = [(Q(-1, 8), Q(-1, 4)), (Q(-1, 8), Q(1, 4)), (Q(1, 8), Q(-1, 4)), (Q(1, 8), Q(1, 4)),
       (Q(-1, 4), Q(-1, 8)), (Q(-1, 4), Q(1, 8)), (Q(1, 4), Q(-1, 8)), (Q(1, 4), Q(1, 8))]
def panels(flip=None):
    out = []
    for r in rows:
        k, s = int(r['normal_axis']), int(r['outward_sign']); C = tuple(Q(r[f'center_{c}']) for c in 'xyz')
        ax = [i for i in range(3) if i != k]; feats = {}
        for j, (u, v) in enumerate(OFF):
            p = list(C); p[ax[0]] += u; p[ax[1]] += v
            a = int(r[f'a_{j}'])
            if flip == (int(r['panel']), j): a = -a
            feats[tuple(p)] = a
        out.append(dict(k=k, s=s, C=C, feats=feats))
    return out
PAN = panels()
# (1) apexes against his exact solid
sol = json.load(open(sys.argv[2])); apex_his = {tuple(Q(x) for x in p['apex']) for p in sol['patches']}
apex_ours = set()
for P in PAN:
    for p, a in P['feats'].items():
        q = list(p); q[P['k']] += Q(a * P['s'], 10000); apex_ours.add(tuple(q))
print(f'(1) feature apexes: ours {len(apex_ours)}, his solid file {len(apex_his)}, identical: {apex_ours == apex_his}')
G = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
def act(g, x): p, s = g; return tuple(s[i] * x[p[i]] for i in range(3))
def det(g):
    p, s = g; sg = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if p[i] > p[j]: sg = -sg
    return sg * s[0] * s[1] * s[2]
CELLS = [a for a in itertools.product((0, 1), repeat=3) if a != (1, 1, 1)]
def cells(g, t):                       # lower corners of the unit cells of the posed chair: image of cell a is the cube g(a+[0,1]^3)+t
    out = set()
    for a in CELLS:
        corners = [act(g, tuple(a[i] + e[i] for i in range(3))) for e in itertools.product((0, 1), repeat=3)]
        out.add(tuple(min(c[i] for c in corners) + t[i] for i in range(3)))
    return out
base = set(CELLS)
TOUCH = []
for g in G:
    for t in itertools.product(range(-4, 6), repeat=3):          # wide box (lesson of 12 Nov: -3..3 missed 486 poses)
        B = cells(g, t)
        if B & base: continue
        if any(tuple(c[i] + (d if i == k else 0) for i in range(3)) in B for c in base for k in range(3) for d in (1, -1)): TOUCH.append((g, t))
assert all(-4 < x < 5 for g, t in TOUCH for x in t), 'GUARD: a touching pose on the edge of the search box: widen it'   # once-only guard (12 Nov)
print(f'(2) touching lattice poses: {len(TOUCH)} (paper 2388)')
def legal(g, t, PANS):
    """every face-to-face panel pair: features coincide in position and their coefficients cancel (bump meets dent of equal size)"""
    A = {(P['C'], P['k']): P for P in PANS}
    shared = 0
    for P in PANS:                     # B's panels mapped into the world
        Cw = tuple(a + b for a, b in zip(act(g, P['C']), t))
        kw = next(i for i in range(3) if act(g, tuple(1 if j == P['k'] else 0 for j in range(3)))[i] != 0)
        Pa = A.get((Cw, kw))
        if Pa is None: continue
        nw = act(g, tuple(P['s'] if j == P['k'] else 0 for j in range(3)))[kw]
        if nw != -Pa['s']: continue    # same plane, same side: cannot happen for interior-disjoint tiles; skip defensively
        shared += 1
        fw = {tuple(a + b for a, b in zip(act(g, p), t)): a_ for p, a_ in P['feats'].items()}
        if set(fw) != set(Pa['feats']): return False, shared
        if any(Pa['feats'][p] + fw[p] != 0 for p in fw): return False, shared
    return True, shared
L = [(g, t) for g, t in TOUCH if legal(g, t, PAN)[0]]
print(f'(3) legal contacts: {len(L)} (paper 44); (4) all proper rotations: {all(det(g) == 1 for g, t in L)}')
P2 = panels(flip=(13, 0)); L2 = [(g, t) for g, t in TOUCH if legal(g, t, P2)[0]]
print(f'(5) control, panel 13 feature 0 sign flipped: legal {len(L2)} (must differ from {len(L)})')
ok = apex_ours == apex_his and len(TOUCH) == 2388 and len(L) == 44 and all(det(g) == 1 for g, t in L) and len(L2) != len(L)
print('FINAL ok' if ok else 'FINAL FAIL')
