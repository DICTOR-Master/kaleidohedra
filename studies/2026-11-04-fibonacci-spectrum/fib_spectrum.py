#!/usr/bin/env python3
"""Spectrum of DICTO's Fibonacci stacking (#69; DICTO 4 Nov 2026 "can fibonacci be harmonized to any degree" / "run the fibonacci spectrum").
Word: Fibonacci (Sturmian) c/h word with h-density 1/φ² (h at n where floor((n+1)/φ²) − floor(n/φ²) = 1).
(1) spectrum of the h-indicator; (2) stacking diffraction along the axis: layer positions x_n in {0,1,2} (A,B,C) from the word
(h: x_{n+1} = x_{n−1}; c: the third position), rod amplitude A(l) = mean ω^{x_n} e^{2πi l n}, ω = e^{2πi/3}.
Peaks are listed with positions written as m + n/φ² (mod 1) where they fit."""
import math, json, os
import numpy as np
phi = (1 + 5**.5)/2; a = 1/phi**2
N = 317811   # F_28
n = np.arange(N); h = (np.floor((n + 1)*a) - np.floor(n*a)).astype(int)
print('h density', h.mean(), 'target', a)
def peaks(sig, k=10):
    F = np.fft.fft(sig)/len(sig); I = np.abs(F); freqs = np.fft.fftfreq(len(sig))
    idx = np.argsort(I)[::-1]; out = []
    for i in idx:
        f = freqs[i] % 1
        if f < 1e-9 or any(abs(f - g) < 2e-5 for g, _ in out): continue
        out.append((f, float(I[i])))
        if len(out) >= k: break
    return out
def ident(f):
    best = None
    for q in range(-30, 31):
        r = (q*a) % 1
        for target in (f, 1 - f):
            d = abs(r - target)
            if d < 1e-4 and (best is None or abs(q) < abs(best)): best = q if target == f else -q
    return best
res = {}
print('(1) c/h word spectrum: frequency, amplitude, q with f = q/φ² mod 1, |sin(π q/φ²)|/(π q)·... check')
P1 = peaks(h - h.mean(), 12); res['word'] = []
for f, A in P1:
    q = ident(f); pred = abs(math.sin(math.pi*q*a))/(math.pi*abs(q)) if q else None
    res['word'].append((f, A, q, pred)); print(f'  f {f:.6f}  amp {A:.5f}  q {q}  formula {pred if pred is None else round(pred,5)}')
x = [0, 1]
for k in range(1, N - 1): x.append(x[k-1] if h[k] else 3 - x[k] - x[k-1])
w = np.exp(2j*math.pi*np.array(x)/3)
print('(2) stacking diffraction (rod with h − k ≠ 0 mod 3): l (in units of 1/layer), amplitude')
P2 = peaks(w, 12); res['stacking'] = []
for f, A in P2:
    q = None
    for qq in range(-30, 31):
        for base in (1/3, 2/3):
            if abs(((base + qq*a) % 1) - f) < 1e-4 and (q is None or abs(qq) < abs(q[1])): q = (base, qq)
    res['stacking'].append((f, A, q)); print(f'  l {f:.6f}  amp {A:.5f}  = {q[0]:.4f} + {q[1]}/φ² (mod 1)' if q else f'  l {f:.6f}  amp {A:.5f}')
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fib-spectrum.json'), 'w'), indent=1, default=str)
