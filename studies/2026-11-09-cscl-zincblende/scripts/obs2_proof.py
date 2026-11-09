# #53 Observation 2 (CsCl and zinc blende), proved exactly.
#
# Units of #53 (Table 1): CsCl  big = 2Z^3 (kind A, weight lam), small = 2Z^3 + (1,1,1) (kind B, weight 0);
#                         ZnS   Zn  = 2D3 = {2k : k in Z^3, k1+k2+k3 even} (A, weight lam), S = 2D3 + (1,1,1) (B, weight 0).
# Range (-3, 3); s = (3 + lam)/2.
#
# What is checked (all exact; floats only order polygon corners and size a search radius, with margin):
#  C1  known-case sanity: S0/SA of yesterday's fluorite circuit = -1/8, of the CsCl and ZnS flip circuits = -1, +1.
#  C2  the four cells (big, small, Zn, S) on each of the three intervals are exactly the polytopes cut out by the nearest unlike and
#      nearest like sites only (8 + 6 in CsCl, 4 + 12 in ZnS): every triple of their planes has constant feasibility on the open
#      interval (so the corner set is constant there), and every other site within a proved-safe radius is satisfied at every
#      corner at both closed ends (slacks affine in lam). Hence cell = polytope on the whole interval.
#  C3  the symmetries used: small cell = (1,1,1) + P_big(-lam); S cell = (1,1,1) - P_Zn(-lam).
#  C4  LEMMA (homothety): the ZnS unlike face between Zn 0 and S (1,1,1) equals s(1,1,1) - 2 F, F the CsCl unlike face between big 0
#      and small (1,1,1), on every interval (corner sets equal as affine functions of lam). F = {x1+x2+x3 = s, 0 <= xi <= 1}.
#  C5  every face area and cell volume equals #53's census polynomial (relay census raw data), for every face of the four cells.
#  C6  the ratios of Observation 2 on every interval and for both kinds: unlike 4, like 1/sqrt2, volume 2.
#  C7  the two identities of the proof: dV/dlam = (+/-) sum over unlike faces of area/(2 d), and 3V = sum over faces of h * area
#      (h = distance from the site to the face plane); and V -> 0 at the end where the cell vanishes.
#  C8  cross-check with #53's own engine at sample lam: engine corners = our corners.
#  C9  the switch-theorem view: the flip circuits differ. The ZnS dual cells at lam = -1, +1 are centred at removed CsCl sites (so
#      their power spheres are not empty in CsCl); no CsCl dual cell at a flip lies inside the ZnS sites; scaling the CsCl sites by 2
#      moves its flips to -4, +4 (S0 scales by 4, SA does not).
import json, os, sys, math
from fractions import Fraction as Fr
from itertools import combinations, product
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
RELAY = os.path.join(HERE, "..", "..", "2026-10-25-relay-census")
SWITCH = os.path.join(HERE, "..", "..", "2026-11-08-switch-theorem")
sys.path.insert(0, os.path.join(RELAY, "scripts"))
LAM = sp.Symbol("lam")
checks = []


def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)


# ---------------------------------------------------------------- site sets
def in_2D3(v):
    return all(x % 2 == 0 for x in v) and (sum(v) // 2) % 2 == 0


def sites(net, R):
    out = []
    for v in product(range(-R, R + 1), repeat=3):
        if net == "cscl":
            if all(x % 2 == 0 for x in v): out.append(("A", v))
            elif all(x % 2 != 0 for x in v): out.append(("B", v))
        else:
            if in_2D3(v): out.append(("A", v))
            elif in_2D3(tuple(x - 1 for x in v)): out.append(("B", v))
    return out


def w(kind):  # weight as affine (c0, c1) in lam
    return (Fr(0), Fr(1)) if kind == "A" else (Fr(0), Fr(0))


def dot(a, b): return sum(Fr(x) * Fr(y) for x, y in zip(a, b))


def plane(c, kc, p, kp):
    """|x-c|^2 - w_c <= |x-p|^2 - w_p  <=>  n.x <= b(lam), n = 2(p-c), b = |p|^2 - |c|^2 + w_c - w_p (affine)."""
    n = tuple(2 * (Fr(pi) - Fr(ci)) for pi, ci in zip(p, c))
    wc, wp = w(kc), w(kp)
    b = (dot(p, p) - dot(c, c) + wc[0] - wp[0], wc[1] - wp[1])
    return n, b


def aff(a, l): return a[0] + a[1] * l


def solve3(N, B):
    """x = N^{-1} B with B a list of affine pairs; returns list of 3 affine pairs or None."""
    M = sp.Matrix([[sp.Rational(x) for x in row] for row in N])
    if M.det() == 0: return None
    Mi = M.inv()
    out = []
    for r in range(3):
        c0 = sum(Mi[r, k] * sp.Rational(B[k][0]) for k in range(3)); c1 = sum(Mi[r, k] * sp.Rational(B[k][1]) for k in range(3))
        out.append((Fr(int(sp.fraction(c0)[0]), int(sp.fraction(c0)[1])), Fr(int(sp.fraction(c1)[0]), int(sp.fraction(c1)[1]))))
    return out


def slack(n, b, X):  # b - n.x as affine pair
    return (b[0] - sum(n[r] * X[r][0] for r in range(3)), b[1] - sum(n[r] * X[r][1] for r in range(3)))


def polytope(H, lo, hi):
    """Corners of {n.x <= b(lam)} valid on the open interval (lo, hi). Returns (corners, ok): each corner = (X affine, tight set).
    ok: every triple's feasibility status and every tight set are constant on the open interval."""
    mid = (lo + hi) / 2; ok = True; corners = []
    for T in combinations(range(len(H)), 3):
        X = solve3([H[k][0] for k in T], [H[k][1] for k in T])
        if X is None: continue
        sl = [slack(n, b, X) for n, b in H]
        vals = [aff(s, mid) for s in sl]
        feas = all(v >= 0 for v in vals)
        for s, v in zip(sl, vals):
            a_lo, a_hi = aff(s, lo), aff(s, hi)
            if v == 0: ok &= (s == (0, 0))
            elif v > 0 and feas: ok &= (a_lo >= 0 and a_hi >= 0)
        if not feas:
            # stays infeasible on the open interval: some plane negative at mid stays negative inside (affine, <=0 at both ends)
            ok &= any(v < 0 and aff(s, lo) <= 0 and aff(s, hi) <= 0 for s, v in zip(sl, vals))
            continue
        tight = frozenset(k for k, s in enumerate(sl) if s == (0, 0))
        if not any(C[0] == X for C in corners):
            corners.append((X, tight))
    return corners, ok


def cell(net, kc, c, lo, hi, D2nb):
    S = sites(net, 9)
    near = [(k, p) for k, p in S if p != c and 0 < dot([a - b for a, b in zip(p, c)], [a - b for a, b in zip(p, c)]) <= D2nb[k == kc]]
    H = [plane(c, kc, p, kp) for kp, p in near]
    corners, ok = polytope(H, lo, hi)
    # all-site check with a proved-safe radius:  (|p-c| - R)^2 >= R^2 + max(w_p - w_c)  =>  site p cannot cut the cell
    R2 = max(float(sum((aff(X[r], l) - c[r]) ** 2 for r in range(3))) for X, _ in corners for l in (lo, hi))
    R = math.sqrt(R2); dw = float(max(abs(lo), abs(hi)))
    Rsafe = R + math.sqrt(R2 + dw) + 1e-6
    allok = True; nchk = 0
    for kp, p in S:
        if p == c: continue
        dv = [a - b for a, b in zip(p, c)]
        if math.sqrt(sum(x * x for x in dv)) > Rsafe: continue
        n, b = plane(c, kc, p, kp); nchk += 1
        for X, _ in corners:
            s = slack(n, b, X)
            allok &= aff(s, lo) >= 0 and aff(s, hi) >= 0
    assert max(abs(x) for x in c) + Rsafe < 9, "site box too small"
    return dict(H=H, near=near, corners=corners, ok=ok, allok=allok, nchk=nchk, Rsafe=Rsafe)


def sym(X): return sp.Matrix([sp.Rational(X[r][0]) + sp.Rational(X[r][1]) * LAM for r in range(3)])


def face_area(C, k, lo, hi):
    """Area polynomial of the face of cell C on plane k (sympy, with the sqrt of |n|^2)."""
    n, b = C["H"][k]
    pts = [X for X, t in C["corners"] if k in t]
    if len(pts) < 3: return None, pts
    mid = float((lo + hi) / 2)
    P = np.array([[float(aff(X[r], Fr(mid))) for r in range(3)] for X in pts]); cen = P.mean(0)
    nf = np.array([float(x) for x in n]); nf /= np.linalg.norm(nf)
    u = P[0] - cen; u /= np.linalg.norm(u); v = np.cross(nf, u)
    order = np.argsort(np.arctan2((P - cen) @ v, (P - cen) @ u)); pts = [pts[i] for i in order]
    if np.linalg.matrix_rank(P - cen, tol=1e-9) < 2: return None, pts
    S = [sym(X) for X in pts]; A = sp.zeros(3, 1)
    for q in range(len(S)): A += S[q].cross(S[(q + 1) % len(S)])
    nv = sp.Matrix([sp.Rational(x) for x in n])
    area = sp.expand(A.dot(nv) / 2) / sp.sqrt(nv.dot(nv))
    return sp.simplify(area), pts


def cell_data(C, c, lo, hi):
    faces = {}
    vol = 0
    for k in range(len(C["H"])):
        a, pts = face_area(C, k, lo, hi)
        if a is None or a == 0: continue
        n, b = C["H"][k]; nv = sp.Matrix([sp.Rational(x) for x in n])
        h = (sp.Rational(b[0]) + sp.Rational(b[1]) * LAM - nv.dot(sp.Matrix(c))) / sp.sqrt(nv.dot(nv))  # signed distance site->plane
        faces[k] = dict(area=a, h=sp.simplify(h), pts=pts)
        vol += h * a / 3
    return faces, sp.expand(sp.simplify(vol))


# ---------------------------------------------------------------- C1 sanity
def alpha(P):
    M = sp.Matrix([[sp.Rational(P[i][r]) for i in range(len(P))] for r in range(3)] + [[1] * len(P)])
    ns = M.nullspace(); assert len(ns) == 1; return list(ns[0])


def S0SA(circ):
    P = [tuple(sp.Rational(x) for x in p) for _, p in circ]; a = alpha(P)
    G = circ_G = None
    return a, P


def lam_star(circ, A, G=sp.eye(3)):
    P = [sp.Matrix([sp.Rational(x) for x in p]) for _, p in circ]
    a = alpha([list(p) for p in P])
    S0 = sum(ai * (p.T * G * p)[0] for ai, p in zip(a, P)); SA = sum(ai for ai, (k, _) in zip(a, circ) if k == A)
    return S0, SA, (S0 / SA if SA != 0 else None)


def main():
    circ = json.load(open(os.path.join(SWITCH, "data", "circuits-all.json")))
    dl = circ["delian"]["-1/8"]
    S0, SA, ls = lam_star(dl["circuit"], "tet", sp.eye(3) / 2)
    check("C1 sanity: fluorite octet circuit (switch-theorem study) S0/SA", ls == sp.Rational(-1, 8),
          f"S0 = {S0/SA}, SA = 1 after scaling alpha by 1/SA, lam* = {ls} (#53: octet switch -1/8; switch study: S0 = -1/8, SA = 1)")
    for key, A in (("bcc", "big"), ("zincblende", "Zn")):
        for lv in ("-1", "1"):
            S0, SA, ls = lam_star(circ[key][lv]["circuit"], A)
            check(f"C1 sanity: {key} flip circuit at {lv}", ls == sp.Rational(lv), f"S0 = {S0}, SA = {SA}, lam* = {ls} (#53 flips -1, 1)")

    census = {k: json.load(open(os.path.join(RELAY, "data", "raw", k + ".json"))) for k in ("bcc", "zincblende")}
    IV = [(Fr(-3), Fr(-1)), (Fr(-1), Fr(1)), (Fr(1), Fr(3))]
    one = (1, 1, 1)
    D2nb = {"cscl": {False: 3, True: 4}, "zb": {False: 3, True: 8}}   # [like?] -> squared distance of the nearest of that kind
    res = {}
    out = {"intervals": []}
    for lo, hi in IV:
        s = (3 + LAM) / 2
        R = {}
        for net in ("cscl", "zb"):
            for kc, c in (("A", (0, 0, 0)), ("B", one)):
                C = cell(net, kc, c, lo, hi, D2nb[net])
                nb = len(C["near"])
                check(f"C2 {net} {kc} cell on ({lo}, {hi}): {len(C['corners'])} corners from the {nb} nearest planes, constant on the open "
                      f"interval; {C['nchk']} sites within the safe radius {C['Rsafe']:.3f} all satisfied", C["ok"] and C["allok"])
                faces, vol = cell_data(C, c, lo, hi)
                R[(net, kc)] = (C, faces, vol)
        # C4 homothety of the unlike faces
        def unlike_face(net):
            C, faces, _ = R[(net, "A")]
            k = next(k for k, (kp, p) in enumerate(C["near"]) if p == one)
            return sorted((tuple(sp.expand(e) for e in sym(X)) for X in faces[k]["pts"]), key=str), faces[k]["area"]
        Fc, ac = unlike_face("cscl"); Fz, az = unlike_face("zb")
        img = sorted((tuple(sp.expand(s - 2 * e) for e in v) for v in Fc), key=str)
        check(f"C4 LEMMA on ({lo}, {hi}): ZnS unlike face = s(1,1,1) - 2 * CsCl unlike face", img == Fz,
              f"{len(Fc)} corners; CsCl face corners {[[str(e) for e in v] for v in Fc]}")
        cube_ok = all(sp.simplify(sum(v) - s) == 0 for v in Fc) and all(
            sp.simplify(e.subs(LAM, (lo + hi) / 2)) >= 0 and sp.simplify(e.subs(LAM, (lo + hi) / 2)) <= 1 for v in Fc for e in v)
        check(f"C4 on ({lo}, {hi}): the CsCl unlike face is the slice x1+x2+x3 = s of the unit cube [0,1]^3", cube_ok)
        # C5 census, C6 ratios, C7 identities
        ivrec = dict(lo=str(lo), hi=str(hi))
        for net, key in (("cscl", "bcc"), ("zb", "zincblende")):
            civ = next(iv for iv in census[key]["intervals"] if Fr(iv["lo"]) == lo)
            for kc, mi in (("A", 0), ("B", 1 if key == "bcc" else 4)):
                C, faces, vol = R[(net, kc)]
                cs = civ["sites"][mi]
                okv = sp.simplify(vol - sp.sympify(cs["volume"], locals={"lam": LAM})) == 0
                cen_a2 = set(sp.expand(sp.sympify(x, locals={"lam": LAM})) for o in cs["orbit_area2"].values() for x in o)
                our_a2 = set(sp.expand(f["area"] ** 2) for f in faces.values())
                check(f"C5 {key} {cs['kind']} on ({lo}, {hi}): volume {vol} and the {len(faces)} face areas = census "
                      f"({cs['faces']} faces)", okv and our_a2 == cen_a2 and len(faces) == cs["faces"])
        for kc in ("A", "B"):
            (Cc, fc, vc), (Cz, fz, vz) = R[("cscl", kc)], R[("zb", kc)]
            def split(C, faces):
                un, li = [], []
                for k, f in faces.items():
                    (un if C["near"][k][0] != kc else li).append(f)
                return un, li
            uc, lc = split(Cc, fc); uz, lz = split(Cz, fz)
            r_un = set(sp.simplify(fz_["area"] / f["area"]) for fz_ in uz for f in uc)
            r_li = set(sp.simplify(fz_["area"] / f["area"]) for fz_ in lz for f in lc) if lc and lz else set()
            r_v = sp.simplify(vz / vc)
            okr = r_un == {4} and r_v == 2 and (r_li == {1 / sp.sqrt(2)} or (not lc and not lz))
            check(f"C6 ratios ZnS/CsCl, kind {kc}, ({lo}, {hi}): unlike {r_un}, like {r_li or 'no like faces in either'}, volume {r_v}",
                  okr, f"face counts CsCl {len(uc)}+{len(lc)}, ZnS {len(uz)}+{len(lz)}")
            for net, faces, vol, un in (("cscl", fc, vc, uc), ("zb", fz, vz, uz)):
                sg = 1 if kc == "A" else -1
                dV = sp.simplify(sp.diff(vol, LAM) - sg * sum(f["area"] for f in un) / (2 * sp.sqrt(3)))
                pyr = sp.simplify(3 * vol - sum(f["h"] * f["area"] for f in faces.values()))
                check(f"C7 {net} {kc} ({lo}, {hi}): dV/dlam = {'+' if sg > 0 else '-'}sum(unlike area)/(2 sqrt3) and 3V = sum h*area",
                      dV == 0 and pyr == 0)
            ivrec[kc] = dict(vol_cscl=str(vc), vol_zb=str(vz), unlike_cscl=str(uc[0]["area"]), unlike_zb=str(uz[0]["area"]),
                             like_cscl=str(lc[0]["area"]) if lc else None, like_zb=str(lz[0]["area"]) if lz else None,
                             faces_cscl=f"{len(uc)}+{len(lc)}", faces_zb=f"{len(uz)}+{len(lz)}")
        ivrec["unlike_face_cscl_corners"] = [[str(e) for e in v] for v in Fc]
        ivrec["unlike_face_zb_corners"] = [[str(e) for e in v] for v in Fz]
        out["intervals"].append(ivrec)
        res[(lo, hi)] = R
    # C3 symmetries: the B cell on (lo, hi) is the A cell on (-hi, -lo) with lam -> -lam, moved to (1,1,1) (+ in CsCl, - in ZnS)
    def cornerset(C, f):
        return sorted((tuple(sp.expand(e) for e in f(sym(X))) for X, _ in C["corners"]), key=str)
    sub = lambda M: M.subs(LAM, -LAM)
    for lo, hi in IV:
        for net, sign in (("cscl", 1), ("zb", -1)):
            Cb, Ca = res[(lo, hi)][(net, "B")][0], res[(-hi, -lo)][(net, "A")][0]
            lhs = cornerset(Cb, lambda M: M)
            rhs = cornerset(Ca, lambda M: sp.Matrix(one) + sign * sub(M))
            check(f"C3 {net}: B cell on ({lo}, {hi}) = (1,1,1) {'+' if sign > 0 else '-'} A cell(-lam) of ({-hi}, {-lo})", lhs == rhs)
    # C7b: the A volume vanishes at lam = -3 (s = 0) in both, so V_zb = 2 V_cscl follows from the derivative identity alone
    for net in ("cscl", "zb"):
        v = res[(Fr(-3), Fr(-1))][(net, "A")][2]
        check(f"C7 {net}: A volume -> 0 at lam = -3; B volume -> 0 at lam = 3", v.subs(LAM, -3) == 0 and
              res[(Fr(1), Fr(3))][(net, "B")][2].subs(LAM, 3) == 0)
    # C8 engine cross-check
    from engine import Net, Cell  # noqa
    from networks import NETS  # noqa
    for key, net in (("bcc", "cscl"), ("zincblende", "zb")):
        spec = NETS[key]; N = Net(spec["name"], spec["G"], spec["T"], spec["motif"], spec["w"])
        for lv in (Fr(-5, 2), Fr(-2), Fr(-1, 3), Fr(0), Fr(1, 2), Fr(2), Fr(11, 4)):
            iv = next((lo, hi) for lo, hi in IV if lo < lv < hi)
            for kc, c in (("A", (0, 0, 0)), ("B", one)):
                i = next(i for i, (k, p) in enumerate(N.motif) if tuple(p) == tuple(Fr(x) for x in c))
                E = Cell(N, i, (lv,), spec["D2"])
                eng = sorted(tuple(x) for x in (cc["p0"] for cc in E.corners))
                ours = sorted(tuple(aff(X[r], lv) for r in range(3)) for X, _ in res[iv][(net, kc)][0]["corners"])
                check(f"C8 {key} {kc} at lam = {lv}: #53 engine corners = ours ({len(ours)})", eng == ours)
    # C9 switch-theorem view of the flips
    for lv in ("-1", "1"):
        cz = circ["zincblende"][lv]; v = tuple(Fr(x) for x in cz["vertex"])
        removed = "small" if all(x.denominator == 1 and x % 2 != 0 for x in v) else ("big" if all(x.denominator == 1 and x % 2 == 0 for x in v) else None)
        inZnS = in_2D3(tuple(int(x) for x in v)) or in_2D3(tuple(int(x) - 1 for x in v)) if removed else None
        pw = Fr(cz["power"])
        own = -Fr(lv) if removed == "big" else Fr(0)   # power of the removed CsCl site at its own position
        check(f"C9 ZnS dual cell at lam = {lv}: centre {tuple(str(x) for x in v)} is a CsCl {removed} site not in ZnS; its CsCl power "
              f"{own} < sphere power {pw}, so the ZnS empty sphere is not empty in CsCl", removed is not None and inZnS is False and own < pw)
    # CsCl dual cells at the flips: the sites at minimal power around each corner of the big and small cells
    allS = sites("cscl", 9)
    for lv in (Fr(-1), Fr(1)):
        bad = 0; ncell = 0
        for kc, c in (("A", (0, 0, 0)), ("B", one)):
            C = cell("cscl", kc, c, Fr(-1), Fr(1), D2nb["cscl"])
            for X, _ in C["corners"]:
                x = [aff(X[r], lv) for r in range(3)]
                pw = {p: sum((xi - pi) ** 2 for xi, pi in zip(x, p)) - (lv if k == "A" else 0) for k, p in allS}
                m = min(pw.values()); D = [p for p, q in pw.items() if q == m]; ncell += 1
                if all(in_2D3(p) or in_2D3(tuple(a - 1 for a in p)) for p in D): bad += 1
        check(f"C9 CsCl at lam = {lv}: none of the {ncell} dual cells around the big and small cell corners lies inside the ZnS sites", bad == 0)
    for lv in ("-1", "1"):
        cb = circ["bcc"][lv]["circuit"]
        S0, SA, ls = lam_star([(k, tuple(2 * Fr(x) for x in p)) for k, p in cb], "big")
        check(f"C9 CsCl flip circuit at {lv} scaled by 2: lam* = {ls} (= 4 x {lv}), not a flip of ZnS", ls == 4 * sp.Rational(lv))
    json.dump(out, open(os.path.join(HERE, "..", "data", "obs2.json"), "w"), indent=1)
    with open(os.path.join(HERE, "..", "data", "obs2-checks.txt"), "w") as fh:
        for s_, n, det in checks: fh.write(f"{s_} {n} {det}\n")
    nf = sum(1 for c in checks if c[0] == "FAIL")
    print(f"{len(checks) - nf}/{len(checks)} PASS")
    print('FINAL ok' if checks and nf == 0 else f'FINAL FAIL: {nf} of {len(checks)} checks failed')


if __name__ == "__main__":
    main()
