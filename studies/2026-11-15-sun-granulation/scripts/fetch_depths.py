"""Fetch further horizontal planes of vertical velocity uz from the public Bifrost run, at extra depths below the mean tau = 1 height,
for the depth-traced swap count (README section "Swaps traced through depth", 16 Nov 2026). Same range-request method and the same
file layout as fetch_bifrost.py (which fetched 0, 0.1, 0.2, 0.4 Mm); this adds the depths between them.

Data: Hinode Science Data Centre Europe (sdc.uio.no), public Bifrost simulations. Credit at the point of use:
  Bifrost code: Gudiksen, Carlsson, Hansteen, Hayek, Leenaarts & Martinez-Sykora 2011, A&A 531, A154.
  en024048_hion: Carlsson, Hansteen, Gudiksen, Leenaarts & De Pontieu 2016, A&A 585, A4 (24 x 24 x 17 Mm, 504 x 504 x 496 points,
  48 km horizontal, 19 to 100 km vertical grid, snapshots 303 to 544 every 10 s; 17 variables per snapshot, 504 MB per file).
  The archive asks users to acknowledge the Hinode mission (ISAS/JAXA with NAOJ, NASA, STFC, ESA and NSC).

Usage: fetch_depths.py RUN FIRST LAST OUTDIR DEPTHS(comma, Mm below tau = 1)   writes OUTDIR/RUN_uz_dz<d>.npy and RUN_depths_meta.json"""
import sys, os, json, time, struct, socket, urllib.request
_gai = socket.getaddrinfo                     # the archive's IPv6 route stalls ~30 s per request from our network: use IPv4
socket.getaddrinfo = lambda *a, **k: [r for r in _gai(*a, **k) if r[0] == socket.AF_INET]
import numpy as np
from concurrent.futures import ThreadPoolExecutor

RUN, FIRST, LAST, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
DEPTHS = [float(x) for x in sys.argv[5].split(',')]
BASE = f'https://sdc.uio.no/vol/simulations/{RUN}/atmos/BIFROST_{RUN}_' + '{var}_{snap}.fits'
NX = 504; P = NX * NX * 4
os.makedirs(OUT, exist_ok=True)


def get(url, a, b, tries=6):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={'Range': f'bytes={a}-{b}', 'User-Agent': 'research-client'})
            with urllib.request.urlopen(req, timeout=120) as r: d = r.read()
            if len(d) == b - a + 1: return d
        except Exception:
            pass
        time.sleep(5 * (t + 1))
    raise RuntimeError(f'range fetch failed {url} {a}-{b}')


def header(url):
    h = get(url, 0, 2880 * 6 - 1)
    cards = [h[i:i + 80].decode('ascii', 'replace') for i in range(0, len(h), 80)]
    kv = {}
    for i, c in enumerate(cards):
        if c.startswith('END') and c[3:].strip() == '':
            H = ((i + 1) * 80 + 2879) // 2880 * 2880; break
        if '=' in c[:10]:
            kv[c[:8].strip()] = c[10:].split('/')[0].strip().strip("'").strip()
    return H, kv


snaps = list(range(FIRST, LAST + 1))
u0 = BASE.format(var='uz', snap=snaps[0])
H, kv = header(u0)
NZ = int(kv['NAXIS3'])
size = int(urllib.request.urlopen(urllib.request.Request(u0, method='HEAD'), timeout=60).headers['Content-Length'])
tail = get(u0, size - 8640, size - 1)
i = tail.find(b'XTENSION')
for k in range(i, len(tail), 80):
    if tail[k:k + 80].startswith(b'END') and tail[k + 3:k + 80].strip() == b'':
        e = (k - i + 80 + 2879) // 2880 * 2880; break
z = np.array(struct.unpack(f'>{NZ}f', tail[i + e:i + e + NZ * 4]))
ztau = float(kv.get('ZTAU51', 'nan'))
if not np.isfinite(ztau): ztau = 0.0588955          # as fetch_bifrost.py (qs headers lack ZTAU51)
ks = [int(np.argmin(abs(z - (ztau - d)))) for d in DEPTHS]
meta = dict(run=RUN, first=FIRST, last=LAST, nz=NZ, ztau51=ztau, depths_below_tau1_Mm=DEPTHS, planes=ks,
            z_of_planes=[float(z[k]) for k in ks], file_bytes=size, z_grid_near_surface_Mm=[float(x) for x in z[55:90]], source=BASE)
print('META', json.dumps({k: v for k, v in meta.items() if k != 'z_grid_near_surface_Mm'}), flush=True)
arrs = {d: np.lib.format.open_memmap(f'{OUT}/{RUN}_uz_dz{d}.npy', mode='w+', dtype=np.float32, shape=(len(snaps), NX, NX)) for d in DEPTHS}
with ThreadPoolExecutor(8) as ex:
    hdr = dict(zip(snaps, ex.map(lambda s: header(BASE.format(var='uz', snap=s))[0], snaps)))
print('PROGRESS 0.05 headers read', flush=True)
jobs = [(n, s, d, ks[j]) for n, s in enumerate(snaps) for j, d in enumerate(DEPTHS)]
def plane(job):
    n, s, d, k = job
    raw = get(BASE.format(var='uz', snap=s), hdr[s] + k * P, hdr[s] + (k + 1) * P - 1)
    arrs[d][n] = np.frombuffer(raw, dtype='>f4').reshape(NX, NX).astype(np.float32)
done = 0
with ThreadPoolExecutor(8) as ex:
    for _ in ex.map(plane, jobs):
        done += 1
        if done % (10 * len(DEPTHS)) == 0 or done == len(jobs): print(f'PROGRESS {0.05 + 0.95 * done / len(jobs):.4f} planes {done}/{len(jobs)}', flush=True)
for a in arrs.values(): a.flush()
json.dump(meta, open(f'{OUT}/{RUN}_depths_meta.json', 'w'), indent=1)
ok = done == len(jobs) and all(np.isfinite(a[:]).all() and float(np.abs(a[-1]).max()) > 0 for a in arrs.values())
print('CHECK', {d: float(np.asarray(arrs[d][0]).std()) for d in DEPTHS}, flush=True)
print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
