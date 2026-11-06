# Protokoll der Studie 1

Stand der Festlegung: 13. Oktober 2026. Die Schwellen in `studie1_parameter.py` sind vor dem Lauf gesetzt. Das Ergebnis steht danach in `ergebnisse/studie1/lauf_2026-10-13_seed20261013/` und wird nicht in dieses Protokoll zurückgeschrieben.

## Frage

Liegen die zehn Gedichte, die Enno Hektor 1848 im *Vagabund* als Heine-Texte von Norderney veröffentlicht hat, dem frühen strophischen Heine nahe, den Liedern aus *Schilda*, nur dem Liedton der Zeit, oder lässt sich das an dieser Textlänge nicht entscheiden?

## Was die Skripte tun

Aufgerufen wird vom Projektordner aus `python3 analyse/00_lauf.py`. Der Laufordner wird angelegt und nicht überschrieben. `00_lauf.py` schreibt `parameter.json` und `pakete.txt` und ruft dann der Reihe nach auf:

| Skript | Leistung | Liest | Schreibt in den Laufordner |
| --- | --- | --- | --- |
| `01_proben_schneiden.py` | schneidet die Eichproben | `studie1_dateien.csv`, die dort genannten Dateien außer dem Kandidaten | `proben/`, `teilung.json`, `eingaben.csv` |
| `02_eichung_cosine_delta.py` | Cosine Delta der häufigsten Wörter | `teilung.json` und die Heine- und Hektor-Ströme | `02_woerter.json`, `02_woerter_merkmale.txt`, `02_woerter_abstaende.csv`, `02_woerter_versatz.csv` |
| `03_eichung_zeichengramme.py` | Cosine Delta der Zeichengramme | dieselben Proben | `03_zeichen.json`, `03_zeichen_versatz.csv` |
| `04_eichung_interpunktion.py` | Cosine Delta der Interpunktion | dieselben Proben | `04_interpunktion.json`, `04_interpunktion_versatz.csv` |
| `05_eichung_auswerten.py` | öffnet oder schließt das Tor | die drei JSON-Dateien und die Abstandstabelle | `eichung_tor.json`, `abstand_woerter.svg` |
| `06_impostors_kandidat.py` | Impostors-Prüfung | das Tor, die Teilung, zum ersten Mal `Kandidat_Vagabund.txt` | `06_impostors.json`, `06_impostors_loo.csv`, `ENTSCHEIDUNG.md` |
| `07_versifikation.py` | Strophe, Reim, Kadenznäherung | Kandidat, Heine-Dateien, `Hektor_Schilda.txt` | `07_strophen_kandidat.csv`, `07_strophen_vergleich.csv` |
| `08_abbildungen.py` | zeichnet die gerechnete Studie, ohne sie neu zu entscheiden | den bestehenden Laufordner | `abb_*.svg`, `abb_uebersicht.html`, `08_konsens_kladen.csv` |

`gemeinsame.py` enthält die Rechenwege und wird nicht selbst aufgerufen. `anforderungen.txt` nennt das Paket. Gerechnet wird mit numpy und der Standardbibliothek.

## Dateien

Die Liste `studie1_dateien.csv` ist die einzige Eingabeliste. `01` prüft die Wortzahlen und schreibt SHA-256 der gelesenen Dateien nach `eingaben.csv`. Der Kandidat bleibt in diesem Schritt ungeöffnet. `06` schreibt seine Prüfsumme in `06_impostors.json`.

Heine, in dieser Reihenfolge aneinandergehängt: `Heine_Aurora.txt`, `Heine_Biene.txt`, `Heine_Almanach.txt`, `Heine_Agrippina.txt`, `Heine_Heimkehr.txt`, `Heine_Kevlaar.txt`, `Heine_DonnaClara.txt`.

Hektor: nur `Hektor_Schilda.txt`, die strophischen Lieder. In den Abbildungen heißt dieses Blatt Schilda.

Ablenker, jeder für sich: `Mueller_1.txt`, `Wunderhorn_1806.txt`, `Uhland_Lieder.txt`, `Geibel_Lieder.txt`.

Kandidat: `corpus_diplomatisch/Kandidat_Vagabund.txt`, 548 Wörter. `Kandidat_I-V.txt` und `Kandidat_VI-X.txt` bleiben draußen.

Ausgeschieden und in der Liste als solche geführt: `Heine_Ballade.txt`, `Heine_Ratcliff.txt`, `Mueller_2.txt`, `Uhland_Balladen.txt`, `Geibel_Buecher.txt`, `Geibel_Sonette.txt`, `Hektor_Intro.txt`, `Hektor_Knittel.txt`, `Hektor_Ballade.txt`, `Hektor_XXXV.txt`, `Hektor_LXX.txt`, der Ganztext `Hektor/Hektor_Schilda_1847.txt`.

## Proben

Die Probenlänge ist 548 Wörter, die Wortzahl des Kandidaten. Ein Wort ist eine durch Leerraum getrennte Zeichenfolge. Der Kandidat wird weder gerundet noch gekürzt.

Der Seed ist 20261013. Daraus entstehen drei getrennte Zufallsströme: Teilung, Impostors, Versifikation. Der Versatz der Primärteilung ist die erste Ziehung des Teilungsstroms, für Heine und dann für Hektor. Eine Ziehung ist eine ganze Zahl von 0 bis zum Rest der Wortzahl bei Teilung durch 548. Danach werden nicht überlappende Proben gelegt. Beide Verfasser behalten nur so viele Proben, wie der kürzere Strom hergibt, genommen vom Anfang der Teilung. Es folgen 100 weitere Versätze. Sie prüfen, ob die Wort-AUC an der Primärteilung hängt.

Ablenker werden ohne weitere Zufallszahl in nicht überlappende Proben gelegt. Von einem langen Text werden so viele Proben genommen, wie die Verfasserproben zählen, verteilt vom Anfang bis zum Ende. Ein kürzerer Text behält alle nicht überlappenden Proben. Weniger als fünf Proben brechen den Lauf ab.

## Drei Maße

Die Merkmale der Eichung werden nur aus den Heine- und Hektor-Proben gewählt.

Wörter. Aus jedem Token wird ein klein geschriebenes Buchstabenwort, Apostroph und Bindestrich bleiben am Wort, andere Satzzeichen fallen weg. Gezählt werden die 150 häufigsten Wörter. 100 und 300 werden mitgerechnet und entscheiden nicht. Pronomen werden nicht entfernt. Die relative Häufigkeit teilt durch alle Buchstabenwörter der Probe. Cosine Delta: Standardwert über die Proben, Standardabweichung mit Teilung durch n − 1, Abstand 1 minus Kosinusähnlichkeit. Spalten ohne Streuung fallen weg.

Zeichengramme. Die Probe wird klein geschrieben und mit einem Leerzeichen zwischen den Token verbunden. Entschieden wird mit den 500 häufigsten 4-Grammen. 3- und 5-Gramme werden mitgerechnet und entscheiden nicht.

Interpunktion. Gezählt je Wort der Probe: Komma, Punkt, Frage- und Ausrufezeichen, Apostroph, Semikolon, Doppelpunkt, Gedankenstrich, öffnende und schließende Anführung, Auslassungspunkte, übrige Satzzeichen. Ein Bindestrich zwischen zwei Buchstaben zählt nicht mit. Der Apostroph zählt auch im Wortbild. Diese Gruppe entscheidet nicht.

Die AUC ist der Anteil der Paare, in denen zwei Proben desselben Verfassers näher beieinander liegen als eine Heine- und eine Hektor-Probe. Gleiche Abstände zählen halb. Dieselbe Herkunft umfasst Heine gegen Heine und Hektor gegen Hektor.

## Tor

Das Tor ist offen, wenn die Primär-AUC der 150 Wörter mindestens 0,75 ist, die Primär-AUC der 4-Gramme mindestens 0,75 ist und mindestens 95 von 100 Versatz-Wiederholungen der Wörter ebenfalls 0,75 erreichen. Sonst ist der Ausgang unentschieden. Die Impostors-Anteile werden auch dann berechnet und in `ENTSCHEIDUNG.md` nicht als Zuschreibung gelesen.

## Impostors

Der Abstand ist der Ružička-Abstand auf den relativen Häufigkeiten: 1 minus Summe der Minima, geteilt durch Summe der Maxima. In jeder von 500 Ziehungen bleibt jedes Merkmal mit Wahrscheinlichkeit 0,5 erhalten. Der Anteil ist der Anteil der Ziehungen, in denen das Ziel näher liegt als jeder Ablenker.

Ein Profil ist das Mittel der relativen Häufigkeiten seiner Proben. In der Leave-one-out-Prüfung wird die Probe, die gerade geprüft wird, aus ihrem eigenen Profil herausgenommen. Positive Fälle sind Heine-Proben gegen das Heine-Profil und Hektor-Proben gegen das Hektor-Profil. Negative Fälle sind dieselben Proben gegen den anderen Verfasser und die Ablenker-Proben gegen Heine und gegen Hektor. Die Schwelle ist der Median der Schwellen mit dem größten Youden-Index. Liegt dieser Index unter 0,5, trägt die Impostors-Prüfung die Zuschreibung nicht.

Dieselbe Schwelle, mit einem Band von 0,05, gilt für den Kandidaten. Darüber und darunter sind entschieden. Dazwischen bleibt der Anteil unbeantwortet. Wörter und Zeichengramme haben je eine eigene Schwelle. Die Interpunktion wird nach demselben Verfahren mitgeteilt und entscheidet nicht.

Der Kandidat gilt als heine-nah, wenn beide Gruppen Heine nennen, und als hektor-nah, wenn beide Hektor nennen. Gemischt ist das Ergebnis, wenn eine Gruppe Heine und die andere Hektor nennt oder eine Gruppe beide Schwellen überschritten sieht. Nur der Liedton liegt vor, wenn beide Gruppen unter beiden Schwellen bleiben und der Kandidat im Cosine Delta der Wörter näher an einem Ablenker-Profil liegt als an Heine und an Hektor. Die Standardwerte dieses Abstands stammen aus den Heine- und Hektor-Proben und werden auf die Profile und den Kandidaten angewendet, nicht neu aus ihnen berechnet. Jeder andere Ausgang ist unentschieden.

## Versifikation

`07_versifikation.py` trennt Strophen an Leerzeilen. Römische Gedichtnummern sind Überschriften. Der Reim ist orthographisch. Die Kadenzregel und die Vokalgruppen sind Näherungen und keine metrische Sicherung. Zu jeder Kandidatenstrophe wird, soweit vorhanden, eine Strophe derselben Zeilenzahl aus dem frühen Heine und eine aus den Hektor-Liedern gezogen.

## Abbildungen

`08_abbildungen.py` läuft nach der Entscheidung und schreibt in denselben Laufordner. Ein schon bestehender Lauf wird damit nicht neu gerechnet. Der Aufruf allein ist `python3 analyse/08_abbildungen.py`.

Der Konsensbaum aus dem Merkmal-Bootstrap zieht 500-mal eine zufällige Hälfte der festgelegten Merkmale, rechnet darauf Cosine Delta und UPGMA und behält jede Klade, die in mindestens der Hälfte der Bäume steht. Die Zahl am Ast ist dieser Anteil in Prozent. Die Normierung eines Baums mit dem Kandidaten kommt aus den Eichproben, nicht aus dem Kandidaten. Die Merkmalleiter zeichnet je einen Baum für 100, 150 und 300 häufigste Wörter und bildet daraus den Konsens. Das ist die Form des Bootstrap Consensus Tree in stylo, hier nur mit den drei festgelegten Merkmalzahlen. 100 und 300 entscheiden in der Studie nicht, und die Abbildungen ändern `ENTSCHEIDUNG.md` nicht.

## Zweite Studie

Weitere Heine zugeschriebene Gedichte sind eine eigene Studie. Sie bekommen eine eigene Dateiliste und einen eigenen Ergebnisordner. Dieselben Funktionen in `gemeinsame.py` können sie lesen. Sie werden nicht in die Heine-Referenz dieser Studie aufgenommen, und der Vagabund-Text wird dort nicht nachträglich zum gesicherten Heine.
