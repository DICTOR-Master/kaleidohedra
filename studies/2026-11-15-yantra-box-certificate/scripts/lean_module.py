"""Lean module-system layout shared by every Lean generator of this study (Palomar source rule, 16 Nov 2026):
`module` first, the leading imports made public, then `@[expose] public section` and the rest of the file unchanged.
Module doc comments therefore come after `module`. Idempotent: a text that already starts with `module` is returned as is.
The same transformation that scripts/c14_palomar_entry.py used for the entry built on 16 Nov 2026."""
import re

_HEAD = re.compile(r'(?:\s+|--[^\n]*\n|/-(?![-!])(?:.|\n)*?-/)*')   # blanks, line comments, plain block comments


def is_module(text):
    m = _HEAD.match(text)
    rest = text[m.end():]
    return rest.startswith('module') and (len(rest) == 6 or not (rest[6].isalnum() or rest[6] in "_'.!?"))


def modulize(text):
    """`module`, public imports, an exposed public section, then the body"""
    if is_module(text):
        return text
    lines = text.split('\n'); out = ['module', '']; i = 0
    while i < len(lines) and (lines[i].startswith('import ') or lines[i].strip() == ''):
        if lines[i].startswith('import '): out.append('public ' + lines[i])
        i += 1
    out += ['', '@[expose] public section', '']
    assert not any(l.startswith('import ') for l in lines[i:]), 'an import after the leading block'
    return '\n'.join(out + lines[i:])


if __name__ == '__main__':
    # usage: lean_module.py FILE...   rewrites each file in module form (for hand-written sources)
    import sys
    for f in sys.argv[1:]:
        t = open(f).read(); n = modulize(t)
        if n != t: open(f, 'w').write(n); print('modulized', f)
