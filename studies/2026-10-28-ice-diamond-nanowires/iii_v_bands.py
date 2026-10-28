# Belabbes, Panse, Furthmueller, Bechstedt, arXiv 1206.2209 (PRB 86, 075208 (2012)), Table II, LDA-1/2 QP with spin-orbit.
# Four polytypes 3C (h 0), 6H (1/3), 4H (1/2), 2H (1). Test: each quantity on the law line through 3C and 2H?
H=[0,1/3,1/2,1]
T={ # Eg (Gamma-Gamma where given), Delta_cf, dEv (meV), dEc (meV)
'GaAs':dict(Eg=[1.421,1.439,1.443,1.453],cf=[0,.052,.071,.129],dEv=[0,38,55,117],dEc=[0,56,77,149]),
'GaSb':dict(Eg=[.783,.806,.814,.835],cf=[0,.057,.076,.148],dEv=[0,57,67,95],dEc=[0,50,70,146]),
'InP': dict(Eg=[1.475,1.518,1.533,1.576],cf=[0,.029,.039,.062],dEv=[0,7,19,82],dEc=[0,50,77,183]),
'InAs':dict(Eg=[.411,.431,.440,.481],cf=[0,.034,.055,.095],dEv=[0,14,29,56],dEc=[0,34,58,126]),
'InSb':dict(Eg=[.230,.244,.249,.264],cf=[0,.036,.061,.113],dEv=[0,25,40,79],dEc=[0,39,59,113]),
'GaP': dict(Eg=[2.790,2.322,2.267,2.181],cf=[0,.021,.027,.045],dEv=[0,45,56,135],dEc=None)}
import statistics as st
summary={}
for c,d in T.items():
    for q,v in d.items():
        if v is None: continue
        span=v[3]-v[0]; line=[v[0]+span*h for h in H]
        dev=[(v[i]-line[i])/span*100 if span else 0 for i in (1,2)]   # deviation as % of the 3C->2H change
        summary.setdefault(q,[]).extend(dev)
        print(f'{c:5s} {q:4s} {v}  line at 6H,4H: {line[1]:.4g}, {line[2]:.4g}   off (% of 3C->2H change): 6H {dev[0]:+.0f}, 4H {dev[1]:+.0f}')
print()
for q,v in summary.items(): print(f'{q}: mean |off| {st.mean(abs(x) for x in v):.0f}% of the 3C->2H change; signs {"".join("+" if x>0 else "-" for x in v)}')
print('note GaP 3C is indirect (Gamma-X); Gamma-Gamma gaps listed: excluded from the Eg verdict')
