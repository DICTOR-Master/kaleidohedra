"""Proper round, part 2: without a shape restriction, ONE helper kind always exists (exact construction).
C1 (edge 1) with a 5-fold axis n vertical.  D = {S(x,y) - h <= z <= S(x,y)}, (x,y) in a W x W square, where S is the plane z = zc plus,
over each lattice point, the tip of the top spike above zc.  D tiles space by the translations (W,0,0), (0,W,0), (0,0,h).
Checks (sympy, every comparison certified at 50 digits with the margin printed): only the top spike reaches above zc; C1 lies in the
ball of radius RA (the apex distance); W > 2 RA; h > 2 RA (the bump of the bottom surface stays below C1).  Then K = closure(D minus C1)
is a flat-faced solid; with C1 it tiles space, 1 K per C1, periodically.  Run: python round_trivial.py (writes data/round_trivial.json)"""
import itertools, json
import sympy as sp
phi = (1 + sp.sqrt(5)) / 2
cyc = lambda t: [(t[0], t[1], t[2]), (t[2], t[0], t[1]), (t[1], t[2], t[0])]
TV = set()
for b in [(0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, 2 * phi + 1)]:
    for sg in itertools.product((1, -1), repeat=3):
        for c in cyc(tuple(sg[i] * b[i] for i in range(3))): TV.add(tuple(sp.nsimplify(x / 2) for x in c))
TV = [sp.Matrix(v) for v in TV]; assert len(TV) == 60
pd = []
for a_, b_ in itertools.product((1, -1), repeat=2):
    for c in cyc((0, a_, b_ * phi)): pd.append(sp.Matrix(c) / sp.sqrt(1 + phi ** 2))
Rd2 = 3 * phi ** 2 / 4
def apex(n):
    rp = max(sp.N(v.dot(n), 30) for v in TV)
    pent = [v for v in TV if abs(sp.N(v.dot(n), 30) - rp) < 1e-20]; assert len(pent) == 5
    c = sum(pent, sp.zeros(3, 1)) / 5
    return sp.simplify(c + sp.sqrt(sp.radsimp(Rd2 - (pent[0] - c).dot(pent[0] - c))) * n), sp.radsimp(c.norm())
n = pd[0]
A, rp = apex(n)
zA = sp.radsimp(A.dot(n)); RA = sp.radsimp(A.norm())
others = [sp.N(v.dot(n), 50) for v in TV] + [sp.N(apex(m)[0].dot(n), 50) for m in pd[1:]]
second = max(others)
zc = (rp + zA) / 2
W = 2 * RA + 1; h = 2 * RA + 1
pr = lambda s: print(s, flush=True)
ok = True
def chk(name, margin):
    global ok
    m = sp.N(margin, 50); ok = ok and m > 0; pr(f"  [{'pass' if m > 0 else 'FAIL'}] {name}  (margin {float(m):.6f})")
pr(f"top spike apex height zA = {sp.nsimplify(zA)} = {float(zA):.6f}; pentagon height rp = {float(rp):.6f}; next-highest C1 vertex {float(second):.6f}")
chk("only the top spike rises above zc = (rp + zA)/2: zc - (next-highest vertex)", zc - second)
chk("zc inside the top spike: zA - zc", zA - zc)
# C1 is a union of convex pieces with vertices among TV and the 12 apices; all have norm <= RA
norms = [sp.N(v.norm(), 50) for v in TV]
chk("every truncated-icosahedron vertex is inside the ball of radius RA (apex distance)", RA - max(norms))
chk("lateral period W = 2RA + 1 exceeds 2RA", W - 2 * RA)
chk("bottom surface bump stays below C1: (h - zA) - RA  i.e. bump top zA - h < -RA", h - zA - RA)
VTI = (125 + 43 * sp.sqrt(5)) / 4
Apent = sp.sqrt(25 + 10 * sp.sqrt(5)) / 4
hp = sp.sqrt(sp.radsimp(Rd2 - (1 / (2 * sp.sin(sp.pi / 5))) ** 2))
VC1 = sp.nsimplify(VTI + 12 * Apent * hp / 3)
VK = W ** 2 * h - VC1
pr(f"vol C1 = {float(VC1):.6f} (step 3 float value 62.950850); vol K = W^2 h - vol C1 = {float(VK):.4f}")
ok = ok and abs(float(VC1) - 62.950850) < 1e-5
json.dump(dict(zA=float(zA), rp=float(rp), next_highest=float(second), zc=float(zc), RA=float(RA), W=float(W), h=float(h),
               vol_C1=float(VC1), vol_K=float(VK), K_per_C1=1,
               note="K = closure(D minus C1): flat faces, homeomorphic to a ball; its face in the plane z = zc has a pentagonal hole "
                    "(where the spike tip of the C1 below enters). Variant: K = box minus C1 (a box with a C1-shaped cavity)."),
          open('data/round_trivial.json', 'w'), indent=1)
pr("FINAL ok" if ok else "FINAL FAIL")
