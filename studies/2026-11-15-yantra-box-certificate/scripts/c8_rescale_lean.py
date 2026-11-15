"""Lean export of the rescaling identities: each stored chart polynomial of the certificate (Data/<chart>/Polys.lean, rescaled
to the unit cube) equals a positive constant times the chart polynomial of the derivation (Deriv.Data, chart coordinates):
  (prod d_j^D_j) * stored(Y) = den * scaleW(F_c)(Y),   i.e.   stored(Y) = den * F_c(W Y),   W_j = n_j / d_j.
Writes lean/YantraCert/Deriv/KR<chart>.lean and appends them to Deriv/mods-rescale.txt.  FINAL ok iff every pair is found."""
import json, os
from fractions import Fraction as Fq
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D_ = lambda *p: os.path.join(HERE, *p)
man = json.load(open(D_('data', 'lean-cert-files.json'))); J = json.load(open(D_('data', 'lean-deriv.json')))
TK = list(J['tests'])
CHN = {'main': 'Main', 'A': 'A', 'B': 'B', 'C1': 'C1', 'C2': 'C2', 'W': 'W', 'Wt+': 'Wtp', 'Wt-': 'Wtm', 'Wr+': 'Wrp', 'Wr-': 'Wrm'}
OUT = D_('lean', 'YantraCert', 'Deriv'); mods = []; ok = True
def degs(P): return [max([e[j] for e, c in P] + [0]) for j in range(3)]
for ch, C in CHN.items():
    m = man['charts'][ch]; W = [Fq(w) for w in m['W']]
    if ch == 'main':
        polys = [(f'F{i}', f'Fm_{k}', J['pull'][k]['Fm'], m['KF'][k]) for i, k in enumerate(m['F'])]
        for i, k in enumerate(m['T']):
            n = TK.index(k); polys += [(f'T{i}N', f'TN_{n}', J['tests'][k]['N'], m['KT'][k][0]), (f'T{i}D', f'TD_{n}', J['tests'][k]['D'], m['KT'][k][1])]
    else:
        cd = J['charts'][ch]
        polys = [(f'F{i}', f'Fc{C}_{k}', cd['F'][k]['Fc'], m['KF'][k]) for i, k in enumerate(m['F'])]
        for i, k in enumerate(m['T']):
            n = TK.index(k); polys += [(f'T{i}N', f'Nc{C}_{n}', cd['T'][k]['Nc'], m['KT'][k][0]), (f'T{i}D', f'Dc{C}_{n}', cd['T'][k]['Dc'], m['KT'][k][1])]
        if set(m['F']) != set(cd['F']) or set(m['T']) != set(cd['T']): ok = False; print('MISMATCH', ch, m['F'], list(cd['F']), m['T'], list(cd['T']))
    L = [f'import YantraCert.Data.{C}.Polys', 'import YantraCert.Deriv.Data', 'import YantraCert.ZPoly2', '',
         'set_option maxRecDepth 200000', 'set_option maxHeartbeats 0', '', f'namespace YantraCert.Deriv.R{C}', 'open YantraCert YantraCert.Deriv', '']
    for st, zp, P, K in polys:
        D = degs(P); Lc = 1
        for j in range(3): Lc *= W[j].denominator ** D[j]
        args = ' '.join(f'{W[j].numerator} {W[j].denominator} {D[j]}' for j in range(3))
        L.append(f'theorem deg_{st} : {zp}.degLE {D[0]} {D[1]} {D[2]} = true := by decide +kernel')
        L.append(f'theorem res_{st} : ZP.eqv (ZP.mul (ZP.const {Lc}) (ZP.ofSP YantraCert.Data.{C}.{st})) '
                 f'(ZP.mul (ZP.const {int(Fq(K))}) (ZP.scaleW {args} {zp})) = true := by decide +kernel')
    L += ['', f'end YantraCert.Deriv.R{C}', '']
    open(os.path.join(OUT, f'KR{C}.lean'), 'w').write('\n'.join(L)); mods.append(f'YantraCert.Deriv.KR{C}')
open(os.path.join(OUT, 'mods-rescale.txt'), 'w').write('\n'.join(mods) + '\n')
print('FINAL ok' if ok else 'FINAL FAIL')
