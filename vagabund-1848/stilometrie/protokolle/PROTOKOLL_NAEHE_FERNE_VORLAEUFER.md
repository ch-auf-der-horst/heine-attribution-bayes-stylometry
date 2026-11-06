# Protokoll der Nähe- und Ferne-Prüfung mit Uhland und dem Wunderhorn

Stand der Festlegung: 16. Oktober 2026, vor dem Lauf. Die Zahlen stehen danach in `ergebnisse/naehe_ferne_vorlaeufer/BERICHT.md` und werden nicht in dieses Protokoll zurückgeschrieben. Dieser Lauf ersetzt die Prüfung in `ergebnisse/naehe_ferne/` nicht und ersetzt Studie 1 bis 6 nicht.

## Frage

Liegt der Kandidat den frühen strophischen Heine-Liedern näher als Schilda, den Vagabunden-Liedern, Müller, Steinmann, Uhlands Liedern und dem Wunderhorn? Die Frage lautet auf Nähe oder Ferne. Sie lautet nicht auf Verfasserschaft. Uhland und das Wunderhorn stehen hier neben Müller als Vergleich, nicht auf der Seite Heines.

## Proben

Länge 351 Wörter. Versatz 0. Eine Probe überschreitet keine Textgrenze. Nichts wird aneinandergehängt. Die Dateien werden nicht gedehnt.

Texte: Aurora, Biene, Almanach, Agrippina, Heimkehr, Kevlaar, Donna Clara, Schilda, die Vagabunden-Lieder, Müller Teil 1, `Steinmann_Lieder.txt`, `Uhland_Lieder.txt` und `Wunderhorn_1806.txt`. Das Wunderhorn bleibt die anonyme Sammlung von 1806 und wird nicht Arnim oder Brentano zugeschrieben. Uhlands Balladen bleiben draußen.

Der Kandidat hat 548 Wörter. Entschieden wird mit den ersten 351. Die letzten 351 werden in denselben Ziehungen mitgerechnet und entscheiden nicht. Die beiden Fenster überlappen.

## Ziehung

500-mal wird aus jedem bekannten Text genau eine seiner Proben gezogen. Texte mit nur einer Probe geben immer diese, und für sie wird keine Zufallszahl verbraucht. Der Zufallsstrom ist `SeedSequence([20261013, 12])`. Gezogen wird in der festen Reihenfolge Aurora, Agrippina, Heimkehr, Schilda, Vagabund, Müller, Uhland, Wunderhorn. Biene, Almanach, Kevlaar, Donna Clara und Steinmann haben nur eine Probe.

Die 150 häufigsten Wörter und die 500 häufigsten Vierergruppen werden in jedem Durchgang nur aus den dreizehn gezogenen Proben gezählt. Der Kandidat wählt keine Merkmale. Mittel und Streuung kommen aus diesen dreizehn Proben, jeder Text einmal. Der Kandidat geht darin nicht ein. Der Abstand ist Cosine Delta.

## Leseregel

In einem Durchgang und auf einem Maß liegt Heine näher, wenn die nächste Heine-Probe einen kleineren Abstand hat als Schilda, als die Vagabunden-Lieder, als Müller, als Steinmann, als Uhland und als das Wunderhorn. Fern liegt der Kandidat, wenn einer dieser sechs Texte jeder Heine-Probe näher liegt. Gleiche Abstände zählen weder als nah noch als fern. Verglichen werden die unverrundeten Abstände.

Heine-nah ist der Ausgang nur, wenn der Anteil der näheren Heine-Proben auf beiden Maßen mindestens die Hälfte ist und der Anteil der ferneren Durchgänge auf beiden Maßen unter der Hälfte bleibt. Heine-fern ist der Ausgang nur, wenn der Anteil der ferneren Durchgänge auf beiden Maßen mindestens die Hälfte ist und der Anteil der näheren Heine-Proben auf beiden Maßen unter der Hälfte bleibt. Jeder andere Ausgang ist unentschieden. Liegt ein Maß genau auf der Hälfte, bleibt der Ausgang unentschieden.

Welcher Heine-Text am häufigsten der nächste ist, welcher der sechs Vergleichstexte am häufigsten näher liegt und wie groß der Abstand im Median ist, wird berichtet und entscheidet nicht. Die letzten 351 Wörter entscheiden nicht. Die Abbildungen entscheiden nicht.

## Aufruf

Vom Projektordner aus:

    python3 analyse/17_naehe_ferne_vorlaeufer.py

Der Ordner `ergebnisse/naehe_ferne_vorlaeufer/` wird angelegt und nicht überschrieben. `AUTOR_NEUZEICHNEN=1` schreibt ihn neu.
