# Gnomon table of the golden cycle, exact where the Progenitors study gives exact volumes (o-dharma.txt layer volumes, cleo-star.txt,
# gap-pieces-exact.txt). Stations without exact data in the study (rTI, the hull jtI) are left out. Ratios V_next / V_prev in Q(√5),
# and each station as a multiple of I; marks ratios that are a power of φ or a rational number.
from fractions import Fraction as F
class Q:
    def __init__(s, a, b=0): s.a, s.b = F(a), F(b)
    def __add__(s, o): return Q(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Q(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    def __truediv__(s, o): n = o.a*o.a - 5*o.b*o.b; return s * Q(o.a / n, -o.b / n)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __float__(s): return float(s.a) + float(s.b) * 5 ** .5
    def __repr__(s): return f'{s.a}' + (f' + {s.b}√5' if s.b else '')
phi = Q(F(1, 2), F(1, 2)); I = Q(F(-5, 12), F(5, 12))
lay = {'I→ID': Q(F(65, 16), F(59, 48)), 'ID→O': Q(F(625, 912), F(289, 912)), 'O→TI': Q(F(-5965, 456), F(3551, 456)), 'TI→H': Q(F(-165, 2), F(75, 2)), 'H→RT': Q(F(-175, 4), F(81, 4))}
st = [('I', I), ('Cleo star', I * 2), ("D′", Q(F(10, 9), F(14, 27)))]
ID = I + lay['I→ID']; O = ID + lay['ID→O']; TI = O + lay['O→TI']; Hh = TI + lay['TI→H']; RT = Hh + lay['H→RT']
st += [('ID', ID), ('OG', O), ('TI', TI), ('H', Hh), ('RT', RT), ('M', Q(F(145, 12), F(65, 12))), ('I·φ³', Q(F(235, 12), F(35, 4)))]
assert RT == Q(-135, F(135, 2)), RT                      # matches gap-pieces-exact.txt (vol RT)
pw = [Q(1)]
for _ in range(12): pw.append(pw[-1] * phi)
def name(r):
    for k, p in enumerate(pw):
        if r == p: return f'= φ^{k}'
    if r.b == 0: return '= rational'
    return ''
print('station      volume (exact)                         × I            step ratio            ')
prev = None
for nm, V in st:
    r = V / prev if prev else None; mI = V / I
    print(f'{nm:10s} {str(V):38s} {float(mI):10.5f}   ' + (f'{float(r):9.5f} {name(r)}' if r else ''))
    prev = V
print('\nsteps from I: star 2·I; M = φ⁸·I (' + str(st[8][1] / I == pw[8]) + '); I·φ³ = φ⁹·I (' + str(st[9][1] / I == pw[9]) + ')')
for nm, V in st: 
    r = V / I; print(f'{nm:10s} / I = {r}   {name(r)}')
