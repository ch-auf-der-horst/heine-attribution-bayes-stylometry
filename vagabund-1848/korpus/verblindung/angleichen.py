#!/usr/bin/env python3
"""Angleichung der Schreibung nach Protokoll II.3, Punkt 5 (Stichtag 16.10.2026).

Feste Regelliste, für alle Korpora gleich. Vers, Zeilen, Satzzeichen und alle
übrigen Wortformen bleiben unverändert.

  R1  th -> t          (außer geschützten Wörtern und Kompositionsfugen t|h)
  R2  ey -> ei         (außer geschützten Namen)
  R3  aͤ oͤ uͤ -> ä ö ü ; Ae/Oe/Ue am Wortanfang vor Kleinbuchstaben -> Ä/Ö/Ü
  R4  Apostrophe ’ ‘ ´ ` -> '
  R5  Anführungszeichen „ “ ” » « ‚ › ‹ " -> "
  R6  Gedankenstrich – -> —
  (ſ -> s, falls vorhanden)

Aufruf:  python3 angleichen.py EINGABE.txt AUSGABE.txt [protokoll.csv]
"""
import re, sys, csv, unicodedata, collections

# R1: Wörter, deren th erhalten bleibt (Fremdwörter, Namen, heute noch mit th)
TH_ANFANG = ['thron', 'theater', 'thema', 'themist', 'theorb', 'thyrs', 'theben', 'tharau', 'thetis',
             'thalatta', 'theolog', 'theodor', 'thüring', 'athen', 'arthur', 'bertha', 'martha', 'mathild',
             'nathan', 'esther', 'elisabeth', 'margreth', 'matthi', 'timothe', 'jephtha', 'erichthon',
             'kallisthen', 'aperanthos', 'bagiratha', 'neithard', 'göthe', 'goethe', 'lethe', 'golgatha',
             'äther', 'aether', 'lothring', 'bethlehem', 'theresia', 'walther', 'elsbeth', 'käth', 'seither']
TH_INNEN = ['thron', 'theater', 'kathed', 'cathedr', 'method', 'myth', 'pantheon', 'marathon', 'ästhet',
            'aesthet', 'rhythm', 'labyrinth', 'hyacinth', 'iazinth', 'panther', 'zither', 'cither', 'zebaoth', 'kathol', 'apothek', 'sympath', 'enthusias', 'mathem']
# R1: Kompositionsfuge t|h (z. B. Gast|hof, Gott|heit): th vor diesen Wortteilen bleibt
TH_FUGE = re.compile(r'th(?=(aus|äus|of|öf|orn|örn|and|auch|eit|emd|aft|eft|err|in))|(?<=^en)th|(?<=^unen)th', re.I)
EY_SCHUTZ = ['meyer']

WORT = re.compile(r"[A-Za-zÄÖÜäöüßſ]+")
log = collections.Counter()

def r1(w):
    lw = w.lower()
    if 'th' not in lw or lw.startswith(tuple(TH_ANFANG)) or any(s in lw for s in TH_INNEN):
        return w
    out = []; i = 0
    while i < len(w):
        if w[i:i+2].lower() == 'th' and not TH_FUGE.match(w, i):
            out.append(w[i]); i += 2      # 't' bzw. 'T' bleibt, 'h' entfällt
        else:
            out.append(w[i]); i += 1
    return ''.join(out)

def r2(w):
    lw = w.lower()
    if 'ey' not in lw or any(s in lw for s in EY_SCHUTZ):
        return w
    return re.sub('ey', 'ei', re.sub('Ey', 'Ei', re.sub('EY', 'EI', w)))

def r3(w):
    w2 = re.sub(r'^Ae(?=[a-zäöüß])', 'Ä', w)
    w2 = re.sub(r'^Oe(?=[a-zäöüß])', 'Ö', w2)
    w2 = re.sub(r'^Ue(?=[a-zäöüß])', 'Ü', w2)
    return w2

def wort(m):
    w0 = m.group(0); w = w0.replace('ſ', 's')
    for name, f in (('R1 th', r1), ('R2 ey', r2), ('R3 Ae', r3)):
        w1 = f(w)
        if w1 != w:
            log[(name, w, w1)] += 1
            w = w1
    return w

def angleichen(text):
    text = unicodedata.normalize('NFC', text)
    for a, b in (('aͤ', 'ä'), ('oͤ', 'ö'), ('uͤ', 'ü'), ('Aͤ', 'Ä'), ('Oͤ', 'Ö'), ('Uͤ', 'Ü')):
        n = text.count(a)
        if n: log[('R3 e-Überstrich', a, b)] += n; text = text.replace(a, b)
    text = WORT.sub(wort, text)
    for chars, ziel, name in (("’‘´`", "'", 'R4 Apostroph'), ('„“”»«‚›‹"', '"', 'R5 Anführung'), ('–', '—', 'R6 Strich')):
        for c in chars:
            n = text.count(c)
            if n and c != ziel:
                log[(name, c, ziel)] += n; text = text.replace(c, ziel)
    return text

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    t = open(src, encoding='utf-8').read()
    open(dst, 'w', encoding='utf-8').write(angleichen(t))
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=';'); w.writerow(['Regel', 'vorher', 'nachher', 'Anzahl'])
            for (r, a, b), n in sorted(log.items()): w.writerow([r, a, b, n])
