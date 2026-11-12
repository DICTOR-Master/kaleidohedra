"""Referee's own model of the based ring of C0(A3) x| C2 (Section 5 labels) and
tube-corner dimensions sum_s sum_k N_{s i}^k N_{i s}^k, compared with Table 'tab:frames'."""
import itertools, re, sys, json
from collections import Counter
def comp(u, v): return tuple(u[v[i]] for i in range(4))
e = (0, 1, 2, 3)
gens = []
for k in range(3):
    t = list(e); t[k], t[k+1] = t[k+1], t[k]; gens.append(tuple(t))
order = [e]; word = {e: ()}
q = [e]
while q:
    w = q.pop(0)
    for k, s in enumerate(gens):
        ws = comp(w, s)
        if ws not in word:
            word[ws] = word[w] + (k,); order.append(ws); q.append(ws)
assert len(order) == 24
def ell(w): return sum(1 for a in range(4) for b in range(a+1, 4) if w[a] > w[b])
def sig(w): return tuple(3 - w[3 - i] for i in range(4))
# Hecke-Fibonacci based ring on S4:  X_s X_w = X_sw (+ X_w if l(sw)<l(w))
def left_s(k, vec):
    s = gens[k]; out = Counter()
    for w, c in vec.items():
        sw = comp(s, w); out[sw] += c
        if ell(sw) < ell(w): out[w] += c
    return out
def mult(u, v):  # X_u X_v
    vec = Counter({v: 1})
    for k in reversed(word[u]): vec = left_s(k, vec)
    return vec
labels = [(w, 0) for w in order] + [(w, 1) for w in order]
idx = {l: i for i, l in enumerate(labels)}
def cmult(a, b):  # (w,g)(w',g') = X_w X_{sigma^g(w')} h^{g+g'}
    (w, g), (w2, g2) = a, b
    w2s = sig(w2) if g else w2
    return Counter({(x, (g+g2) % 2): c for x, c in mult(w, w2s).items()})
N = {}
for a in labels:
    for b in labels:
        N[(idx[a], idx[b])] = Counter({idx[k]: c for k, c in cmult(a, b).items()})
# sanity: associativity on all triples (based ring)
def mulvec(vec, j):
    out = Counter()
    for i, c in vec.items():
        for k, d in N[(i, j)].items(): out[k] += c*d
    return out
def lmul(i, vec):
    out = Counter()
    for j, c in vec.items():
        for k, d in N[(i, j)].items(): out[k] += c*d
    return out
assoc = all(mulvec(N[(i, j)], k) == lmul(i, N[(j, k)]) for i in range(48) for j in range(48) for k in range(48))
print("associative:", assoc)
dual = {}
for i in range(48):
    for j in range(48):
        if N[(i, j)][0] == 1: dual[i] = j
w, g = labels[5]
paper_dual = lambda l: ((sig(tuple(sorted(range(4), key=lambda t: l[0][t]))) if l[1] else tuple(sorted(range(4), key=lambda t: l[0][t]))), l[1])
print("duality matches paper formula (w,g)* = (sigma^g(w^-1),g):", all(labels[dual[i]] == paper_dual(labels[i]) for i in range(48)))
def corner(i, j=None):
    j = i if j is None else j
    return sum(N[(s, i)][k] * N[(j, s)][k] for s in range(48) for k in N[(s, i)])
dims = [corner(i) for i in range(48)]
print("corner dims:", dims)
tex = open(sys.argv[1], encoding="utf8").read()
tab = tex[tex.index("\\label{tab:frames}"):tex.index("\\end{tabular}", tex.index("\\label{tab:frames}"))]
paper = {}
for m in re.finditer(r"^(\d+)&(\d+)&.*?&(\d+)&(\d+)&", tab, re.M):
    paper[int(m.group(1))] = int(m.group(2)); paper[int(m.group(3))] = int(m.group(4))
mism = [(i, dims[i], paper[i]) for i in range(48) if dims[i] != paper[i]]
print("table entries parsed:", len(paper), " mismatches:", mism)
for J in ([0, 2, 5, 11], [24, 26, 29, 35]):
    tot = sum(corner(i, j) for i in J for j in J)
    even = sum(N[(s, i)][k] * N[(j, s)][k] for i in J for j in J for s in range(24) for k in N[(s, i)])
    print("selected", J, "total dim", tot, "even-winding dim", even, "fixed by sigma:", all(idx[(sig(labels[i][0]), labels[i][1])] in J for i in J))
print("label 47 =", labels[47], "w0?", ell(labels[47][0]) == 6)
# FPdim
import math
phi = (1+5**.5)/2
print("sum d^2 =", sum(phi**(2*ell(l[0])) for l in labels), " D=", 1080+480*5**.5)
