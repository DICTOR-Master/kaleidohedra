"""Run a list of census settings in parallel. Usage: run_matrix.py CONFIGS.jsonl WORKERS
Each line: {"data", "run", "var", "dz", "sigma", "h" ("thr:0.25" / "hmax:600"), "steps", "W", "out"}. Prints PROGRESS per finished setting
and MATRIX_OK when every setting passed its checks (balance, negative control)."""
import sys, json, os, traceback
from multiprocessing import Pool
os.environ['CENSUS_QUIET'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def one(cfg):
    import census
    try:
        method, hv = cfg['h'].split(':')
        res, ok = census.run_config(cfg['data'], cfg['run'], cfg['var'], cfg['dz'], cfg['sigma'], float(hv), cfg['steps'], cfg['W'],
                                    cfg['out'], cfg.get('nframes'), method)
        return cfg['out'], ok, None
    except Exception:
        return cfg['out'], False, traceback.format_exc()

if __name__ == '__main__':
    cfgs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
    nw = int(sys.argv[2]); good = 0
    import io, contextlib
    with Pool(nw) as p:
        for i, (out, ok, err) in enumerate(p.imap_unordered(one, cfgs)):
            good += ok
            print(f'PROGRESS {(i + 1) / len(cfgs):.4f} {os.path.basename(out)} {"ok" if ok else "FAIL"}', flush=True)
            if err: print(err, flush=True)
    print('MATRIX_OK' if good == len(cfgs) else f'MATRIX_FAIL {len(cfgs) - good} settings', flush=True)
