# Splash Rules II driver (DICTO 2026-10-31): every perovskite polytype up to period 12 + a random-stacking sample.
# For each per-formula-unit quantity: exact straight line in h?  in (h, p_hh)?  else the smallest window m of layer types
# whose block frequencies fit it exactly. Also: per-site locality (smallest window that fixes each site's value) and the
# Swap Rule F(c,h) + F(h,c) = F(c,c) + F(h,h) for per-gap quantities fixed by the gap's two layers.
# Exact rational arithmetic throughout (fractions.Fraction); no floats in any test.
# Usage (dicto-big-brother): python3 splash.py <outdir>
import sys, os, json, itertools, random
from fractions import Fraction as Fr
from collections import Counter, defaultdict
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from perov import analyse

MAXN = 12
def bracelets(maxn):
    seen, out = set(), []
    for n in range(1, maxn + 1):
        for w in itertools.product('ch', repeat=n):
            w = ''.join(w)
            if any(n % p == 0 and w == w[:p] * (n // p) for p in range(1, n)): continue     # primitive only
            rots = [w[i:] + w[:i] for i in range(n)]; r = w[::-1]; rots += [r[i:] + r[:i] for i in range(n)]
            key = min(rots)
            if key in seen: continue
            seen.add(key); out.append(key)
    return out

def randoms(seed=20261031):
    rng = random.Random(seed); out = []
    for a in (Fr(1, 10), Fr(3, 10), Fr(1, 2), Fr(7, 10), Fr(9, 10)):          # P(h | previous h)
        for b in (Fr(1, 10), Fr(3, 10), Fr(1, 2), Fr(7, 10), Fr(9, 10)):      # P(h | previous c)
            for rep in range(2):
                w = ['c']
                while len(w) < 48: w.append('h' if rng.random() < float(a if w[-1] == 'h' else b) else 'c')
                w = ''.join(w)
                if 'c' not in w or 'h' not in w: continue
                out.append(('rand', str(a), str(b), w))
    return out

KNOWN = [  # name, c/h word, example compound(s), source of the sequence
    ('3C', 'c', 'SrTiO3, BaTiO3 (cubic), BaRuO3 at 18 GPa', 'Jin et al. PNAS 105, 7115 (2008); Cava et al. arXiv 2006.05864'),
    ('2H', 'h', 'BaNiO3, BaCoO3, 2H-BaMnO3', 'Cava et al. arXiv 2006.05864 (2H = hh, chains of face-sharing octahedra)'),
    ('4H', 'hc', '4H-BaRuO3 (3 GPa), SrMnO3, 4H-BaMnO2.59', 'Jin et al. 2008 (CFCF); Cava et al. ((ch)2)'),
    ('6H', 'hcc', 'hexagonal BaTiO3, 6H-BaRuO3 (5 GPa), Ba3MRu2O9', 'Jin et al. 2008 (FCC); Cava et al. ((chc)2 = (hcc)2)'),
    ('9R', 'hhc', 'BaRuO3 (ambient), Ba3MnRu2O9', 'Jin et al. 2008 (CFF); Cava et al. ((chh)3)'),
    ('8H', 'hhhc', '8H-BaMnO3-x', 'Adkin and Hayward, Chem. Mater. 19, 755 (2007) (polytype); sequence from Ramsdell 8H + Cava et al. (8H strings share corners)'),
    ('10H', 'hhhcc', '10H-BaMnO3-x, 10H-Ba5Sb1-xMn4+xO15', 'Cava et al. ((chhhc)2, tetramers); Adkin and Hayward 2007'),
    ("10H'", 'hhchc', '10H-Ba5Fe4NiO13.5', 'Cava et al. (trimers corner-sharing with dimers)'),
    ('12R', 'hhcc', '12R-Ba4Fe3NiO12, 12R-Ba4Ni2Ir2O12', 'Cava et al. (12R trimers bridged by single octahedra)'),
    ('15R', 'hhhhc', '15R-BaMnO3-x', 'Adkin and Hayward 2007 (polytype); sequence from Ramsdell 15R + strings sharing corners'),
    ('5H', 'hhccc', '5H-Ba5Ta4O15 (one B in five vacant)', 'Cava et al. (5H strings bridged by single octahedra)'),
]

def run(w): return json.loads(json.dumps(analyse(w)))   # string keys, as in the saved data

def blocks(T, m):
    n = len(T); c = Counter(''.join(T[(k + i) % n] for i in range(m)) for k in range(n))
    return {b: Fr(c[b], n) for b in (''.join(x) for x in itertools.product('ch', repeat=m))}

def per_word(r):
    T = r['types']; N = r['N']; Q = {}
    fB = Counter(); shells = Counter(); An = Counter(); faces = Fr(0); corners = Fr(0); edges = Fr(0)
    for b in r['perB']:
        f = b['share'].get('3', 0); faces += f; corners += b['share'].get('1', 0); edges += b['share'].get('2', 0)
        fB[f] += 1
        for k_, v in b['shells'].items(): shells[int(k_)] += v
        for k_, v in b['A'].items(): An[int(k_)] += v
    Q['face partners per B'] = faces / N; Q['corner partners per B'] = corners / N; Q['edge partners per B'] = edges / N
    for f in (0, 1, 2): Q[f'B with {f} shared faces'] = Fr(fB[f], N)
    for r2 in sorted(set(list(shells)) | ALLR2):
        Q[f'B-B at r2={Fr(r2, 72)}'] = Fr(shells[r2], N)
    Q['A neighbours per B (r2=3/2)'] = Fr(An[108], N)
    nX = len(r['perX']); Q['face X (cos BXB = 1/3) share'] = Fr(sum(1 for x in r['perX'] if x['cosBXB'] == '1/3'), nX)
    Q['corner X (cos BXB = -1) share'] = Fr(sum(1 for x in r['perX'] if x['cosBXB'] == '-1'), nX)
    Q['A per X'] = Fr(sum(x['nA'] for x in r['perX']), nX)
    Q['cuboctahedral A share'] = Fr(sum(1 for a in r['perA'] if a['cage'] == 'cubo'), len(r['perA']))
    Q['empty octahedral holes per gap'] = Fr(len(r['octE']), N)
    Q['  of them A trans (r2=2) in both triangles'] = Fr(sum(1 for e in r['octE'] if e[1] == [1, 1] and e[2] == [144]), N)
    Q['tetrahedral holes per gap, X apex + 1 A in base'] = Fr(sum(1 for t in r['tet'] if t[2] == 'X' and t[3] == 1), N)
    Q['tetrahedral holes per gap, A apex + 0 A in base'] = Fr(sum(1 for t in r['tet'] if t[2] == 'A' and t[3] == 0), N)
    cl = r['clusters']
    if cl is None: cl = []                                                     # 2H: one endless chain, no finite cluster
    Q['face-sharing clusters per B (incl. single octahedra)'] = Fr(len(cl), N)
    Q['strings (2 or more octahedra) per B'] = Fr(sum(1 for x in cl if x >= 2), N)
    for L in range(1, 6): Q[f'clusters of {L} octahedra per B'] = Fr(sum(1 for x in cl if x == L), N)
    Q['octahedra in strings of 4 or more, share'] = Fr(sum(x for x in cl if x >= 4), N) if cl else Fr(1)
    return Q

ALLR2 = set()


def solve_exact(A, y):
    """least-squares-free exact solve: returns x with A x = y if consistent (any solution), else None. A rows of Fractions."""
    m = len(A); n = len(A[0]); M = [list(A[i]) + [y[i]] for i in range(m)]
    piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, m) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; inv = 1 / M[r][c]; M[r] = [v * inv for v in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == m: break
    for i in range(r, m):
        if M[i][n] != 0: return None
    x = [Fr(0)] * n
    for i, c in enumerate(piv): x[c] = M[i][n]
    return x

if __name__ == '__main__':
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True)
    W = bracelets(MAXN); RW = randoms()
    allw = W + [x[3] for x in RW]
    with Pool(22) as pool: res = pool.map(run, allw, chunksize=4)
    for r in res:
        for b in r['perB']: ALLR2.update(int(k) for k in b['shells'])
    words = []
    for w, r in zip(allw, res):
        T = r['types']; n = len(w)
        st = dict(h=Fr(w.count('h'), n), p_hh=blocks(w, 2)['hh'], p_hhh=blocks(w, 3)['hhh'], p_hch=blocks(w, 3)['hch'])
        words.append(dict(word=w, N=r['N'], letters=r['letters'], stats=st, Q=per_word(r), random=len(w) == 48 and w in [x[3] for x in RW]))
    keys = list(words[0]['Q'].keys())
    # ---- splash fits on all words (bracelets up to 12 + random) ----
    fits = {}
    for key in keys:
        y = [wd['Q'][key] for wd in words]
        res1 = solve_exact([[Fr(1), wd['stats']['h']] for wd in words], y)
        res2 = solve_exact([[Fr(1), wd['stats']['h'], wd['stats']['p_hh']] for wd in words], y)
        mmin = None
        for m in range(1, 8):
            bl = [blocks(wd['word'], m) for wd in words]; names = sorted(bl[0])
            if solve_exact([[b[nm] for nm in names] for b in bl], y) is not None: mmin = m; break
        if res1 is not None: fits[key] = dict(kind='line in h', a=str(res1[0]), b=str(res1[1]), m=mmin)
        elif res2 is not None: fits[key] = dict(kind='line in (h, p_hh)', a=str(res2[0]), b=str(res2[1]), c=str(res2[2]), m=mmin)
        else: fits[key] = dict(kind=f'needs window m = {mmin}' if mmin else 'no finite window <= 7', m=mmin)
    # ---- per-site locality and Swap Rule for per-B quantities ----
    loc = defaultdict(dict)
    for w, r in zip(allw, res):
        T = r['types']; N = r['N']
        for b in r['perB']:
            k = b['k']
            vals = {'face partners': b['share'].get('3', 0), 'corner partners': b['share'].get('1', 0), 'A neighbours': b['A'].get('108', 0)}
            for f in (0, 1, 2): vals[f'B with {f} shared faces'] = int(b['share'].get('3', 0) == f)
            for r2 in sorted(ALLR2): vals[f'B-B at r2={Fr(r2, 72)}'] = b['shells'].get(str(r2), 0)
            for name, v in vals.items():
                for j in range(1, 7):
                    win = ''.join(T[(k - j + 1 + i) % N] for i in range(2 * j))
                    loc[(name, j)].setdefault(win, set()).add(v)
    locality = {}; swap = {}
    names = sorted(set(nm for nm, _ in loc))
    for nm in names:
        jmin = next((j for j in range(1, 7) if all(len(s) == 1 for s in loc[(nm, j)].values())), None)
        locality[nm] = jmin
        if jmin == 1:
            F = {win: next(iter(s)) for win, s in loc[(nm, 1)].items()}
            if len(F) == 4: swap[nm] = dict(F={k_: F[k_] for k_ in ('cc', 'ch', 'hc', 'hh')}, holds=F['ch'] + F['hc'] == F['cc'] + F['hh'])
    # ---- known polytypes table ----
    canon = {wd['word']: wd for wd in words}
    def canon_of(w):
        n = len(w); rots = [w[i:] + w[:i] for i in range(n)]; r = w[::-1]; rots += [r[i:] + r[:i] for i in range(n)]; return min(rots)
    known = []
    for name, w, comp, src in KNOWN:
        wd = canon[canon_of(w)]
        known.append(dict(name=name, word=w, compounds=comp, source=src, N=wd['N'], letters=wd['letters'],
                          stats={k_: str(v) for k_, v in wd['stats'].items()}, Q={k_: str(v) for k_, v in wd['Q'].items()}))
    out = dict(n_words=len(W), n_random=len(RW), keys=keys, fits=fits, locality=locality, swap=swap, known=known,
               words=[dict(word=wd['word'], N=wd['N'], random=wd['random'], stats={k_: str(v) for k_, v in wd['stats'].items()},
                           Q={k_: str(v) for k_, v in wd['Q'].items()}) for wd in words])
    json.dump(out, open(os.path.join(outdir, 'splash2_perovskite.json'), 'w'), indent=1)
    print('words', len(W), 'random', len(RW))
    for k_ in keys: print(f'{k_:55s}', fits[k_])
    print('locality (half-window j: layers k-j+1..k+j around gap k):'); [print('  ', nm, locality[nm]) for nm in names]
    print('swap:'); [print('  ', nm, v) for nm, v in swap.items()]
