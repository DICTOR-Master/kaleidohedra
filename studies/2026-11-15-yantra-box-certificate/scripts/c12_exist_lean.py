"""Lean export of the existence direction: writes lean/YantraCert/Exist.lean.  The figure is rebuilt from the zero of F~ in the
small Krawczyk box Xs: every named quantity is its stored fraction at (u, t, S) (denominators nonzero by the signs of KEx), the
construction steps hold (Frac.step_of_inv), every admissibility test is positive (the signs of the stored test pairs on Xs and the
KTest identities), the three equations hold (KPull, KFin), and every triple point holds by a `linear_combination` certificate that
Singular finds here (`lift` into the ideal of the step relations).
Usage: c12_exist_lean.py   FINAL ok iff every certificate is found."""
from lean_module import modulize   # Palomar source rule: every generated file in module form (16 Nov 2026)
import json, os, itertools
from fractions import Fraction as Fq
from sage.all__sagemath_singular import QQ, PolynomialRing
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D_ = lambda *p: os.path.join(HERE, *p)
J = json.load(open(D_('data', 'lean-deriv.json'))); EX = json.load(open(D_('data', 'lean-exist.json')))
TK = list(J['tests']); NQ = len(J['names'])
Rv = PolynomialRing(QQ, [f'v{i}' for i in range(NQ)]); v = Rv.gens()
def parse(s, mode):
    toks = s.replace('(', ' ( ').replace(')', ' ) ').split(); pos = [0]
    def ex():
        pos[0] += 1; op = toks[pos[0]]; pos[0] += 1
        if op == '.v':
            i = int(toks[pos[0]]); pos[0] += 2
            return v[i] if mode == 'poly' else f'(W {i})'
        if op == '.c':
            z = int(toks[pos[0] + 1]); pos[0] += 4
            return Rv(z) if mode == 'poly' else f'(({z} : ℤ) : ℝ)'
        a = ex(); b = ex(); pos[0] += 1
        if mode == 'poly': return {'add': a + b, 'sub': a - b, 'mul': a * b}[op[1:]]
        return f'({a} {dict(add="+", sub="-", mul="*")[op[1:]]} {b})'
    return ex()
STEPS = {s['i']: (parse(s['d'], 'poly'), parse(s['n'], 'poly'), parse(s['d'], 'lean'), parse(s['n'], 'lean')) for s in J['steps']}
HYP = {f's{i}': v[i] * d - n for i, (d, n, _, _) in STEPS.items()}
HYP['e146'] = v[25] - v[26]
B = [v[6], v[17], v[4], v[18], v[20], v[12], v[3], v[14], v[2]]
Wc = [v[7], v[22], v[5], v[23], v[21], v[16], v[5], v[24], v[10]]
A = [v[12], v[2], Rv(1), v[14], v[3], v[17], Rv(0), v[6], v[4]]
def conc(p, q, r): return Wc[p] * (B[q] - A[p]) * (B[r] - A[r]) - Wc[r] * (B[q] - A[r]) * (B[p] - A[p])
CONC = [('m127', 0, 1, 6), ('m237', 1, 2, 6), ('m138', 0, 2, 7), ('m146', 0, 3, 5), ('m159', 0, 4, 8), ('m469', 3, 5, 8),
        ('m279', 1, 6, 8), ('m378', 2, 6, 7), ('m389', 2, 7, 8), ('t448', 3, 3, 7), ('t556', 4, 4, 5), ('t266', 1, 5, 5)]
# factors known nonzero at the rebuilt figure: (polynomial, Lean proof of `≠ 0`)
POS = {}
for n, k in enumerate(TK):
    if k == 'corner t9 in disc': continue
    POS[f'q{n}'] = (parse(J['tests'][k]['e'], 'poly'), f'(tpos_{n}).ne\'', parse(J['tests'][k]['e'], 'lean'))
POS['u'] = (v[0], 'W0_pos.ne\'', '(W 0)')
POS['1+u2'] = (1 + v[0]**2, '(by positivity)', '(1 + W 0 ^ 2)')
ok = True; certs = {}
names = list(POS)
REL = {'m127': [3, 5, 13, 17], 'm237': [3, 4, 5, 8, 22], 'm138': [3, 4, 6, 7, 11, 12, 13, 24], 'm146': [13, 19, 25, 26, 'e146'],
       'm159': [10, 13, 20], 'm469': [10, 15, 23], 'm279': [9, 10, 22], 'm378': [3, 4, 5, 11, 24], 'm389': [3, 4, 5, 10, 14],
       't448': [18, 23, 24], 't556': [19, 21], 't266': [16, 22]}
for nm, p, q, r in CONC:
    target = conc(p, q, r)
    hyps = [((f's{i}' if i != 'e146' else 'e146'), HYP[f's{i}' if i != 'e146' else 'e146']) for i in REL[nm]]
    I = Rv.ideal([h for _, h in hyps])
    found = None
    for nfac in range(0, 3):
        for combo in itertools.combinations_with_replacement(names, nfac):
            c = Rv(1)
            for k in combo: c *= POS[k][0]
            f = c * target
            if f in I:
                co = f.lift(I); found = (combo, [(hyps[j][0], co[j]) for j in range(len(hyps)) if co[j] != 0]); break
        if found: break
    if not found: ok = False; print('NO CERTIFICATE', nm); continue
    certs[nm] = found; print(nm, 'c =', found[0], [k for k, _ in found[1]], flush=True)
def lexpr(p):
    if p == 0: return '0'
    out = []
    for mon, c in p.dict().items():
        fac = [f'W {j}' + (f' ^ {e}' if e > 1 else '') for j, e in enumerate(mon) if e > 0]
        cq = QQ(c); cs = f'({cq.numerator()} : ℝ)' if cq.denominator() == 1 else f'(({cq.numerator()} : ℝ) / {cq.denominator()})'
        out.append(' * '.join([cs] + [f'({f_})' for f_ in fac]))
    return ' + '.join(out)
json.dump({k: {'c': list(c), 'h': [[h, str(p)] for h, p in cs]} for k, (c, cs) in certs.items()}, open(D_('data', 'lean-exist-certs.json'), 'w'))
# ---------------- Lean ----------------
def rat(c): q = Fq(c); return q.numerator, q.denominator
KINDP = {'u': 'linarith [eu_pos]', '1-u': 'linarith [eu_lt1]', '1+u': 'linarith [eu_pos]', 'tau': 'linarith [etau_pos]',
         '1-tau': 'linarith [etau_lt1]', 'rho': 'linarith [er_pos]', '1+u2': 'positivity'}
X = '(xs 0) (xs 1) (xs 2)'
def prodexpr(nms):
    e = '1'
    for nm, m in reversed(nms): e = f'{nm}.eval {X} ^ {m} * ' + (e if e == '1' else f'({e})')
    return e if nms else '(1 : ℝ)'
def prodpos(hs):
    pr = 'one_pos'
    for h in reversed(hs): pr = f'mul_pos {h} ({pr})'
    return pr
SIMPP = 'simp only [ZP.eval_mul, ZP.eval_const, ZP.eval_prod, List.map_cons, List.map_nil, List.prod_cons, List.prod_nil, ZP.eval_pow]'
LS = 'KEx.QS'
src = ['import YantraCert.ExistBase']
src += ['', 'set_option maxHeartbeats 8000000', 'set_option maxRecDepth 100000', '',
        '/-! Existence (generated by scripts/c12_exist_lean.py; hand-written parts in ExistBase.lean). -/', '',
        'namespace YantraCert.Y', 'open YantraCert YantraCert.Deriv', '']
# denominators nonzero, and every quantity is its fraction
for i in range(3, NQ):
    dD = EX['D'][str(i)] if str(i) in EX['D'] else EX['D'][i]
    g = dD['deg']
    src += [f'theorem Dne{i} : D{i}.eval eu et eS ≠ 0 := by',
            f'  have h := box_sign{dD["s"]} (ZP.toSP {g[0]} {g[1]} {g[2]} (ZP.substH PX PY PZn PZd {dD["d"]} D{i})) KEx.gQ{i} KEx.sQ{i}',
            f'  rw [ZP.toSP_eval, subst_x _ _ KEx.zQ{i}] at h',
            f'  intro h0; rw [h0, zero_mul] at h; exact lt_irrefl _ h', '']
src += ['theorem invE : ∀ i < 27, Inv T W eu et eS i := by', '  intro i hi', '  interval_cases i',
        '  · exact inv_W0', '  · exact inv_W1', '  · exact inv_W2'] + [f'  · exact inv_W _ Dne{i}' for i in range(3, NQ)] + ['']

src += ['theorem stepE (i : Nat) (d n : Ex) (K : ZP) (hok : stepOK T i d n K = true) (hi : i < 27 := by norm_num) :',
        '    W i * d.ev W = n.ev W := step_of_inv T W eu et eS i d n K hok (fun j hj => invE j (by omega))', '']
KK = {'G': ('0', 'k0', 'P0'), 'H1': ('1', 'k1', 'P1'), 'D': ('2', 'k2', 'P2')}
for k, f in J['finals'].items():
    a, b = rat(f['c']); pk = J['pull'][k]; pa, pb = rat(pk['c'])
    idx, kk, P = KK[k]
    src += [f'theorem fmE_{k} : Fm_{k}.eval (xs 0) (xs 1) (xs 2) = 0 := by',
            f'  have h := xs_spec.2 {idx}', f'  change KBox.{P}.eval (xs 0) (xs 1) (xs 2) = 0 at h',
            f'  rw [← ZP.eval_ofSP, ZP.eq_of_eqv KKBox.{kk}] at h', '  exact h', '',
            f'theorem fsE_{k} : Fs_{k}.eval eu et eS = 0 := by',
            f'  have h := ZP.eq_of_eqv pull_{k} (xs 0) (xs 1) (xs 2)',
            f'  rw [ZP.eval_mul, ZP.eval_const, subst_x _ _ zd_{k}, ZP.eval_mul, ZP.eval_const, ZP.eval_mul, fmE_{k}, zero_mul, mul_zero] at h',
            f'  have hA : (0 : ℝ) < (1 + eu ^ 2) ^ {pk["d"]} := by positivity',
            '  push_cast at h', '  rcases mul_eq_zero.mp h with h | h', '  · norm_num at h',
            '  rcases mul_eq_zero.mp h with h | h', '  · exact h', '  · exact absurd h hA.ne\'', '',
            f'theorem eE_{k} : Ex.ev W E_{k} = 0 := by',
            f'  apply zero_of_num T W eu et eS 27 invE E_{k} finb_{k}',
            f'  have h := ZP.eq_of_eqv fin_{k} eu et eS',
            f'  rw [ZP.eval_mul, ZP.eval_const, ZP.eval_mul, ZP.eval_const, ZP.eval_mul, fsE_{k}, zero_mul, mul_zero] at h',
            '  push_cast at h', '  rcases mul_eq_zero.mp h with h | h', '  · norm_num at h', '  · exact h', '']
src += ['theorem eH1E : W 25 - W 26 = 0 := eE_H1', '']
# test positivity, directly from the signs of the pulled-back numerator and denominator on Xs
ITEMS = [(n, k) for n, k in enumerate(TK) if k not in ('corner t9 in disc', 'corner t5 in disc')] + [(x, x) for x in ('A28', 'B28', 'C28')]
for n, k in ITEMS:
    tn = EX['T'][str(n)]
    sg = tn['N']['s']; dN = tn['N']['deg']; dD = tn['D']['deg']; d = tn['d']
    qn = f'KEx.Q{n}' if isinstance(n, str) else f'Q_{n}'
    name = f'tpos_{n}'
    L = [f'theorem {name} : 0 < Ex.ev W {qn} := by',
         f'  obtain ⟨fr1, fr2⟩ := frac_sound T W eu et eS 27 invE {qn} KEx.w{n}',
         f'  have hN := box_sign{sg} (ZP.toSP {dN[0]} {dN[1]} {dN[2]} (ZP.substH PX PY PZn PZd {d} (Ex.frac T {qn}).1)) KEx.gN{n} KEx.sN{n}',
         f'  have hD := box_sign{sg} (ZP.toSP {dD[0]} {dD[1]} {dD[2]} (ZP.substH PX PY PZn PZd {d} (Ex.frac T {qn}).2)) KEx.gD{n} KEx.sD{n}',
         f'  rw [ZP.toSP_eval, subst_x _ _ KEx.zN{n}] at hN', f'  rw [ZP.toSP_eval, subst_x _ _ KEx.zD{n}] at hD',
         f'  have e : Ex.ev W {qn} * ((Ex.frac T {qn}).2.eval eu et eS * (1 + eu ^ 2) ^ {d}) = (Ex.frac T {qn}).1.eval eu et eS * (1 + eu ^ 2) ^ {d} := by',
         '    rw [← fr1]; ring',
         '  rw [← e] at hN', '  by_contra hq; push Not at hq', '  nlinarith']
    src += L + ['']
src += ['theorem tpos_28 : 0 < Ex.ev W Q_28 := by',
        '  have a := tpos_A28; change 0 < ((5 : ℤ) : ℝ) * W 20 - ((2 : ℤ) : ℝ) at a',
        '  have b := tpos_B28; change 0 < ((3 : ℤ) : ℝ) - ((5 : ℤ) : ℝ) * W 20 at b',
        '  have c := tpos_C28; change 0 < ((1 : ℤ) : ℝ) - ((5 : ℤ) : ℝ) * W 21 at c',
        '  have w := tpos_12; change 0 < W 21 at w',
        '  show 0 < W 20 * (((1 : ℤ) : ℝ) - W 20) - W 21 * W 21',
        '  push_cast at a b c ⊢', '  nlinarith', '']
# triple points
for nm, p, q, r in CONC:
    if nm not in certs: continue
    combo, cs = certs[nm]
    c = ' * '.join(POS[k][2] for k in combo) if combo else '(1 : ℝ)'
    tgt = conc(p, q, r)
    L = [f'theorem ex_{nm} : {lexpr(tgt)} = 0 := by']
    for h, _ in cs:
        if h == 'e146': L.append('  have e146 : W 25 - W 26 = 0 := eH1E')
        else:
            i = int(h[1:]); d, n_, dl, nl = STEPS[i]
            L += [f'  have {h} : W {i} * {dl} = {nl} := stepE {i} d{i} n{i} K{i} step{i}', f'  push_cast at {h}']
    cert = ' + '.join(f'({lexpr(co)}) * {h}' for h, co in cs)
    L += [f'  have h0 : {c} * ({lexpr(tgt)}) = 0 := by', f'    linear_combination {cert}']
    if combo:
        nz = [POS[k][1] for k in combo]; pr = nz[-1]
        for z in reversed(nz[:-1]): pr = f'mul_ne_zero {z} ({pr})'
        L += [f'  exact (mul_eq_zero.mp h0).resolve_left ({pr})', '']
    else:
        L += ['  simpa using h0', '']
    src += L
src += ['end YantraCert.Y', '']
open(D_('lean', 'YantraCert', 'Exist.lean'), 'w').write(modulize('\n'.join(src)))
print('FINAL ok' if ok else 'FINAL FAIL')
