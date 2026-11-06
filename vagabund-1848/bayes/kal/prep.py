"""Datenaufbereitung für Kalibrierung und Verblindung (Protokoll II.3, Stichtag 16.10.2026)."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, glob, os, csv, random, unicodedata
S = str(pfade.ARBEIT)
HIST = {'korpus': str(pfade.KORPUS), 'bdl': S+'/out/Heine_Buch_der_Lieder_1827_restituiert.txt', 'a2': S+'/out/A2/Gedichte'}
ANG  = {'korpus': S+'/norm/out/korpus', 'bdl': S+'/norm/out/korpus/Heine_Buch_der_Lieder_1827_restituiert_ang.txt', 'a2': S+'/norm/out/A2/Gedichte'}
NUMERAL = re.compile(r'^\s*([IVXLC]+|\d+)\s*\.?\s*$')

def clean(text):
    """Präzisierung (vermerkt): Zeilen, die nur aus einer Zahl bestehen, entfallen."""
    text = unicodedata.normalize('NFC', text)
    return '\n'.join(l for l in text.split('\n') if not NUMERAL.match(l))

def toks(text):
    return clean(text).split()

def kf(layer, name):
    d = HIST if layer == 'hist' else ANG
    return os.path.join(d['korpus'], name + ('.txt' if layer == 'hist' else '_ang.txt'))

CLASSES = {  # Klasse -> Dateien in corpus_diplomatisch (Reihenfolge = Probenfolge)
    'B1': ['Hektor_Vagabund'],
    'B2': ['Hektor_Schilda'],
    'C1': ['Steinmann_Lieder'],
    'C2': ['Geibel_Junius', 'Geibel_Lieder', 'Geibel_Buecher'],
    'C3': ['Mueller_1', 'Mueller_2', 'Wunderhorn_1806'],
}
SECT = ['Junge Leiden.','Traumbilder.','Lieder.','Romanzen.','Sonette.','Lyrisches Intermezzo.','Die Heimkehr.','Aus der Harzreise.','Die Nordsee.','Erster Cyklus.','Zweiter Cyklus.']
LIED = {'Lieder', 'Lyrisches Intermezzo', 'Die Heimkehr'}
NORD = {'Erster Cyklus', 'Zweiter Cyklus'}

def bdl_poems(layer):
    """Buch der Lieder 1827 in Gedichte zerlegt: Liste (Abschnitt, Nummer, Text)."""
    p = HIST['bdl'] if layer == 'hist' else ANG['bdl']
    poems = []; sec = ''; num = ''; buf = []; stop = False
    def flush():
        if buf and sec and num and not stop: poems.append((sec, num, '\n'.join(buf)))
    for l in open(p, encoding='utf-8').read().split('\n'):
        t = l.strip()
        if t in SECT:
            flush(); buf = []; sec = t.rstrip('.'); num = ''; stop = False; continue
        if sec == 'Die Heimkehr' and t == 'Götterdämmerung.':
            flush(); buf = []; stop = True; continue
        if re.fullmatch(r'[IVXLC]+\.', t):
            flush(); buf = []; num = t; continue
        if num: buf.append(l)
    flush()
    return poems

def a2_poems(layer):
    d = HIST['a2'] if layer == 'hist' else ANG['a2']
    return [(os.path.basename(f)[:-4], open(f, encoding='utf-8').read()) for f in sorted(glob.glob(d + '/*.txt'))]

def a2_mapping():
    """A2-Gedicht-ID -> Entsprechung im Buch der Lieder ('Lyrisches Intermezzo XII.')"""
    m = {}
    for r in csv.DictReader(open(S + '/out/A2/A2_Manifest.csv', encoding='utf-8'), delimiter=';'):
        if r['ID']: m[r['ID']] = r['Entsprechung im Buch der Lieder 1827'].strip()
    return m

def stream(layer, cls):
    out = []
    for n in CLASSES[cls]:
        out += [(w, n) for w in toks(open(kf(layer, n), encoding='utf-8').read())]
    return out

def a2_stream(layer):
    out = []
    for pid, t in a2_poems(layer):
        out += [(w, pid) for w in toks(t)]
    return out

def blocks(stream, size):
    return [stream[i*size:(i+1)*size] for i in range(len(stream)//size)]

# Täuschungsblöcke (Verblindung): fest gewählt vor jeder Rechnung, Startwert 20261016.
POOL_SPEC = [('A2', 3), ('C2', 3), ('C3', 3), ('B2', 1)]
def decoy_pool():
    rng = random.Random(20261016)
    pool = []
    for cls, k in POOL_SPEC:
        n = len(blocks(a2_stream('ang') if cls == 'A2' else stream('ang', cls), 548))
        for i in sorted(rng.sample(range(n), k)): pool.append((cls, i))
    return pool
