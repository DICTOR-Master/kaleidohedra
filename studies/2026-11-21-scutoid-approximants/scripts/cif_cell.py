"""Scutoid approximants study (21 Nov 2026), step 1: read a CIF, expand the asymmetric unit with the CIF's own symmetry operators
(plus centring as listed there), merge coincident sites, write the full cubic cell in Angstrom.
No crystallography library: a small loop parser (values with standard uncertainties "0.123(4)" -> 0.123).
Sites with mixed occupancy at one position are merged into one site (species string joined, occupancies added);
split positions closer than SPLIT Angstrom are merged into the one of highest occupancy (the alternative positions are kept in 'alts').
Usage: python -I cif_cell.py CIF OUT.json"""
import sys, re, json, itertools
import numpy as np

SPLIT = 0.75

def tokens(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith('#'): continue
        if s.startswith(';'): out.append(('SEMI', s)); continue
        for m in re.finditer(r"'[^']*'(?=\s|$)|\"[^\"]*\"(?=\s|$)|\S+", s):
            t = m.group(0)
            if t[0] in "'\"": t = t[1:-1]
            out.append(('T', t))
    return out

def parse(text):
    """returns dict tag->value and list of loops (tags, rows)"""
    tk = tokens(text); tags, loops, i, insemi = {}, [], 0, False
    clean = []
    for kind, t in tk:                       # drop semicolon text fields
        if kind == 'SEMI': insemi = not insemi; continue
        if not insemi: clean.append(t)
    i = 0
    while i < len(clean):
        t = clean[i]
        if t.lower() == 'loop_':
            i += 1; lt = []
            while i < len(clean) and clean[i].startswith('_'): lt.append(clean[i].lower()); i += 1
            vals = []
            while i < len(clean) and not clean[i].startswith('_') and clean[i].lower() != 'loop_' and not clean[i].lower().startswith('data_'):
                vals.append(clean[i]); i += 1
            rows = [vals[k:k+len(lt)] for k in range(0, len(vals) - len(vals) % len(lt), len(lt))]
            loops.append((lt, rows))
        elif t.startswith('_'):
            tags[t.lower()] = clean[i+1] if i + 1 < len(clean) else None; i += 2
        else: i += 1
    return tags, loops

def num(s):
    s = re.sub(r'\(\d+\)', '', s)
    return float(s) if s not in ('.', '?') else None

def op(expr):
    expr = expr.replace(' ', '').lower()
    R = np.zeros(3); t = 0.0
    M = np.zeros((3, 3)); T = np.zeros(3)
    for r, part in enumerate(expr.split(',')):
        for m in re.finditer(r'([+-]?)(\d+/\d+|\d*\.?\d+)?([xyz])?', part):
            sg, c, v = m.groups()
            if not (c or v): continue
            f = -1.0 if sg == '-' else 1.0
            if v:
                M[r, 'xyz'.index(v)] += f * (eval(c) if c else 1.0)
            else:
                T[r] += f * eval(c)
    return M, T

def main(cif, out):
    tags, loops = parse(open(cif, encoding='utf-8', errors='replace').read())
    a = num(tags['_cell_length_a'])
    assert abs(num(tags['_cell_length_b']) - a) < 1e-6 and abs(num(tags['_cell_length_c']) - a) < 1e-6, "cubic"
    sg = tags.get('_symmetry_space_group_name_h-m') or tags.get('_space_group_name_h-m_alt')
    ops = None
    for lt, rows in loops:
        for name in ('_symmetry_equiv_pos_as_xyz', '_space_group_symop_operation_xyz'):
            if name in lt: ops = [op(r[lt.index(name)]) for r in rows]
    assert ops, "symmetry operators"
    sites = None
    for lt, rows in loops:
        if '_atom_site_fract_x' in lt: sites = (lt, rows)
    lt, rows = sites
    ix = {k: lt.index(k) for k in lt}
    asym = []
    for r in rows:
        lab = r[ix['_atom_site_label']]
        typ = r[ix['_atom_site_type_symbol']] if '_atom_site_type_symbol' in ix else re.match(r'[A-Z][a-z]?', lab).group(0)
        typ = re.match(r'[A-Z][a-z]?', typ).group(0)
        occ = num(r[ix['_atom_site_occupancy']]) if '_atom_site_occupancy' in ix else 1.0
        x = np.array([num(r[ix[k]]) for k in ('_atom_site_fract_x', '_atom_site_fract_y', '_atom_site_fract_z')])
        asym.append((lab, typ, 1.0 if occ is None else occ, x))
    # merge mixed-occupancy sites at the same position in the asymmetric unit
    merged = []
    for lab, typ, occ, x in asym:
        for m in merged:
            if np.allclose(m['x'], x, atol=1e-5):
                m['label'] += '/' + lab; m['species'][typ] = m['species'].get(typ, 0) + occ; m['occ'] += occ; break
        else:
            merged.append(dict(label=lab, x=x, species={typ: occ}, occ=occ))
    atoms = []
    for m in merged:
        orb = []
        for M, T in ops:
            y = (M @ m['x'] + T) % 1.0
            y[np.isclose(y, 1.0, atol=1e-6)] = 0.0
            if not any(np.linalg.norm(((y - z + 0.5) % 1.0 - 0.5) * a) < 0.05 for z in orb): orb.append(y)
        for y in orb: atoms.append(dict(label=m['label'], species=m['species'], occ=round(m['occ'], 4), frac=y.tolist(), mult=len(orb)))
    # split positions: keep highest occupancy within SPLIT Angstrom
    order = sorted(range(len(atoms)), key=lambda i: -atoms[i]['occ'])
    keep, alts = [], {}
    for i in order:
        fi = np.array(atoms[i]['frac'])
        for k in keep:
            d = np.linalg.norm(((fi - np.array(atoms[k]['frac']) + 0.5) % 1.0 - 0.5) * a)
            if d < SPLIT:
                alts.setdefault(k, []).append(dict(label=atoms[i]['label'], occ=atoms[i]['occ'], d=round(float(d), 3))); break
        else: keep.append(i)
    cell = []
    for k in keep:
        A = dict(atoms[k]); A['alts'] = alts.get(k, []); A['cart'] = (np.array(A['frac']) * a).tolist(); cell.append(A)
    res = dict(cif=cif.split('/')[-1], a=a, space_group=sg, n_ops=len(ops), n_sites_asym=len(merged), n_atoms_full=len(atoms),
               n_atoms_kept=len(cell), split_merge_A=SPLIT, journal=tags.get('_journal_name_full'), year=tags.get('_journal_year'),
               doi=tags.get('_journal_paper_doi'), formula=tags.get('_chemical_formula_sum'), atoms=cell)
    json.dump(res, open(out, 'w'), indent=0)
    print(f"{res['cif']}: a = {a} A, {sg}, {len(ops)} ops, {len(merged)} sites, {len(atoms)} atoms in cell, {len(cell)} after merging split positions < {SPLIT} A")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
