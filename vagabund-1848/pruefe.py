"""Automatische Prüfung des öffentlichen Stands (Fall vagabund-1848).

Prüft ohne die nicht veröffentlichten Heine-Texte:
1. die Prüfsummen aller Dateien nach ../MANIFEST.sha256,
2. dass alle CSV-Dateien je Zeile gleich viele Felder und alle JSON-Dateien gültiges JSON haben,
3. die sechs öffentlich nachrechenbaren Skripte und ihre erwarteten Ergebnisse (in einer Wegwerfkopie).

Aufruf aus dem Wurzelordner des Repositoriums oder aus diesem Ordner:  python vagabund-1848/pruefe.py
Rückgabewert 0 = alles bestanden.
"""
import collections, csv, glob, hashlib, json, os, shutil, subprocess, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(HIER)
fehler = []


def melde(ok, text):
    print(('OK    ' if ok else 'FEHLER') + '  ' + text)
    if not ok:
        fehler.append(text)


# 1. Prüfsummen
n = 0
for zeile in open(os.path.join(WURZEL, 'MANIFEST.sha256'), encoding='utf-8'):
    h, pfad = zeile.rstrip('\n').split('  ', 1)
    p = os.path.join(WURZEL, pfad)
    if not os.path.isfile(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != h:
        melde(False, f'Prüfsumme: {pfad}')
    n += 1
melde(not any(f.startswith('Prüfsumme') for f in fehler), f'Prüfsummen ({n} Dateien)')

# 2. CSV- und JSON-Dateien
for f in sorted(glob.glob(os.path.join(WURZEL, '**', '*.csv'), recursive=True)):
    txt = open(f, encoding='utf-8').read()
    kopf = txt.split('\n', 1)[0]
    trenner = max([';', ',', '\t'], key=kopf.count)
    laengen = {len(r) for r in csv.reader(txt.splitlines(), delimiter=trenner) if r}
    if len(laengen) != 1:
        melde(False, f'CSV-Struktur: {os.path.relpath(f, WURZEL)} {sorted(laengen)}')
jfehl = []
for f in glob.glob(os.path.join(WURZEL, '**', '*.json'), recursive=True):
    try:
        json.load(open(f, encoding='utf-8'))
    except ValueError:
        jfehl.append(os.path.relpath(f, WURZEL))
melde(not jfehl, 'JSON-Dateien gültig' + (': ' + ', '.join(jfehl) if jfehl else ''))
melde(not any(f.startswith('CSV') for f in fehler), 'CSV-Dateien mit einheitlicher Feldzahl')

# 3. Öffentliche Skripte in einer Wegwerfkopie
ERWARTET = {
    'bayes/bilanz/posterior.py': ['Hauptwertung (Referenzklasse, ausgewogen): 55% bis 67%',
                                  'Warnebold-Befund gegenüber H3 neutral: 42% bis 55%',
                                  'Skeptische Wertung, Steinmann als Untergrenze: 7% bis 17%'],
    'bayes/bilanz/schwelle.py': ['1:3  Ziel 10%: Verschiebung -1.26 Punkte (Faktor 18.4)'],
    'textkorrektur_e11/nachrechnung/tab5_warnebold_neutral.py': ['Warnebold-Befund neutral: 42% bis 55%'],
    'textkorrektur_e11/nachrechnung/abb1_EN.py': ['ok'],
    'textkorrektur_e11/nachrechnung/abb2_EN.py': ['ok'],
    'textkorrektur_e11/nachrechnung/tippett_EN.py': ["Cllr {'w': 0.78, 'c': 0.793}"],
}
DATEIEN = ['textkorrektur_e11/nachrechnung/abb/Fig1_Heine-likeness_imitators_EN.pdf',
           'textkorrektur_e11/nachrechnung/abb/Fig2_Prior_Posterior_EN.pdf',
           'textkorrektur_e11/nachrechnung/abb/Tippett_Repositorium.pdf']
with tempfile.TemporaryDirectory() as tmp:
    kopie = os.path.join(tmp, 'vagabund-1848')
    shutil.copytree(HIER, kopie)
    umgebung = dict(os.environ, MPLBACKEND='Agg', PYTHONDONTWRITEBYTECODE='1')
    for skript, zeilen in ERWARTET.items():
        r = subprocess.run([sys.executable, skript], cwd=kopie, capture_output=True, text=True, env=umgebung)
        fehlt = [z for z in zeilen if z not in r.stdout]
        melde(r.returncode == 0 and not fehlt, f'{skript}' + (f' (fehlt: {fehlt}; {r.stderr.strip()[-200:]})' if fehlt or r.returncode else ''))
    for d in DATEIEN:
        melde(os.path.isfile(os.path.join(kopie, d)), f'erzeugt: {d}')

print()
print('Alle Prüfungen bestanden.' if not fehler else f'{len(fehler)} Prüfung(en) nicht bestanden.')
sys.exit(1 if fehler else 0)
