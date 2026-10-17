# DICTO 2026-10-18 octet study -- STEP 18: DICTO chose Fable's improvement 1, drop the keys in the full kit. Re-run the step-14 fit of
# the three Penrose prisms with no keys: are the flanking prisms now clear (they failed only on keys), and inside the hull? -> data/step18-fit.json
import json
src = open('step14_penrose_fit.py').read()
src = src.replace("keys = [(E, np.zeros(3)) for E in keys] + [(E, o) for E in keys]", "keys = []   # step 18: no keys")
src = src.replace("save('step14-fit.json', dict(mark=MARK, step=14, status='float sampling', fit=out))", "save('step18-fit.json', dict(mark=MARK, step=18, status='float sampling, no keys', fit=out))")
exec(compile(src, 'step14_penrose_fit.py (no keys)', 'exec'))
