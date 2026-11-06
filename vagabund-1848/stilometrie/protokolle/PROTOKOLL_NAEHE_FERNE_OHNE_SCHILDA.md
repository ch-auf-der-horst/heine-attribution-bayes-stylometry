# Protokoll der Nähe- und Ferne-Prüfung ohne Schilda

Stand der Festlegung: 16. Oktober 2026, vor dem Lauf. Die Zahlen stehen danach in `ergebnisse/naehe_ferne_ohne_schilda/BERICHT.md` und werden nicht in dieses Protokoll zurückgeschrieben. Dieser Lauf ersetzt die Prüfung mit Schilda nicht und ersetzt Studie 1 bis 6 nicht.

## Anlass

Schilda wird auf Wunsch aus dem Vergleich genommen. Die Datei `Hektor_Schilda.txt` enthält die strophischen Schilda-Lieder, nicht die Knittelverse. Die Knittelverse stehen in `Hektor_Knittel.txt` und waren in der Nähe- und Ferne-Prüfung schon nicht enthalten. Der Lauf prüft die engere Vergleichsgruppe. Er berichtigt keine falsch einsortierte Versart.

## Frage

Liegt der Kandidat den frühen strophischen Heine-Liedern näher als den Vagabunden-Liedern, Müller und Steinmann? Die Frage lautet auf Nähe oder Ferne. Sie lautet nicht auf Verfasserschaft.

## Proben

Länge 351 Wörter. Versatz 0. Eine Probe überschreitet keine Textgrenze. Nichts wird aneinandergehängt. Die Dateien werden nicht gedehnt.

Texte: Aurora, Biene, Almanach, Agrippina, Heimkehr, Kevlaar, Donna Clara, die Vagabunden-Lieder, Müller Teil 1 und `Steinmann_Lieder.txt`. Schilda, Uhland, das Wunderhorn und die Juniuslieder bleiben draußen. Sonette, Balladen, Müller Teil 2, die Knittelverse und der Ganztext von Schilda bleiben draußen.

Der Kandidat hat 548 Wörter. Entschieden wird mit den ersten 351. Die letzten 351 werden in denselben Ziehungen mitgerechnet und entscheiden nicht. Die beiden Fenster überlappen.

## Ziehung

500-mal wird aus jedem bekannten Text genau eine seiner Proben gezogen. Texte mit nur einer Probe geben immer diese, und für sie wird keine Zufallszahl verbraucht. Der Zufallsstrom ist `SeedSequence([20261013, 11])`. Gezogen wird in der festen Reihenfolge Aurora, Agrippina, Heimkehr, Vagabund, Müller. Biene, Almanach, Kevlaar, Donna Clara und Steinmann haben nur eine Probe.

Die 150 häufigsten Wörter und die 500 häufigsten Vierergruppen werden in jedem Durchgang nur aus den zehn gezogenen Proben gezählt. Schilda und der Kandidat wählen keine Merkmale. Mittel und Streuung kommen aus diesen zehn Proben, jeder Text einmal. Der Kandidat geht darin nicht ein. Der Abstand ist Cosine Delta.

## Leseregel

In einem Durchgang und auf einem Maß liegt Heine näher, wenn die nächste Heine-Probe einen kleineren Abstand hat als die Vagabunden-Lieder, als Müller und als Steinmann. Fern liegt der Kandidat, wenn einer dieser drei Texte jeder Heine-Probe näher liegt. Gleiche Abstände zählen weder als nah noch als fern. Verglichen werden die unverrundeten Abstände.

Heine-nah ist der Ausgang nur, wenn der Anteil der näheren Heine-Proben auf beiden Maßen mindestens die Hälfte ist und der Anteil der ferneren Durchgänge auf beiden Maßen unter der Hälfte bleibt. Heine-fern ist der Ausgang nur, wenn der Anteil der ferneren Durchgänge auf beiden Maßen mindestens die Hälfte ist und der Anteil der näheren Heine-Proben auf beiden Maßen unter der Hälfte bleibt. Jeder andere Ausgang ist unentschieden. Liegt ein Maß genau auf der Hälfte, bleibt der Ausgang unentschieden.

Welcher Heine-Text am häufigsten der nächste ist, welcher der drei Vergleichstexte am häufigsten näher liegt und wie groß der Abstand im Median ist, wird berichtet und entscheidet nicht. Die letzten 351 Wörter entscheiden nicht. Die Abbildungen entscheiden nicht.

## Aufruf

Vom Projektordner aus:

    python3 analyse/16_naehe_ferne_ohne_schilda.py

Der Ordner `ergebnisse/naehe_ferne_ohne_schilda/` wird angelegt und nicht überschrieben. `AUTOR_NEUZEICHNEN=1` schreibt ihn neu.
