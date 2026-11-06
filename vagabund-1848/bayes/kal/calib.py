"""Kalibrierung II.4 nach Protokoll II.3 (Stichtag 16.10.2026). Ohne Kandidat, ohne Täuschungsblöcke."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, random, json, collections, numpy as np, prep
RNG = np.random.default_rng(20261016)
WORD = re.compile(r"[^\W\d_]+(?:'[^\W\d_]*)?|'[^\W\d_]+")

def words(b):  return [w.lower() for w in WORD.findall(' '.join(t for t, _ in b))]
def chars(b):
    s = re.sub(r'\s+', ' ', ' '.join(t for t, _ in b).lower())
    return [s[i:i+4] for i in range(len(s)-3)]

def build(layer, size):
    pool = set(prep.decoy_pool()) if True else set()
    D = {}
    a2 = prep.blocks(prep.a2_stream(layer), 548)
    # Täuschungsblöcke (548er-Spannen) aus den Strömen entfernen, dann neu in 'size' teilen
    def strip(stream, cls):
        n548 = len(stream)//548; keep = []
        for i in range(n548+1):
            if (cls, i) in pool: continue
            keep += stream[i*548:(i+1)*548]
        return keep
    D['A2'] = prep.blocks(strip(prep.a2_stream(layer), 'A2'), size)
    for c in ['B1', 'B2', 'C2', 'C3']:
        D[c] = prep.blocks(strip(prep.stream(layer, c), c), size)
    poems = prep.bdl_poems(layer)
    D['_poems'] = poems
    D['A1L'] = prep.blocks([(w, f'{s} {n}') for s, n, t in poems if s in prep.LIED for w in prep.toks(t)], size)
    D['A1N'] = prep.blocks([(w, f'{s} {n}') for s, n, t in poems if s in prep.NORD for w in prep.toks(t)], size)
    return D

def featurize(D, kind):
    f = words if kind == 'w' else chars
    train = [b for c in ['A1L', 'A1N', 'A2', 'B1', 'B2', 'C2', 'C3'] for b in D[c]]   # ohne C1, Kandidat, Täuschung
    tot = collections.Counter()
    for b in train: tot.update(f(b))
    vocab = [k for k, _ in tot.most_common(150)]
    idx = {k: i for i, k in enumerate(vocab)}
    def vec(b):
        c = collections.Counter(f(b)); n = sum(c.values()); v = np.zeros(len(vocab))
        for k, x in c.items():
            if k in idx: v[idx[k]] = x / n
        return v
    M = np.array([vec(b) for b in train]); mu = M.mean(0); sd = M.std(0); sd[sd == 0] = 1
    return (lambda b: (vec(b) - mu) / sd), vocab

def cdist(a, B):
    B = np.atleast_2d(B)
    return 1 - (B @ a) / (np.linalg.norm(B, axis=1) * np.linalg.norm(a) + 1e-12)

def a1_minus(D, Z, poem_ids, size):
    """A1-Liedteile ohne die Gedichte, die im A2-Block stecken (Protokoll Punkt 4)."""
    st = [(w, f'{s} {n}') for s, n, t in D['_poems'] if s in prep.LIED and f'{s} {n}' not in poem_ids for w in prep.toks(t)]
    return np.array([Z(b) for b in prep.blocks(st, size)])

def auc(pos, neg):
    pos = np.asarray(pos); neg = np.asarray(neg)
    return float(((pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean()))

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    p = k / n; d = 1 + z*z/n; c = p + z*z/(2*n); r = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return ((c - r) / d, (c + r) / d)

def rate(k, n):  return (k + 0.5) / (n + 1)     # Präzisierung: Glättung gegen Raten von 0 und 1

def contrast(D, Z, comp, size, mapping):
    A1 = np.array([Z(b) for b in D['A1L']])
    CZ = np.array([Z(b) for b in D[comp]])
    pos = []
    for b in D['A2']:
        pids = {p for _, p in b}; ov = {mapping.get(p, '') for p in pids} - {''}
        ref = a1_minus(D, Z, {o.rstrip('.') + '.' if not o.endswith('.') else o for o in ov} | ov, size)
        x = Z(b); pos.append(np.median(cdist(x, CZ)) - np.median(cdist(x, ref)))
    neg = []
    for i, b in enumerate(D[comp]):
        x = Z(b); others = np.delete(CZ, [j for j in (i-1, i, i+1) if 0 <= j < len(CZ)], axis=0)   # Nachbarblöcke (gleiche Gedichte) ausgeschlossen
        if len(others) == 0: continue
        neg.append(np.median(cdist(x, others)) - np.median(cdist(x, A1)))
    pos, neg = np.array(pos), np.array(neg)
    hit, fa = (pos > 0).sum(), (neg > 0).sum()
    hl, hh = wilson(hit, len(pos)); fl, fh = wilson(fa, len(neg))
    return dict(n_pos=len(pos), n_neg=len(neg), auc=round(auc(pos, neg), 3),
                treffer=f'{hit}/{len(pos)}', fehlalarm=f'{fa}/{len(neg)}',
                LR_nah=round(rate(hit, len(pos)) / rate(fa, len(neg)), 2),
                LR_nah_min95=round(hl / max(fh, 1e-9), 2),
                LR_fern=round((1 - rate(hit, len(pos))) / (1 - rate(fa, len(neg))), 2),
                LR_fern_max95=round((1 - hl) / max(1 - fh, 1e-9), 2))

def impostors(D, Z, comp, size, mapping, iters=100):
    A1 = np.array([Z(b) for b in D['A1L']]); nf = A1.shape[1]
    pool_cls = ['B1', 'B2', 'C2', 'C3']
    def score(x, ref, imps):
        s = 0
        for _ in range(iters):
            m = RNG.random(nf) < 0.5
            h = ref[RNG.integers(len(ref))][m]
            I = imps[RNG.choice(len(imps), size=min(10, len(imps)), replace=False)][:, m]
            s += cdist(x[m], h[None])[0] < cdist(x[m], I).min()
        return s / iters
    allimp = {c: np.array([Z(b) for b in D[c]]) for c in pool_cls}
    pos = []
    for b in D['A2']:
        pids = {p for _, p in b}; ov = {mapping.get(p, '') for p in pids} - {''}
        ref = a1_minus(D, Z, ov, size)
        pos.append(score(Z(b), ref, np.vstack([allimp[c] for c in pool_cls])))
    neg = []
    for i, b in enumerate(D[comp]):
        imps = np.vstack([np.delete(allimp[c], [j for j in (i-1, i, i+1) if 0 <= j < len(allimp[c])], 0) if c == comp else allimp[c] for c in pool_cls])
        neg.append(score(Z(b), A1, imps))
    pos, neg = np.array(pos), np.array(neg)
    # Schwelle nach Youden an A2 und Gegenklasse (Protokoll II.4)
    best = max(sorted(set(pos) | set(neg)), key=lambda t: (pos >= t).mean() - (neg >= t).mean())
    hit, fa = (pos >= best).sum(), (neg >= best).sum()
    hl, hh = wilson(hit, len(pos)); fl, fh = wilson(fa, len(neg))
    return dict(auc=round(auc(pos, neg), 3), schwelle=round(float(best), 2), treffer=f'{hit}/{len(pos)}', fehlalarm=f'{fa}/{len(neg)}', LR_nah_min95=round(hl / max(fh, 1e-9), 2),
                LR_nah=round(rate(hit, len(pos)) / rate(fa, len(neg)), 2), LR_fern=round((1 - rate(hit, len(pos))) / (1 - rate(fa, len(neg))), 2))

def genre(D, Z, draws=1000):
    L = np.array([Z(b) for b in D['A1L']]); N = np.array([Z(b) for b in D['A1N']]); Mu = np.array([Z(b) for b in D['C3'][:41]])  # C3: nur Müller (vor Wunderhorn)
    c = 0
    for _ in range(draws):
        l = L[RNG.integers(len(L))]; n = N[RNG.integers(len(N))]; m = Mu[RNG.integers(len(Mu))]
        c += cdist(l, n[None])[0] > cdist(l, m[None])[0]
    return round(c / draws, 3)

if __name__ == '__main__':
    mapping = prep.a2_mapping()
    R = {'stichtag': '2026-10-16', 'ergebnisse': []}
    for layer in ['hist', 'ang']:
        for size in [200, 351, 548]:
            D = build(layer, size)
            for kind in ['w', 'c']:
                Z, vocab = featurize(D, kind)
                row = dict(schicht=layer, groesse=size, mass='Wörter 150' if kind == 'w' else 'Zeichen-4 150',
                           bloecke={k: len(v) for k, v in D.items() if not k.startswith('_')})
                for comp, lab in [('B1', 'H1:H2 (A2 gg. B1)'), ('C2', 'H1:H3 (A2 gg. C2)'), ('C3', 'Kontrolle (A2 gg. C3)')]:
                    row[lab] = contrast(D, Z, comp, size, mapping)
                if size == 548:
                    row['gattung_anteil'] = genre(D, Z)
                    for comp, lab in [('B1', 'Impostors H1:H2'), ('C2', 'Impostors H1:H3')]:
                        row[lab] = impostors(D, Z, comp, size, mapping)
                R['ergebnisse'].append(row)
                print(json.dumps(row, ensure_ascii=False))
    json.dump(R, open('kalibrierung.json', 'w'), ensure_ascii=False, indent=1)
