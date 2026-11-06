"""Offene Gegenprobe für H1:H3: Der Nachahmer ist nicht im Vergleichssatz (wie Warnebold)."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import numpy as np, json, calib, prep
from calib import cdist, auc, rate, wilson
mapping = prep.a2_mapping()
out = []
for layer in ['hist', 'ang']:
    D = calib.build(layer, 548)
    for kind in ['w', 'c']:
        Z, _ = calib.featurize(D, kind)
        A1 = np.array([Z(b) for b in D['A1L']]); C2 = np.array([Z(b) for b in D['C2']])
        pos = []
        for b in D['A2']:
            ov = {mapping.get(p, '') for _, p in b} - {''}
            ref = calib.a1_minus(D, Z, ov, 548); x = Z(b)
            pos.append(np.median(cdist(x, C2)) - np.median(cdist(x, ref)))
        res = {}
        for lab, cls in [('Müller/Wunderhorn (C3)', ['C3']), ('Hektor (B1+B2)', ['B1', 'B2'])]:
            neg = [np.median(cdist(Z(b), C2)) - np.median(cdist(Z(b), A1)) for c in cls for b in D[c]]
            pos_, neg = np.array(pos), np.array(neg)
            h, f = (pos_ > 0).sum(), (neg > 0).sum(); hl, hh = wilson(h, len(pos_)); fl, fh = wilson(f, len(neg))
            res[lab] = dict(auc=round(auc(pos_, neg), 3), treffer=f'{h}/{len(pos_)}', fehlalarm=f'{f}/{len(neg)}',
                            LR_nah=round(rate(h, len(pos_)) / rate(f, len(neg)), 2), LR_nah_min95=round(hl / max(fh, 1e-9), 2),
                            LR_fern=round((1 - rate(h, len(pos_))) / (1 - rate(f, len(neg))), 2))
        # Steinmann (C1) als Einzelfall, 485 Wörter, gleiche Regel
        st = prep.stream(layer, 'C1'); x = Z(st)
        res['Steinmann (C1, 485 Wörter)'] = dict(s=round(float(np.median(cdist(x, C2)) - np.median(cdist(x, A1))), 3))
        row = dict(schicht=layer, mass='Wörter 150' if kind == 'w' else 'Zeichen-4 150', **res)
        out.append(row); print(json.dumps(row, ensure_ascii=False))
json.dump(out, open('openset.json', 'w'), ensure_ascii=False, indent=1)
