"""EXPLORATIV, ausserhalb des Protokolls: E-11 mit Teilklassen H1a/H1b/H1c und H3a/H3b
nach Protokollerweiterung Fassung 2 (16:55) und Nachtrag 2a (19:05), 31.10.2026.
Mass, Merkmalsraum, Bezugsklassen und Schaetzer wie e11.py; neu sind nur Klassen, Mischung und Variante K."""
import pfade
import re, json, math, os, sys, itertools, numpy as np, prep, calib
sys.path.insert(0, '../norm'); import angleichen as A
from calib import cdist, auc, rate
E = str(pfade.E11 / 'texte') + '/'
K = os.environ['KLASSEN'] + '/'          # eingefrorene Klassentexte
OUT = os.environ['E11_OUT']

def rd(p): return open(p, encoding='utf-8').read()
TX = {a: rd(E + a + '.txt') for a in ['Gaudy_1829_1833', 'Gaudy_Lieder_1829_1833', 'Beck_1840', 'Meissner_1846',
      'Hartmann_1845_1847', 'Dingelstedt_1842', 'Mueller_WvK_1841', 'Scherr_1842', 'Storm_1843', 'ThMommsen_1843']}
TX['Steinmann_1861'] = rd(K + 'Steinmann_1861.txt')
H1C = {'Haupt': rd(K + 'H1c_Haupt.txt'), 'mitZeit': rd(K + 'H1c_mitZeit.txt')}
MAN = json.load(open(K + 'H1b_manifest.json', encoding='utf-8'))
H1BPLUS = rd(K + 'H1b_plus.txt')
CAND = rd(str(pfade.KANDIDAT))

def tk(t): return prep.toks(A.angleichen(t))
def sc(x, ref, comp): return float(np.median(cdist(x, comp)) - np.median(cdist(x, ref)))
def norm4(ws): return ' '.join(re.sub(r'[^\wäöüß]', '', w.lower()) for w in ws[:4])

D = calib.build('ang', 548)
mapping = prep.a2_mapping()
# Entsprechungen H1b -> Buch der Lieder ueber die ersten vier Woerter (Nachtrag 2a, 1)
BDL = {}
for s, n, t in D['_poems']:
    if s in prep.LIED: BDL.setdefault(norm4(prep.toks(t)), set()).add(f'{s} {n}')
for m in MAN: m['bdl'] = sorted(BDL.get(norm4(tk(m['text'])), set()))
# H1b+: Entsprechungen fuer alle Zeilenanfaenge
plus_ids = set()
L = A.angleichen(H1BPLUS).split('\n')
for i in range(len(L)):
    ws = ' '.join(L[i:i + 3]).split()
    plus_ids |= BDL.get(norm4(ws), set())
def ref_minus(Z, ids): return calib.a1_minus(D, Z, set(ids), 548)

def halves(b): return [b[:274], b[274:548]]

def compute(kind):
    Z, _ = calib.featurize(D, kind)
    A1 = np.array([Z(b) for b in D['A1L']]); C2 = np.array([Z(b) for b in D['C2']])
    r = {548: {}, 274: {}}
    c = [(w, 'K') for w in tk(CAND)][:548]
    r[548]['cand'] = sc(Z(c), A1, C2)
    hs = [sc(Z(h), A1, C2) for h in halves(c)]
    r[274]['cand'] = float(np.mean(hs)); r[274]['cand_haelften'] = hs
    # H1a = A2 mit a1_minus
    for b in D['A2']:
        ids = {mapping.get(p, '') for _, p in b} - {''}
        ref = ref_minus(Z, ids)
        r[548].setdefault('H1a', []).append(sc(Z(b), ref, C2))
        for h in halves(b):
            idh = {mapping.get(p, '') for _, p in h} - {''}
            r[274].setdefault('H1a', []).append(sc(Z(h), ref_minus(Z, idh), C2))
    # H1b mit Gedichtkennung
    st = [(w, i) for i, m in enumerate(MAN) for w in tk(m['text'])]
    for size in (548, 274):
        v = []
        for b in prep.blocks(st, size):
            ids = set().union(*[set(MAN[i]['bdl']) for i in {p for _, p in b}])
            v.append(sc(Z(b), ref_minus(Z, ids), C2))
        r[size]['H1b'] = v
        refp = ref_minus(Z, plus_ids)
        r[size]['H1b+'] = [sc(Z(b), refp, C2) for b in prep.blocks([(w, 'p') for w in tk(H1BPLUS)], size)]
        for nm, t in H1C.items():
            r[size]['H1c_' + nm] = [sc(Z(b), A1, C2) for b in prep.blocks([(w, nm) for w in tk(t)], size)]
        for a, t in TX.items():
            r[size][a] = [sc(Z(b), A1, C2) for b in prep.blocks([(w, a) for w in tk(t)], size)]
    return r

def compute_vers():
    src = open('e7.py').read().split("HK=np.vstack")[0]; g = {}; exec(src, g)
    f = lambda t: [g['s'](g['Z'](g['F'](b)), g['A1'], g['CZ']['C2']) for b in g['blk'](g['sel'](g['lines_of'](t)))]
    r = {'cand': g['s'](g['Z'](g['F'](g['cl'])), g['A1'], g['CZ']['C2']), 'H1a': list(g['pos3'])}
    r['H1b'] = f('\n\n'.join(m['text'] for m in MAN)); r['H1b+'] = f(H1BPLUS)
    for nm, t in H1C.items(): r['H1c_' + nm] = f(t)
    for a, t in TX.items(): r[a] = f(t)
    return {548: r}

H3A = ['Gaudy_1829_1833', 'Steinmann_1861', 'Meissner_1846']
H3B = ['Beck_1840', 'Hartmann_1845_1847', 'Dingelstedt_1842', 'Mueller_WvK_1841', 'Scherr_1842', 'Storm_1843', 'ThMommsen_1843']

def setup(name):
    h3a, h3b, h1c, h1b = list(H3A), list(H3B), 'H1c_Haupt', 'H1b'
    if name == 'Beck_in_H3a': h3b.remove('Beck_1840'); h3a.append('Beck_1840')
    if name == 'Gaudy_nur_Lieder': h3a[0] = 'Gaudy_Lieder_1829_1833'
    if name == 'H1c_mit_Zeitgedichten': h1c = 'H1c_mitZeit'
    if name == 'H1b_plus': h1b = 'H1b+'
    return h1b, h1c, h3a, h3b

def kn(v, s): return int((np.array(v) >= s).sum()), len(v)

def evaluate(R, size, textset, wH1, wH3):
    h1b, h1c, h3a, h3b = setup(textset)
    out = {}
    for meas, r in R.items():
        if size not in r: continue
        rr = r[size]; s = rr['cand']
        parts1 = {'H1a': rr['H1a'], 'H1b': rr[h1b], 'H1c': rr[h1c]}
        parts3 = {'H3a': [x for a in h3a for x in rr[a]], 'H3b': [x for a in h3b for x in rr[a]]}
        use1 = {k: w for k, w in wH1.items() if w > 0 and len(parts1[k]) >= 3}
        num = sum(w * rate(*kn(parts1[k], s)) for k, w in use1.items()) / sum(use1.values())
        den = sum(w * rate(*kn(parts3[k], s)) for k, w in wH3.items()) / sum(wH3.values())
        pos = [x for k in use1 for x in parts1[k]]; neg = [x for k in parts3 for x in parts3[k]]
        a = auc(pos, neg)
        out[meas] = dict(Kandidat_s=round(s, 3), AUC=round(a, 3), Tor=a >= 0.75,
                         log10LR=round(math.log10(num / den), 3),
                         Teilklassen={k: '%d/%d' % kn(v, s) for k, v in {**parts1, **parts3}.items()},
                         beschreibend=[k for k in parts1 if k not in use1])
    def wert(neutral):
        ok = [(0.0 if (neutral and m == 'Zeichen-4-Gramme') else d['log10LR']) for m, d in out.items() if d['Tor']]
        return round(max(-0.5, min(0.5, float(np.median(ok)))), 2) if ok else 0.0, round(float(np.median(ok)), 3) if ok else 0.0
    w, wu = wert(False); wn, _ = wert(True)
    return dict(Masse=out, Wertung=w, Wertung_ungekappt=wu, Wertung_4g_neutral=wn)

def post(w):
    f = lambda n, a, b: 100 / (1 + n / 2 * 10 ** -a + n / 2 * 10 ** -b)
    B = lambda n: f(n, 1.5, 0.20 + w); S = lambda n: f(n, 0.75, -0.40 + w)
    return {'Haupt_1:5-1:3': f'{B(5):.0f}-{B(3):.0f}', 'offen_unecht_1:7': f'{B(7):.0f}',
            'skeptisch_Ref': f'{S(5):.0f}-{S(3):.0f}', 'skeptisch_1:7': f'{S(7):.0f}', 'skeptisch_1:20-1:7': f'{S(20):.0f}-{S(7):.0f}'}

if __name__ == '__main__':
    R = {'Delta Wörter (MFW150)': compute('w'), 'Zeichen-4-Gramme': compute('c'),
         'Versmerkmale (E-7)': compute_vers()}
    desc = {}
    for meas, r in R.items():
        for size, rr in r.items():
            desc[f'{meas} | {size}'] = {k: (dict(n=len(v), median=round(float(np.median(v)), 3), mind_so_nah='%d/%d' % kn(v, rr['cand']))
                                         if isinstance(v, list) and k != 'cand_haelften' else v) for k, v in rr.items()}
    runs = []
    W3 = {'1:1': {'H3a': 1, 'H3b': 1}, '1:3': {'H3a': 1, 'H3b': 3}, '3:1': {'H3a': 3, 'H3b': 1}}
    W1 = {548: {'1:1': {'H1a': 1, 'H1b': 0, 'H1c': 1}, '2:1': {'H1a': 2, 'H1b': 0, 'H1c': 1}, '1:2': {'H1a': 1, 'H1b': 0, 'H1c': 2}},
          274: {'1:1:1': {'H1a': 1, 'H1b': 1, 'H1c': 1}, '2:1:1': {'H1a': 2, 'H1b': 1, 'H1c': 1},
                '1:2:1': {'H1a': 1, 'H1b': 2, 'H1c': 1}, '1:1:2': {'H1a': 1, 'H1b': 1, 'H1c': 2}}}
    for size in (548, 274):
        for ts in ['Haupt', 'Beck_in_H3a', 'Gaudy_nur_Lieder', 'H1c_mit_Zeitgedichten'] + (['H1b_plus'] if size == 274 else []):
            for n1, w1 in W1[size].items():
                for n3, w3 in W3.items():
                    if ts != 'Haupt' and (n1 not in ('1:1', '1:1:1') or n3 != '1:1'): continue
                    e = evaluate(R, size, ts, w1, w3)
                    runs.append(dict(Variante='548' if size == 548 else 'K (274)', Texte=ts, H1=n1, H3=n3, **e,
                                     Bilanz=post(e['Wertung']), Bilanz_4g_neutral=post(e['Wertung_4g_neutral'])))
    out = dict(H1b_Entsprechungen_BdL={f"{m['gruppe']} {m['nr']}": m['bdl'] for m in MAN},
               H1bplus_Entsprechungen_BdL=sorted(plus_ids), Beschreibung=desc, Laeufe=runs)
    json.dump(out, open(OUT, 'w'), ensure_ascii=False, indent=1)
    for r in runs:
        print(r['Variante'], r['Texte'], r['H1'], r['H3'], '|', r['Wertung'], f"(ungekappt {r['Wertung_ungekappt']}, 4g neutral {r['Wertung_4g_neutral']})",
              '|', {m: (d['AUC'], d['log10LR'], d['Teilklassen']) for m, d in r['Masse'].items()})
