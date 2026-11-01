# Star Cores book: the dataset facts for every card (DICTO Solids v7): name, D-number, symmetry, f-vector, faces by sides, volume,
# number field, paper and the inventory note. Usage: meta.py <dataset-v7 dir> <out json>
import json, csv, os, sys
DS, OUT = sys.argv[1:3]
rows = {r['dataset_file']: r for r in csv.DictReader(l for l in open(os.path.join(DS, 'index.csv'), encoding='utf8') if not l.startswith('#'))}
out = {}
for fn in sorted(os.listdir(os.path.join(DS, 'solids'))):
    if not fn.endswith('.json'): continue
    d = json.load(open(os.path.join(DS, 'solids', fn), encoding='utf8')); r = rows.get('solids/' + fn, {})
    vol = d.get('volume'); 
    out[fn[:-5]] = dict(name=d.get('name'), D=r.get('universal_number'), symmetry=(d.get('symmetry') or {}).get('schoenflies'),
        order=(d.get('symmetry') or {}).get('order'), f_vector=d.get('f_vector'), faces_by_sides=d.get('faces_by_sides'), volume=vol,
        field=d.get('field'), convex=d.get('convex', (d.get('checks') or {}).get('convex')), paper=r.get('paper'), doi=r.get('dicto_doi'),
        status=r.get('status'), note=r.get('prior_art_or_note'), sq_edges=d.get('squared_edge_lengths'))
json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False, default=str); print(len(out))
