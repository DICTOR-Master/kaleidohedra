import sys, numpy as np
sys.argv=['vacuus_queens.py','none']
src=open('vacuus_queens.py').read().split("out = []")[0]
exec(src)
for name in ['600-cell','120-cell']:
    X,F=stage(name); mats=sym_group(X)
    R=[]
    for M in mats:
        if np.allclose(M,M.T,atol=1e-7) and np.isclose(np.linalg.det(M),-1):
            ev,vec=np.linalg.eigh(M)
            if np.sum(np.isclose(ev,-1,atol=1e-6))==1: R.append(vec[:,np.argmin(ev)])
    N=[normal_of(X[f]) for f in F]
    def has(n,L): return any(abs(abs(n@m)-1)<1e-7 for m in L)
    planes=[]
    for n in N:
        if not has(n,planes): planes.append(n)
    print(name, 'mirrors', len(R), 'Vacuus planes', len(planes), 'every Vacuus plane is a mirror:', all(has(n,R) for n in planes), '| every mirror is a Vacuus plane:', all(has(r,planes) for r in R))
