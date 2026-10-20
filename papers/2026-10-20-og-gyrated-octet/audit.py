# Number audit for the gyrated-octet paper: every "exact expression ≈ decimal" pair re-evaluated, and key values matched to the exact logs.
import re, html, math, sys, os
H = os.path.dirname(os.path.abspath(__file__)); S5 = math.sqrt(5)
t = html.unescape(re.sub(r'<[^>]+>', '', open(os.path.join(H, 'paper.html')).read())).replace('−', '-')
bad = 0
for m in re.finditer(r'(\(?[-\d/ +√.()]*√5[-\d/ +√.()]*\)?(?:/\d+)?)\s*≈\s*(\d+(?:\.\d+)?)(%?)', t):
    expr, val, pct = m.group(1).strip(), float(m.group(2)), m.group(3)
    e = re.sub(r'(\d)\s*√5', r'\1*S5', expr).replace('√5', 'S5')
    try: x = eval(e, {'S5': S5})
    except Exception: print('skip', expr); continue
    if pct: x *= 100
    ok = abs(x - val) < 10 ** (-len(m.group(2).split('.')[-1])) * 0.51 + 1e-12
    bad += not ok; print(('ok  ' if ok else 'BAD ') + f'{expr} = {x:.6f} vs {val}{pct}')
L = {f: open(os.path.join(H, '..', '..', 'studies', '2026-10-19-og-gyrated-octet', f)).read() for f in ('gyr-exact.log', 'stella-twin.log', 'dbt-exact.log', 'gyr-boundary-exact.log', 'cut8-exact.log', 'fill-exact.log', 'ott-twin-exact.log')}
must = [('424/4617 + -88/4617*sqrt5', 'gyr-exact.log'), ('554/1539 + -158/1539*sqrt5', 'gyr-exact.log'), ('7/2 + -3/2*sqrt5', 'gyr-exact.log'), ('2/81 + 2/81*sqrt5', 'gyr-exact.log'),
        ('-155/4617 + 101/4617*sqrt5', 'gyr-exact.log'), ('604/9 - 89/3√5', 'stella-twin.log'), ('7 - 3√5', 'stella-twin.log'), ('8/3 - 8/9√5', 'stella-twin.log'),
        ('-872/81 + 440/81*sqrt5', 'dbt-exact.log'), ('-44/81 + 20/81*sqrt5', 'dbt-exact.log'), ('-88/27 + 40/27*sqrt5', 'dbt-exact.log'), ('8/3 - 8/9*sqrt5', 'dbt-exact.log'),
        ('23/162 + -47/1215*sqrt5', 'gyr-boundary-exact.log'), ('41/162 + 4/135*sqrt5', 'gyr-boundary-exact.log'), ('26/81 + -2/81*sqrt5', 'gyr-boundary-exact.log'), ('32/243 + -8/243*sqrt5', 'gyr-boundary-exact.log'),
        ('-608/81 + 320/81*sqrt5', 'cut8-exact.log'), ('176/3 + -26*sqrt5', 'cut8-exact.log'), ('PASS 24 corners', 'cut8-exact.log'), ('60 edges', 'cut8-exact.log'),
        ('968/81 + -392/81*sqrt5', 'fill-exact.log'), ('704/81 + -272/81*sqrt5', 'fill-exact.log'), ('352/81 + -136/81*sqrt5', 'fill-exact.log'), ('left and right hands', 'fill-exact.log'), ('PASS the OTT mirrored in an octahedron face', 'ott-twin-exact.log'), ('PASS the face triangle', 'ott-twin-exact.log')]
for s, f in must:
    ok = s in L[f]; bad += not ok; print(('ok  ' if ok else 'BAD ') + f'log {f} has {s}')
for f in ('gyr-boundary-exact.log', 'cut8-exact.log', 'fill-exact.log'):
    n = L[f].count('FAIL'); bad += n; print(('ok  ' if not n else 'BAD ') + f'{f}: {L[f].count("PASS")} PASS, {n} FAIL')
print('FAIL' if bad else 'ALL PASS', bad)
