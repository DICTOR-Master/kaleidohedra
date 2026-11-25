"""Quality overlaps on the 15 192 certified Aequi (study 2026-11-25-quality-overlaps).

For every die P = {x : u_k.x <= d_k} (fair about O = 0), with its certified combinatorics:
  Resonus  = the planes u_k^perp (one per face line);
  Vacuus   = the plates through O and each edge; the plate of the edge of faces k, j has normal n = d_j u_k - d_k u_j;
  mirrors  = the reflections among the frame maps that keep every labelled face orbit (the die's labelled group).
Exact decisions:
  - lines, families, frame maps: a fixed finite set of exact directions over Q(sqrt5) (study aequi-certify-extend); float
    equality there is decisive because distinct values are separated (separation printed);
  - a plate is parallel to the Resonus plane of face m only if det(u_k, u_j, u_m) = 0 (exact, Q(sqrt5)); then
    u_m = a u_k + b u_j exactly and the plate is u_m^perp iff d_j/d_k = r* := (-a/b)|v_k|/|v_j| (with ab < 0).
    Same orbit (d_j = d_k exactly): r* = 1 is decided exactly. Different orbits: r* (arb) against the certified depth balls;
    overlapping balls are reported as CANDIDATES (none is claimed).
  - mirror laws (study 2026-11-24-resonus-4d, Theorems 1-2): the plate of edge kj is a mirror iff a reflection of the group
    swaps faces k and j; the Resonus plane of face k is a mirror iff the reflection in u_k^perp is in the group.
  - simplicial Resonus: exact arrangement count in Q(sqrt5): f0 points, f1 = sum of multiplicities, f2 = 1 - f0 + f1
    (projective plane), simplicial iff 3 f2 = 2 f1.
Joined: Tacitus beyond symmetry (study 2026-11-25-tacitus), equal corner curvature (study 2026-11-25-inversions).
Usage: aequi_overlaps.py OUT.jsonl NPROC [LIMIT]   -> PROGRESS lines, summary, FINAL ok only if every control passes.
"""
import os, sys, json, gzip, csv, time, itertools
from fractions import Fraction as Fr
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
ST = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ST, '2026-11-25-inversions', 'scripts'))
import polar_aequi as PA                      # records(): the 15 192 dice; certify module as PA.C
import q5
from q5 import Q
from flint import arb, ctx
ctx.prec = 200
C = PA.C
DIRS, DFAM = C.DIRS, C.DFAM if hasattr(C, 'DFAM') else None
import groups as GR                           # certify-extend groups (DFAM)
DFAM = GR.DFAM
ND = len(DIRS)

# ---------- exact directions ----------
def qv(i):  # EXACT[i]: coordinates (a, b) meaning a + b*phi  ->  Q(sqrt5)
    return tuple(Q(Fr(a) + Fr(b) / 2, Fr(b) / 2) for (a, b) in C.EXACT[i])
VX = [qv(i) for i in range(ND)]
N2 = [q5.dot(v, v) for v in VX]               # |v|^2 in Q(sqrt5)
def qarb(x): return arb(x.a.numerator) / x.a.denominator + arb(x.b.numerator) / x.b.denominator * arb(5).sqrt()
dd = np.linalg.norm(DIRS[:, None, :] - DIRS[None, :, :], axis=2)
SEP = float(np.min(dd[dd > 1e-12]))
OPP = [int(np.argmin(np.linalg.norm(DIRS + DIRS[i], axis=1))) for i in range(ND)]
assert all(np.linalg.norm(DIRS[OPP[i]] + DIRS[i]) < 1e-12 for i in range(ND))
LINE = [min(i, OPP[i]) for i in range(ND)]
def det3(a, b, c): return q5.dot(a, q5.cross(b, c))
def is0(x): return x.a == 0 and x.b == 0

# zero-determinant triples, decided exactly (float only as a filter, with the margin checked)
U = DIRS
ZT = {}          # (a, b) -> list of (c, same_ok, rstar_arb)
fl = np.einsum('ij,kj->ik', U, U)
minnz = 1.0
for a in range(ND):
    for b in range(ND):
        if LINE[a] == LINE[b]: continue
        cr = np.cross(U[a], U[b]); dts = U @ cr
        for c in range(ND):
            if abs(dts[c]) > 1e-6:
                minnz = min(minnz, abs(dts[c])); continue
            if LINE[c] in (LINE[a], LINE[b]): continue
            assert is0(det3(VX[a], VX[b], VX[c])), ('float-small det not exactly zero', a, b, c)
            # v_c = al v_a + be v_b  (exact): solve with the Gram system
            g11, g12, g22 = N2[a], q5.dot(VX[a], VX[b]), N2[b]
            r1, r2 = q5.dot(VX[c], VX[a]), q5.dot(VX[c], VX[b])
            den = g11 * g22 - g12 * g12
            al = (r1 * g22 - r2 * g12) / den; be = (r2 * g11 - r1 * g12) / den
            if is0(al) or is0(be) or (al * be).sign() > 0: continue
            same_ok = (al * al * N2[a] == be * be * N2[b])
            rstar = (-qarb(al) / qarb(be)) * (qarb(N2[a]) / qarb(N2[b])).sqrt()
            ZT.setdefault((a, b), []).append((c, same_ok, rstar))
print('directions', ND, 'separation', SEP, 'smallest |det| above the filter', minnz, 'pairs with coplanar third line', len(ZT), flush=True)
assert SEP > 1e-3 and minnz > 1e-4

FAMS_A = {'C6', 'O8', 'D12', 'I12', 'RT24'}; FAMS_B = {'C6', 'O8', 'D12p', 'I12p', 'RT24p'}

# ---------- exact simplicial test of a set of central planes (normals = exact direction indices) ----------
def canon(v):
    for t in v:
        if not is0(t):
            return tuple((x / t).key() for x in v)
    return None
SIMP = {}
def simplicial(lines):
    key = tuple(sorted(lines))
    if key in SIMP: return SIMP[key]
    L = list(key); pts = {}
    for i, j in itertools.combinations(range(len(L)), 2):
        p = canon(q5.cross(VX[L[i]], VX[L[j]]))
        pts.setdefault(p, set()).update((i, j))
    f0 = len(pts); f1 = sum(len(s) for s in pts.values()); f2 = 1 - f0 + f1
    rank3 = f0 > 1
    out = dict(planes=len(L), f0=f0, f1=f1, f2=f2, simplicial=bool(rank3 and 3 * f2 == 2 * f1),
               regions_sphere=2 * f2, max_mult=max(len(s) for s in pts.values()))
    SIMP[key] = out; return out

# ---------- depth balls ----------
ENC = {}
for s in ('2a', '2caps', '2caps2', '2caps3'):
    for line in gzip.open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'certify%s.jsonl.gz' % s), 'rt'):
        d = json.loads(line); t = d.get('tight') or {}
        if t.get('ok') and t.get('enclosure'): ENC[(d['study'], int(d['sid']))] = t['enclosure']

FRAME = list(GR.ALLG)          # the 144 distinct frame maps (Oh and Ih share Th)

def group_of(idx, sizes):
    lab = np.repeat(np.arange(len(sizes)), sizes); P = DIRS[idx]; G = []
    for g in FRAME:
        img = P @ np.asarray(g).T; d2 = np.linalg.norm(img[:, None, :] - P[None, :, :], axis=2); j = d2.argmin(1)
        if d2.min(1).max() < 1e-9 and all(lab[j] == lab) and len(set(j.tolist())) == len(j):
            G.append((np.asarray(g), j))
    return G

def work(rec):
    t0 = time.time()
    idx, sizes = [int(x) for x in rec['idx']], [int(x) for x in rec['sizes']]; N = len(idx)
    orb = np.repeat(np.arange(len(sizes)), sizes)
    V, inc = C.combinatorics(idx, sizes, rec['depths'])
    out = dict(part=rec['part'], study=rec['study'], sid=int(rec['sid']), name=rec['name'], label=rec.get('label', ''),
               group=rec['group'], m=len(sizes), N=N, corners=len(V))
    if len(V) != int(rec['corners']): out['fail'] = 'corner count'; return out
    # depth balls per orbit
    if rec['prec60']:
        dep = [arb(arb(str(x)).mid(), 1e-55) for x in rec['depths']]; out['depth_source'] = '60 digits'
    else:
        e = ENC.get((rec['study'], int(rec['sid']))); dfl = [float(x) for x in rec['depths']]; dep = None
        if e:
            eb = [arb(x) for x in e]
            if len(eb) == len(sizes) - 1 and abs(dfl[0] - 1) < 1e-15: eb = [arb(1)] + eb     # first orbit fixed at depth 1
            if len(eb) == len(sizes) and all(abs(float(b.mid()) - x) < 1e-9 for b, x in zip(eb, dfl)):
                dep = eb; out['depth_source'] = 'certified enclosure'
        if dep is None: dep = [arb(x, 1e-9) for x in dfl]; out['depth_source'] = 'float (uncertified, +-1e-9)'
    # edges: faces sharing two corners
    cnt = {}
    for I in inc:
        for a, b in itertools.combinations(sorted(I), 2): cnt[(a, b)] = cnt.get((a, b), 0) + 1
    edges = [ab for ab, c in cnt.items() if c >= 2]
    nV, nE = len(V), len(edges)
    out['edges'] = nE; out['euler_ok'] = (nV - nE + N == 2)
    lines = sorted({LINE[i] for i in idx})
    face_of_line = {}
    for k, i in enumerate(idx): face_of_line.setdefault(LINE[i], []).append(k)
    out['resonus'] = len(lines)
    # group, reflections
    G = group_of(idx, sizes); out['group_order'] = len(G)
    refl = []
    for g, j in G:
        if np.linalg.det(g) < 0 and abs(np.trace(g) - 1) < 1e-9:
            w, vec = np.linalg.eigh((g + g.T) / 2); r = vec[:, int(np.argmin(w))]; refl.append((r, j))
    out['mirrors'] = len(refl)
    # Vacuus plates parallel to Resonus planes (exact)
    rv_lines = set(); edge_hits = [False] * nE; cands = []
    for t, (k, j) in enumerate(edges):
        a, b = idx[k], idx[j]
        for (c, same_ok, rstar) in ZT.get((a, b), []):
            if LINE[c] not in face_of_line: continue
            if orb[k] == orb[j]:
                hit = same_ok
            else:
                ratio = dep[orb[j]] / dep[orb[k]]
                if ratio.overlaps(rstar):
                    cands.append([k, j, int(c)]); hit = False
                else: hit = False
            if hit: rv_lines.add(LINE[c]); edge_hits[t] = True
    out['RV'] = len(rv_lines); out['R_sub_V'] = (len(rv_lines) == len(lines)); out['V_sub_R'] = all(edge_hits)
    out['candidates'] = cands[:10]; out['n_candidates'] = len(cands)
    # mirror laws
    def swapped(k, j): return any(jj[k] == j and jj[j] == k for _, jj in refl)
    v_on_m = [swapped(k, j) for (k, j) in edges]
    m_in_v = [any(jj[k] == j for (k, j) in edges) for _, jj in refl]
    out['V_sub_M'] = all(v_on_m); out['M_sub_V'] = all(m_in_v); out['V_eq_M'] = out['V_sub_M'] and out['M_sub_V']
    def is_mirror_normal(u): return any(abs(abs(float(r @ u)) - 1) < 1e-9 for r, _ in refl)
    r_on_m = [is_mirror_normal(DIRS[l]) for l in lines]
    m_in_r = [any(abs(abs(float(r @ DIRS[l])) - 1) < 1e-9 for l in lines) for r, _ in refl]
    out['R_sub_M'] = all(r_on_m); out['M_sub_R'] = all(m_in_r); out['R_eq_M'] = out['R_sub_M'] and out['M_sub_R']
    out['R_on_mirrors'] = sum(r_on_m); out['V_edges_on_mirrors'] = sum(v_on_m)
    fams = {DFAM[i] for i in idx}
    out['hubA'] = fams <= FAMS_A; out['hubB'] = fams <= FAMS_B
    out['res_arr'] = simplicial(lines)
    # harmonious Sphericus candidates (Theorem: Resonus = 3 perpendicular planes <=> box; Vacuus <=> axial octahedron)
    perp3 = len(lines) == 3 and all(abs(float(DIRS[x] @ DIRS[y])) < 1e-12 for x, y in itertools.combinations(lines, 2))
    out['res_harmonious'] = perp3
    out['vac_axial_octahedron'] = (N == 8 and nV == 6)
    out['sec'] = round(time.time() - t0, 3)
    return out

def tacitus_index():
    """name -> beyond list, keyed by (study short, sid) or by (batch, sorted idx)"""
    T = {}
    for f in ('aequi-0.jsonl', 'aequi-1.jsonl', 'aequi-2.jsonl'):
        for line in open(os.path.join(ST, '2026-11-25-tacitus', 'data', f)):
            d = json.loads(line); T[d['name']] = d
    cat = {}
    batches = {}
    for row in csv.DictReader(open(os.path.join(ST, '2026-11-24-aequi-catalogue-2', 'catalogue.csv'))):
        b = row['source_batch']
        if b == 'reserved': continue
        if b not in batches:
            batches[b] = json.load(gzip.open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'aequi%s.json.gz' % b)))['new']
        d = batches[b][int(row['source_id'])]
        cat[(b, tuple(sorted(d['idx'])))] = (row['No'], row['name_shown'])
    return T, cat

if __name__ == '__main__':
    outp, npr = sys.argv[1], int(sys.argv[2]); lim = int(sys.argv[3]) if len(sys.argv) > 3 else None
    recs = PA.records()
    print('dice', len(recs), flush=True)
    if lim: recs = recs[:lim // 2] + recs[-(lim - lim // 2):]
    T, cat = tacitus_index()
    EQ = {}
    for line in gzip.open(os.path.join(ST, '2026-11-25-inversions', 'data', 'polar-aequi.jsonl.gz'), 'rt'):
        d = json.loads(line); EQ[(d['part'], d['study'], int(d['sid']))] = not d['unequal_proved']
    res = []; t0 = time.time()
    with Pool(npr) as pool, open(outp, 'w') as fo:
        for k, o in enumerate(pool.imap(work, recs, chunksize=8)):
            rec = recs[k]
            if o['part'] in ('1232', '4404'):
                tn = '%s:%d' % (o['study'][:10], o['sid'])
            else:
                b = o['part']; c = cat.get((b, tuple(sorted(int(x) for x in rec['idx']))))
                tn = 'No.%s' % c[0] if c else None
                if c: o['No'] = int(c[0]); o['name'] = c[1]
            t = T.get(tn) if tn else None
            o['tacitus_name'] = tn if t else None
            o['tacitus_beyond'] = (t['i']['beyond'] if t else None)
            o['equal_curvature'] = EQ.get((o['part'], o['study'], o['sid']))
            res.append(o); fo.write(json.dumps(o) + '\n')
            if (k + 1) % 500 == 0: print('PROGRESS %.3f %d dice %.0fs' % ((k + 1) / len(recs), k + 1, time.time() - t0), flush=True)
    bad = [o for o in res if 'fail' in o or not o['euler_ok']]
    def c(f): return sum(1 for o in res if f(o))
    print('dice', len(res), 'failures', len(bad), [(o['part'], o['sid'], o.get('fail')) for o in bad[:10]])
    print('depth sources', {s: c(lambda o, s=s: o.get('depth_source') == s) for s in ('60 digits', 'certified enclosure', 'float (uncertified, +-1e-9)')})
    print('Tacitus joined', c(lambda o: o['tacitus_beyond'] is not None), '| equal curvature joined', c(lambda o: o['equal_curvature'] is not None))
    print('R∩V nonempty', c(lambda o: o['RV'] > 0), '| max', max(o['RV'] for o in res))
    print('R ⊆ V', c(lambda o: o['R_sub_V']), '| V ⊆ R', c(lambda o: o['V_sub_R']), '| R = V', c(lambda o: o['R_sub_V'] and o['V_sub_R']))
    print('different-orbit candidates (balls overlap)', c(lambda o: o['n_candidates'] > 0))
    print('V = mirrors', c(lambda o: o['V_eq_M']), '| V ⊆ mirrors', c(lambda o: o['V_sub_M']), '| R = mirrors', c(lambda o: o['R_eq_M']), '| R ⊆ mirrors', c(lambda o: o['R_sub_M']))
    print('Resonus in hub A', c(lambda o: o['hubA']), 'hub B', c(lambda o: o['hubB']), 'either', c(lambda o: o['hubA'] or o['hubB']))
    print('simplicial Resonus', c(lambda o: o['res_arr']['simplicial']), '| distinct Resonus arrangements', len({(o['resonus'], o['res_arr']['f0'], o['res_arr']['f1']) for o in res}))
    print('Tacitus beyond', c(lambda o: o['tacitus_beyond']), '| ∧ simplicial Resonus', c(lambda o: o['tacitus_beyond'] and o['res_arr']['simplicial']))
    print('equal curvature', c(lambda o: o['equal_curvature']))
    print('harmonious Resonus', c(lambda o: o['res_harmonious']), '| axial octahedra', c(lambda o: o['vac_axial_octahedron']))
    if not bad and len(res) == len(recs): print('FINAL ok')
