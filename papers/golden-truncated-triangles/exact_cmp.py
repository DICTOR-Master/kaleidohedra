# Exact (sympy, Q(sqrt5)) scale-free congruence: atlas slice vs dataset solid / exact golden-cut icosahedron.
import sys, os, json, itertools, sympy as sp
sys.path.insert(0, os.path.expanduser('~/work/studies/2026-10-27-white-queen-polar/scripts'))
os.chdir(os.path.expanduser('~/work/studies/2026-10-27-white-queen-polar/scripts'))
import atlas120 as A
from fractions import Fraction as Fr
s5 = sp.sqrt(5); G = (1+s5)/2
def q2s(q):  # Q5 -> sympy via q5str
    return sp.nsimplify(A.q5str(q).replace('√5','*sqrt(5)').replace(' ', ''))
def invariant(P):
    P = [sp.Matrix(p) for p in P]; c = sum(P, sp.zeros(3,1))/len(P); P = [p-c for p in P]
    d2 = [sp.expand((a-b).dot(a-b)) for a,b in itertools.combinations(P,2)]; tot = sp.expand(sum(d2))
    return sorted((sp.radsimp(sp.simplify(x/tot)) for x in d2), key=float)
def slice_pts(lab, h, at):
    d = A.DIRS[lab][0]; hs = sorted(set(A.dot(p, d) for p in A.R), key=float); tip = hs[-1]
    item, keep, _ = A.cut((lab, h, at, tip))
    sp_ = A.Space(4, d, None)
    # exact 3D coords of hull vertices: hh V are exact points in the slice space
    return [[q2s(c) for c in v] for v in item_pts(keep, lab, h, at, tip)]
def item_pts(keep, lab, h, at, tip):
    # recompute exact hull points: redo cut internals (pts exact) and keep those that are hull vertices (match floats)
    d = A.DIRS[lab][0]; spc = A.Space(4, d, None); H = [A.dot(p, d) for p in A.R]; pts = []
    for p, x in zip(A.R, H):
        if x == h: pts.append(spc.y(p))
    for a, b in A.E:
        ha, hb = H[a], H[b]
        if ((ha - h) * (hb - h)).sign() < 0:
            t = (h - ha) / (hb - ha); pts.append(spc.y(tuple(x + t * (y - x) for x, y in zip(A.R[a], A.R[b]))))
    fV = [tuple(round(float(c), 9) for c in v) for v in keep['fV']]
    out = [p for p in pts if tuple(round(float(c), 9) for c in p) in set(fV)]
    assert len(out) == len(fV), (len(out), len(fV)); return out
def ds(name):
    w = json.load(open(os.path.expanduser(f'~/work/dataset-v7/solids/{name}.json'))); return [[sp.sympify(c) for c in v['exact']] for v in w['vertices']]
def golden_icosa(x):
    P = [sp.Matrix(p)/2 for a in (-1,1) for b in (-1,1) for p in ([0,a,b*G],[a,b*G,0],[b*G,0,a])]
    E = [(i,j) for i,j in itertools.combinations(range(12),2) if sp.simplify((P[i]-P[j]).dot(P[i]-P[j])-1)==0]
    return [list(P[i]+x*(P[j]-P[i])) for i,j in E]+[list(P[j]+x*(P[i]-P[j])) for i,j in E]
Q5 = A.Q5
tests = [('cell-first', Q5(Fr(9,16),Fr(1,4)), True, 'greater golden TI', golden_icosa(1/G**2)),
         ('cell-first', Q5(Fr(29,32),Fr(13,32)), True, 'lesser golden TI', golden_icosa(1/(G*s5))),
         ('cell-first', Q5(Fr(33,32),Fr(15,32)), False, 'TI Star core', ds('dicto-ti-star-core')),
         ('vertex-first', Q5(Fr(11,8),Fr(5,8)), True, 'Icosaxes', ds('dicto-icosaxes')),
         ('cell-first', Q5(Fr(29,64),Fr(13,64)), False, 'White Knight', ds('dicto-white-knight'))]
for lab, h, at, name, target in tests:
    S = slice_pts(lab, h, at); a = invariant(S); b = invariant(target)
    same = len(a)==len(b) and all(sp.simplify(x-y)==0 for x,y in zip(a,b))
    print(name, lab, A.q5str(h), 'exact congruent up to scale:', same, '(n=%d)' % len(S), flush=True)
