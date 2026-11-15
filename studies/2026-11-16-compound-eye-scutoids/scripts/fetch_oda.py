#!/usr/bin/env python3
"""Fetch single members of the ODA-3D benchmark zip (Currea et al. 2023, figshare 10.6084/m9.figshare.21521142, CC BY 4.0,
file benchmark_3D_data.zip, 17.1 GB) by HTTP range requests, without downloading the whole zip.
Usage: python3 -I fetch_oda.py OUTDIR MEMBER [MEMBER ...]   (the figshare link is resolved afresh for each call; the signed
storage link expires within seconds, so call once per member). Members used here:
  apis_mellifera/_prefiltered_stack/ommatidial_data.csv, drosophila_mauritiana/_prefiltered_stack/ommatidial_data.csv,
  deilephila_elpenor/_prefiltered_stack/ommatidial_data.csv, manduca_sexta/_prefiltered_stack/ommatidial_data.csv
Check the result against data/raw_sha256.txt."""
import sys, struct, urllib.request, zlib, os
FIG = 'https://ndownloader.figshare.com/files/38181174'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
def signed_url():
    try: urllib.request.build_opener(NoRedirect).open(urllib.request.Request(FIG, method='HEAD'))
    except urllib.error.HTTPError as e: return e.headers['Location']
outdir = sys.argv[1]; want = sys.argv[2:]
for member in want:
    url = signed_url()
    def rng(a,b):
        return urllib.request.urlopen(urllib.request.Request(url,headers={'Range':f'bytes={a}-{b}'})).read()
    h=urllib.request.urlopen(urllib.request.Request(url,headers={'Range':'bytes=0-0'}));size=int(h.headers['Content-Range'].split('/')[1])
    tail=rng(size-200000,size-1);i=tail.rfind(b'PK\x06\x06')
    cd_size,cd_off=struct.unpack('<QQ',tail[i+40:i+56]) if i>=0 else struct.unpack('<II',tail[tail.rfind(b'PK\x05\x06')+12:][:8])
    cd=rng(cd_off,cd_off+cd_size-1);p=0
    while p<len(cd) and cd[p:p+4]==b'PK\x01\x02':
        meth=struct.unpack('<H',cd[p+10:p+12])[0];csz,usz=struct.unpack('<II',cd[p+20:p+28]);n,e,c=struct.unpack('<HHH',cd[p+28:p+34]);off=struct.unpack('<I',cd[p+42:p+46])[0]
        name=cd[p+46:p+46+n].decode();ex=cd[p+46+n:p+46+n+e];q=0
        while q<len(ex):
            hid,hl=struct.unpack('<HH',ex[q:q+4])
            if hid==1:
                v=list(struct.unpack('<'+'Q'*(hl//8),ex[q+4:q+4+8*(hl//8)]))
                if usz==0xffffffff: usz=v.pop(0)
                if csz==0xffffffff: csz=v.pop(0)
                if off==0xffffffff: off=v.pop(0)
            q+=4+hl
        if name == member:
            lh=rng(off,off+29);ln,le=struct.unpack('<HH',lh[26:30]);d=rng(off+30+ln+le,off+30+ln+le+csz-1)
            d=zlib.decompress(d,-15) if meth==8 else d
            fn=os.path.join(outdir,name.replace('/','__').replace(' ','_'));open(fn,'wb').write(d);print(fn,len(d))
        p+=46+n+e+c
