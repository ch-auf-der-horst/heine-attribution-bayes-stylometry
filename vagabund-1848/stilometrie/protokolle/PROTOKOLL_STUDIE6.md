# Protokoll der Studie 6

Stand der Festlegung: 14. Oktober 2026, vor dem Lauf. Die Zahlen stehen danach in `ergebnisse/studie6/NAEHE.md` und werden nicht in dieses Protokoll zurückgeschrieben. Studie 6 ersetzt Studie 1, Studie 2, Studie 3, Studie 4 und Studie 5 nicht.

## Frage

Trennt das festgelegte Verfahren die frühen Heine-Lieder von den Strophenliedern, die Steinmann 1857 Heine zuschreibt? Steinmann führt sie als Heines Gedichte. Diese Studie behandelt `Steinmann_Lieder.txt` als die Fälschungsprobe. Sie prüft, ob diese Probe außerhalb der Abstände liegt, die die Heine-Texte untereinander haben. Sie weist den Text keinem Verfasser zu und schätzt keine Fälschungsrate. Es ist ein Text und, auf der Hauptlänge, eine Probe.

## Was nicht in die Entscheidung eingeht

Die beiden Sonette in `Steinmann_Sonette.txt` bleiben draußen. Sie sind eine andere Gedichtart. Ein Abstand dort würde Gedichtart und Zuschreibung mischen.

Der Kandidat aus dem *Vagabund* wird nicht gelesen und nicht gerechnet. Die Schwellen der Studien 1 bis 3 werden nicht geändert. Impostors werden nicht gerechnet. Mehrere Heine-Texte tragen bei 548 Wörtern nur eine Probe.

Schilda, die Vagabunden-Lieder, Müllers erster Waldhornist, das *Wunderhorn*, Uhlands Lieder und die Juniuslieder stehen in der Tafel, damit ein großer Abstand zu Heine nicht mit einem nahen anderen Text verwechselt wird. Sie wählen keine Merkmale, gehen nicht in die Standardwerte ein und entscheiden die Trennung nicht. Ein eigener Gedichttext Achim von Arnims liegt nicht vor. Das *Wunderhorn* bleibt unter diesem Namen.

Ebenfalls draußen: *Götterdämmerung*, *Ratcliff*, Müller Teil 2, Uhlands Balladen, Geibels Gedichte von 1849, Hektors Introduktion, der Knittelvers, die Ballade, der Block um XXXV, die Gedichte LXX bis LXXVII und der Ganztext von *Schilda*.

## Aufruf

Vom Projektordner aus:

    AUTOR_STUDIE=6 python3 analyse/13_studie6_trennung.py

`00_lauf.py` verweigert diesen Aufruf. Es würde die Heine-Dateien aneinanderhängen. Der Ordner `ergebnisse/studie6/` wird angelegt und nicht überschrieben. Der Zufallsstrom der Bäume ist `SeedSequence([20261013, 6])`. Die Ströme der Studien 1 bis 5 bleiben unberührt. Die Trennung selbst zieht keine Zufallszahl. Die Bäume ändern sie nicht.

## Proben

Versatz 0. Eine Probe überschreitet keine Textgrenze. Nichts wird aneinandergehängt.

Die Haupttabelle hat 548 Wörter. Ein Text kommt nur hinein, wenn er mindestens eine solche Probe trägt. Biene, Kevlaar und Donna Clara bleiben darunter. Steinmann hat nach der letzten Änderung 492 Wörter und trägt keine solche Probe. Die Datei wird nicht auf 548 Wörter gedehnt und nicht über eine Textgrenze hinaus aufgefüllt. Die Haupttabelle wird dann nicht gebildet.

Der Lauf an der Datei mit 556 Wörtern, Prüfsumme 6bb317b3471d94c5297abc0ed9b64066742ea8cab3fb9805112c0308bb43c768, hatte den Ausgang nicht getrennt. Davor galt die Datei mit 598 Wörtern, Prüfsumme f7c27a55f7a45404e14eb29d9230f89a6fef222fd1511e2b5c511fa20d9502a1, ebenfalls mit dem Ausgang nicht getrennt. Die Regel ist dieselbe. Der neue Lauf überschreibt `ergebnisse/studie6/`.

Die Nebentafel hat 351 Wörter. Damit stehen alle sieben Heine-Texte in einer Tafel. Von Steinmann stehen dort die ersten 351 Wörter. Die letzten 351 Wörter werden berichtet und entscheiden nicht. Sie überlappen die ersten.

## Maße

Cosine Delta wie in den Studien: relative Häufigkeit, Standardwerte mit Teilung durch n − 1, Abstand 1 minus Kosinus.

Die häufigsten Wörter und die Zeichengruppen werden nur aus den Heine-Proben der jeweiligen Tafel gezählt. Steinmann und die übrigen Texte wählen keine Merkmale. Primär sind 150 Wörter. 100 und 300 werden berichtet und entscheiden nicht. Primär sind die 500 häufigsten Vierergruppen. Dreier- und Fünfergruppen werden berichtet und entscheiden nicht. Die Interpunktion wird berichtet und entscheidet nicht.

Das Profil eines Textes ist der Mittelwert der relativen Häufigkeiten seiner Proben. Mittel und Streuung der Standardwerte kommen nur aus den Profilen der Heine-Texte, die in der Tafel stehen. Jeder dieser Texte zählt einmal. Steinmann ist auf der Hauptlänge eine einzelne Probe und wird mit diesen Profilen verglichen.

## Wann die Trennung deutlich ist

Gerechnet wird auf vier Stellen, wie die Tafeln sie schreiben. Verglichen werden der kleinste Abstand von Steinmann zu einem Heine-Text dieser Tafel, der größte Abstand zwischen zwei Heine-Texten und der kleinste Abstand zwischen zwei Heine-Texten.

Auf einem Maß liegt Steinmann außerhalb, wenn sein kleinster Heine-Abstand größer ist als der größte Abstand zweier Heine-Texte. Deutlich außerhalb ist er nur, wenn der Überschuss mindestens so groß ist wie der kleinste Heine-Abstand. Sonst ist er knapp außerhalb. Ist der kleinste Heine-Abstand nicht größer, liegt er innerhalb.

Der Ausgang der Haupttabelle:

- deutlich getrennt, wenn beide Hauptmaße deutlich außerhalb sind;
- knapp außerhalb, wenn beide außerhalb sind und nicht beide deutlich;
- uneinig, wenn ein Hauptmaß außerhalb ist und das andere innerhalb;
- nicht getrennt, wenn beide innerhalb sind.

Die Nebentafel wird nach derselben Regel gelesen. Sie entscheidet nicht. Der nächste Text der ganzen Tafel wird genannt und entscheidet nicht.
