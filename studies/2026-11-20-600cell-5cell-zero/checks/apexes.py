"""Follow-up to dehn600.py: the 120 cap apexes, all five left orbits, and right orbits (mirror choice).
Exact Q(sqrt5) arithmetic reused from dehn600.py (imported, its checks rerun on import)."""
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import dehn600 as D
from itertools import combinations
from fractions import Fraction as F
ok=True
def check(name,c):
    global ok; ok&=bool(c); print(("PASS " if c else "FAIL ")+name)
Q5,V,C,cen,dot,idx,qmul,tri_cells=D.Q5,D.V,D.C,D.cen,D.dot,D.idx,D.qmul,D.tri_cells
cc=dot(cen[0],cen[0])  # |centroid|^2 ; apex = sqrt2 * centroid/|centroid| ; apex.apex' = 2 c.c'/cc
for oi,o in enumerate(D.orbits):
    U=set(o)
    ec={}
    for k in U:
        for e in combinations(C[k],2): ec[e]=ec.get(e,0)+1
    sh=sum(1 for x,y in tri_cells.values() if x in U and y in U)
    dots=sorted({(2*dot(cen[i],cen[j])/cc).f() for i in U for j in U if i<j})
    vset={2*dot(V[0],V[j]) for j in range(1,120)}
    aset={2*dot(cen[i],cen[j])/cc for i in [min(U)] for j in U if j!=i}
    check(f"left orbit {oi}: every edge in exactly one capped facet, no shared ridge; apexes form a regular 600-cell of radius sqrt2",
          len(ec)==720 and set(ec.values())=={1} and sh==0 and aset==vset)
# right orbits
Cset={frozenset(c):k for k,c in enumerate(C)}
R=set(Cset[frozenset(idx[qmul(V[i],g)] for i in C[0])] for g in V)
ec={}
for k in R:
    for e in combinations(C[k],2): ec[e]=ec.get(e,0)+1
check("right orbit of a facet: also 120 facets covering every edge once", len(R)==120 and set(ec.values())=={1})
# mirror x -> conj(x) maps left orbits to right orbits
conjv=lambda v:(v[0],-v[1],-v[2],-v[3])
Lm=set(Cset[frozenset(idx[conjv(V[i])] for i in C[k])] for k in D.orbits[0])
check("the mirror image (quaternion conjugation) of a left-orbit choice is a right-orbit choice",
      any(Lm==set(Cset[frozenset(idx[qmul(V[i],g)] for i in C[k0])] for g in V) for k0 in range(600)) )
print("FINAL ok" if ok else "FINAL MISMATCH")
