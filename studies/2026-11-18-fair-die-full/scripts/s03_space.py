"""Protocol steps 10-14 for the fair 14-face die: space filling.
10 alone: decided by Dehn (step 7; Debrunner 1980: a space-filler has Dehn invariant zero) -> the forced-sector search is not needed.
11 with a partner: the CsCl pair (#48 Theorem 4 in the x-form; #90 Prop. 6): S(mu) on 2Z^3 and S(3 - mu) on 2Z^3 + (1,1,1).
   Checked here: exact volume identity V(mu) + V(3 - mu) = 8, pair Dehn sum zero, and no interior overlap between a piece and all its
   neighbours (separating-axis test, studies/_lib/methods.py overlap) -> density 1 with no overlap = a tiling.
12 foam wall area W = (A(mu) + A(3 - mu))/16 (studies/2026-11-04-mahler-sweep, Kelvin's problem on the CsCl pairs).
13 regular octahedra: the octahedron filling of the line holds on chamber II only (God's Dice); n/a in chamber I.
14 halves (ortho/gyro): cut through the centre across a 3-fold axis and turn one half 60 deg, across a 4-fold axis and turn 45 deg;
   is the result convex? (twist() as in studies/2026-11-04-halves/scripts/sweep_twist.py.)  Control: CO convex (60), Kelvin TO dented.
Interlocking slab test: n/a (the CsCl tiling has no flat one-tile-thick layer: the Concordance's CsCl-pairs cell)."""
import math, json, sys, os, itertools
import numpy as np, sympy as sp, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '_lib'))
from fdlib import *
import methods as Mth
from scipy.spatial import ConvexHull, HalfspaceIntersection
C = Checks(); R = {}
mu = sp.Symbol('mu')
V = lambda t: sp.Rational(4, 3)*t**3 - 4*(t - 1)**3
A = lambda t: 12*(t - 1)**2 + 4*sp.sqrt(3)*(t**2 - 3*(t - 1)**2)
print("STEP 10. Alone: Dehn invariant nonzero (s02) -> no tiling by the die alone (Debrunner 1980); forced-sector search not needed")
print("\nSTEP 11. CsCl pair with S(3 - mu)")
C("exact: V(mu) + V(3 - mu) = 8 for all mu in chamber I", sp.expand(V(mu) + V(3 - mu) - 8) == 0)
C("exact: Dehn coefficients 24 sqrt2 (3 - 2mu) + 24 sqrt2 (3 - 2(3 - mu)) = 0", sp.expand(24*(3 - 2*mu) + 24*(3 - 2*(3 - mu))) == 0)
P = corners(MUF); Q = corners(3 - MUF)
shifts = [np.array(s, float) for s in itertools.product((-2, 0, 2), repeat=3) if any(s)]
bad = 0; tested = 0
for piece, others in ((P, [(P, s) for s in shifts] + [(Q, np.array(h, float)) for h in itertools.product((-1, 1), repeat=3)]),
                      (Q, [(Q, s) for s in shifts] + [(P, np.array(h, float)) for h in itertools.product((-1, 1), repeat=3)])):
    for o, s in others:
        tested += 1; bad += Mth.overlap(piece, o + s) > 1e-9
C(f"no interior overlap of either piece with its {tested//2} neighbours (26 same-kind, 8 other-kind)", bad == 0, f"{tested} pairs")
# control: a slightly too large partner must overlap
C("control: S(mu_f) with S(3 - mu_f + 0.01) overlaps (the test can fail)", Mth.overlap(P, corners(3 - MUF + 0.01) + np.ones(3)) > 1e-6)
# Monte Carlo point-location as a second check of density 1 (computed): every point of the cell lies in exactly one piece
rng = np.random.default_rng(1); X = rng.uniform(-1, 1, (200000, 3))
def inside(Xs, m_): return (np.abs(Xs).max(1) <= 1 + 1e-12) & (np.abs(Xs).sum(1) <= m_ + 1e-12)
cnt = inside(X, MUF).astype(int)
for h in itertools.product((-1, 1), repeat=3): cnt += inside(X - np.array(h), 3 - MUF)
C("computed: 200000 random points of the cube cell each lie in exactly one piece", int((cnt == 1).sum()) == len(X), f"{(cnt == 1).sum()}")
pc = lambda t: 4*mp.atan((t - 1)**2/(2*mp.sqrt(1 + (t - 1)**2)))/(4*mp.pi)
print(f"  partner S(3 - mu_f) = S({3 - MUF:.10f}): p(square) = {mp.nstr(pc(3 - MU_HP), 10)}, p(hexagon) = {mp.nstr((1 - 6*pc(3 - MU_HP))/8, 10)} (loaded towards the hexagons)")
print("\nSTEP 12. Foam wall area per unit volume W = (A(mu) + A(3 - mu))/16")
W = lambda t: (A(t) + A(3 - t))/16
wf = float(W(sp.Float(MUF, 30))); wk = float(W(sp.Rational(3, 2)))
dW = sp.diff(W(mu), mu)
C("W is symmetric under mu <-> 3 - mu and largest at Kelvin 3/2 (exact: W' = 0 only at 3/2, W'' < 0)", sp.simplify(W(3 - mu) - W(mu)) == 0 and sp.solve(dW, mu) == [sp.Rational(3, 2)] and float(sp.diff(W(mu), mu, 2)) < 0)
print(f"  W(mu_f) = {wf:.10f}; Kelvin W(3/2) = {wk:.5f} (studies/2026-11-04-mahler-sweep 1.67404); W exact = {sp.simplify(sp.expand(W(mu)))}")
C("Kelvin control reproduces 1.67404", abs(wk - 1.67404) < 1e-5)
R.update({'W_fair': wf, 'W_kelvin': wk, 'partner_mu': 3 - MUF})
print("\nSTEP 13. Regular octahedra: fill only in chamber II (God's Dice); mu_f is in chamber I -> n/a")
C("mu_f lies in chamber I (1 < mu_f < 2)", 1 < MUF < 2)
print("\nSTEP 14. Halves: cut through the centre, turn one half (twist as in halves/sweep_twist.py)")
def rot_to_z(a):
    a = a/np.linalg.norm(a); zz = np.array([0, 0, 1.]); v = np.cross(a, zz)
    if np.linalg.norm(v) < 1e-12: return np.eye(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]); return np.eye(3) + K + K @ K*((1 - a @ zz)/np.linalg.norm(v)**2)
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
def twist(P0, axis, ang):
    Pr = P0 @ rot_to_z(np.array(axis, float)).T; h = ConvexHull(Pr)
    def half(top):
        Hs = np.vstack([h.equations, [0, 0, -1 if top else 1, 0]]); return HalfspaceIntersection(Hs, np.array([0, 0, 1e-3 if top else -1e-3])).intersections
    T, B = half(True), half(False); U = np.unique(np.round(np.vstack([T, B @ rz(ang).T]), 9), axis=0); hu = ConvexHull(U)
    return abs(hu.volume - h.volume) < 1e-7*h.volume
for name, m_ in (("cuboctahedron 2 (control)", 2.0), ("Kelvin TO 3/2 (control)", 1.5), ("fair die mu_f", MUF)):
    g = twist(corners(m_), (1, 1, 1), math.pi/3); o = twist(corners(m_), (0, 0, 1), math.pi/4)
    print(f"  {name:26s} 60 deg about a 3-fold axis: {'convex' if g else 'dented'};  45 deg about a 4-fold axis: {'convex' if o else 'dented'}")
    R[f'twist {name}'] = (g, o)
    if name.startswith('cubo'): C("control: CO turned 60 deg is convex (the anticuboctahedron J27)", g)
    if name.startswith('Kelvin'): C("control: Kelvin TO turned 60 deg is dented (Concordance)", not g)
json.dump(R, open(os.path.join(HERE, '..', 'data', 's03-space.json'), 'w'), indent=1, default=str)
C.final()
