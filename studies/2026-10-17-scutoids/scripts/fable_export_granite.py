# DICTO 2026-10-17 night: "I want the normal vertical ones in red granite." Exports Fable's 8-piece flat scutoid group (fable_render.cell3d,
# float) as face polygons plus the layer's repeat vectors, for render_granite.html. -> data/fable-group-geometry.json
import sys, json, numpy as np
H = json.load(open('data/fable-group-pieces.json'))['H']
sys.argv = ['fable_render.py', 'data/fable-group-params.json', '/tmp/unused', str(H)]
sys.path.insert(0, 'scripts')
src = open('scripts/fable_render.py').read().split("\nif __name__ == '__main__':")[0]
exec(src)
cells = [cell3d(*g, H) for g in grp]
out = dict(mark='DICTO · dictospheres.com', H=H, L=[list(map(float, L[0])) + [0.0], list(map(float, L[1])) + [0.0]],
           pieces=[dict(num=NUM[g[0]], psi=round(C['psi'], 4), faces=[F.tolist() for _, F in C['faces']]) for g, C in zip(grp, cells)])
json.dump(out, open('data/fable-group-geometry.json', 'w'))
print('pieces', len(cells), 'H', H, 'volume', sum(C['vol'] for C in cells), 'period', abs(np.linalg.det(L)) * H)
