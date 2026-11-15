"""Fetch horizontal planes of public Bifrost radiative-MHD snapshots by HTTP range requests (only the planes needed, not the cubes).

Data: Hinode Science Data Centre Europe (sdc.uio.no), public Bifrost simulations. Credit at the point of use:
  Bifrost code: Gudiksen, Carlsson, Hansteen, Hayek, Leenaarts & Martinez-Sykora 2011, A&A 531, A154.
  en024048_hion public run: Carlsson, Hansteen, Gudiksen, Leenaarts & De Pontieu 2016, A&A 585, A4 (enhanced network, 24 x 24 Mm,
  48 km horizontal grid, periodic in x and y, snapshots every 10 s).
  qs024048_by3363: quiet-Sun run on the same grid, listed by the same archive.
Each FITS file is one variable of one snapshot: 504 x 504 x 496 float32 big-endian (x fastest), a z-coordinate extension at the end.
A plane k is the contiguous byte range [H + k*P, H + (k+1)*P) with P = 504*504*4 and H the main header length (read from the file).

Usage: fetch_bifrost.py RUN FIRST LAST OUTDIR [STRIDE]   (writes OUTDIR/RUN_<var>_dz<depth>.npy of shape (nt, 504, 504), times.npy, meta.json)
Planes: uz at the mean height of tau(500 nm) = 1 (header ZTAU51) and 0.1, 0.2, 0.4 Mm below it; lg(T) at the top two."""
import sys, os, json, time, struct, socket, urllib.request
_gai = socket.getaddrinfo                     # the archive's IPv6 route stalls ~30 s per request from our network: use IPv4
socket.getaddrinfo = lambda *a, **k: [r for r in _gai(*a, **k) if r[0] == socket.AF_INET]
import numpy as np

RUN, FIRST, LAST, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
STRIDE = int(sys.argv[5]) if len(sys.argv) > 5 else 1
BASE = f'https://sdc.uio.no/vol/simulations/{RUN}/atmos/BIFROST_{RUN}_' + '{var}_{snap}.fits'
VARS = ['lgtg', 'uz']
DEPTHS = [0.0, 0.1, 0.2, 0.4]          # Mm below the mean tau = 1 height
NX = 504; P = NX * NX * 4
os.makedirs(OUT, exist_ok=True)


def get(url, a, b, tries=6):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={'Range': f'bytes={a}-{b}', 'User-Agent': 'research-client'})
            with urllib.request.urlopen(req, timeout=120) as r: d = r.read()
            if len(d) == b - a + 1: return d
        except Exception as e:
            err = e
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
            k, v = c[:8].strip(), c[10:].split('/')[0].strip().strip("'").strip()
            kv[k] = v
    return H, kv


snaps = list(range(FIRST, LAST + 1, STRIDE))
u0 = BASE.format(var='lgtg', snap=snaps[0])
H, kv = header(u0)
assert int(kv['NAXIS1']) == NX and int(kv['NAXIS2']) == NX, kv
NZ = int(kv['NAXIS3'])
size = int(urllib.request.urlopen(urllib.request.Request(u0, method='HEAD'), timeout=60).headers['Content-Length'])
tail = get(u0, size - 8640, size - 1)
i = tail.find(b'XTENSION')
for k in range(i, len(tail), 80):
    if tail[k:k + 80].startswith(b'END') and tail[k + 3:k + 80].strip() == b'':
        e = (k - i + 80 + 2879) // 2880 * 2880; break
z = np.array(struct.unpack(f'>{NZ}f', tail[i + e:i + e + NZ * 4]))
assert H + NZ * P <= size - 2880, (H, NZ, size)
ztau = float(kv.get('ZTAU51', 'nan'))
ztau_note = 'header ZTAU51'
if not np.isfinite(ztau):                      # qs024048_by3363 headers carry no ZTAU51: use the en024048_hion value (same code, same
    ztau, ztau_note = 0.0588955, 'ZTAU51 absent; en024048_hion value used, checked by the mean temperature of the plane'
# z increases upward in these files (corona at the top end); below the surface = smaller z
ks = [int(np.argmin(abs(z - (ztau - d)))) for d in DEPTHS]
meta = dict(run=RUN, first=FIRST, last=LAST, stride=STRIDE, header_bytes=H, nz=NZ, ztau51=ztau, depths_below_tau1_Mm=DEPTHS,
            planes=ks, z_of_planes=[float(z[k]) for k in ks], dx_Mm=float(kv['CDELT1']), dtsnap_s=float(kv['DTSNAP']) * 100,
            source=BASE, ztau_note=ztau_note)
print('META', json.dumps(meta), flush=True)
PLANES = [(v, d) for v in VARS for d in DEPTHS if v == 'uz' or d in (0.0, 0.1)]     # uz at all depths, lg T at the top two
arrs = {(v, d): np.lib.format.open_memmap(f'{OUT}/{RUN}_{v}_dz{d}.npy', mode='w+', dtype=np.float32, shape=(len(snaps), NX, NX))
        for v, d in PLANES}
from concurrent.futures import ThreadPoolExecutor
# the archive serves about 0.35 MB/s per connection; 8 connections in parallel
with ThreadPoolExecutor(8) as ex:
    hdrs = dict(zip([(s, v) for s in snaps for v in VARS], ex.map(lambda sv: header(BASE.format(var=sv[1], snap=sv[0])),
                                                                   [(s, v) for s in snaps for v in VARS])))
times = [float(hdrs[(s, 'lgtg')][1]['ELAPSED']) for s in snaps]
for (s, v), (Hs, kvs) in hdrs.items():
    assert int(kvs['NAXIS3']) == NZ and int(kvs['NAXIS1']) == NX
print('PROGRESS 0.05 headers read', flush=True)
jobs = [(n, s, v, d, ks[DEPTHS.index(d)]) for n, s in enumerate(snaps) for v, d in PLANES]
def plane(job):
    n, s, v, d, k = job
    Hs = hdrs[(s, v)][0]
    raw = get(BASE.format(var=v, snap=s), Hs + k * P, Hs + (k + 1) * P - 1)
    arrs[(v, d)][n] = np.frombuffer(raw, dtype='>f4').reshape(NX, NX).astype(np.float32)
    return n
done = 0
with ThreadPoolExecutor(8) as ex:
    for n in ex.map(plane, jobs):
        done += 1
        if done % len(PLANES) == 0: print(f'PROGRESS {0.05 + 0.95 * done / len(jobs):.4f} planes {done}/{len(jobs)}', flush=True)
for a in arrs.values(): a.flush()
np.save(f'{OUT}/{RUN}_times.npy', np.array(times))
meta['times_first_last'] = [times[0], times[-1]]; meta['n'] = len(times)
json.dump(meta, open(f'{OUT}/{RUN}_meta.json', 'w'), indent=1)
dt = np.diff(times)
ok = len(times) == len(snaps) and np.all(dt > 0) and all(np.isfinite(a[:]).all() for a in arrs.values())
T0 = 10 ** np.asarray(arrs[('lgtg', 0.0)][0], dtype=float)
print('CHECK cadence', dt.min(), dt.max(), 'finite', ok, 'mean T at the tau=1 plane', T0.mean(), flush=True)
meta['meanT_tau1_plane_first'] = float(T0.mean()); json.dump(meta, open(f'{OUT}/{RUN}_meta.json', 'w'), indent=1)
print('FETCH_OK' if ok else 'FETCH_FAIL', flush=True)
