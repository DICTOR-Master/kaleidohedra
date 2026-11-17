#!/usr/bin/env python3
"""Build the kernel copy of a study module (shape kernel, stage 1 proper): replace the named top-level definitions (classes, functions,
which must stand together) by the text of a shim file; every other line stays byte for byte.  The study file itself is only read.
usage: swap.py <original .py> <output .py> <shim .py> <name> [<name> ...]     prints the replaced line range"""
import ast, sys
src_path, out_path, shim_path, names = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
src = open(src_path, encoding='utf-8').read(); lines = src.splitlines(keepends=True)
tree = ast.parse(src)
top = [n for n in tree.body]
idx = [i for i, n in enumerate(top) if getattr(n, 'name', None) in names]
found = {top[i].name for i in idx}
if found != set(names): sys.exit(f'swap: not found in {src_path}: {sorted(set(names) - found)}')
if idx != list(range(idx[0], idx[-1] + 1)): sys.exit(f'swap: {names} do not stand together in {src_path}')
first, last = top[idx[0]], top[idx[-1]]
a = min([first.lineno] + [d.lineno for d in getattr(first, 'decorator_list', [])]) - 1; b = last.end_lineno
shim = open(shim_path, encoding='utf-8').read()
if not shim.endswith('\n'): shim += '\n'
open(out_path, 'w', encoding='utf-8').write(''.join(lines[:a]) + shim + ''.join(lines[b:]))
shown = src_path.split('/studies/', 1)[-1]
print(f'swap {shown}: lines {a + 1}-{b} ({b - a} lines: {", ".join(names)}) -> {shim_path.rsplit("/", 1)[-1]} ({shim.count(chr(10))} lines)')
