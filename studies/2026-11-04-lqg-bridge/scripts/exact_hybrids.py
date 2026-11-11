"""Exact Dehn (exact_dehn.py) for: Covenant (must be 0), the RD/TRD half-cell (0), the twisted cube (0: it tiles with the brick), and the two
Narcissus + half-RD hybrids (turn 0° and 60°). Corners converted to lattice coordinates (u, v, z) and snapped to fractions with denominator <= 72."""
import math, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
exec(open('scripts/exact_dehn.py').read().split("if __name__")[0])
exec(open('~/study-runs/2026-11-04-dehn-screen/scripts/halfcell.py').read().split('print("RD"')[0])
s3 = math.sqrt(3)
def to_lat(p):
    u = p[0] - p[1]/s3; v = 2*p[1]/s3; z = p[2]/Hh
    out = []
    for x in (u, v, z):
        f = Fr(x).limit_denominator(72); assert abs(float(f) - x) < 1e-7, (x, f); out.append(f)
    return tuple(out)
N = np.array([[0,0,0],[0,1/s3,-Hh/2],[0,1/s3,0],[.5,-1/(2*s3),-Hh/2],[.5,-1/(2*s3),0],[.5,1/(2*s3),-Hh],[.5,s3/2,0],[1,0,0],[1,1/s3,-Hh/2],[1,1/s3,0]])
cN = np.array([.5, 1/(2*s3), 0]); Nc = N - cN
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
T = half(RD, True); B = half(RD, False)
cases = {
 'Covenant (N + N turned 60°)': np.vstack([Nc, (Nc*np.array([1, 1, -1])) @ rz(math.pi/3).T]),
 'twisted cube (N + N straight)': np.vstack([Nc, Nc*np.array([1, 1, -1])]),
 'RD/TRD half-cell': B,
 'hybrid N + half-RD, turn 0°': np.vstack([Nc, T]),
 'hybrid N + half-RD, turn 60°': np.vstack([Nc, T @ rz(math.pi/3).T]),
 'Narcissus alone': Nc,
}
for name, P in cases.items():
    P = P[ConvexHull(P).vertices] + cN   # back to the frame where hexagon corners are lattice points
    L = [to_lat(p) for p in P]; S = exact_dehn(L); z = all(v == 0 for v in S.values())
    print(f"{name:32s}: {'ZERO' if z else 'NONZERO ' + str({d: str(v) for d, v in S.items() if v != 0})}")
