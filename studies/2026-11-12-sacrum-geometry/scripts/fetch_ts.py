#!/usr/bin/env python3
"""DICTO · dictospheres.com — sacrum study (12 Nov 2026).
Fetch only the needed segmentation masks from the TotalSegmentator small dataset (Wasserthal et al. 2023, Zenodo record 10047263,
CC BY 4.0) by HTTP range requests into the zip (no 3.2 GB download). For each subject: sacrum, vertebrae_L5, vertebrae_L4, hip_left,
hip_right (.nii.gz) + the dataset's meta.csv. Each file is CRC-checked by zipfile on read and its SHA256 written to provenance.tsv.
Usage: python3 -I fetch_ts.py OUTDIR MAXSUBJECTS
"""
import sys, os, io, zipfile, hashlib, urllib.request, json, time, socket
sys.stdout.reconfigure(line_buffering=True)   # python -I ignores PYTHONUNBUFFERED; PROGRESS lines must reach the log live

# the compute host's IPv6 route to Zenodo hangs (SYN-SENT seen 12 Nov); use IPv4 only
_gai = socket.getaddrinfo
socket.getaddrinfo = lambda host, port, family=0, *a, **k: _gai(host, port, socket.AF_INET, *a, **k)

URL = 'https://zenodo.org/records/10047263/files/Totalsegmentator_dataset_small_v201.zip?download=1'
WANT = ['sacrum', 'vertebrae_L5', 'vertebrae_L4', 'hip_left', 'hip_right']


class HTTPRange(io.RawIOBase):
    def __init__(self, url):
        self.url, self.pos = url, 0
        req = urllib.request.Request(url, headers={'Range': 'bytes=0-0', 'User-Agent': 'research-fetch'})
        with urllib.request.urlopen(req, timeout=30) as r:
            self.size = int(r.headers['Content-Range'].split('/')[-1])
        self.nreq = 0

    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off)
        return self.pos

    def read(self, n=-1):
        if n is None or n < 0: n = self.size - self.pos
        if n == 0 or self.pos >= self.size: return b''
        end = min(self.size, self.pos + n) - 1
        for attempt in range(5):
            try:
                req = urllib.request.Request(self.url, headers={'Range': f'bytes={self.pos}-{end}', 'User-Agent': 'research-fetch'})
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
                break
            except Exception as e:
                print('retry', attempt, e); time.sleep(5 * (attempt + 1))
        else:
            raise IOError('range read failed')
        self.nreq += 1
        self.pos += len(data)
        return data

    def readinto(self, b):
        d = self.read(len(b)); b[:len(d)] = d; return len(d)


def main():
    out, maxs = sys.argv[1], int(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    f = io.BufferedReader(HTTPRange(URL), buffer_size=1 << 20)
    z = zipfile.ZipFile(f)
    names = z.namelist()
    subj = sorted({n.split('/')[-3] for n in names if n.endswith('/segmentations/sacrum.nii.gz')})
    print(f'zip entries {len(names)}, subjects with a sacrum file {len(subj)}')
    prov = open(os.path.join(out, 'provenance.tsv'), 'w')
    prov.write('# source\t' + URL + '\n# licence\tCC BY 4.0 (Wasserthal J. et al., TotalSegmentator, Radiology: AI 2023)\nfile\tbytes\tsha256\tzip_crc32\n')
    meta = [n for n in names if n.endswith('meta.csv')]
    for m in meta:
        data = z.read(m); open(os.path.join(out, 'meta.csv'), 'wb').write(data)
        prov.write(f'{m}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}\t{z.getinfo(m).CRC:08x}\n')
    todo = subj[:maxs]
    for i, s in enumerate(todo):
        d = os.path.join(out, s); os.makedirs(d, exist_ok=True)
        for w in WANT:
            cand = [n for n in names if n.endswith(f'{s}/segmentations/{w}.nii.gz')]
            if not cand: continue
            data = z.read(cand[0])  # zipfile verifies the CRC32
            open(os.path.join(d, w + '.nii.gz'), 'wb').write(data)
            prov.write(f'{cand[0]}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}\t{z.getinfo(cand[0]).CRC:08x}\n')
        print(f'PROGRESS {(i + 1) / len(todo):.3f} fetched {s}')
    prov.close()
    ok = all(os.path.exists(os.path.join(out, s, 'sacrum.nii.gz')) for s in todo) and len(todo) > 0
    print(f'fetched {len(todo)} subjects, {f.raw.nreq} range requests')
    print('FETCH ok' if ok else 'FETCH FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
