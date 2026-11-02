# Linear-elastic lattice mechanics of the Knitted HexOct (DICTO proposed) for c/h stacking sequences.
# Members: circular rods r = 0.05 a, E_s = 1, nu = 0.3, length a = 1. Joints: pin (bars) or rigid (3D Euler-Bernoulli frame).
# Variants: links  = inter-sheet links only (no in-sheet members; every node keeps its 3+3 links)
#           stiff  = links + in-sheet triangular members 100x stiffer (sheets nearly rigid in-plane and in bending)
#           full   = links + in-sheet members of the same rod (= nearest-neighbour network: 3C = octet truss, 2H = hcp truss)
#           sheet<f> = links + in-sheet members f times as stiff as the links (axial and bending), for the sheet-stiffness sweep
# Usage: mech.py <task> <out.json>   task = periodic:<seq>:<joint>:<variant> | block:<seq>:<joint>:<variant> | rigidity:<seq>
#        | energy:<seq>:<variant>
import sys, json, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spl
from lattice import build, word_from_labels, SEQ_LABELS, PERIODIC_WORDS, D, check
R = 0.05; ES = 1.0; NU = 0.3; GS = ES / (2 * (1 + NU))
AREA = np.pi * R ** 2; I2 = np.pi * R ** 4 / 4; J = 2 * I2
PCR = np.pi ** 2 * ES * I2  # pinned Euler load, L = 1
VOIGT = ['xx', 'yy', 'zz', 'yz', 'xz', 'xy']

def Bmat(Dv, comps):
    """3 x len(comps): displacement E.D for unit Voigt strain components (engineering shears)."""
    Dx, Dy, Dz = Dv; col = {'xx': (Dx, 0, 0), 'yy': (0, Dy, 0), 'zz': (0, 0, Dz),
                            'yz': (0, Dz / 2, Dy / 2), 'xz': (Dz / 2, 0, Dx / 2), 'xy': (Dy / 2, Dx / 2, 0)}
    return np.array([col[c] for c in comps]).T

def frame_local(E, A, Iy, Iz, G, Jt, L=1.0):
    k = np.zeros((12, 12))
    def put(i, j, v): k[i, j] += v; (k.__setitem__((j, i), k[j, i] + v) if i != j else None)
    a = E * A / L; put(0, 0, a); put(6, 6, a); put(0, 6, -a)
    t = G * Jt / L; put(3, 3, t); put(9, 9, t); put(3, 9, -t)
    for (v, th, s, EI) in [(1, 5, 1, E * Iz), (2, 4, -1, E * Iy)]:  # v-bending (about z), w-bending (about y)
        c1, c2, c3, c4 = 12 * EI / L ** 3, 6 * EI / L ** 2, 4 * EI / L, 2 * EI / L
        put(v, v, c1); put(v + 6, v + 6, c1); put(v, v + 6, -c1)
        put(v, th, s * c2); put(v, th + 6, s * c2); put(v + 6, th, -s * c2); put(v + 6, th + 6, -s * c2)
        put(th, th, c3); put(th + 6, th + 6, c3); put(th, th + 6, c4)
    return k

def rot(n):
    ref = np.array([0, 0, 1.0]) if abs(n[2]) < 0.9 else np.array([1.0, 0, 0])
    y = np.cross(ref, n); y /= np.linalg.norm(y); z = np.cross(n, y)
    return np.array([n, y, z])

class Model:
    def __init__(self, lat, joint, variant, comps):
        self.lat, self.joint, self.variant, self.comps = lat, joint, variant, comps
        X = lat['X']; self.nn = len(X); self.nd = 3 if joint == 'pin' else 6
        self.ne = len(comps); self.ndof = self.nd * self.nn + self.ne
        self.mem = [m for m in lat['members'] if not (variant == 'links' and m[3] == 'sheet')]
        rows, cols, vals, mids = [], [], [], []
        self.g = []  # axial compatibility rows (dof index array, coefficient array)
        self.k_ax = []; self.pcr = []
        kl = None
        for mi, (a, b, s, kind) in enumerate(self.mem):
            fac = 1.0 if kind == 'link' else {'stiff': 100.0, 'full': 1.0}.get(variant, None)
            if fac is None: fac = float(variant[5:])  # variant 'sheet<f>': in-sheet members f x the link rod stiffness
            Dv = X[b] + s - X[a]; n = Dv / np.linalg.norm(Dv); B = Bmat(Dv, comps)
            ea = np.arange(self.nd) + self.nd * a; eb = np.arange(self.nd) + self.nd * b; ee = self.nd * self.nn + np.arange(self.ne)
            idx = np.concatenate([ea, eb, ee])
            # P maps [node a dofs, node b dofs, eps] -> element dofs [w_a, (th_a), w_b + B eps, (th_b)]
            P = np.zeros((2 * self.nd, 2 * self.nd + self.ne)); P[:, :2 * self.nd] = np.eye(2 * self.nd)
            P[self.nd:self.nd + 3, 2 * self.nd:] = B
            if joint == 'pin':
                g = np.concatenate([-n, n]) @ P; ke = fac * ES * AREA * np.outer(g, g)
            else:
                if kl is None: kl = frame_local(ES, AREA, I2, I2, GS, J)
                Rm = rot(n); T = np.kron(np.eye(4), Rm); ke = fac * (P.T @ (T.T @ kl @ T) @ P)
                g = np.concatenate([-n, np.zeros(3), n, np.zeros(3)]) @ P
            self.g.append((idx, g)); self.k_ax.append(fac * ES * AREA); self.pcr.append(fac * PCR)
            ii, jj = np.meshgrid(idx, idx, indexing='ij')
            rows.append(ii.ravel()); cols.append(jj.ravel()); vals.append(ke.ravel()); mids.append(np.full(ii.size, mi))
        self.rows, self.cols, self.vals, self.mids = map(np.concatenate, (rows, cols, vals, mids))
        self.k_ax = np.array(self.k_ax); self.pcr = np.array(self.pcr)
        Lx, Ly, Lz = lat['cell']; self.area = Lx * Ly; self.vol = self.area * lat['N'] * D
        self.rho = len(self.mem) * AREA / self.vol  # relative density (overlaps at nodes ignored)

    def K(self, active=None):
        if active is None: v, r, c = self.vals, self.rows, self.cols
        else:
            m = active[self.mids]; v, r, c = self.vals[m], self.rows[m], self.cols[m]
        return sps.coo_matrix((v, (r, c)), shape=(self.ndof, self.ndof)).tocsr()

    def solve(self, presc, active=None, K=None):
        """presc: dict dof -> value; all other dofs free with zero external force. Returns full displacement vector."""
        K = self.K(active) if K is None else K
        p = np.array(sorted(presc)); up = np.array([presc[i] for i in p])
        f = np.setdiff1d(np.arange(self.ndof), p)
        Kff = K[f][:, f]; lam = 1e-10 * (Kff.diagonal().mean() or 1.0)  # 'or': every member buckled -> K = 0
        Kff = Kff + lam * sps.identity(len(f))
        rhs = -(K[f][:, p] @ up) if len(p) else np.zeros(len(f))
        u = np.zeros(self.ndof); u[p] = up; u[f] = spl.spsolve(Kff.tocsc(), rhs)
        return u

    def ext(self, u):
        return np.array([g @ u[idx] for idx, g in self.g])

def node_dofs(M, nodes, comps_local):
    return [M.nd * n + c for n in nodes for c in comps_local]

def periodic_C(M):
    """effective Voigt stiffness (6x6) / E_s by condensing out the periodic fluctuations."""
    K = M.K().toarray(); nw = M.nd * M.nn; Kww = K[:nw, :nw]; Kwe = K[:nw, nw:]; Kee = K[nw:, nw:]
    lam = 1e-10 * np.mean(np.diag(Kww)); Kww = Kww + lam * np.eye(nw)
    C = (Kee - Kwe.T @ np.linalg.solve(Kww, Kwe)) / M.vol
    return 0.5 * (C + C.T)

def engineering(C):
    S = np.linalg.inv(C)
    return dict(E1=1 / S[0, 0], E2=1 / S[1, 1], E3=1 / S[2, 2], G23=1 / S[3, 3], G13=1 / S[4, 4], G12=1 / S[5, 5],
                nu12=-S[0, 1] / S[0, 0], nu13=-S[0, 2] / S[0, 0], nu31=-S[2, 0] / S[2, 2],
                C33=C[2, 2], C11=C[0, 0], C44=C[3, 3], C55=C[4, 4], C66=C[5, 5])

def block_tests(M):
    lat = M.lat; sh = lat['sheet']; N = lat['N']; bot = np.where(sh == 0)[0]; top = np.where(sh == N - 1)[0]
    H = (N - 1) * D; nw = M.nd * M.nn; eps = {c: nw + i for i, c in enumerate(M.comps)}
    rot_all = (lambda nodes: node_dofs(M, nodes, [3, 4, 5])) if M.nd == 6 else (lambda nodes: [])
    out = {}
    def bonded(disp):  # bottom clamped, top moved rigidly by disp (rotations held), eps = 0
        pr = {i: 0.0 for i in node_dofs(M, bot, [0, 1, 2]) + rot_all(bot) + rot_all(top) + list(eps.values())}
        for c in range(3):
            for i in node_dofs(M, top, [c]): pr[i] = disp[c]
        u = M.solve(pr); F = M.K() @ u
        return np.array([F[node_dofs(M, top, [c])].sum() for c in range(3)]) / M.area, u
    d = 1e-3
    s, _ = bonded((0, 0, -d)); out['C33_bonded'] = -s[2] / (d / H)
    s, _ = bonded((d, 0, 0)); out['G13_bonded'] = s[0] / (d / H)
    s, _ = bonded((0, d, 0)); out['G23_bonded'] = s[1] / (d / H)
    # lubricated compression: z prescribed on the faces, everything else free (one bottom node held in x, y)
    pr = {i: 0.0 for i in node_dofs(M, bot, [2])}; pr.update({i: -d for i in node_dofs(M, top, [2])})
    pr.update({i: 0.0 for i in node_dofs(M, bot[:1], [0, 1])})
    u = M.solve(pr); F = M.K() @ u; out['E3_free'] = -F[node_dofs(M, top, [2])].sum() / M.area / (d / H)
    # free transverse shear: faces held against relative sliding only in the shear direction; in-plane strain, top z,
    # other top in-plane direction and rotations free (bulk limit = 1/S55, 1/S44)
    for c, name in ((0, 'G13_free'), (1, 'G23_free')):
        pr = {i: 0.0 for i in node_dofs(M, bot, [0, 1, 2])}; pr.update({i: d for i in node_dofs(M, top, [c])})
        u = M.solve(pr); F = M.K() @ u; out[name] = F[node_dofs(M, top, [c])].sum() / M.area / (d / H)
    # in-plane: free plate, prescribed eps_xx (or eps_yy); other in-plane strains free; one node held
    for c in ('xx', 'yy'):
        pr = {eps[c]: d}; pr.update({i: 0.0 for i in node_dofs(M, [0], [0, 1, 2])})
        u = M.solve(pr); F = M.K() @ u; out['E1_inplane' if c == 'xx' else 'E2_inplane'] = F[eps[c]] / M.vol / d
    pr = {eps['xy']: d}; pr.update({i: 0.0 for i in node_dofs(M, [0], [0, 1, 2])})
    u = M.solve(pr); F = M.K() @ u; out['G12_inplane'] = F[eps['xy']] / M.vol / d
    return out

def rigidity(lat, comps):
    """pin-jointed counts from the compatibility matrix (dense SVD)."""
    M = Model(lat, 'pin', 'links' if lat.get('_links') else 'full', comps)
    Cm = np.zeros((len(M.g), M.ndof))
    for r, (idx, g) in enumerate(M.g): Cm[r, idx] += g
    sv = np.linalg.svd(Cm, compute_uv=False); tol = 1e-9 * sv[0]; rank_full = int((sv > tol).sum())
    nw = M.nd * M.nn; sw = np.linalg.svd(Cm[:, :nw], compute_uv=False); rank_w = int((sw > 1e-9 * sw[0]).sum())
    return dict(bars=len(M.g), nodes=M.nn, dof_w=nw, rank_w=rank_w, rank_with_strain=rank_full,
                mechanisms_w=nw - rank_w - 3, self_stress=len(M.g) - rank_w,
                soft_macro_strains=M.ne - (rank_full - rank_w), maxwell_bars_minus_3N=len(M.g) - 3 * M.nn)

def energy(M, mode, eps_end=0.05, max_events=50000):
    """event-to-event: struts buckle at the pinned Euler load and then carry it constant (elastic-perfectly-plastic in
    compression, elastic in tension). Bonded platens. Returns the stress-strain path and the work to eps_end."""
    lat = M.lat; sh = lat['sheet']; N = lat['N']; bot = np.where(sh == 0)[0]; top = np.where(sh == N - 1)[0]
    H = (N - 1) * D; c = {'compress': 2, 'compress_free': 2, 'shear13': 0, 'shear23': 1}[mode]
    sgn = -1.0 if mode.startswith('compress') else 1.0
    nw = M.nd * M.nn; epsd = list(range(nw, M.ndof))
    if mode == 'compress_free':  # lubricated platens, free lateral strain (one bottom node held in x, y)
        pr = {i: 0.0 for i in node_dofs(M, bot, [2]) + node_dofs(M, bot[:1], [0, 1])}
    else:                        # bonded platens, no lateral strain
        pr = {i: 0.0 for i in node_dofs(M, bot, [0, 1, 2]) + node_dofs(M, top, [0, 1, 2]) + epsd}
    for i in node_dofs(M, top, [c]): pr[i] = sgn * H  # unit macro strain rate
    topc = node_dofs(M, top, [c])
    active = np.ones(len(M.g), bool); F = np.zeros(len(M.g)); t = 0.0; sig = 0.0; path = [(0.0, 0.0)]; first = None
    G = sps.csr_matrix((np.concatenate([g for _, g in M.g]), (np.repeat(np.arange(len(M.g)), [len(g) for _, g in M.g]),
                        np.concatenate([idx for idx, _ in M.g]))), shape=(len(M.g), M.ndof))
    for ev in range(max_events):
        for _ in range(50):
            K = M.K(active); u = M.solve(pr, K=K); e = G @ u
            back = (~active) & (e > 1e-12 * np.abs(e).max())
            if not back.any(): break
            active[back] = True
        fr = np.where(active, M.k_ax * e, 0.0); dsig = sgn * (K @ u)[topc].sum() / M.area
        with np.errstate(divide='ignore', invalid='ignore'):
            dt = np.where(active & (fr < 0), (-M.pcr - F) / fr, np.inf)
        step = min(dt.min(), eps_end - t)
        F = F + fr * step; t += step; sig += dsig * step; path.append((t, sig))
        if t >= eps_end - 1e-15: break
        hit = active & (dt <= step * (1 + 1e-7) + 1e-15); active[hit] = False; F[hit] = -M.pcr[hit]
        if first is None: first = dict(strain=t, stress=sig, n_buckled=int(hit.sum()))
    path = np.array(path); W = np.trapezoid(path[:, 1], path[:, 0])
    return dict(first_buckling=first, work_to_end=W, eps_end=eps_end, events=ev + 1, path=path[::max(1, len(path) // 400)].tolist(),
                buckled_at_end=int((~active).sum()), stress_at_end=float(sig))

if __name__ == '__main__':
    task, outp = sys.argv[1], sys.argv[2]; parts = task.split(':'); kind = parts[0]; res = dict(task=task)
    if kind == 'periodic':
        seq, joint, var = parts[1:]; lat = build(PERIODIC_WORDS[seq], zper=True); check(lat)
        M = Model(lat, joint, var, VOIGT); C = periodic_C(M)
        res.update(rho=M.rho, C=C.tolist(), eng=engineering(C) if np.linalg.cond(C) < 1e12 else None,
                   eigC=np.linalg.eigvalsh(C).tolist())
    elif kind == 'block':
        seq, joint, var = parts[1:]; lat = build(word_from_labels(SEQ_LABELS[seq])); check(lat)
        M = Model(lat, joint, var, ['xx', 'yy', 'xy']); res.update(rho=M.rho, **block_tests(M))
    elif kind == 'blockL':  # block from an explicit c/h label string (10 labels, bottom to top)
        lab, joint, var = parts[1:]; lat = build(word_from_labels(lab)); check(lat)
        M = Model(lat, joint, var, ['xx', 'yy', 'xy']); res.update(rho=M.rho, labels=lab, **block_tests(M))
    elif kind == 'rigidity':
        seq, var = parts[1:]
        if seq in PERIODIC_WORDS:
            lat = build(PERIODIC_WORDS[seq], zper=True); lat['_links'] = var == 'links'; res['periodic'] = rigidity(lat, VOIGT)
        lat = build(word_from_labels(SEQ_LABELS[seq])); lat['_links'] = var == 'links'; res['block'] = rigidity(lat, ['xx', 'yy', 'xy'])
    elif kind == 'energy':
        seq, var, mode = parts[1:]; lat = build(word_from_labels(SEQ_LABELS[seq]))
        M = Model(lat, 'pin', var, ['xx', 'yy', 'xy']); res.update(rho=M.rho, **energy(M, mode))
    elif kind == 'size':  # cell-size check: periodic 3C/2H full pin with a 4 x 4 in-plane cell
        seq = parts[1]; lat = build(PERIODIC_WORDS[seq], nx=4, ny=4, zper=True)
        M = Model(lat, 'pin', 'full', VOIGT); res.update(rho=M.rho, eng=engineering(periodic_C(M)))
    json.dump(res, open(outp, 'w'), indent=1); print(task, 'done')
