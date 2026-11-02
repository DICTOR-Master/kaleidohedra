# DICTO Vacuus as modular origami (DICTO proposed 2026-11-02): the geometry of the open-pyramid fans of one solid.
# The Vacuus of a solid (study 2026-11-02-dicto-vacuus) is the set of fins O-A-B, one per edge AB, O = the corner centroid. One sheet
# cannot fold the whole Vacuus (3 or more fins meet along each strut O-v), but the centre pyramid of each face, OPEN (no base), is a fan
# of triangles O-v_k-v_(k+1), one per face edge, which folds from one flat net. Nesting all open pyramids with their apices at O makes
# every fin a double wall (the two pyramids on the two sides of the edge, glued back to back).
# Computed per solid, exact in Q / Q(sqrt2) / Q(sqrt3) / Q(sqrt5) where the source is exact (float64 otherwise, flagged):
#  - per face: strut lengths |Ov_k|^2, rim edges |v_k v_(k+1)|^2, fan angles theta_k (apex angles of the fins, cos^2 exact),
#    fan angle sum (must be < 360 deg for a flat net), fold dihedrals psi_k at the struts (inside the pyramid, cos^2 + sign exact);
#  - fin letters (a, b, ... by exact congruence of the fin), net types (faces whose fans agree as cyclic sequences of
#    (strut, fin, neighbour net type), refined until stable; read counter-clockwise on the printed side = the inside of the pyramid,
#    which is counter-clockwise seen from outside the solid), mirror pairs;
#  - closure check: the flat net is folded by the computed psi_k, triangle by triangle about each strut, and the folded corners are
#    compared with the true corners (the last one must return to the first: the fan closes up).
#  - central discs (flat sheets of fins closing round O), marked per fin.
# Usage: fan.py <solid json> <out json>
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qf
from qf import QF, vsub, dot, cross
SRC, OUTF = sys.argv[1:3]
d = json.load(open(SRC)); F = [list(f) for f in d['faces']]
dq = qf.field(d.get('field', ''))
exact = dq is not None and d['vertices'][0].get('exact') is not None
V = [[qf.parse(x) for x in v['exact']] for v in d['vertices']] if exact else [[float(x) for x in v['decimal']] for v in d['vertices']]
n = len(V); Z = (lambda: QF(0)) if exact else (lambda: 0.0)
c = [sum((p[i] for p in V), Z()) / n for i in range(3)]; V = [vsub(p, c) for p in V]      # O = corner centroid at the origin
VF = np.array([[float(x) for x in p] for p in V]); R2 = float(max(float(dot(p, p)) for p in V)); R = math.sqrt(R2)
def sg(x): return x.sign() if exact else (0 if abs(x) < 1e-10 * R2 * R else (1 if x > 0 else -1))
def key(x): return f'{x.a}|{x.b}' if exact else f'{x / R2:.9f}'
def ex(x): return str(x) if exact else None
vol = sum(float(qf.det3(V[f[0]], V[f[k]], V[f[k + 1]])) for f in F for k in range(1, len(f) - 1))
if vol < 0: F = [f[::-1] for f in F]                    # faces counter-clockwise seen from outside
NF = []
for f in F:
    N = [Z(), Z(), Z()]
    for k in range(len(f)): N = [x + y for x, y in zip(N, cross(V[f[k]], V[f[(k + 1) % len(f)]]))]
    NF.append(N)
assert all(sg(dot(NF[i], V[f[0]])) > 0 for i, f in enumerate(F)), 'O not inside every face plane: no Vacuus'
E = {}
for i, f in enumerate(F):
    for k in range(len(f)): a, b = f[k], f[(k + 1) % len(f)]; E.setdefault((min(a, b), max(a, b)), []).append(i)
assert all(len(l) == 2 for l in E.values())
def other(e, i): l = E[(min(e), max(e))]; return l[1] if l[0] == i else l[0]
# fin letters by exact congruence (sorted strut pair + rim edge)
fk = {}
for (a, b) in E:
    s = sorted([dot(V[a], V[a]), dot(V[b], V[b])], key=float); D = vsub(V[b], V[a])
    fk[(a, b)] = (key(s[0]), key(s[1]), key(dot(D, D)))
cnt = {}
for k in fk.values(): cnt[k] = cnt.get(k, 0) + 1
def apex_of(a, b):
    A, B = VF[a], VF[b]; return math.atan2(np.linalg.norm(np.cross(A, B)), A @ B)
order = sorted(cnt, key=lambda k: (-cnt[k], apex_of(*next(e for e in fk if fk[e] == k))))
letter = {k: 'abcdefghijklmnopqrstuvwxyz'[i] for i, k in enumerate(order)}
def fin(a, b): return letter[fk[(min(a, b), max(a, b))]]
# strut classes (numbers 1, 2, ... longest first)
sk = sorted({key(dot(p, p)) for p in V}, key=lambda s: -float(dot(V[[key(dot(p, p)) for p in V].index(s)], V[[key(dot(p, p)) for p in V].index(s)])))
strut_no = [sk.index(key(dot(p, p))) + 1 for p in V]
# central discs: fins that share a strut and lie in one plane, joined; a sheet whose apex angles sum to 360 deg is a central disc
fins_l = list(E); pf = list(range(len(fins_l)))
def fp(x):
    while pf[x] != x: pf[x] = pf[pf[x]]; x = pf[x]
    return x
at = {}
for i, (a, b) in enumerate(fins_l):
    at.setdefault(a, []).append(i); at.setdefault(b, []).append(i)
for v, l in at.items():
    for i in l:
        for j in l:
            if i >= j: continue
            a = [x for x in fins_l[i] if x != v][0]; b = [x for x in fins_l[j] if x != v][0]
            if sg(qf.det3(V[v], V[a], V[b])) == 0 and sg(dot(cross(V[v], V[a]), cross(V[v], V[b]))) < 0: pf[fp(i)] = fp(j)
comp = {}
for i in range(len(fins_l)): comp.setdefault(fp(i), []).append(i)
disc = set()
for l in comp.values():
    if len(l) > 1 and abs(sum(apex_of(*fins_l[i]) for i in l) - 2 * math.pi) < 1e-9: disc |= {fins_l[i] for i in l}
# per face: fan data
def wedge(f, k):
    """dihedral psi at strut O-v_k inside the pyramid of face f (between fins v_(k-1)v_k and v_k v_(k+1)); exact cos^2 and sign"""
    m = len(f); u, v, w = V[f[k - 1]], V[f[k]], V[f[(k + 1) % m]]; vv = dot(v, v)
    up = vsub(u, [x * (dot(u, v) / vv) for x in v]); wp = vsub(w, [x * (dot(w, v) / vv) for x in v])
    cw = dot(up, wp); uu, ww = dot(up, up), dot(wp, wp)
    a = np.array([float(x) for x in up]); b = np.array([float(x) for x in wp]); ang = math.atan2(np.linalg.norm(np.cross(a, b)), a @ b)
    i = F.index(f); reflex = sg(dot(cross(vsub(v, u), vsub(w, v)), NF[i])) < 0
    return (2 * math.pi - ang if reflex else ang), ex(cw * cw / (uu * ww)), sg(cw), reflex
faces = []
for i, f in enumerate(F):
    m = len(f); tri = []
    for k in range(m):
        a, b = f[k], f[(k + 1) % m]; A, B = V[a], V[b]; D = vsub(B, A)
        tri.append(dict(a=a, b=b, ra2=float(dot(A, A)), rb2=float(dot(B, B)), ra2_exact=ex(dot(A, A)), rb2_exact=ex(dot(B, B)),
                        ab2=float(dot(D, D)), ab2_exact=ex(dot(D, D)), theta=apex_of(a, b),
                        cos2theta_exact=ex(dot(A, B) * dot(A, B) / (dot(A, A) * dot(B, B))), sign_cos_theta=sg(dot(A, B)),
                        fin=fin(a, b), nbr_face=other((a, b), i), disc=(min(a, b), max(a, b)) in disc))
    ws = [wedge(f, k) for k in range(m)]
    faces.append(dict(corners=f, tri=tri, psi=[w[0] for w in ws], cos2psi_exact=[w[1] for w in ws], sign_cos_psi=[w[2] for w in ws],
                      reflex=[w[3] for w in ws], fan_sum=sum(t['theta'] for t in tri)))
# net types: cyclic sequences of (strut class, fin, neighbour type), refined until stable; canonical start = least rotation
def seq(i, typ, rev=False):
    f = faces[i]; m = len(f['corners'])
    s = [f"{strut_no[t['a']]}{t['fin']}{typ[t['nbr_face']]}" for t in f['tri']]
    if rev: s = [f"{strut_no[t['b']]}{t['fin']}{typ[t['nbr_face']]}" for t in f['tri']][::-1]
    rots = [tuple(s[k:] + s[:k]) for k in range(m)]; best = min(rots); return best, rots.index(best)
def relabel(keys):
    u = sorted(set(keys), key=lambda k: (len(k), -keys.count(k), keys.index(k))); return [u.index(k) for k in keys]
typ = relabel([(0,) * len(f['corners']) for f in faces]); prev = -1
while True:
    typ = relabel([seq(i, typ)[0] for i in range(len(faces))])
    if len(set(typ)) == prev: break
    prev = len(set(typ))
keys = [seq(i, typ)[0] for i in range(len(faces))]; t2 = relabel(keys)
assert t2 == typ, 'type numbering not stable'
uk = sorted(set(keys), key=lambda k: typ[keys.index(k)])
for i, f in enumerate(faces): f['type'] = typ[i]; f['start'] = seq(i, typ)[1]
names = {3: 'triangle', 4: 'quadrilateral', 5: 'pentagon', 6: 'hexagon', 8: 'octagon', 10: 'decagon'}
types = []
for t in range(len(uk)):
    mem = [i for i in range(len(faces)) if typ[i] == t]; f = faces[mem[0]]; m = len(f['corners'])
    reg = len({round(x['ab2'], 9) for x in f['tri']}) == 1 and len({round(x['ra2'], 9) for x in f['tri']}) == 1
    nm = names.get(m, f'{m}-gon')
    if reg: nm = {3: 'equilateral triangle', 4: 'square'}.get(m, 'regular ' + nm)
    rk = seq(mem[0], typ, rev=True)[0]; mirror = uk.index(rk) if rk in uk else None
    st = f['start']; tri = [f['tri'][(st + k) % m] for k in range(m)]
    psi = [f['psi'][(st + k) % m] for k in range(m)]; c2 = [f['cos2psi_exact'][(st + k) % m] for k in range(m)]
    sgn = [f['sign_cos_psi'][(st + k) % m] for k in range(m)]
    types.append(dict(id=t, name=f'N{t + 1}', sides=m, face=nm, count=len(mem), faces=mem, mirror_of=None if mirror in (None, t) else mirror,
                      self_mirror=mirror == t, tri=[dict(tt, nbr_type=typ[tt['nbr_face']], strut_a=strut_no[tt['a']], strut_b=strut_no[tt['b']]) for tt in tri],
                      psi=psi, cos2psi_exact=c2, sign_cos_psi=sgn, fan_sum_deg=math.degrees(f['fan_sum'])))
# closure check: fold each type's flat net by its psi and compare with the true corners of every member face (rigidly moved)
def fold(ty):
    tri = ty['tri']; m = len(tri); r = [math.sqrt(t['ra2']) for t in tri] + [math.sqrt(tri[0]['ra2'])]; th = [t['theta'] for t in tri]
    P = [np.array([r[0], 0, 0]), r[1] * np.array([math.cos(th[0]), math.sin(th[0]), 0])]
    for s in (1, -1):
        Q = list(P)
        for k in range(1, m):
            a = Q[k] / np.linalg.norm(Q[k]); e1 = Q[k - 1] - (Q[k - 1] @ a) * a; e1 /= np.linalg.norm(e1); e2 = np.cross(a, e1)
            psi = ty['psi'][k]; dirp = math.cos(psi) * e1 + s * math.sin(psi) * e2
            Q.append(r[k + 1] * (math.cos(th[k]) * a + math.sin(th[k]) * dirp))
        yield s, np.array(Q)
def kabsch(A, B):
    H = A.T @ B; U, S, Wt = np.linalg.svd(H); D = np.diag([1, 1, np.sign(np.linalg.det(Wt.T @ U.T))]); return Wt.T @ D @ U.T
worst = 0.0; worst_close = 0.0
for ty in types:
    errs = []
    for s, Q in fold(ty):
        e = 0.0
        for i in ty['faces']:
            f = faces[i]; m = len(f['corners']); st = f['start']; T = np.array([VF[f['corners'][(st + k) % m]] for k in range(m)] + [VF[f['corners'][st]]])
            Rm = kabsch(Q[:m], T[:m]); e = max(e, np.abs(Q @ Rm.T - T).max() / R)
        errs.append((e, s, np.linalg.norm(Q[m] - Q[0]) / R))
    e, s, cl = min(errs); ty['fold_err'] = e; ty['closure_err'] = cl; ty['fold_sense'] = s; worst = max(worst, e); worst_close = max(worst_close, cl)
assert all(t['fan_sum_deg'] < 360 for t in types)
# flat-net side check: in the plane, |P_k P_(k+1)|^2 must equal the exact rim edge
side = 0.0
for ty in types:
    tri = ty['tri']; phi = 0.0
    for t in tri:
        A = math.sqrt(t['ra2']) * np.array([math.cos(phi), math.sin(phi)]); phi += t['theta']; B = math.sqrt(t['rb2']) * np.array([math.cos(phi), math.sin(phi)])
        side = max(side, abs(((B - A) @ (B - A)) - t['ab2']) / R2)
fins_out = []
for k in order:
    e = next(e for e in fk if fk[e] == k); a, b = e; A, B = V[a], V[b]; D = vsub(B, A)
    fins_out.append(dict(letter=letter[k], count=cnt[k], OA2_exact=ex(min(dot(A, A), dot(B, B), key=float)), OB2_exact=ex(max(dot(A, A), dot(B, B), key=float)),
                         AB2_exact=ex(dot(D, D)), OA=math.sqrt(min(float(dot(A, A)), float(dot(B, B)))), OB=math.sqrt(max(float(dot(A, A)), float(dot(B, B)))),
                         AB=math.sqrt(float(dot(D, D))), apex_deg=math.degrees(apex_of(a, b)), disc=e in disc))
struts = []
for s in range(len(sk)):
    i = strut_no.index(s + 1); struts.append(dict(no=s + 1, count=strut_no.count(s + 1), L=math.sqrt(float(dot(V[i], V[i]))), L2_exact=ex(dot(V[i], V[i]))))
res = dict(src=os.path.basename(SRC), name=d['name'], field=d.get('field'), exact=exact, R=R, V=n, E=len(E), F=len(F), points=VF.tolist(),
           faces=[dict(corners=f['corners'], type=f['type'], start=f['start']) for f in faces], strut_no=strut_no, struts=struts, fins=fins_out,
           types=types, disc_fins=[list(e) for e in sorted(disc)], checks=dict(fold_err=worst, closure_err=worst_close, side_err=side,
           fan_sum_max_deg=max(t['fan_sum_deg'] for t in types), fan_sum_min_deg=min(t['fan_sum_deg'] for t in types),
           half_tabs_per_edge=2))
os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True); json.dump(res, open(OUTF, 'w'), indent=1)
print(d['name'], 'faces', len(F), 'net types', len(types), [(t['name'], t['sides'], t['count'], round(t['fan_sum_deg'], 3), t['mirror_of']) for t in types],
      'fold err %.1e closure %.1e side %.1e' % (worst, worst_close, side), 'disc fins', len(disc), 'exact', exact, flush=True)
