import sys, json, re, pikepdf
from collections import Counter
PATHOPS = {'m','l','c','v','y','h','re'}
PAINT = {'f','F','f*','S','s','B','B*','b','b*','n'}
def analyse(fn):
    pdf = pikepdf.open(fn)
    out = {'file': fn.split('/')[-1], 'pages': []}
    seen_img = {}
    def walk_xobj(res, depth=0):
        ops = Counter(); imgs = []; nbytes = 0
        if res is None or '/XObject' not in res: return ops, imgs, nbytes
        for name, xo in res.XObject.items():
            st = xo.Subtype
            if st == '/Image':
                key = xo.objgen
                imgs.append(dict(w=int(xo.Width), h=int(xo.Height), filt=str(xo.get('/Filter')), bytes=len(xo.read_raw_bytes()), smask='/SMask' in xo, obj=key))
            elif st == '/Form' and depth < 6:
                try:
                    for operands, op in pikepdf.parse_content_stream(xo):
                        ops[str(op)] += 1
                    nbytes += len(xo.read_bytes())
                except Exception as e: ops['ERR'] += 1
                o2, i2, b2 = walk_xobj(xo.get('/Resources'), depth+1)
                ops += o2; imgs += i2; nbytes += b2
        return ops, imgs, nbytes
    for i, pg in enumerate(pdf.pages):
        ops = Counter(); nbytes = 0
        for operands, op in pikepdf.parse_content_stream(pg):
            ops[str(op)] += 1
        for c in ([pg.Contents] if isinstance(pg.Contents, pikepdf.Stream) else list(pg.Contents)):
            nbytes += len(c.read_bytes())
        o2, imgs, b2 = walk_xobj(pg.Resources)
        ops += o2; nbytes += b2
        # also shading / pattern count
        out['pages'].append(dict(page=i+1, path_ops=sum(ops[o] for o in PATHOPS), paint_ops=sum(ops[o] for o in PAINT),
            total_ops=sum(ops.values()), content_bytes=nbytes, images=[{k:v for k,v in d.items() if k!='obj'} for d in imgs],
            img_bytes=sum(d['bytes'] for d in imgs)))
    # per-object size totals
    tot = Counter()
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream):
            t = str(obj.get('/Subtype', obj.get('/Type', 'other')))
            tot[t] += len(obj.read_raw_bytes())
    out['stream_bytes_by_type'] = dict(tot)
    return out
res = [analyse(f) for f in sys.argv[1:]]
json.dump(res, open('analysis.json','w'), indent=1)
for r in res:
    print('==', r['file'], 'streams by type:', {k: round(v/1e6,2) for k,v in r['stream_bytes_by_type'].items()})
    print(' page pathops paintops contentMB nimg imgMB maxImg(px)')
    for p in r['pages']:
        mx = max([(d['w'],d['h']) for d in p['images']], default=None, key=lambda t: t[0]*t[1] if t else 0)
        print(f" {p['page']:3d} {p['path_ops']:8d} {p['paint_ops']:7d} {p['content_bytes']/1e6:8.2f} {len(p['images']):3d} {p['img_bytes']/1e6:6.2f} {mx}")
