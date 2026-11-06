"""E-2 Zeta (Craig) nach II.3a."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, json, collections, numpy as np, calib, prep, sys
sys.path.insert(0, '../norm'); import angleichen as A
from calib import auc, rate, wilson
WRE = re.compile(r"[^\W\d_]+(?:'[^\W\d_]*)?")
CAND = str(pfade.KANDIDAT)
def words(tokens): return [w.lower() for t in tokens for w in WRE.findall(t)]
def segs(ws, n=100): return [set(ws[i:i+n]) for i in range(0, len(ws) - n + 1, n)]
def markers(H, K, m=100):
    vh = collections.Counter(w for s in H for w in s); vk = collections.Counter(w for s in K for w in s)
    vocab = [w for w in set(vh) | set(vk) if vh[w] + vk[w] >= 3]
    z = {w: vh[w] / len(H) - vk[w] / len(K) for w in vocab}
    srt = sorted(vocab, key=lambda w: (z[w], w))  # Gleichstände alphabetisch, damit das Ergebnis nicht vom Hash-Zufall abhängt
    return set(srt[-m:]), set(srt[:m]), z
def val(ws, hm, km):
    t = set(ws); return len(t & hm) / len(t) - len(t & km) / len(t)
D = calib.build('ang', 548); mapping = prep.a2_mapping()
poems = [(f'{s} {n}', words(prep.toks(t))) for s, n, t in D['_poems'] if s in prep.LIED]
A2b = [words([t for t, _ in b]) for b in D['A2']]; A2ids = [{p for _, p in b} for b in D['A2']]
B1b = [words([t for t, _ in b]) for b in D['B1']]; B2b = [words([t for t, _ in b]) for b in D['B2']]
def heine_segs(excl_block=None, excl_poems=set()):
    s = []
    for pid, ws in poems:
        if pid not in excl_poems: s += segs(ws)
    for i, ws in enumerate(A2b):
        if i != excl_block: s += segs(ws)
    return s
def hek_segs(excl=None):
    s = []
    for i, ws in enumerate(B1b + B2b):
        if i != excl: s += segs(ws)
    return s
pos = []
for i, ws in enumerate(A2b):
    ov = {mapping.get(p, '') for p in A2ids[i]} - {''}
    hm, km, _ = markers(heine_segs(i, ov), hek_segs()); pos.append(val(ws, hm, km))
negB1, negB2 = [], []
for j, ws in enumerate(B1b + B2b):
    hm, km, _ = markers(heine_segs(), hek_segs(j)); (negB1 if j < len(B1b) else negB2).append(val(ws, hm, km))
def summ(neg):
    p, n = np.array(pos), np.array(neg); h, f = (p > 0).sum(), (n > 0).sum()
    return dict(auc=round(auc(p, n), 3), treffer=f'{h}/{len(p)}', fehlalarm=f'{f}/{len(n)}')
hm, km, z = markers(heine_segs(), hek_segs())
cand = words(prep.toks(A.angleichen(open(CAND, encoding='utf-8').read())))
ct = set(cand)
res = dict(kalibrierung_B1=summ(negB1), kalibrierung_B2=summ(negB2), kandidat=round(val(cand, hm, km), 4),
           kandidat_heine_marker=sorted(ct & hm, key=lambda w: (-z[w], w)), kandidat_hektor_marker=sorted(ct & km, key=lambda w: (z[w], w)),
           heine_marker_top30=sorted(hm, key=lambda w: (-z[w], w))[:30], hektor_marker_top30=sorted(km, key=lambda w: (z[w], w))[:30],
           A2_median=round(float(np.median(pos)), 4), B1_werte=[round(x, 4) for x in negB1], B2_median=round(float(np.median(negB2)), 4))
stein = words([t for t, _ in prep.stream('ang', 'C1')]); res['steinmann'] = round(val(stein, hm, km), 4)
json.dump(res, open('e2.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=0))
