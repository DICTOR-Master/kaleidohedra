exec(open('twenty-lja.py').read().split("print('piece volume'")[0])
touch = 2.267283
def parts(f):
    U = U_at(touch * f); P = sorted(U.decompose(), key=lambda m: -m.volume())
    # a part with tiny volume is a cavity's boundary when it is negative-oriented; report signed volumes and genus
    return U.genus(), [(round(p.volume(), 5), p.genus()) for p in P]
for f in [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.66, 0.64, 0.63, 0.62, 0.618034, 0.61, 0.5, 0.4, 0.34, 0.3334, 0.3333, 0.3, 0.25, 0.2, 0.15, 0.1]:
    g, p = parts(f); print(f'{f:.6f}: genus {g:3d} | parts (volume, genus): {p[:6]}{" ..." if len(p) > 6 else ""} ({len(p)})')
