"""Is 156 the most neighbour pairs C116 and Minana #377 can share? (27 Nov 2026; DICTO yes to the exact check.) With Claude (Anthropic).
The best pairing of faces is a quadratic assignment problem (Koopmans-Beckmann 1957). Exact model for the CP-SAT solver (OR-Tools):
x[a][t] = core face a goes to Minana face t (a bijection); kept[e] for each core neighbour pair e = (a, b) may be 1 only if the
partners are Minana neighbours: kept[e] + x[a][t] - sum_{u neighbour of t} x[b][u] <= 1 for every t (and the same with a, b swapped).
Maximise sum kept. Start hint: the floating-resin state (156). The solver reports its best pairing and a PROVED upper bound;
OPTIMAL means the bound equals the best found. Usage: python c116_qap.py [seconds]"""
import os, sys, json
from ortools.sat.python import cp_model
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json'))); faces, mf = d['faces'], d['minana_faces']
def adj(fl): return sorted((a, b) for a in range(60) for b in range(a + 1, 60) if len(set(fl[a]) & set(fl[b])) == 2)
EC, EM = adj(faces), adj(mf); assert len(EC) == len(EM) == 174
NM = {t: [u for u in range(60) if (min(t, u), max(t, u)) in set(EM)] for t in range(60)}
m = cp_model.CpModel()
x = [[m.NewBoolVar(f'x{a}_{t}') for t in range(60)] for a in range(60)]
for a in range(60): m.AddExactlyOne(x[a])
for t in range(60): m.AddExactlyOne([x[a][t] for a in range(60)])
# side counts must stay close? no: any bijection allowed (the floating state pairs pentagons with heptagons)
kept = {}
for a, b in EC:
    k = m.NewBoolVar(f'k{a}_{b}'); kept[(a, b)] = k
    for t in range(60):
        m.Add(k + x[a][t] - sum(x[b][u] for u in NM[t]) <= 1)
        m.Add(k + x[b][t] - sum(x[a][u] for u in NM[t]) <= 1)
m.Maximize(sum(kept.values()))
fl = json.load(open(os.path.join(HERE, '../data/c116/float.json')))[0]['pairing']
for a in range(60):
    for t in range(60): m.AddHint(x[a][t], int(fl[a] == t))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 600
s.parameters.num_workers = 16; s.parameters.log_search_progress = False
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(self): super().__init__(); self.n = 0
    def on_solution_callback(self):
        self.n += 1; print(f'  solution {self.n}: kept {int(self.ObjectiveValue())}, proved bound {int(self.BestObjectiveBound())}, {self.WallTime():.0f}s', flush=True)
st = s.Solve(m, CB())
best = int(s.ObjectiveValue()); bound = int(s.BestObjectiveBound())
print('status', s.StatusName(st), '; best kept', best, '; proved upper bound', bound, flush=True)
sig = [next(t for t in range(60) if s.Value(x[a][t])) for a in range(60)]
json.dump(dict(status=s.StatusName(st), best=best, bound=bound, pairing=sig), open(os.path.join(HERE, '../data/c116/qap.json'), 'w'))
kc = sum(1 for a, b in EC if (min(sig[a], sig[b]), max(sig[a], sig[b])) in set(EM))
print('recount of the best pairing:', kc, flush=True)
print('RESULT:', 'OPTIMAL: the most is %d' % best if bound == best else 'best found %d, at most %d (not closed)' % (best, bound))
print('FINAL ok' if kc == best and best >= 156 else 'FINAL FAIL (recount differs or below the hint)')
