# Mutant for the harness self-test (G6): zsign comparing u^2 with 4 v^2 instead of 5 v^2.
def zadd(u, v): return (u[0] + v[0], u[1] + v[1])
def zmul(u, v): return (u[0]*v[0] + u[1]*v[1], u[0]*v[1] + u[1]*v[0] + u[1]*v[1])
def zsign(u):
    x, y = u; a, b = 2*x + y, y
    if a >= 0 and b >= 0: return 0 if a == 0 and b == 0 else 1
    if a <= 0 and b <= 0: return -1
    return (1 if a > 0 else -1) if a*a > 4*b*b else (1 if b > 0 else -1)
