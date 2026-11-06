"""Tab. 5, Zeile 'Warnebold-Befund gegenüber H3 neutral' (2.11.2026).
Formel aus Abschnitt 5.2: P(H1) = 1 / (1 + r*10^-a + r*10^-b), r = n/2.
Hauptwertung: a = 1,5; b = 0,53 (davon +0,25 Warnebold-Befund). Neutral: b = 0,28.
Keine neue Analyse, nur Einsetzen in die bestehende Formel."""
P = lambda n, a, b: 1 / (1 + n / 2 * 10 ** -a + n / 2 * 10 ** -b)
for lab, b in [('Hauptwertung', 0.53), ('Warnebold-Befund neutral', 0.28), ('Zeichen-4-Gramme neutral (Kontrolle)', 0.38)]:
    print(f'{lab}: {P(5, 1.5, b):.0%} bis {P(3, 1.5, b):.0%}')
