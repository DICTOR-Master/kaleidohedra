"""Amber-Ammann study (21 Nov 2026), step 1: a finite patch of the 3D Penrose tiling by the two golden rhombohedra
(Ammann-Kramer-Neri tiling), exactly in Q(sqrt5), by cut-and-project from Z^6 (dualisation of the cubic complex).
Star: e_i = the six 5-fold vectors (0,1,phi),(0,-1,phi),(1,phi,0),(-1,phi,0),(phi,0,1),(-phi,0,1) (icosahedron vertices, one per axis;
the same axes as the solids of the amber-cell sweep). Perpendicular star: e_i' = Galois conjugate (sqrt5 -> -sqrt5).
Rule: the 3-face n + C_A (A a triple) is a tile iff gamma lies in the open parallelepiped pi'(n + 1_A/2) + sum_{b not in A} [-1/2,1/2] e_b'.
Checks (exact unless stated): sum e_i e_i'^T = 0 (parallel and perpendicular spaces orthogonal); no boundary tie for gamma; every face of the
patch used by 1 or 2 tiles, by 2 only from opposite sides; at every edge with all faces shared the dihedral angles sum to 360 deg (exact
cos^2 identification as multiples of 36 deg); volume of tiles = volume enclosed by the boundary surface; float solid-angle sum 4 pi at
every interior vertex. Writes ../data/patch.json.  Usage: python tiling.py RADIUS_IN_EDGES"""
import itertools, json, os, sys, time
from collections import Counter
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, os.environ.get("RESIN_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts")))
from resin import Q, PHI, dot, cross, vsub, vadd, vsc, det3
T0 = time.time()
def pr(*a): print(*a, flush=True)
def conj(x): return Q(x.a, -x.b)
def fl(v): return np.array([float(x) for x in v])
O, I = Q(0), Q(1)
E = [[O, I, PHI], [O, -I, PHI], [I, PHI, O], [-I, PHI, O], [PHI, O, I], [-PHI, O, I]]
EP = [[conj(x) for x in v] for v in E]
TRIPLES = list(itertools.combinations(range(6), 3))
def tvol(A): return det3(*[E[a] for a in A])
def absq(x): return x if x.sign() >= 0 else -x

def main():
    Rn = Fr(sys.argv[1]) if len(sys.argv) > 1 else Fr(7, 2)
    M = [[sum((E[i][r]*EP[i][c] for i in range(6)), O) for c in range(3)] for r in range(3)]
    assert all(x.sign() == 0 for row in M for x in row), "sum e e'^T = 0"
    G = [[sum((E[i][r]*E[i][c] for i in range(6)), O) for c in range(3)] for r in range(3)]
    pr(f"sum e_i e_i'^T = 0 (exact); sum e_i e_i^T = {G[0][0]} I; |e|^2 = {dot(E[0], E[0])}")
    vols = sorted({absq(tvol(A)).key(): absq(tvol(A)) for A in TRIPLES}.values(), key=float)
    assert len(vols) == 2
    vO, vP = vols
    kind = {A: ("P" if (absq(tvol(A)) - vP).sign() == 0 else "O") for A in TRIPLES}
    pr(f"volumes (edge |e|): prolate {vP} = {float(vP):.6f}, oblate {vO} = {float(vO):.6f}, ratio {vP/vO}; prolate triples {sum(k == 'P' for k in kind.values())}")
    fr = {A: absq(det3(*[EP[b] for b in range(6) if b not in A])) for A in TRIPLES}
    fP = sum((fr[A] for A in TRIPLES if kind[A] == "P"), O); fO = sum((fr[A] for A in TRIPLES if kind[A] == "O"), O)
    pr(f"window frequencies: prolate : oblate = {fP/fO} = {float(fP/fO):.9f} (phi = {float(PHI):.9f}); irrational: {(fP/fO).b != 0}")
    gamma = [Q(Fr(1234, 10007)), Q(Fr(-567, 10009)), Q(Fr(891, 10037))]
    edge = float(np.sqrt(float(dot(E[0], E[0]))))
    R = float(Rn)*edge
    Ef = np.array([fl(v) for v in E]); EPf = np.array([fl(v) for v in EP]); gf = fl(gamma)
    a2 = 2*float(dot(E[0], E[0])); b2 = 2*float(dot(EP[0], EP[0]))
    N = int(np.ceil(R*edge/a2 + (np.linalg.norm(gf) + 3*np.sqrt(b2/2))*np.sqrt(b2/2)/b2)) + 1
    N = int(os.environ.get("NBOX", N))
    pr(f"patch: tile centres within {Rn} edges = {R:.4f}; search box |n_i| <= {N}")
    rng = np.arange(-N, N+1)
    grid = np.array(np.meshgrid(*[rng]*6, indexing="ij")).reshape(6, -1).T
    par = grid @ Ef; per = grid @ EPf
    tiles = []
    for A in TRIPLES:
        Bc = [b for b in range(6) if b not in A]
        hA = np.zeros(6); hA[list(A)] = 0.5
        cpar = par + hA @ Ef; cper = per + hA @ EPf
        sel = np.linalg.norm(cpar, axis=1) <= R
        Minv = np.linalg.inv(EPf[Bc].T)
        t = (gf - cper[sel]) @ Minv.T
        ok = np.all(np.abs(t) < 0.5 + 1e-6, axis=1)
        for n in grid[sel][ok]:
            n = [int(x) for x in n]
            c6 = [Fr(n[i]) + (Fr(1, 2) if i in A else 0) for i in range(6)]
            p = [sum((EP[i][r]*c6[i] for i in range(6)), O) for r in range(3)]
            d = vsub(gamma, p)
            Mx = [EP[b] for b in Bc]; D = det3(*Mx)
            ts = [det3(*[d if q == k else Mx[q] for q in range(3)])/D for k in range(3)]
            for x in ts: assert (absq(x) - Fr(1, 2)).sign() != 0, "gamma on a window boundary"
            if all((absq(x) - Fr(1, 2)).sign() < 0 for x in ts):
                tiles.append(dict(n=n, A=list(A), kind=kind[A], c6=c6))
    pr(f"tiles selected: {len(tiles)}  (P {sum(t['kind']=='P' for t in tiles)}, O {sum(t['kind']=='O' for t in tiles)})  ({time.time()-T0:.1f}s)")
    def P3(v6): return [sum((E[i][r]*v6[i] for i in range(6)), O) for r in range(3)]
    faces = {}
    for ti, t in enumerate(tiles):
        n, A = t["n"], t["A"]
        for k in range(3):
            i, j = [A[q] for q in range(3) if q != k]; l = A[k]
            for side in (0, 1):
                base = list(n); base[l] += side
                pts = []
                for a, b in ((0, 0), (1, 0), (1, 1), (0, 1)):
                    v = list(base); v[i] += a; v[j] += b; pts.append(tuple(v))
                faces.setdefault(frozenset(pts), []).append((ti, i, j, l, 1 if side == 0 else -1, pts))
    bad = [f for f, L in faces.items() if len(L) > 2]
    opp = 0
    for f, L in faces.items():
        if len(L) == 2:
            (t1, i, j, l1, s1, _), (t2, i2, j2, l2, s2, _) = L
            d1 = det3(E[i], E[j], vsc(s1, E[l1])); d2 = det3(E[i], E[j], vsc(s2, E[l2]))
            if d1.sign()*d2.sign() >= 0: bad.append(f)
            else: opp += 1
    nb = sum(1 for L in faces.values() if len(L) == 1)
    pr(f"faces {len(faces)}: shared {opp} (all from opposite sides), boundary {nb}, bad {len(bad)}")
    def ident36(n1, n2):
        c = dot(n1, n2); c2 = c*c/(dot(n1, n1)*dot(n2, n2))
        if (c2 - PHI*PHI/4).sign() == 0: return 1 if c.sign() < 0 else 4   # interior angle = pi - angle between outward normals
        if (c2 - (PHI-1)*(PHI-1)/4).sign() == 0: return 2 if c.sign() < 0 else 3
        raise AssertionError("dihedral not a multiple of 36 deg")
    edges = {}
    for ti, t in enumerate(tiles):
        n, A = t["n"], t["A"]
        for k in range(3):
            l = A[k]; o1, o2 = [A[q] for q in range(3) if q != k]
            for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
                v = list(n); v[o1] += a; v[o2] += b; w = list(v); w[l] += 1
                d1 = E[o1] if a == 0 else vsc(-1, E[o1]); d2 = E[o2] if b == 0 else vsc(-1, E[o2])   # directions into the tile
                n1 = cross(E[l], E[o2]); n1 = n1 if dot(n1, d1).sign() < 0 else vsc(-1, n1)
                n2 = cross(E[l], E[o1]); n2 = n2 if dot(n2, d2).sign() < 0 else vsc(-1, n2)
                edges.setdefault(frozenset((tuple(v), tuple(w))), []).append(ident36(n1, n2))
    fac_by_edge = {}
    for f, L in faces.items():
        pts = L[0][5]
        for q in range(4): fac_by_edge.setdefault(frozenset((pts[q], pts[(q+1) % 4])), []).append(f)
    interior_e = [e for e in edges if all(len(faces[f]) == 2 for f in fac_by_edge[e])]
    bad_e = [e for e in interior_e if sum(edges[e]) != 10]
    pr(f"edges {len(edges)}: interior {len(interior_e)}, dihedral sum != 360 deg at {len(bad_e)}; dihedrals (x36 deg) used: {sorted(set(x for L in edges.values() for x in L))}")
    vt = sum((absq(tvol(t["A"])) for t in tiles), O)
    vb = O
    for f, L in faces.items():
        if len(L) != 1: continue
        ti, i, j, l, s, pts = L[0]
        X = [P3(p) for p in pts]
        nrm = cross(vsub(X[1], X[0]), vsub(X[3], X[0]))
        inward = vsc(s, E[l])
        sg = -1 if dot(nrm, inward).sign() > 0 else 1
        vb = vb + sg*(det3(X[0], X[1], X[2]) + det3(X[0], X[2], X[3]))
    vb = vb/6
    pr(f"volume: tiles {float(vt):.6f}, enclosed by boundary {float(vb):.6f}, difference {vt - vb} ({'exact 0' if (vt-vb).sign()==0 else 'NONZERO'})")
    vt_tiles = {}
    for ti, t in enumerate(tiles):
        n, A = t["n"], t["A"]
        for bits in itertools.product((0, 1), repeat=3):
            v = list(n)
            for q in range(3): v[A[q]] += bits[q]
            vt_tiles.setdefault(tuple(v), []).append((ti, bits))
    bverts = {p for f, L in faces.items() if len(L) == 1 for p in f}
    worst = 0
    for v, L in vt_tiles.items():
        if v in bverts: continue
        tot = 0
        for ti, bits in L:
            A = tiles[ti]["A"]
            a, b, c = [Ef[A[q]]*(1 if bits[q] == 0 else -1) for q in range(3)]
            a, b, c = a/np.linalg.norm(a), b/np.linalg.norm(b), c/np.linalg.norm(c)
            tot += 2*np.arctan2(abs(a @ np.cross(b, c)), 1 + a@b + b@c + c@a)
        worst = max(worst, abs(tot - 4*np.pi))
    nint = sum(1 for v in vt_tiles if v not in bverts)
    pr(f"vertices {len(vt_tiles)}: interior {nint}, max |solid angle sum - 4pi| = {worst:.2e}")
    ok = bool(not bad and not bad_e and (vt - vb).sign() == 0 and worst < 1e-9)
    cnt = Counter((t["kind"], tuple(t["A"])) for t in tiles)
    pr(f"orientations present: P {sum(1 for k in cnt if k[0]=='P')}/10, O {sum(1 for k in cnt if k[0]=='O')}/10")
    sharedpairs = Counter()
    for f, L in faces.items():
        if len(L) == 2: sharedpairs["".join(sorted(tiles[L[0][0]]["kind"] + tiles[L[1][0]]["kind"]))] += 1
    pr(f"shared faces by cell pair: {dict(sharedpairs)}")
    out = dict(radius_edges=str(Rn), gamma=[str(g) for g in gamma], E=[[str(x) for x in v] for v in E],
               tiles=[dict(n=t["n"], A=t["A"], kind=t["kind"], centre=[float(x) for x in P3(t["c6"])], centre_exact=[str(x) for x in P3(t["c6"])]) for t in tiles],
               shared=[[L[0][0], L[1][0], [list(p) for p in L[0][5]]] for f, L in faces.items() if len(L) == 2],
               shared_faces=opp, shared_by_pair=dict(sharedpairs), boundary_faces=nb, interior_edges=len(interior_e), interior_vertices=nint,
               volume=str(vt), checks_ok=ok, freq_ratio_P_O=str(fP/fO), vol_P=str(vP), vol_O=str(vO))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/patch.json"), "w"), indent=0)
    pr(("PATCH OK" if ok else "PATCH FAILED") + f"  tiles {len(tiles)}  ({time.time()-T0:.1f}s)")

if __name__ == "__main__":
    main()
