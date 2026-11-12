"""Viewpoint (DICTO 11-08: could perspective/tilt/position make a more perfect construction fit all conditions?). The projective
maps that keep the yantra's circle as a circle and keep the vertical axis are the hyperbolic translations of Klein's model along the
axis: in the unit disc (y up) T_beta(x, y) = (x sqrt(1 - beta^2)/(1 + beta y), (y + beta)/(1 + beta y)). They keep lines straight
and every concurrency (18 marmas, 24 sandhis, 43 triangles), every level base level, every corner on the circle; the slopes go
u -> lambda*u, v -> v/lambda, lambda = sqrt((1 + beta)/(1 - beta)) (u v invariant). Take the DICTO Yantra (Cleo-Octangula: u = 2/phi^2, v = 1/sqrt2, t1 and t9 corners on
the circle), find beta that centres the bindu's incircle, and check everything in the image directly from its lines."""
import json, mpmath as mp, itertools
mp.mp.dps = 50
K = json.load(open('../figures/kites.json'))['K1'] if __import__('os').path.exists('../figures/kites.json') else json.load(open('kites.json'))['K1']
g = lambda d: {int(k): mp.mpf(v['a']) for k, v in d.items()}
b, w, a = g(K['b']), g(K['w']), g(K['apex'])
def disc(p): x, d = p; return (2 * x, 1 - 2 * d)                 # depth/diameter-1 -> unit disc, y up
def T(p, be): x, y = p; return (x * mp.sqrt(1 - be**2) / (1 + be * y), (y + be) / (1 + be * y))
def tri(be):
    out = {}
    for i in range(1, 10):
        L, R, A = T(disc((-w[i], b[i])), be), T(disc((w[i], b[i])), be), T(disc((0, a[i])), be)
        out[i] = (L, R, A)
    return out
def incircle_centre_y(tr):   # bindu: lines of t1's legs and t5's base (as in Kulaichev's (d))
    (L1, R1, A1) = tr[1]; (L5, R5, A5) = tr[5]
    def meet(p, q, r, s):
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p, q, r, s; den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        return (((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den, ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den)
    P1 = meet(L1, A1, L5, R5); P2 = meet(R1, A1, L5, R5); P3 = A1                       # bindu corners
    la, lb, lc = [mp.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2) for p, q in ((P2, P3), (P3, P1), (P1, P2))]
    return (la * P1[1] + lb * P2[1] + lc * P3[1]) / (la + lb + lc), (la * P1[0] + lb * P2[0] + lc * P3[0]) / (la + lb + lc)
be = mp.findroot(lambda be: incircle_centre_y(tri(be))[0], mp.mpf('0.02'))
tr = tri(be); lam = mp.sqrt((1 + be) / (1 - be))
slope = lambda L, A: abs(L[0] / (L[1] - A[1]))
u2 = slope(tr[7][0], tr[7][2]); v2 = slope(tr[3][0], tr[3][2])
on_circle = {i: max(abs(p[0]**2 + p[1]**2 - 1) for p in tr[i][:2]) for i in (1, 3, 7, 9)}
print(f'beta = {mp.nstr(be, 20)}  (lambda = {mp.nstr(lam, 15)})')
print(f'slopes after the viewpoint: upper u = {mp.nstr(u2, 15)} (was 2/phi^2 = 0.763932), lower v = {mp.nstr(v2, 15)} (was 1/sqrt2 = 0.707107); u v = {mp.nstr(u2 * v2, 12)} (before {mp.nstr((2 / ((1 + mp.sqrt(5)) / 2)**2) / mp.sqrt(2), 12)})')
print('corners on the circle (residual):', {i: mp.nstr(r, 3) for i, r in on_circle.items()})
print('bindu incircle centre:', [mp.nstr(c, 3) for c in incircle_centre_y(tr)])
# write the image as a yantra file (depth/diameter-1 frame) for the counts and the figure
s = lambda x: {'a': mp.nstr(x, 40)}; dep = lambda y: (1 - y) / 2
img = {'V1': {'b': {str(i): s(dep(tr[i][0][1])) for i in tr}, 'w': {str(i): s(abs(tr[i][0][0]) / 2) for i in tr}, 'apex': {str(i): s(dep(tr[i][2][1])) for i in tr}, 'beta': mp.nstr(be, 30)}}
json.dump(img, open('../figures/viewpoint.json', 'w'), indent=1)
ok = max(on_circle.values()) < mp.mpf(10)**-35 and abs(incircle_centre_y(tr)[0]) < mp.mpf(10)**-35   # input data carry 40 digits
print('FINAL ok' if ok else 'FINAL FAIL viewpoint')
