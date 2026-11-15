"""Lean export of the geometric step facts (step 2, the construction is forced).  For each construction step i (Deriv.Data
d_i, n_i) it writes a lemma `V y i * Ex.ev (V y) d_i = Ex.ev (V y) n_i`, proved by `linear_combination` with a certificate that
Singular finds here (`lift` of c * (lhs - rhs) into the ideal of the hypotheses: triple points, circles, slope definitions),
c a product of factors that are nonzero at an admissible figure.  Writes lean/YantraCert/GeomSteps.lean.
Usage: c6_geom_lean.py   FINAL ok iff every certificate is found."""
import os, itertools
from sage.all__sagemath_singular import QQ, PolynomialRing
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D_ = lambda *p: os.path.join(HERE, *p)
names = [f'b{i}' for i in range(9)] + [f'w{i}' for i in range(9)] + ['u', 't', 'k2', 'k9', 'k8', 'k1', 'k4', 'k6']
Rg = PolynomialRing(QQ, names); G = dict(zip(names, Rg.gens()))
globals().update(G)
A = {0: b5, 1: b8, 2: Rg(1), 3: b7, 4: b6, 5: b1, 6: Rg(0), 7: b0, 8: b2}     # apexes after (ii) and (i)
B = [b0, b1, b2, b3, b4, b5, b6, b7, b8]; Wv = [w0, w1, w2, w3, w4, w5, w6, w7, w8]
def conc(p, q, r): return Wv[p] * (B[q] - A[p]) * (B[r] - A[r]) - Wv[r] * (B[q] - A[r]) * (B[p] - A[p])
# hypotheses: name -> (polynomial lhs - rhs, Lean term producing `lhs = rhs`)
H = {
 'm127': conc(0, 1, 6), 'm237': conc(1, 2, 6), 'm138': conc(0, 2, 7), 'm146': conc(0, 3, 5), 'm159': conc(0, 4, 8),
 'm469': conc(3, 5, 8), 'm279': conc(1, 6, 8), 'm378': conc(2, 6, 7), 'm389': conc(2, 7, 8), 't448': conc(3, 3, 7),
 't556': conc(4, 4, 5), 't266': conc(1, 5, 5),
 'c7': w6**2 + b6**2 - b6, 'c1': w0**2 + b0**2 - b0, 'hP': b2 - (1 - b6), 'kw': w2 - w6,
 'hu': u * b6 - w6, 'ht': t * w0 - b0, 'hk2': k2 * (b8 - b1) - w1, 'hk9': k9 * (b8 - b2) - w8, 'hk8': k8 * (b7 - b0) - w7,
 'hk1': k1 * (b5 - b0) - w0, 'hk4': k4 * (b7 - b3) - w3, 'hk6': k6 * (b5 - b1) - w5}
LEANV = {**{f'b{i}': f'y.b {i}' for i in range(9)}, **{f'w{i}': f'y.w {i}' for i in range(9)}, 'u': 'u', 't': 't',
         'k2': 'k2', 'k9': 'k9', 'k8': 'k8', 'k1': 'k1', 'k4': 'k4', 'k6': 'k6'}
# the quantities V i in these variables, and the Lean expression of V y i (as `V` unfolds)
VQ = {0: u, 1: t, 2: b8, 3: b6, 4: b2, 5: w6, 6: b0, 7: w0, 8: k2, 9: k9, 10: w8, 11: k8, 12: b5, 13: k1, 14: b7, 15: k4,
      16: w5, 17: b1, 18: b3, 19: k6, 20: b4, 21: w4, 22: w1, 23: w3, 24: w7, 25: k1 * (b5 - b3), 26: k6 * (b3 - b1)}
GEN = {'u': ('y.w 6 / y.b 6', 'y.b 6'), 't': ('y.b 0 / y.w 0', 'y.w 0'), 'k2': ('y.w 1 / (y.b 8 - y.b 1)', '(y.b 8 - y.b 1)'),
       'k9': ('y.w 8 / (y.b 8 - y.b 2)', '(y.b 8 - y.b 2)'), 'k8': ('y.w 7 / (y.b 7 - y.b 0)', '(y.b 7 - y.b 0)'),
       'k1': ('y.w 0 / (y.b 5 - y.b 0)', '(y.b 5 - y.b 0)'), 'k4': ('y.w 3 / (y.b 7 - y.b 3)', '(y.b 7 - y.b 3)'),
       'k6': ('y.w 5 / (y.b 5 - y.b 1)', '(y.b 5 - y.b 1)')}
VL = {0: 'y.w 6 / y.b 6', 1: 'y.b 0 / y.w 0', 2: 'y.b 8', 3: 'y.b 6', 4: 'y.b 2', 5: 'y.w 6', 6: 'y.b 0', 7: 'y.w 0',
      8: 'y.w 1 / (y.b 8 - y.b 1)', 9: 'y.w 8 / (y.b 8 - y.b 2)', 10: 'y.w 8', 11: 'y.w 7 / (y.b 7 - y.b 0)', 12: 'y.b 5',
      13: 'y.w 0 / (y.b 5 - y.b 0)', 14: 'y.b 7', 15: 'y.w 3 / (y.b 7 - y.b 3)', 16: 'y.w 5', 17: 'y.b 1', 18: 'y.b 3',
      19: 'y.w 5 / (y.b 5 - y.b 1)', 20: 'y.b 4', 21: 'y.w 4', 22: 'y.w 1', 23: 'y.w 3', 24: 'y.w 7',
      25: '(y.w 0 / (y.b 5 - y.b 0)) * (y.b 5 - y.b 3)', 26: '(y.w 5 / (y.b 5 - y.b 1)) * (y.b 3 - y.b 1)'}
# parse the Ex strings of the steps (from c4) into (Sage polynomial, Lean real expression)
import json
J = json.load(open(D_('data', 'lean-deriv.json')))
def parse(s):
    toks = s.replace('(', ' ( ').replace(')', ' ) ').split(); pos = [0]
    def ex():
        assert toks[pos[0]] == '('; pos[0] += 1
        op = toks[pos[0]]; pos[0] += 1
        if op == '.v': i = int(toks[pos[0]]); pos[0] += 2; return VQ[i], f'(V y {i})', i
        if op == '.c':
            assert toks[pos[0]] == '('; z = int(toks[pos[0] + 1]); pos[0] += 4; return Rg(z), f'(({z} : ℤ) : ℝ)', -1
        a = ex(); b = ex(); assert toks[pos[0]] == ')'; pos[0] += 1
        sym = {'.add': '+', '.sub': '-', '.mul': '*'}[op]
        f = {'.add': lambda x, y: x + y, '.sub': lambda x, y: x - y, '.mul': lambda x, y: x * y}[op]
        return f(a[0], b[0]), f'({a[1]} {sym} {b[1]})', max(a[2], b[2])
    return ex()
NZ = {'b6': b6, 'w0': w0, 'b8-b1': b8 - b1, 'b8-b2': b8 - b2, 'b7-b0': b7 - b0, 'b5-b0': b5 - b0, 'b7-b3': b7 - b3,
      'b5-b1': b5 - b1, 'b6-b0': b6 - b0, 'b4-b6': b4 - b6, 'b3-b7': b3 - b7, 'b5-b8': b5 - b8, 'b2-b0': b2 - b0}
NZL = {'b6': 'y.b 6', 'w0': 'y.w 0', 'b8-b1': '(y.b 8 - y.b 1)', 'b8-b2': '(y.b 8 - y.b 2)', 'b7-b0': '(y.b 7 - y.b 0)',
       'b5-b0': '(y.b 5 - y.b 0)', 'b7-b3': '(y.b 7 - y.b 3)', 'b5-b1': '(y.b 5 - y.b 1)', 'b6-b0': '(y.b 6 - y.b 0)',
       'b4-b6': '(y.b 4 - y.b 6)', 'b3-b7': '(y.b 3 - y.b 7)', 'b5-b8': '(y.b 5 - y.b 8)', 'b2-b0': '(y.b 2 - y.b 0)'}
I = Rg.ideal(list(H.values()))
REL = {3: ['c7', 'hu'], 4: ['c7', 'hu', 'hP'], 5: ['c7', 'hu'], 6: ['c1', 'ht'], 7: ['c1', 'ht'], 8: ['m237', 'hk2', 'hu'],
       9: ['m279', 'hk2', 'hk9'], 10: ['hk9'], 11: ['m378', 'hk8', 'hu', 'hP', 'kw', 'c7'],
       12: ['m138', 'm378', 'hk8', 'hu', 'hP', 'kw', 'c7', 'c1', 'ht'], 13: ['hk1'], 14: ['m389', 'hk9', 'hu', 'hP', 'kw', 'c7'],
       15: ['m469', 'hk4', 'hk9'], 16: ['t266', 'hk2'], 17: ['m127', 'hk1', 'hu'], 18: ['t448', 'hk4', 'hk8'], 19: ['hk6'],
       20: ['m159', 'hk1', 'hk9'], 21: ['t556', 'hk6'], 22: ['hk2'], 23: ['hk4'], 24: ['hk8'], 25: ['hk1'], 26: ['hk6']}
def find(target, i):
    hyps = [(k, H[k]) for k in REL[i]]
    Ih = Rg.ideal([h for k, h in hyps])
    for n in range(0, 3):
        for combo in itertools.combinations_with_replacement(list(NZ), n):
            c = Rg(1)
            for k in combo: c *= NZ[k]
            f = c * target
            if f in Ih:
                co = f.lift(Ih)
                return combo, [(hyps[j][0], co[j]) for j in range(len(hyps)) if co[j] != 0]
    return None
def lexpr(p):
    """Lean expression of a polynomial in the variables"""
    if p == 0: return '0'
    terms = []
    for mon, c in p.dict().items():
        fac = [f'{LEANV[names[j]]}' + (f' ^ {e}' if e > 1 else '') for j, e in enumerate(mon) if e > 0]
        cq = QQ(c); cs = f'({cq.numerator()} : ℝ)' if cq.denominator() == 1 else f'(({cq.numerator()} : ℝ) / {cq.denominator()})'
        terms.append(' * '.join([cs] + fac))
    return ' + '.join(terms)
ok = True; out = []; facts = {}
for s in J['steps']:
    i = s['i']; d = parse(s['d']); n = parse(s['n'])
    target = VQ[i] * d[0] - n[0]
    res = find(target, i)
    if res is None: ok = False; print('NO CERTIFICATE for step', i, s['name']); continue
    combo, cert = res
    facts[i] = target
    used_gens = sorted({str(v) for v in Rg.gens() if any(v in p.variables() for _, p in cert) or v in target.variables()}
                       & set(GEN))
    L = [f'lemma gstep{i} (F : Facts y) : V y {i} * Ex.ev (V y) d{i} = Ex.ev (V y) n{i} := by',
         f'  show {VL[i]} * {d[1]} = {n[1]}' if False else f'  show ({VL[i]}) * {d[1].replace("(V y ", "(Vy ")} = {n[1].replace("(V y ", "(Vy ")}']
    out.append((i, combo, cert, d, n, used_gens))
    print('step', i, s['name'], 'c =', combo, 'hyps', [k for k, _ in cert])
# ---------------- Lean ----------------
src = ['import YantraCert.Geom', 'import YantraCert.Deriv.Data', '', 'set_option maxHeartbeats 4000000', '',
       '/-! The construction steps from the geometry (generated by scripts/c6_geom_lean.py; certificates by Singular `lift`). -/', '',
       'namespace YantraCert.Y', 'open YantraCert YantraCert.Deriv', '', 'section', 'variable {y : Yantra}', '']
def vsub(e):
    for k in range(26, -1, -1): e = e.replace(f'(V y {k})', f'({VL[k]})')
    return e
for i, combo, cert, d, n, gens in out:
    L = [f'lemma gstep{i} (F : Facts y) : V y {i} * Ex.ev (V y) d{i} = Ex.ev (V y) n{i} := by',
         f'  show ({VL[i]}) * {vsub(d[1])} = {vsub(n[1])}', '  push_cast',
         '  have hyps := hyps_of F',
         '  obtain ⟨m127, m237, m138, m146, m159, m469, m279, m378, m389, t448, t556, t266, c7, c1, hP, kw, hu, ht, hk2, hk9, hk8, hk1, hk4, hk6⟩ := hyps']
    for g in ['u', 't', 'k2', 'k9', 'k8', 'k1', 'k4', 'k6']:
        L.append(f'  generalize {GEN[g][0]} = {g} at *')
    c = ' * '.join(NZL[k] for k in combo) if combo else '(1 : ℝ)'
    certs = ' + '.join(f'({lexpr(p)}) * {nm}' for nm, p in cert)
    L += [f'  have h0 : {c} * ({lexpr(VQ[i])} * ({lexpr(d[0])}) - ({lexpr(n[0])})) = 0 := by',
          (f'    linear_combination {certs}' if certs else '    ring')]
    nzs = [f'nz_{k.replace("-", "_")} F' for k in combo]
    if not combo: hcl = '    exact one_ne_zero'
    elif len(combo) == 1: hcl = f'    exact {nzs[0]}'
    else: hcl = '    simp only [ne_eq, mul_eq_zero, not_or]; exact ⟨' + ', '.join(nzs) + '⟩'
    L += ['  have hc : ' + c + ' ≠ 0 := by', hcl,
          '  have := (mul_eq_zero.mp h0).resolve_left hc', '  linear_combination this', '']
    src += L
ORD = 'F.o01, F.o12, F.o23, F.o34, F.o45, F.o56, F.o67, F.o78'
def sl(w, a, b): return f'(div_pos (F.wp {w}) (by linarith [{ORD}] : (0:ℝ) < y.b {a} - y.b {b}) : 0 < y.w {w} / (y.b {a} - y.b {b}))'
SLOPE = {'u': '(div_pos (F.wp 6) (b6pos F) : 0 < y.w 6 / y.b 6)', 'k9': sl(8, 8, 2), 'k1': sl(0, 5, 0), 'k4': sl(3, 7, 3), 'k8': sl(7, 7, 0)}
SQ = 'nlinarith [mul_self_nonneg (y.w 6 / y.b 6), mul_self_nonneg (y.b 0 / y.w 0)]'
PF = {3: SQ, 4: SQ, 5: SQ, 6: SQ, 7: SQ,
      8: f'linarith [{ORD}]', 9: f'linarith [{ORD}]', 11: f'linarith [{ORD}]', 13: f'linarith [{ORD}]',
      15: f'linarith [{ORD}]', 19: f'linarith [{ORD}]',
      14: 'linarith [' + SLOPE['u'] + ', ' + SLOPE['k9'] + ']', 17: 'linarith [' + SLOPE['u'] + ', ' + SLOPE['k1'] + ']',
      18: 'linarith [' + SLOPE['k4'] + ', ' + SLOPE['k8'] + ']', 20: 'linarith [' + SLOPE['k1'] + ', ' + SLOPE['k9'] + ']'}
for i, combo, cert, d, n, gens in out:
    if i == 12:
        src += [f'lemma dne12 (F : Facts y) : Ex.ev (V y) d12 ≠ 0 := by',
                '  have g := gstep12 F',
                f'  show {vsub(d[1])} ≠ 0', f'  change ({VL[12]}) * {vsub(d[1])} = {vsub(n[1])} at g', '  push_cast at g ⊢',
                '  intro h0', '  rw [h0, mul_zero] at g',
                '  have hu := div_pos (F.wp 6) (b6pos F)',
                '  have h1 : 0 < 1 - y.b 6 := by linarith [b8lt1 F, F.o78, F.o67]',
                '  have h2 : 0 < y.b 2 - y.b 0 := by linarith [F.o01, F.o12]',
                '  have key : y.w 6 / y.b 6 * (1 - y.b 6) * (y.b 2 - y.b 0) ^ 2 = 0 := by linear_combination -g - (y.b 2) * h0',
                '  have : 0 < y.w 6 / y.b 6 * (1 - y.b 6) * (y.b 2 - y.b 0) ^ 2 := by positivity',
                '  linarith', '']
        continue
    if d[0] == 1:
        src += [f'lemma dne{i} (F : Facts y) : Ex.ev (V y) d{i} ≠ 0 := by', f'  show {vsub(d[1])} ≠ 0', '  norm_num', '']
        continue
    src += [f'lemma dne{i} (F : Facts y) : Ex.ev (V y) d{i} ≠ 0 := by', f'  show {vsub(d[1])} ≠ 0', '  push_cast',
            '  apply ne_of_gt', f'  {PF[i]}', '']
src += ['end', '', 'end YantraCert.Y', '']
open(D_('lean', 'YantraCert', 'GeomSteps.lean'), 'w').write('\n'.join(src))
print('FINAL ok' if ok else 'FINAL FAIL')
