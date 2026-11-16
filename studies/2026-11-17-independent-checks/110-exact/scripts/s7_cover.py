"""Item 6 (part 2): fewest dual copies covering all 720 pentagons.
usage: s7_cover.py FAMILY MODE K TIMELIMIT [fix0]
  FAMILY  A | B | C3
  MODE    find   : CP-SAT search for a cover with <= K copies; verified as a set union
          cpsat  : CP-SAT, is there a cover with <= K copies?   (INFEASIBLE = proof)
          cpsatmin: as cpsat, also minimising the number (LP-based bounding)
          highs  : HiGHS MIP, minimise the number of copies (dual bound > K = proof)
          sat    : CaDiCaL (pysat) with a totalizer at-most-K encoding (UNSAT = proof)
  fix0    optional: force copy 0 into the cover.  Justified: the symmetry group
          of Q is transitive on the copies (exact, s6/W-orbit), so if a cover of
          size <= K exists, an image of it under a symmetry contains copy 0.
No other symmetry breaking is used."""
import json, sys, time, threading
from common import Log

fam, mode, K, T = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
fix0 = len(sys.argv) > 5 and sys.argv[5] == 'fix0'
tag = f'{fam}_{mode}_le{K}' + ('_fix0' if fix0 else '')
L = Log(f'logs/s7_cover_{tag}.log')
inst = json.load(open('data/dual_cover_instance.json'))
sets = inst[fam]['sets']
n = len(sets)
cov = [[] for _ in range(720)]
for c, s in enumerate(sets):
    for p in s:
        cov[p].append(c)
L(f'family {fam}*: {n} copies, 720 pentagons, copies per pentagon {sorted({len(c) for c in cov})}; '
  f'question: cover with <= {K} copies; fix0={fix0}')
t0 = time.time()
verdict = None
if mode in ('find', 'cpsat', 'cpsatmin'):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{c}') for c in range(n)]
    for p in range(720):
        m.AddBoolOr([x[c] for c in cov[p]])
    m.Add(sum(x) <= K)
    if mode == 'cpsatmin':
        # same question, with the objective given to CP-SAT so that its LP-based
        # workers can raise the lower bound (proof: infeasible or bound > K)
        m.Minimize(sum(x))
    if fix0:
        m.Add(x[0] == 1)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = T
    s.parameters.num_workers = 24
    if mode == 'cpsatmin':
        s.parameters.linearization_level = 2
    st = s.Solve(m)
    name = s.StatusName(st)
    L(f'CP-SAT status {name}, wall time {s.WallTime():.1f} s, branches {s.NumBranches()}, conflicts {s.NumConflicts()}')
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = [c for c in range(n) if s.Value(x[c])]
        U = set()
        for c in chosen:
            U |= set(sets[c])
        ok = len(U) == 720
        L(f'cover found with {len(chosen)} copies: {chosen}; union = all 720 pentagons: {ok}')
        mult = [sum(1 for c in chosen if p in set(sets[c])) for p in range(720)]
        L(f'multiplicity histogram {{times covered: pentagons}}: {dict(sorted(__import__("collections").Counter(mult).items()))}')
        json.dump({'family': fam, 'copies': chosen, 'size': len(chosen), 'union_is_all_720': ok,
                   'copy_corner_ids': [inst[fam]['copies_600cell_corner_ids'][c] for c in chosen]},
                  open(f'data/cover_{fam}_{len(chosen)}.json', 'w'))
        verdict = 'FEASIBLE' if ok else 'BAD'
        if mode == 'cpsatmin' and st == cp_model.OPTIMAL and len(chosen) == K:
            pass
    elif st == cp_model.INFEASIBLE:
        verdict = 'INFEASIBLE'
    else:
        verdict = 'UNKNOWN'
elif mode == 'highs':
    import highspy, numpy as np
    h = highspy.Highs()
    h.setOptionValue('time_limit', T)
    h.setOptionValue('mip_rel_gap', 0.0)
    h.setOptionValue('threads', 24)
    h.setOptionValue('output_flag', False)
    inf = highspy.kHighsInf
    for c in range(n):
        h.addVar(0.0, 1.0)
    h.changeColsIntegrality(n, np.arange(n, dtype=np.int32), np.array([highspy.HighsVarType.kInteger] * n))
    h.changeColsCost(n, np.arange(n, dtype=np.int32), np.ones(n))
    for p in range(720):
        h.addRow(1.0, inf, len(cov[p]), np.array(cov[p], dtype=np.int32), np.ones(len(cov[p])))
    if fix0:
        h.changeColBounds(0, 1.0, 1.0)
    h.run()
    ms = h.getModelStatus()
    info = h.getInfo()
    obj = info.objective_function_value
    db = info.mip_dual_bound
    L(f'HiGHS status {h.modelStatusToString(ms)}, objective {obj}, dual bound {db}, '
      f'nodes {info.mip_node_count}, time {time.time() - t0:.1f} s')
    if h.modelStatusToString(ms) == 'Optimal':
        sol = h.getSolution().col_value
        chosen = [c for c in range(n) if sol[c] > 0.5]
        U = set()
        for c in chosen:
            U |= set(sets[c])
        L(f'HiGHS optimum {len(chosen)} copies, union all 720: {len(U) == 720}')
        verdict = 'INFEASIBLE' if db > K + 1e-6 and len(U) == 720 else 'FEASIBLE'
    else:
        verdict = 'INFEASIBLE' if db > K + 1e-6 else 'UNKNOWN'
elif mode == 'sat':
    # the solver runs in a child process that is killed at the time limit
    import multiprocessing as mp
    def child(q):
        from pysat.card import CardEnc, EncType
        from pysat.solvers import Solver
        cnf = CardEnc.atmost(lits=list(range(1, n + 1)), bound=K, top_id=n, encoding=EncType.totalizer)
        with Solver(name='cadical195', bootstrap_with=cnf.clauses) as S:
            for p in range(720):
                S.add_clause([c + 1 for c in cov[p]])
            if fix0:
                S.add_clause([1])
            r = S.solve()
            mdl = S.get_model() if r else None
            q.put((r, mdl, str(S.accum_stats()), len(cnf.clauses), cnf.nv))
    ctx = mp.get_context('fork')
    q = ctx.Queue()
    pr = ctx.Process(target=child, args=(q,))
    pr.start()
    pr.join(T)
    if pr.is_alive():
        pr.kill()
        L(f'CaDiCaL (totalizer at-most-{K}): no answer within {T} s')
        verdict = 'UNKNOWN'
    else:
        r, mdl, stats, ncl, nv = q.get()
        L(f'CaDiCaL (totalizer at-most-{K}, {ncl} cardinality clauses, {nv} vars): '
          f'{"SAT" if r else "UNSAT"}, time {time.time() - t0:.1f} s, stats {stats}')
        if r:
            chosen = [c for c in range(n) if mdl[c] > 0]
            U = set()
            for c in chosen:
                U |= set(sets[c])
            L(f'SAT cover {len(chosen)} copies, union all 720: {len(U) == 720}')
            verdict = 'FEASIBLE'
        else:
            verdict = 'INFEASIBLE'
L(f'VERDICT {fam}* cover with <= {K} copies: {verdict}; runtime {time.time() - t0:.1f} s')
if verdict in ('UNKNOWN', 'BAD'):
    L.fails.append(f'{tag} {verdict}')
L.final()
