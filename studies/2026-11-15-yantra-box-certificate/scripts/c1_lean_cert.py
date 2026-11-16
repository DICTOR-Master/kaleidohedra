"""Lean export of the whole box certificate (step 1 of the Lean plan): writes, for each of the 10 charts,
  lean/YantraCert/Data/<Ch>/Polys.lean   the chart's polynomials rescaled to the unit cube (Lean core only) and `C_deg`;
  lean/YantraCert/Data/<Ch>/P<k>.lean    one subtree of the bisection tree each, proved by `decide +kernel` (Lean core only);
  lean/YantraCert/Data/<Ch>/All.lean     the assembly: `covered : C.Covered root` from the subtrees (needs Mathlib, via Cover).
plus lean/YantraCert/Data/All.lean (imports every chart) and data/lean-cert-files.json (file list with cost estimates, sizes, hashes).

Rescaling: every chart box is prod [0, W_j], so y_j = x_j / W_j and the stored polynomial is K * p(W y) with K > 0 the common
denominator (recorded in the Polys file).  Methods: each leaf's test is tried with the monotone split first, then the slope form,
exactly as b4_check.py; the method bits go into the codes.  Split rule and preorder as in b4_check.py.
Usage: c1_lean_cert.py [budget]   (budget = estimated cost units per subtree file; 1 unit = one slope-form term evaluation)"""
from lean_module import modulize   # Palomar source rule: every generated file in module form (16 Nov 2026)
import json, os, sys, hashlib
from multiprocessing import get_context
NW = int(os.environ.get('NW', '8'))
LEAFCODE = {}
def leaf_code_g(arg):
    ch, lf = arg
    return LEAFCODE[ch](lf)
from fractions import Fraction as Fq
from math import gcd
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D_ = lambda *p: os.path.join(HERE, *p)
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 4e5
CHARTS = [('main', 'Main'), ('A', 'A'), ('B', 'B'), ('C1', 'C1'), ('C2', 'C2'), ('W', 'W'), ('Wt+', 'Wtp'), ('Wt-', 'Wtm'),
          ('Wr+', 'Wrp'), ('Wr-', 'Wrm')]
ONLY = os.environ.get('ONLY', '').split(',') if os.environ.get('ONLY') else None
HOLES = {'main': json.load(open(D_('data', 'holes-main.json')))['holes'], 'C1': json.load(open(D_('data', 'holes-C1.json')))['holes']}
OUT = D_('lean', 'YantraCert', 'Data')

def rescale(p, W):
    out = [(tuple(e), Fq(int(c)) * W[0]**e[0] * W[1]**e[1] * W[2]**e[2]) for e, c in p]
    den = 1
    for e, v in out: den = den * v.denominator // gcd(den, v.denominator)
    return [(e, int(v * den)) for e, v in out if v != 0], den

def degs(p): return [max([e[j] for e, c in p] + [0]) for j in range(3)]

def mono_sign(p, D, cell):
    lo = hi = 0
    for e, c in p:
        a = 1; b = 1
        for j, (d, i) in enumerate(cell): a *= i**e[j] << ((D[j] - e[j]) * d); b *= (i + 1)**e[j] << ((D[j] - e[j]) * d)
        if c > 0: lo += c * a; hi += c * b
        else: lo += c * b; hi += c * a
    return 1 if lo > 0 else (2 if hi < 0 else 0)

def slope_sign(p, D, cell):
    """the Lean `slopeAcc` / `signOf` computation, literally"""
    E = [d + 1 for d, i in cell]; L = [2 * i for d, i in cell]
    sp = lambda j, n, a: n**a << ((D[j] - a) * E[j])
    acc = {s: [0] * 7 for s in (1, -1)}
    for e, c in p:
        a, b, g = e; s = 1 if c > 0 else -1; c = abs(c); A = acc[s]
        lx, mx, hx = sp(0, L[0], a), sp(0, L[0] + 1, a), sp(0, L[0] + 2, a)
        ly, my, hy = sp(1, L[1], b), sp(1, L[1] + 1, b), sp(1, L[1] + 2, b)
        lz, mz, hz = sp(2, L[2], g), sp(2, L[2] + 1, g), sp(2, L[2] + 2, g)
        A[0] += c * mx * my * mz; A[1] += c * (hx - mx) * hy * hz; A[2] += c * (mx - lx) * ly * lz
        A[3] += c * mx * (hy - my) * hz; A[4] += c * mx * (my - ly) * lz; A[5] += c * mx * my * (hz - mz); A[6] += c * mx * my * (mz - lz)
    P, N = acc[1], acc[-1]
    rad = max(abs(P[1] - N[2]), abs(P[2] - N[1])) + max(abs(P[3] - N[4]), abs(P[4] - N[3])) + max(abs(P[5] - N[6]), abs(P[6] - N[5]))
    return 1 if N[0] + rad < P[0] else (2 if P[0] + rad < N[0] else 0)

def sign_with(p, D, cell):
    s = mono_sign(p, D, cell)
    if s: return s, 0, 0.5 * len(p) * (1 if s == 1 else 2)
    s = slope_sign(p, D, cell)
    return s, 1, len(p) * 1.0 + len(p)

def np_lit(terms, name):
    """NP literal, in chunks of at most 400 nested terms"""
    chunks = [terms[k:k + 400] for k in range(0, len(terms), 400)] or [[]]
    defs = []; names = []
    for ci, ch in enumerate(chunks):
        s = '.nil'
        for e, c in reversed(ch): s = f'(.cons {c} {e[0]} {e[1]} {e[2]} {s})'
        defs.append(f'noncomputable def {name}_{ci} : NP := {s}'); names.append(f'{name}_{ci}')
    expr = names[-1]
    for nm in reversed(names[:-1]): expr = f'(NP.app {nm} {expr})'
    defs.append(f'noncomputable def {name} : NP := {expr}')
    return defs

def sp_defs(p, name):
    D = degs(p)
    # 17 Nov 2026: each part in ascending lexicographic order of (a, b, e), the order of ZP.add, so that ZP.ofSP's insertion
    # sorts are linear (unsorted, the largest polynomial took 11.7 GB of kernel memory in Deriv/KRWtp)
    pos = sorted((tuple(e), c) for e, c in p if c > 0); neg = sorted((tuple(e), -c) for e, c in p if c < 0)
    assert len({e for e, _ in pos + neg}) == len(pos) + len(neg), 'repeated monomial'
    return np_lit(pos, name + 'p') + np_lit(neg, name + 'n') + [f'noncomputable def {name} : SP := ⟨{D[0]}, {D[1]}, {D[2]}, {name}p, {name}n⟩']

manifest = {'budget': BUDGET, 'charts': {}}
os.makedirs(OUT, exist_ok=True)
allmods = []
for ch, CH in CHARTS:
    if ONLY and ch not in ONLY: continue
    data = json.load(open(D_('data', 'polys-utr.json' if ch == 'main' else f'polys-utr-{ch}.json')))
    cert = json.load(open(D_('data', f'bnb-{ch}.json')))
    box = [[Fq(a), Fq(b)] for a, b in data['box']]
    assert all(a == 0 for a, b in box), ch
    W = [b for a, b in box]
    usedF = {l[7] for l in cert['leaves'] if l[6] == 'F'}; Fk = [k for k in data['F'] if k in usedF]
    used = {l[7] for l in cert['leaves'] if l[6] == 'T'}; Tk = [k for k in data['tests'] if k in used]
    F = {}; FK = {}
    for k in Fk: F[k], FK[k] = rescale(data['F'][k], W)
    T = {}; TK = {}
    for k in Tk:
        n, kn = rescale(data['tests'][k]['N'], W); d, kd = rescale(data['tests'][k]['D'], W); T[k] = (n, d); TK[k] = (kn, kd)
    holes = HOLES.get(ch, [])
    Hk = [h['name'] for h in holes]
    # holes in unit coordinates: y = x / W
    HB = []
    for h in holes:
        row = []
        for j in range(3):
            lo = Fq(h['box'][j][0]) / W[j]; hi = Fq(h['box'][j][1]) / W[j]
            row += [lo.numerator, lo.denominator, hi.numerator, hi.denominator]
        HB.append(row)
    leaves = {(l[0], l[1], l[2], l[3], l[4], l[5]): l for l in cert['leaves']}
    assert len(leaves) == len(cert['leaves']) and not cert.get('open')
    # rebuild the tree in preorder; compute codes and costs
    def kids(nd):
        d = [nd[0], nd[2], nd[4]]; j = min(range(3), key=lambda k: (d[k], k)); out = []
        for b in (0, 1):
            c = list(nd); c[2 * j] += 1; c[2 * j + 1] = 2 * nd[2 * j + 1] + b; out.append(tuple(c))
        return out
    def leaf_code(lf):

        cell = ((lf[0], lf[1]), (lf[2], lf[3]), (lf[4], lf[5])); kind, nm = lf[6], lf[7]
        if kind == 'F':
            p = F[nm]; s, m, cost = sign_with(p, degs(p), cell); assert s, (ch, lf)
            return 8 * (2 * Fk.index(nm) + m) + 1, cost
        if kind == 'T':
            n, d = T[nm]; sN, mN, c1 = sign_with(n, degs(n), cell); sD, mD, c2 = sign_with(d, degs(d), cell)
            assert sN and sD and sN != sD, (ch, lf, sN, sD)
            return 8 * (4 * Tk.index(nm) + 2 * mN + mD) + 2, c1 + c2
        if kind == 'H':
            k = Hk.index(nm)
            for j, (dd, ii) in enumerate(cell):
                lo, lq, hi, hq = HB[k][4 * j:4 * j + 4]
                assert lo * 2**dd <= ii * lq and (ii + 1) * hq <= hi * 2**dd, (ch, lf)
            return 8 * k + 3, 1.0
        raise ValueError(lf)
    LEAFCODE[ch] = leaf_code
    # every leaf's code and cost once (in parallel), then subtree costs and depths bottom-up
    keys = list(leaves)
    with get_context('fork').Pool(NW) as pool: LC = dict(zip(keys, pool.map(leaf_code_g, [(ch, leaves[k]) for k in keys], chunksize=64)))
    root = (0, 0, 0, 0, 0, 0)
    order = []; stack = [root]
    while stack:
        nd = stack.pop(); order.append(nd)
        if nd not in leaves: stack.extend(kids(nd))
    COST = {}; DEP = {}
    for nd in reversed(order):
        if nd in leaves: COST[nd] = LC[nd][1]; DEP[nd] = 1
        else:
            a, b = kids(nd); COST[nd] = COST[a] + COST[b] + 1; DEP[nd] = 1 + max(DEP[a], DEP[b])
    def codes_of(nd):
        out = []; st = [nd]
        while st:
            x = st.pop()
            if x in leaves: out.append(LC[x][0])
            else: out.append(0); a, b = kids(x); st.append(b); st.append(a)
        return out
    files = []; top = {}
    def part(nd):
        if COST[nd] <= BUDGET or nd in leaves:
            files.append((nd, codes_of(nd), COST[nd], DEP[nd])); return ('F', len(files) - 1)
        a, b = kids(nd); top[nd] = (part(a), part(b)); return ('T', nd)
    rootref = part(root)
    cdir = os.path.join(OUT, CH); os.makedirs(cdir, exist_ok=True)
    for f in os.listdir(cdir):
        if f.endswith('.lean'): os.remove(os.path.join(cdir, f))
    ns = f'YantraCert.Data.{CH}'
    # Polys
    src = ['import YantraCert.Check', '', 'set_option maxRecDepth 100000', '', f'/-! Chart {ch}: polynomials rescaled to the unit cube',
           f'(box {data["box"]}; stored = K * p(W y), K > 0).  Generated by scripts/c1_lean_cert.py from data/{"polys-utr.json" if ch == "main" else "polys-utr-" + ch + ".json"}. -/', '',
           f'namespace {ns}', 'open YantraCert', '']
    for i, k in enumerate(Fk):
        src.append(f'-- F{i} = {k}~, K = {FK[k]}'); src += sp_defs(F[k], f'F{i}')
    for i, k in enumerate(Tk):
        src.append(f'-- T{i} = test "{k}", K_N = {TK[k][0]}, K_D = {TK[k][1]}'); src += sp_defs(T[k][0], f'T{i}N') + sp_defs(T[k][1], f'T{i}D')
    hb = ', '.join('⟨' + ', '.join(map(str, r)) + '⟩' for r in HB)
    for i, k in enumerate(Hk): src.append(f'-- H{i} = hole "{k}"')
    src.append('noncomputable def C : Chart := ⟨[' + ', '.join(f'F{i}' for i in range(len(Fk))) + '], [' +
               ', '.join(f'(T{i}N, T{i}D)' for i in range(len(Tk))) + '], [' + hb + ']⟩')
    src += ['', 'theorem C_deg : C.degOK = true := by decide +kernel', '', f'end {ns}', '']
    open(os.path.join(cdir, 'Polys.lean'), 'w').write(modulize('\n'.join(src)))
    # subtree files
    fl = []
    for k, (nd, codes, cost, dep) in enumerate(files):
        cell = '⟨' + ', '.join(map(str, nd)) + '⟩'
        s = ['import YantraCert.Data.' + CH + '.Polys', '', f'namespace {ns}.P{k}', 'open YantraCert', '',
             f'def cell : Cell := {cell}', f'noncomputable def codes : TC := TC.ofList [{", ".join(map(str, codes))}]', '',
             f'theorem ok : checkTree C {dep + 1} cell codes = true := by decide +kernel', '', f'end {ns}.P{k}', '']
        txt = modulize('\n'.join(s)); open(os.path.join(cdir, f'P{k}.lean'), 'w').write(txt)
        fl.append({'file': f'YantraCert/Data/{CH}/P{k}.lean', 'module': f'{ns}.P{k}', 'cell': nd, 'leaves': sum(1 for c in codes if c % 8),
                   'cost': cost, 'depth': dep, 'bytes': len(txt), 'sha256': hashlib.sha256(txt.encode()).hexdigest()})
    # assembly
    s = ['import YantraCert.Cover', f'import YantraCert.Data.{CH}.Polys'] + [f'import {ns}.P{k}' for k in range(len(files))] + \
        ['', f'/-! Chart {ch}: the whole bisection tree covers the unit cube (assembled from {len(files)} subtree files). -/', '',
         f'namespace {ns}', 'open YantraCert', '']
    for k, (nd, codes, cost, dep) in enumerate(files):
        s.append(f'theorem f{k} : C.Covered P{k}.cell := checkTree_sound C C_deg {dep + 1} P{k}.cell P{k}.codes P{k}.ok')
    names = {}
    def nm(ref): return f'f{ref[1]}' if ref[0] == 'F' else names[ref[1]]
    # bottom-up over top nodes (children before parents): sort by depth descending
    for i, nd in enumerate(sorted(top, key=lambda n: -(n[0] + n[2] + n[4]))):
        names[nd] = f't{i}'
    for nd in sorted(top, key=lambda n: -(n[0] + n[2] + n[4])):
        a, b = top[nd]
        s.append(f'theorem {names[nd]} : C.Covered ⟨{", ".join(map(str, nd))}⟩ := C.covered_split _ {nm(a)} {nm(b)}')
    s += ['', '/-- every point of the unit cube is `Good` for this chart -/',
          f'theorem covered : C.Covered ⟨0, 0, 0, 0, 0, 0⟩ := {nm(rootref)}', '', f'end {ns}', '']
    open(os.path.join(cdir, 'All.lean'), 'w').write(modulize('\n'.join(s)))
    allmods.append(f'{ns}.All')
    manifest['charts'][ch] = {'lean': CH, 'W': [str(w) for w in W], 'F': Fk, 'T': Tk, 'H': Hk, 'files': fl,
                              'KF': {k: str(FK[k]) for k in Fk}, 'KT': {k: [str(TK[k][0]), str(TK[k][1])] for k in Tk},
                              'total_cost': sum(f['cost'] for f in fl), 'leaves': len(leaves), 'top_nodes': len(top)}
    print(f'{ch}: {len(leaves)} leaves, {len(files)} files, top nodes {len(top)}, cost {sum(f["cost"] for f in fl):.3g}', flush=True)
if not ONLY: open(os.path.join(OUT, 'All.lean'), 'w').write(modulize('\n'.join([f'import {m}' for m in allmods] + [''])))
json.dump(manifest, open(D_('data', 'lean-cert-files.json' if not ONLY else 'lean-cert-files-partial.json'), 'w'), indent=1)
# every leaf's test was re-proved above (assert); the codes must hold exactly one entry per leaf in every chart
ok = all(sum(f['leaves'] for f in c['files']) == c['leaves'] for c in manifest['charts'].values())
ok = ok and (ONLY or sum(c['leaves'] for c in manifest['charts'].values()) == 64613)
print('FINAL ok' if ok else 'FINAL FAIL: leaf counts do not match')
