# Protokoll der Prüfung gleicher Proben

Stand der Festlegung: 15. Oktober 2026, vor dem Lauf. Die Zahlen stehen danach in `ergebnisse/gleiche_proben/BERICHT.md` und werden nicht in dieses Protokoll zurückgeschrieben. Diese Prüfung ersetzt Studie 1 bis 6 nicht und ändert ihre Schwellen nicht.

## Frage

Die Bäume der Studien 4 bis 6 setzen jeden Text als ein Blatt. Das Blatt eines langen Textes ist der Mittelwert vieler Proben, das Blatt eines kurzen Textes ist eine einzelne Probe. Ein kurzes Blatt kann deshalb bei anderen kurzen Blättern stehen, weil beide verrauscht sind. Dasselbe gilt für den Profilbaum der Studien 1 bis 3, in dem der Kandidat neben den Mittelwerten der Klassen steht. Die Eichbäume der Studien 1 bis 3 tun das nicht: dort ist jede der elf Heine-Proben und jede der elf Schilda-Proben ein eigenes Blatt.

Diese Prüfung fragt, ob sich die Verfasser noch trennen, wenn dieser Unterschied entfällt.

## Proben

Länge 351 Wörter. Versatz 0. Eine Probe überschreitet keine Textgrenze. Nichts wird aneinandergehängt. 548 Wörter tragen Steinmann und mehrere Heine-Texte nicht; diese Länge wird nicht verwendet und die kurzen Dateien werden nicht gedehnt.

Texte: die sieben frühen Heine-Texte, Schilda, die Vagabunden-Lieder, Müller Teil 1, das Wunderhorn, Uhlands Lieder, die Juniuslieder, `Steinmann_Lieder.txt` und der Kandidat. Sonette, Balladen, Müller Teil 2 und der Ganztext von Schilda bleiben draußen.

## Prüfung A

500-mal wird aus jedem Text genau eine seiner Proben gezogen. Texte mit nur einer Probe geben immer diese. Der Kandidat hat nur die ersten 351 Wörter; eine zweite Probe würde überlappen und wird nicht gezogen. Der Zufallsstrom ist `SeedSequence([20261013, 7])`.

Die 150 häufigsten Wörter und die 500 häufigsten Vierergruppen werden in jedem Durchgang nur aus den gezogenen Proben der bekannten Texte gezählt. Der Kandidat wählt keine Merkmale. Mittel und Streuung kommen aus diesen gezogenen Proben, jeder bekannte Text einmal. Der Kandidat geht darin nicht ein. Auf dem Abstand steht ein UPGMA-Baum. Es gibt keinen zweiten Zufall über die Merkmale.

Getrennt ist ein Durchgang, wenn alle Heine-Blätter darin eine Gruppe bilden. Schilda, die Vagabunden-Lieder, Müller und Steinmann liegen dann außerhalb dieser Gruppe. Die Prüfung trennt die Verfasser nur, wenn das auf beiden Hauptmaßen in mindestens 50 Prozent der 500 Durchgänge geschieht. Uhland, das Wunderhorn und die Juniuslieder werden berichtet und entscheiden nicht. Wie oft der Kandidat in der kleinsten Gruppe liegt, die alle Heine-Blätter enthält, wird berichtet und ist keine Zuschreibung. Die Größe dieser Gruppe wird mitberichtet und entscheidet nicht. Ohne sie wäre der Anteil nicht lesbar: die Gruppe kann fast der ganze Baum sein.

## Prüfung B

Jede Probe von 351 Wörtern ist ein eigenes Blatt: die Heine-Texte, Schilda, die Vagabunden-Lieder, Müller, Uhland, die Juniuslieder, Steinmann und der Kandidat. Das Wunderhorn hat 151 solche Proben. Sie würden die Mehrheit der Blätter stellen und bleiben in diesem Baum draußen. In Prüfung A bleibt das Wunderhorn mit einer Probe je Durchgang dabei.

Die Merkmale werden so gezählt, dass jeder bekannte Text gleich viel beiträgt: der Mittelwert seiner relativen Häufigkeiten, dann der Durchschnitt über die Texte. Der Kandidat zählt dabei nicht mit. Mittel und Streuung der Standardwerte kommen aus diesen Textmitteln. Gezeichnet wird je Hauptmaß ein UPGMA-Baum, ohne Ziehung.

Getrennt ist dieser Baum nur, wenn alle Heine-Proben in einer Gruppe liegen, die keine Probe von Schilda, den Vagabunden-Liedern, Müller oder Steinmann enthält. Der Ort des Kandidaten wird berichtet und entscheidet nicht.

## Aufruf

Vom Projektordner aus:

    python3 analyse/14_gleiche_proben.py

Der Ordner `ergebnisse/gleiche_proben/` wird angelegt und nicht überschrieben. `AUTOR_NEUZEICHNEN=1` schreibt ihn neu.
