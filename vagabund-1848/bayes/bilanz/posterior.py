"""Ausgangswahrscheinlichkeit (Abschnitt 5.3), Posterior (Abschnitt 8.2) und Sensitivität (Tab. 5).
Formel (Abschnitt 5.2): P(H1) = 1 / (1 + r*10^-a + r*10^-b), r = n/2 bei Ausgangschance 1:n;
a, b = Summen der log10-Punkte gegenüber H2 (Hektor) und H3 (Nachahmer), aus befunde.csv."""
import csv, os

HIER = os.path.dirname(os.path.abspath(__file__))

def summen(spalte_h2, spalte_h3, ohne=()):
    a = b = 0.0
    with open(os.path.join(HIER, 'befunde.csv'), encoding='utf-8') as f:
        for z in csv.DictReader(f, delimiter=';'):
            if z['befund'] in ohne: continue
            a += float(z[spalte_h2] or 0); b += float(z[spalte_h3] or 0)
    return round(a, 2), round(b, 2)

def laplace(k, u):
    """Anteil echter Fälle (k + 1) / (k + u + 2); Rückgabe n der Chance 1:n."""
    p = (k + 1) / (k + u + 2); return (1 - p) / p

def P(n, a, b, anteil_h3=0.5):
    return 1 / (1 + n * (1 - anteil_h3) * 10 ** -a + n * anteil_h3 * 10 ** -b)

if __name__ == '__main__':
    n_ohne_offene, n_offen_halb, n_offen_unecht = laplace(0, 4), laplace(1, 5), laplace(0, 6)
    print(f'Referenzklasse: 1:{n_ohne_offene:g} bis 1:{n_offen_halb:g}; offene Fälle als unecht: 1:{n_offen_unecht:g}')
    a, b = summen('gegen_H2_ausgewogen', 'gegen_H3_ausgewogen')
    sa, sb = summen('gegen_H2_skeptisch', 'gegen_H3_skeptisch')
    print(f'Summen ausgewogen a = {a:+.2f}, b = {b:+.2f}; skeptisch a = {sa:+.2f}, b = {sb:+.2f}')
    zeilen = [
        ('Hauptwertung (Referenzklasse, ausgewogen)', [5, 3], a, b, 0.5),
        ('Zagreber Gedicht offen statt unecht', [4, 2.2], a, b, 0.5),
        ('Offene Fälle als unecht gezählt', [7], a, b, 0.5),
        ('Gesamte Gegenmasse bei einem Nachahmer', [5, 3], a, b, 1.0),
        ('Glättungswert der Zeichen-4-Gramme neutral', [5, 3], a, b - 0.33 + 0.18, 0.5),
        ('Warnebold-Befund gegenüber H3 neutral', [5, 3], a, b - 0.25, 0.5),
        ('Nur philologische Befunde', [5, 3], a - 0.5, b - 0.33, 0.5),
        ('Skeptische Wertung', [7], sa, sb, 0.5),
        ('Skeptische Wertung, Steinmann als Untergrenze', [20, 7], sa, sb, 0.5),
    ]
    for name, ns, x, y, s3 in zeilen:
        werte = ' bis '.join(f'{P(n, x, y, s3):.0%}' for n in ns)
        print(f'{name}: {werte}')
