"""E-1 Textverzerrung (DV-MA) nach II.3a."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, json, collections, numpy as np, calib, prep, sys
sys.path.insert(0, '../norm'); import angleichen as A
from calib import cdist, auc, rate, wilson
WRE = re.compile(r"[^\W\d_]+")
CAND = str(pfade.KANDIDAT)
def topk(D, k):
    c = collections.Counter()
    for cl in ['A1L', 'A1N', 'A2', 'B1', 'B2', 'C2', 'C3']:
        for b in D[cl]:
            for t, _ in b: c.update(w.lower() for w in WRE.findall(t))
    return {w for w, _ in c.most_common(k)}
def dist_tok(t, keep): return WRE.sub(lambda m: m.group(0) if m.group(0).lower() in keep else '*' * len(m.group(0)), t)
def distort(D, keep):
    E = {}
    for cl, v in D.items():
        if cl == '_poems': E[cl] = [(s, n, ' '.join(dist_tok(t, keep) for t in prep.toks(x))) for s, n, x in v]
        else: E[cl] = [[(dist_tok(t, keep), p) for t, p in b] for b in v]
    return E
def score(x, ref, comp): return float(np.median(cdist(x, comp)) - np.median(cdist(x, ref)))
def summarize(pos, neg):
    pos, neg = np.array(pos), np.array(neg); h, f = (pos > 0).sum(), (neg > 0).sum(); hl, hh = wilson(h, len(pos)); fl, fh = wilson(f, len(neg))
    return dict(auc=round(auc(pos, neg), 3), treffer=f'{h}/{len(pos)}', fehlalarm=f'{f}/{len(neg)}', LR_nah=round(rate(h, len(pos)) / rate(f, len(neg)), 2),
                LR_nah_min95=round(hl / max(fh, 1e-9), 2), LR_fern=round((1 - rate(h, len(pos))) / (1 - rate(f, len(neg))), 2))
mapping = prep.a2_mapping(); out = []
cand_ang = prep.toks(A.angleichen(open(CAND, encoding='utf-8').read()))
stein = prep.stream('ang', 'C1')
D0 = calib.build('ang', 548)
for k in [150, 50, 300]:
    keep = topk(D0, k); D = distort(D0, keep)
    Z, _ = calib.featurize(D, 'c')
    A1 = np.array([Z(b) for b in D['A1L']]); cls = {c: np.array([Z(b) for b in D[c]]) for c in ['B1', 'B2', 'C2', 'C3']}
    row = dict(k=k)
    for comp in ['B1', 'C2']:
        row[f'geschlossen {comp}'] = calib.contrast(D, Z, comp, 548, mapping)
    pos = []
    for b in D['A2']:
        ov = {mapping.get(p, '') for _, p in b} - {''}
        pos.append(score(Z(b), calib.a1_minus(D, Z, ov, 548), cls['C2']))
    row['offen C3 gg. C2-Referenz'] = summarize(pos, [score(x, A1, cls['C2']) for x in cls['C3']])
    row['offen Hektor gg. C2-Referenz'] = summarize(pos, [score(x, A1, cls['C2']) for x in np.vstack([cls['B1'], cls['B2']])])
    xc = Z([(dist_tok(t, keep), 'K') for t in cand_ang]); xs = Z([(dist_tok(t, keep), 'S') for t, _ in stein])
    row['Kandidat'] = dict(s_H2=round(score(xc, A1, cls['B1']), 3), s_H3=round(score(xc, A1, cls['C2']), 3))
    row['Steinmann'] = dict(s_H3=round(score(xs, A1, cls['C2']), 3))
    out.append(row); print(json.dumps(row, ensure_ascii=False))
json.dump(out, open('e1.json', 'w'), ensure_ascii=False, indent=1)
