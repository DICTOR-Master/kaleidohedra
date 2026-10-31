# Part 2 of valley_law.py for further shapes (the skewed solids D1-D3, whose centre-foot lies outside some faces). Usage as valley_law.py.
import sys, json, os, multiprocessing as mp
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import valley_law as L
if __name__ == "__main__":
    sc = json.load(open(L.SC)); extra = ["D1", "D2", "D3"]
    items = [(r["D"], r["name"], r["file"], t) for r in sc if r["D"] in extra for t in (2.0, L.phi)]
    with mp.Pool(4) as pool: p2 = pool.map(L.part2, items)
    json.dump(p2, open(os.path.join(L.OUT, "valley-law-run-extra.json"), "w"), indent=1, default=float)
    for r in p2: print(r["D"], r["name"][:24], r["t"], "formula err %.2e" % r["formula_max_err"], "closed-yet-full", r["closed_yet_full"], "regrown", r["regrown_after_closing"], "closed", r["closed_edges"], "/", r["edges"])
