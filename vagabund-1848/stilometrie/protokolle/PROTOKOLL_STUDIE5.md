# Protokoll der Studie 5

Stand der Festlegung: 14. Oktober 2026, vor dem Lauf. Die Zahlen stehen danach in `ergebnisse/studie5/NAEHE.md` und werden nicht in dieses Protokoll zurückgeschrieben. Studie 5 ersetzt Studie 1, Studie 2, Studie 3 und Studie 4 nicht.

## Frage

Wo steht der Kandidat, wenn die sieben frühen Heine-Texte einzeln bleiben und von Hektor zwei getrennte Texte in derselben Tafel stehen: die strophischen Lieder aus *Schilda* und die Vagabunden-Lieder von 1848? Daneben stehen Müllers erster Waldhornist, das *Wunderhorn* von 1806, Uhlands Lieder von 1815 und der Abschnitt Lieder aus Geibels *Juniusliedern* von 1848.

Das ist eine Reihung der Abstände, keine Zuschreibung. Die Entscheidung heine-nah, hektor-nah, nur-liedton, gemischt oder unentschieden bleibt die der Studien 1 bis 3. Impostors werden hier nicht gerechnet. Mehrere Texte tragen bei 548 Wörtern nur eine Probe. Eine Schwelle je Text lässt sich daran nicht eichen.

## Was nicht in der Tafel steht

Ein diplomatischer Text eigener Gedichte Achim von Arnims liegt im Projekt nicht vor. Das *Wunderhorn* ist die anonyme Liedsammlung von 1806 und bleibt unter diesem Namen. Es ist kein Verfasserprofil Arnims und wird nicht unter dem Namen Arnim geführt.

Ebenfalls draußen, aus demselben Grund wie in den früheren Studien: *Götterdämmerung*, *Ratcliff*, Müller Teil 2, Uhlands Balladen, Geibels Gedichte von 1849, Hektors Introduktion, der Knittelvers, die Ballade, der Block um XXXV, die Gedichte LXX bis LXXVII und der Ganztext von *Schilda*. Die Vagabunden-Lieder werden nicht an die Schilda-Lieder gehängt.

## Aufruf

Vom Projektordner aus:

    AUTOR_STUDIE=5 python3 analyse/12_studie5_naehe.py

`00_lauf.py` verweigert diesen Aufruf. Es würde die Heine-Dateien aneinanderhängen. Der Ordner `ergebnisse/studie5/` wird angelegt und nicht überschrieben. Der Zufallsstrom der Bäume ist `SeedSequence([20261013, 5])`. Die Ströme der Studien 1 bis 4 bleiben unberührt. Die Rangliste selbst zieht keine Zufallszahl.

## Proben

Versatz 0. Eine Probe überschreitet keine Textgrenze. Nichts wird aneinandergehängt.

Die Hauptrangliste hat die Länge des Kandidaten, 548 Wörter. Ein Text kommt nur hinein, wenn er mindestens eine solche Probe trägt. Biene, Kevlaar und Donna Clara bleiben darunter und fehlen in dieser Rangliste.

Die Nebentafel hat 351 Wörter, die Länge der Biene. Damit stehen alle sieben Heine-Texte in einer Tafel. Der Kandidat ist dort die ersten 351 Wörter. Die übrigen 197 Wörter bleiben ungenutzt. Daneben werden die letzten 351 Wörter gerechnet. Diese zweite Scheibe wird berichtet und entscheidet nicht.

## Maße

Cosine Delta wie in den Studien: relative Häufigkeit, Standardwerte mit Teilung durch n − 1, Abstand 1 minus Kosinus.

Die häufigsten Wörter und die Zeichengruppen werden nur aus den Proben der Heine-Texte gezählt, die in der jeweiligen Tafel stehen, und aus den Proben von Schilda und von den Vagabunden-Liedern derselben Länge. Ablenker und Kandidat wählen keine Merkmale. Primär sind 150 Wörter. 100 und 300 werden berichtet und reihen nicht. Primär sind die 500 häufigsten Vierergruppen. Dreier- und Fünfergruppen werden berichtet und reihen nicht. Die Interpunktion wird berichtet und reiht nicht.

Das Profil eines Textes ist der Mittelwert der relativen Häufigkeiten seiner Proben. Mittel und Streuung der Standardwerte kommen aus diesen Profilen der Heine-Texte der Tafel, aus Schilda und aus den Vagabunden-Liedern. Jeder dieser Texte zählt dabei einmal, auch wenn er mehrere Proben trägt. Ablenker und Kandidat gehen in Mittel und Streuung nicht ein. Längere Texte tragen mehr Tokens zu der Liste der häufigsten Wörter bei. Schilda trägt mehr Proben bei als die Vagabunden-Lieder. Das ändert die Zählung der Profile nicht: dort zählt jeder Text einmal.

## Was die Reihung nennt

Unter den Heine-Texten der Hauptrangliste gilt der kleinste Abstand auf den 150 Wörtern und der kleinste Abstand auf den Vierergruppen. Nennen beide denselben Text, wird er genannt. Nennen sie verschiedene Texte, bleiben beide Namen stehen. Ob Schilda, die Vagabunden-Lieder oder ein Ablenker näher liegt als dieser Heine-Text, wird daneben gesagt.

Auf der ganzen Tafel wird derselbe Vergleich über alle Texte berichtet. Nennen Wörter und Vierergruppen dort verschiedene Texte, bleiben beide Namen stehen. Das wandelt die Nennung nicht in eine Zuschreibung.

Die Konsensbäume folgen dem Verfahren der Studien: 500-mal wird jedes Merkmal mit Wahrscheinlichkeit 0,5 behalten, darauf ein UPGMA-Baum, gezeichnet werden Äste ab 50 Prozent. Dazu die Merkmalleiter aus 100, 150 und 300 Wörtern. UPGMA auf dem Kosinusabstand ist nicht ultrametrisch. Gelesen wird die Verzweigung, nicht die Astlänge. Die Bäume ändern die Rangliste nicht.
