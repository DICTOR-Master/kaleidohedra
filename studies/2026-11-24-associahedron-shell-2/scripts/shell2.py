#!/usr/bin/env python3
"""The associahedron shell, part 2 (24 Nov 2026), exact. LEAD 1 of study 2026-11-24-associahedron-shell.

Two divisions of the shell Asso_c minus P, and their overlay:
  I (inner, equal-speed, the straight skeleton from P outward; as in the first study):
      piece_I(R) = {x in Asso_c : d_R(x) >= 0, d_R(x) >= d_R'(x) for every removed R'},  d = signed Euclidean distance to the plane.
  O (outer, nearest associahedron face; the straight skeleton of Asso_c inward):
      cell(A) = {x in Asso_c : D_A(x) <= D_A'(x) for every face A' of Asso_c},  D_A(x) = distance from x to the plane of A.
      piece_O(A) = cell(A) minus the interior of P. Its outer end is the whole shell part of A (flat).
  I ^ O (overlay, the common refinement): piece(R, A) = piece_I(R) intersected with cell(A); convex.
Labels: ("R", r) inner face (removed face r of P), ("F", a) associahedron face a (outer), ("W", r') wall of rule I,
("O", a') wall of rule O. Arithmetic: the exact tower fields of scripts/shell.py of the first study (imported unchanged).
Usage: shell2.py A3 B3 H3 -> data/shell2-<type>.json; log on stdout; FINAL ok only if every exact check passed.
Optional: --c <part of the c name> restricts to one Coxeter element (pilots).
"""
import sys, os, json, time, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../2026-11-24-associahedron-shell/scripts"))
from shell import *          # Tower, F_, setup, unit_scale, Poly, box, clip, volume, area_vec, dot, ... (unchanged)
# the import also brings shell.py's own HERE and OUT (the first study's folders): recompute ours afterwards, and guard it
HERE2 = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE2, "../data")
assert os.path.basename(os.path.dirname(HERE2)) == "2026-11-24-associahedron-shell-2", "output folder"

# ---- geometry: copied from run() of the first study's shell.py (up to the associahedron), as a generator over c
def geometry(typ):
    t0 = time.time()
    T, K, mir, a, name, sqrts, rho = setup(typ)
    N = len(mir)
    mir = [m if K.sign(dot(K, m, a)) > 0 else vneg(K, m) for m in mir]
    R = [refl(K, m) for m in mir]
    I = tuple(tuple(K.one if i == j else K.zero for j in range(3)) for i in range(3))
    def length(A):
        b = apply(K, A, a); return sum(1 for m in mir if K.sign(dot(K, m, b)) < 0)
    simple = [k for k in range(N) if length(R[k]) == 1]
    assert len(simple) == 3
    S0 = [R[k] for k in simple]; al0 = [mir[k] for k in simple]
    def order(A):
        B = A
        for o in range(1, 13):
            if B == I: return o
            B = mmul(K, B, A)
        raise AssertionError
    m0 = [[order(mmul(K, S0[i], S0[j])) if i != j else 1 for j in range(3)] for i in range(3)]
    mid = [i for i in range(3) if all(m0[i][j] > 2 for j in range(3) if j != i)][0]
    ends = sorted([i for i in range(3) if i != mid], key=lambda i: -m0[i][mid])
    perm = [ends[0], mid, ends[1]]
    S = [S0[i] for i in perm]; al = [al0[i] for i in perm]
    M = [[order(mmul(K, S[i], S[j])) if i != j else 1 for j in range(3)] for i in range(3)]
    # the group
    W = {I: I}; fr = [I]
    while fr:
        nf = []
        for A in fr:
            for s in S:
                B = mmul(K, A, s)
                if B not in W: W[B] = B; nf.append(B)
        fr = nf
    W = list(W)
    assert len(W) == WORD[typ], len(W)
    pr(f"{typ} ({name}): |W| = {len(W)}, mirrors {N}, Coxeter matrix {M}, tower radicands {[K.s(r, k) for k, r in enumerate(T.R)]}")
    om = []
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        w = cross(K, al[j], al[k])
        if K.sign(dot(K, w, al[i])) < 0: w = vneg(K, w)
        om.append(w)
    Vp = [apply(K, A, a) for A in W]
    keyV = {v: i for i, v in enumerate(Vp)}
    assert len(keyV) == len(W)
    facets = {}; vfac = {}
    us = [unit_scale(K, om[i], typ, sqrts, rho) for i in range(3)]
    for A in W:
        v = apply(K, A, a)
        for i in range(3):
            n = apply(K, A, om[i])
            j, l = [x for x in range(3) if x != i]
            facets.setdefault(n, {"n": n, "b": dot(K, a, om[i]), "type": i, "sides": 2 * M[j][l], "u": us[i][0]})
            vfac.setdefault(keyV[v], set()).add(n)
    assert len(facets) == PERMF[typ]
    fkeys = sorted(facets, key=lambda k: (facets[k]["type"], [K.val(x) for x in k]))
    fid = {k: i for i, k in enumerate(fkeys)}
    pr(f"  facet types (sides): {[2 * M[[x for x in range(3) if x != i][0]][[x for x in range(3) if x != i][1]] for i in range(3)]}; |n|^2 = q^2 * {[us[i][1] for i in range(3)]}")
    # the permutahedron, exactly, by clipping a box
    Bx = 10 ** 4
    def build(keys):
        p = box(K, Bx)
        for k in keys:
            p = clip(p, facets[k]["n"], facets[k]["b"], ("F", fid[k]))
        assert not any(l[0] == "box" for l in p.faces), "box face survived"
        return p
    P = build(fkeys)
    assert len(P.verts) == len(W) and len(P.faces) == PERMF[typ]
    for k in fkeys:
        assert len(P.faces[("F", fid[k])][2]) == facets[k]["sides"]
    volP = volume(P)
    pr(f"  permutahedron: {len(P.verts)} vertices, {len(P.faces)} faces, volume {K.val(volP):.6f} (exact)")
    CW = {"s1 s2 s3 (linear)": [0, 1, 2], "s3 s2 s1 (linear, inverse)": [2, 1, 0],
          "s2 s1 s3 (bipartite)": [1, 0, 2], "s1 s3 s2 (bipartite, inverse)": [0, 2, 1]}
    for cname, cw in CW.items():
        word, A = [], I
        while length(A) < N:
            for s in cw:
                B = mmul(K, A, S[s])
                if length(B) > length(A): word.append(s); A = B
                if length(A) == N: break
        cls = {tuple(word)}; fr = [tuple(word)]
        while fr:
            nf = []
            for w in fr:
                for p in range(len(w) - 1):
                    if M[w[p]][w[p + 1]] == 2:
                        u = w[:p] + (w[p + 1], w[p]) + w[p + 2:]
                        if u not in cls: cls.add(u); nf.append(u)
            fr = nf
        sing = {}
        for w in cls:
            A = I; sing[A] = A
            for s in w: A = mmul(K, A, S[s]); sing[A] = A
        singV = {keyV[apply(K, A, a)] for A in sing}
        kept = set()
        for vi in singV: kept |= vfac[vi]
        removed = [k for k in fkeys if k not in kept]
        keptl = [k for k in fkeys if k in kept]
        assert len(kept) == 3 + N
        Asso = build(keptl)
        assert len(Asso.verts) == CATALAN[typ], len(Asso.verts)
        volA = volume(Asso)
        yield cname, dict(T=T, K=K, typ=typ, us=us, facets=facets, fkeys=fkeys, fid=fid, removed=removed, keptl=keptl, P=P, Asso=Asso, volP=volP, volA=volA, M=M)

# ---------------------------------------------------------------- classification
def edges_of(Q):
    ef = {}
    for lab, (_, _, cyc) in Q.faces.items():
        for i in range(len(cyc)):
            e = frozenset((cyc[i], cyc[(i + 1) % len(cyc)])); ef.setdefault(e, []).append(lab)
    return ef

def classify_convex(Q, inner, outer):
    """Q convex; inner, outer: predicates on face labels. Scutoid Frusta decisions (24 Nov): two disjoint ends, simple,
    every lateral face meets an end along an edge; Y-corner = vertex on neither end. Convex tier needs each end one flat face."""
    ef = edges_of(Q)
    deg = {}
    for e in ef:
        for v in e: deg[v] = deg.get(v, 0) + 1
    closed = all(len(l) == 2 for l in ef.values())
    simple = all(d == 3 for d in deg.values())
    euler = len(Q.verts) - len(ef) + len(Q.faces) == 2
    IN = [l for l in Q.faces if inner(l)]; OU = [l for l in Q.faces if outer(l)]
    lat = [l for l in Q.faces if not inner(l) and not outer(l)]
    Vin = {v for l in IN for v in Q.faces[l][2]}; Vout = {v for l in OU for v in Q.faces[l][2]}
    Y = [v for v in Q.verts if v not in Vin and v not in Vout]
    vlab = {v: [] for v in Q.verts}
    for l, (_, _, cyc) in Q.faces.items():
        for v in cyc: vlab[v].append(l)
    ykinds = sorted("".join(sorted(l[0] for l in vlab[v])) for v in Y)
    bnd_in = [(e, fl) for e, fl in ef.items() if sum(1 for l in fl if inner(l)) == 1]
    bnd_out = [(e, fl) for e, fl in ef.items() if sum(1 for l in fl if outer(l)) == 1]
    n = len(bnd_in); m = len(bnd_out)
    nb_in = sorted({str(l) for e, fl in bnd_in for l in fl if not inner(l)})
    nb_out = sorted({str(l) for e, fl in bnd_out for l in fl if not outer(l)})
    meets = all(any(l in fl and any(inner(x) or outer(x) for x in fl) for fl in ef.values()) for l in lat)
    disjoint = not (Vin & Vout)
    why = []
    if not IN: why.append("no inner end")
    if not OU: why.append("no outer end")
    if IN and OU and not disjoint: why.append("ends meet")
    if not meets: why.append("a lateral face meets no end")
    if not simple: why.append("not simple")
    k = len(Y)
    if why: tier = "not a scutoid frustum: " + ", ".join(why)
    elif len(IN) == 1 and len(OU) == 1:
        tier = "convex Scutoid Frustum" if k else "convex frustum"
    else:
        tier = "Scutoid Frustum (general tier)" if k else "frustum (general tier)"
    sf = f"SF {n}-{m}-{k}" if not why else None
    law = (k >= abs(n - m)) and ((k - n - m) % 2 == 0)
    return {"tier": tier, "SF": sf, "n": n, "m": m, "Y": k, "Y_kinds": ykinds, "law": law, "simple": simple,
            "closed": closed, "euler": euler, "inner_faces": len(IN), "outer_faces": len(OU), "lateral": len(lat),
            "neighbours_in": nb_in, "neighbours_out": nb_out, "neighbours_change": nb_in != nb_out,
            "ends_share_vertices": len(Vin & Vout), "V": len(Q.verts), "E": len(ef), "F": len(Q.faces), "_Y": Y}

def inside(K, Q, v):
    return all(K.sign(K.sub(dot(K, n, v), off)) <= 0 for (n, off, _) in Q.faces.values())

def classify_union(K, parts, internal, inner, outer):
    """A union of convex parts glued along their internal faces (labels for which internal(l) is True).
    Corners of the union = boundary points on >= 3 boundary planes with independent normals (exact). Y-corner = corner on no end."""
    planes = {}
    for Q in parts:
        for l, (n, off, _) in Q.faces.items():
            if not internal(l): planes[l] = (n, off)
    pts = {v for Q in parts for v in Q.verts}
    corners = {}
    for v in pts:
        labs = set()
        for Q in parts:
            if not inside(K, Q, v): continue
            for l, (n, off, _) in Q.faces.items():
                if not internal(l) and K.isz(K.sub(dot(K, n, v), off)): labs.add(l)
        L = sorted(labs, key=str)
        if any(not K.isz(det3(K, planes[a][0], planes[b][0], planes[c][0])) for a, b, c in itertools.combinations(L, 3)):
            corners[v] = L
    Y = [v for v, L in corners.items() if not any(inner(l) or outer(l) for l in L)]
    meet = [v for v, L in corners.items() if any(inner(l) for l in L) and any(outer(l) for l in L)]
    n_in = len({l for l in planes if inner(l)}); n_out = len({l for l in planes if outer(l)})
    return {"corners": len(corners), "Y": len(Y), "Y_kinds": sorted("".join(sorted(l[0] for l in corners[v])) for v in Y),
            "ends_share_corners": len(meet), "inner_faces": n_in, "outer_faces": n_out,
            "lateral_planes": len([l for l in planes if not inner(l) and not outer(l)])}

# ---------------------------------------------------------------- the three divisions
def divisions(G):
    K = G["K"]; facets = G["facets"]; fkeys = G["fkeys"]; fid = G["fid"]; P = G["P"]
    keptl = G["keptl"]; removed = list(G["removed"]); Asso = G["Asso"]
    shellvol = K.sub(volume(Asso), G["volP"])
    u = {k: facets[k]["u"] for k in fkeys}
    off = {k: facets[k]["b"] for k in fkeys}
    # inner pieces (equal-speed)
    PI = {}
    for k in removed:
        r = fid[k]; n = facets[k]["n"]; b = facets[k]["b"]
        Q = clip(Asso, vneg(K, n), K.neg(b), ("R", r)); assert Q is not None
        for k2 in removed:
            if k2 == k: continue
            nn = vsub(K, scal(K, u[k2], facets[k2]["n"]), scal(K, u[k], n))
            oo = K.sub(K.mul(u[k2], facets[k2]["b"]), K.mul(u[k], b))
            Q = clip(Q, nn, oo, ("W", fid[k2])); assert Q is not None, "empty inner piece"
        PI[r] = Q
    # outer cells (nearest associahedron face): D_A = u_A (B_A - n_A.x); D_A <= D_A'
    CO = {}
    for k in keptl:
        a = fid[k]; n = facets[k]["n"]; B = off[k]
        Q = Asso
        for k2 in keptl:
            if k2 == k: continue
            nn = vsub(K, scal(K, u[k2], facets[k2]["n"]), scal(K, u[k], n))
            oo = K.sub(K.mul(u[k2], off[k2]), K.mul(u[k], B))
            Q = clip(Q, nn, oo, ("O", fid[k2])); assert Q is not None, "empty outer cell"
        CO[a] = Q
    # overlay
    OV = {}
    for r, Q0 in PI.items():
        for a, C in CO.items():
            Q = Q0
            for l, (n, o, _) in C.faces.items():
                if l[0] != "O": continue
                Q = clip(Q, n, o, l)
                if Q is None: break
            if Q is not None: OV[(r, a)] = Q
    # ---- exact checks
    chk = {}
    chk["overlay volumes sum to the shell volume"] = K.isz(K.sub(sum_(K, [volume(Q) for Q in OV.values()]), shellvol))
    chk["outer cells sum to vol(Asso)"] = K.isz(K.sub(sum_(K, [volume(C) for C in CO.values()]), volume(Asso)))
    chk["inner pieces sum to the shell volume"] = K.isz(K.sub(sum_(K, [volume(Q) for Q in PI.values()]), shellvol))
    chk["per removed face: overlay sums to its inner piece"] = all(
        K.isz(K.sub(sum_(K, [volume(Q) for (r2, a), Q in OV.items() if r2 == r]), volume(PI[r]))) for r in PI)
    ok_a = True
    for a, C in CO.items():
        CP = C
        for k in fkeys:
            CP = clip(CP, facets[k]["n"], facets[k]["b"], ("P", fid[k]))
            if CP is None: break
        vin = volume(CP) if CP is not None else K.zero
        s = sum_(K, [volume(Q) for (r, a2), Q in OV.items() if a2 == a])
        ok_a &= K.isz(K.sub(s, K.sub(volume(C), vin)))
    chk["per associahedron face: overlay sums to vol(cell) - vol(cell meet P)"] = ok_a
    wall_ok = True
    for (r, a), Q in OV.items():
        for l, (_, _, cyc) in Q.faces.items():
            if l[0] == "W":
                o = OV.get((l[1], a)); o = o.faces.get(("W", r)) if o else None
            elif l[0] == "O":
                o = OV.get((r, l[1])); o = o.faces.get(("O", a)) if o else None
            else: continue
            if o is None or set(o[2]) != set(cyc): wall_ok = False
    chk["every wall matches its partner piece vertex for vertex"] = wall_ok
    in_ok = True
    for k in removed:
        r = fid[k]; nh = scal(K, u[k], facets[k]["n"])
        s = sum_(K, [dot(K, area_vec(Q, Q.faces[("R", r)][2]), nh) for (r2, a), Q in OV.items() if r2 == r and ("R", r) in Q.faces])
        in_ok &= K.isz(K.add(s, dot(K, area_vec(P, P.faces[("F", r)][2]), nh)))   # the piece's inner face points along -n
    chk["inner ends tile each removed face (areas)"] = in_ok
    out_ok = True
    for k in keptl:
        a = fid[k]; nh = scal(K, u[k], facets[k]["n"])
        aA = dot(K, area_vec(Asso, Asso.faces[("F", a)][2]), nh)
        aP = dot(K, area_vec(P, P.faces[("F", a)][2]), nh)
        s = sum_(K, [dot(K, area_vec(Q, Q.faces[("F", a)][2]), nh) for (r, a2), Q in OV.items() if a2 == a and ("F", a) in Q.faces])
        out_ok &= K.isz(K.sub(s, K.sub(aA, aP)))
    chk["outer ends tile each associahedron face minus its kept face (areas)"] = out_ok
    chk["every overlay piece closed, Euler 2"] = True
    chk["every Y-corner lies in the open shell"] = True
    inner = lambda l: l[0] == "R"; outer = lambda l: l[0] == "F"
    rows = []
    for (r, a), Q in OV.items():
        c = classify_convex(Q, inner, outer)
        if not (c["closed"] and c["euler"]): chk["every overlay piece closed, Euler 2"] = False
        for v in c.pop("_Y"):       # a Y-corner lies in the open shell: strictly outside P, strictly inside Asso_c (exact signs)
            outP = any(K.sign(K.sub(dot(K, facets[k]["n"], v), facets[k]["b"])) > 0 for k in fkeys)
            inA = all(K.sign(K.sub(dot(K, n, v), o)) < 0 for (n, o, _) in Asso.faces.values())
            if not (outP and inA): chk["every Y-corner lies in the open shell"] = False
        c.update({"R": r, "A": a, "R_sides": facets[fkeys[r]]["sides"], "volume": K.s(volume(Q)),
                  "verts_float": [[K.val(x) for x in v] for v in Q.verts],
                  "faces": {str(l): [list(Q.verts).index(v) for v in cyc] for l, (_, _, cyc) in Q.faces.items()}})
        rows.append(c)
    # O pieces as unions over r; I pieces as unions over a (cross-check against the first study)
    orows = []
    for a in CO:
        parts = [Q for (r, a2), Q in OV.items() if a2 == a]
        if not parts: continue
        c = classify_union(K, parts, lambda l: l[0] == "W", inner, outer); c["A"] = a; c["parts"] = len(parts)
        orows.append(c)
    irows = []
    for r in PI:
        parts = [Q for (r2, a), Q in OV.items() if r2 == r]
        c = classify_union(K, parts, lambda l: l[0] == "O", inner, outer); c["R"] = r; c["parts"] = len(parts)
        irows.append(c)
    return chk, rows, orows, irows, K.val(shellvol)

def summarise(rows, key="tier"):
    d = {}
    for w in rows: d[w[key]] = d.get(w[key], 0) + 1
    return d

def main():
    args = sys.argv[1:]; conly = None
    if args and args[0] == "--c": conly = args[1]; args = args[2:]
    todo = args or ["A3", "B3", "H3"]
    allok = True
    for i, typ in enumerate(todo):
        t0 = time.time(); res = {}
        for cname, G in geometry(typ):
            if conly and conly not in cname: continue
            chk, rows, orows, irows, sv = divisions(G)
            ok = all(chk.values()); allok &= ok
            pr(f"  c = {cname}: shell volume {sv:.6f}; overlay pieces {len(rows)} ({time.time() - t0:.0f} s)")
            for k, v in chk.items(): pr(f"    check: {k}: {v}")
            pr(f"    overlay tiers: {summarise(rows)}")
            sft = {}
            for w in rows:
                if w["SF"]:
                    key = (w["tier"], w["SF"], tuple(w["Y_kinds"]), w["neighbours_change"]); sft[key] = sft.get(key, 0) + 1
            for (t, s, yk, nc), cnt in sorted(sft.items(), key=lambda t: (t[0][0], t[0][1])):
                pr(f"      {cnt:3d} x {s}  ({t}; Y-corner wall kinds {list(yk)}; neighbours change {nc})")
            pr(f"    overlay pieces with a Y-corner (any tier): {sum(1 for w in rows if w['Y'])}; "
               f"law Y >= |n-m|, Y = n+m mod 2 holds for {sum(1 for w in rows if w['law'] and w['SF'])}/{sum(1 for w in rows if w['SF'])} pieces meeting the definition")
            pr(f"    overlay pieces failing the definition, by reason: {summarise([w for w in rows if not w['SF']])}")
            pr(f"    O pieces (nearest associahedron face, unions): {len(orows)}; with a Y-corner {sum(1 for w in orows if w['Y'])} "
               f"{sorted(w['Y_kinds'] for w in orows if w['Y'])}; ends share a corner in {sum(1 for w in orows if w['ends_share_corners'])}; "
               f"inner faces per piece {sorted(w['inner_faces'] for w in orows)}")
            pr(f"    I pieces (equal-speed, unions, cross-check with the first study): {len(irows)}; with a Y-corner {sum(1 for w in irows if w['Y'])}; "
               f"ends share a corner in {sum(1 for w in irows if w['ends_share_corners'])}")
            res[cname] = {"checks": chk, "overlay": rows, "O": orows, "I": irows, "shell_volume_float": sv}
        tag = "" if not conly else "-pilot"
        json.dump({"type": typ, "results": res, "secs": round(time.time() - t0, 1)},
                  open(os.path.join(OUT, f"shell2-{typ}{tag}.json"), "w"), indent=0, default=str)
        pr(f"{typ} done in {time.time() - t0:.1f} s")
        pr(f"PROGRESS {(i + 1) / len(todo):.2f} {typ}")
    pr("FINAL ok" if allok else "FINAL FAILED")

if __name__ == "__main__":
    main()
