"""Item 6 (part 3): looking for a short, human-checkable lower bound.
(1) LP relaxation (fractional cover) and its dual.
(2) Packing bound: largest set of pentagons no two of which are covered by a
    common copy (any cover needs at least that many copies).
(3) Local double counting: for a family of pentagon sets U (all images of
    one U under the symmetry group), r = fewest copies covering U, t = the
    most members of the family that one copy meets.  Then any cover has at
    least ceil(N r / t) copies (count pairs (copy in cover, U it meets)).
"""
import json, itertools, collections
from common import *
from ortools.sat.python import cp_model
import highspy

L = Log('logs/s9_lowerbound.log')
B = load_base()
P, Q, cells, pent, edges = B['P'], B['Q'], B['cells'], B['pent'], B['edges']
inst = json.load(open('data/dual_cover_instance.json'))

# families of pentagon sets
fams = {}
# pentagons of each dodecahedral cell of Q = P0 edges at a P0 corner
fams['cell (12 pentagons of a dodecahedron)'] = [[k for k, (a, b) in enumerate(edges) if v in (a, b)] for v in range(120)]
# pentagons at a corner of Q = edges of a P0 cell (6)
ek = {tuple(e): k for k, e in enumerate(edges.tolist())}
fams['corner of Q (6 pentagons)'] = [[ek[tuple(sorted(p))] for p in itertools.combinations(c, 2)] for c in cells]
# pentagons round an edge of Q = edges of a P0 triangle (3)
fams['edge of Q (3 pentagons)'] = [[ek[tuple(sorted(p))] for p in itertools.combinations(t, 2)] for t in B['tris']]
# pentagons on a mirror (12)
mk = {}
for k, (a, b) in enumerate(edges):
    mk.setdefault(canon_dir(P[a] - P[b]), []).append(k)
fams['mirror (12 pentagons)'] = list(mk.values())

def mincover(U, sets):
    """fewest sets covering U: exact small ILP (HiGHS)."""
    U = sorted(U)
    rel = [c for c, s in enumerate(sets) if s & set(U)]
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('mip_rel_gap', 0.0)
    m = len(rel)
    for _ in rel:
        h.addVar(0.0, 1.0)
    h.changeColsIntegrality(m, np.arange(m, dtype=np.int32), np.array([highspy.HighsVarType.kInteger] * m))
    h.changeColsCost(m, np.arange(m, dtype=np.int32), np.ones(m))
    for p in U:
        idx = [i for i, c in enumerate(rel) if p in sets[c]]
        h.addRow(1.0, highspy.kHighsInf, len(idx), np.array(idx, dtype=np.int32), np.ones(len(idx)))
    h.run()
    assert h.modelStatusToString(h.getModelStatus()) == 'Optimal'
    return int(round(h.getInfo().objective_function_value))

for fam in ['A', 'B', 'C3']:
    sets = [set(s) for s in inst[fam]['sets']]
    n = len(sets)
    cov = [[c for c in range(n) if p in sets[c]] for p in range(720)]
    # (1) LP
    h = highspy.Highs(); h.setOptionValue('output_flag', False)
    for c in range(n):
        h.addVar(0.0, 1.0)
    h.changeColsCost(n, np.arange(n, dtype=np.int32), np.ones(n))
    for p in range(720):
        h.addRow(1.0, highspy.kHighsInf, len(cov[p]), np.array(cov[p], dtype=np.int32), np.ones(len(cov[p])))
    h.run()
    L(f'{fam}*: LP relaxation optimum {h.getInfo().objective_function_value:.6f} '
      f'(uniform x = 1/{len(cov[0])} and uniform dual weight 1/60 give 720/60 = 12 exactly)')
    # (2) packing
    m = cp_model.CpModel()
    y = [m.NewBoolVar('') for _ in range(720)]
    for s in sets:
        m.Add(sum(y[p] for p in s) <= 1)
    m.Maximize(sum(y))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 60; sv.parameters.num_workers = 24
    st = sv.Solve(m)
    L(f'{fam}*: packing bound (pentagons pairwise never covered by one copy): {sv.ObjectiveValue():.0f} '
      f'({sv.StatusName(st)}, upper bound {sv.BestObjectiveBound():.0f})')
    # (3) double counting
    best = 0
    for name, U_list in fams.items():
        r = sorted({mincover(U, sets) for U in U_list})
        meets = [sum(1 for U in U_list if set(U) & s) for s in sets]
        t = max(meets)
        mm = max(len(set(U) & s) for U in U_list for s in sets)
        L(f'    most pentagons of one member covered by one copy: {mm} -> each member needs >= ceil({len(U_list[0])}/{mm}) = {-(-len(U_list[0]) // mm)} copies')
        bound = -(-len(U_list) * min(r) // t)
        best = max(best, bound)
        L(f'{fam}*: family "{name}": N = {len(U_list)}, fewest copies covering one member r = {r}, '
          f'members met by one copy t = {sorted(set(meets))} -> bound ceil(N r / t) = {bound}')
    L(f'{fam}*: best simple bound found: {max(best, 12)} (claimed optimum {16 if fam != "C3" else 22})')
L.final()
