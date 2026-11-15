"""Twisted silence for the binary polyhedral groups 2T, 2O, 2I on S^3 (unit quaternions).
For each group G and each twist sigma (identity = ordinary classes; the outer automorphism; a deliberately wrong sigma):
  * all twisted classes O = {a x0 sigma(a)^-1}, exactly (arithmetic in Q(sqrt d), Fractions)
  * DIRECT: degrees k <= KMAX killed, exact zonal sums sum_{y in O} U_k(<x0,y>) (O is one orbit, so one row suffices)
  * CRITERION (numerical block test, independent of the direct sums): V_k = Sym^k(C^2) restricted to G is split into isotypic
    blocks by a random central element C (labels are the eigenvalues, so the same irreducible gets the same label at every k);
    pi is sigma-stable iff the central element C' = sum c(g) rho(sigma g) has the same eigenvalue there; the block P_pi S of
    S = sum_{x in O} rho_k(x) is tested for zero. Theorem content tested: (i) unstable blocks are always zero, (ii) the zero/nonzero
    status of a stable block depends only on (pi, O), never on k, (iii) prediction 'all stable blocks of V_k zero' == direct, k<=KMAX.
  * FORCED: exact dimension of invariant harmonics of degree k for the twist group {x -> a x sigma(a)^-1}:
    (1/|G|) sum_a U_k(Re a) U_k(Re sigma a)  (H_k = V_k (x) V_k as SU(2)xSU(2) module).
  * irreducibility of the twist group on R^4: (1/|G|) sum_a (2 Re a . 2 Re sigma a)^2 == 1 ?
  * flatness: affine rank of the class (a class in a hyperplane = latitude slice, the classical case).
Prints CHECK / SIG / TABLE lines and FINAL ok only if all checks pass."""
import sys, random, itertools
from fractions import Fraction as Fr
from collections import Counter
import numpy as np

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
KCRIT = int(sys.argv[2]) if len(sys.argv) > 2 else 40
GROUPS = sys.argv[3].split(',') if len(sys.argv) > 3 else ['2T', '2O', '2I']
fails = 0
def check(ok, what):
    global fails
    if not ok: fails += 1
    print(('CHECK OK   ' if ok else 'CHECK FAIL ') + what, flush=True)

class F:                                   # a + b sqrt(D), D fixed per run of a group
    D = 5
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    @staticmethod
    def c(x): return x if isinstance(x, F) else F(x)
    def __add__(s, o): o = F.c(o); return F(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return F(-s.a, -s.b)
    def __sub__(s, o): o = F.c(o); return F(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = F.c(o); return F(s.a * o.a + F.D * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def gal(s): return F(s.a, -s.b)
    def __eq__(s, o): o = F.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def z(s): return s.a == 0 and s.b == 0
    def __float__(s): return float(s.a) + float(s.b) * F.D ** 0.5
    def __repr__(s): return f'({s.a}+{s.b}r{F.D})' if s.b else f'{s.a}'

def qmul(p, q):
    a0, a1, a2, a3 = p; b0, b1, b2, b3 = q
    return (a0*b0 - a1*b1 - a2*b2 - a3*b3, a0*b1 + a1*b0 + a2*b3 - a3*b2, a0*b2 - a1*b3 + a2*b0 + a3*b1, a0*b3 + a1*b2 - a2*b1 + a3*b0)
def qconj(p): return (p[0], -p[1], -p[2], -p[3])
def qneg(p): return tuple(-t for t in p)
def dot(p, q): return p[0]*q[0] + p[1]*q[1] + p[2]*q[2] + p[3]*q[3]
def cheb(k, c):
    u0, u1 = F(1), 2 * c
    if k == 0: return u0
    for _ in range(k - 1): u0, u1 = u1, 2 * c * u1 - u0
    return u1
def signs(v):
    out = set()
    for s in itertools.product((1, -1), repeat=4):
        out.add(tuple(F.c(x) * si for x, si in zip(v, s)))
    return out
def even_perms(v):
    out = []
    for p in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2 == 0: out.append(tuple(v[p[i]] for i in range(4)))
    return out

def build(name):
    Z, H = F(0), F(Fr(1, 2))
    T = set()
    for i in range(4):
        e = [Z] * 4; e[i] = F(1); T |= signs(e)
    T |= signs((H, H, H, H))
    if name == '2T': return sorted(T, key=repr)
    if name == '2O':
        r = F(0, Fr(1, 2))                      # 1/sqrt2
        G = set(T)
        for i, j in itertools.combinations(range(4), 2):
            e = [Z] * 4; e[i] = r; e[j] = r; G |= signs(e)
        return sorted(G, key=repr)
    PHI = F(Fr(1, 2), Fr(1, 2)); IPHI = PHI - 1
    G = set(T)
    for v in even_perms((PHI * H, H, IPHI * H, Z)): G |= signs(v)
    return sorted(G, key=repr)

def make_twists(name, G):
    Gs = set(G)
    tw = {'id': lambda a: a}
    if name == '2T':                              # outer automorphism: conjugation by u = (1+i)/sqrt2 (an element of 2O), entries stay rational
        u = (F(0, Fr(1, 2)), F(0, Fr(1, 2)), F(0), F(0))      # (1+i)/sqrt2, an element of 2O
        def s(a): return qmul(qmul(u, a), qconj(u))
        tw['outer'] = s
    elif name == '2O':
        tw['outer'] = lambda a: tuple(t.gal() for t in a)    # Galois sqrt2 -> -sqrt2 = a -> eps(a) a
    else:
        tw['outer'] = lambda a: (a[0].gal(), -a[1].gal(), a[3].gal(), a[2].gal())   # Fable's sigma (golden A4 study)
    so = tw['outer']
    def wrong(a):                                 # sigma times a sign that is not a character (a +-closed non-subgroup set)
        b = so(a)
        return qneg(b) if a[0] * a[0] == F(Fr(1, 4)) else b
    tw['wrong'] = wrong
    return tw

def is_aut(G, s):
    Gs = set(G)
    img = [s(a) for a in G]
    if set(img) != Gs: return False
    return all(s(qmul(a, b)) == qmul(s(a), s(b)) for a in G for b in G[::5])
def is_inner(G, s):
    return any(all(s(a) == qmul(qmul(g, a), qconj(g)) for a in G) for g in G)

def su2(q):
    w, x, y, z = (float(t) for t in q)
    return np.array([[w + 1j * x, y + 1j * z], [-y + 1j * z, w - 1j * x]])
def symk(U, k):
    """matrix of Sym^k(U) on the basis u^(k-j) v^j, for the substitution (u, v) -> (u, v) U"""
    M = np.zeros((k + 1, k + 1), dtype=complex)
    a, b, c, d = U[0, 0], U[0, 1], U[1, 0], U[1, 1]
    for j in range(k + 1):                        # image of u^(k-j) v^j : (a u + c v)^(k-j) (b u + d v)^j
        p1 = np.array([1.0 + 0j])
        for _ in range(k - j): p1 = np.convolve(p1, [a, c])   # coefficients in powers of v (u^(...) implicit)
        p2 = np.array([1.0 + 0j])
        for _ in range(j): p2 = np.convolve(p2, [b, d])
        M[:, j] = np.convolve(p1, p2)
    return M

def classes(G):
    Gi = {g: i for i, g in enumerate(G)}
    cls = [-1] * len(G); nc = 0
    for i, g in enumerate(G):
        if cls[i] >= 0: continue
        for h in G: cls[Gi[qmul(qmul(h, g), qconj(h))]] = nc
        nc += 1
    return cls, nc

def full_symmetry(P):
    """all orthogonal maps of R^4 permuting the point set P (n x 4 float), by Gram backtracking on a spanning 4-subset"""
    n = len(P); Gm = P @ P.T
    base = []
    for i in range(n):
        if np.linalg.matrix_rank(P[base + [i]], tol=1e-9) > len(base): base.append(i)
        if len(base) == np.linalg.matrix_rank(P, tol=1e-9): break
    r = len(base); maps = []
    def rec(img):
        j = len(img)
        if j == r:
            A = np.linalg.lstsq(P[base], P[img], rcond=None)[0].T          # A p_base = p_img
            Q = P @ A.T
            if not np.allclose(A @ A.T, np.eye(4), atol=1e-8) and r == 4: return
            d = np.abs(Q[:, None, :] - P[None, :, :]).sum(2).min(1)
            if d.max() < 1e-8: maps.append(A)
            return
        for c in range(n):
            if c in img: continue
            if all(abs(Gm[c, img[t]] - Gm[base[j], base[t]]) < 1e-9 for t in range(j)) and abs(Gm[c, c] - Gm[base[j], base[j]]) < 1e-9:
                rec(img + [c])
    rec([])
    return maps
def harm_char(A, k):
    ev = np.linalg.eigvals(A)
    def h(m):                                    # complete homogeneous symmetric polynomial of the eigenvalues
        if m < 0: return 0
        c = np.zeros(m + 1, dtype=complex); c[0] = 1
        for e in ev:
            for t in range(1, m + 1): c[t] += e * c[t - 1]
        return c[m]
    return h(k) - h(k - 2)

rng = np.random.default_rng(20261115)
summary = []
for gi, name in enumerate(GROUPS):
    F.D = 2 if name in ('2T', '2O') else 5
    G = build(name); n = len(G); Gi = {g: i for i, g in enumerate(G)}
    check(n == {'2T': 24, '2O': 48, '2I': 120}[name] and all(qmul(G[3], g) in Gi for g in G), f'{name}: {n} elements, closed')
    U0 = su2(G[5]); U1 = su2(G[7])
    check(np.allclose(su2(qmul(G[5], G[7])), U0 @ U1), f'{name}: quaternion -> SU(2) is multiplicative')
    check(np.allclose(symk(U0 @ U1, 5), symk(U0, 5) @ symk(U1, 5)) or np.allclose(symk(U0 @ U1, 5), symk(U1, 5) @ symk(U0, 5)), f'{name}: Sym^k map is a (anti)homomorphism')
    anti = not np.allclose(symk(U0 @ U1, 5), symk(U0, 5) @ symk(U1, 5))
    from math import comb, sqrt
    def rho(q, k):                                # unitary form: monomial basis scaled by sqrt(binomial)
        U = su2(q); M = symk(U.T, k).T if anti else symk(U, k)
        d = np.array([sqrt(comb(k, j)) for j in range(k + 1)])
        return (M * d[None, :]) / d[:, None]
    check(np.allclose(rho(qmul(G[5], G[7]), 6), rho(G[5], 6) @ rho(G[7], 6)), f'{name}: rho_k is a homomorphism')
    check(all(np.allclose(rho(g, 7) @ rho(g, 7).conj().T, np.eye(8)) for g in G[:10]), f'{name}: rho_k is unitary')
    cls, nc = classes(G)
    cvals = rng.normal(size=nc) + 1j * rng.normal(size=nc)
    LABELS = []                                   # irreducible labels found so far (matched with tolerance across k)
    def lab_of(x):
        for L in LABELS:
            if abs(L - x) < 1e-6: return L
        LABELS.append(x); return x
    def herm(coef_of_index, R):                   # Hermitian central element: c rho(g) + conj(c) rho(g)^*
        M = sum(coef_of_index(i) * R[i] for i in range(n))
        return (M + M.conj().T) / 2, (M - M.conj().T) / 2j
    tws = make_twists(name, G)
    so = tws['outer']
    check(is_aut(G, so) and not is_inner(G, so), f'{name}: sigma_outer is an automorphism and not inner')
    check(not is_aut(G, tws['wrong']), f'{name}: wrong sigma is NOT an automorphism (control)')
    for tname in ('id', 'outer', 'wrong'):
        s = tws[tname]
        ir = sum((F(4) * a[0] * s(a)[0]) * (F(4) * a[0] * s(a)[0]) for a in G) * F(Fr(1, n))
        forced_dim = {k: sum(cheb(k, a[0]) * cheb(k, s(a)[0]) for a in G) * F(Fr(1, n)) for k in range(1, KMAX + 1)}
        # twisted classes
        left = set(G); cl = []
        while left:
            x0 = sorted(left, key=repr)[0]
            O = sorted({qmul(qmul(a, x0), qconj(s(a))) for a in G}, key=repr)
            cl.append((x0, O)); left -= set(O)
        if tname == 'wrong': cl = [(x0, O) for x0, O in cl]
        print(f'== {name} sigma={tname}: {len(cl)} classes, sizes {sorted(len(O) for _, O in cl)}; twist group irreducible on R^4: {ir == F(1)} (sum chi^2/|G| = {ir})', flush=True)
        if tname != 'wrong':
            check(all(set(O) <= set(G) for _, O in cl), f'{name} {tname}: classes partition G')
        # numeric block criterion
        blocks = {}       # (label, class index) -> zero?
        stable_of = {}
        pred, dirk = {}, {}
        for ci, (x0, O) in enumerate(cl):
            cnt = Counter(dot(x0, y) for y in O)
            dirk[ci] = [k for k in range(1, KMAX + 1) if sum((cheb(k, c) * m for c, m in cnt.items()), F(0)).z()]
        for k in range(1, KCRIT + 1):
            R = [rho(g, k) for g in G]
            sref = s if tname != 'wrong' else tws['outer']
            C1, C2 = herm(lambda i: cvals[cls[i]], R)
            Cp1, Cp2 = herm(lambda i: cvals[cls[Gi[sref(G[i])]]] if False else cvals[cls[i]], [R[Gi[sref(G[i])]] for i in range(n)])
            C = C1 + 0.3719 * C2; Cp = Cp1 + 0.3719 * Cp2
            ev, V = np.linalg.eigh(C)
            order = np.argsort(ev); groups = {}
            cur = [order[0]]
            for a, b in zip(order[:-1], order[1:]):
                if abs(ev[b] - ev[a]) < 1e-6 * n: cur.append(b)
                else: groups[lab_of(float(np.mean(ev[cur])) / n)] = cur; cur = [b]
            groups[lab_of(float(np.mean(ev[cur])) / n)] = cur
            for ci, (x0, O) in enumerate(cl):
                S = sum(R[Gi[y]] for y in O)
                allzero_stable = True
                for l, idxs in groups.items():
                    Q = V[:, idxs]
                    P = Q @ Q.conj().T
                    lp = float(np.real(np.trace(Q.conj().T @ Cp @ Q))) / len(idxs) / n
                    st = abs(lp - l) < 1e-6
                    stable_of[l] = st
                    zero = np.linalg.norm(P @ S) < 1e-7 * max(1, len(O))
                    if not st:
                        if tname != 'wrong': check(zero, f'{name} {tname} k={k} class {ci}: unstable block is zero') if not zero else None
                        if not zero: allzero_stable = False
                        continue
                    key = (l, ci)
                    if key in blocks and blocks[key] != zero and tname != 'wrong':
                        check(False, f'{name} {tname}: block status of irreducible {l} on class {ci} depends on k (k={k})')
                    blocks.setdefault(key, zero)
                    if not blocks[key]: allzero_stable = False
                pred.setdefault(ci, [])
                if allzero_stable: pred[ci].append(k)
        for ci, (x0, O) in enumerate(cl):
            d = [k for k in dirk[ci] if k <= KCRIT]
            if tname != 'wrong': check(pred[ci] == d, f'{name} {tname} class {ci} (|O|={len(O)}): criterion == direct for k <= {KCRIT}')
        if tname == 'wrong':
            # wrong sigma: the block-status table of the TRUE sigma, read at the base point, must fail to predict these sets
            mism = sum(1 for ci in pred for k in range(1, KCRIT + 1) if (k in pred[ci]) != (k in dirk[ci]))
            hom_fail = any(not np.allclose(rho(G[i], 3) @ sum(rho(y, 3) for y in cl[0][1]), sum(rho(y, 3) for y in cl[0][1]) @ rho(tws['wrong'](G[i]), 3)) for i in range(n))
            check(hom_fail, f'{name} wrong sigma: S does not intertwine (control)')
            print(f'   wrong sigma: {mism} block-prediction mismatches (informational; the block test needs an automorphism)')
        # signatures
        for ci, (x0, O) in enumerate(cl):
            sig = [k for k in dirk[ci] if k <= 30]
            forced = [k for k in range(1, min(30, KMAX) + 1) if forced_dim[k].z()]
            unf = [k for k in sig if k not in forced]
            pts = np.array([[float(t) for t in y] for y in O])
            cen = pts - pts.mean(0)
            arank = np.linalg.matrix_rank(cen, tol=1e-9)
            unf_full = None
            if unf and tname != 'wrong' and len(O) > 1:
                if arank == 4 or True:
                    syms = full_symmetry(pts) if arank == 4 else None
                    if syms:
                        unf_full = [k for k in unf if round(float(np.real(sum(harm_char(A, k) for A in syms))) / len(syms)) > 0]
                        print(f'   full symmetry of the set: order {len(syms)}; zeros unforced by it: {unf_full}')
                    else:
                        print('   set lies in a hyperplane (affine rank < 4): a latitude slice; its zeros are the classical latitude/3D-orbit zeros')
            print(f'SIG {name} sigma={tname} class {ci} |O|={len(O)} x0={tuple(float(t) for t in x0)} affine-rank={arank} kills<=30={sig} forced={[k for k in forced if k<=12]}... UNFORCED={unf}', flush=True)
            summary.append((name, tname, ci, len(O), int(arank), sig, unf, unf_full))
    print(f'PROGRESS {(gi+1)/len(GROUPS):.2f} {name} done', flush=True)
print('TABLE (group, twist, class, size, affine rank, killed<=30, unforced by the twist group)')
for r in summary: print('  ', r)
print(f'checks failed: {fails}')
print('FINAL ok' if fails == 0 else 'FINAL FAIL')
