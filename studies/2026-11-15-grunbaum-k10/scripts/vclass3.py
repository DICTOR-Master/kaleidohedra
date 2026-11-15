#!/usr/bin/env python3
"""Third filter on the zone-word survivors of vclass2 (class C(n), face-to-face lattice tiling), n = 5 (control) and n = 6.
(1) one vector per pair: zones a and c must realise the SAME lambda_ac (a joint choice over all zones; backtracking);
(2) the 15 (10) chosen lambdas span rank 3; Lambda = their Z-span;
(3) sign coherence (P a union of golden rhombohedra): in the torus R^3/Lambda the dual surfaces of families i, j, k meet with algebraic
    intersection number p_ijk(B) (B a basis of Lambda in Z^n); every triple point is a cell of type ijk counted with the sign of its
    orientation, and covolume = volume forces N_ijk = |p_ijk(B)| and p_ijk(B) det(e_i,e_j,e_k) >= 0 for all ijk (up to one global
    sign). Tested for the golden axes and for their Galois twin (Double Vision: sqrt5 -> -sqrt5). Survivors: cell counts N_ijk.
Prints PROGRESS and FINAL."""
import sys, json, itertools, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from zsurf import Geo, zsign, int_rank_basis, rank_Q
t0 = time.time()
OUT = sys.argv[1]

# zone words, as in vclass2.py
def norm(v):
    for x in v:
        if x: return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)

def word_table(m):
    """m letters 0..m-1 each twice with opposite signs, cyclic, first letter 0 with sign +; key = tuple of normalised lambda_c"""
    table = {}
    rest = [0] + [x for c in range(1, m) for x in (c, c)]
    perms = set(itertools.permutations(rest))
    for perm in perms:
        word = (0,) + perm
        for signs in itertools.product((1, -1), repeat=m - 1):
            sg = (1,) + signs; seen = set(); w = []
            for c in word:
                s = sg[c] if c not in seen else -sg[c]; seen.add(c); w.append((c, s))
            lam = []
            ok = True
            for c in range(m):
                i, j = [k for k, (x, _) in enumerate(w) if x == c]
                v = [0]*m
                for k in range(i + 1, j): v[w[k][0]] += w[k][1]
                if not any(v): ok = False; break
                lam.append(norm(v))
            if ok: table.setdefault(tuple(lam), w)
    return table


def minor(B, t):
    m = [[B[r][c] for c in t] for r in range(3)]
    return (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]))

def run(n):
    m = n - 1; tab = word_table(m); keys = set(tab)
    geos = {'golden': Geo(n), 'twin': Geo(n, twin=True)}
    cells = 3*(n - 3); total = 3**cells
    allv = [v for v in itertools.product((0, 1, -1), repeat=n) if any(v)]
    st = {'subspaces': total, 'zone_words_ok': 0, 'pair_consistent': 0, 'rank3': 0, 'coherent_golden': 0, 'coherent_twin': 0}
    surv = []
    for idx in range(total):
        d = [(idx // 3**j) % 3 for j in range(cells)]; X = [[(0, 1, -1)[d[r*(n-3) + c]] for c in range(n - 3)] for r in range(3)]
        inV = [v for v in allv if all(v[3 + c] == sum(v[r]*X[r][c] for r in range(3)) for c in range(n - 3))]
        K = {}; ok = True
        for a in range(n):
            others = [b for b in range(n) if b != a]; allowed = []
            for c in others:
                A = sorted(set(norm([v[b] for b in others]) for v in inV if v[a] == 0 and v[c] == 0))
                if not A: ok = False; break
                allowed.append(A)
            if not ok: break
            K[a] = [combo for combo in itertools.product(*allowed) if combo in keys]
            if not K[a]: ok = False; break
        if not ok: continue
        st['zone_words_ok'] += 1
        # global lambda_ac (normalised, global coordinates) from zone a's tuple
        def glob(a, combo, ci):
            others = [b for b in range(n) if b != a]; v = [0]*n
            for b, x in zip(others, combo[ci]): v[b] = x
            return norm(v)
        sols = []
        def bt(a, chosen):
            if len(sols) >= 50: return
            if a == n: sols.append(dict(chosen)); return
            others = [b for b in range(n) if b != a]
            for combo in K[a]:
                good = True; new = {}
                for ci, c in enumerate(others):
                    key = (min(a, c), max(a, c)); g = glob(a, combo, ci)
                    if key in chosen and chosen[key] != g: good = False; break
                    new[key] = g
                if good:
                    added = {k: v for k, v in new.items() if k not in chosen}
                    chosen.update(added); bt(a + 1, chosen)
                    for k in added: del chosen[k]
        bt(0, {})
        if not sols: continue
        st['pair_consistent'] += 1
        for sol in sols:
            rows = [list(v) for v in sol.values()]
            if rank_Q(rows) != 3: continue
            st['rank3'] += 1
            B = int_rank_basis(rows)
            P = {t: minor(B, t) for t in itertools.combinations(range(n), 3)}
            rec = {'X': X, 'lambdas': {f'{k[0]}{k[1]}': v for k, v in sol.items()}, 'basis': B}
            for name, G in geos.items():
                sg = set(zsign(G.D[t])*(1 if P[t] > 0 else -1) for t in P if P[t])
                coh = len(sg) == 1
                rec[name] = coh
                if coh:
                    st['coherent_' + name] += 1
                    rec[name + '_cells'] = {''.join(map(str, t)): abs(P[t]) for t in P if P[t]}
            if rec['golden'] or rec['twin']: surv.append(rec)
        if idx % max(1, total//20) == 0: print(f'PROGRESS {idx/total:.3f} n={n} {st} t={time.time()-t0:.0f}s', flush=True)
    return {'n': n, 'stats': st, 'survivors': surv[:300], 'n_survivors': len(surv)}

res = {n: run(n) for n in (5, 6)}
for n, r in res.items(): print(f'n={n}: {r["stats"]} coherent survivors {r["n_survivors"]}')
D1 = sorted([(1, 0, 0, -1, 1), (0, -1, 0, 0, 1), (0, 0, 1, 1, 0)])
def same_lattice(B1, B2):
    return rank_Q([list(r) for r in B1] + [list(r) for r in B2]) == 3
ctrl = any(s['golden'] and same_lattice(s['basis'], D1) for s in res[5]['survivors'])
print('CONTROL D1/D2 lattice among n=5 golden-coherent survivors:', ctrl)
json.dump({str(k): v for k, v in res.items()}, open(OUT, 'w'), indent=0)
print('RESULT', {n: r['n_survivors'] for n, r in res.items()}, f'| {time.time()-t0:.0f}s')
print('FINAL ok' if ctrl else 'FINAL FAIL: D1/D2 control not met')
