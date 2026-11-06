# Protokoll der Prüfung mit dem Buch der Lieder 1827

Stand der Festlegung: 16. Oktober 2026, vor dem Lauf. Die Zahlen stehen danach in `ergebnisse/bdl1827/BERICHT.md` und werden nicht in dieses Protokoll zurückgeschrieben. Dieser Lauf ersetzt die Studien 1 bis 6 und die Nähe-Prüfungen mit den sieben einzelnen Heine-Texten nicht.

## Frage

Liegt der Kandidat einer Probe aus `Heine/Heine_Buch_der_Lieder_1827_restituiert.txt` näher als Müller, dem Wunderhorn, Schilda, den Vagabunden-Liedern und Steinmann? Die Frage lautet auf Nähe oder Ferne zu diesem Band. Sie lautet nicht auf Verfasserschaft.

Steinmann wird daneben als Fälschungsprobe gelesen und entscheidet die Frage des Kandidaten nicht.

## Datei des Bandes

Der Heine-Text ist diese eine Datei, nicht die sieben frühen Lieder. Sie behält Verszeile, Satzzeichen und historische Schreibung. Gezählt wird jedes durch Leerraum getrennte Wort, auch Jahreszeilen und Widmungen, weil sie in der Datei stehen.

Der Band enthält Traumbilder, Lieder, Romanzen, Sonette, die Heimkehr, die Harzreise und die Nordsee. Eine Probe kann in jeden dieser Teile fallen. Welcher Teil gezogen wurde, wird berichtet und entscheidet nicht. Nichts wird aus der Datei gestrichen.

## Proben

Länge 351 Wörter. Versatz 0. Eine Probe überschreitet keine Textgrenze. Nichts wird aneinandergehängt. Kurze Dateien werden nicht gedehnt.

Verglichen werden: der Band, `Mueller_1.txt`, `Wunderhorn_1806.txt`, `Hektor_Schilda.txt`, `Hektor_Vagabund.txt`, `Steinmann_Lieder.txt` und `Kandidat_Vagabund.txt`. Das Wunderhorn bleibt die anonyme Sammlung. Schilda sind die strophischen Lieder, nicht die Knittelverse. Steinmann sind die Strophenlieder der Datei, nicht die Sonette.

Der Kandidat hat 548 Wörter. Entschieden wird mit den ersten 351. Die letzten 351 werden in denselben Ziehungen mitgerechnet und entscheiden nicht. Steinmann hat 492 Wörter und gibt nur die ersten 351. Die übrigen Wörter bleiben liegen.

## Ziehung

500-mal wird aus dem Band, aus Müller, dem Wunderhorn, Schilda und den Vagabunden-Liedern genau eine Probe gezogen. Der Zufallsstrom ist `SeedSequence([20261013, 13])`. Gezogen wird in dieser Reihenfolge. Steinmann und der Kandidat haben nur ein Fenster und verbrauchen keine Zufallszahl.

Die 150 häufigsten Wörter und die 500 häufigsten Vierergruppen werden nur aus diesen fünf gezogenen Proben gezählt. Steinmann und der Kandidat wählen keine Merkmale. Mittel und Streuung kommen aus diesen fünf Proben. Der Abstand ist Cosine Delta.

## Leseregel

In einem Durchgang und auf einem Maß liegt der Band näher, wenn seine Probe einen kleineren Abstand hat als Müller, als das Wunderhorn, als Schilda, als die Vagabunden-Lieder und als Steinmann. Fern liegt der Kandidat, wenn einer dieser fünf Texte der Bandprobe näher liegt. Gleiche Abstände zählen weder als nah noch als fern. Verglichen werden die unverrundeten Abstände.

Heine-nah ist der Ausgang nur, wenn der Anteil der näheren Bandproben auf beiden Maßen mindestens die Hälfte ist und der Anteil der ferneren Durchgänge auf beiden Maßen unter der Hälfte bleibt. Heine-fern ist der Ausgang nur, wenn der Anteil der ferneren Durchgänge auf beiden Maßen mindestens die Hälfte ist und der Anteil der näheren Bandproben auf beiden Maßen unter der Hälfte bleibt. Jeder andere Ausgang ist unentschieden.

Für Steinmann gilt dieselbe Hälfte, aber ohne ihn selbst unter den Vergleichstexten. Bei Steinmann heißt die Nähe, dass die Bandprobe näher liegt als Müller, das Wunderhorn, Schilda und die Vagabunden-Lieder. Dieser Ausgang entscheidet den Kandidaten nicht. Die letzten 351 Wörter des Kandidaten entscheiden nicht. Der Teil des Bandes, aus dem die Probe stammt, entscheidet nicht.

## Aufruf

Vom Projektordner aus:

    python3 analyse/18_bdl1827.py

Der Ordner `ergebnisse/bdl1827/` wird angelegt und nicht überschrieben. `AUTOR_NEUZEICHNEN=1` schreibt ihn neu.
