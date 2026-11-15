"""Print the scaling tests and counts of the scaling-state froth runs (reads results/*_count.json). Usage: summary.py RESULTS_DIR"""
import sys, os, json, glob
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*_count.json'))):
    r = json.load(open(f)); print('=====', os.path.basename(f), 'stationary', r['stationary'], 'window', r['count_window'])
    for t in r['scaling_tests']:
        print(' test window', t['window'], 'ok', t['ok'], 'N first/last', t['N_first_last'], 'A first/last', [round(x) for x in t['Abar_first_last']],
              'mu2 %.3f <n> %.3f' % (t['mu2'], t['mean_n']), 'slope %.3f t0 %.0f' % (t['growth_slope'], t['t0']))
        print('   p(3..9)', {k: round(v, 4) for k, v in t['p'].items()})
        for i, q in enumerate(t['q']): print('   q%d' % i, {k: q[k] for k in ('max_dp', 'dmu2', 'ks', 'slope_rel', 'ok')}, 'mu2 %.3f' % q['mu2'])
        vn = t['von_neumann']; print('   vN slope %.3f n0 %.3f growth/vN %.3f (RM %.3f)' % (vn['slope'], vn['n0'], vn['growth_over_vn'], vn['RM_growth_over_vn']))
        if 'n2' in t: print('   n2 mu2 %.3f <n2> %.3f quarters' % (t['n2']['mu2'], t['n2']['mean_n']), [round(x, 3) for x in t['n2']['mu2_quarters']])
    if 'sums' in r:
        for k, x in r['sums'].items():
            print(' ', k, 'T2', x['vanished'], 'swaps', x['swaps'], 'total/T2', x['total_per_T2'], 'SS/T2', x['SS_side_shedding_per_T2'],
                  'RM/T2 rc1 %s rc0.5 %s rc2 %s' % tuple(x['RM'][c]['per_T2'] for c in ('1.0', '0.5', '2.0')),
                  'shares345 rc1', x['RM']['1.0']['shares_3_4_5'], 'rc2', x['RM']['2.0']['shares_3_4_5'], 'rc0.5', x['RM']['0.5']['shares_3_4_5'])
        print('  sides rc1 step1', r['sums']['step1 W=P=8']['RM']['1.0']['sides_at_ell2'])
        print('  shifted', r['shifted_step1_W=P=8']['total_per_T2'], r['shifted_step1_W=P=8']['RM']['1.0']['per_T2'])
        for b in r['per_block']:
            s = b['step1']; print('  block', b['block'], 'cells', b['cells_first_last'], 'T2', s['vanished'], 'RM1/T2', s['RM1_per_T2'], 'tot/T2', s['total_per_T2'], 'l2', s['ell2'])
