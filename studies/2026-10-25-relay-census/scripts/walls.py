# Relay census, part C2 (added 2026-10-25 after the referee report on #53, point 5): the five interior wall segments of the
# perovskite chamber map, checked exactly at their midpoints. On an open wall segment no other wall crosses, so every slack
# keeps its sign and the face lattice is constant along it; one exact point per segment therefore covers the whole segment.
# Check: at each midpoint all three kinds have cells and at least one like bond exists (no switch point on any wall).
# Output: ../data/checks/perovskite-walls-checks.txt
from fractions import Fraction as Fr
from engine import Net, Cell
net = Net("perovskite ABX3", [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [(2, 0, 0), (0, 2, 0), (0, 0, 2)],
          [("A", (0, 0, 0)), ("B", (1, 1, 1)), ("X", (1, 1, 0)), ("X", (1, 0, 1)), ("X", (0, 1, 1))],
          {"A": (0, 1, 0), "B": (0, 0, 1), "X": (0, 0, 0)}, m=2)
MID = {"lam = 0, mu > 0": (Fr(0), Fr(1, 2)), "lam = 0, mu < 0": (Fr(0), Fr(-1, 2)),
       "lam + 2mu = 0, lam < 0": (Fr(-1), Fr(1, 2)), "lam + 2mu = 0, lam > 0": (Fr(1), Fr(-1, 2)), "lam + mu = 1": (Fr(1), Fr(0))}
out = []
for name, p in MID.items():
    cs = [Cell(net, i, p, Fr(40)) for i in range(len(net.motif))]
    alive = all(not c.empty for c in cs)
    bt = sorted(set("-".join(sorted((c.kind, c.H[k]["kind"]))) for c in cs if not c.empty for k in c.faces()))
    like = [t for t in bt if t in ("A-A", "B-B", "X-X")]
    ok = alive and bool(like)
    out.append(("PASS" if ok else "FAIL", f"perovskite wall {name}, midpoint ({p[0]}, {p[1]}): all kinds alive, a like bond present", " ".join(bt)))
    print(*out[-1])
with open("../data/checks/perovskite-walls-checks.txt", "w") as fh:
    for s, n, d in out: fh.write(f"{s} {n} {d}\n")
print(sum(o[0] == "PASS" for o in out), "/", len(out))
