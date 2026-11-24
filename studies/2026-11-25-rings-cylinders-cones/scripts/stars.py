#!/usr/bin/env python3
"""Rings in the fins of the stellation-cycle polyhedra (25 Nov 2026), exact in Q(sqrt5) (q5 of study 2026-11-25-stellation-cycle).

Polyhedra: I0, D0 (frame of the Aequi), the four Kepler-Poinsot stars on D0 / I0 (vertices as Theorem 2 there), the Dogstar
and the Sunstar (surfaces rebuilt by that study's own cycle.py, run unchanged; its edge pieces merged into edges here).
For each: fin classes by exact key ({|Oa|^2, |Ob|^2}, |ab|^2); whether the radial projections of two edges cross
(exact signs); at each crossing, how the two rings meet the common ray (float chords, 40 digits by mpmath):
  'cross' (two common points, the rings pass through each other), 'linked', 'nested' or 'apart'.
Output data/stars.json; FINAL ok when every count was decided.
"""
import os, sys, json, re, io, itertools, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
SC = os.path.normpath(os.path.join(HERE, "../../2026-11-25-stellation-cycle/scripts"))
sys.path.insert(0, SC)
from q5 import Q, PHI, phipow, dot, cross, vsub, vadd, vsc, vkey, cyclic_signs
import mpmath as mp
mp.mp.dps = 40

def r2(v): return dot(v, v)
def mv(v): return [mp.mpf(x.a.numerator) / x.a.denominator + mp.mpf(x.b.numerator) / x.b.denominator * mp.sqrt(5) for x in v]

I0 = cyclic_signs([(Q(0), PHI, Q(1))])
D0 = cyclic_signs([(Q(1), Q(1), Q(1))]) + cyclic_signs([(Q(0), 1 / PHI, PHI)])
D0 = list({vkey(v): v for v in D0}.values()); I0 = list({vkey(v): v for v in I0}.values())
assert len(I0) == 12 and len(D0) == 20

def edges_at(V, e2f):
    """edges = the pairs at the exact squared distance whose float is e2f"""
    ds = {}
    for i, j in itertools.combinations(range(len(V)), 2):
        d = r2(vsub(V[i], V[j])); ds.setdefault(d.key(), []).append((i, j))
    k = [k for k in ds if abs(Q(*k).f() - e2f) < 1e-9]
    assert len(k) == 1, "edge length not unique"
    return ds[k[0]]

def parse_q(s):
    s = s.replace(" ", "").replace("−", "-")
    m = re.fullmatch(r"([+-]?[\d/]+)?(?:([+-])([\d/]*)√5)?", s)
    from fractions import Fraction as Fr
    a = Fr(m.group(1)) if m.group(1) else Fr(0)
    b = Fr(0)
    if m.group(2): b = (Fr(m.group(3)) if m.group(3) else Fr(1)) * (1 if m.group(2) == "+" else -1)
    return float(a) + float(b) * 5 ** 0.5

def det3(a, b, c): return dot(a, cross(b, c))

def arcs_cross(a, b, c, d):
    """exact: do the great-circle arcs ab and cd (shorter arcs, no common end) cross at an inner point?"""
    n1, n2 = cross(a, b), cross(c, d)
    w = cross(n1, n2)
    if all(x == 0 for x in w): return None
    for s in (1, -1):
        x = vsc(Q(s), w)
        # x inside arc ab: (a x x).n1 > 0 and (x x b).n1 > 0 ; same for cd
        if (dot(cross(a, x), n1).sign() > 0 and dot(cross(x, b), n1).sign() > 0 and
                dot(cross(c, x), n2).sign() > 0 and dot(cross(x, d), n2).sign() > 0):
            return x
    return None

def ring(a, b):
    A, B = mv(a), mv(b)
    la, lb = mp.sqrt(sum(x * x for x in A)), mp.sqrt(sum(x * x for x in B))
    lab = mp.sqrt(sum((x - y) ** 2 for x, y in zip(A, B)))
    P = la + lb + lab
    c = [(lab * 0 + lb * x + la * y) / P for x, y in zip(A, B)]      # incentre: (|ab| O + |Ob| a + |Oa| b) / P
    cr = [A[1] * B[2] - A[2] * B[1], A[2] * B[0] - A[0] * B[2], A[0] * B[1] - A[1] * B[0]]
    r = mp.sqrt(sum(x * x for x in cr)) / P
    return c, r, (la + lb - lab) / 2

def chord(c, r, w):
    W = mv(w); n = mp.sqrt(sum(x * x for x in W)); W = [x / n for x in W]
    wc = sum(x * y for x, y in zip(W, c)); disc = wc * wc - sum(x * x for x in c) + r * r
    assert disc > 0
    return wc - mp.sqrt(disc), wc + mp.sqrt(disc)

def study(name, V, E):
    cls = {}
    for i, j in E:
        key = (tuple(sorted([r2(V[i]).key(), r2(V[j]).key()])), r2(vsub(V[i], V[j])).key())
        cls[key] = cls.get(key, 0) + 1
    rad = {}
    for i, j in E:
        c, r, t = ring(V[i], V[j]); rad.setdefault(mp.nstr(r, 30), 0); rad[mp.nstr(r, 30)] += 1
    kinds = {"cross": 0, "linked": 0, "nested": 0, "apart": 0}; ncross = 0
    for (i, j), (k, l) in itertools.combinations(E, 2):
        if len({i, j, k, l}) < 4: continue
        w = arcs_cross(V[i], V[j], V[k], V[l])
        if w is None: continue
        ncross += 1
        c1, ra, _ = ring(V[i], V[j]); c2, rb, _ = ring(V[k], V[l])
        p, q = chord(c1, ra, w), chord(c2, rb, w)
        eps = mp.mpf(10) ** -30
        if abs(p[0] - q[0]) < eps or abs(p[1] - q[1]) < eps or abs(p[0] - q[1]) < eps or abs(p[1] - q[0]) < eps:
            kinds["cross"] += 1
        elif p[1] < q[0] or q[1] < p[0]: kinds["apart"] += 1
        elif (p[0] < q[0]) == (p[1] < q[1]): kinds["linked"] += 1
        else: kinds["nested"] += 1
    shells = sorted({r2(v).key() for v in V}, key=lambda k: Q(*k).f())
    out = dict(name=name, V=len(V), E=len(E), vertex_shells=len(shells), fin_classes=len(cls),
               ring_radii=sorted(rad.items(), key=lambda kv: -float(kv[0])), projected_edge_crossings=ncross, ring_meetings_at_crossings=kinds)
    print(json.dumps(out), flush=True)
    return out

RES = []
cyc = json.load(open(os.path.join(SC, "../data/cycle.json")))
def star_edges(label, V):
    return edges_at(V, parse_q(cyc[label]["edge2"]))
I1 = [vsc(PHI, v) for v in I0]; D3 = [vsc(phipow(3), v) for v in D0]; I3 = [vsc(phipow(3), v) for v in I0]
RES.append(study("icosahedron I0", I0, edges_at(I0, 4.0)))
RES.append(study("dodecahedron D0", D0, edges_at(D0, 6 - 2 * 5 ** 0.5)))
for lab, V in (("star small stellated dodecahedron {5/2,5} on D0", I1), ("star great dodecahedron {5,5/2} on D0", I1),
               ("star great stellated dodecahedron {5/2,3} on D0", D3), ("star great icosahedron {3,5/2} on I0", I3)):
    RES.append(study(lab.replace("star ", ""), V, star_edges(lab, V)))

# Dogstar and Sunstar: run the stellation study's cycle.py unchanged, keeping surface_report's returns
src = open(os.path.join(SC, "cycle.py")).read()
src = src.replace('surface_report("Sunstar (D0 + six Dogstars)", Spl, sun_member, keep=near)',
                  'SUN = surface_report("Sunstar (D0 + six Dogstars)", Spl, sun_member, keep=near)')
src = src.split("# ---------- 6.")[0]
ns = {"__file__": os.path.join(SC, "cycle.py"), "__name__": "cycle_run"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "cycle.py", "exec"), ns)

def merge_edges(verts, pieces):
    bylk = {}
    for pc in pieces: bylk.setdefault(pc[0], []).append(pc)
    E = []; idx = {k: n for n, k in enumerate(verts)}
    for lk, ps in bylk.items():
        ps.sort(key=lambda pc: pc[3].f())
        cur = None
        for lk_, p, u, t0, t1, fp in ps:
            x0, x1 = vadd(p, vsc(t0, u)), vadd(p, vsc(t1, u))
            if cur is not None and vkey(cur[1]) == vkey(x0) and vkey(x0) not in verts:
                cur = (cur[0], x1)
            else:
                if cur is not None: E.append(cur)
                cur = (x0, x1)
        E.append(cur)
    out = []
    for a, b in E:
        assert vkey(a) in verts and vkey(b) in verts, "edge piece does not end at corners"
        out.append((idx[vkey(a)], idx[vkey(b)]))
    return out

for lab, (rep, verts, pieces) in (("Dogstar", (ns["dog"], ns["dogV"], ns["dogP"])), ("Sunstar", ns["SUN"])):
    keys = list(verts); V = [verts[k] for k in keys]
    E = merge_edges({k: n for n, k in enumerate(keys)}, pieces)
    assert len(E) == rep["edges"], (lab, len(E), rep["edges"])
    RES.append(study(lab, V, E))

json.dump(RES, open(os.path.join(STUDY, "data/stars.json"), "w"), indent=1)
print("FINAL ok" if len(RES) == 8 else "FINAL FAIL row count")
