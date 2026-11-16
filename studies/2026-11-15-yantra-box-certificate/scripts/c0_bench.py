"""Benchmark of kernel evaluators (no Mathlib): writes lean/bench/Bench<V>.lean for 50 slope leaves of H1~ (same leaves as the pilot
file SlopeH1_0).  V = R (recursor-based Nat-only evaluator)."""
from lean_module import modulize   # Palomar source rule: every generated file in module form (16 Nov 2026)
import json, sys, os
from fractions import Fraction as Fq
from math import gcd
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(HERE, 'data/polys-utr.json'))); cert = json.load(open(os.path.join(HERE, 'data/bnb-main.json')))
W = [Fq(b) - Fq(a) for a, b in data['box']]
def rescale(p):
    out = [(e, Fq(int(c)) * W[0]**e[0] * W[1]**e[1] * W[2]**e[2]) for e, c in p]
    den = 1
    for e, v in out: den = den * v.denominator // gcd(den, v.denominator)
    return [(e, int(v * den)) for e, v in out]
name = 'H1'; N = int(sys.argv[1]) if len(sys.argv) > 1 else 50
p = rescale(data['F'][name]); D = [max(e[j] for e, c in p) for j in range(3)]
def mono_ok(cell):
    lo = hi = 0
    for e, c in p:
        a = 1; b = 1
        for j, (d, i) in enumerate(cell): a *= i**e[j] << ((D[j] - e[j]) * d); b *= (i + 1)**e[j] << ((D[j] - e[j]) * d)
        if c > 0: lo += c * a; hi += c * b
        else: lo += c * b; hi += c * a
    return lo > 0 or hi < 0
leaves = [l for l in cert['leaves'] if l[6] == 'F' and l[7] == name]
slp = [l for l in leaves if not mono_ok(((l[0], l[1]), (l[2], l[3]), (l[4], l[5])))][:N]
def np_(terms): 
    s = '.nil'
    for e, c in reversed(terms): s = f'(.cons {c} {e[0]} {e[1]} {e[2]} {s})'
    return s
pos = [(e, c) for e, c in p if c > 0]; neg = [(e, -c) for e, c in p if c < 0]
def lv(ls):
    s = '.nil'
    for l in reversed(ls): s = f'(.cons {l[0]} {l[1]} {l[2]} {l[3]} {l[4]} {l[5]} {s})'
    return s
src = f'''import YantraCert.Check
set_option maxRecDepth 100000
namespace YantraCert.Bench
open YantraCert
def Pp : NP := {np_(pos)}
def Pn : NP := {np_(neg)}
def L : LL := {lv(slp)}
theorem ok : allLeaves (fun dx ix dy iy dz iz => slopeSign {D[0]} {D[1]} {D[2]} Pp Pn dx ix dy iy dz iz) L = true := by decide +kernel
end YantraCert.Bench
'''
open(os.path.join(HERE, 'lean/bench/BenchR.lean'), 'w').write(modulize(src))
print(len(p), 'terms', D, len(slp), 'leaves')
