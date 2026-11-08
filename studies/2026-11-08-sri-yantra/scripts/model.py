"""Sri Yantra model (shared by every script in this study).

Frame: vertical axis = symmetry axis; d = DEPTH below the top point O of the circle,
so the circle is x^2 + (d - 1/2)^2 = 1/4 (diameter 1, O at d = 0, T at d = 1).
Nine isosceles triangles t1..t9 (Chiodo 2021 numbering): bases ordered top to bottom,
t1..t5 point down, t6..t9 point up.  Triangle ti has base depth b[i], base half-width w[i],
apex (0, a[i]).  A leg is the right-hand side x = w[i] * (d - a[i]) / (b[i] - a[i]).

Conditions (Chiodo 2021, (i)-(iii), equivalent to Huet 2002):
 (i)   t3, t7 inscribed in the circle: a3 = 1, a7 = 0, corners on the circle.
 (ii)  apex on base point: a8=b1, a6=b2, a9=b3, a1=b6, a5=b7, a4=b8, a2=b9.
 (iii) leg of down-triangle p, base of q, leg of up-triangle r concur (each side):
       MARMAS (9 pairs = 18 points): (1,2,7) (2,3,7) (1,3,8) (1,4,6) (1,5,9) (4,6,9)
                                     (2,7,9) (3,7,8) (3,8,9)
       CORNER TOUCHES (3 pairs = 6 points): (4,4,8) (5,5,6) (2,6,6)
Free parameters (Chiodo's P,Q,R,S): P=b3, Q=b6, R=b7, S=b9.
"""

MARMAS = [(1, 2, 7), (2, 3, 7), (1, 3, 8), (1, 4, 6), (1, 5, 9), (4, 6, 9), (2, 7, 9), (3, 7, 8), (3, 8, 9)]
CORNERS = [(4, 4, 8), (5, 5, 6), (2, 6, 6)]
APEX_ON_BASE = [(8, 1), (6, 2), (9, 3), (1, 6), (5, 7), (4, 8), (2, 9)]
DOWN = (1, 2, 3, 4, 5)


def solve(P, Q, R, S, w3, w7, sqrt, root=0, b1=None):
    """Exact sequential solution. w3, w7: half-widths of t3, t7 (w3^2 = P(1-P), w7^2 = R(1-R)).
    sqrt(z): exact square root in the caller's number system.  root picks the Apollonius branch.
    Returns dict b, w, a (index 1..9) and the quadratic (A, B, C) in b1 that closes the system."""
    xW = w7 * P / R                        # t7 leg on base of t3           (2,3,7)
    xX = xW * (S - R) / (S - P)            # t2 leg (apex S through W) at depth R  (2,7,9)
    # t9 leg: apex P, through (xX, R):  x = xX (d - P)/(R - P)
    # t3 leg: x = w3 (1 - d)/(1 - P).  Y = t3 & t9 -> depth b8               (3,8,9)
    k9 = xX / (R - P); k3 = w3 / (1 - P)
    b8 = (k3 + k9 * P) / (k3 + k9)
    xF = k9 * (Q - P)                      # t9 at depth Q, t4 leg passes here     (4,6,9)
    w6 = xW * (S - Q) / (S - P)            # t2 leg at depth Q = corner of t6       (2,6,6)
    xZ = k3 * (1 - R)                      # t3 at depth R, t8 leg passes here     (3,7,8)
    k7 = w7 / R
    # unknown b1 (apex of t8).  t8: x = xZ (d - b1)/(R - b1)
    # (1,3,8): t1 (apex Q): x = m1 (Q - d);  m1 (Q - P) = xZ (P - b1)/(R - b1)
    # (1,2,7): b2 = m1 Q/(m1 + k7);  (4,4,8): xF (b8 - b4)/(b8 - Q) = xZ (b4 - b1)/(R - b1)
    # (1,4,6): m1 (Q - b4) = w6 (b4 - b2)/(Q - b2)   -> quadratic in b1 (Apollonius)
    def pieces(b1):
        m1 = xZ * (P - b1) / ((R - b1) * (Q - P))
        b2 = m1 * Q / (m1 + k7)
        c4 = xF / (b8 - Q); c8 = xZ / (R - b1)
        b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
        return m1, b2, b4
    # clear denominators by hand: write everything as polynomials in b1 = t
    # m1 = mA (P - t)/(R - t) with mA = xZ/(Q-P)
    mA = xZ / (Q - P)
    # b2 = m1 Q/(m1+k7) = mA Q (P-t) / (mA (P-t) + k7 (R-t))
    # b4 = (c4 b8 (R-t) + xZ t) / (c4 (R-t) + xZ),  c4 = xF/(b8-Q)
    c4 = xF / (b8 - Q)
    # polynomial coefficients via evaluation at three points (equation is quadratic in t
    # after multiplying by D2 * D4 where D2 = mA(P-t)+k7(R-t), D4 = c4(R-t)+xZ)
    def F(t):
        D2 = mA * (P - t) + k7 * (R - t); N2 = mA * Q * (P - t)
        D4 = c4 * (R - t) + xZ; N4 = c4 * b8 * (R - t) + xZ * t
        # m1 (Q-b4)(Q-b2) - w6 (b4-b2) = 0, times D2*D4*(R-t)/(...)
        # m1 = mA (P-t)/(R-t); Q-b2 = k7 Q (R-t)/D2
        # => mA (P-t) * (Q D4 - N4) * k7 Q / (D2 D4) - w6 (N4 D2 - N2 D4)/(D2 D4) = 0
        return mA * (P - t) * (Q * D4 - N4) * k7 * Q - w6 * (N4 * D2 - N2 * D4)
    f0, f1, f2 = F(0), F(1), F(2)
    A = (f2 - 2 * f1 + f0) / 2; B = f1 - f0 - A; C = f0
    disc = B * B - 4 * A * C
    if b1 is None:                         # otherwise b1 is supplied exactly by the caller
        sq = sqrt(disc)
        b1 = (-B + sq) / (2 * A) if root == 0 else (-B - sq) / (2 * A)
    m1, b2, b4 = pieces(b1)
    # (1,5,9): t1 & t9 -> depth b5:  m1 (Q - d) = k9 (d - P)
    b5 = (m1 * Q + k9 * P) / (m1 + k9)
    # (5,5,6): corner of t5 at depth b5 lies on t6 leg: x = w6 (d - b2)/(Q - b2)
    w5 = w6 * (b5 - b2) / (Q - b2)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: 1, 7: 0}
    # half-widths: each leg evaluated at its own base depth
    w = {3: w3, 7: w7, 6: w6, 5: w5,
         1: m1 * (Q - b1),
         2: xW * (S - b2) / (S - P),
         4: xF * (b8 - b4) / (b8 - Q),
         8: xZ * (b8 - b1) / (R - b1),
         9: k9 * (S - P)}
    return dict(b=b, w=w, a=a, quad=(A, B, C), disc=disc)


def leg(tri, i):
    """Right leg of ti as (point1, point2) = (corner, apex)."""
    return ((tri['w'][i], tri['b'][i]), (0, tri['a'][i]))


def base(tri, i):
    return ((-tri['w'][i], tri['b'][i]), (tri['w'][i], tri['b'][i]))


def det3(p, q, r):
    """Concurrency test of three lines given as point pairs: returns the 3x3 determinant
    of their homogeneous line coordinates (zero iff concurrent or parallel)."""
    def line(pp):
        (x1, y1), (x2, y2) = pp
        return (y1 - y2, x2 - x1, x1 * y2 - x2 * y1)
    A, B, C = line(p), line(q), line(r)
    return (A[0] * (B[1] * C[2] - B[2] * C[1]) - A[1] * (B[0] * C[2] - B[2] * C[0])
            + A[2] * (B[0] * C[1] - B[1] * C[0]))


def all_conditions(tri):
    """Every condition as an expression that must vanish exactly. Returns list of (name, value)."""
    out = []
    for i in (3, 7):  # corners on the circle x^2 + (d-1/2)^2 = 1/4  <=>  x^2 + d^2 - d = 0
        out.append((f'circle t{i}', tri['w'][i] ** 2 + tri['b'][i] ** 2 - tri['b'][i]))
    out.append(('apex t3 on circle', tri['a'][3] ** 2 - tri['a'][3]))
    out.append(('apex t7 on circle', tri['a'][7] ** 2 - tri['a'][7]))
    for (p, q) in APEX_ON_BASE:
        out.append((f'apex t{p} = base point t{q}', tri['a'][p] - tri['b'][q]))
    for (p, q, r) in MARMAS:
        out.append((f'marma ({p},{q},{r})', det3(leg(tri, p), base(tri, q), leg(tri, r))))
    for (p, q, r) in CORNERS:
        out.append((f'corner ({p},{q},{r})', det3(leg(tri, p), base(tri, q), leg(tri, r))))
    return out


def marma_point(tri, p, q, r):
    """Right-hand marma point: on base of q, on leg of p (x from leg p at depth b[q])."""
    d = tri['b'][q]
    x = tri['w'][p] * (d - tri['a'][p]) / (tri['b'][p] - tri['a'][p])
    return (x, d)


def order_ok(tri, tol=0):
    """Configuration checks: bases strictly ordered, corners inside the closed disc, apex sides right."""
    b, w, a = tri['b'], tri['w'], tri['a']
    ok = all(b[i] < b[i + 1] for i in range(1, 9)) and all(w[i] > 0 for i in range(1, 10))
    ok = ok and all((a[i] > b[i]) if i in DOWN else (a[i] < b[i]) for i in range(1, 10))
    ok = ok and all(w[i] ** 2 + b[i] ** 2 - b[i] <= tol for i in range(1, 10))
    return bool(ok)
