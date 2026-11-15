"""Minimal reader for Himawari Standard Data (HSD) files, as published by JMA and mirrored by NOAA on AWS open data
(s3://noaa-himawari9, no login). Format: JMA, "Himawari Standard Data User's Guide" v1.3 (2017), free from the JMA
Meteorological Satellite Center. Written for this study from the guide; no code copied from other readers.

Only what the study needs: the image counts (uint16), the calibration (count -> radiance; for visible bands also radiance ->
albedo), and the fixed-grid navigation (line/column -> latitude/longitude, CGMS LRIT/HRIT normalized geostationary projection).

Usage as a script: hsd.py FILE.DAT[.bz2] -> prints shape, band, time, corner lat/lon."""
import bz2, sys, struct
import numpy as np


def _open(path):
    with (bz2.open(path, 'rb') if path.endswith('.bz2') else open(path, 'rb')) as f:
        return f.read()


def read(path):
    b = _open(path)
    off = 0; blocks = {}
    # block 1 gives the total header length; blocks are [number u1][length u2][...]
    while True:
        num = b[off]; ln = struct.unpack_from('<H', b, off + 1)[0]
        blocks[num] = b[off:off + ln]; off += ln
        if num == 11: break
    b1, b2, b3, b5 = blocks[1], blocks[2], blocks[3], blocks[5]
    t_start = struct.unpack_from('<d', b1, 46)[0]           # MJD
    hdr_len = struct.unpack_from('<I', b1, 70)[0]
    ncol, nlin = struct.unpack_from('<HH', b2, 5)
    sub_lon = struct.unpack_from('<d', b3, 3)[0]
    cfac, lfac = struct.unpack_from('<II', b3, 11)
    coff, loff = struct.unpack_from('<ff', b3, 19)
    band = struct.unpack_from('<H', b5, 3)[0]
    wl = struct.unpack_from('<d', b5, 5)[0]
    err_count, out_count = struct.unpack_from('<HH', b5, 15)
    gain, const = struct.unpack_from('<dd', b5, 19)
    b7 = blocks[7]
    seg_first_line = struct.unpack_from('<H', b7, 5)[0]
    alb = None
    if band <= 6:
        alb = struct.unpack_from('<d', b5, 35)[0]            # radiance -> albedo coefficient (c')
    cnt = np.frombuffer(b, dtype='<u2', count=ncol * nlin, offset=hdr_len).reshape(nlin, ncol)
    return dict(counts=cnt, band=band, wavelength_um=wl, err=err_count, out=out_count, gain=gain, const=const, albedo_coef=alb,
                mjd=t_start, sub_lon=sub_lon, cfac=cfac, lfac=lfac, coff=coff, loff=loff, first_line=seg_first_line,
                ncol=ncol, nlin=nlin)


def calibrated(h):
    c = h['counts'].astype(np.float64)
    bad = (h['counts'] == h['err']) | (h['counts'] == h['out'])
    r = h['gain'] * c + h['const']
    if h['albedo_coef'] is not None: r = r * h['albedo_coef']
    r[bad] = np.nan
    return r


def latlon(h, lines, cols):
    """lines, cols: 1-based image line/column numbers (as in the guide). Returns lat, lon in degrees (nan off the disc)."""
    lines = np.asarray(lines, float); cols = np.asarray(cols, float)
    x = np.deg2rad((cols - h['coff']) / (h['cfac'] / 2 ** 16))
    y = np.deg2rad((lines - h['loff']) / (h['lfac'] / 2 ** 16))
    req, rpol, H = 6378.1370, 6356.7523, 42164.0
    a = np.sin(x) ** 2 + np.cos(x) ** 2 * (np.cos(y) ** 2 + (req / rpol) ** 2 * np.sin(y) ** 2)
    bq = H * np.cos(x) * np.cos(y)
    disc = bq ** 2 - a * (H ** 2 - req ** 2)
    with np.errstate(invalid='ignore'):
        sd = np.sqrt(disc)
    sn = (bq - sd) / a
    s1 = H - sn * np.cos(x) * np.cos(y); s2 = sn * np.sin(x) * np.cos(y); s3 = -sn * np.sin(y)
    sxy = np.hypot(s1, s2)
    lat = np.rad2deg(np.arctan((req / rpol) ** 2 * s3 / sxy))
    lon = np.rad2deg(np.arctan2(s2, s1)) + h['sub_lon']
    return lat, lon


if __name__ == '__main__':
    h = read(sys.argv[1])
    print('band', h['band'], 'wl', round(h['wavelength_um'], 3), 'shape', h['counts'].shape, 'first_line', h['first_line'],
          'mjd', h['mjd'], 'albedo_coef', h['albedo_coef'])
    L0 = h['first_line']
    for (l, c) in ((L0, 1), (L0, h['ncol']), (L0 + h['nlin'] - 1, 1), (L0 + h['nlin'] - 1, h['ncol'])):
        print('corner line', l, 'col', c, 'latlon', [round(float(v), 3) for v in latlon(h, l, c)])
