# Figure 1 of "Fair Dice — The Aequi": the polar picture of Theorem A, drawn in the plane.
# Left: a polygon P = {x : n_k.x <= d_k}; the rays from the centre that meet edge k fill an angle (shaded).
# Right: its polar P° = conv{n_k/d_k}; the outer normals at the corner n_k/d_k fill the same angle (shaded).
# The figure checks this: the two angles are computed separately and must agree (printed, and asserted).
# Standard library only. Writes ../figures/fig-polar.svg.
import math, os
ANG = [0, 68, 140, 205, 282]          # face normal directions in degrees (an irregular pentagon)
DEP = [1.0, 1.25, 0.9, 1.15, 0.95]    # depths d_k
K = 0                                  # the face shown
n = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in ANG]
N = len(n)
def meet(i, j):                        # corner of P where the lines of faces i and j meet
    (a, b), (c, d) = n[i], n[j]; det = a * d - b * c
    return ((DEP[i] * d - b * DEP[j]) / det, (a * DEP[j] - c * DEP[i]) / det)
P = [meet(k, (k + 1) % N) for k in range(N)]                  # corner k lies between faces k and k+1
Q = [(n[k][0] / DEP[k], n[k][1] / DEP[k]) for k in range(N)]  # polar corners
for k in range(N):                                            # each polar corner is a corner (convex position)
    a, b, c = Q[k - 1], Q[k], Q[(k + 1) % N]
    assert (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) > 0
ang = lambda p: math.atan2(p[1], p[0])
def span(u, v):
    d = (ang(v) - ang(u)) % (2 * math.pi); return d
# angle of the rays meeting edge K: from corner K-1 to corner K of P
t_face = span(P[K - 1], P[K])
# normal cone of P° at Q[K]: between the outer normals of edges (K-1,K) and (K,K+1)
def outer(a, b):
    ex, ey = b[0] - a[0], b[1] - a[1]; return (ey, -ex)
u1, u2 = outer(Q[K - 1], Q[K]), outer(Q[K], Q[(K + 1) % N])
t_cone = span(u1, u2)
assert abs(t_face - t_cone) < 1e-12, (t_face, t_cone)
print(f'angle subtended by face {K}: {math.degrees(t_face):.9f} deg; normal angle at the polar corner: {math.degrees(t_cone):.9f} deg')

S = 95.0                                   # px per unit
W, H = 760, 330
def tr(p, cx, cy, s=None): s = s or S; return (cx + s * p[0], cy - s * p[1])
def poly(pts, cx, cy, s=None): return ' '.join(f'{x:.2f},{y:.2f}' for x, y in (tr(p, cx, cy, s) for p in pts))
SLATE, SAND, INK, GREY = '#4f6480', '#d8c49a', '#222', '#888'
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="DejaVu Sans, sans-serif" font-size="13">',
       f'<rect width="{W}" height="{H}" fill="#fff"/>']
# left panel
cx, cy = 190, 170
out.append(f'<polygon points="{poly([(0, 0), P[K - 1], P[K]], cx, cy)}" fill="{SAND}" stroke="none"/>')
out.append(f'<polygon points="{poly(P, cx, cy)}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
a, b = tr(P[K - 1], cx, cy), tr(P[K], cx, cy)
out.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{SLATE}" stroke-width="4"/>')
for p in (P[K - 1], P[K]):
    q = tr(p, cx, cy); out.append(f'<line x1="{cx}" y1="{cy}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" stroke="{GREY}" stroke-width="1" stroke-dasharray="4 3"/>')
out.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{INK}"/>')
m = ((P[K - 1][0] + P[K][0]) / 2, (P[K - 1][1] + P[K][1]) / 2); q = tr(m, cx, cy)
out.append(f'<text x="{q[0] + 10:.1f}" y="{q[1] + 4:.1f}" fill="{SLATE}">face k</text>')
out.append(f'<text x="{cx - 8}" y="{cy + 22}" fill="{INK}">0</text>')
out.append(f'<text x="{cx - 150}" y="24" fill="{INK}">P = {{x : n·x ≤ d for each face}}</text>')
out.append(f'<text x="{cx - 150}" y="{H - 12}" fill="{INK}">shaded: the rays from 0 that meet face k</text>')
# right panel
cx, cy = 510, 170
S2 = 125.0
c = tr(Q[K], cx, cy, S2)
r = 0.8
p1 = (Q[K][0] + r * u1[0] / math.hypot(*u1), Q[K][1] + r * u1[1] / math.hypot(*u1))
p2 = (Q[K][0] + r * u2[0] / math.hypot(*u2), Q[K][1] + r * u2[1] / math.hypot(*u2))
out.append(f'<polygon points="{poly([Q[K], p1, p2], cx, cy, S2)}" fill="{SAND}" stroke="none"/>')
for p in (p1, p2):
    q = tr(p, cx, cy, S2); out.append(f'<line x1="{c[0]:.2f}" y1="{c[1]:.2f}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" stroke="{GREY}" stroke-width="1" stroke-dasharray="4 3"/>')
out.append(f'<polygon points="{poly(Q, cx, cy, S2)}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
out.append(f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="5" fill="{SLATE}"/>')
out.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{INK}"/>')
out.append(f'<text x="{cx - 8}" y="{cy + 22}" fill="{INK}">0</text>')
out.append(f'<text x="{c[0] - 30:.1f}" y="{c[1] + 52:.1f}" fill="{SLATE}">n/d of face k</text>')
out.append(f'<text x="{cx - 120}" y="24" fill="{INK}">P° = hull of the points n/d</text>')
out.append(f'<text x="{cx - 120}" y="{H - 12}" fill="{INK}">shaded: the outer normals at that corner</text>')
out.append('</svg>')
here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here, '..', 'figures', 'fig-polar.svg'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('fig-polar.svg written; FINAL ok')
