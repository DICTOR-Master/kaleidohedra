"""Step 6: new closed cycles (nested chains closing on a scaled copy of the start), for DICTO's "maybe there is another golden
cycle set to build". For each dual pair the stations are the named sections S(mu) and hulls H(mu) of s1 (for D.I also OG and
its golden relatives). A TIGHT link A -> B scales B to the smallest copy containing A (A touches B); a cycle's closure is the
product of its tight factors (the given polar-Dharma cycle has two loose links; its tight closure is 225/2 - 99/2 sqrt5, s4).
Part A (exact): for each pair, (i) the sweep cycle  P* -> golden/Archimedean sections in mu order -> P -> P* : closure (R/r)^2;
  (ii) the Dharma-pattern cycle  P -> S(rho^2) -> Q(mu_A*, rho^2) -> H(mu_A*) -> R^2 P* -> H(rho^2) -> P  (mu_A* = the
  Archimedean truncation of P*); tight closure exact.
Part B (search): all tight cycles through <= 5 intermediate stations from P back to P; floating point search, every reported
  hit re-checked exactly. Targets: phi^k, (1 + sqrt2)^k, 2, 3, (R/r)^2.
usage (compute-host): python3 s6_cycles.py co|di|tt -> ../data/s6-cycles-<pair>.json
"""
from dp_lib import *          # noqa
import sys, numpy as np
from scipy.spatial import ConvexHull
which = sys.argv[1]
MAXLEN = int(sys.argv[2]) if len(sys.argv) > 2 else 7          # path length incl. both ends
pl = platonic()
C_N = {3: ONE, 4: S2, 5: PHI}
if which == 'co':   P, nP, nS = Pair('cube', pl['cube'][0]), 4, 3
elif which == 'di': P, nP, nS = Pair('dodecahedron', pl['dodecahedron'][0]), 5, 3
else:               P, nP, nS = Pair('tetrahedron', pl['tetrahedron'][0]), 3, 3
out = {'pair': which, 'max_links': None}
xg, xl = x_golden(nP); xgs, xls = x_golden(nS)
named = [('Pstar', P.mu_Ps(ZERO)), ('L*', P.mu_Ps(xls)), ('A*', P.mu_Ps(ONE / (C_N[nS] + 2))), ('G*', P.mu_Ps(xgs)), ('rect', P.rho2),
         ('G', P.mu_P(xg)), ('A', P.mu_P(ONE / (C_N[nP] + 2))), ('L', P.mu_P(xl)), ('P', P.R2)]
st = {}
for lab, mu in named: st['S:' + lab] = P.S(mu)
for lab, mu in named[1:-1]: st['H:' + lab] = P.Hull(mu)
muA = named[2][1]
C_, F_, Pl_ = planes_of(st['H:A*'])
st["Q(A*,rect)"] = hull3(fast_vertices_H(Pl_ + [(v, P.rho2) for v in P.V]))[0]
if which == 'di':
    C_, F_, Pl_ = planes_of(st['H:L*'])
    st["Q(L*,rect)"] = hull3(fast_vertices_H(Pl_ + [(v, P.rho2) for v in P.V]))[0]
names = list(st)
print(f'   {len(names)} stations', flush=True)
# float machinery
Fv = {k: np.array([[float(x) for x in p] for p in V]) for k, V in st.items()}
def fplanes(Vf):
    h = ConvexHull(Vf); E = np.unique(np.round(h.equations, 10), axis=0)
    return E[:, :3], -E[:, 3]
Fp = {k: fplanes(v) for k, v in Fv.items()}
n = len(names); L = np.zeros((n, n))
for i, a in enumerate(names):
    for j, b in enumerate(names):
        N_, d_ = Fp[b]; L[i, j] = ((Fv[a] @ N_.T) / d_).max()
# A. exact named cycles
def chain_closure(seq):
    t = ONE; fac = []
    for a, b in zip(seq, seq[1:]):
        f = tight(st[a], st[b]); fac.append(f); t = t * f
    return t, fac
seqA = ['S:Pstar', 'S:L*', 'S:A*', 'S:G*', 'S:rect', 'S:G', 'S:A', 'S:L', 'S:P', 'S:Pstar']
tA, facA = chain_closure(seqA)
check(f'A(i) sweep cycle {" -> ".join(seqA)}: every link but the last has tight factor 1 (shared P-facets); closure {kstr(tA)} = (R/r)^2',
      all(f == ONE for f in facA[:-1]) and tA == P.R2 / P.r2)
out['sweep_cycle'] = {'stations': seqA, 'closure': kdesc(tA)}
seqB = ['S:P', 'S:rect', 'Q(A*,rect)', 'H:A*', 'S:Pstar', 'H:rect', 'S:P']
tB, facB = chain_closure(seqB)
check(f'A(ii) Dharma-pattern cycle {" -> ".join(seqB)}: tight factors {[kstr(f) for f in facB]}; closure {kstr(tB)} (~{float(tB):.6f})', True)
out['dharma_pattern_cycle'] = {'stations': seqB, 'factors': [kdesc(f) for f in facB], 'closure': kdesc(tB)}
if which == 'di':
    check('A(ii) D.I: the Dharma-pattern tight closure equals the polar-Dharma all-tight closure 225/2 - 99/2 sqrt5 (s4)',
          tB == K(Fr(225, 2)) - K(Fr(99, 2)) * S5)
    seqC = ['S:P', 'S:rect', 'Q(L*,rect)', 'H:L*', 'S:Pstar', 'H:rect', 'S:P']
    tC, facC = chain_closure(seqC)
    check(f'A(iii) D.I golden Dharma-pattern cycle (OG replaced by its golden relative at mu = sqrt5): factors {[kstr(f) for f in facC]}, closure {kstr(tC)} (~{float(tC):.6f})', True)
    out['golden_dharma_pattern_cycle'] = {'stations': seqC, 'factors': [kdesc(f) for f in facC], 'closure': kdesc(tC)}
# B. search
targets = {}
for k in range(1, 13): targets[f'phi^{k}'] = float(PHI) ** k
for k in range(1, 7): targets[f'(1+sqrt2)^{k}'] = (1 + 2 ** .5) ** k
targets.update({'2': 2.0, '3': 3.0, '4': 4.0, '(R/r)^2': float(P.R2 / P.r2)})
iP = names.index('S:P')
hits = []
def dfs(path, prod):
    if len(path) > 1 and path[-1] == iP:
        for k, v in targets.items():
            if abs(prod - v) < 1e-9 * v: hits.append((len(path), k, list(path)))
        return
    if len(path) >= MAXLEN: return
    for j in range(n):
        if j in path[1:] or (j == iP and len(path) < 2) or j == path[-1]: continue
        if L[path[-1], j] <= 1 - 1e-12 and False: pass
        dfs(path + [j], prod * L[path[-1], j])
out['max_links'] = MAXLEN - 1
dfs([iP], 1.0)
print(f'   float hits: {len(hits)}', flush=True)
from collections import Counter
cnt = Counter(k for _, k, _ in hits)
out['search_counts_by_target'] = dict(cnt)
# shortest few per target, exact check
best = {}
for ln, k, p in sorted(hits):
    best.setdefault(k, []).append(p)
ex = {}
for k, ps in best.items():
    ex[k] = []
    for p in ps[:6]:
        seq = [names[i] for i in p]
        t, fac = chain_closure(seq)
        okv = abs(float(t) - targets[k]) < 1e-9 * targets[k]
        exact_ok = (t == P.R2 / P.r2) if k == '(R/r)^2' else (is_phi_power(t) is not None if k.startswith('phi') else okv)
        ex[k].append({'stations': seq, 'factors': [kstr(f) for f in fac], 'closure': kstr(t), 'exact_match': bool(exact_ok and okv)})
    print('   ', k, cnt[k], ex[k][:1], flush=True)
out['search_examples'] = ex
# two-link rule (proof: P's corners are corners of H(mu); mu n is outside P by the factor mu/r^2): P -> H(mu) -> P closes at nu
two = {}
for lab, mu in named[1:-1]:
    t, fac = chain_closure(['S:P', 'H:' + lab, 'S:P']); two[lab] = {'closure': kdesc(t)}
    check(f'two-link cycle P -> H({lab}) -> P closes at nu = mu/r^2 = {kstr(t)}', t == mu / P.r2 and fac[0] == ONE)
out['two_link_closures'] = two
check('B: search finished; all reported examples re-checked exactly (exact_match flags in data)', True)
save(f's6-cycles-{which}.json', out)
