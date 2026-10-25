"""Part C: real compounds against the census stops (contact model), with Shannon radii (Imperial College transcription).
C1 alkali halides (B1 / B2; transition pressures), C2 AB tetrahedral vs rock-salt compounds, C3 titanate perovskites.
Every structure label and pressure is cited in DATA below; radii are read from ../data/raw/shannon.json.
Writes ../data/raw/compounds.json and ../data/checks/compounds-checks.txt."""
import json, os
from fractions import Fraction as Fr
import sympy as sp

here = os.path.dirname(os.path.abspath(__file__))
SH = json.load(open(os.path.join(here, '..', 'data', 'raw', 'shannon.json')))
CHECKS = []


def check(name, ok, detail=''):
    CHECKS.append((name, bool(ok), detail))
    if not ok:
        print('FAIL', name, detail)


def rad(el, charge, cn, kind='IR'):
    for r in SH[el]:
        if r['charge'] == charge and r['CN'] == cn and r['spin'] in ('', 'HS'):
            return Fr(r[kind]), r['key']
    raise KeyError((el, charge, cn))


DELTA = Fr(14, 100)  # IR -> CR convention shift per ion (scale-anomalies study; checked below against the table)
for el, ch, cn in [('Cs', 1, 'VIII'), ('Na', 1, 'VI'), ('Cl', -1, 'VI'), ('O', -2, 'VI'), ('Ti', 4, 'VI'), ('Zn', 2, 'IV'), ('S', -2, 'VI')]:
    ir, cr = rad(el, ch, cn, 'IR')[0], rad(el, ch, cn, 'CR')[0]
    check(f'C0 CR - IR = {"+" if ch > 0 else "-"}0.14 for {el}{ch:+d} {cn}', cr - ir == (DELTA if ch > 0 else -DELTA), f'{ir} -> {cr}')

PAULING8, PAULING6, PAULING4 = (sp.sqrt(3) - 1), (sp.sqrt(2) - 1), (sp.sqrt(sp.Rational(3, 2)) - 1)
out = {}

# ------------------------------------------------------------------ C1 alkali halides
# ambient structure: Weir & Piermarini 1964 (full text): all alkali halides are NaCl type except CsCl, CsBr, CsI (CsCl type).
# P_t: B1 -> B2 transition pressure, Weir & Piermarini 1964 Table 2 (read from the printed page image; units 10^9 dyn/cm^2
# = 0.1 GPa; values from Bridgman 1945, those in parentheses are their estimates). NaCl: ~30 GPa (Xu et al. 2024, citing
# Bassett et al. 1968).
PT = {'KI': (Fr(1785, 1000), 'measured'), 'KBr': (Fr(1805, 1000), 'measured'), 'KCl': (Fr(1968, 1000), 'measured'),
      'KF': (Fr(2), 'estimate'), 'RbI': (Fr(397, 1000), 'measured'), 'RbBr': (Fr(451, 1000), 'measured'),
      'RbCl': (Fr(490, 1000), 'measured'), 'RbF': (Fr(1176, 1000), 'estimate'), 'CsF': (Fr(2), 'estimate'),
      'NaCl': (Fr(30), 'about 30 (secondary)')}
halides = []
for M in ['Li', 'Na', 'K', 'Rb', 'Cs']:
    for X in ['F', 'Cl', 'Br', 'I']:
        name = M + X
        b2 = name in ('CsCl', 'CsBr', 'CsI')
        rows = {}
        for conv in ['IR', 'CR']:
            for cnm in (['VI', 'VIII'] if M == 'Cs' else ['VI']):
                rc, kc = rad(M, 1, cnm, conv)
                ra, ka = rad(X, -1, 'VI', conv)
                small, large = min(rc, ra), max(rc, ra)
                rho = small / large
                rows[f'{conv}-{cnm}'] = dict(r_cat=str(rc), r_an=str(ra), key_cat=kc, key_an=ka, rho_small_large=float(rho),
                                             rho_cat_an=float(rc / ra), pauling_says_B2=bool(rho >= PAULING8),
                                             nacl_side='cation larger (Na-Na faces)' if rc > ra else 'anion larger (Cl-Cl faces)',
                                             cscl_chamber='soft chamber (1/2, 1]' if rho > Fr(1, 2) else 'below flip 1/2')
        halides.append(dict(compound=name, ambient='B2 (CsCl type)' if b2 else 'B1 (NaCl type)', P_t_GPa=None if name not in PT else float(PT[name][0]),
                            P_t_status=None if name not in PT else PT[name][1], radii=rows))
out['alkali_halides'] = halides


def score(rows_key, pred):
    ok = sum(1 for h in halides if (pred(h['radii'][rows_key]) == h['ambient'].startswith('B2')))
    return ok


for conv in ['IR', 'CR']:
    key = f'{conv}-VI'
    s_p = score(key, lambda r: r['pauling_says_B2'])
    s_f = score(key, lambda r: r['rho_small_large'] > 0.5)
    out[f'halide_scores_{conv}'] = dict(pauling_0732=s_p, census_flip_05=s_f, n=len(halides))
# with actual CN for Cs (VIII)
s_p8 = sum(1 for h in halides if (h['radii']['IR-VIII' if h['compound'].startswith('Cs') else 'IR-VI']['pauling_says_B2'] == h['ambient'].startswith('B2')))
out['halide_scores_IR_CsVIII'] = dict(pauling_0732=s_p8, n=len(halides))
mis = [h['compound'] for h in halides if h['radii']['IR-VI']['pauling_says_B2'] != h['ambient'].startswith('B2')]
out['halide_pauling_misfits_IR_VI'] = mis
check('C1 20 alkali halides placed, 3 of them B2', len(halides) == 20 and sum(h['ambient'].startswith('B2') for h in halides) == 3)
cscl = [h for h in halides if h['compound'] == 'CsCl'][0]
check('C1 regression: CsCl rho (IR, Cs VIII) = 174/181 = 0.9613 (physical anchors)', abs(cscl['radii']['IR-VIII']['rho_small_large'] - 174 / 181) < 1e-12)


def spearman(xs, ys):
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        for k, i in enumerate(o):
            r[i] = k + 1
        return r
    rx, ry = rank(xs), rank(ys); n = len(xs)
    return 1 - 6 * sum((a - b) ** 2 for a, b in zip(rx, ry)) / (n * (n * n - 1))


meas = [h for h in halides if h['P_t_status'] == 'measured']
xs = [h['radii']['IR-VI']['rho_small_large'] for h in meas]; ys = [h['P_t_GPa'] for h in meas]
out['halide_Pt_spearman_measured'] = dict(n=len(meas), rho_spearman=spearman(xs, ys), compounds=[h['compound'] for h in meas])
# within each cation family: does P_t fall with rho?
fam = {}
for M in ['K', 'Rb']:
    hs = sorted([h for h in meas if h['compound'].startswith(M)],
                key=lambda h: h['radii']['IR-VI']['rho_small_large'])
    fam[M] = [(h['compound'], round(h['radii']['IR-VI']['rho_small_large'], 4), h['P_t_GPa']) for h in hs]
out['halide_Pt_by_family'] = fam
check('C1 within K and within Rb halides, P_t increases with rho (opposite to "nearer 0.732 -> easier B2")',
      all(all(a[2] < b[2] for a, b in zip(v, v[1:])) for v in fam.values()), str(fam))

# ------------------------------------------------------------------ C2 AB compounds: tetrahedral (ZB / wurtzite) vs rock salt
# structure labels: Wikipedia, 'Cubic crystal system' (rock-salt and zincblende example tables) and 'Wurtzite crystal
# structure' (examples), fetched 2026-10-25 -- secondary, general knowledge.  MgTe (listed rock salt there) left out:
# its ambient form is not settled in the sources read here.
AB = {'BeS': ('Be', 2, 'S', 'ZB'), 'BeSe': ('Be', 2, 'Se', 'ZB'), 'BeTe': ('Be', 2, 'Te', 'ZB'),
      'ZnS': ('Zn', 2, 'S', 'ZB'), 'ZnSe': ('Zn', 2, 'Se', 'ZB'), 'ZnTe': ('Zn', 2, 'Te', 'ZB'), 'CdTe': ('Cd', 2, 'Te', 'ZB'),
      'CuCl': ('Cu', 1, 'Cl', 'ZB'), 'CuBr': ('Cu', 1, 'Br', 'ZB'), 'CuI': ('Cu', 1, 'I', 'ZB'),
      'ZnO': ('Zn', 2, 'O', 'W'), 'CdS': ('Cd', 2, 'S', 'W'), 'CdSe': ('Cd', 2, 'Se', 'W'), 'AgI': ('Ag', 1, 'I', 'W'),
      'MgO': ('Mg', 2, 'O', 'RS'), 'MgS': ('Mg', 2, 'S', 'RS'), 'MgSe': ('Mg', 2, 'Se', 'RS'), 'CaO': ('Ca', 2, 'O', 'RS'),
      'CaS': ('Ca', 2, 'S', 'RS'), 'SrO': ('Sr', 2, 'O', 'RS'), 'SrS': ('Sr', 2, 'S', 'RS'), 'BaO': ('Ba', 2, 'O', 'RS'),
      'BaS': ('Ba', 2, 'S', 'RS'), 'CdO': ('Cd', 2, 'O', 'RS')}
ANCH = {'O': -2, 'S': -2, 'Se': -2, 'Te': -2, 'Cl': -1, 'Br': -1, 'I': -1}
abrows = []
for name, (M, ch, X, st) in AB.items():
    rec = dict(compound=name, structure=st)
    for conv in ['IR', 'CR']:
        for mode in ['actual', 'VI']:
            cn_c = ('IV' if st in ('ZB', 'W') else 'VI') if mode == 'actual' else 'VI'
            cn_a = ('IV' if (X == 'O' and st in ('ZB', 'W') and mode == 'actual') else 'VI')
            rc, kc = rad(M, ch, cn_c, conv); ra, ka = rad(X, ANCH[X], cn_a, conv)
            rec[f'{conv}-{mode}'] = dict(r_cat=str(rc), cn_cat=cn_c, r_an=str(ra), cn_an=cn_a, rho=float(rc / ra),
                                         lam_ZB=float(3 * (rc - ra) / (rc + ra)))
    abrows.append(rec)
out['AB'] = abrows
scores = {}
for key in ['IR-actual', 'IR-VI', 'CR-actual', 'CR-VI']:
    for thr_name, thr in [('pauling_0414', float(PAULING6)), ('census_flip_05', 0.5)]:
        ok = sum(1 for r in abrows if (r[key]['rho'] >= thr) == (r['structure'] == 'RS'))
        wrong = [r['compound'] for r in abrows if (r[key]['rho'] >= thr) != (r['structure'] == 'RS')]
        scores[f'{key}/{thr_name}'] = dict(correct=ok, n=len(abrows), wrong=wrong)
    # best single threshold (for reference): midpoint of the best split
    vals = sorted((r[key]['rho'], r['structure'] == 'RS') for r in abrows)
    best = max(((sum(1 for v, rs in vals if (v >= c) == rs), c) for c in [v for v, _ in vals] + [9]), key=lambda z: z[0])
    scores[f'{key}/best_threshold'] = dict(correct=best[0], threshold=best[1])
out['AB_scores'] = scores
check('C2 24 AB compounds placed', len(abrows) == 24)
check('C2 regression: ZnS IR (Zn IV 0.60, S VI 1.84) rho = 0.3261', abs([r for r in abrows if r['compound'] == 'ZnS'][0]['IR-actual']['rho'] - 0.60 / 1.84) < 1e-12)

# ------------------------------------------------------------------ C3 titanate perovskites
# structures: SrTiO3 cubic Pm-3m at room temperature (Pai et al. 2018, arXiv:1702.07690, full text); BaTiO3 cubic above
# ~393 K, tetragonal P4mm below (Amoroso, Cano, Ghosez 2018, arXiv:1801.08886, full text); CaTiO3 orthorhombic Pnma
# ground state, cubic above ~1634 K (same).  Radii: A XII, Ti4+ VI, O2- VI.
per = []
for A, st in [('Ca', 'orthorhombic Pnma (octahedral tilts)'), ('Sr', 'cubic Pm-3m at room T'), ('Ba', 'tetragonal P4mm at room T (cubic above ~393 K)')]:
    rec = dict(compound=A + 'TiO3', structure_room_T=st)
    for conv in ['IR', 'CR']:
        ra, rb, rx = rad(A, 2, 'XII', conv)[0], rad('Ti', 4, 'VI', conv)[0], rad('O', -2, 'VI', conv)[0]
        tv = (ra + rx) / (sp.sqrt(2) * (rb + rx)); mo = rb / rx
        # cell edge 2: lattice by the tighter contact
        s = min(1 / (rb + rx), sp.sqrt(2) / (ra + rx), key=lambda z: float(z))
        lv, mv = s**2 * (ra**2 - rx**2), s**2 * (rb**2 - rx**2)
        tAA = sp.sqrt(2) / (1 + mo)
        rec[conv] = dict(r_A=str(ra), r_B=str(rb), r_X=str(rx), t=float(tv), mu_oct=float(mo), rA_over_rX=float(ra / rx),
                         lam=float(lv), mu=float(mv), contact='B-X' if float(1 / (rb + rx)) <= float(sp.sqrt(2) / (ra + rx)) else 'A-X',
                         t_wall_AA=float(tAA), side='A-A faces present (lam > 0)' if ra > rx else 'no A-A faces (lam < 0)',
                         lam_plus_2mu=float(lv + 2 * mv), lam_plus_mu=float(lv + mv))
    per.append(rec)
out['perovskites'] = per
check('C3 t is identical under IR and CR for every titanate (convention invariance, G9)', all(abs(r['IR']['t'] - r['CR']['t']) < 1e-12 for r in per))
check('C3 IR: the A-A wall r_A = r_X separates CaTiO3 (tilted) from SrTiO3 / BaTiO3',
      per[0]['IR']['rA_over_rX'] < 1 < per[1]['IR']['rA_over_rX'] < per[2]['IR']['rA_over_rX'])
check('C3 CR: all three titanates on the same side of the A-A wall (the separation is convention-dependent)',
      all(r['CR']['rA_over_rX'] > 1 for r in per))
out['perovskite_note'] = 'A-B wall side recorded per compound as lam_plus_2mu (A-B faces exist iff > 0)'

json.dump(out, open(os.path.join(here, '..', 'data', 'raw', 'compounds.json'), 'w'), indent=1, default=str)
with open(os.path.join(here, '..', 'data', 'checks', 'compounds-checks.txt'), 'w') as f:
    for n, ok, det in CHECKS:
        f.write(f"{'PASS' if ok else 'FAIL'}  {n}  {det}\n")
print(f"compounds: {sum(ok for _, ok, _ in CHECKS)} PASS, {sum(not ok for _, ok, _ in CHECKS)} FAIL")
