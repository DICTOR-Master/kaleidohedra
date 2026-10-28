# Group-IV polytypes vs the Hexagonality Law. Keller, Belabbes, Furthmueller, Bechstedt, Botti, arXiv 2302.10822, Table I
# (energies meV/atom, volume A^3 per atom pair; present work) and Ziembicki et al., arXiv 2404.05718, Table III (ANNNI, meV/bilayer pair).
H={'3C':0,'6H':1/3,'4H':1/2,'2H':1}
T1={'Si':{'E':{'3C':0,'6H':1.2,'4H':2.5,'2H':9.7},'V':{'3C':40.152,'6H':40.106,'4H':40.095,'2H':40.109}},
    'Ge':{'E':{'3C':0,'6H':4.5,'4H':7.1,'2H':16.0},'V':{'3C':45.596,'6H':45.535,'4H':45.516,'2H':45.493}}}
for el,d in T1.items():
    for q,v in d.items():
        span=v['2H']-v['3C']; out=[]
        for p in ('6H','4H'):
            line=v['3C']+span*H[p]; out.append(f"{p} {v[p]} vs line {line:.3f} ({(v[p]-line)/span*100:+.0f}% of change)")
        print(f'{el} {q}: '+'; '.join(out))
print()
J={'C':(25.448,-3.435,-0.337),'Si':(10.587,-2.593,-0.766),'Ge':(16.816,-1.054,-0.344),'Sn':(15.178,-0.222,-0.045),'SiC':(2.735,-2.424,-0.396)}
print('distance from the law, |J2|+|J3| over J1 (0 = exact law); #71 reference: cobalt 0.15-0.4, iron 0.17')
for k,(a,b,c) in sorted(J.items(),key=lambda kv:(abs(kv[1][1])+abs(kv[1][2]))/abs(kv[1][0])):
    print(f'  {k:4s} J1 {a:7.3f} J2 {b:7.3f} J3 {c:7.3f}   |J2/J1| {abs(b/a):.3f}   (|J2|+|J3|)/J1 {(abs(b)+abs(c))/abs(a):.3f}')
