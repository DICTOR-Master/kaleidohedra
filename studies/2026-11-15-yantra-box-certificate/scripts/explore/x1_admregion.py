"""Exploration: extent of the admissible region (#103 Theorem 1 inequalities only, no equations) in (u, t, S), by random sampling."""
import random, math
def construct(u, t, S):
    v = u; one = 1.0
    P = v**2 / (1 + v**2); R = one / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
    b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
    xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); w9 = k9 * (S - P)
    k3 = w3 / (1 - P); xZ = k3 * (1 - R)
    c138 = w1 * (R - b1) - xZ * (P - b1); Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
    m1 = w1 / (Q - b1); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); k7 = w7 / R
    b2 = m1 * Q / (m1 + k7); c4 = xF / (b8 - Q); c8 = xZ / (R - b1); b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
    b5 = (m1 * Q + k9 * P) / (m1 + k9); w5 = w6 * (b5 - b2) / (Q - b2)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: one, 7: 0.0}
    w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q), 8: xZ * (b8 - b1) / (R - b1), 9: w9}
    return b, w, a
def adm(u, t, S):
    try: b, w, a = construct(u, t, S)
    except ZeroDivisionError: return False
    if not all(b[i] < b[i+1] for i in range(1, 9)): return False
    if not all(w[i] > 0 for i in range(1, 10)): return False
    if not all((a[i] > b[i]) if i <= 5 else (a[i] < b[i]) for i in range(1, 10)): return False
    if not all(w[i]**2 + b[i]**2 - b[i] <= 0 for i in (2, 4, 5, 6, 8)): return False
    if not (b[5] < 0.5 < b[6]): return False
    return True
random.seed(1); N = 2_000_000; hits = []
for _ in range(N):
    u = random.random(); t = random.random() * u; R = 1/(1+u*u); S = R + random.random() * (1 - R)
    if adm(u, t, S): hits.append((u, t, S))
print('samples', N, 'admissible', len(hits))
if hits:
    for i, nm in enumerate('utS'):
        print(nm, 'range', min(h[i] for h in hits), max(h[i] for h in hits))
    print('t/u range', min(h[1]/h[0] for h in hits), max(h[1]/h[0] for h in hits))
    print('(S-R) range', min(h[2]-1/(1+h[0]**2) for h in hits), max(h[2]-1/(1+h[0]**2) for h in hits))
    print('(1-S) min', min(1-h[2] for h in hits))
