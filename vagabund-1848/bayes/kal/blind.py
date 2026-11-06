"""II.5 Verblindete Anwendung: X01–X10 nach den Regeln der Kalibrierung. Gibt nur Zahlen aus, keinen Text."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import json, glob, os, numpy as np, calib
from calib import cdist
B = str(pfade.KORPUS / 'verblindung' / 'blind')
# Eingabeprüfung (nachträglich ergänzt, 6.11.2026): Alle zehn Proben müssen in beiden Schichten vorliegen.
# Fehlen einzelne, liefe das Skript sonst mit weniger Proben durch, und die Zufallsfolge (Impostors) verschöbe sich.
ERWARTET = [f'X{i:02d}' for i in range(1, 11)]
FEHLT = [f'{l}/{c}.txt' for l in ('ang', 'hist') for c in ERWARTET if not os.path.isfile(f'{B}/{l}/{c}.txt')]
if FEHLT:
    raise SystemExit('Abbruch, es fehlen Blindproben: ' + ', '.join(FEHLT) +
                     '. Die Proben mit Heine-Text sind nicht veröffentlicht; s. EINGABEN_NICHT_ENTHALTEN.md.')
K = json.load(open('kalibrierung.json'))['ergebnisse']; O = json.load(open('openset.json'))
def kal(layer, mass): return next(r for r in K if r['schicht'] == layer and r['groesse'] == 548 and r['mass'] == mass)
def opn(layer, mass): return next(r for r in O if r['schicht'] == layer and r['mass'] == mass)
rng = np.random.default_rng(20261016)
res = {}
for layer in ['ang', 'hist']:
    D = calib.build(layer, 548)
    for kind, mass in [('w', 'Wörter 150'), ('c', 'Zeichen-4 150')]:
        Z, _ = calib.featurize(D, kind)
        A1 = np.array([Z(b) for b in D['A1L']]); B1 = np.array([Z(b) for b in D['B1']]); C2 = np.array([Z(b) for b in D['C2']])
        imp = np.vstack([np.array([Z(b) for b in D[c]]) for c in ['B1', 'B2', 'C2', 'C3']]); nf = A1.shape[1]
        k = kal(layer, mass); o = opn(layer, mass)
        for f in sorted(glob.glob(f'{B}/{layer}/X*.txt')):
            code = os.path.basename(f)[:-4]
            x = Z([(w, code) for w in open(f, encoding='utf-8').read().split()])
            s2 = float(np.median(cdist(x, B1)) - np.median(cdist(x, A1)))
            s3 = float(np.median(cdist(x, C2)) - np.median(cdist(x, A1)))
            sc = 0
            for _ in range(100):
                m = rng.random(nf) < 0.5
                h = A1[rng.integers(len(A1))][m]; I = imp[rng.choice(len(imp), 10, replace=False)][:, m]
                sc += cdist(x[m], h[None])[0] < cdist(x[m], I).min()
            sc /= 100
            r = res.setdefault(code, {})
            kh2, kh3, ko = k['H1:H2 (A2 gg. B1)'], k['H1:H3 (A2 gg. C2)'], o['Müller/Wunderhorn (C3)']
            r[f'{layer} {mass}'] = dict(
                s_H2=round(s2, 3), H2='nah' if s2 > 0 else 'fern', LR_H2=kh2['LR_nah'] if s2 > 0 else kh2['LR_fern'],
                s_H3=round(s3, 3), H3='nah' if s3 > 0 else 'fern',
                LR_H3_offen=ko['LR_nah'] if s3 > 0 else ko['LR_fern'],
                LR_H3_offen_Hektorfremd=o['Hektor (B1+B2)']['LR_nah'] if s3 > 0 else o['Hektor (B1+B2)']['LR_fern'],
                LR_H3_geschlossen=kh3['LR_nah'] if s3 > 0 else kh3['LR_fern'],
                imp=round(sc, 2), imp_H2='nah' if sc >= k['Impostors H1:H2']['schwelle'] else 'fern',
                imp_H3='nah' if sc >= k['Impostors H1:H3']['schwelle'] else 'fern')
json.dump(res, open('blind_ergebnis.json', 'w'), ensure_ascii=False, indent=1)
for code in sorted(res):
    a = res[code]['ang Wörter 150']; c = res[code]['ang Zeichen-4 150']; h = res[code]['hist Wörter 150']
    print(code, '| W:', a['H2'], a['LR_H2'], a['H3'], a['LR_H3_offen'], 'imp', a['imp'], a['imp_H2'], a['imp_H3'],
          '| Z:', c['H2'], c['H3'], 'imp', c['imp'], '| hist W:', h['H2'], h['H3'], f"s2={a['s_H2']} s3={a['s_H3']}")
