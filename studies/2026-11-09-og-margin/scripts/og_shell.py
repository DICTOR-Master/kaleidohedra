# og_shell.py, DICTO 11 Nov 2026 ("measure the shell thickness too"): thickness of the shell between D_k and D_{k+1} along rays.
# rho_k(u) = distance from O to the boundary of D_k in direction u = min over faces (m, d) with m.u > 0 of d/(m.u).
# (1) unscaled shell: rho_{k+1}(u) - rho_k(u) (both signs); (2) gnomon shell of the grown family S_k = phi^k D_k (#43 Cor. 1):
# phi^{k+1} rho_{k+1}(u) - phi^k rho_k(u) >= 0, reported relative to phi^k rho_k(u) (scale-free: phi rho_{k+1}/rho_k - 1).
# Directions: 20 000 quasi-uniform (Fibonacci sphere), plus the 5-, 3-, 2-fold axes. Control: thickness (2) >= 0 (Cor. 1), and
# rho at a corner direction equals that corner's distance.
import sys, os, json, numpy as np
here = '/home/dicto/k-research/studies/2026-11-09-og-margin/scripts'
src = open(here + '/og_sweep.py').read().split('rows_out = []')[0]
KM = int(sys.argv[2]); OUTJ = os.path.abspath(sys.argv[3])
sys.argv = ['x', sys.argv[1], '0', '/dev/null']; exec(src)
PHI = (1 + 5 ** .5) / 2
N = 20000; i = np.arange(N) + .5; z = 1 - 2 * i / N; th = np.pi * (1 + 5 ** .5) * i
U = np.stack([np.sqrt(1 - z * z) * np.cos(th), np.sqrt(1 - z * z) * np.sin(th), z], 1)
ax5 = OGf[np.argmax(np.linalg.norm(OGf, axis=1))]          # placeholder; axes found from the group below
def axes(order):
    out = []
    for g in Gf:
        w, v = np.linalg.eig(g); tr = np.trace(g)
        ang = np.arccos(np.clip((tr - 1) / 2, -1, 1))
        if abs(ang - 2 * np.pi / order) < 1e-6:
            a = np.real(v[:, np.argmin(abs(w - 1))]); out.append(a / np.linalg.norm(a))
    return out[0]
AX = {'5-fold': axes(5), '3-fold': axes(3), '2-fold': axes(2)}
def rho(M, Dd, dirs):
    P = dirs @ M.T; P = np.where(P > 1e-12, P, np.nan)
    return np.nanmin(Dd[None, :] / P, axis=1)
rows = []; ok = True
V = OGf; FF = faces(V)
M, Dd, cor = FF
for k in range(KM + 1):
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2 = FN
    r0, r1 = rho(M, Dd, U), rho(M2, D2, U)
    a0 = {n: rho(M, Dd, a[None])[0] for n, a in AX.items()}; a1 = {n: rho(M2, D2, a[None])[0] for n, a in AX.items()}
    un = r1 - r0; gn = PHI * r1 / r0 - 1
    V0 = V[cor] if len(cor) else V; c = V0[np.argmax(np.linalg.norm(V0, axis=1))]   # control: corner direction
    ctl = abs(rho(M, Dd, (c / np.linalg.norm(c))[None])[0] - np.linalg.norm(c)) < 1e-9
    ok &= ctl and gn.min() > -1e-9
    row = dict(k=k, unscaled_min=float(un.min() / r0.mean()), unscaled_max=float(un.max() / r0.mean()), unscaled_mean=float(un.mean() / r0.mean()),
               inward_share=float((un < -1e-12).mean()), gnomon_min=float(gn.min()), gnomon_mean=float(gn.mean()), gnomon_max=float(gn.max()),
               gnomon_axes={n: float(PHI * a1[n] / a0[n] - 1) for n in AX})
    rows.append(row)
    print(f"k {k:2d}->{k + 1:2d}: unscaled shell (rel. to mean radius) min {row['unscaled_min']:+.4f} mean {row['unscaled_mean']:+.4f} max {row['unscaled_max']:+.4f}, "
          f"new solid inside old on {100 * row['inward_share']:.1f}% of rays | gnomon shell (rel.) min {row['gnomon_min']:.4f} mean {row['gnomon_mean']:.4f} max {row['gnomon_max']:.4f} "
          f"| on axes 5f {row['gnomon_axes']['5-fold']:.4f} 3f {row['gnomon_axes']['3-fold']:.4f} 2f {row['gnomon_axes']['2-fold']:.4f}", flush=True)
    V, FF = W, FN; M, Dd, cor = FN
json.dump(rows, open(OUTJ, 'w'), indent=1)
print('FINAL ok' if ok else 'FINAL FAIL: a control failed (corner radius or gnomon shell negative)')
