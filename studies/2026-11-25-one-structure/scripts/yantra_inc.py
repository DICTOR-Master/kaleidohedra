"""The Sri Yantra's incidence structure (study 2026-11-08-sri-yantra, scripts/model.py; Chiodo's numbering): 27 lines
B1..B9 (bases), L1..L9 (left legs), R1..R9 (right legs); t1-t5 apex down, t6-t9 apex up; 31 triple points:
18 marmas (down-leg, base, up-leg on each side), 6 corner touches (same format) and 7 apex-on-base points; the 9 bases are
parallel. YREQ: which members must pass through the point inside a drawn side (a marma is interior to all three sides, an
apex lies inside its base, a corner touch inside the other triangle's leg)."""
MARMAS = [(1, 2, 7), (2, 3, 7), (1, 3, 8), (1, 4, 6), (1, 5, 9), (4, 6, 9), (2, 7, 9), (3, 7, 8), (3, 8, 9)]
CORNERS = [(4, 4, 8), (5, 5, 6), (2, 6, 6)]
APEX_ON_BASE = [(8, 1), (6, 2), (9, 3), (1, 6), (5, 7), (4, 8), (2, 9)]
B = lambda i: i - 1
L = lambda i: 8 + i
R = lambda i: 17 + i
NAMES = [f"B{i}" for i in range(1, 10)] + [f"L{i}" for i in range(1, 10)] + [f"R{i}" for i in range(1, 10)]
YTRIPLES = ([(L(a), B(b), L(c)) for a, b, c in MARMAS] + [(R(a), B(b), R(c)) for a, b, c in MARMAS]
            + [(L(a), B(b), L(c)) for a, b, c in CORNERS] + [(R(a), B(b), R(c)) for a, b, c in CORNERS]
            + [(L(a), R(a), B(b)) for a, b in APEX_ON_BASE])
# a corner touch (a, b, c): the corner of triangle b (its base and its own leg end there) lies inside the other triangle's leg
_corner = [(None, None, "int") if a == b else ("int", None, None) for a, b, c in CORNERS]
YREQ = [("int", "int", "int")] * 18 + _corner + _corner + [(None, None, "int")] * 7
assert len(YTRIPLES) == 31 and len(YREQ) == 31
NANY = [sum(1 for tr in YTRIPLES if y in tr) for y in range(27)]
NINT = [sum(1 for tr, rq in zip(YTRIPLES, YREQ) for z, r in zip(tr, rq) if z == y and r == "int") for y in range(27)]
NEED_ANY = sorted(NANY[:9], reverse=True)
NEED_INT = sorted(NINT[:9], reverse=True)
