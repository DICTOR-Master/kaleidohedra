# BaMnO3 polytypes vs h: Chen and Millis, arXiv 1509.06650 (PRB), Table II, DFT (GGA+U), per Mn. 2H h=1, 4H h=1/2, cubic h=0.
data={'FM': {'E':(103,186,837),'V':(71.6,66.4,62.9)}, 'AFM':{'E':(0,109,775),'V':(71.0,66.1,61.9)}}
for m,d in data.items():
    for q,(a2h,a4h,ac) in d.items():
        line=(a2h+ac)/2
        print(f'{m:3s} {q}: 2H {a2h}  4H {a4h}  3C {ac}   law line at h=1/2 {line:.2f}   4H off {a4h-line:+.2f} ({(a4h-line)/line*100:+.1f}%)')
