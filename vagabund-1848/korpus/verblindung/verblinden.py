#!/usr/bin/env python3
"""Verblindung nach Protokoll II.3, Punkt 9 (Stichtag 16.10.2026).

Aufruf:  python3 verblinden.py PFAD/Kandidat_Vagabund.txt

- Der Kandidat wird wie alle Korpora behandelt: reine Zahlzeilen entfallen,
  dazu eine historische und eine angeglichene Fassung (angleichen.py).
- Aus den 10 Täuschungsblöcken im Ordner pool/ werden 9 zufällig gezogen und auf
  die Wortzahl des Kandidaten gekürzt.
- Die 10 Texte erhalten zufällige Codes (X01–X10) und landen in blind/hist und blind/ang.
- Der Schlüssel (Code -> Herkunft, mit Zufallssalz) geht nach schluessel/schluessel.json.
  Ausgegeben werden nur Wortzahl, Codes und der SHA-256-Prüfwert der Schlüsseldatei.
  Die Schlüsseldatei erst öffnen, wenn alle Ergebnisse festgehalten sind.
"""
import sys, os, re, json, hashlib, secrets, datetime, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import angleichen as A
NUMERAL = re.compile(r'^\s*([IVXLC]+|\d+)\s*\.?\s*$')
def clean(t):
    t = unicodedata.normalize('NFC', t)
    return '\n'.join(l for l in t.split('\n') if not NUMERAL.match(l))

if os.path.exists(os.path.join(HERE, 'schluessel', 'schluessel.json')):
    sys.exit('Abbruch: Es gibt schon eine Schlüsseldatei. Die Verblindung wird nur einmal erzeugt.')
raw = open(sys.argv[1], encoding='utf-8').read()
hist = clean(raw).split(); ang = clean(A.angleichen(raw)).split()
assert len(ang) == len(hist)
n = min(len(hist), 548); hist, ang = hist[:n], ang[:n]   # Blockgröße 548 (Protokoll Punkt 3)
rng = secrets.SystemRandom()
pool = sorted(f[:-4] for f in os.listdir(os.path.join(HERE, 'pool', 'hist')) if f.endswith('.txt'))
chosen = rng.sample(pool, 9)
items = [('Kandidat', hist, ang)]
for p in chosen:
    h = open(os.path.join(HERE, 'pool', 'hist', p + '.txt'), encoding='utf-8').read().split()[:n]
    a = open(os.path.join(HERE, 'pool', 'ang', p + '.txt'), encoding='utf-8').read().split()[:n]
    items.append((p, h, a))
rng.shuffle(items)
codes = [f'X{i:02d}' for i in range(1, len(items) + 1)]
for layer in ('hist', 'ang'): os.makedirs(os.path.join(HERE, 'blind', layer), exist_ok=True)
os.makedirs(os.path.join(HERE, 'schluessel'), exist_ok=True)
key = {'erstellt': datetime.datetime.now().isoformat(timespec='seconds'), 'woerter': n,
       'salz': secrets.token_hex(32), 'zuordnung': {}}
for c, (src, h, a) in zip(codes, items):
    open(os.path.join(HERE, 'blind', 'hist', c + '.txt'), 'w', encoding='utf-8').write(' '.join(h) + '\n')
    open(os.path.join(HERE, 'blind', 'ang', c + '.txt'), 'w', encoding='utf-8').write(' '.join(a) + '\n')
    key['zuordnung'][c] = src
kp = os.path.join(HERE, 'schluessel', 'schluessel.json')
data = json.dumps(key, ensure_ascii=False, indent=1).encode('utf-8')
open(kp, 'wb').write(data)
print('Wörter je Text:', n)
print('Codes:', ', '.join(codes))
print('SHA-256 der Schlüsseldatei:', hashlib.sha256(data).hexdigest())
