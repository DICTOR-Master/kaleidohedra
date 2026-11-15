"""Fetch a Himawari-9 Japan-area time series from NOAA's open-data mirror (https://noaa-himawari9.s3.amazonaws.com, no login;
data JMA, distributed by NOAA under the Open Data Dissemination programme), crop a region, average down, store float32 albedo.

Japan-area files: one 10-minute folder holds four 2.5-minute observations JP01..JP04.
Usage: fetch.py OUTDIR YYYYMMDD HHMM_START HHMM_END CADENCE_MIN BAND RES r0 r1 c0 c1 DOWN
  BAND e.g. B03 with RES R05 (0.5 km); rows/cols in the file grid; DOWN = block-average factor.
Writes OUTDIR/frames.npy (T x H x W float32 albedo, nan = no data), times.npy (minutes from START), meta.json. Raw files deleted."""
import sys, os, json, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, hsd

out, day, hs, he, cad, band, res = sys.argv[1:8]
r0, r1, c0, c1, down = map(int, sys.argv[8:13])
cad = float(cad)
os.makedirs(out, exist_ok=True)
t0 = dt.datetime.strptime(day + hs, '%Y%m%d%H%M'); t1 = dt.datetime.strptime(day + he, '%Y%m%d%H%M')
if t1 <= t0: t1 += dt.timedelta(days=1)
times = []
t = t0
while t <= t1:
    times.append(t); t += dt.timedelta(minutes=cad)


def url(t):
    base = t - dt.timedelta(minutes=t.minute % 10, seconds=t.second)
    slot = 1 + int(round(((t - base).total_seconds() / 60) / 2.5))
    name = f'HS_H09_{base:%Y%m%d_%H%M}_{band}_JP{slot:02d}_{res}_S0101.DAT.bz2'
    return f'https://noaa-himawari9.s3.amazonaws.com/AHI-L1b-Japan/{base:%Y/%m/%d/%H%M}/{name}', name


def get(k):
    u, name = url(times[k]); p = os.path.join(out, name)
    for _ in range(3):
        try:
            urllib.request.urlretrieve(u, p); break
        except Exception as e:
            err = e
    else:
        return k, None, str(err)
    h = hsd.read(p)
    a = hsd.calibrated(h)[r0:r1, c0:c1]
    H, W = (a.shape[0] // down) * down, (a.shape[1] // down) * down
    a = a[:H, :W].reshape(H // down, down, W // down, down).mean(axis=(1, 3)).astype(np.float32)
    lat, lon = hsd.latlon(h, np.array([h['first_line'] + r0, h['first_line'] + r1]), np.array([1 + c0, 1 + c1]))
    os.remove(p)
    return k, a, (float(lat[0]), float(lon[0]), float(lat[1]), float(lon[1]), float(h['mjd']))


frames = [None] * len(times); meta_c = None; missing = []
with ThreadPoolExecutor(8) as ex:
    for i, (k, a, info) in enumerate(ex.map(get, range(len(times)))):
        if a is None: missing.append((k, info)); continue
        frames[k] = a; meta_c = info
        print(f'PROGRESS {(i + 1) / len(times):.3f} fetched {times[k]:%H:%M}', flush=True)
keep = [k for k in range(len(times)) if frames[k] is not None]
np.save(os.path.join(out, 'frames.npy'), np.stack([frames[k] for k in keep]))
np.save(os.path.join(out, 'times.npy'), np.array([(times[k] - t0).total_seconds() / 60 for k in keep]))
json.dump(dict(day=day, start=hs, end=he, cadence_min=cad, band=band, res=res, rows=[r0, r1], cols=[c0, c1], down=down,
               corner_latlon=meta_c[:4] if meta_c else None, frames=len(keep), missing=[(times[k].isoformat(), e) for k, e in missing],
               source='NOAA open-data mirror of JMA Himawari-9 HSD, AHI-L1b-Japan'), open(os.path.join(out, 'meta.json'), 'w'), indent=1)
print('FETCH_OK' if keep and not missing else f'FETCH_PARTIAL missing {len(missing)}', len(keep), 'frames', flush=True)
