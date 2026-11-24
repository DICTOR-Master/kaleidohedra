#!/usr/bin/env python3
"""The emptiness (§8): Betti numbers of the complexified complement (Orlik-Solomon) and region counts (Zaslavsky) of every Vacuus and Resonus in the catalogue, exact integers from the catalogue study's intersection data. Rank 3: chi(t)=t^3-N t^2+b2 t-b3 with b2=sum over intersection lines of (m-1), b3=b2-N+1 (chi(1)=0); Poincare polynomial (-t)^3 chi(-1/t) = 1+N t+b2 t^2+b3 t^3; regions = its value at 1, asserted equal to the traced region count."""
import os, json, math
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..','studies','2026-11-24-vacuus-resonus-catalogue','data'))
d=json.load(open('catalogue-all.json'))
names=['tetrahedron','octahedron','cube','icosahedron','dodecahedron','cuboctahedron','icosidodecahedron','truncated tetrahedron','truncated octahedron','truncated cube','rhombicuboctahedron','truncated cuboctahedron','snub cube','truncated icosahedron','truncated dodecahedron','rhombicosidodecahedron','truncated icosidodecahedron','snub dodecahedron','rhombic dodecahedron','rhombic triacontahedron']
E={e['name']:e for e in d}
def fac(N,b3):
  D=(N-1)**2-4*b3; r=math.isqrt(D) if D>=0 else -1
  if r>=0 and r*r==D: return ((N-1)-r)//2,((N-1)+r)//2
  return None
def recs(e):
  if 'corner' in e: return [('corner',e['corner'])]+([('volume',e['volume'])] if 'volume' in e else [])
  return [('',e)]
tot=split=0; splitlist=[]
for e in d:
  if e['family']=='Platonic polar': continue
  for cen,c in recs(e):
    for key in ['vacuus_arr','resonus_arr']:
      a=c[key]; N=a['planes']; b2=sum((int(m)-1)*k for m,k in a['point_multiplicities'].items()); b3=b2-N+1
      assert 1+N+b2+b3==a['regions']
      tot+=1
      if fac(N,b3): split+=1; splitlist.append((e['name'],cen,key[0],N,fac(N,b3),a['simplicial']))
for n in names:
  c=recs(E[n])[0][1]; out=[]
  for key in ['vacuus_arr','resonus_arr']:
    a=c[key]; N=a['planes']; b2=sum((int(m)-1)*k for m,k in a['point_multiplicities'].items()); b3=b2-N+1
    out.append((N,b2,b3,fac(N,b3),1+N+b2+b3))
  print(n,out)
print('split',split,'of',tot)
nonsimp=[s for s in splitlist if not s[5]]
print('split but not simplicial',len(nonsimp),nonsimp[:30])
simpnot=0
ns=0;bad=[]
for e in d:
  if e['family']=='Platonic polar': continue
  for cen,c in recs(e):
    for key in ['vacuus_arr','resonus_arr']:
      a=c[key]; N=a['planes']; b2=sum((int(m)-1)*k for m,k in a['point_multiplicities'].items()); b3=b2-N+1
      if a['simplicial']:
        ns+=1
        if not fac(N,b3): bad.append((e['name'],key))
print('simplicial',ns,'unsplit simplicial',bad)
