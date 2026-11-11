# axis_shapes.py (from mirror_track.py), DICTO 11 Nov 2026 ("any truncated triangles"): per level k, the DOWN face on a three-fold and a
# five-fold axis (if any): sides, side lengths, long/short ratio, all angles equal? (truncated triangle = 6 sides alternating, angles 120;
# truncated pentagon = 10 sides alternating, angles 144); and the UP face there = polar of D_k's corner on the axis: its sides = the
# corner's degree, its shape from the polar polygon of the corner's face normals. Original header:
# mirror_track.py, DICTO 11 Nov 2026 ("track the mirror faces to level 37"). Float companion of certified_orbit.py (same orbit storage,
# exact point labels by separation, face classes by exact point keys, non-flat groups re-split), without ball arithmetic. Per level k:
# faces n, mirror faces M (class stabiliser of order 2 in I_h), axis faces, mu = (M + axis)/n, largest and mean mirror cap (deg), mean cap
# of all faces, size ratio (mean solid angle all / mirror), the §38 bound 15 sin(2 gamma_M) ratio + 62/n, and the death shares at hop k
# (generic classes g, mirror classes) from the next hull. Controls: solid angles add to 4 pi; class sizes 120/stabiliser add to n;
# mu <= bound.
# usage: python -u axis_shapes.py <five-fold-octet dir> <K0> <KMAX> <out.json>
import sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__)); ARGS = list(sys.argv)
sys.argv = [ARGS[0], ARGS[1], ARGS[2], ARGS[3], '/dev/null', '/tmp/mirror-track-unused-ck']
src = open(os.path.join(here, 'certified_orbit.py')).read().split('# ---------------- level K0')[0]
exec(src)
OUTJ = os.path.abspath(ARGS[4])
def sa_cap(P):
    U = P / np.linalg.norm(P, axis=1)[:, None]; c = U.mean(0); c /= np.linalg.norm(c); om = 0.0
    for a, b in zip(U, np.roll(U, -1, 0)):
        om += 2 * np.arctan2(np.dot(c, np.cross(a, b)), 1 + c @ a + c @ b + a @ b)
    return abs(om), float(np.arccos(np.clip(U @ c, -1, 1)).max())
W = [tuple(cv(x) for x in v) for v in OG]
for k in range(K0):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W])
    F_, ne, _ = exact_faces(W, idx, Wfx); feet = {}
    for n_, d_, _ in F_.values():
        s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
    W = list(feet)
Wf = np.array([fl(v) for v in W]); rows = []; ok = True; prev = None
for k in range(K0, KMAX + 2):
    t = time.time(); N = len(Wf)
    pm = perm_maps(Wf, f'D_{k} points')
    mems, Nf = hull_faces(Wf); F = len(mems)
    memb = np.concatenate(mems); offs = np.concatenate([[0], np.cumsum([len(m) for m in mems])[:-1]])
    wt = np.random.default_rng(k).integers(1, 2 ** 62, N, dtype=np.uint64)
    fkey = np.add.reduceat(wt[memb], offs); order_ = np.argsort(fkey); sk = fkey[order_]
    fm = np.empty((120, F), np.int32)
    for g in range(120):
        kg = np.add.reduceat(wt[pm[g][memb]], offs); pos = np.searchsorted(sk, kg); pos[pos >= F] = 0
        if not (sk[pos] == kg).all(): fail(f'D_{k}: face set not closed under I_h')
        fm[g] = order_[pos]
    orbit_min = fm.min(0); reps = np.unique(orbit_min); R = len(reps); ridx = {int(r): i for i, r in enumerate(reps)}
    rep_of = np.array([ridx[int(x)] for x in orbit_min]); gof = -np.ones(F, np.int64)
    for g in range(120):
        img = fm[g][reps[rep_of]]; hit = (img == np.arange(F)) & (gof < 0); gof[hit] = g
    stab = np.array([int((fm[:, r] == r).sum()) for r in reps]); csize = 120 // stab
    ok &= int(csize.sum()) == F
    # this level's faces are the candidates of hop k; their deaths: read at the next level (prev holds hop k-1 data)
    if prev is not None:
        pr, pcs, pstab = prev                                               # hop k-1: candidate j of D_{k-1} = point j of D_k
        corner = np.zeros(N, bool); corner[np.unique(memb)] = True          # points of D_k that are corners
        dies_rep = np.array([not corner[int(np.where(pr == i)[0][0])] for i in range(len(pcs))])
        gen = pstab == 1; mir = pstab == 2
        rows[-1].update(cut_share=float((pcs * dies_rep).sum() / pcs.sum()), g=float(dies_rep[gen].mean()) if gen.any() else None,
                        mirror_die=float(dies_rep[mir].mean()) if mir.any() else None)
        r_ = rows[-1]
        print(f"      hop {k - 1}: cut share {r_['cut_share']:.3f} | generic classes dying {r_['g'] if r_['g'] is None else round(r_['g'], 3)} | mirror classes dying {r_['mirror_die'] if r_['mirror_die'] is None else round(r_['mirror_die'], 3)}", flush=True)
    if k == KMAX + 1: break
    om = np.zeros(R); cap = np.zeros(R); footf = np.zeros((R, 3))
    for i, r in enumerate(reps):
        mm = np.array(sorted(mems[r])); P = Wf[mm]; P = P[polygon_order(P)]
        om[i], cap[i] = sa_cap(P)
        c0 = P.mean(0); nrm = np.linalg.svd(P - c0)[2][2]
        if nrm @ c0 < 0: nrm = -nrm
        footf[i] = (nrm @ c0) * nrm
        st = np.where(fm[:, r] == r)[0]                                      # 11-11 (D_34): pin the foot point to its stabiliser exactly
        footf[i] = np.mean([FULLF[g] @ footf[i] for g in st], axis=0)       # (float drift off a mirror plane doubled points 2e-11 apart)
    tot = float((om * csize).sum()); ok &= abs(tot - 4 * np.pi) < 1e-6
    for order, sides_t in ((3, 6), (5, 10)):
        ax_ = None
        for g in range(60):
            M_ = FULLF[g]
            if abs(np.trace(M_) - (1 + 2 * np.cos(2 * np.pi / order))) < 1e-9:
                w_, v_ = np.linalg.eig(M_); ax_ = np.real(v_[:, np.argmin(abs(w_ - 1))]); ax_ /= np.linalg.norm(ax_); break
        # DOWN: face with normal along the axis
        j = int(np.argmax(Nf @ ax_)); down = '-'
        if Nf[j] @ ax_ > 1 - 1e-9:
            P = Wf[np.array(sorted(mems[j]))]; P = P[polygon_order(P)]; L = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1)
            e1 = np.roll(P, -1, 0) - P; e0 = P - np.roll(P, 1, 0)
            ang = np.degrees(np.arccos(np.clip((-e0 * e1).sum(1) / (np.linalg.norm(e0, axis=1) * np.linalg.norm(e1, axis=1)), -1, 1)))
            alt = len(P) == sides_t and np.allclose(L[0::2], L[0], rtol=1e-6) and np.allclose(L[1::2], L[1], rtol=1e-6) and abs(L[0] - L[1]) > 1e-9
            down = f'{len(P)}-gon' + (f' TRUNCATED (long/short {max(L[0], L[1]) / min(L[0], L[1]):.6f}, angles {ang.min():.3f}-{ang.max():.3f})' if alt else ('' if len(P) != sides_t else ' (equal sides)'))
        else:
            # corner on the axis?
            dd = np.abs(Wf @ ax_ - np.linalg.norm(Wf, axis=1)); pidx = int(np.argmin(dd))
            if dd[pidx] < 1e-9 and pidx in set(np.concatenate([np.array(sorted(m)) for m in mems]).tolist()): down = 'corner'
            else: down = 'edge/other'
        # UP: the up face on the axis = polar of D_k's corner on the axis (if a corner): normals of the faces at that corner
        up = '-'
        dd = np.abs(Wf @ ax_ - np.linalg.norm(Wf, axis=1)); pidx = int(np.argmin(dd))
        if dd[pidx] < 1e-9:
            fa = [jj for jj, m in enumerate(mems) if pidx in set(m)]
            if fa:
                # polar face: points n_f / d_f for faces at the corner, in the plane x . p = 1
                pts = []
                for jj in fa:
                    mm = np.array(sorted(mems[jj])); c0 = Wf[mm].mean(0); nrm = Nf[jj]; dist = nrm @ c0; pts.append(nrm / dist)
                Pp = np.array(pts); Pp = Pp[polygon_order(Pp)]; L = np.linalg.norm(np.roll(Pp, -1, 0) - Pp, axis=1)
                alt = len(Pp) == sides_t and np.allclose(L[0::2], L[0], rtol=1e-6) and np.allclose(L[1::2], L[1], rtol=1e-6) and abs(L[0] - L[1]) > 1e-9 * L.max()
                up = f'{len(Pp)}-gon' + (f' TRUNCATED (long/short {max(L[0], L[1]) / min(L[0], L[1]):.6f})' if alt else '')
        print(f'      AXIS {order}-fold at D_{k}: down {down} | up {up}', flush=True)
    mir = stab == 2; ax = stab > 2; M = int(csize[mir].sum()); A = int(csize[ax].sum()); mu = (M + A) / F
    gM = float(cap[mir].max()) if mir.any() else 0.0; ratio = float((4 * np.pi / F) / om[mir].mean()) if mir.any() else 0.0
    bound = 15 * np.sin(min(2 * gM, np.pi / 2)) * ratio + 62 / F; ok &= mu <= bound + 1e-12
    meancap = float((cap * csize).sum() / F)
    rows.append(dict(k=k, n=F, mirror=M, axis=A, mu=mu, gamma_M_deg=float(np.degrees(gM)), mean_mirror_cap_deg=float(np.degrees(cap[mir].mean())) if mir.any() else None,
                     mean_cap_deg=float(np.degrees(meancap)), size_ratio=ratio, bound=float(bound), M_over_sqrt_n=M / F ** .5))
    print(f'PROGRESS {(k - K0 + 1) / (KMAX - K0 + 2):.3f} level {k}', flush=True)
    print(f'k {k:2d}: n {F:8d} mirror {M:6d} axis {A:3d} | mu {mu:.4f} | M/sqrt(n) {M / F ** .5:.1f} | gamma_M {np.degrees(gM):6.3f} deg, mean mirror cap {rows[-1]["mean_mirror_cap_deg"]:.3f}, mean cap {np.degrees(meancap):.3f} | size ratio {ratio:.3f} | bound {bound:.3f} ({time.time() - t:.0f} s)', flush=True)
    prev = (rep_of.copy(), csize.copy(), stab.copy())
    Wf = np.einsum('pij,pj->pi', FULLF[gof], footf[rep_of])
    json.dump(rows, open(OUTJ, 'w'), indent=1)
json.dump(rows, open(OUTJ, 'w'), indent=1)
print('levels where the §38 bound alone proves mu < 1/4:', [r['k'] for r in rows if r['bound'] < .25])
print('FINAL ok' if ok else 'FINAL FAIL: solid angles, class sizes or mu > bound')
