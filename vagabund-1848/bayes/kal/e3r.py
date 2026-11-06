"""E-3 Versmerkmale nach II.3a."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, json, glob, os, numpy as np, prep, sys
sys.path.insert(0, '../norm'); import angleichen as A
from calib import cdist, auc, rate, wilson
NUM = re.compile(r'^\s*([IVXLC]+|\d+)\s*\.?\s*$')
CAND = str(pfade.KANDIDAT)
def lines_of(text):
    L = [l.rstrip() for l in A.angleichen(text).split('\n') if not NUM.match(l)]
    out = []
    for i, l in enumerate(L):   # isolierte Einzelzeilen zwischen Leerzeilen = Überschriften
        prev = L[i-1].strip() if i else ''; nxt = L[i+1].strip() if i + 1 < len(L) else ''
        if l.strip() and not prev and not nxt: continue
        out.append(l)
    return out
def blocks(lines, size=548):
    B, cur, n = [], [], 0
    for l in lines:
        cur.append(l); n += len(l.split())
        if n >= size: B.append(cur); cur, n = [], 0
    return B
V = re.compile(r'[aeiouyäöü]+')
def syl(w): return max(1, len(V.findall(w.lower())))
NORM = [('ie', 'i'), ('ü', 'i'), ('y', 'i'), ('ö', 'e'), ('ä', 'e'), ('äu', 'ai'), ('eu', 'ai'), ('ei', 'ai'), ('ey', 'ai'), ('h', ''), ('b', 'p'), ('d', 't'), ('g', 'k'), ('ß', 's'), ('ss', 's')]
def rkey(w):
    w = re.sub(r"[^a-zäöüß]", '', w.lower())
    if not w: return None
    g = list(V.finditer(w))
    if not g: return None
    fem = len(g) >= 2 and re.search(r'(e|en|er|el|em|es|ern|eln)$', w)
    m = g[-2] if fem else g[-1]
    return w[m.start():]
def nkey(k):
    for a, b in NORM: k = k.replace(a, b)
    return re.sub(r'(.)\1', r'\1', k)
def feats(lines):
    vs = [l.strip() for l in lines if l.strip()]
    words = sum(len(l.split()) for l in vs)
    last = [re.sub(r"[^\wäöüß']", '', l.split()[-1]) for l in vs]
    fem = np.mean([bool(re.search(r'(e|en|er|el|em|es|ern|eln)$', w.lower())) and syl(w) >= 2 for w in last])
    keys = [rkey(w) for w in last]; pure = impure = 0
    for i, k in enumerate(keys):
        if not k: continue
        for j in range(i + 1, min(len(keys), i + 4)):
            if keys[j] and keys[j] == k: pure += 1; break
            if keys[j] and nkey(keys[j]) == nkey(k): impure += 1; break
    unrein = impure / max(1, pure + impure)
    elis = 100 * sum(l.count("'") for l in vs) / words
    enj = np.mean([not re.search(r'[.,;:!?—\-"\']$', l) for l in vs])
    sy = [sum(syl(w) for w in re.findall(r"[^\W\d_]+", l)) for l in vs]
    und = np.mean([l.split()[0].strip('"').lower() == 'und' for l in vs])
    st, cur = [], 0
    for l in lines:
        if l.strip(): cur += 1
        elif cur: st.append(cur); cur = 0
    if cur: st.append(cur)
    four = np.mean([s == 4 for s in st]) if st else 0
    return np.array([fem, unrein, elis, enj, np.mean(sy), np.std(sy), und, four])
_KEEP=[0,1,4,5,6,7]
NAMES = ['weibl. Kadenz', 'unreine Reime', 'Elisionen/100 W.', 'Vers ohne Satzzeichen', 'Silben/Vers', 'Streuung Silben', '"Und" am Versanfang', 'vierzeilige Strophen']
K = prep.ANG['korpus']
_f0=None
_feats_full=feats
def feats(lines): return _feats_full(lines)[_KEEP]
def fileblocks(names): return [b for n in names for b in blocks(lines_of(open(f'{K}/{n}_ang.txt'.replace('_ang_ang', '_ang'), encoding='utf-8').read() if False else open(prep.kf('hist', n), encoding='utf-8').read()))]
C = {c: fileblocks(prep.CLASSES[c]) for c in ['B1', 'B2', 'C2', 'C3']}
a2 = [(pid, lines_of(t)) for pid, t in prep.a2_poems('hist')]
A2B, cur, ids, n = [], [], set(), 0
for pid, L in a2:
    cur += L + ['']; ids.add(pid); n += sum(len(l.split()) for l in L)
    if n >= 548: A2B.append((ids, cur)); cur, ids, n = [], set(), 0
poems = [(f'{s} {n_}', lines_of(t)) for s, n_, t in prep.bdl_poems('hist') if s in prep.LIED]
def a1blocks(excl=set()):
    L = []
    for pid, l in poems:
        if pid not in excl: L += l + ['']
    return blocks(L)
mapping = prep.a2_mapping()
train = [feats(b) for b in a1blocks()] + [feats(b) for _, b in A2B] + [feats(b) for c in C for b in C[c]]
M = np.array(train); mu, sd = M.mean(0), M.std(0); sd[sd == 0] = 1
Z = lambda f: (f - mu) / sd
A1 = np.array([Z(feats(b)) for b in a1blocks()]); CZ = {c: np.array([Z(feats(b)) for b in C[c]]) for c in C}
def s(x, ref, comp): return float(np.median(cdist(x, comp)) - np.median(cdist(x, ref)))
pos2, pos3 = [], []
for ids, b in A2B:
    ref = np.array([Z(feats(x)) for x in a1blocks({mapping.get(p, '') for p in ids} - {''})]); x = Z(feats(b))
    pos2.append(s(x, ref, CZ['B1'])); pos3.append(s(x, ref, CZ['C2']))
def neg_closed(c):
    out = []
    for i in range(len(CZ[c])):
        o = np.delete(CZ[c], [j for j in (i-1, i, i+1) if 0 <= j < len(CZ[c])], 0)
        if len(o): out.append(s(CZ[c][i], A1, o))
    return out
def summ(pos, neg):
    p, n = np.array(pos), np.array(neg); h, f = (p > 0).sum(), (n > 0).sum(); hl, _ = wilson(h, len(p)); _, fh = wilson(f, len(n))
    return dict(auc=round(auc(p, n), 3), treffer=f'{h}/{len(p)}', fehlalarm=f'{f}/{len(n)}', LR_nah=round(rate(h, len(p)) / rate(f, len(n)), 2),
                LR_nah_min95=round(hl / max(fh, 1e-9), 2), LR_fern=round((1 - rate(h, len(p))) / (1 - rate(f, len(n))), 2))
res = {'Blöcke': dict(A1=len(A1), A2=len(A2B), **{c: len(CZ[c]) for c in CZ}),
       'H1:H2 geschlossen': summ(pos2, neg_closed('B1')), 'H1:H3 geschlossen': summ(pos3, neg_closed('C2')),
       'H1:H3 offen C3': summ(pos3, [s(x, A1, CZ['C2']) for x in CZ['C3']]),
       'H1:H3 offen Hektor': summ(pos3, [s(x, A1, CZ['C2']) for x in np.vstack([CZ['B1'], CZ['B2']])])}
cl = lines_of(open(CAND, encoding='utf-8').read()); cf = feats(cl); xc = Z(cf)
res['Kandidat'] = dict(woerter=sum(len(l.split()) for l in cl), s_H2=round(s(xc, A1, CZ['B1']), 3), s_H3=round(s(xc, A1, CZ['C2']), 3))
st = lines_of(open(prep.kf('hist', 'Steinmann_Lieder'), encoding='utf-8').read()); res['Steinmann'] = dict(s_H3=round(s(Z(feats(st)), A1, CZ['C2']), 3))
tab = {'Kandidat': cf, 'A1 Lied': np.mean([feats(b) for b in a1blocks()], 0), 'A2': np.mean([feats(b) for _, b in A2B], 0),
       'Hektor B1': np.mean([feats(b) for b in C['B1']], 0), 'Geibel C2': np.mean([feats(b) for b in C['C2']], 0), 'Müller/Wh. C3': np.mean([feats(b) for b in C['C3']], 0), 'Steinmann': feats(st)}
res['Merkmale'] = {k: dict(zip([NAMES[i] for i in _KEEP], [round(float(x), 3) for x in v])) for k, v in tab.items()}
json.dump(res, open('e3_ohne_ueberlieferung.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'Merkmale'}, ensure_ascii=False))
for k, v in res['Merkmale'].items(): print(k.ljust(14), v)
