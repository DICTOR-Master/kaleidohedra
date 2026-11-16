#!/usr/bin/env python3
"""Prop 6 of #109: automorphisms of finite Coxeter groups W and the three cases
(a) rho o sigma ~ rho, (b) rho o sigma ~ rho (x) lambda (lambda != 1, 1-dim), (c) otherwise,
for rho the reflection (defining) representation.  Written from scratch.

Exact model: roots as integer coefficient vectors over Z[phi] (phi^2 = phi + 1) in the
simple-root basis, closed under the simple reflections s_i(v) = v - <v, alpha_i^vee> alpha_i.
W acts faithfully as permutations of the roots.  The trace of g is
sum_i (coefficient of alpha_i in g(alpha_i)), exact in Z[phi].

Automorphisms: a tuple (t_1..t_r) of involutions with ord(t_i t_j) = m_ij defines a
homomorphism W -> W (Coxeter presentation); it is an automorphism iff it is a bijection.
Pruning: t_i lies in a class of the same size as the class of s_i (automorphisms preserve
class sizes).  Mod inner: t_1 runs over one representative per candidate class, and
|Aut| = sum_R |class R| * #{sigma : sigma(s_1) = R}.
"""
import sys, json, time
import numpy as np
from math import lcm
from multiprocessing import Pool

# ---------- Z[phi] arithmetic on int pairs (a, b) = a + b phi ----------
def zmul(x, y):
    a, b = x; c, d = y
    return (a * c + b * d, a * d + b * c + b * d)
def zadd(x, y): return (x[0] + y[0], x[1] + y[1])
def zsub(x, y): return (x[0] - y[0], x[1] - y[1])
def zgal(x):    # phi -> 1 - phi  (sqrt5 -> -sqrt5)
    return (x[0] + x[1], -x[1])

PHI = (0, 1)
def coxeter_matrix(typ):
    r = int(typ[1:]) if typ[0] != 'I' else 2
    M = [[1 if i == j else 2 for j in range(r)] for i in range(r)]
    def put(i, j, m): M[i][j] = M[j][i] = m
    if typ[0] == 'A':
        for i in range(r - 1): put(i, i + 1, 3)
    elif typ[0] == 'B':
        for i in range(r - 2): put(i, i + 1, 3)
        put(r - 2, r - 1, 4)
    elif typ[0] == 'D':
        for i in range(r - 2): put(i, i + 1, 3)
        put(r - 3, r - 1, 3)
    elif typ == 'F4':
        put(0, 1, 3); put(1, 2, 4); put(2, 3, 3)
    elif typ[0] == 'H':
        put(0, 1, 5)
        for i in range(1, r - 1): put(i, i + 1, 3)
    return M

def cartan(typ, M):
    """A[i][j] = <alpha_j, alpha_i^vee> in Z[phi]; s_i(alpha_j) = alpha_j - A[i][j] alpha_i."""
    r = len(M)
    A = [[(2, 0) if i == j else (0, 0) for j in range(r)] for i in range(r)]
    for i in range(r):
        for j in range(r):
            if i == j: continue
            m = M[i][j]
            if m == 3: A[i][j] = (-1, 0)
            elif m == 5: A[i][j] = (0, -1)          # -2cos(pi/5) = -phi
            elif m == 4:
                # B_r: alpha_{r-1} short (last); F4: alpha_2, alpha_3 short (0-based 2,3)
                long_i = (typ[0] == 'B' and i < r - 1) or (typ == 'F4' and i < 2)
                A[i][j] = (-1, 0) if long_i else (-2, 0)
    return A

def build(typ):
    M = coxeter_matrix(typ); r = len(M); A = cartan(typ, M)
    simple = [tuple((1, 0) if k == i else (0, 0) for k in range(r)) for i in range(r)]
    def refl(i, v):
        c = (0, 0)
        for j in range(r): c = zadd(c, zmul(v[j], A[i][j]))
        return tuple(zsub(v[k], c) if k == i else v[k] for k in range(r))
    roots = list(simple); seen = set(roots); q = list(simple)
    while q:
        v = q.pop()
        for i in range(r):
            w = refl(i, v)
            if w not in seen: seen.add(w); roots.append(w); q.append(w)
    idx = {v: k for k, v in enumerate(roots)}
    N = len(roots)
    gens = [np.array([idx[refl(i, v)] for v in roots], dtype=np.int32) for i in range(r)]
    # group by BFS over right multiplication g -> g * s_i  (perm composition p∘q = p[q])
    ident = np.arange(N, dtype=np.int32)
    elems = [ident]; key = {ident.tobytes(): 0}; parent = [-1]; pgen = [-1]; length = [0]
    frontier = [0]
    while frontier:
        nf = []
        for e in frontier:
            for i in range(r):
                h = elems[e][gens[i]]
                kb = h.tobytes()
                if kb not in key:
                    key[kb] = len(elems); elems.append(h); parent.append(e); pgen.append(i)
                    length.append(length[e] + 1); nf.append(key[kb])
        frontier = nf
    E = np.array(elems)
    coef = [[roots[k][i] for k in range(N)] for i in range(r)]   # coef[i][root] = coefficient on alpha_i
    tr = []
    for g in E:
        t = (0, 0)
        for i in range(r): t = zadd(t, coef[i][g[i]])
        tr.append(t)
    return dict(typ=typ, M=M, r=r, roots=roots, N=N, gens=gens, E=E, key=key,
                parent=np.array(parent), pgen=np.array(pgen), length=np.array(length), tr=tr,
                coef=coef)

def perm_order(p):
    n = len(p); seen = np.zeros(n, bool); o = 1
    for s in range(n):
        if not seen[s]:
            c = 0; x = s
            while not seen[x]:
                seen[x] = True; x = p[x]; c += 1
            o = lcm(o, c)
    return o

G = None
def init(typ):
    global G
    _ocache.clear()   # order cache is per group
    G = build(typ)
    E = G['E']; n = len(E)
    inv = np.empty_like(E); inv[np.arange(n)[:, None], E] = np.arange(G['N'])  # inv[g][g[k]] = k
    G['inv'] = inv
    # BFS layers for vectorised image computation
    order = np.argsort(G['length'], kind='stable')
    G['order'] = order

def conj_class(gidx):
    E = G['E']; key = G['key']
    cl = {gidx}; q = [gidx]
    while q:
        x = q.pop()
        for s in G['gens']:
            y = key[s[E[x][s]].tobytes()]
            if y not in cl: cl.add(y); q.append(y)
    return cl

def images(tup):
    """sigma(g) for every g, as permutations, given sigma(s_i) = E[tup[i]]."""
    E = G['E']; n = len(E)
    img = np.empty_like(E); img[0] = E[0]
    T = [E[t] for t in tup]
    order = G['order']; parent = G['parent']; pgen = G['pgen']
    L = G['length']
    for lev in range(1, L.max() + 1):
        ids = order[L[order] == lev]
        for i in range(G['r']):
            sel = ids[pgen[ids] == i]
            if len(sel): img[sel] = img[parent[sel]][:, T[i]]
    return img

def classify(tup):
    img = images(tup)
    n = len(img)
    keys = set(map(bytes, img))
    if len(keys) != n:
        return None
    key = G['key']
    # homomorphism sanity on generators: sigma(g s_i) = sigma(g) sigma(s_i) is by construction;
    # bijectivity + Coxeter relations => automorphism.
    coef = G['coef']; r = G['r']
    trs = []
    for g in img:
        t = (0, 0)
        for i in range(r): t = zadd(t, coef[i][g[i]])
        trs.append(t)
    chi = G['tr']; gal = [zgal(x) for x in chi]
    res = {'is_chi': trs == chi}
    lam_hits, gal_hits = [], []
    for name, lam in G['lams']:
        twisted = [x if l == 1 else (-x[0], -x[1]) for x, l in zip(chi, lam)]
        if name != 'trivial' and trs == twisted: lam_hits.append(name)
        tg = [x if l == 1 else (-x[0], -x[1]) for x, l in zip(gal, lam)]
        if gal != chi and trs == tg: gal_hits.append(name)
    res['lam'] = lam_hits; res['gal'] = gal_hits
    case = 'a' if res['is_chi'] else ('b' if lam_hits else 'c')
    # inner?  sigma inner iff exists w with w s_i w^-1 = t_i for all i
    inner = bool(np.any(np.all(G['conjgen'] == np.array(tup)[None, :], axis=1)))
    # images of reflections: reflections -> reflections ?
    refl_to_refl = all(int(t) in G['reflset'] for t in tup)
    return (case, tuple(lam_hits), tuple(gal_hits), inner, refl_to_refl,
            [list(x) for x in trs[:0]])

def search_from(args):
    t1, cands, orders = args
    r = G['r']; M = G['M']
    out = []
    def dfs(tup):
        k = len(tup)
        if k == r:
            c = classify(tup)
            if c is not None: out.append((tuple(int(x) for x in tup), c[:5]))
            return
        for t in cands[k]:
            if all(orders(t, tup[j]) == M[k][j] for j in range(k)):
                dfs(tup + [t])
    dfs([t1])
    return out

_ocache = {}
def order_of(a, b):
    k = (a, b) if a < b else (b, a)
    if k not in _ocache:
        _ocache[k] = 1 if a == b else perm_order(G['E'][a][G['E'][b]])
    return _ocache[k]

def worker(args):
    t1, cands = args
    return search_from((t1, cands, order_of))

def main(typ, nproc):
    t0 = time.time()
    init(typ)
    E = G['E']; n = len(E); r = G['r']; key = G['key']
    print(f'{typ}: |W| = {n}, roots = {G["N"]}, Coxeter matrix rows = {G["M"]}', flush=True)
    # 1-dim characters: +-1 on generators, equal across odd m_ij
    lams = []
    import itertools
    for vals in itertools.product((1, -1), repeat=r):
        if all(vals[i] == vals[j] for i in range(r) for j in range(r) if G['M'][i][j] % 2 == 1):
            lv = np.ones(n, int)
            for e in G['order'][1:]:
                lv[e] = lv[G['parent'][e]] * vals[G['pgen'][e]]
            lams.append(('trivial' if all(v == 1 for v in vals) else 'eps' + ''.join('+' if v == 1 else '-' for v in vals), list(lv)))
    G['lams'] = lams
    gidx = [key[s.tobytes()] for s in G['gens']]
    # involutions and class sizes
    inv_ids = [i for i in range(1, n) if np.array_equal(E[i][E[i]], E[0])]
    classes = []; done = set()
    for i in inv_ids:
        if i in done: continue
        c = conj_class(i); done |= c; classes.append(sorted(c))
    csize = {}
    for c in classes:
        for x in c: csize[x] = len(c)
    reflset = set()
    for g in gidx: reflset |= set(conj_class(g))
    G['reflset'] = reflset
    print(f'involution classes (size, trace of rep): {[(len(c), G["tr"][c[0]]) for c in classes]}', flush=True)
    # conjugates of generators by every w: conjgen[w, i] = index of w s_i w^-1
    inv = G['inv']
    conjgen = np.zeros((n, r), dtype=np.int64)
    for i, gi in enumerate(gidx):
        s = E[gi]
        P = inv[:, :][:, :]  # w^-1
        # w s w^-1 as permutation: w[s[w^-1]]
        prods = np.take_along_axis(E, s[inv], axis=1)
        conjgen[:, i] = [key[p.tobytes()] for p in prods]
    G['conjgen'] = conjgen
    cands = [[x for x in inv_ids if csize[x] == csize[gidx[i]]] for i in range(r)]
    reps = []
    for c in classes:
        if len(c) == csize[gidx[0]]: reps.append(c[0])
    print(f'candidates per generator: {[len(c) for c in cands]}; class reps for t1: {len(reps)}', flush=True)
    # split work: t1 fixed to a class rep, parallelise over t2
    tasks = []
    for R in reps:
        tasks.append((R, cands))
    # finer split over t2
    fine = []
    for R in reps:
        for t2 in cands[1]:
            if order_of(R, t2) == G['M'][1][0]:
                fine.append((R, t2))
    def task_list():
        for R, t2 in fine:
            yield (R, t2)
    global CANDS
    CANDS = cands
    with Pool(nproc, initializer=_winit, initargs=(typ, cands, lams, reflset, conjgen)) as pool:
        results = pool.map(_w2, fine, chunksize=1)
    found = [x for res in results for x in res]
    print(f'fine tasks {len(fine)}, tuples found {len(found)}', flush=True)
    # weights: |class(R)|
    Z = [i for i in range(n) if all(G['E'][i][G['E'][g]].tolist() == G['E'][g][G['E'][i]].tolist() for g in gidx)]
    inn = n // len(Z)
    total = 0; bytype = {}
    for (tup, c) in found:
        w = csize[tup[0]]
        total += w
        k = (c[0], c[1], c[2], c[3], c[4])
        bytype[k] = bytype.get(k, 0) + w
    print(f'|Z(W)| = {len(Z)}, |Inn| = {inn}, |Aut| = {total}, |Out| = {total / inn}', flush=True)
    summary = []
    for k, v in sorted(bytype.items(), key=lambda kv: (kv[0][0], kv[0][3] is False)):
        line = dict(case=k[0], lambda_twists=list(k[1]), galois_twists=list(k[2]), inner=k[3],
                    reflections_to_reflections=k[4], n_automorphisms=v, n_outer_classes=v / inn)
        summary.append(line)
        print('  ', line, flush=True)
    print(f'time {time.time() - t0:.1f}s', flush=True)
    return dict(type=typ, order=n, center=len(Z), inn=inn, aut=total, out=total / inn, classes=summary)

def _winit(typ, cands, lams, reflset, conjgen):
    init(typ); G['lams'] = lams; G['reflset'] = reflset; G['conjgen'] = conjgen
    global CANDS; CANDS = cands

def _w2(args):
    R, t2 = args
    r = G['r']; M = G['M']; out = []
    def dfs(tup):
        k = len(tup)
        if k == r:
            c = classify(tup)
            if c is not None: out.append((tuple(int(x) for x in tup), c[:5]))
            return
        for t in CANDS[k]:
            if all(order_of(t, tup[j]) == M[k][j] for j in range(k)):
                dfs(tup + [t])
    dfs([R, t2])
    return out

if __name__ == '__main__':
    types = sys.argv[1].split(',')
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    outp = sys.argv[3] if len(sys.argv) > 3 else None
    allr = []
    fail = None
    for t in types:
        try:
            res = main(t, nproc)
            allr.append(res)
            out = res['out']
            if abs(out - round(out)) > 1e-9: fail = f'{t}: |Aut|/|Inn| not integral'
            cs = [c for c in res['classes'] if c['case'] == 'c']
            if t in ('H3', 'H4'):
                if any(not c['galois_twists'] for c in cs): fail = f'{t}: case (c) without Galois'
            elif t == 'A5':
                if not cs or any(c['galois_twists'] for c in cs): fail = 'A5: expected case (c) w/o Galois'
            else:
                if cs: fail = f'{t}: unexpected case (c)'
        except Exception as e:
            import traceback; traceback.print_exc(); fail = f'{t}: {e!r}'
    if outp: json.dump(allr, open(outp, 'w'), indent=1)
    print('FINAL ok' if fail is None else 'FINAL FAIL ' + fail)
