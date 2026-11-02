import csv, sys, os
from collections import defaultdict, OrderedDict
repo = sys.argv[1]
preds = list(csv.DictReader(open(repo + '/data/predictions/predictions_log.csv', encoding='utf-8')))
res = {(r['run_id'], r['fixture_id']): r for r in csv.DictReader(open(repo + '/data/results/results_log.csv', encoding='utf-8'))}
CUT_H, CUT_M = 0.630204, 0.58084
BH, BM = 0.574623, 0.513753

def scored(run):
    out = []
    for p in preds:
        if p['run_id'] != run: continue
        r = res.get((run, p['fixture_id']))
        if not r or not r['score']: continue
        out.append((p, r))
    return out

for run in ['weekend_20261030_1200', 'weekend_20261029_0917']:
    rows = scored(run)
    print(f"\n########## {run}  scored {len(rows)}")
    # ---- Investigation 2: equal size comparison
    high = [(p, r) for p, r in rows if p['classification'] == 'High']
    med = [(p, r) for p, r in rows if p['classification'] == 'Medium']
    rej = sorted([(p, r) for p, r in rows if p['classification'] == 'rejected'], key=lambda x: -float(x[0]['model_score']))
    n = len(high)
    hits = lambda L: sum(r['over25_result'] == 'Y' for p, r in L)
    print(f"High: {hits(high)} of {n}; score range {min(float(p['model_score']) for p,r in high):.3f} to {max(float(p['model_score']) for p,r in high):.3f}")
    print(f"Medium: {hits(med)} of {len(med)}")
    top = rej[:n]
    print(f"Top {n} rejected by model_score: {hits(top)} of {n}; score range {float(top[-1][0]['model_score']):.3f} to {float(top[0][0]['model_score']):.3f}")
    print(f"Remaining rejected: {hits(rej[n:])} of {len(rej[n:])}")
    print(f"All rejected: {hits(rej)} of {len(rej)}")
    for p, r in top:
        print(f"   {float(p['model_score']):.3f} d20={p['drivers20']:>2} {p['competition']:<24} {p['home']} v {p['away']} {r['score']} {'HIT' if r['over25_result']=='Y' else 'miss'}  notes: {p['notes'][:70]}")
    # check rejection reason: scores above cut yet rejected?
    above = [(p, r) for p, r in rej if float(p['model_score']) >= CUT_M]
    print(f"Rejected with model_score >= medium cut {CUT_M}: {len(above)} ({hits(above)} hit)")
    for p, r in above: print("    ", p['home'], 'v', p['away'], p['model_score'], p['h_n'], p['a_n'], p['notes'][:60])
    # by drivers20 ranking
    topd = sorted(rej, key=lambda x: (-int(x[0]['drivers20'] or 0), -float(x[0]['model_score'])))[:n]
    print(f"Top {n} rejected by drivers20: {hits(topd)} of {n}")
    # High by drivers20 vs top rejected
    allsel = sorted(rows, key=lambda x: -float(x[0]['model_score']))
    print(f"Top {n} overall by model_score: {hits(allsel[:n])} of {n}")
    # score deciles across all scored
    bins = defaultdict(lambda: [0, 0])
    for p, r in rows:
        s = float(p['model_score']); b = f"{int(s*20)/20:.2f}"
        bins[b][1] += 1; bins[b][0] += r['over25_result'] == 'Y'
    print("by model_score 0.05 bin:", ', '.join(f"{k} {v[0]} of {v[1]}" for k, v in sorted(bins.items())))
    bins = defaultdict(lambda: [0, 0])
    for p, r in rows:
        d = int(p['drivers20'] or 0); b = d
        bins[b][1] += 1; bins[b][0] += r['over25_result'] == 'Y'
    print("by drivers20:", ', '.join(f"{k} {v[0]} of {v[1]}" for k, v in sorted(bins.items())))

    # ---- Investigation 3: BTTS
    print("\n--- BTTS ---")
    # verdict mapping check
    bad = []
    for p, r in rows:
        pb = float(p['p_btts']); lab = 'High' if pb >= BH else 'Medium' if pb >= BM else 'Low'
        if lab != p['btts_likelihood']: bad.append(('likelihood', p['home'], p['away'], pb, p['btts_likelihood']))
        if run.startswith('weekend_20261030'):
            exp_yes = lab == 'High' or p['trump'] == '1'
            if (p['btts'] == 'YES') != exp_yes: bad.append(('verdict', p['home'], p['away'], pb, p['btts'], lab))
            cs_h, cs_a, f_h, f_a = int(p['h_cs']), int(p['a_cs']), int(p['h_fts']), int(p['a_fts'])
            caution = cs_h >= 3 or cs_a >= 3 or f_h >= 3 or f_a >= 3
            exp_lean = 'YES' if exp_yes else ('lean YES' if lab == 'Medium' else 'no lean')
            if caution and exp_lean == 'YES' and p['trump'] != '1': exp_lean = 'lean YES'
            if exp_lean != p['btts_lean']: bad.append(('lean', p['home'], p['away'], pb, lab, p['btts_lean'], exp_lean, cs_h, cs_a, f_h, f_a))
        else:
            # V4 rule: YES iff pattern 'Both teams contribute'
            if (p['btts'] == 'YES') != (p['pattern'] == 'Both teams contribute'): bad.append(('v4verdict', p['home'], p['away'], p['pattern'], p['btts']))
    print("mapping mismatches:", len(bad)); [print('   ', b) for b in bad]
    # scoring by model band
    g = OrderedDict((k, [0, 0]) for k in ['High', 'Medium', 'Low'])
    for p, r in rows:
        g[p['btts_likelihood']][1] += 1; g[p['btts_likelihood']][0] += r['btts_result'] == 'Y'
    print("both scored by BTTS model band:", ', '.join(f"{k} {v[0]} of {v[1]}" for k, v in g.items()))
    g = OrderedDict()
    for p, r in rows:
        g.setdefault(p['btts'], [0, 0]); g[p['btts']][1] += 1; g[p['btts']][0] += r['btts_result'] == 'Y'
    print("both scored by verdict:", ', '.join(f"{k} {v[0]} of {v[1]}" for k, v in g.items()))
    # caution analysis
    g = OrderedDict()
    for p, r in rows:
        cs_h, cs_a, f_h, f_a = int(p['h_cs']), int(p['a_cs']), int(p['h_fts']), int(p['a_fts'])
        cs = cs_h >= 3 or cs_a >= 3; ft = f_h >= 3 or f_a >= 3
        k = (p['btts_likelihood'], 'cs3+' if cs else '', 'fts3+' if ft else '')
        g.setdefault(k, [0, 0]); g[k][1] += 1; g[k][0] += r['btts_result'] == 'Y'
    print("both scored by band x caution:")
    for k, v in sorted(g.items()): print("   ", k, f"{v[0]} of {v[1]}")
    # p_btts bins
    bins = defaultdict(lambda: [0, 0])
    for p, r in rows:
        s = float(p['p_btts']); b = f"{int(s*20)/20:.2f}"
        bins[b][1] += 1; bins[b][0] += r['btts_result'] == 'Y'
    print("by p_btts 0.05 bin:", ', '.join(f"{k} {v[0]} of {v[1]}" for k, v in sorted(bins.items())))
    # BTTS vs over25 independence: both scored by over25 class
    g = OrderedDict()
    for p, r in rows:
        g.setdefault(p['classification'], [0, 0]); g[p['classification']][1] += 1; g[p['classification']][0] += r['btts_result'] == 'Y'
    print("both scored by Over 2.5 band:", ', '.join(f"{k} {v[0]} of {v[1]}" for k, v in g.items()))
    # lean table for v4.1
    if run.startswith('weekend_20261030'):
        g = OrderedDict()
        for p, r in rows:
            g.setdefault((p['btts_likelihood'], p['btts_lean']), [0, 0]); g[(p['btts_likelihood'], p['btts_lean'])][1] += 1; g[(p['btts_likelihood'], p['btts_lean'])][0] += r['btts_result'] == 'Y'
        print("band x lean:", g)
        print("High band rows:")
        for p, r in sorted(rows, key=lambda x: -float(x[0]['p_btts'])):
            if p['btts_likelihood'] == 'High':
                print(f"   {p['p_btts']} {p['home']} v {p['away']} cs {p['h_cs']}/{p['a_cs']} fts {p['h_fts']}/{p['a_fts']} lean={p['btts_lean']} result {r['score']} btts {r['btts_result']}")
