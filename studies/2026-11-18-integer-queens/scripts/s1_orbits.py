#!/usr/bin/env python3
"""Integer Queens, part 1: orbit splits and hidden symmetry (18 Nov 2026).
E8 in sum-zero R^9, scaled by 3: E8 = {y in Z^9 : sum 0, all y_i congruent mod 3} = A8 u (A8+[3]) u (A8+[6]).
E7 in sum-zero R^8, scaled by 4: E7 = {y : sum 0, all y_i = 0 mod 4 or all = 2 mod 4} = A7 u (A7+[4]);
E7* = {y : sum 0, all y_i congruent mod 4}.  (Glue construction: Conway-Sloane, SPLAG ch. 4.)
Shells: E8 norm 2 (240, 4_21), norm 4 (2160, 2_41); E7 norm 2 (126, 2_31); E7* norm 3/2 (56, 3_21).
For every finite set X: all reflections of X are found exactly (a reflection of X maps some x to some y != x, so its root
is parallel to x - y; one difference line per S-class is tested, since S is in the group).
Usage: s1_orbits.py out.json"""
import sys, os, json, time, math, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
from fractions import Fraction as Fr
from sympy.combinatorics import Permutation, PermutationGroup
OUT = sys.argv[1]; C = Checks(); t0 = time.time(); out = {}
WE = {7: 2903040, 8: 696729600}

def rings(seed):
    gaps = [seed[k] - seed[k+1] for k in range(len(seed) - 1)]
    return [k for k, g in enumerate(gaps) if g > 0], gaps

def name(seed, n, scale):
    vals = sorted(set(seed), reverse=True); rg, gaps = rings(seed)
    t = 't_{' + ','.join(str(k) for k in rg) + '}{3^' + str(n - 1) + '}'
    uni = len({gaps[k] for k in rg}) == 1
    if len(vals) == 2:
        k = seed.count(vals[0])
        pre = {1: '', 2: 'rectified ', 3: 'birectified ', 4: 'trirectified '}[min(k, n + 1 - k)]
        return f'hypersimplex Delta({n+1},{k}), centred = {pre}{n}-simplex', t, True
    if rg == [0, n - 1] and uni: return f'expanded {n}-simplex (A{n} root polytope)', t, True
    return ('uniform' if uni else 'non-uniform') + f' {n}-simplex orbit polytope ' + t, t, uni

def frac_seed(seed, scale): return [str(Fr(v, scale)) for v in seed]

def coord_perm_gens(X, idx):
    d = X.shape[1]
    sw = list(range(d)); sw[0], sw[1] = 1, 0
    cy = list(range(1, d)) + [0]
    return [Permutation(as_perm(X, X[:, sw], idx)), Permutation(as_perm(X, X[:, cy], idx))]

def diff_classes(X):
    """S-class representatives of all difference lines x - y (x != y, equal norm) of X; vectorised, exact integers"""
    n2 = (X*X).sum(1); reps = set()
    for i in range(len(X) - 1):
        D = X[i] - X[i+1:][n2[i+1:] == n2[i]]
        if len(D) == 0: continue
        g = np.gcd.reduce(np.abs(D), axis=1); D = D // g[:, None]
        P = -np.sort(-D, axis=1); N = -np.sort(D, axis=1)      # sorted descending of D and of -D
        for p, q in zip(map(tuple, P), map(tuple, N)): reps.add(max(p, q))
    return sorted(reps)

def reflection_lines(Y, cand):
    """exact set of root lines v with s_v(Y) = Y, among the S-classes cand (must contain every difference line of Y)"""
    keys = set(index_of(Y)); good = set()
    for c in cand:
        v = np.array(c, dtype=np.int64); Z = reflect(Y, v)
        if Z is not None and all(z.tobytes() in keys for z in Z):
            for p in orbit(c): good.add(line_key(p))
    return sorted(good)

def central(X):
    keys = set(index_of(X)); return all((-x).tobytes() in keys for x in X)

setups = {
    8: dict(scale=3, shells=[('4_21 (E8 roots)', 18, 3, None), ('2_41', 36, 3, None)], r=np.array([2, 2, 2, -1, -1, -1, -1, -1, -1])),
    7: dict(scale=4, shells=[('2_31 (E7 roots)', 32, 4, (0, 2)), ('3_21', 24, 4, None)], r=np.array([2, 2, 2, 2, -2, -2, -2, -2])),
}
expect = {'4_21 (E8 roots)': 240, '2_41': 2160, '2_31 (E7 roots)': 126, '3_21': 56}
for n, S in setups.items():
    d = n + 1; scale = S['scale']; r = S['r']; out[f'E{n}'] = res = {}
    C(int(r @ r) == 2 * scale**2 and r.sum() == 0, f'E{n}: extra root r = {list(r)}/{scale} has norm 2')
    for sname, N2, q, resid in S['shells']:
        seeds = shell_seeds(d, q, N2)
        if resid: seeds = [s for s in seeds if s[0] % q in resid]
        X = np.concatenate([orbit(s) for s in seeds]); idx = index_of(X)
        C(len(X) == expect[sname], f'E{n} {sname}: shell of norm {Fr(N2, scale**2)} has {len(X)} vectors (expected {expect[sname]})')
        # group
        gens = coord_perm_gens(X, idx); pr = as_perm(X, reflect(X, r), idx)
        C(pr is not None, f'E{n} {sname}: reflection in r maps the shell to itself (exact)')
        Gp = PermutationGroup(gens + [Permutation(pr)]); o = Gp.order()
        st = Gp.stabilizer(0).order(); orb0 = len(Gp.orbit(0))
        C(o == WE[n] and st * orb0 == o and Gp.is_transitive(),
          f'E{n} {sname}: S{d} + s_r generate order {o} (W(E{n}) = {WE[n]}), transitive; stabiliser {st} x orbit {orb0}')
        rows = []
        for s in seeds:
            nm, t, uni = name(s, n, scale)
            rows.append(dict(seed=frac_seed(s, scale), seed_int=list(s), count=n_perms(s), name=nm, rings=t))
            print(f'  {n_perms(s):5d}  {frac_seed(s, scale)}  {nm}')
        res[sname] = dict(total=len(X), group_order=o, orbits=rows)
        # reflections and symmetry order of every union of S-orbits in this shell
        O = [orbit(s) for s in seeds]; uni = []; cand = diff_classes(X)
        for m in range(1, len(O) + 1):
            for sub in itertools.combinations(range(len(O)), m):
                Y = np.concatenate([O[i] for i in sub]); L = reflection_lines(Y, cand)
                cs = central(Y)
                if len(L) == {7: 63, 8: 120}[n]: G = WE[n]; kind = f'W(E{n})'
                elif len(L) == n * (n + 1) // 2: G = math.factorial(d) * (2 if cs else 1); kind = f'S{d}' + (' x {+-1}' if cs else '')
                else: G = None; kind = f'{len(L)} reflections (unexpected)'
                uni.append(dict(orbits=[O[i].shape[0] for i in sub], seeds=[frac_seed(seeds[i], scale) for i in sub],
                                reflections=len(L), centrally_symmetric=cs, group=kind, order=G))
        full = [u for u in uni if len(u['orbits']) == len(O)]
        C(full[0]['order'] == WE[n] and all(u['order'] != WE[n] for u in uni if u is not full[0]) and all(u['order'] for u in uni),
          f'E{n} {sname}: of {len(uni)} unions of S{d}-orbits only the whole shell has W(E{n}) symmetry; every other union has '
          f'exactly the {n*(n+1)//2} reflections of S{d} (exact)')
        for u in uni: print(f"     union {u['orbits']}: {u['reflections']} reflections, |G| = {u['order']} ({u['group']})")
        res[sname]['unions'] = uni

# expected starting points (verify, not assume)
e8 = out['E8']; e7 = out['E7']
C(sorted(o['count'] for o in e8['4_21 (E8 roots)']['orbits']) == [72, 84, 84], '240 = 72 + 84 + 84')
C(sorted(o['count'] for o in e7['2_31 (E7 roots)']['orbits']) == [56, 70], '126 = 56 + 70')
C(sorted(o['count'] for o in e7['3_21']['orbits']) == [28, 28], '56 = 28 + 28')

# must-fail control: A8 roots with the two 84-orbits scaled by 2 (same S9-orbits, not one W(E8)-orbit)
A8r = orbit((3, 0, 0, 0, 0, 0, 0, 0, -3)); D3 = orbit((2, 2, 2, -1, -1, -1, -1, -1, -1))
Y = np.concatenate([A8r, 2*D3, -2*D3]); L = reflection_lines(Y, diff_classes(Y))
C(len(L) == 36, f'control (must fail): A8 roots + 2 x (+-Delta(9,3)) keeps only {len(L)} reflections (S9: 36)')
# cross-shell union: 240 u 2160 is W(E8)-invariant; 240 u (one S9-orbit of 2160) is not
s241 = shell_seeds(9, 3, 36); X240 = np.concatenate([orbit(s) for s in shell_seeds(9, 3, 18)])
k = set(index_of(np.concatenate([X240] + [orbit(s) for s in s241])))
Yall = np.concatenate([X240] + [orbit(s) for s in s241]); Rr = reflect(Yall, setups[8]['r'])
C(all(y.tobytes() in k for y in Rr), 'cross-shell: 4_21 u 2_41 (2400 points) is preserved by s_r')
Y1 = np.concatenate([X240, orbit(s241[0])]); k1 = set(index_of(Y1))
C(not all(y.tobytes() in k1 for y in reflect(Y1, setups[8]['r'])), 'cross-shell (must fail): 4_21 u one S9-orbit of 2_41 is not')

# ---- heptagon link: S7 (first seven coordinates) on the E7 roots ----
X = np.concatenate([orbit(s) for s in shell_seeds(8, 4, 32) if s[0] % 4 in (0, 2)])
cl = {}
for x in X: cl.setdefault((tuple(sorted(x[:7], reverse=True)), int(x[7])), []).append(x)
s7 = sorted([dict(count=len(v), first7=[str(Fr(int(a), 4)) for a in key[0]], last=str(Fr(key[1], 4))) for key, v in cl.items()],
            key=lambda z: -z['count'])
for z in s7: print(f"  S7: {z['count']:3d}  ({', '.join(z['first7'])} | {z['last']})")
C(sum(z['count'] for z in s7) == 126 and sorted(z['count'] for z in s7) == [7, 7, 35, 35, 42],
  f"E7 roots under S7: {sorted(z['count'] for z in s7)} = 42 + 7 + 7 + 35 + 35")
out['E7_S7_split'] = s7
json.dump(out, open(OUT, 'w'), indent=1, default=int)
print(f'time {time.time()-t0:.1f}s'); C.final()
