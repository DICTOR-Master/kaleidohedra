"""Loaders for the two stored-decimal yantras (shared by calibrate.py's data and chapati_cross.py)."""
import os, json, re
from fractions import Fraction as Fr


def gf1(ST):
    g = json.load(open(os.path.join(ST, 'data', 'input', 'golden_family.json')))['GF1']
    f = lambda z: Fr(z['a']) if isinstance(z, dict) else Fr(z)
    return [(f(g['b'][str(i)]), f(g['w'][str(i)]), f(g['apex'][str(i)])) for i in range(1, 10)]


def kulaichev(ST):
    txt = open(os.path.join(ST, 'data', 'input', 'kulaichev-numeric-data.txt')).read()
    b = {int(m.group(1)): Fr(m.group(2)) for m in re.finditer(r"b(\d) = ([0-9.]+)", txt)}
    w = {int(m.group(1)): Fr(m.group(2)) for m in re.finditer(r"w(\d) = ([0-9.]+)", txt)}
    a = {8: b[1], 6: b[2], 9: b[3], 1: b[6], 5: b[7], 4: b[8], 2: b[9], 3: Fr(1), 7: Fr(0)}
    return [(b[i], w[i], a[i]) for i in range(1, 10)]
