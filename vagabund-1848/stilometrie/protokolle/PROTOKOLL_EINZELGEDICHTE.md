# Protokoll der Einzelgedichte

Stand der Festlegung: 14. Oktober 2026, vor dem Lauf. Die Zahlen stehen danach in `ergebnisse/einzelgedichte/EINZEL.md` und werden nicht in dieses Protokoll zurückgeschrieben. Der Lauf ersetzt die Studien 1 bis 5 nicht und ist keine Zuschreibung.

## Frage

Tragen wenige der zehn Kandidatengedichte die Nähe des Blocks, oder liegen die Gedichte so beieinander wie gleich lange Stücke eines Textes?

## Gedichte

Jedes Gedicht bleibt ganz. Die römische Nummer ist die Überschrift und gehört nicht zum Gedicht. Aus dem Kandidaten wird keine Scheibe geschnitten. Die zehn Gedichte haben zwischen 34 und 80 Wörtern.

## Vergleichsstücke

Für die Länge eines Gedichts werden aus jedem der sieben frühen Heine-Texte, aus `Hektor_Schilda.txt` und aus `Hektor_Vagabund.txt` nicht überlappende Scheiben dieser Länge geschnitten. Versatz 0. Eine Scheibe überschreitet keine Textgrenze. Nichts wird aneinandergehängt.

Die Merkmale kommen nur aus diesen Scheiben. Der Kandidat wählt sie nicht. Primär sind 150 Wörter und die 500 häufigsten Vierergruppen. 100 und 300 Wörter sowie Dreier- und Fünfergruppen werden berichtet und entscheiden nicht. Cosine Delta wie in den Studien: relative Häufigkeit, Standardwerte mit Teilung durch n − 1, Abstand 1 minus Kosinus. Mittel und Streuung kommen aus den neun Textprofilen, jedes Text einmal. Ein Profil ist der Mittelwert der relativen Häufigkeiten seiner Scheiben.

## Zwei Vergleiche

Der Abstand eines Gedichts zum Mittel der anderen neun wird mit den leave-one-out-Abständen der Heimkehr-Scheiben derselben Länge verglichen. Jede Heimkehr-Scheibe wird am Mittel der übrigen Heimkehr-Scheiben gemessen. Ein Gedicht fällt aus dem Block, wenn dieser Abstand auf den 150 Wörtern und auf den Vierergruppen über dem 95%-Quantil der Heimkehr-Scheiben liegt. Das Quantil ist das lineare Quantil.

Der Abstand eines Gedichts zum Heimkehr-Profil wird mit den leave-one-out-Abständen der Heimkehr-Scheiben zum Heimkehr-Profil derselben Länge verglichen. Ein Gedicht liegt im Heimkehr-Bereich, wenn der Abstand auf beiden Maßen höchstens das 95%-Quantil erreicht. Das sagt nicht, dass das Gedicht von Heine ist. Es sagt, dass es dem Heimkehr-Profil nicht ferner liegt als gleich lange Heimkehr-Scheiben einander liegen.

## Was als Antwort gilt

Die Nähe des Blocks wird von wenigen Gedichten getragen, wenn höchstens drei der zehn im Heimkehr-Bereich beider Maße liegen und mindestens eines darin liegt. Liegen vier oder mehr darin, ist sie breit geteilt. Liegt keines darin, oder liegt auf beiden Maßen jedes Gedicht so nah oder so fern, dass der Heimkehr-Bereich sie nicht trennt, kann die Einzelprobe die Nähe nicht auf wenige Gedichte zurückführen. Die Streuung gleich langer Heimkehr-Scheiben ist dann bereits so groß wie die Unterschiede unter den Gedichten.

Schilda und die Vagabunden-Lieder werden daneben gemessen und entscheiden nicht.

## Aufruf

Vom Projektordner aus:

    AUTOR_STUDIE=5 python3 analyse/13_einzelgedichte.py

Der Ordner `ergebnisse/einzelgedichte/` wird angelegt und nicht überschrieben. Der Lauf zieht keine Zufallszahl.
