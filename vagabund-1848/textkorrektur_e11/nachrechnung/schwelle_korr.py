"""Schwellenrechnung (Abschnitt 8.3): Um wie viele log10-Punkte müssten die
philologischen Summen sinken, damit P(H1) unter einen Zielwert fällt?
Stilometrische Werte unverändert; gleiche Verschiebung gegen H2 und H3."""
from scipy.optimize import brentq

def p_heine(a, b, n):
    r = n / 2
    return 1 / (1 + r * 10 ** -a + r * 10 ** -b)

A, B = 1.5, 0.53          # ausgewogene Summen gegen H2 / H3
for n in (5, 3):          # Ausgangschance 1:n
    for ziel in (0.5, 0.25, 0.1):
        d = brentq(lambda d: p_heine(A + d, B + d, n) - ziel, -5, 5)
        print(f"1:{n}  Ziel {ziel:.0%}: Verschiebung {d:+.2f} Punkte (Faktor {10**-d:.1f})")
