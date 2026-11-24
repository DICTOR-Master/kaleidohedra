from math import isqrt
def fib_stacking(N):   # the ENTRIES.md program, unchanged
    w = 'c'
    while len(w) < N: w = ''.join('ch' if t == 'c' else 'c' for t in w)
    a = [0, 1]; s = 1
    for k in range(1, N-1):
        if w[k] == 'h': s = -s
        a.append((a[-1] + s) % 3)
    return a[:N]
# independent method: layer types from the Beatty form of the Fibonacci word, exact integer floor(n/phi) = floor((isqrt(5n^2)-n)/2)
def fl_over_phi(n): return (isqrt(5*n*n) - n) // 2
def h(n):  # A003849(n) as 1 for h: 1 + floor((n+1)/phi) - floor((n+2)/phi)
    return 1 + fl_over_phi(n+1) - fl_over_phi(n+2)
def by_rule(N):
    a = [0, 1]
    for k in range(1, N-1):
        step = (a[k] - a[k-1]) % 3
        a.append((a[k] + (step if h(k) == 0 else -step)) % 3)
    # Jagodzinski check: layer k is h iff its two neighbours have the same position
    assert all((a[k-1] == a[k+1]) == (h(k) == 1) for k in range(1, N-1))
    return a
N = 2000
A, B = fib_stacking(N), by_rule(N)
assert A == B
w = 'c'
while len(w) < N: w = ''.join('ch' if t == 'c' else 'c' for t in w)
assert all((w[k] == 'h') == (h(k) == 1) for k in range(N))
s69 = 'ABACBCACBABCACBCABACABCBAC'
assert ''.join('ABC'[x] for x in A[:26]) == s69
d = ''
n = 0
for x in A:
    t = (',' if d else '') + str(x)
    if len(d) + len(t) > 260: break
    d += t; n += 1
print(n, len(d)); print(d)
print("FINAL ok: two methods agree to n = 1999; Jagodzinski types = Fibonacci word; #69's 26 letters match")
fphi = lambda k: (k + isqrt(5*k*k)) // 2          # floor(phi*k), exact
A085002 = lambda k: fphi(k) % 2
assert all(A[n] == (2*sum(A085002(k) for k in range(2, n+2)) - n) % 3 for n in range(N))
print("FINAL ok formula with A085002, n < 2000")
