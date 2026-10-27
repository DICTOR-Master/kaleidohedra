# Splash Rules map (DICTO 2026-10-27): every layer spacing s (rows) and weight window (columns), coloured by the exact rule that holds
# for ALL hole pieces in that window: halves (#57), Swap Rule (mixed tetrahedra = Janus at the mid-plane), layer sums (reach 2: volume =
# one share per layer reached), layer + pair sums (plus one share per neighbouring pair of layers). Exact (sympy), from data/s_*.json.
import json, glob, os
from fractions import Fraction as Fr
import sympy as sp
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Patch
D = os.path.expanduser('~/kres-tmp/splash/data'); L = sp.Symbol('lam')
COL = {'halves': '#4f7cc9', 'swap': '#d97a3a', 'sums': '#4caf6a', 'pairs': '#9a5fc0', 'open': '#d0453b', 'na': '#3b4048'}
NAME = {'halves': 'rule of halves (#57)', 'swap': 'Swap Rule', 'sums': 'layer sums (reach 2)', 'pairs': 'layer + pair sums (reach 2)',
        'open': 'no rule found', 'na': 'pure stackings missing a piece: not compared'}
def types(ctx):
    s = [1 if ch == '+' else -1 for ch in ctx]; return [int(s[i] != s[i + 1]) for i in range(len(s) - 1)]
def fits(rows, feats):
    F = [feats(t) for t, _ in rows]; c = sp.symbols(f'c0:{len(F[0])}'); deg = max(sp.Poly(v, L).degree() for _, v in rows)
    return all(sp.solve([sum(a * b for a, b in zip(c, f)) - sp.Poly(v, L).coeff_monomial(L ** e) for f, (_, v) in zip(F, rows)], c, dict=True) for e in range(deg + 1))
def classify(d, w):
    X = d['mix'][w]
    if any(x['fit'] == 'no pure ref' for x in X): return 'na'
    if int(d['rmin']) == 1:
        if all(isinstance(x['fit'], dict) for x in X): return 'halves'
        roles = {}
        for x in X: roles.setdefault(x['role'], {})[x['ctx']] = sp.sympify(x['volume'])
        ok = all(sp.expand(V['--+'] + V['-++'] - V['---'] - V['-+-']) == 0 for r, V in roles.items() if r != 'oct' and '--+' in V)
        return 'swap' if ok and all(isinstance(x['fit'], dict) for x in X if x['role'] == 'oct') else 'open'
    res = 'sums'
    for role in ('oct', 'tetX', 'tetY'):
        rows = [(types(x['ctx']), sp.expand(sp.sympify(x['volume']))) for x in X if x['role'] == role]
        if fits(rows, lambda t: [1] + t): continue
        if fits(rows, lambda t: [1] + t + [t[i] * t[i + 1] for i in range(len(t) - 1)]): res = 'pairs'; continue
        return 'open'
    return res
files = sorted(glob.glob(f'{D}/s_*.json'), key=lambda p: Fr(json.load(open(p))['s']))
fig, ax = plt.subplots(figsize=(15, 8.5), facecolor='#2b2f36'); ax.set_facecolor('#2b2f36')
ys = []
for k, p in enumerate(files):
    d = json.load(open(p)); s = Fr(d['s']); ys.append(str(s))
    for w in d['mix']:
        lo = Fr(w); hi = next(Fr(b) for a, b in d['windows'] if a == w)
        c = classify(d, w); ax.add_patch(plt.Rectangle((float(lo), k + 0.06), float(hi - lo), 0.88, color=COL[c], lw=0))
        if c != 'na' and float(hi - lo) > 0.035: ax.text(float(lo + hi) / 2, k + 0.5, f'{lo}…{hi}', ha='center', va='center', fontsize=6.5, color='white')
    print(s, 'reach', d['rmin'], flush=True)
ax.axhline(ys.index('1') + 0.5 if '1' in ys else 0, color='#c9a646', lw=0.6, ls=':')
ax.set_yticks([k + 0.5 for k in range(len(ys))]); ax.set_yticklabels([f'{y} × ⅔' + ('  (#57)' if y == '1' else '') for y in ys], color='#ddd')
ax.set_ylim(0, len(ys)); ax.set_xlim(-0.55, 0.45); ax.tick_params(colors='#ddd')
ax.set_xlabel('weight λ (tetrahedral hole weight − octahedral)', color='#ddd'); ax.set_ylabel('layer spacing²  (squashed ↓   stretched ↑)', color='#ddd')
for sp_ in ax.spines.values(): sp_.set_visible(False)
ax.set_title('Splash Rules map: which exact rule shares out the holes of every close-packed stacking', color='white', fontsize=13)
fig.legend(handles=[Patch(color=COL[k], label=NAME[k]) for k in COL], loc='lower center', ncol=3, facecolor='#2b2f36', labelcolor='white', fontsize=10)
fig.text(0.985, 0.015, 'DICTO', color='#c9a646', ha='right', fontsize=16, weight='bold')
plt.tight_layout(rect=(0, 0.09, 1, 1)); out = os.path.expanduser('~/kres-tmp/splash/splash-map.png'); plt.savefig(out, dpi=140, facecolor=fig.get_facecolor()); print('wrote', out)
