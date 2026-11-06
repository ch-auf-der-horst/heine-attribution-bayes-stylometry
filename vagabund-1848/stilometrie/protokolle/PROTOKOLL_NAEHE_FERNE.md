# Protokoll der Nähe- und Ferne-Prüfung

Stand der Festlegung: 16. Oktober 2026, vor dem Lauf. Die Zahlen stehen danach in `ergebnisse/naehe_ferne/BERICHT.md` und werden nicht in dieses Protokoll zurückgeschrieben. Diese Prüfung ersetzt Studie 1 bis 6 nicht und ändert die Prüfung gleicher Proben nicht.

## Frage

Liegt der Kandidat den frühen strophischen Heine-Liedern näher als Schilda, den Vagabunden-Liedern, Müller und Steinmann? Die Frage lautet auf Nähe oder Ferne. Sie lautet nicht auf Verfasserschaft.

## Proben

Länge 351 Wörter. Versatz 0. Eine Probe überschreitet keine Textgrenze. Nichts wird aneinandergehängt. Die Dateien werden nicht gedehnt.

Texte: Aurora, Biene, Almanach, Agrippina, Heimkehr, Kevlaar, Donna Clara, Schilda, die Vagabunden-Lieder, Müller Teil 1 und `Steinmann_Lieder.txt`. Uhland, das Wunderhorn und die Juniuslieder bleiben draußen. Sonette, Balladen, Müller Teil 2 und der Ganztext von Schilda bleiben draußen.

Der Kandidat hat 548 Wörter. Entschieden wird mit den ersten 351. Die letzten 351 werden in denselben Ziehungen mitgerechnet und entscheiden nicht. Die beiden Fenster überlappen.

## Ziehung

500-mal wird aus jedem bekannten Text genau eine seiner Proben gezogen. Texte mit nur einer Probe geben immer diese, und für sie wird keine Zufallszahl verbraucht. Der Zufallsstrom ist `SeedSequence([20261013, 10])`. Gezogen wird in der festen Reihenfolge Aurora, Agrippina, Heimkehr, Schilda, Vagabund, Müller. Biene, Almanach, Kevlaar, Donna Clara und Steinmann haben nur eine Probe.

Die 150 häufigsten Wörter und die 500 häufigsten Vierergruppen werden in jedem Durchgang nur aus den elf gezogenen Proben gezählt. Der Kandidat wählt keine Merkmale. Mittel und Streuung kommen aus diesen elf Proben, jeder Text einmal. Der Kandidat geht darin nicht ein. Der Abstand ist Cosine Delta.

## Leseregel

In einem Durchgang und auf einem Maß liegt Heine näher, wenn die nächsten Heine-Probe einen kleineren Abstand hat als Schilda, als die Vagabunden-Lieder, als Müller und als Steinmann. Fern liegt der Kandidat, wenn einer dieser vier Texte jeder Heine-Probe näher liegt. Gleiche Abstände zählen weder als nah noch als fern. Verglichen werden die unverrundeten Abstände.

Heine-nah ist der Ausgang nur, wenn der Anteil der näheren Heine-Proben auf beiden Maßen mindestens die Hälfte ist und der Anteil der ferneren Durchgänge auf beiden Maßen unter der Hälfte bleibt. Heine-fern ist der Ausgang nur, wenn der Anteil der ferneren Durchgänge auf beiden Maßen mindestens die Hälfte ist und der Anteil der näheren Heine-Proben auf beiden Maßen unter der Hälfte bleibt. Jeder andere Ausgang ist unentschieden. Liegt ein Maß genau auf der Hälfte, bleibt der Ausgang unentschieden.

Welcher Heine-Text am häufigsten der nächste ist, welcher der vier Vergleichstexte am häufigsten näher liegt und wie groß der Abstand im Median ist, wird berichtet und entscheidet nicht. Die letzten 351 Wörter entscheiden nicht.

## Aufruf

Vom Projektordner aus:

    python3 analyse/15_naehe_ferne.py

Der Ordner `ergebnisse/naehe_ferne/` wird angelegt und nicht überschrieben. `AUTOR_NEUZEICHNEN=1` schreibt ihn neu.
