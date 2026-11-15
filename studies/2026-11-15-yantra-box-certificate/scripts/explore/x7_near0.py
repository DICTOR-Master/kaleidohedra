"""Exploration: near u = 0 and near (u, tau) = (1, 1) on the G = 0 branch: which inequalities fail, for which tau (mpmath 60 digits)."""
import mpmath as mp
mp.mp.dps = 80
import sys; sys.path.insert(0, '.')
def construct(u, t, S):
    v = u; one = mp.mpf(1)
    P = v**2 / (1 + v**2); R = one / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
    b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
    xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); w9 = k9 * (S - P)
    k3 = w3 / (1 - P); xZ = k3 * (1 - R)
    c138 = w1 * (R - b1) - xZ * (P - b1); Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
    m1 = w1 / (Q - b1); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); k7 = w7 / R
    b2 = m1 * Q / (m1 + k7); c4 = xF / (b8 - Q); c8 = xZ / (R - b1); b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
    b5 = (m1 * Q + k9 * P) / (m1 + k9); w5 = w6 * (b5 - b2) / (Q - b2)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: one, 7: mp.mpf(0)}
    w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q), 8: xZ * (b8 - b1) / (R - b1), 9: w9}
    out = {}
    for i in range(1, 9): out[f'b{i+1}-b{i}'] = b[i+1] - b[i]
    for i in range(1, 10): out[f'w{i}'] = w[i]
    for i in range(1, 10): out[f'apex{i}'] = (a[i] - b[i]) if i <= 5 else (b[i] - a[i])
    for i in (2, 4, 5, 6, 8): out[f'disc{i}'] = -(w[i]**2 + b[i]**2 - b[i])
    out['1/2-b5'] = 0.5 - b[5]; out['Q-1/2'] = b[6] - 0.5
    return out
def Sbranch(u):
    a = (u**2 + 1)**2 * (u**6 + u**4 - 2*u**2 + 1); b = -(u**2 + 1) * (3*u**6 - u**4 - u**2 + 1); c = u**6
    return (-b + mp.sqrt(b*b - 4*a*c)) / (2*a)          # the root in (R, 1)
for u in [mp.mpf(x) for x in ('0.3', '0.2', '0.1', '0.03', '0.01', '0.001')] + [1 - mp.mpf(x) for x in ('0.05', '0.01', '0.001')]:
    S = Sbranch(u); R = 1/(1+u*u); fails = {}
    taus = [mp.mpf(k) / 1000 for k in range(1, 1000)] + [mp.mpf(10)**(-j) for j in range(4, 12)]
    for tau in taus:
        q = construct(u, u * tau, S)
        for n, v in q.items():
            if v <= 0: fails.setdefault(n, []).append(tau)
    always = [n for n, l in fails.items() if len(l) == len(taus)]
    cover = {}
    for tau in taus:
        q = construct(u, u * tau, S); f = [n for n, v in q.items() if v <= 0]
        cover[len(f) > 0] = cover.get(len(f) > 0, 0) + 1
    print(f'u={mp.nstr(u, 6)} S-R={mp.nstr(S-R, 4)} rho={mp.nstr((S-R)/((1-R)*(1-u)), 6)}: fail for all tau: {always}; tau with some failure: {cover}')
    for n in ('w4', 'w5', 'w6', 'b4-b3', 'b5-b4', 'disc4', 'apex5'):
        if n in fails: print(f'    {n} fails on tau in [{mp.nstr(min(fails[n]), 3)}, {mp.nstr(max(fails[n]), 3)}] ({len(fails[n])} of {len(taus)})')
