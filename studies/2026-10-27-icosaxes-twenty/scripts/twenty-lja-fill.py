exec(open('twenty-lja.py').read().split("print('piece volume'")[0])
touch = 2.267283
def hollow(f): return -sum(p.volume() for p in U_at(touch * f).decompose() if p.volume() < -1e-7)
a, b = 0.3, 0.15
for _ in range(36):
    m = (a + b) / 2; a, b = (m, b) if hollow(m) > 1e-9 else (a, m)
phi = (1 + 5 ** .5) / 2
print(f'hollow fills at {(a + b) / 2:.6f} of touch; 1/phi^3 = {phi ** -3:.6f}; hollow at 1/3: {hollow(1 / 3):.6f}, at 1/phi: {hollow(1 / phi + 1e-7):.6f}')
