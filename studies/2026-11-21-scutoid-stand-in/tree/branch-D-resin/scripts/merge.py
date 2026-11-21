"""Branch D lead 2: fewer piece kinds by merging pieces of the central division R1 (bcc mould at s0) across C1 faces.
A merged piece over a set D of C1 faces is (cone over D) cap (mould) minus C1, i.e. D x (radial interval): a flat-faced ball exactly when D is
a disk on C1's surface (edge-connected, Euler characteristic 1, one fan at every vertex) and no point where C1 touches the mould lies inside D
(there the resin has thickness 0 and the piece would be pinched).  Kinds are counted as T_h orbits of merged pieces (one periodic tiling,
pieces of one kind are images of each other under T_h, so they are congruent exactly).
Lower bound (proved in the log): the stabiliser of a disk cluster fixes a point of the disk (finite group acting on a disk), so its order is
1, 2, 3 or 4 (point stabilisers in T_h: trivial, mirror or 2-fold axis, C2v on the coordinate axes, C3 on the 3-fold axes), the orbit size
m is 24, 12, 8 or 6, and m divides the size of every face orbit the kind contains.  The 8-orbit of hexagons forces m = 8; the 12-orbits force
m in {6, 12}: at least 2 kinds.  Search: kind A = C3-invariant disk round the (1,1,1) hexagon (8 images), kind B = the rest, accepted if
its edge-connected components are disks forming one T_h orbit.  Exact volumes from the R1 pieces (Q(sqrt5)).
Usage: python merge.py out.json"""
import itertools, json, sys
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from resin import build_C1, Q, dot, cross, vsc, TH, act, polytope
def pr(*a): print(*a, flush=True)
C = build_C1(); V, faces, planes = C["V"], C["faces"], C["planes"]; NF = len(faces)
fv = [f for f, k in faces]
edge_face = {}
for f, vs in enumerate(fv):
    for i in range(len(vs)): edge_face.setdefault(frozenset((vs[i], vs[(i+1) % len(vs)])), []).append(f)
adj = {f: set() for f in range(NF)}
for e, (a, b) in edge_face.items(): adj[a].add(b); adj[b].add(a)
keyv = {tuple(x.key() for x in v): i for i, v in enumerate(V)}
fid = {frozenset(f): i for i, f in enumerate(fv)}
def gf(g, f): return fid[frozenset(keyv[tuple(x.key() for x in act(g, V[i]))] for i in fv[f])]
orbits, done = [], set()
for f in range(NF):
    if f in done: continue
    o = sorted({gf(g, f) for g in TH}); done |= set(o); orbits.append(o)
orb_of = {f: k for k, o in enumerate(orbits) for f in o}
pr("face orbits:", [(faces[o[0]][1], len(o)) for o in orbits])
# mould: bcc at s0, contact points of C1 with the mould (exact)
s0 = Q(Fr(10, 3), Fr(4, 3))
Hs = []
for i in range(3):
    for sg in (1, -1):
        n = [Q(0)]*3; n[i] = Q(sg); Hs.append((n, s0*Fr(1, 2), ("shell", f"e{i}{sg}")))
for sg in itertools.product((1, -1), repeat=3): Hs.append(([Q(x) for x in sg], s0*Fr(3, 4), ("shell", f"111{sg}")))
contact = [v for v in range(len(V)) if any((dot(n, V[v]) - c).sign() == 0 for n, c, l in Hs)]
pr(f"bcc s0 = {s0}: C1 vertices on the mould: {len(contact)} ({sorted(set('apex' if v >= 60 else 'TI' for v in contact))})")
def is_disk(D):
    D = set(D)
    if not D: return False
    seen = {min(D)}; st = [min(D)]
    while st:
        f = st.pop()
        for g in adj[f] & D:
            if g not in seen: seen.add(g); st.append(g)
    if seen != D: return False
    vs = set().union(*[set(fv[f]) for f in D])
    es = {e for e, fs in edge_face.items() if set(fs) & D}
    if len(vs) - len(es) + len(D) != 1: return False
    for v in vs:      # one fan at each vertex
        ring = [f for f in range(NF) if v in fv[f]]
        inD = [f for f in ring if f in D]
        if len(inD) == len(ring): continue
        # faces of D at v must be connected through edges at v
        sub = set(inD); seen = {inD[0]}; st = [inD[0]]
        while st:
            f = st.pop()
            for g in adj[f] & sub:
                if g not in seen and frozenset(set(fv[f]) & set(fv[g])) and v in set(fv[f]) & set(fv[g]): seen.add(g); st.append(g)
        if seen != sub: return False
    return True
def pinched(D):
    D = set(D)
    return [v for v in contact if all(f in D for f in range(NF) if v in fv[f])]
def components(R):
    R = set(R); out = []
    while R:
        f = R.pop(); comp = {f}; st = [f]
        while st:
            x = st.pop()
            for g in adj[x] & R:
                R.discard(g); comp.add(g); st.append(g)
        out.append(comp)
    return out
# C3 about (1,1,1): cyclic permutation, no signs
c3 = [(c, (1, 1, 1)) for c in range(3)]
hexA = [f for f in orbits[0] if all(x.sign() > 0 for x in [sum((V[i][j] for i in fv[f]), Q(0)) for j in range(3)])][0]
tri24 = [k for k, o in enumerate(orbits) if len(o) == 24]
def c3orbits(k):
    res, dn = [], set()
    for f in orbits[k]:
        if f in dn: continue
        t = frozenset(gf(g, f) for g in c3); dn |= t; res.append(t)
    return res
choices = [[None] + c3orbits(k) for k in tri24]
found = []
for a, b in itertools.product(*choices):
    DA = {hexA} | (set(a) if a else set()) | (set(b) if b else set())
    if not is_disk(DA) or pinched(DA): continue
    imgsA = {frozenset(gf(g, f) for f in DA) for g in TH}
    if len(imgsA) != 8: continue
    covered = set().union(*imgsA)
    R = set(range(NF)) - covered
    comps = components(R)
    if not all(is_disk(c) and not pinched(c) for c in comps): continue
    c0 = comps[0]; imgsB = {frozenset(gf(g, f) for f in c0) for g in TH}
    if set(map(frozenset, comps)) != imgsB: continue
    found.append((DA, c0, len(imgsB)))
pr(f"2-kind merges found: {len(found)}")
# exact volumes and face counts of the merged pieces
def r1_piece(fi):
    f = fv[fi]; n, c = planes[fi]
    H = [(vsc(-1, n), -c, ("bottom", fi))]
    cen = [sum((V[i][j] for i in f), Q(0))/len(f) for j in range(3)]
    for i in range(len(f)):
        a, b = V[f[i]], V[f[(i+1) % len(f)]]; m = cross(a, b)
        if dot(m, cen).sign() < 0: m = vsc(-1, m)
        G = [g for g in edge_face[frozenset((f[i], f[(i+1) % len(f)]))] if g != fi][0]
        H.append((vsc(-1, m), Q(0), ("lat", G)))
    return polytope(H + Hs), H + Hs
cache = {}
def piece_info(D):
    vol = Q(0); shells = set(); bottoms = len(D); lat = 0
    for f in D:
        if f not in cache: cache[f] = r1_piece(f)
        P, H = cache[f]; vol = vol + P["vol"]
        for t in P["faces"]:
            lab = H[t][2]
            if lab[0] == "shell": shells.add(lab[1])
            if lab[0] == "lat" and lab[1] not in D: lat += 1
    return vol, bottoms, lat, len(shells)
out = []
best = None
for DA, DB, mB in found:
    vA, bA, lA, sA = piece_info(DA); vB, bB, lB, sB = piece_info(DB)
    total = vA*8 + vB*mB
    resin = s0*s0*s0*Fr(1, 2) - Q(35, Fr(25, 2))
    okv = (total - resin).sign() == 0
    rec = dict(A=sorted(DA), A_faces=[faces[f][1] for f in sorted(DA)], A_count=8, A_vol=str(vA), A_planes=bA + lA + sA, A_bottom=bA, A_lateral=lA, A_mould=sA,
               B=sorted(DB), B_faces=[faces[f][1] for f in sorted(DB)], B_count=mB, B_vol=str(vB), B_planes=bB + lB + sB, B_bottom=bB, B_lateral=lB, B_mould=sB,
               volume_exact=okv)
    out.append(rec)
    pr(f" A: {len(DA)} C1 faces ({rec['A_faces'].count('hex')} hex, {rec['A_faces'].count('tri')} tri) x 8 per cell, vol {vA} = {float(vA):.6f}, "
       f"flat faces {rec['A_planes']} (on C1 {bA}, cone walls {lA}, mould {sA});  B: {len(DB)} C1 faces ({rec['B_faces'].count('hex')} hex, "
       f"{rec['B_faces'].count('tri')} tri) x {mB}, vol {vB} = {float(vB):.6f}, flat faces {rec['B_planes']} (on C1 {bB}, walls {lB}, mould {sB}); "
       f"8 vA + {mB} vB = resin exactly: {okv}")
json.dump(dict(lower_bound=2, found=out), open(sys.argv[1] if len(sys.argv) > 1 else "merge.json", "w"), indent=1)
ok = bool(out) and all(r["volume_exact"] for r in out)
pr(f"minimum number of kinds (disk pieces, T_h orbits): {'2 (bound attained)' if out else 'not attained by this search'}")
pr("FINAL ok" if ok else "FINAL FAIL: no 2-kind merge verified")
