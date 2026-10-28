# Stacking faults and the Hexagonality Law (DICTO 10-28): how many layers each classical fault turns from cubic to hexagonal (in fcc)
# or from hexagonal to cubic (in hcp). Jagodzinski's rule: a layer is h when its two neighbours sit in the same position, c otherwise.
# Each fault is written as a long sequence with the fault in the middle (the classical letter sequences); the layer types are read
# away from the ends and compared with the perfect crystal. By the Hexagonality Law (#66), a fault changes the total volume of every
# kind of piece by exactly (change in h layers) x (V(hh) - V(cc)) -- wherever the law's hypothesis holds.
def types_inner(w, pad=6):
    return ''.join('h' if w[k - 1] == w[k + 1] else 'c' for k in range(pad, len(w) - pad))
FAULTS = {   # name: (perfect, faulted), the classical letter sequences (e.g. Hirth and Lothe; Verma and Krishna)
    'fcc twin boundary':        ('ABCABCABCABCABCABC', 'ABCABCABCBACBACBAC'),
    'fcc intrinsic fault':      ('ABCABCABCABCABCABC', 'ABCABCABCBCABCABCA'),   # one layer (A) removed
    'fcc extrinsic fault':      ('ABCABCABCABCABCABC', 'ABCABCABCBABCABCAB'),   # one layer (B) inserted
    'hcp growth fault I1':      ('ABABABABABABABABAB', 'ABABABABCBCBCBCBCB'),
    'hcp deformation fault I2': ('ABABABABABABABABAB', 'ABABABABCACACACACA'),
    'hcp extrinsic fault E':    ('ABABABABABABABABAB', 'ABABABABCABABABABA'),
}
out = {}
for name, (p, f) in FAULTS.items():
    tp, tf = types_inner(p), types_inner(f)
    dh = tf.count('h') - tp.count('h')
    out[name] = dh
    print(f'{name:26s} perfect {tp}  faulted {tf}  change in h layers {dh:+d}')
import json, os
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'faults.json'), 'w'), indent=1)
