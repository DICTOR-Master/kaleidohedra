"""Independent referee checks for Tang, aiXiv 2611.01161 (written by the referee;
does not import or run any of the author's code).  Reads the paper's .tex appendix,
the CHEVIE family definitions (as text) and the parsed Alvis rank-24 ring (as data).
Pure python + numpy.  Run: python3 -I referee_checks.py <pkgdir>
"""
import sys, json, math, cmath, itertools, re
from fractions import Fraction as Fr
import numpy as np

PKG = sys.argv[1]
TEX = PKG + "/Lusztig_Fourier_Conjecture.tex"
OUT = {}
def rec(k, v):
    OUT[k] = v
    print(f"[{k}] {v}")

# ---------------------------------------------------------------- Q(sqrt5)
class Q5:
    __slots__ = ("a", "b")
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def conj(s): return Q5(s.a, -s.b)
    def norm(s): return s.a*s.a - 5*s.b*s.b
    def inv(s): n = s.norm(); return Q5(s.a/n, -s.b/n)
    def __truediv__(s, o): o = o if isinstance(o, Q5) else Q5(o); return s * o.inv()
    def __eq__(s, o): o = o if isinstance(o, Q5) else Q5(o); return s.a == o.a and s.b == o.b
    def __float__(s): return float(s.a) + float(s.b)*math.sqrt(5)
    def __repr__(s): return f"({s.a}+{s.b}r5)"
PHI = Q5(Fr(1, 2), Fr(1, 2)); ALPHA = Q5(Fr(-1, 2), Fr(1, 2)); D = Q5(1080, 480)

# ---------------------------------------------------------------- 1. separation bound
N_D = D.norm()
rec("1a N_{Q(r5)/Q}(1080+480r5)", N_D)
assert N_D == 14400
# [Q(zeta60):Q] = phi(60)
eul = sum(1 for k in range(1, 61) if math.gcd(k, 60) == 1)
rec("1b [Q(zeta60):Q]", eul)
# N_L(D) = N_{Q5}(D)^{[L:Q5]} = 14400^8; bound 1 <= 14400^8 |d|^2 2^14  =>  |d| >= 1/(2^7 14400^4)
thr = 2**7 * 14400**4
rec("1c 128*14400^4", thr)
assert thr == 5503765708800000000
rec("1d threshold decimal", float(Fr(1, thr)))
rec("1e certified error 3.422e-140 < threshold", 3.422e-140 < 1/thr)
# sqrt5 in Q(zeta60): sqrt5 = zeta5 - zeta5^2 - zeta5^3 + zeta5^4 (Gauss sum)
z5 = cmath.exp(2j*math.pi/5)
rec("1f Gauss sum zeta5-z^2-z^3+z^4 = sqrt5", abs((z5 - z5**2 - z5**3 + z5**4) - math.sqrt(5)) < 1e-12)
# D*(A+B r5)/120 = (9A+20B)+(4A+9B) r5 ?
Asym, Bsym = Q5(1, 0), Q5(0, 1)
lhs_A = D * Q5(Fr(1, 120)); lhs_B = D * Q5(0, Fr(1, 120))
rec("1g D/120 = 9+4r5 ; D*r5/120 = 20+9r5", (lhs_A == Q5(9, 4), lhs_B == Q5(20, 9)))

# ---------------------------------------------------------------- 2. HS4 target from appendix
tex = open(TEX, encoding="utf8").read()
# dictionary table
dict_block = tex[tex.index("Code&$a$&$b$"):tex.index("\\bottomrule", tex.index("Code&$a$&$b$"))]
codes = {}
for m in re.finditer(r"\\texttt\{(\\?.)\}&(-?\d+)&(-?\d+)", dict_block):
    c = m.group(1).replace("\\", "")
    codes[c] = (int(m.group(2)), int(m.group(3)))
rec("2a dictionary size", len(codes))
rows = {}
for m in re.finditer(r"^(\d\d)  (\S{74})$", tex, re.M):
    rows[int(m.group(1))] = m.group(2)
assert sorted(rows) == list(range(1, 75)), sorted(rows)[:5]
A = np.array([[codes[ch][0] for ch in rows[i]] for i in range(1, 75)], dtype=object)
B = np.array([[codes[ch][1] for ch in rows[i]] for i in range(1, 75)], dtype=object)
At, Bt = A.T, B.T
I74 = np.identity(74, dtype=object) * 1
rec("2b A symmetric, B symmetric", (bool((A == At).all()), bool((B == Bt).all())))
rec("2c A^2+5B^2 = 14400 I", bool(((A.dot(A) + 5*B.dot(B)) == 14400*I74).all()))
rec("2d AB+BA = 0", bool(((A.dot(B) + B.dot(A)) == 0).all()))
F = [[Q5(Fr(A[i, j], 120), Fr(B[i, j], 120)) for j in range(74)] for i in range(74)]
Ff = np.array([[float(x) for x in r] for r in F])
Fc = np.array([[float(x.conj()) for x in r] for r in F])
rec("2e both real embeddings orthogonal (float)", (np.abs(Ff @ Ff.T - np.eye(74)).max() < 1e-12, np.abs(Fc @ Fc.T - np.eye(74)).max() < 1e-12))
pos_rows = [i+1 for i in range(74) if (Ff[i] > 0).all()]
rec("2f strictly positive rows (1-based)", pos_rows)
rec("2g F[9,9] == 1/D exactly", F[8][8] == D.inv())
dims = [F[8][j] * D for j in range(74)]
rec("2h D*F[9,j] all positive", all(float(d) > 0 for d in dims))
s = Q5(0)
for d in dims: s = s + d*d
rec("2i sum_j (D F9j)^2 == D^2", s == D*D)
twophi6 = Q5(2)*PHI*PHI*PHI*PHI*PHI*PHI
rec("2j D*F[9,73], D*F[9,74] == 2 phi^6 == 18+8r5", (dims[72] == twophi6, dims[73] == twophi6, twophi6 == Q5(18, 8)))
# twist exponents
tblock = tex[tex.index("(t_1,\\ldots,t_{74})"):tex.index("\\end{aligned}", tex.index("(t_1,\\ldots,t_{74})"))]
tvals = [int(x) for x in re.findall(r"\d+", tblock.split("={}")[1])]
assert len(tvals) == 74, len(tvals)
theta = np.array([cmath.exp(2j*math.pi*t/60) for t in tvals])
rec("2k t-vector length, lcm of orders", (len(tvals), np.lcm.reduce([60//math.gcd(t, 60) for t in tvals])))
for sgn in (+1, -1):
    T = np.diag(theta**sgn)
    M = Ff @ T
    M3 = M @ M @ M
    lam = M3[0, 0] / (Ff @ Ff)[0, 0]
    ok = np.abs(M3 - lam*(Ff @ Ff)).max()
    rec(f"2l (F T^{sgn:+d})^3 = lambda F^2 residual, lambda", (float(ok), complex(round(lam.real, 12), round(lam.imag, 12))))
# Gauss sum check: p+ = sum d_i^2 theta_i ; |p+| should be D
dimsf = np.array([float(d) for d in dims])
pplus = (dimsf**2 * theta).sum()
rec("2m |sum d^2 theta| / D", abs(pplus)/float(D))
# Verlinde integrality of fusion from F (sanity of target as modular data)
Nmax_err = 0; neg = 0
Sf = Ff
for i in range(74):
    for j in range(74):
        v = (Sf[i]*Sf[j]*Sf[:, :].T / Sf[8]).sum(axis=1) if False else None
# vectorised Verlinde: N_ij^k = sum_m S_im S_jm S_km / S_9m  (S real, self-dual)
W = Sf / Sf[8][None, :]
Nijk = np.einsum('im,jm,km,m->ijk', Sf, Sf, Sf, 1/Sf[8])
rnd = np.rint(Nijk)
rec("2n Verlinde N_ij^k integral & nonneg (max dev, min)", (float(np.abs(Nijk - rnd).max()), int(rnd.min())))
# squared F = I => all self-dual in modular convention
rec("2o F^2 = I (exact via 2c,2d)", True)

# ---------------------------------------------------------------- 3. pointed corner Vec_{C2}^-
# Z(Vec_{C2}^omega), omega(1,1,1) = -1. Objects (g, lam) with lam^2 = omega(g,g,g)^g ... (0,+-1),(1,+-i)
objs = [(0, 1), (0, -1), (1, 1j), (1, -1j)]
# S_+ (positive pivot), unnormalised: S(a,b) = conj? use standard: S_{(g,x),(h,y)} = x(h)^-1 y(g)^-1 with chars ext.
# For C2: half-braiding of (g,lam) with the generator is lam; double braiding of (g,lam),(h,mu) = lam^h mu^g (times sign
# corrections are absorbed for C2 since lam is chosen with lam^2=omega).  Use the semion x antisemion model instead,
# which is canonical: (0,1)=1, (0,-1)=s(x)sbar boson, (1,i)=s, (1,-i)=sbar.
Ssem = np.array([[1, 1], [1, -1]])/math.sqrt(2)
Santi = Ssem.conj()
basis = [(0, 0), (1, 1), (1, 0), (0, 1)]   # (semion label, antisemion label)
Splus = np.array([[Ssem[a[0], b[0]]*Santi[a[1], b[1]] for b in basis] for a in basis])
theta_sem = [1, 1j]; theta_anti = [1, -1j]
twists = [theta_sem[a]*theta_anti[b] for a, b in basis]
rec("3a twists of (1, boson, s, sbar)", twists)
Dd = np.diag([1, 1, -1, -1])
SEW = Dd @ Splus @ Dd
paper_pointed = np.array([[1, 1, -1, -1], [1, 1, 1, 1], [-1, 1, -1, 1], [-1, 1, 1, -1]])/2
rec("3b D S_+ D == paper (pointedS)", bool(np.allclose(SEW, paper_pointed)))
# CHEVIE TwistedDrinfeldDoubleCyclic(2,-1,[1,-1]) re-implemented from the GAP source text
def tqz(n, zeta, piv):
    piv = [0, piv[1]] if piv[0] == 1 else piv  # AsRootOfUnity(1)*n = 0
    def omega(a, b, c): return zeta**((a % n)*(((b % n)+(c % n))//n))
    def th(g, a, b): return omega(g, a, b)/omega(a, g, b)*omega(a, b, g)
    simple = []
    for i in range(n):
        prod = 1
        for k in range(1, n): prod *= th(i, 1, k)
        r = cmath.exp(1j*cmath.phase(prod)/n)   # GetRoot: principal root
        for j in range(n): simple.append((i, r*cmath.exp(2j*math.pi*j/n)))
    p0, p1 = piv
    Fm = np.array([[p1**i[0]*p1**j[0]*i[1]**p0*j[1]**p0*i[1]**j[0]*j[1]**i[0] for j in simple] for i in simple])/(n*p1**(-2*p0))
    ev = [p1**i[0]*i[1]**p0*i[1]**i[0] for i in simple]
    return simple, Fm, ev
simp, Ftqz, evtqz = tqz(2, -1, [1, -1])
rec("3c CHEVIE TQZ(2,-1,[1,-1]) labels", [(g, complex(round(l.real, 9), round(l.imag, 9))) for g, l in simp])
rec("3d CHEVIE TQZ fourierMat == paper (pointedS) in this order", bool(np.allclose(Ftqz, paper_pointed)))
rec("3e TQZ eigenvalues", [complex(round(e.real, 9), round(e.imag, 9)) for e in evtqz])
rec("3f TQZ F^2 == I (perm trivial)", bool(np.allclose(Ftqz @ Ftqz, np.eye(4))))
# untwisted Vec_C2 (toric code) would have twists 1,1,1,-1 -- cannot carry eigenvalues +-i
rec("3g twists of Z(Vec_C2) untwisted", [1, 1, 1, -1])
# FS/snake: skeletal g with ev scalar e, coev scalar c, unit-normalised associator w: snake gives c*e*w = 1
for w in (1, -1):
    rec(f"3h snake: ev.coev = 1/omega for omega={w}", 1/w)

# ---------------------------------------------------------------- 4. Fibonacci corner
phi = (1+math.sqrt(5))/2
Sfib = np.array([[1, phi], [phi, -1]])/math.sqrt(1+phi**2)
fibbasis = [(0, 0), (1, 1), (0, 1), (1, 0)]
SZfib = np.array([[Sfib[a[0], b[0]]*Sfib[a[1], b[1]] for b in fibbasis] for a in fibbasis])
paperFib = np.array([[1/phi, phi, 1, 1], [phi, 1/phi, -1, -1], [1, -1, -1/phi, phi], [1, -1, phi, -1/phi]])/math.sqrt(5)
rec("4a tensor square of Fib S == paper (FibS)", bool(np.allclose(SZfib, paperFib)))
# CHEVIE Dihedral(5)
e = 5; e1 = e//2
nc = [[0, l] for l in range(1, e1+1)] + [[k, l] for k in range(1, e1) for l in range(k+1, e-k)]
c = lambda a: 2*math.cos(2*math.pi*a/e)
Fpair = np.array([[(c(i[0]*j[1]+i[1]*j[0]) - c(i[0]*j[0]+i[1]*j[1]))/e for j in nc] for i in nc])
perm = {}
for a, i in enumerate(nc):
    t = [i[0], e - i[1]]
    if t in nc and nc.index(t) > a: perm[a] = nc.index(t); perm[nc.index(t)] = a
P = np.eye(4)[:, [perm.get(k, k) for k in range(4)]]
Fmod = Fpair @ P
rec("4b Dihedral(5) labels, perm", (nc, perm))
rec("4c traces: pairing, modular", (round(np.trace(Fpair), 12), round(np.trace(Fmod), 12)))
found = [p for p in itertools.permutations(range(4)) if np.allclose(Fmod[np.ix_(p, p)], paperFib)]
rec("4d simultaneous perms sending F^mod(Dihedral5) to paper (FibS)", found)
found2 = [p for p in itertools.permutations(range(4)) if np.allclose(Fpair[np.ix_(p, p)], paperFib)]
rec("4e simultaneous perms sending unconverted pairing to (FibS) [should be none]", found2)
# Fib F-matrix pentagon (orthonormal gauge) and autoequivalence constraint
al = 1/phi
Fm = np.array([[al, math.sqrt(al)], [math.sqrt(al), -al]])
rec("4f FibF^2 = I, unitary", bool(np.allclose(Fm @ Fm, np.eye(2))))
# a diagonal tensorator diag(lam, mu^2) must commute with Fm  => lam = mu^2
rec("4g commutant of FibF among diagonals is scalar", bool(abs(Fm[0, 1]) > 0))
z = math.sqrt(al)
Up = np.linalg.inv(np.diag([z, 1])) @ Fm @ np.diag([z, 1])
rec("4h U' = diag(z,1)^-1 U diag(z,1) == [[a,1],[a,-a]], U'^2=I", (bool(np.allclose(Up, [[al, 1], [al, -al]])), bool(np.allclose(Up @ Up, np.eye(2)))))
# sign character on Fib must be trivial: t^2=1 and t^2=t
rec("4i solutions of t^2=1,t^2=t", [t for t in (1, -1) if t*t == 1 and t*t == t])

# ---------------------------------------------------------------- 5. SU(2)_8 even part = K4 table
k = 8
def su2(a, b):
    return [cc for cc in range(abs(a-b), min(a+b, 2*k-a-b)+1, 2)]
labs = [0, 2, 4, 6, 8]
tab = {(i, j): [labs.index(cc) for cc in su2(labs[i], labs[j])] for i in range(5) for j in range(5)}
paperK4 = {(1, 1): [0, 1, 2], (1, 2): [1, 2, 3], (1, 3): [2, 3, 4], (1, 4): [3], (2, 2): [0, 1, 2, 3, 4], (2, 3): [1, 2, 3], (2, 4): [2], (3, 3): [0, 1, 2], (3, 4): [1], (4, 4): [0]}
rec("5a SU(2)_8 even fusion == paper K4 table", all(tab[kk] == v for kk, v in paperK4.items()) and all(tab[(0, j)] == [j] for j in range(5)))
q = cmath.exp(1j*math.pi/(k+2))
qd = [((q**(j+1) - q**(-(j+1)))/(q - q**-1)).real for j in labs]
rec("5b quantum dims", [round(x, 9) for x in qd])
rec("5c == (1,phi^2,2phi,phi^2,1)", bool(np.allclose(qd, [1, phi**2, 2*phi, phi**2, 1])))
th8 = cmath.exp(2j*math.pi*8*10/(4*(k+2)))
mono = [cmath.exp(2j*math.pi*((8+j)*(8+j+2) - 8*10 - j*(j+2))/(4*(k+2))) for j in labs]  # monodromy via twists of fusion product 8 x j = 8-j
mono = [cmath.exp(2j*math.pi*(((8-j)*(8-j+2)) - 80 - j*(j+2))/(4*(k+2))) for j in labs]
rec("5d twist of label 8, monodromies with even j", (complex(round(th8.real, 9), round(th8.imag, 9)), [round(m.real, 9) for m in mono]))
DimE = sum(x*x for x in qd)
rec("5e Dim E, Dim K=Dim E/2, (1+phi^2)^2", (round(DimE, 9), round(DimE/2, 9), round((1+phi**2)**2, 9)))

# ---------------------------------------------------------------- 6. dims of D0, grading
def inv(p): return sum(1 for a in range(len(p)) for b in range(a+1, len(p)) if p[a] > p[b])
s = Q5(0)
phi2 = PHI*PHI
for p in itertools.permutations(range(4)):
    t = Q5(1)
    for _ in range(inv(p)): t = t*phi2
    s = s + t
rec("6a sum_{w in S4} phi^{2 l(w)}", s)
rec("6b == 540+240r5 and 2x == D", (s == Q5(540, 240), s*2 == D))
# Gram determinant for path p-m-q with labels k,k
for kk in range(3, 9):
    cth = math.cos(math.pi/kk)
    G = np.array([[1, -cth, 0], [-cth, 1, -cth], [0, -cth, 1]])
    rec(f"6c k={kk}: det G, 1-2cos^2, posdef", (round(np.linalg.det(G), 12), round(1-2*cth**2, 12), bool(np.all(np.linalg.eigvalsh(G) > 1e-12))))

# ---------------------------------------------------------------- 7. family / cell counts from CHEVIE text
h4 = open(PKG + "/source_package/fourier_s/sources/chevie_coxh4.g", encoding="utf8").read()
h3 = open(PKG + "/source_package/fourier_s/fs_agent/sources/chevie_coxh3.g", encoding="utf8").read()
def families(txt):
    blk = txt[txt.index("families:=["):]
    blk = blk[:re.search(r"\n\s*a:=\[", blk).start()]
    fams = re.findall(r'Family\((?:"(\w+)"|CHEVIE\.families\.(\w+)\(([^)]*)\)),\s*\[([^\]]*)\]', blk)
    out = []
    for name1, name2, arg, lst in fams:
        out.append((name1 or f"{name2}({arg})", [int(x) for x in lst.replace("\n", " ").split(",")]))
    avals = [int(x) for x in re.findall(r"-?\d+", blk.split("a:=")[0]) ] if False else None
    a = txt[txt.index("a:=[", txt.index("families:=[")):]
    a = [int(x) for x in re.findall(r"\d+", a[:a.index("]")])]
    return out, a
for nm, txt in (("H3", h3), ("H4", h4)):
    fams, a = families(txt)
    summary = [(f, len(l), sorted({a[i-1] for i in l})) for f, l in fams]
    rec(f"7a {nm}: #families, #unipotent", (len(fams), sum(len(l) for _, l in fams)))
    rec(f"7b {nm}: (type, size, a)", summary)
# dihedral: CHEVIE Dihedral(e) family size vs paper formula
bad = []
for e in range(3, 41):
    e1 = e//2
    ncs = [(k, l) for k in range(1, e1) for l in range(k+1, e-k)]
    size = (2 + (e1-1) + len(ncs)) if e % 2 == 0 else (e1 + len(ncs))
    formula = ((e-1)//2)**2 if e % 2 else e*(e-2)//4 + 2
    if size != formula: bad.append((e, size, formula))
rec("7c dihedral family size == paper center-rank formula for m=3..40 (mismatches)", bad)

# ---------------------------------------------------------------- 8. Alvis rank-24 ring (data parsed by author; we only read it)
al24 = json.load(open(PKG + "/source_package/fourier_s/computation_agent/alvis_ring_24.json"))
M = np.array(al24["multiplication"], dtype=np.int64)  # shape 24x24x24
rec("8a shape", M.shape)
# find convention N[i][j][k] = coeff of x_k in x_i x_j  by associativity + unit x2 (index 1)
def prod(N, u, v): return np.einsum('i,j,ijk->k', u, v, N)
convs = {"M[i][j][k]": M, "M[i][k][j]": M.transpose(0, 2, 1), "M[j][i][k]": M.transpose(1, 0, 2),
         "M[j][k][i]": M.transpose(2, 0, 1), "M[k][i][j]": M.transpose(1, 2, 0), "M[k][j][i]": M.transpose(2, 1, 0)}
E = np.eye(24, dtype=np.int64)
good = {}
for nm, N in convs.items():
    unit = all((prod(N, E[1], E[j]) == E[j]).all() and (prod(N, E[j], E[1]) == E[j]).all() for j in range(24))
    assoc = all((prod(N, prod(N, E[i], E[j]), E[k]) == prod(N, E[i], prod(N, E[j], E[k]))).all() for i in range(24) for j in range(24) for k in range(24))
    good[nm] = (unit, assoc)
rec("8b (unit x2, associative) per index convention", good)
x = lambda i: E[i-1]
def show(v): return "+".join(f"{'' if c == 1 else c}x{k+1}" for k, c in enumerate(v) if c)
for nm, N in convs.items():
    if not all(good[nm]): continue
    r = {"a0^2": show(prod(N, x(1), x(1))), "g^2": show(prod(N, x(23), x(23))), "g a0": show(prod(N, x(23), x(1))), "a0 g": show(prod(N, x(1), x(23))),
         "g b": show(prod(N, x(23), x(17))), "b g": show(prod(N, x(17), x(23))), "a0 b": show(prod(N, x(1), x(17))), "b a0": show(prod(N, x(17), x(1))),
         "b^2": show(prod(N, x(17), x(17)))}
    rec(f"8c products under {nm}", r)
# FP dims: Perron eigenvector of left mult by a0+b over the convention that works
N = convs["M[i][j][k]"] if all(good["M[i][j][k]"]) else [v for k2, v in convs.items() if all(good[k2])][0]
L = sum(N[i] for i in range(24))  # left mult by sum of all basis elements: L[j,k] coefficient
ev, vec = np.linalg.eig(L.T.astype(float))
i0 = np.argmax(ev.real); v = np.abs(vec[:, i0].real); v = v / v[1]
rec("8d FPdim sum of squares vs D", (round(float((v**2).sum()), 9), round(float(D), 9)))
rec("8e FPdims of x1,x2,x8,x17,x22,x23,x24", [round(float(v[i-1]), 9) for i in (1, 2, 8, 17, 22, 23, 24)])
# generation by a0, b : closure of supports
S0 = {1}; frontier = {1}
gens = [0, 16]
while frontier:
    new = set()
    for s_ in frontier:
        for g_ in gens:
            for vv in (prod(N, E[s_], E[g_]), prod(N, E[g_], E[s_])):
                for k2 in np.nonzero(vv)[0]:
                    if k2 not in S0: new.add(int(k2))
    S0 |= new; frontier = new
rec("8f basis elements reached from unit by a0,b (count)", len(S0))
# K4 and B tables from the data
lab = {0: 2, 1: 8, 2: 17, 3: 22, 4: 23}
k4ok = all(sorted(int(k2)+1 for k2 in np.nonzero(prod(N, x(lab[i]), x(lab[j])))[0]) == sorted(lab[t] for t in paperK4.get((min(i, j), max(i, j)), [j if i == 0 else i]))
           for i in range(5) for j in range(5))
rec("8g Alvis {x2,x8,x17,x22,x23} multiplication == K4 table", k4ok)

# ---------------------------------------------------------------- 9. H4 words
# H4 Coxeter matrix with m12=5, m23=m34=3 ; simple roots via Cartan-type Gram matrix
m = {(1, 2): 5, (2, 3): 3, (3, 4): 3}
def mm(i, j):
    if i == j: return 1
    return m.get((min(i, j), max(i, j)), 2)
Gm = np.array([[-math.cos(math.pi/mm(i, j)) if i != j else 1.0 for j in range(1, 5)] for i in range(1, 5)])
def refl(i):
    R = np.eye(4); R[i, :] -= 2*Gm[i, :]  # acting on root coordinates: s_i(a_j) = a_j - 2 B(a_i,a_j) a_i
    return R
Sg = [refl(i) for i in range(4)]
# generate all roots
roots = set(); frontier = [tuple(np.eye(4)[i]) for i in range(4)]
def key(v): return tuple(round(c, 6) for c in v)
allr = {key(v): np.array(v) for v in frontier}
while frontier:
    nf = []
    for v in frontier:
        for R in Sg:
            w = R @ np.array(v); kk = key(w)
            if kk not in allr: allr[kk] = w; nf.append(w)
    frontier = nf
pos = [v for v in allr.values() if (v > -1e-9).all()]
rec("9a #roots, #positive roots of H4", (len(allr), len(pos)))
def mat(word):
    Mx = np.eye(4)
    for ch in word: Mx = Mx @ Sg[int(ch)-1]
    return Mx
def length(Mx): return sum(1 for v in pos if ((Mx @ v) < -1e-9).any() and ((Mx @ v) < 1e-9).all())
w0 = -np.eye(4)
for w in ("232", "232123"):
    Mx = mat(w); rec(f"9b l({w}), l(w0*{w}), involution", (length(Mx), length(w0 @ Mx), bool(np.allclose(Mx @ Mx, np.eye(4)))))
rec("9c w0 = -1 in H4 (l(w0))", length(w0))
# Alvis words: generators a,b,c,d ; try both orderings of the Coxeter labels
aw = json.load(open(PKG + "/audit/morita/audit_alvis_source.json"))["selected_words"]
for order in ("abcd", "dcba"):
    mp = {ch: str(i+1) for i, ch in enumerate(order)}
    res = {k2: (len(v2), length(mat("".join(mp[ch] for ch in v2))), bool(np.allclose(mat("".join(mp[ch] for ch in v2)) @ mat("".join(mp[ch] for ch in v2)), np.eye(4)))) for k2, v2 in aw.items()}
    rec(f"9d Alvis words (wordlen, Coxeter length, involution) with a,b,c,d->{order}", res)

# ---------------------------------------------------------------- 10. sign arithmetic in Prop 3.1
okp = True
for lx in range(0, 61):
    for ld in range(0, 61):
        for a in range(0, 61):
            if (ld - a) % 2 or (2*lx - ld - a) % 2: continue
            e = (ld - a)//2 + (2*lx - ld - a)//2
            if (e - (lx - a)) % 2: okp = False
rec("10a (l(d)-a)/2 + (2l(x)-l(d)-a)/2 == l(x)-a", okp)

json.dump({k2: str(v2) for k2, v2 in OUT.items()}, open(sys.argv[2] if len(sys.argv) > 2 else "referee_checks_out.json", "w"), indent=1)

# ---------------------------------------------------------------- 11. pointed: twisted vs untwisted distinguishable by S?
Stor = np.array([[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]])/2   # Z(Vec_C2) order (1,e,m,f): e,m bosons? (0,1),(0,-1),(1,1),(1,-1)
LTQZ2 = np.array([[1, 1, -1, -1], [1, 1, 1, 1], [-1, 1, 1, -1], [-1, 1, -1, 1]])/2
DS = Dd @ Stor @ Dd
rec("11a Z(Vec_C2) with EW-type dims (1,1,-1,-1) equals CHEVIE LTQZ2 (Lusztig pairing form)", bool(np.allclose(DS, LTQZ2)))
rec("11b LTQZ2 * P(3,4) == TQZ (modular form)", bool(np.allclose(LTQZ2[:, [0, 1, 3, 2]], paper_pointed)))
cands = [p for p in itertools.permutations(range(4)) if np.allclose(Stor[np.ix_(p, p)], paper_pointed) or np.allclose(DS[np.ix_(p, p)], paper_pointed)]
rec("11c simultaneous perms making untwisted center S equal to TQZ (none expected)", cands)
