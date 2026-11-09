# DICTO 9 Nov ("make it so"): is the equality t_min(D_3) = 3/phi^2 a Hopscotch TURN value? Turn Theorem: at the turn every face
# touches one sphere and t_min = (R/r)^2. Exact Q(sqrt5): for D_0..D_5 list the distinct squared face distances (n.p)^2/|n|^2,
# the distinct squared corner radii, (R/r)^2, (R/H)^2, and which corner/face pair attains t_min(D_3) (against D_4's faces).
import sys, os, math
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exact_family.py')).read()
sys.argv = [sys.argv[0], sys.argv[1], '0', '/dev/null']; exec(src.split("t0 = time.time()")[0])
W = [tuple(cv(x) for x in v) for v in OG]; L = {}
for k in range(6):
    idx = {v: i for i, v in enumerate(W)}; Wf = np.array([fl(v) for v in W])
    F, ne, _ = exact_faces(W, idx, Wf)
    fd = sorted(set(((d * d) / dot(n, n)) for n, d, _ in F.values()), key=lambda x: x.f())
    cr = sorted(set(dot(v, v) for v in W), key=lambda x: x.f())
    corners = set(j for mem in F for j in mem); crc = sorted(set(dot(W[j], W[j]) for j in corners), key=lambda x: x.f())
    R2, r2, H2 = crc[-1], fd[0], fd[-1]
    L[k] = (W, F)
    print(f'D_{k}: faces {len(F)} corners {len(corners)}; distinct face distances^2 {len(fd)}: ' + ', '.join(f'{x.f():.6f}' for x in fd[:6]) +
          f'; corner radii^2 {len(crc)}: ' + ', '.join(f'{x.f():.6f}' for x in crc[:6]))
    print(f'   (R/r)^2 = {(R2 / r2).f():.9f} = {R2 / r2!r}   (R/H)^2 = {(R2 / H2).f():.9f}   all faces tangent: {len(fd) == 1}', flush=True)
    feet = {}
    for n, d, _ in F.values():
        s = d / dot(n, n); feet[tuple(s * x for x in n)] = 1
    W = list(feet)
T = TARGET; print(f'3/phi^2 = {T.f():.9f}')
for k in (2, 3, 4):
    Wk, _ = L[k]; _, F1 = L[k + 1]
    best = max(((dot(n, v) / d, i, n, d) for n, d, isrep in F1.values() if isrep for i, v in enumerate(Wk)), key=lambda x: x[0].f())
    t, i, n, d = best; v = Wk[i]
    print(f't_min(D_{k}) = {t.f():.9f} {t!r}: corner |v|^2 = {dot(v, v).f():.6f}, face dist^2 of D_{k+1} = {((d * d) / dot(n, n)).f():.6f}, '
          f'angle(v, n) = {math.degrees(math.acos(min(1, dot(n, v).f() / (dot(n, n).f() * dot(v, v).f()) ** .5))):.4f} deg, ratio^2 |v|^2/dist^2 = {(dot(v, v) * dot(n, n) / (d * d)).f():.9f}')
print('FINAL ok' if max(((dot(n, v) / d) for n, d, isrep in L[4][1].values() if isrep for v in L[3][0]), key=lambda x: x.f()) == TARGET else 'FINAL FAIL: t_min(D_3) != 3/phi^2')
