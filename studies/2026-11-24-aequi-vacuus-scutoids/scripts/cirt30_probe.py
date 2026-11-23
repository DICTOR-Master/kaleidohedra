"""Probe (not a proof): Aequus CIRT-30, T 26 (C6 + I12 + RT24/12a).  With C6 depth 1, I12 depth d, RT24/12a depth t: solid angles of
one C6 face and one RT24/12a face, mpmath 50 digits.  Question: is Omega_C6(1, d) - Omega_RT(1, d) zero for every d (an identity), or
only at the fair d?"""
import itertools, json, os, sys
import mpmath as mp
mp.mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import classify as C
D = json.load(open(os.path.join(HERE, "../src/dice.json"))); e = D["dice"][83]
ED = C.exact_dirs(D["dirs"])
def unit(i):
    v = [mp.mpf(x.a.numerator)/x.a.denominator + mp.mpf(x.b.numerator)/x.b.denominator*mp.sqrt(5) for x in ED[i][0]]
    n = mp.sqrt(sum(x*x for x in v)); return [x/n for x in v]
orbs = [D["groups"]["T"][oi]["dirs"] for oi in e["o"]]
def omegas(depths):
    P = [(unit(i), depths[k], k) for k, ob in enumerate(orbs) for i in ob]
    V = []
    for a, b, c in itertools.combinations(range(len(P)), 3):
        A_, B_, C_ = P[a][0], P[b][0], P[c][0]
        def cr(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        bc, ca, ab = cr(B_, C_), cr(C_, A_), cr(A_, B_)
        det = sum(A_[t]*bc[t] for t in range(3))
        if abs(det) < mp.mpf(10)**-30: continue
        x = mp.matrix([(P[a][1]*bc[t] + P[b][1]*ca[t] + P[c][1]*ab[t])/det for t in range(3)])
        if all(sum(P[j][0][t]*x[t] for t in range(3)) <= P[j][1] + mp.mpf(10)**-35 for j in range(len(P))):
            if not any(mp.norm(x - y) < mp.mpf(10)**-25 for y in V): V.append(x)
    out = {}
    for j, (n, dd, k) in enumerate(P):
        if k in out: continue
        F = [x for x in V if abs(sum(n[t]*x[t] for t in range(3)) - dd) < mp.mpf(10)**-30]
        cen = sum(F, mp.matrix([0, 0, 0]))/len(F)
        u = F[0] - cen; u = u/mp.norm(u); w = mp.matrix([n[1]*u[2]-n[2]*u[1], n[2]*u[0]-n[0]*u[2], n[0]*u[1]-n[1]*u[0]])
        F.sort(key=lambda x: mp.atan2(mp.fdot(x - cen, w), mp.fdot(x - cen, u)))
        om = 0
        for q in range(1, len(F) - 1):   # Van Oosterom-Strackee
            a, b, c = F[0], F[q], F[q+1]
            la, lb, lc = mp.norm(a), mp.norm(b), mp.norm(c)
            num = mp.det(mp.matrix([list(a), list(b), list(c)]))
            den = la*lb*lc + mp.fdot(a, b)*lc + mp.fdot(a, c)*lb + mp.fdot(b, c)*la
            om += 2*mp.atan2(num, den)
        out[k] = abs(om)
    return out
d_fair = mp.mpf("1.01493580273976924160395072939389889123650394152433484404268")
for d in (d_fair, d_fair + mp.mpf("0.001"), d_fair - mp.mpf("0.002"), d_fair + mp.mpf("0.01")):
    o = omegas([mp.mpf(1), d, mp.mpf(1)])
    print("d", mp.nstr(d, 15), "Omega C6", mp.nstr(o[0], 20), "Omega RT", mp.nstr(o[2], 20), "diff", mp.nstr(o[0] - o[2], 5), "4pi/30", mp.nstr(4*mp.pi/30, 20))

if __name__ == "__main__" and len(sys.argv) > 1:
    # vertices of one C6 face and one RT24/12a face at the fair depths, with directions compared to the triacontahedron
    d = d_fair; P = [(unit(i), [mp.mpf(1), d, mp.mpf(1)][k], k, i) for k, ob in enumerate(orbs) for i in ob]
    V = []
    for a, b, c in itertools.combinations(range(len(P)), 3):
        A_, B_, C_ = P[a][0], P[b][0], P[c][0]
        def cr(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        bc, ca, ab = cr(B_, C_), cr(C_, A_), cr(A_, B_)
        det = sum(A_[t]*bc[t] for t in range(3))
        if abs(det) < mp.mpf(10)**-30: continue
        x = [(P[a][1]*bc[t] + P[b][1]*ca[t] + P[c][1]*ab[t])/det for t in range(3)]
        if all(sum(P[j][0][t]*x[t] for t in range(3)) <= P[j][1] + mp.mpf(10)**-35 for j in range(len(P))):
            if not any(sum((x[t]-y[t])**2 for t in range(3)) < mp.mpf(10)**-40 for y in V): V.append(x)
    print("vertices", len(V))
    phi = (1 + mp.sqrt(5))/2
    for k in (0, 2):
        n = P[[j for j in range(len(P)) if P[j][2] == k][0]][0]; dd = P[[j for j in range(len(P)) if P[j][2] == k][0]][1]
        F = [x for x in V if abs(sum(n[t]*x[t] for t in range(3)) - dd) < mp.mpf(10)**-30]
        print("orbit", k, "normal", [mp.nstr(c, 8) for c in n])
        for x in F:
            r = mp.sqrt(sum(c*c for c in x))
            print("   ", [mp.nstr(c, 12) for c in x], "|v|^2", mp.nstr(r*r, 15), "identify", [mp.identify(c, ["sqrt(5)"]) for c in x])
