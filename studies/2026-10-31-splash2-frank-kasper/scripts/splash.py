# Splash Rules II, Frank-Kasper run (DICTO 2026-10-31). Driver: builds every structure, computes the exact census
# (scripts/fk.py), and tests every count for exact straight lines. Run on dicto-big-brother:
#   ~/geom/bin/python splash.py <rawdir with CIFs> <outdir>
# Exact Fractions in every test; floats only inside the Delaunay step of fk.py.
import sys, os, json, itertools, random
from fractions import Fraction as Fr
from collections import Counter
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fk import parse_cif, expand, lattice, analyse, census, skeleton
import sqtri, fk59

# ---------------------------------------------------------------- the physical structures (source of every file) ----
CIFS = [  # name, file, compound, source
    ('A15', 'aflow_A3B_cP8_223_c_a-001.cif', 'Cr3Si', 'AFLOW A3B_cP8_223_c_a-001 (Jauch et al. 1987)'),
    ('C15', 'aflow_A2B_cF24_227_c_b-001.cif', 'MgCu2', 'AFLOW A2B_cF24_227_c_b-001'),
    ('C14', 'aflow_AB2_hP12_194_f_ah-001.cif', 'MgZn2', 'AFLOW AB2_hP12_194_f_ah-001'),
    ('C14 ternary', 'aflow_A3BC2_hP12_194_h_a_f-002.cif', 'U2Cr3Si', 'AFLOW A3BC2_hP12_194_h_a_f-002'),
    ('C36', 'aflow_AB2_hP24_194_ef_fgh-001.cif', 'MgNi2', 'AFLOW AB2_hP24_194_ef_fgh-001'),
    ('9R Laves', 'cod_1522206.cif', 'Mg(Li,Zn)2', 'COD 1522206 (Komura et al.)'),
    ('Laves 9-layer (Ag)', 'cod_2105354.cif', 'Mg9(Zn,Ag)18', 'COD 2105354 (Komura et al.)'),
    ('Laves long period (Ag)', 'cod_2105334.cif', 'Mg(Zn,Ag)2', 'COD 2105334 (Komura et al.)'),
    ('Z', 'aflow_A3B4_hP7_191_f_de-001.cif', 'Zr4Al3', 'AFLOW A3B4_hP7_191_f_de-001'),
    ('sigma', 'aflow_A4B4C4DE2_tP30_136_i_j_i_a_f-001.cif', 'CrFe-type (Cr,Fe,Ni,Pd,Rh)', 'AFLOW A4B4C4DE2_tP30_136_i_j_i_a_f-001'),
    ('sigma (COD)', 'cod_2106167.cif', '(Cr,Fe,Mn,Mo,Ni)30', 'COD 2106167'),
    ('mu', 'aflow_A7B6_hR13_166_ah_3c-001.cif', 'W6Fe7', 'AFLOW A7B6_hR13_166_ah_3c-001'),
    ('delta', 'cod_2310246.cif', 'MoNi', 'COD 2310246 (Shoemaker and Shoemaker 1963)'),
    ('P', 'cod_2311049.cif', 'Mo-Ni-Cr', 'COD 2311049 (Shoemaker, Shoemaker and Wilson 1957)'),
    ('R', 'cod_2310299.cif', 'Mo-Co-Cr', 'COD 2310299 (Komura, Sly and Shoemaker 1960)'),
    ('R (Mn-Si)', 'cod_2107202.cif', 'Mn85.5Si14.5', 'COD 2107202'),
    ('nu', 'cod_2106034.cif', 'Mn81.5Si18.5', 'COD 2106034'),
    ('T (Bergman)', 'aflow_AB32C48_cI162_204_a_2efg_2gh-001.cif', 'Mg32(Al,Zn)49', 'AFLOW AB32C48_cI162_204_a_2efg_2gh-001'),
]
NONFK = [
    ('chi (alpha-Mn)', 'aflow_A_cI58_217_ac2g-001.cif', 'alpha-Mn', 'AFLOW A_cI58_217_ac2g-001'),
    ('Mg17Al12 (alpha-Mn type)', 'cod_1576218.cif', 'Mg17Al12', 'COD 1576218'),
    ('Mg23Al30', 'aflow_A30B23_hR53_148_5f_a2c3f-001.cif', 'Mg23Al30', 'AFLOW A30B23_hR53_148_5f_a2c3f-001'),
    ('Mg21Zn25', 'cod_2013036.cif', 'Mg21Zn25', 'COD 2013036'),
]
# Known structures with counts only (Deza, Delgado Friedrichs and Dutour Sikiric, talk 'Space fullerenes', table of 24/27 known
# FK structures, and their computer search; fractions F20:F24:F26:F28 = Z12:Z14:Z15:Z16). Used for the fraction laws only.
TABLE = [('K', 'complex, Pmmm', (14, 21, 6, 0)), ('F', 'complex, P6/mmm', (9, 13, 4, 0)), ('J', 'complex, Pmmm', (4, 5, 2, 0)),
         ('H', 'complex, Cmmm', (5, 8, 2, 0)), ('K*', 'Mn77Fe4Si19, C2', (25, 19, 4, 7)), ('-* (K7Cs6)', 'K7Cs6, P63/mmc', (7, 2, 2, 2)),
         ('p-sigma', 'Th6Cd7, Pbam', (7, 2, 2, 2)), ('M', 'Nb48Ni39Al13, Pnam', (7, 2, 2, 2)), ('C', 'V2(Co,Si)3, C2/m', (15, 2, 2, 6)),
         ('I', 'V41Ni36Si23, Cc', (11, 2, 2, 4)), ('SM', 'Mg32(Zn,Al)49, Pm-3n', (49, 9, 0, 23)), ('X', 'Mn45Co40Si15, Pnnm', (23, 2, 2, 10)),
         ('Mg4Zn7', 'Mg4Zn7, C2/m', (35, 2, 2, 16)),
         ('hyp. 7422', 'computer search no. 1', (7, 4, 2, 2)), ('hyp. 6640', 'computer search no. 40', (6, 6, 4, 0)),
         ('hyp. 6840', 'computer search nos. 18, 62, 63', (6, 8, 4, 0)),
         ('hyp. 6602', 'computer search, new', (6, 6, 0, 2)), ('hyp. 9223', 'new', (9, 2, 2, 3)), ('hyp. 8522', 'new', (8, 5, 2, 2)),
         ('hyp. 8441', 'new', (8, 4, 4, 1)), ('hyp. 7821', 'new', (7, 8, 2, 1)), ('hyp. 7740', 'new', (7, 7, 4, 0)),
         ('hyp. 11224', 'new', (11, 2, 2, 4)), ('hyp. 11143', 'new', (11, 1, 4, 3)), ('hyp. 61120', 'new', (6, 11, 2, 0)),
         ('hyp. 10604', 'new', (10, 6, 0, 4)), ('hyp. 10523', 'new', (10, 5, 2, 3)), ('hyp. 10442', 'new', (10, 4, 4, 2)),
         ('hyp. 10361', 'new', (10, 3, 6, 1))]

# ---------------------------------------------------------------- the two layered families ----
def canon(w, alphabet_flip=None, rev_flip=False):
    n = len(w); cands = []
    vs = [w]
    if alphabet_flip: vs.append(w.translate(alphabet_flip))
    for v in list(vs):
        r = v[::-1]
        if rev_flip and alphabet_flip: r = r.translate(alphabet_flip)
        vs.append(r)
    for v in vs:
        cands += [v[i:] + v[:i] for i in range(n)]
    return min(cands)

def primitive(w): n = len(w); return not any(n % p == 0 and w == w[:p] * (n // p) for p in range(1, n))

FLIP = str.maketrans('+-', '-+')
def words_fk59(maxn):
    seen = set()
    for n in range(1, maxn + 1):
        for w in itertools.product('0+-', repeat=n):
            w = ''.join(w)
            if not primitive(w): continue
            c = canon(w, FLIP, True)
            if c not in seen: seen.add(c); yield c
def words_st(maxn):
    seen = set()
    for n in range(1, maxn + 1):
        for w in itertools.product('ST', repeat=n):
            w = ''.join(w)
            if not primitive(w): continue
            c = canon(w)
            if c not in seen: seen.add(c); yield c
def random_words(alpha, n, k, seed):
    rng = random.Random(seed); out = []
    for i in range(k):
        p = [rng.random() for _ in alpha]; s = sum(p); p = [x / s for x in p]
        stick = rng.choice([0.0, 0.3, 0.6, 0.85])       # tendency to repeat the last letter: varies pair statistics
        w = [rng.choices(alpha, p)[0]]
        while len(w) < n:
            w.append(w[-1] if rng.random() < stick else rng.choices(alpha, p)[0])
        w = ''.join(w)
        if len(set(w)) > 1 and primitive(w): out.append(w)
    return out

# ---------------------------------------------------------------- workers ----
def jobs(raw):
    J = []
    for name, f, comp, src in CIFS + NONFK:
        J.append(('cif', name, os.path.join(raw, f), comp, src, (name, f, comp, src) in NONFK))
    for w in words_st(7): J.append(('st', w))
    for w in random_words('ST', 20, 30, 20261031): J.append(('st', w))
    for w in words_fk59(6): J.append(('fk59', w))
    for w in random_words('0+-', 14, 40, 20261032): J.append(('fk59', w))
    return J

def work(job):
    kind = job[0]
    if kind == 'cif':
        c = parse_cif(job[2]); frac, lab = expand(c); L = lattice(c['cell']); meta = dict(name=job[1], compound=job[3], source=job[4], nonfk=job[5])
    elif kind == 'st':
        L, frac, ww = sqtri.build(job[1]); meta = dict(name='ST ' + job[1], word=job[1], cellword=ww, units=len(ww))
    else:
        L, frac, ww = fk59.build(job[1]); meta = dict(name='FK59 ' + job[1], word=job[1], cellword=ww, units=len(ww))
    try:
        r = analyse(L, frac)
    except Exception as e:
        return dict(kind=kind, meta=meta, ok=False, msgs=[repr(e)])
    out = dict(kind=kind, meta=meta, ok=r['ok'], msgs=r['msgs'], margin=float(r['margin']), N=r['n'],
               Zcount=dict(Counter(r['Z'].values())))
    if r['ok']:
        out['census'] = dict(census(r)); out['skeleton'] = skeleton(r)
    return out

# ---------------------------------------------------------------- exact fitting ----
def solve_exact(A, y):
    m = len(A); n = len(A[0]); M = [list(map(Fr, A[i])) + [Fr(y[i])] for i in range(m)]
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

def windows(cellword, m, flip=None):
    n = len(cellword); c = Counter()
    for k in range(n):
        v = ''.join(cellword[(k + i) % n] for i in range(m))
        if flip: v = min(v, v.translate(flip), v[::-1].translate(flip), v[::-1])
        else: v = min(v, v[::-1])
        c[v] += 1
    return {k: Fr(v, n) for k, v in c.items()}

def fit_windows(rows, key, flip, maxm=5):
    y = [Fr(r['census'].get(key, 0), r['meta']['units']) for r in rows]
    for m in range(0, maxm + 1):
        if m == 0:
            if len(set(y)) == 1: return 0, {'': y[0]}
            continue
        W = [windows(r['meta']['cellword'], m, flip) for r in rows]
        names = sorted(set().union(*W))
        x = solve_exact([[w.get(nm, 0) for nm in names] for w in W], y)
        if x is not None: return m, {nm: v for nm, v in zip(names, x) if v != 0}
    return None, None

def main(raw, outdir):
    os.makedirs(outdir, exist_ok=True)
    J = jobs(raw)
    with Pool(22) as pool: R = pool.map(work, J, chunksize=1)
    bad = [r for r in R if not r['ok'] and not r['meta'].get('nonfk')]
    print('structures', len(R), 'not TCP (unexpected):', [(r['meta']['name'], r['msgs'][:1]) for r in bad])
    for r in R:
        if r['meta'].get('nonfk'): print('  non-FK check', r['meta']['name'], 'TCP' if r['ok'] else 'not TCP:', r['msgs'][:1])
    FK = [r for r in R if r['ok']]
    keys = sorted(set().union(*[r['census'] for r in FK]))
    # per-atom values, site fractions, YK defect
    for r in FK:
        C = r['census']; N = C['N']
        x = {z: Fr(C[f'N{z}'], N) for z in (12, 14, 15, 16)}
        r['x'] = {str(z): str(v) for z, v in x.items()}
        r['Zbar'] = str(Fr(C['Zsum'], N))
        r['a0'] = str(x[12] - x[14] / 3 - Fr(7, 6) * x[15] - 2 * x[16])
    # ---- global fits across every TCP structure (physical + both families) ----
    def fits_global(rows):
        F = {}
        for key in keys:
            y = [Fr(r['census'].get(key, 0), r['census']['N']) for r in rows]
            X = [{z: Fr(r['census'][f'N{z}'], r['census']['N']) for z in (12, 14, 15, 16)} for r in rows]
            Zb = [Fr(r['census']['Zsum'], r['census']['N']) for r in rows]
            a0 = [Fr(r['a0']) for r in rows]
            res = None
            for name, A in (('constant', [[1] for _ in rows]),
                            ('line in Zbar', [[1, z] for z in Zb]),
                            ('line in x12', [[1, x[12]] for x in X]),
                            ('plane in (x12, a0)', [[1, x[12], a] for x, a in zip(X, a0)]),
                            ('site-additive (linear in x12, x14, x15, x16)', [[x[12], x[14], x[15], x[16]] for x in X])):
                s = solve_exact(A, y)
                if s is not None: res = (name, [str(v) for v in s]); break
            F[key] = res or ('not site-additive', None)
        return F
    phys = [r for r in FK if r['kind'] == 'cif']
    G_all = fits_global(FK); G_phys = fits_global(phys)
    # ---- family window fits (per unit: per row of tiles / per kagome slab) ----
    ST = [r for r in FK if r['kind'] == 'st']; K59 = [r for r in FK if r['kind'] == 'fk59']
    W_st = {k: fit_windows(ST, k, None) for k in keys}
    W_59 = {k: fit_windows(K59, k, FLIP) for k in keys}
    # ---- fraction-only check of the YK law on the table ----
    tab = []
    for name, desc, v in TABLE:
        N = sum(v); x = [Fr(a, N) for a in v]
        Zb = Fr(12 * v[0] + 14 * v[1] + 15 * v[2] + 16 * v[3], N)
        a0 = x[0] - x[1] / 3 - Fr(7, 6) * x[2] - 2 * x[3]
        tab.append(dict(name=name, desc=desc, counts=v, Zbar=str(Zb), a0=str(a0), yk_line=str(Fr(68, 5) - Fr(2, 5) * x[0])))
    out = dict(structures=R, keys=keys, global_all=G_all, global_phys=G_phys,
               window_st={k: (m, {a: str(b) for a, b in (c or {}).items()}) for k, (m, c) in W_st.items()},
               window_fk59={k: (m, {a: str(b) for a, b in (c or {}).items()}) for k, (m, c) in W_59.items()},
               table=tab, n=dict(phys=len(phys), st=len(ST), fk59=len(K59)))
    json.dump(out, open(os.path.join(outdir, 'splash2_fk.json'), 'w'), indent=1, default=str)
    print('TCP structures: physical', len(phys), 'square-triangle', len(ST), 'FK59', len(K59))
    print('\nGLOBAL (all TCP, per atom):')
    for k in keys: print(f'  {k:28s} all: {G_all[k][0]:45s} {G_all[k][1]}   | physical: {G_phys[k][0]}')
    print('\nWINDOWS square-triangle rows (per row) / FK59 (per slab):')
    for k in keys: print(f'  {k:28s} ST m={W_st[k][0]} {dict(list((W_st[k][1] or {}).items())[:6])}  | FK59 m={W_59[k][0]} {dict(list((W_59[k][1] or {}).items())[:6])}')
    print('\nTABLE (counts only):')
    for t in tab: print('  ', t)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
