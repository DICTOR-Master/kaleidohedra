# Driver: builds scene specs from camera fits + look settings and renders with Blender.
# Usage (dicto-big-brother, in the work dir): ~/geom/bin/python run.py look.json view... (view = 1|2|3|clean|open|htile)
# look.json: {samples, res, ring{}, wood{}, world{}, exposure, light{...}, views{"1": {light{}, cam, obj}}, ...}
import json, sys, subprocess, os, copy
HERE = os.path.dirname(os.path.abspath(__file__))
look = json.load(open(sys.argv[1])); outdir = look.get('outdir', 'renders'); os.makedirs(outdir, exist_ok=True)
for v in sys.argv[2:]:
    V = look['views'][v]; spec = copy.deepcopy({k: x for k, x in look.items() if k != 'views'})
    cam = json.load(open(V['cam'])); spec.update(M_obj=cam['M_obj'], cam=cam['cam'], lens_mm=cam['lens_mm'])
    for k in ('light', 'world', 'wood', 'ring'):
        if k in V: spec[k] = {**spec.get(k, {}), **V[k]}
    for k in ('obj', 'exposure', 'res', 'samples', 'cam_override', 'M_override'):
        if k in V: spec[k] = V[k]
    if 'cam_override' in spec: spec['cam'] = spec['cam_override']
    if 'M_override' in spec: spec['M_obj'] = spec['M_override']
    spec['out'] = os.path.abspath(os.path.join(outdir, f'render-{v}.png'))
    sp = os.path.join(outdir, f'spec-{v}.json'); json.dump(spec, open(sp, 'w'))
    r = subprocess.run(['blender', '-b', '-P', os.path.join(HERE, 'scene.py'), '--', sp], capture_output=True, text=True)
    print(v, 'ok' if 'RENDERED' in r.stdout else r.stdout[-2000:] + r.stderr[-2000:])
