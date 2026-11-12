# LOCALITY of the six Laves roles, exact Farkas certificates (DICTO 12 Nov 2026; LEAD 1 of this study; method of #61 step 2).
# Claim certified: for every lam-window of #64's Laves walk, every role (M0 M1 K1 K2 K3 T) and every one of the 32 six-layer
# neighbourhoods (layers -2 .. 3 round gap 0), the power cell K of the role's site against the sites fixed by those six layers
# (lavgeom.inside_levels) is cut by NO other site of any stacking that extends the neighbourhood:
#   one certificate pow_i <= pow_j on K x window for each site j of gap 3 (its T site, both choices of layer 4), of gap -3 (both
#   choices of layer -3), and of the supersets of gaps 4 and -4 (all six ordered position pairs); plus zeta <= 4 and zeta >= -3 on K.
# Lateral dominance (lists within Q <= 4/3) and vertical dominance (gaps >= 5 by gap 4, gaps <= -5 by gap -4, given the zeta bounds)
# make the finite lists complete (README). Then each piece is the same in every stacking with that neighbourhood: locality.
# Controls: (C1) #61's own locality certificate (splash-rules/proof/locality.py at q0 = 1/3) reproduced: 1070 PASS 0 FAIL;
#   (C2) negative: the cell against FOUR layers (-1 .. 2) is NOT local: an exact witness (lam, p) with pow_j(p) < pow_i(p) for a site
#   of gap -2 or gap 2 must be found for M0 above 17/96 (M0 reads layer -2 there, this study); (C3) the model cell K against the census
#   engine (#64 raw walks, ABC and AC): face counts equal and float volume ratio model/engine one constant per stacking.
# Output: out/lavloc_<mode>.log, out/lavloc_<mode>.json (summary), out/lavloc_<mode>_certs.jsonl.gz (every certificate, for
# verify_lavloc.py). Usage: python3 lavloc.py pilot|full
import os, sys, json, gzip, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lavgeom import *
OUT = os.path.normpath(os.path.join(HERE, '..', 'out')); os.makedirs(OUT, exist_ok=True)
PROOF61 = os.path.normpath(os.path.join(HERE, '..', '..', '2026-10-27-splash-rules', 'proof'))
RAW = os.path.normpath(os.path.join(HERE, '..', '..', '2026-10-27-splash-rules', 'run2', 'raw'))
MODE = sys.argv[1] if len(sys.argv) > 1 else 'pilot'
WINDOWS = [(Fr(-11, 32), Fr(-5, 32)), (Fr(-5, 32), Fr(17, 96)), (Fr(17, 96), Fr(7, 32)), (Fr(7, 32), Fr(9, 32)), (Fr(9, 32), Fr(11, 32))]
NB = neighbourhoods()
if MODE == 'pilot': WINDOWS = [WINDOWS[2], WINDOWS[4]]
fails = []
def bad(msg): fails.append(msg); print('  !! ' + msg, flush=True)
def sref(s): return [str(s[0][0]), str(s[0][1]), str(s[1]), s[2]]

def build(P, role, lo_gap, hi_gap, lo, hi):
    i0 = gap_sites(0, P[0], P[1])[role]; ci, zi = i0[0], i0[1]; i = (ci, zi, i0[2])
    ins = expand(inside_levels(P, lo_gap, hi_gap), ci, zi)
    rows = [row(i, j) for j in ins] + domain_rows(lo, hi)
    refs = [['site'] + sref(j) for j in ins] + [['dom', 'lo'], ['dom', 'hi']]
    outl = outside_levels(P, lo_gap, hi_gap)
    outs = {g: expand(v, ci, zi) for g, v in outl.items()}
    return i, ins, rows, refs, outs

def exact_witness(i, j, rows, res):
    """exact check of a cut: z in K (all rows) and pow_i(z) > pow_j(z)"""
    z = res.get('z')
    if z is None: return None
    if any(sum(a[r] * z[r] for r in range(4)) > b for a, b in rows): return None
    a, b = row(i, j)
    return z if sum(a[r] * z[r] for r in range(4)) > b else None

def certify_case(P, role, lo_gap, hi_gap, lo, hi, sink=None, tag=None):
    """returns (n_pass, n_fail, list of exact cut witnesses, list of unresolved)"""
    i, ins, rows, refs, outs = build(P, role, lo_gap, hi_gap, lo, hi)
    K = Poly(rows); npass = nfail = 0; cuts = []; unres = []
    zb = [('zeta_hi', [Fr(0), Fr(0), Fr(0), Fr(1)], Fr(hi_gap + 2)), ('zeta_lo', [Fr(0), Fr(0), Fr(0), Fr(-1)], -Fr(lo_gap - 1))]
    tests = [(k, c, beta, None) for k, c, beta in zb]
    for g in ('near_up', 'near_dn', 'far_up', 'far_dn'):
        for j in outs[g]:
            a, b = row(i, j); tests.append((g, a, b, j))
    for g, c, beta, j in tests:
        res = K.lp_max(c)
        if res['status'].startswith('optimal') and res['value'] <= beta and check_cert(c, rows, res['y'], beta):
            npass += 1
            if sink is not None:
                sink.write(json.dumps({'case': tag, 'kind': g, 'j': sref(j) if j else None, 'beta': str(beta),
                                       'y': [[refs[k], str(v)] for k, v in sorted(res['y'].items())]}) + '\n')
        else:
            nfail += 1
            w = exact_witness(i, j, rows, res) if (j is not None and res['status'] == 'optimal') else None
            if w is not None: cuts.append({'kind': g, 'j': sref(j), 'witness_lam_x_y_zeta': [str(x) for x in w], 'value': str(res['value']), 'beta': str(beta)})
            else: unres.append({'kind': g, 'j': sref(j) if j else None, 'status': res['status'], 'value': str(res.get('value', res.get('float')))})
    return npass, nfail, cuts, unres, len(ins)

# ---------------- (C1) #61 reproduced
def control_61():
    t0 = time.time(); sys.path.insert(0, PROOF61)
    import io, contextlib, locality
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): ok, badn = locality.certify(Fr(1, 3))
    sys.path.remove(PROOF61)
    print(f'  (C1) #61 step 2 reproduced: {ok} PASS {badn} FAIL (published: 1070 PASS, 0 FAIL), {time.time() - t0:.0f} s', flush=True)
    if (ok, badn) != (1070, 0): bad('C1 #61 certificate not reproduced')
    return {'pass': ok, 'fail': badn}

# ---------------- (C2) negative: four layers are not enough for M0 above 17/96
def control_nonlocal():
    out = {}; found = 0
    for lo, hi in [(Fr(17, 96), Fr(7, 32)), (Fr(7, 32), Fr(9, 32))]:
        for name in ('BCABCA', 'ACACAC', 'BCACBA', 'CBABCA'):
            P = NB[name]; npass, nfail, cuts, unres, _ = certify_case(P, 'M0', -1, 1, lo, hi)
            near = [c for c in cuts if c['kind'].startswith('near')]
            out[f'{lo},{hi},{name}'] = {'pass': npass, 'fail': nfail, 'cuts': cuts[:3], 'unresolved': unres[:3]}
            found += len(near) > 0
            print(f'  (C2) M0 cell against layers -1..2, window ({lo}, {hi}), neighbourhood {name}: {npass} PASS {nfail} FAIL, exact cuts by near sites {len(near)}'
                  + (f'; e.g. site {near[0]["j"]} at (lam, x, y, zeta) = {near[0]["witness_lam_x_y_zeta"]}' if near else ''), flush=True)
    if found == 0: bad('C2 negative control: no exact cut found for the four-layer M0 cell')
    return out

# ---------------- (C3) model cell against the census engine
def float_cell(P, role, lam):
    i, ins, rows, refs, outs = build(P, role, -2, 2, lam, lam)
    H = [(np.array([float(x) for x in a[1:]]), float(b - a[0] * lam)) for a, b in rows[:-2]]
    A = np.array([h[0] for h in H]); bb = np.array([h[1] for h in H]); nr = np.linalg.norm(A, axis=1)
    r = linprog(np.r_[0, 0, 0, -1.0], A_ub=np.c_[A, nr], b_ub=bb, bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    hs = HalfspaceIntersection(np.c_[A, -bb], r.x[:3]); V = hs.intersections
    J = np.array([[1, .5, 0], [0, np.sqrt(3) / 2, 0], [0, 0, np.sqrt(2 / 3)]])     # hex basis -> Cartesian
    Vc = V @ J.T; vol = ConvexHull(Vc).volume
    nf = sum(1 for k in range(len(H)) if np.sum(np.abs(V @ A[k] - bb[k]) < 1e-7) >= 3 and np.linalg.matrix_rank(V[np.abs(V @ A[k] - bb[k]) < 1e-7] - V[np.abs(V @ A[k] - bb[k]) < 1e-7][0], tol=1e-7) == 2)
    return vol, nf

def control_engine():
    import sympy as sp
    out = {}
    for w, name in (('ABC', 'BCABCA'), ('AC', 'ACACAC')):
        d = json.load(open(os.path.join(RAW, f'lvw_{w}.json'))); P = {m: name[m + 2] for m in range(-2, 4)}
        assert P[0] == 'A' and P[1] == w[1], (w, P)
        ratios = []; fok = ftot = 0
        for lo, hi in WINDOWS_ALL:
            lam = (lo + hi) / 2
            iv = next(iv for iv in d['intervals'] if iv['lo'] not in (None, 'None') and Fr(iv['lo']) <= lo and hi <= Fr(iv['hi']))
            for ri, role in enumerate(ROLES):
                s = iv['sites'][ri]; ev = float(sp.sympify(s['volume']).subs('lam', sp.Rational(lam.numerator, lam.denominator)))
                vol, nf = float_cell(P, role, lam); ratios.append(vol / ev); ftot += 1; fok += (nf == s['faces'])
                if nf != s['faces']: print(f'    face count {w} {role} lam={lam}: model {nf}, engine {s["faces"]}', flush=True)
        spread = max(ratios) / min(ratios) - 1
        print(f'  (C3) model vs engine on {w}: face counts equal {fok}/{ftot}; volume ratio model/engine {min(ratios):.9f} .. {max(ratios):.9f} (spread {spread:.1e})', flush=True)
        if fok != ftot or spread > 1e-7: bad(f'C3 model vs engine on {w}')
        out[w] = {'faces_equal': fok, 'of': ftot, 'ratio_min': min(ratios), 'ratio_max': max(ratios)}
    return out

WINDOWS_ALL = [(Fr(-11, 32), Fr(-5, 32)), (Fr(-5, 32), Fr(17, 96)), (Fr(17, 96), Fr(7, 32)), (Fr(7, 32), Fr(9, 32)), (Fr(9, 32), Fr(11, 32))]

def main():
    t0 = time.time(); print(f'lavloc {MODE}: Laves locality certificates, six roles, {len(WINDOWS)} lam-windows', flush=True)
    rep = {'mode': MODE, 'controls': {}}
    rep['controls']['C3'] = control_engine()
    rep['controls']['C2'] = control_nonlocal()
    rep['controls']['C1'] = control_61()
    print(f'PROGRESS 0.05 controls done ({time.time() - t0:.0f} s)', flush=True)
    nbk = sorted(NB) if MODE == 'full' else ['BCABCA', 'ACACAC', 'BCACBA', 'CBABCA']
    total = len(WINDOWS) * len(ROLES); done = 0; tp = tf = 0; allcuts = []; allunres = []; rep['cases'] = []
    with gzip.open(os.path.join(OUT, f'lavloc_{MODE}_certs.jsonl.gz'), 'wt') as sink:
        for lo, hi in WINDOWS:
            for role in ROLES:
                cp = cf = 0
                for name in nbk:
                    tag = [str(lo), str(hi), role, name]
                    npass, nfail, cuts, unres, nin = certify_case(NB[name], role, -2, 2, lo, hi, sink, tag)
                    cp += npass; cf += nfail
                    for c in cuts: c['case'] = tag; allcuts.append(c)
                    for u in unres: u['case'] = tag; allunres.append(u)
                    rep['cases'].append({'case': tag, 'pass': npass, 'fail': nfail, 'inside_sites': nin})
                tp += cp; tf += cf; done += 1
                print(f'PROGRESS {0.05 + 0.95 * done / total:.3f} window ({lo}, {hi}) {role}: {len(nbk)} neighbourhoods, {cp} certificates PASS, {cf} FAIL ({time.time() - t0:.0f} s)', flush=True)
    rep.update(total_pass=tp, total_fail=tf, cuts=allcuts[:200], n_cuts=len(allcuts), unresolved=allunres[:200], n_unresolved=len(allunres), seconds=time.time() - t0)
    json.dump(rep, open(os.path.join(OUT, f'lavloc_{MODE}.json'), 'w'), indent=1, default=str)
    print(f'TOTAL {tp} certificates PASS, {tf} FAIL; exact cuts {len(allcuts)}; unresolved {len(allunres)}; {time.time() - t0:.0f} s', flush=True)
    for c in allcuts[:10]: print('  CUT', c, flush=True)
    for u in allunres[:10]: print('  UNRESOLVED', u, flush=True)
    if allunres: bad(f'{len(allunres)} cases neither certified nor cut exactly')
    verdict = 'LOCAL: every role, every window, every neighbourhood certified' if tf == 0 else f'NOT LOCAL: {len(allcuts)} exact cuts'
    print('VERDICT ' + verdict, flush=True)
    print('FINAL ok' if not fails else f'FINAL FAIL {fails}', flush=True)
    sys.exit(0 if not fails else 1)

if __name__ == '__main__': main()
