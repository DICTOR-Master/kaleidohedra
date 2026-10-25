"""Part G (exact, sympy): contact maps rho(lambda) for every 3D two-kind census network, the like-contact (Pauling)
windows, every flip / hinge / named stop translated into a radius ratio, the 'max-packing' map, hcp-hole site
identification, the C15 / A15 like-contact models, and the perovskite walls in Goldschmidt (t, mu_oct) coordinates.

Reads the relay census (../../2026-10-25-relay-census/scripts/networks.py and data/raw/relay-summary.json, perovskite.json).
Writes ../data/raw/geometry.json and ../data/checks/geometry-checks.txt."""
import json, os, sys, itertools
from fractions import Fraction as Fr
import sympy as sp

here = os.path.dirname(os.path.abspath(__file__))
census = os.path.join(here, '..', '..', '2026-10-25-relay-census')
sys.path.insert(0, os.path.join(census, 'scripts'))
from networks import NETS  # noqa: E402

relay = json.load(open(os.path.join(census, 'data', 'raw', 'relay-summary.json')))
CHECKS = []


def check(name, ok, detail=''):
    CHECKS.append((name, bool(ok), detail))
    if not ok:
        print('FAIL', name, detail)


S = lambda x: sp.nsimplify(sp.sympify(str(x)))  # exact sympy number from census strings
lam, rA, rB, d, rho, x, t = sp.symbols('lam r_A r_B d rho x t', real=True)


# ---------------------------------------------------------------- distances from the census site sets (exact)
def d2(G, p, q):
    v = [Fr(a) - Fr(b) for a, b in zip(p, q)]
    return sum(v[i] * Fr(G[i][j]) * v[j] for i in range(len(v)) for j in range(len(v)))


def min_d2(net, k1, k2):
    G, T, motif = net['G'], net['T'], net['motif']
    best = None
    for (ka, pa), (kb, pb) in itertools.product(motif, motif):
        if ka != k1 or kb != k2:
            continue
        for n in itertools.product(range(-2, 3), repeat=len(T)):
            q = [Fr(pb[i]) + sum(n[j] * Fr(T[j][i]) for j in range(len(T))) for i in range(len(pb))]
            dd = d2(G, pa, q)
            if dd > 0 and (best is None or dd < best):
                best = dd
    return best


# ---------------------------------------------------------------- G1: the general contact map
sol = sp.solve([rA + rB - d, rA**2 - rB**2 - lam], [rA, rB], dict=True)[0]
rho_map = sp.simplify(sol[rA] / sol[rB])
check('G1 contact map: r_A + r_B = d and r_A^2 - r_B^2 = lam give rho = r_A/r_B = (d^2+lam)/(d^2-lam)',
      sp.simplify(rho_map - (d**2 + lam) / (d**2 - lam)) == 0, str(rho_map))
check('G1 r_A - r_B = lam/d', sp.simplify(sol[rA] - sol[rB] - lam / d) == 0)


def rho_of(lv, D2):
    return sp.nsimplify(sp.simplify((D2 + lv) / (D2 - lv))) if lv != D2 else sp.oo


# regressions against the physical-anchors study
lam_golden = (x - 1) / (x + 1)  # census: golden loop lam = (x-1)/(x+1) in half-edge units, d^2 = 3
check('G1 regression golden: rho_small/big = (x+2)/(2x+1)',
      sp.simplify((3 - lam_golden) / (3 + lam_golden) - (x + 2) / (2 * x + 1)) == 0)
lam_delian = sp.Rational(3, 8) * (2 * t - 1)
check('G1 regression Delian: rho_tet/oct = t/(1-t)',
      sp.simplify((sp.Rational(3, 8) + lam_delian) / (sp.Rational(3, 8) - lam_delian) - t / (1 - t)) == 0)

NETS3 = ['bcc', 'nacl', 'zincblende', 'delian', 'hcpholes', 'a15', 'c15']
PAULING = {'bcc': sp.sqrt(3) - 1, 'nacl': sp.sqrt(2) - 1, 'zincblende': sp.sqrt(sp.Rational(3, 2)) - 1,
           'delian': sp.sqrt(sp.Rational(3, 2)) - 1}
out = {'nets': {}}


def max_pack_lambda(rv, D, lA, lB):
    """largest non-overlapping packing on the fixed sites with r_A/r_B = rv: r_B = s, r_A = rv*s."""
    s = sp.Min(lB / 2, lA / (2 * rv), D / (1 + rv))
    return s**2 * (rv**2 - 1)


def solve_max_pack(lv, D, lA, lB):
    """all rho > 0 with max-packing lambda(rho) = lv, branch by branch (exact)."""
    sols = []
    for name, s in [('B-B contact', lB / 2), ('A-A contact', lA / (2 * rho)), ('A-B contact', D / (1 + rho))]:
        for r in sp.solve(sp.Eq(s**2 * (rho**2 - 1), lv), rho):
            r = sp.nsimplify(sp.simplify(r))
            if not (r.is_real and r > 0):
                continue
            s_true = sp.Min(lB / 2, lA / (2 * r), D / (1 + r))
            if sp.simplify(s_true - s.subs(rho, r)) == 0:
                sols.append((name, r))
    return sols


for k in NETS3:
    net, rs = NETS[k], relay[k]
    A, B = net['A'], net['B']
    D2 = min_d2(net, A, B)
    lA2, lB2 = min_d2(net, A, A), min_d2(net, B, B)
    D, lA, lB = sp.sqrt(sp.Rational(D2)), sp.sqrt(sp.Rational(lA2)), sp.sqrt(sp.Rational(lB2))
    lo, hi = S(rs['range'][0]), S(rs['range'][1])
    rec = dict(A=A, B=B, d2=str(D2), likeA2=str(lA2), likeB2=str(lB2), range=[str(lo), str(hi)],
               range_is_pm_d2=bool(lo == -D2 and hi == D2))
    # unlike-contact window (both like pairs not overlapping)
    w_lo, w_hi = sp.simplify((D - lB) * D), sp.simplify((lA - D) * D)
    rec['window_lambda'] = [str(w_lo), str(w_hi)] if w_lo <= w_hi else 'EMPTY'
    rec['window_rho'] = ([str(sp.nsimplify(sp.radsimp(rho_of(w_lo, D2)))), str(sp.nsimplify(sp.radsimp(rho_of(w_hi, D2))))]
                         if w_lo <= w_hi else 'EMPTY')
    if k in PAULING:
        pa = PAULING[k]
        lo_r = sp.radsimp(rho_of(w_lo, D2))
        # the Pauling limit is r_small/r_large; check it appears as a window end (either orientation)
        ok = any(sp.simplify(e - pa) == 0 or sp.simplify(1 / e - pa) == 0 for e in [lo_r, sp.radsimp(rho_of(w_hi, D2))])
        check(f'G2 {k}: unlike-contact window end = Pauling limit {pa}', ok, f'window rho = {rec["window_rho"]}')
    # stops -> radius ratio
    stops = []
    for f in rs['flips']:
        stops.append(('flip' + (' (hinge)' if f in (rs.get('hinge') or []) else ''), S(f)))
    for n in rs.get('named', []):
        if n.get('lam') not in (None, 'all') and 'area' not in n.get('what', ''):
            stops.append(('named: ' + n['what'], S(n['lam'])))
    stops += [('range end', lo), ('range end', hi)]
    seen, srec = set(), []
    for what, lv in stops:
        key = (what.split(':')[0], sp.srepr(lv))
        if key in seen:
            continue
        seen.add(key)
        r_contact = rho_of(lv, D2) if abs(lv) <= D2 else None   # contact map needs |lam| <= d^2 (radii >= 0)
        mp = solve_max_pack(lv, D, lA, lB)
        in_win = (w_lo <= w_hi) and bool(w_lo <= lv <= w_hi)
        srec.append(dict(what=what, lam=str(lv), lam_float=float(lv),
                         rho_contact=None if r_contact is None else str(sp.radsimp(r_contact)),
                         rho_contact_float=None if r_contact is None or r_contact == sp.oo else float(r_contact),
                         in_touching_window=in_win,
                         rho_max_packing=[(b, str(r), float(r)) for b, r in mp]))
    rec['stops'] = srec
    # theorem check: at each window edge the touching like pair still has a face, strictly inside its life
    lives = rs['orbits']
    def life(key):
        s = lives[key]
        a, b = s[1:-1].split(',')
        return S(a), S(b), s[0], s[-1]
    if w_lo <= w_hi:
        for edge, kind, l2 in [(w_lo, B, lB2), (w_hi, A, lA2)]:
            key = f'{kind}-{kind}@{l2}'
            if key in lives:
                a, b, _, _ = life(key)
                check(f'G3 {k}: like contact {kind}-{kind} at lam = {edge} lies strictly inside the life {lives[key]}',
                      bool(a < edge < b), f'gap to life ends {float(edge - a):.4f}, {float(b - edge):.4f}')
            else:
                check(f'G3 {k}: like orbit {key} has a life', False, 'missing')
    out['nets'][k] = rec

# exact numbers that the README quotes
nacl = out['nets']['nacl']
check('G4 NaCl hinge lam=0 is rho = 1 (equal radii)', nacl['stops'][0]['rho_contact'] == '1')
zb = out['nets']['zincblende']
check('G4 zinc blende flips +-1 are rho_Zn/S = 1/2 and 2', {s['rho_contact'] for s in zb['stops'] if s['what'] == 'flip'} == {'1/2', '2'})
bcc = out['nets']['bcc']
check('G4 CsCl flips +-1 are rho_big/small = 1/2 and 2 (contact map)', {s['rho_contact'] for s in bcc['stops'] if s['what'] == 'flip'} == {'1/2', '2'})
check('G4 CsCl flips are reached by the max-packing map only at rho = 0 or infinity (no positive solution)',
      all(len(s['rho_max_packing']) == 0 or all(abs(r[2]) < 1e-12 for r in s['rho_max_packing'])
          for s in bcc['stops'] if s['what'] == 'flip'))
de = out['nets']['delian']
check('G4 fluorite octet hinge -1/8 is rho_tet/oct = 1/2', [s['rho_contact'] for s in de['stops'] if 'hinge' in s['what']] == ['1/2'])
check('G4 zinc blende and CsCl: same d^2 = 3 and same flips, so same rho at the flips', zb['d2'] == bcc['d2'] == '3')
c15 = out['nets']['c15']
check('G4 C15: unlike-contact window is EMPTY (sqrt11 > sqrt3 + sqrt2: Mg-Cu never touch when like spheres do not overlap)',
      c15['window_lambda'] == 'EMPTY' and sp.sqrt(11) > sp.sqrt(3) + sp.sqrt(2))

# ---------------------------------------------------------------- G5: C15 Laves like-contact models (edge 8)
q = sp.symbols('q', positive=True)  # q = r_Mg / r_Cu
lam_MgMg = 3 - 3 / q**2          # Mg-Mg contact: r_Mg = sqrt3, r_Cu = sqrt3/q
lam_CuCu = 2 * q**2 - 2          # Cu-Cu contact: r_Cu = sqrt2, r_Mg = sqrt2 q
ideal = sp.sqrt(sp.Rational(3, 2))
check('G5 C15 ideal ratio (both like contacts) = sqrt(3/2) and lam = 1', sp.simplify(lam_MgMg.subs(q, ideal) - 1) == 0 and sp.simplify(lam_CuCu.subs(q, ideal) - 1) == 0)
# max-packing on C15 is Cu-Cu contact for q <= sqrt(3/2), Mg-Mg contact above; unlike never binding in the range used
check('G5 C15 max packing: unlike pair not overlapping on both branches for q in [1, 1.7]',
      all(float(sp.sqrt(2) * (1 + qq)) <= float(sp.sqrt(11)) for qq in [1, 1.2247]) and
      all(float(sp.sqrt(3) * (1 + 1 / qq)) <= float(sp.sqrt(11)) for qq in [1.2247, 1.7]))
lam_sup = sp.limit(lam_MgMg, q, sp.oo); lam_inf = sp.limit(lam_CuCu, q, 0)
check('G5 C15: the max-packing lambda stays in (-2, 3) for every ratio, so flips -5, 7, 9 are unreachable',
      lam_sup == 3 and lam_inf == -2 and -5 < lam_inf and lam_sup < 7)
laves_range = (sp.Rational(105, 100), sp.Rational(168, 100))   # Costa et al. 1992 (observed r_A/r_B 1.05-1.68)
hs_range = (sp.Rational(119, 100), sp.Rational(135, 100))      # hard-sphere Laves window (Lindquist et al. 2018, citing Hynninen et al. 2007)
def lam_c15_maxpack(qq):
    return lam_CuCu.subs(q, qq) if qq <= ideal else lam_MgMg.subs(q, qq)
out['c15_laves'] = dict(
    ideal_q='sqrt(3/2)', ideal_lam='1',
    observed_q=[str(v) for v in laves_range], observed_lam_maxpack=[float(lam_c15_maxpack(v)) for v in laves_range],
    hardsphere_q=[str(v) for v in hs_range], hardsphere_lam_maxpack=[float(lam_c15_maxpack(v)) for v in hs_range],
    flips=[-5, 7, 9], maxpack_lambda_range=['-2', '3'],
    flips_as_q_unlike_contact={f: float((11 + f) / sp.Integer(11 - f)) for f in [-5, 7, 9]},
    flips_as_q_MgMg_contact={f: [float(s) for s in sp.solve(sp.Eq(lam_MgMg, f), q)] for f in [-5, 7, 9]},
    flips_as_q_CuCu_contact={f: [float(s) for s in sp.solve(sp.Eq(lam_CuCu, f), q)] for f in [-5, 7, 9]})
check('G5 Laves observed range 1.05-1.68 maps inside the chamber (-5, 7)',
      all(-5 < v < 7 for v in out['c15_laves']['observed_lam_maxpack']))

# ---------------------------------------------------------------- G6: A15 (edge 2): Cr chain contact + ratio, ideal ratio
p = sp.symbols('p', positive=True)  # p = r_Si / r_Cr  (B-site / A-site of A3B)
lam_chain = (p**2 - 1) / 4                       # r_Cr = 1/2 (chains touch)
lam_unlike = sp.Rational(5, 4) * (p - 1) / (p + 1)  # unlike contact, d^2 = 5/4
p_ideal = sp.sqrt(5) - 1                          # chains touch AND Cr-Si touch
check('G6 A15 ideal ratio (Cr chain contact + Cr-Si contact) r_Si/r_Cr = sqrt5 - 1, lam = (5 - 2 sqrt5)/4',
      sp.simplify(lam_chain.subs(p, p_ideal) - (5 - 2 * sp.sqrt(5)) / 4) == 0 and sp.simplify(lam_unlike.subs(p, p_ideal) - (5 - 2 * sp.sqrt(5)) / 4) == 0)
out['a15'] = dict(ideal_p='sqrt(5) - 1', ideal_p_float=float(p_ideal), ideal_lam='(5 - 2*sqrt(5))/4',
                  flip_1_4={'chain_contact_p': str(sp.solve(sp.Eq(lam_chain, sp.Rational(1, 4)), p)), 'unlike_contact_p': str(sp.solve(sp.Eq(lam_unlike, sp.Rational(1, 4)), p))},
                  flip_3_4={'chain_contact_p': str(sp.solve(sp.Eq(lam_chain, sp.Rational(3, 4)), p)), 'unlike_contact_p': str(sp.solve(sp.Eq(lam_unlike, sp.Rational(3, 4)), p))},
                  SiSi_contact_with_chain_contact_p='sqrt(3)')
check('G6 A15 flip 1/4: p = sqrt2 (chain contact), 3/2 (unlike contact)', out['a15']['flip_1_4'] == {'chain_contact_p': '[sqrt(2)]', 'unlike_contact_p': '[3/2]'})
check('G6 A15 flip 3/4: p = 2 (chain contact), 4 (unlike contact)', out['a15']['flip_3_4'] == {'chain_contact_p': '[2]', 'unlike_contact_p': '[4]'})

# ---------------------------------------------------------------- G7: hcp holes - which real structures use these sites?
hn = NETS['hcpholes']; G = hn['G']
atoms = [(0, 0, 0), (Fr(1, 3), Fr(1, 3), Fr(1, 2))]   # the vertices of the gyrated octet (ideal hcp, edge 1)
def neigh(p, pts, r2):
    c = 0
    for a in pts:
        for n in itertools.product(range(-2, 3), repeat=3):
            if d2(G, p, [Fr(a[i]) + n[i] for i in range(3)]) == r2:
                c += 1
    return c
check('G7 hcp atoms at (0,0,0), (1/3,1/3,1/2) are ideal hcp: 12 neighbours at distance 1', neigh(atoms[0], atoms, 1) == 12)
oct_ok = all(neigh(pp, atoms, Fr(1, 2)) == 6 for kk, pp in hn['motif'] if kk == 'oct')
tet_ok = all(neigh(pp, atoms, Fr(3, 8)) == 4 for kk, pp in hn['motif'] if kk == 'tet')
check('G7 every census "oct" site has 6 hcp atoms at distance^2 1/2 (octahedral hole)', oct_ok)
check('G7 every census "tet" site has 4 hcp atoms at distance^2 3/8 (tetrahedral hole)', tet_ok)
check('G7 the oct-hole set is simple hexagonal, not hcp: oct-oct nearest distance^2 = 2/3 (along c), not 1',
      min_d2(hn, 'oct', 'oct') == Fr(2, 3))
check('G7 tet holes come in face-sharing pairs at distance^2 1/6 (shorter than the oct-tet distance^2 3/8)',
      min_d2(hn, 'tet', 'tet') == Fr(1, 6))
out['hcpholes_identification'] = {
    'hcp atoms (the third, missing kind)': '(0,0,0), (1/3,1/3,1/2) in the census 60-degree basis',
    'NiAs': 'cations = all census oct sites; anions = the hcp atoms (not in the census network); census tet sites empty',
    'wurtzite': 'cations = one tet site of each face-sharing pair (half of the census tet sites, one polarity); anions = hcp atoms; oct sites empty',
    'conclusion': 'no real two-kind structure found with exactly these two site sets; the census oct-tet contact is hole-to-hole, not cation-anion'}

# ---------------------------------------------------------------- G8: perovskite walls in Goldschmidt coordinates
tt, m, rx = sp.symbols('t mu_oct r_X', positive=True)
# scale-free radii relative to r_X = 1: r_B = m, r_A = sqrt2 t (1 + m) - 1  (definition of t)
RA = sp.sqrt(2) * tt * (1 + m) - 1
check('G8 Goldschmidt t from r_A = sqrt2 t (1+mu) - 1 (r_X = 1)', sp.simplify((RA + 1) / (sp.sqrt(2) * (m + 1)) - tt) == 0)
# lattice set by the tighter contact; cell edge 2: B-X = 1, A-X = sqrt2
sBX = 1 / (m + 1)              # B-X contact scale (t <= 1)
sAX = sp.sqrt(2) / (RA + 1)    # A-X contact scale (t >= 1)
def lm(scale):
    return sp.simplify(scale**2 * (RA**2 - 1)), sp.simplify(scale**2 * (m**2 - 1))
L1, M1 = lm(sBX)
check('G8 with B-X contact: mu = (mu_oct - 1)/(mu_oct + 1)', sp.simplify(M1 - (m - 1) / (m + 1)) == 0)
wall_AA = sp.solve(sp.Eq(RA, 1), tt)[0]                       # lam = 0  <=>  r_A = r_X (scale-free)
wall_AB = [s for s in sp.solve(sp.Eq(RA**2 + 2 * m**2, 3), tt)]  # lam + 2 mu = 0 <=> r_A^2 + 2 r_B^2 = 3 r_X^2 (scale-free)
wall_XX_BX = sp.solve(sp.Eq(sp.simplify(L1 + M1), 1), tt)       # lam + mu = 1 with B-X contact
check('G8 wall lam = 0 is t = sqrt2/(1 + mu_oct) (r_A = r_X)', sp.simplify(wall_AA - sp.sqrt(2) / (1 + m)) == 0)
# X-X wall with B-X contact: r_A^2 = 3 + 2 mu_oct (r_X = 1) -- check
xx_closed = (sp.sqrt(3 + 2 * m) + 1) / (sp.sqrt(2) * (1 + m))
check('G8 wall lam + mu = 1 (B-X contact) is r_A^2 = (3 + 2 mu_oct) r_X^2, i.e. t = (1 + sqrt(3 + 2 mu_oct))/(sqrt2 (1 + mu_oct))',
      any(sp.simplify(s - xx_closed) == 0 for s in wall_XX_BX))
# A-B wall for the relevant root
ab_closed = (1 + sp.sqrt(3 - 2 * m**2)) / (sp.sqrt(2) * (1 + m))
check('G8 wall lam + 2 mu = 0 is r_A^2 + 2 r_B^2 = 3 r_X^2, t = (1 + sqrt(3 - 2 mu_oct^2))/(sqrt2 (1 + mu_oct))',
      any(sp.simplify(s - ab_closed) == 0 for s in wall_AB))
# X-X wall with A-X contact (t >= 1): scale sqrt2/(r_A + 1); lam + mu = 1  <=>  r_A = 1 + sqrt(6 - 2 mu^2)
L2, M2 = lm(sAX)
xx_AX = (2 + sp.sqrt(6 - 2 * m**2)) / (sp.sqrt(2) * (1 + m))
check('G8 wall lam + mu = 1 with A-X contact: t = (2 + sqrt(6 - 2 mu_oct^2))/(sqrt2 (1 + mu_oct))',
      sp.simplify((L2 + M2 - 1).subs(tt, xx_AX)) == 0)
check('G8 for mu_oct in [0.35, 0.65] the A-B and X-X walls lie at t > 1.0 (outside the perovskite range t <= 1)',
      all(float(ab_closed.subs(m, mv)) > 1 and float(xx_AX.subs(m, mv)) > 1 for mv in [0.35, 0.45, 0.55, 0.65]))
# Pauling octahedral limit: X-X contact with B-X contact at mu_oct = sqrt2 - 1; t = 1 with r_A = r_X there
check('G8 ideal all-touching perovskite: mu_oct = sqrt2 - 1, t = 1, r_A = r_X (on the A-A wall)',
      sp.simplify(wall_AA.subs(m, sp.sqrt(2) - 1) - 1) == 0)
# X-X contact (Pauling 0.414) vs census X-X wall: X-X face dies where?  at B-X contact the X-X wall needs r_A^2 = 3 + 2 mu
out['perovskite'] = dict(
    radii_rel_rX='r_B = mu_oct, r_A = sqrt2 t (1 + mu_oct) - 1',
    wall_AA_t='sqrt(2)/(1 + mu_oct)   [lam = 0 <=> r_A = r_X]',
    wall_AB_t='(1 + sqrt(3 - 2 mu_oct^2))/(sqrt2 (1 + mu_oct))   [lam + 2 mu = 0 <=> r_A^2 + 2 r_B^2 = 3 r_X^2]',
    wall_XX_t_BXcontact='(1 + sqrt(3 + 2 mu_oct))/(sqrt2 (1 + mu_oct))   [lam + mu = 1 <=> r_A^2 = (3 + 2 mu_oct) r_X^2]',
    wall_XX_t_AXcontact='(2 + sqrt(6 - 2 mu_oct^2))/(sqrt2 (1 + mu_oct))   [lam + mu = 1 with A-X contact (t >= 1)]',
    note='for t > 1 the lattice is fixed by A-X contact; the X-X wall is then the A-X-contact form; the B-X form is listed only where it is <= 1',
    table=[dict(mu_oct=float(mv), t_AA=float(wall_AA.subs(m, mv)), t_AB=float(ab_closed.subs(m, mv)),
                t_XX=float(xx_closed.subs(m, mv)) if float(xx_closed.subs(m, mv)) <= 1 else float(xx_AX.subs(m, mv)))
           for mv in [sp.Rational(4, 10), sp.sqrt(2) - 1, sp.Rational(45, 100), sp.Rational(5, 10), sp.Rational(6, 10), sp.Rational(7, 10)]])
# t is invariant under the IR -> CR convention shift (cation +delta, anion -delta)
dl = sp.symbols('delta')
a_, b_, x_ = sp.symbols('a b x', positive=True)
tdef = lambda A_, B_, X_: (A_ + X_) / (sp.sqrt(2) * (B_ + X_))
check('G9 Goldschmidt t is unchanged by a uniform cation +delta / anion -delta shift (IR -> CR)',
      sp.simplify(tdef(a_ + dl, b_ + dl, x_ - dl) - tdef(a_, b_, x_)) == 0)
check('G9 two-kind contact: d = r+ + r- unchanged, lambda shifts by 2 delta d (in the units of d)',
      sp.simplify(((a_ + dl) - (x_ - dl)) * (a_ + x_) - (a_ - x_) * (a_ + x_) - 2 * dl * (a_ + x_)) == 0)

out['skipped_2d'] = ('square + centres, honeycomb + centres and kagome + centres: no real two-kind 2D crystal family was found '
                     'whose two kinds touch as unlike neighbours on these exact sites; skipped as instructed')

os.makedirs(os.path.join(here, '..', 'data', 'raw'), exist_ok=True)
os.makedirs(os.path.join(here, '..', 'data', 'checks'), exist_ok=True)
json.dump(out, open(os.path.join(here, '..', 'data', 'raw', 'geometry.json'), 'w'), indent=1, default=str)
with open(os.path.join(here, '..', 'data', 'checks', 'geometry-checks.txt'), 'w') as f:
    for n, ok, det in CHECKS:
        f.write(f"{'PASS' if ok else 'FAIL'}  {n}  {det}\n")
print(f"geometry: {sum(ok for _, ok, _ in CHECKS)} PASS, {sum(not ok for _, ok, _ in CHECKS)} FAIL")
