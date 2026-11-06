# Korrektur der Nachahmertexte (E-11) und Nachrechnung

Stand: 31. Oktober 2026. Diese Arbeit gehört nicht zum Auswertungsprotokoll. Sie betrifft nur die Eingabetexte. Die Skripte sind unverändert.

> **Statusnotiz zur Veröffentlichung (6. November 2026).** Der Bericht ist im Stand vom 31. Oktober belassen. Die in Abschnitt 6 genannten Stellen des Aufsatzes sind inzwischen angepasst; alle Werte des Aufsatzes beruhen auf den korrigierten Texten. Abschnitts- und Anmerkungsnummern folgen dem damaligen Stand (die Fehlerquote steht heute in Anm. 8). Die korrigierten Texte, im Bericht `texte_korrigiert/`, liegen im Repositorium unter `bayes/e11/texte/`; ihre Prüfsummen stehen dort in `SHA256SUMS.txt`, mit dem damaligen Pfadpräfix `texte_neu/`. Die alten, unkorrigierten Texte sind nicht beigegeben.

## 1. Was korrigiert wurde

Betroffen sind die vier Texte der offenen Gegenprobe E-11. Die Bestandsaufnahme vom 30.10. hat gezeigt, dass alle anderen Texte der Hauptauswertung abgeschrieben, am Seitenbild gelesen oder aus dem DTA übernommen sind (`../BERICHT_Textqualitaet.md`).

| Text | Vorgehen |
|---|---|
| Scherr, *Laute und leise Lieder* (1842), PDF-Seiten 9–116 | jede Seite vollständig am Seitenbild gelesen und neu geschrieben |
| Müller von Königswinter, *Junge Lieder* (1841), PDF-Seiten 15–136 | alte Texterkennung Seite für Seite durchgesehen, abgeglichen mit einer zweiten Fraktur-Erkennung (Tesseract 5, Modell `deu_latf`); Stellen, an denen die beiden abweichen oder die verdächtig sind, korrigiert, bei Zweifel am Seitenbild |
| Storm und Th. Mommsen, *Liederbuch dreier Freunde* (1843), Seitenzuordnung wie bisher (`lb/split.py`) | Durchsicht jeder Seite, bei Zweifel am Seitenbild; drei Seiten mit zerstörter Erkennung neu abgeschrieben |

**Einheitlich für alle vier Texte:**
- Satzzeichen stehen am Wort wie in den übrigen Korpustexten, nicht mehr als eigene Tokens (vorher z. B. `Rebenlauben ,`). Das ist eine Angleichung an die Form der anderen Klassen.
- Gedankenstriche sind vereinheitlicht (`=-`, `--`, `==` werden zu `—`).
- Worttrennungen am Zeilenende sind aufgelöst (`zehn- tausend` wird zu `zehntausend`).
- Langes s wird s.

**Entfernt wurden** (als Fremdtext oder Paratext, wie bei den diplomatischen Korpustexten):
- fremdsprachige Mottos und Titel (Burns, Byron, Horaz, ein lateinisches Motto);
- Mottos anderer Verfasser (Platen);
- Melodieangaben, Fußnoten, Widmungsblatt, Abteilungstitel;
- Hinweise wie „Nach Byron“ oder „Nach Viktor Hugo“.

Die Nachdichtungen selbst bleiben im Text, wie bisher.

**Wieder aufgenommen** wurde Scherr, PDF-Seite 102 (rund 110 Wörter). Sie war wegen eines Bibliotheksstempels bisher ganz herausgefallen.

**Wie bisher nicht aufgenommen:**
- die zwei gedreht gesetzten Figurengedichte im *Liederbuch* (Druckseiten 72–73);
- die Seiten, die das Inhaltsverzeichnis keinem einzelnen Verfasser zuordnet.

Jede Änderung ist protokolliert: `Aenderungsprotokoll_E11.csv` (1.619 Zeilen, Seite für Seite, vorher und nachher), dazu die Korrekturlisten `werkzeug/korr_mu.txt` und `werkzeug/korr_lb.txt` sowie die korrigierten Einzelseiten (`werkzeug/seiten_korrigiert.tgz`).

## 2. Fehlerquote vorher und nachher

| Text | vorher (30.10.) | nachher: alte Stichprobe | nachher: neue Stichprobe |
|---|---:|---:|---:|
| Scherr | 6,6 % (21/316) | 0 Fehler* | 0/450 (95-%-Obergrenze 0,9 %) |
| Müller v. Königswinter | 1,4 % (3/216) | 0/216 | 0/266 (≤ 1,4 %) |
| Storm | 2,1 % (7/340) | 0/339 | 0/356 (≤ 1,1 %) |
| Th. Mommsen | 0,9 % (3/337) | 0* | 0/428 (≤ 0,9 %) |
| zusammen | 2,8 % (34/1.209) | 0 | 0/1.500 (≤ 0,3 %) |

\* Die einzigen Abweichungen sind die bewusst entfernten Mottos (Burns, Horaz).

Die alte Stichprobe wurde am 30.10. vor jeder Korrektur am Seitenbild abgeschrieben und prüft die Korrektur daher unabhängig. Die neue Stichprobe ist zufällig gezogen (Startwert 20261031, `stichprobe_nachher.json`) und enthält keine Seite der alten.

## 3. Einfrieren

Die korrigierten Texte liegen in `texte_korrigiert/`, gesichert durch SHA-256 (`SHA256SUMS.txt`). Erst danach wurde gerechnet. Die alten Texte bleiben unverändert in `Repositorium_Vorbereitung/Bayes_Arbeitsskripte/e11/texte/`.

## 4. Nachrechnung

Gerechnet wurde in einer Kopie von `Bayes_Arbeitsskripte`, in der nur die vier Dateien in `e11/texte/` ausgetauscht waren. `e11prep.py` wurde nicht ausgeführt, weil es die Texte aus der Erkennung neu erzeugen würde. Ein Kontrolllauf mit den alten Texten reproduziert alle bisherigen Ergebnisse bitgenau.

Alle Skripte liefen neu (`calib`, `openset`, `blind`, `e1`, `e2`, `e3`, `e3r`, `e7`, `e9`, `e9c`, `e11`). Bitgleich geblieben sind Kalibrierung, offene Gegenprobe, Verblindung, E-1, E-2, E-3, E-7 und E-9. Nur E-11 hat sich geändert, weil nur E-11 die korrigierten Texte liest (`nachrechnung/`).

| E-11 | vorher | nachher |
|---|---|---|
| Delta Wörter: AUC Heine gegen Nachahmer | 0,832 | 0,811 |
| Nachahmerproben mindestens so heine-nah wie der Kandidat | 13/65 | 19/62 |
| je Verfasser | Müller v. K. 3/16, Scherr 1/24, Storm 3/7, Mommsen 6/18 | Müller v. K. 6/15, Scherr 3/23, Storm 3/7, Mommsen 7/17 |
| Quotient (log10) | 3,39 (+0,53) | 2,24 (+0,35) |
| Zeichen-4-Gramme: AUC | 0,805 | 0,803 |
| Quotient (log10) | 2,13 (+0,33) | 2,03 (+0,31) |
| Versmerkmale: AUC (Tor 0,75) | 0,60, nicht bestanden | 0,60, nicht bestanden |
| **Wertung H1 : H3 (Median der bestandenen Maße)** | **+0,43** | **+0,33** |
| Zeichen-4-Gramme neutral | +0,27 | +0,18 |

Der Wert des Kandidaten selbst ist unverändert (s = 0,004 bzw. 0,234), ebenso sein Bootstrap-Intervall, denn der Kandidat wurde nicht korrigiert.

**Deutung:** Mit sauberen Texten liegen die Nachahmer im Wortschatz-Delta etwas häufiger auf Höhe des Kandidaten. Die Fehler hatten die Nachahmertexte also eher von Heine *weg*geschoben und die Heine-Hypothese begünstigt. So hatte es Endnote 7 vermutet. Am stärksten verschiebt sich Müller von Königswinter (3/16 → 6/15).

## 5. Folgen für die Bilanz

Die Summe gegenüber H3 sinkt um 0,10: ausgewogen von +0,63 auf +0,53, skeptisch von +0,03 auf −0,07. Die Summe gegenüber H2 bleibt +1,5.

| Variante | Chance | vorher | nachher |
|---|---|---:|---:|
| Hauptwertung | 1 : 5 bis 1 : 3 | 60–71 % | **55–67 %** |
| Zagreber Gedicht offen | 1 : 4 bis 1 : 2,2 | 65–77 % | 60–74 % |
| Offene Fälle als unecht | 1 : 7 | 52 % | **47 %** |
| Gesamte Gegenmasse bei einem Nachahmer | 1 : 5 bis 1 : 3 | 46–59 % | 40–53 % |
| Zeichen-4-Gramme neutral | 1 : 5 bis 1 : 3 | 52–64 % | 47–60 % |
| Nur philologische Befunde | 1 : 5 bis 1 : 3 | 35–48 % | 35–48 % |
| Skeptisch, Referenzklasse | 1 : 5 bis 1 : 3 | 26–38 % | 23–33 % |
| Skeptisch | 1 : 7 | 21 % | 17 % |
| Skeptisch, Steinmann als Untergrenze | 1 : 20 bis 1 : 7 | 8–21 % | 7–17 % |
| Schwelle 50 % (8.3) | | 0,2–0,4 Punkte | 0,1–0,3 Punkte |
| Schwelle 10 % (8.3) | | 1,1–1,4 Punkte | 1,0–1,3 Punkte |

Die Kernaussage bleibt bestehen und wird eher schärfer: Die Gedichte sind als zweifelhaft zu führen, nicht als unecht. „Wahrscheinlich echt“ ist noch weniger belastbar als vorher. Zählt man die offenen Fälle wie bisher üblich als unecht, liegt Heine jetzt knapp unter 50 %.

## 6. Im Aufsatz betroffen (noch nicht geändert)

- Abstract (Ergebnisse);
- 7.4 (Absatz zu Abb. 1 sowie der Absatz mit den Werten je Verfasser);
- 7.7, 8.1, 8.2 und 8.3 mit Anm. 10;
- Tab. 4 (zwei Zeilen) und Tab. 5;
- Abb. 1 (neu zu zeichnen) und Abb. 2 mit Alternativtext;
- Endnote 7 (gemessene Fehlerquote statt „etwa 3 %“, Korrektur, Ergebnis);
- 5.5 (ein Satz unter „Abweichungen“);
- Arbeitsdokument „Bayesianische Vorgehensweise“.

Ebenfalls auf den alten Texten beruht die Zusatzprüfung `Stilometrie_Schilda_Heine`. Sie ist nicht Teil des Aufsatzes und kann bei Bedarf nachgerechnet werden.
