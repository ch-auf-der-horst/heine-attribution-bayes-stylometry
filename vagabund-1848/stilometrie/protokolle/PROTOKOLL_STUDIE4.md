# Protokoll der Studie 4

Stand der Festlegung: 13. Oktober 2026, vor dem Lauf. Die Zahlen stehen danach in `ergebnisse/studie4/NAEHE.md` und werden nicht in dieses Protokoll zurückgeschrieben. Studie 4 ersetzt Studie 1, Studie 2 und Studie 3 nicht.

## Frage

Welchem einzelnen frühen Heine-Text kommt der Kandidat am nächsten, wenn die sieben Texte nicht zu einem Heine-Profil gemittelt werden? In derselben Tafel stehen die Lieder aus *Schilda*, Müllers erster Waldhornist, das *Wunderhorn* von 1806, Uhlands Lieder von 1815 und der Abschnitt Lieder aus Geibels *Juniusliedern* von 1848.

Das ist eine Reihung der Abstände, keine Zuschreibung. Die Entscheidung heine-nah, hektor-nah, nur-liedton, gemischt oder unentschieden bleibt die der Studien 1 bis 3. Impostors werden hier nicht gerechnet. Mehrere Heine-Texte tragen bei 548 Wörtern nur eine Probe. Eine Schwelle je Text lässt sich daran nicht eichen.

## Aufruf

Vom Projektordner aus:

    AUTOR_STUDIE=4 python3 analyse/11_studie4_naehe.py

`00_lauf.py` verweigert diesen Aufruf. Es würde die Heine-Dateien aneinanderhängen. Der Ordner `ergebnisse/studie4/` wird angelegt und nicht überschrieben. Der Zufallsstrom der Bäume ist `SeedSequence([20261013, 4])`. Die drei Ströme der Studien bleiben unberührt. Die Rangliste selbst zieht keine Zufallszahl.

## Proben

Versatz 0. Eine Probe überschreitet keine Textgrenze. Nichts wird aneinandergehängt.

Die Hauptrangliste hat die Länge des Kandidaten, 548 Wörter. Ein Text kommt nur hinein, wenn er mindestens eine solche Probe trägt. Biene, Kevlaar und Donna Clara bleiben darunter und fehlen in dieser Rangliste.

Die Nebentafel hat 351 Wörter, die Länge der Biene. Damit stehen alle sieben Heine-Texte in einer Tafel. Der Kandidat ist dort die ersten 351 Wörter. Die übrigen 197 Wörter bleiben ungenutzt. Daneben werden die letzten 351 Wörter gerechnet. Diese zweite Scheibe wird berichtet und entscheidet nicht.

## Maße

Cosine Delta wie in den Studien: relative Häufigkeit, Standardwerte mit Teilung durch n − 1, Abstand 1 minus Kosinus.

Die häufigsten Wörter und die Zeichengruppen werden nur aus den Proben der Heine-Texte gezählt, die in der jeweiligen Tafel stehen, und aus den Hektor-Proben derselben Länge. Ablenker und Kandidat wählen keine Merkmale. Primär sind 150 Wörter. 100 und 300 werden berichtet und reihen nicht. Primär sind die 500 häufigsten Vierergruppen. Dreier- und Fünfergruppen werden berichtet und reihen nicht. Die Interpunktion wird berichtet und reiht nicht.

Das Profil eines Textes ist der Mittelwert der relativen Häufigkeiten seiner Proben. Mittel und Streuung der Standardwerte kommen aus diesen Profilen der Heine-Texte der Tafel und aus dem Hektor-Profil. Jeder dieser Texte zählt dabei einmal, auch wenn die Heimkehr mehrere Proben trägt. Ablenker und Kandidat gehen in Mittel und Streuung nicht ein. Längere Texte tragen mehr Tokens zu der Liste der häufigsten Wörter bei. Das Profil der Heimkehr ist der Mittelwert mehrerer Proben, das der Aurora bei 548 Wörtern eine einzige Scheibe.

## Was als nächster Heine-Text gilt

Unter den Heine-Texten der Hauptrangliste gilt der kleinste Abstand auf den 150 Wörtern und der kleinste Abstand auf den Vierergruppen. Nennen beide denselben Text, wird er genannt. Nennen sie verschiedene Texte, bleiben beide Namen stehen. Ob Hektor oder ein Ablenker näher liegt als dieser Heine-Text, wird daneben gesagt. Das wandelt die Nennung nicht in eine Zuschreibung.

Die Konsensbäume folgen dem Verfahren der Studien: 500-mal wird jedes Merkmal mit Wahrscheinlichkeit 0,5 behalten, darauf ein UPGMA-Baum, gezeichnet werden Äste ab 50 Prozent. Dazu die Merkmalleiter aus 100, 150 und 300 Wörtern. UPGMA auf dem Kosinusabstand ist nicht ultrametrisch. Gelesen wird die Verzweigung, nicht die Astlänge. Die Bäume ändern die Rangliste nicht.
