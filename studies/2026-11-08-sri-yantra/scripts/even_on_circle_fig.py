import json, sys; sys.argv = ['x']
import even_yantra as E
x = (0.828646295, 0.6480975804, 0.4948781144, 0.9206010173); t = E.yantra(x)
s = lambda z: {'a': repr(float(z))}
json.dump({'E2': {k: {str(i): s(t[kk][i]) for i in range(1, 10)} for k, kk in (('b', 'b'), ('w', 'w'), ('apex', 'a'))}}, open('even2.json', 'w'))
print('FINAL ok' if t is not None else 'FINAL FAIL: no yantra')
