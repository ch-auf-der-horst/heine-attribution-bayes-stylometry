# E-11 mit Meißner, Hartmann und Dingelstedt: explorative Rechnung

Stand: 31. Oktober 2026. **Diese Rechnung steht außerhalb des Auswertungsprotokolls und gehört nicht in den Aufsatz.** Die Texte wurden nach dem Entwurf `../Protokollerweiterung_Nachahmerklassen_Entwurf.md` (Fassung 1, 12:30 Uhr) hergestellt und ausgewählt. Die Aufteilung in die Teilklassen H3a und H3b ist noch nicht gerechnet, weil Fassung 2 mit den Belegen K1–K3 fehlt.

## 1. Texte

Grundlage sind nur lyrische Sammlungen. Aus dem Gedichtteil jedes Bandes wurden Druckseiten mit dem Startwert 20261031 zufällig gezogen, bis 11.000 Tokens erreicht waren. Die Seiten wurden erst nach der Ziehung erkannt und gesäubert.

| Text | Pool (PDF-Seiten) | gezogene Seiten | Tokens | Proben à 548 |
|---|---|---:|---:|---:|
| Meißner, *Gedichte*, 2. Auflage 1846 | 29–310 | 153 | 10.904 | 19 |
| Hartmann, *Kelch und Schwert* 1845 und *Neuere Gedichte* 1847 (ein gemeinsamer Pool) | 21–330 und 22–339 | 151 | 10.771 | 19 |
| Dingelstedt, *Lieder eines kosmopolitischen Nachtwächters*, 2. Auflage 1842 | 9–176 | 111 | 10.845 | 19 |

Hartmanns *Reimchronik* ist ausgeschlossen, weil sie ein Versepos ist.

**Texterstellung:**
- Fraktur-Erkennung mit Tesseract 5 (Modell `deu_latf`);
- regelhafte Reinigung: langes s, Fraktur-Ligaturen, Seitenzahlen, Bogensignaturen, Google- und Bibliotheksvermerke;
- jede gezogene Seite durchgesehen und korrigiert, im Zweifel am Seitenbild;
- stark gestörte Seiten am Bild neu abgeschrieben (rund 45 Seiten).

**Entfernt** wurden Abteilungstitel, Melodieangaben, fremdsprachige Mottos (Ovid, Spanisch, Latein), Fußnoten, Datierungen und Widmungszeilen, Gedichtnummern und lebende Kolumnentitel.

**Stichprobe nach der Korrektur.** Gezogen wurden 9 Seiten mit einem neuen Startwert (20261101), zusammen 822 Wörter, und am Bild gelesen. Dabei fanden sich ein fehlender Apostroph („reiß'“) und ein fehlender Gedankenstrich. Beide sind korrigiert. Die Wortfehlerquote liegt damit um 0,1–0,2 %.

Die Texte sind vor der Rechnung mit SHA-256 eingefroren (`texte/SHA256SUMS.txt`).

## 2. Ergebnis

`e11.py` lief unverändert; nur die Liste der Nachahmer wird gesetzt (`ergebnisse/e11x.py`). Der Kontrolllauf W0 ergibt wie bisher +0,33.

| Variante | Nachahmer | Wort-Delta: AUC | Proben mindestens so heine-nah wie der Kandidat | log10 LR | 4-Gramme: AUC | log10 LR | **Wertung H1 : H3** |
|---|---|---:|---:|---:|---:|---:|---:|
| W0 | die bisherigen vier | 0,811 | 19/62 (31 %) | +0,35 | 0,803 | +0,31 | **+0,33** |
| W1 | vier + Meißner + Hartmann + Dingelstedt | 0,842 | 29/119 (24 %) | +0,45 | 0,820 | +0,59 | **+0,50** (Grenze) |
| W2 | alle neun (mit Gaudy und Beck) | 0,839 | 35/149 (23 %) | +0,47 | 0,815 | +0,69 | **+0,50** (Grenze) |
| W3 | nur Meißner, Hartmann, Dingelstedt | 0,877 | 10/57 (18 %) | +0,58 | 0,840 | +0,27 | +0,50 (Grenze) |
| W5 | vier + Meißner | 0,831 | 24/81 | +0,37 | 0,822 | +0,42 | +0,39 |
| W6 | vier + Hartmann | 0,824 | 21/81 | +0,42 | 0,814 | +0,42 | +0,42 |
| W7 | vier + Dingelstedt | 0,823 | 22/81 | +0,40 | 0,798 | +0,42 | +0,41 |

**Wort-Delta je Verfasser:** Proben, die mindestens so heine-nah sind wie der Kandidat.

| Verfasser | Proben |
|---|---|
| Müller v. K. | 6/15 |
| Mommsen | 7/17 |
| Storm | 3/7 |
| Scherr | 3/23 |
| Beck | 3/11 |
| **Meißner** | **5/19** |
| Gaudy | 3/19 |
| **Dingelstedt** | **3/19** |
| **Hartmann** | **2/19** |

Die Versmerkmale bestehen das Tor in keiner Variante mit allen Verfassern.

## 3. Folgen für die Bilanz

Gerechnet mit den Formeln aus 8.1; die übrige H3-Masse bleibt unverändert.

| | W0 bisher (+0,33) | W2 alle neun (+0,50) | W2, 4-Gramme neutral (+0,23) |
|---|---:|---:|---:|
| Hauptwertung 1 : 5 bis 1 : 3 | 55–67 % | 63–74 % | 50–62 % |
| Offene Fälle als unecht, 1 : 7 | 47 % | 55 % | 41 % |
| Skeptisch, Referenzklasse | 23–33 % | 29–41 % | 19–29 % |
| Skeptisch 1 : 7 | 17 % | 23 % | 15 % |
| Skeptisch 1 : 20 bis 1 : 7 | 7–17 % | 9–23 % | 6–15 % |

## 4. Deutung

1. **Wie erwartet heben auch die drei politischen Lyriker den Heine-Wert.** Im Wort-Delta liegen sie seltener auf Höhe des Kandidaten als die bisherigen vier. Am heine-nächsten ist noch Meißner (5/19), am fernsten Hartmann (2/19).
2. **Ursache ist wahrscheinlich die Gattung, nicht die Heine-Nähe.** Die gezogenen Seiten sind überwiegend Zeit-, Tendenz- und Erzähllyrik: Balladen auf die böhmische Geschichte, Freiheitslieder, Satiren auf Höfe und Städte. Das Wort-Delta misst Funktionswörter und Pronomen. Dort unterscheiden sich solche Texte vom Liebeslied im *Buch der Lieder* stärker als die Liederbücher von Storm und Mommsen.
3. **Die Wertung stößt an die Grenze von +0,5.** Ohne die Begrenzung läge sie bei rund +0,58. Die Grenze wirkt, wie das Protokoll es vorsieht: Ein einzelnes Bündel stilometrischer Befunde soll nicht mehr als einen halben Zehnerlogarithmus zählen.
4. **Vorbehalt Zeichen-4-Gramme, verschärft.** Auch hier erreicht keiner der neun Verfasser den Kandidatenwert (0/149). Der Quotient wächst darum nur mit der Probenzahl, von +0,31 auf +0,69. Das ist kein Befund. Ohne dieses Maß bleibt eine Wertung von +0,23 (Hauptwertung 50–62 %), also etwa der Stand vor der Erweiterung.
5. **Die Grenzen der Methode zeigen sich jetzt deutlich.** Wer in der Rezeption als Heine-Nachahmer gilt, liegt im Wort-Delta durchweg *nicht* näher an Heine als Storm oder Mommsen. Stilometrische Nähe und Rezeptionsnähe fallen auseinander. Für die geplante Abstufung (Entwurf, Abschnitt 5) heißt das: Wahrscheinlich gilt der Fall „LR_a ≈ LR_b“ oder sogar „LR_a > LR_b“. Die engen Nachahmer wären dann stilometrisch nicht schwerer vom Kandidaten zu trennen als die fernen. Prüfen lässt sich das erst mit den Belegen aus Fassung 2 und mit Steinmann.
6. **Für die Kernaussage ändert sich nichts.** Alle Varianten liegen zwischen etwa 50 und 74 % (ausgewogen) und zwischen 6 und 41 % (skeptisch). „Zweifelhaft“ trägt, „wahrscheinlich echt“ trägt auch mit neun Nachahmern nicht sicher, „unecht“ nicht.

## 5. Dateien

- `texte/`: die drei eingefrorenen Texte mit `SHA256SUMS.txt`;
- `korrektur/`: Korrekturlisten, Änderungsprotokolle, Seitenauswahl (`auswahl_*.json`), Einzelseiten (`seiten.tgz`);
- `werkzeug/`: Skripte für Ziehung, Reinigung und Korrektur;
- `ergebnisse/`: W0–W7 als JSON und `e11x.py`.

## Nachtrag vom 31. Oktober 2026, 22 Uhr: Einschränkungen der Deutung

Nach Durchsicht mit dem Verfasser gilt für alle explorativen Erweiterungen der Nachahmerklasse (Gaudy, Beck, Meißner, Hartmann, Dingelstedt, Steinmann 1861, Teilklassen H3a/H3b):

1. **Gattung statt Heine-Nähe.** Die neu aufgenommenen Proben sind überwiegend Zeit-, Tendenz-, Erzähl- und Balladenlyrik. Das Wort-Delta über die häufigsten Wörter (Pronomen, Artikel, Partikeln) reagiert stark auf die Gattung. Dass diese Proben seltener auf Höhe des Kandidaten liegen, ist deshalb vor allem ein Gattungsbefund. Der Anstieg der Wertung H1 : H3 ist in diesem Sinn eher ein Artefakt der Zusammensetzung der Vergleichsklasse als eine Eigenschaft des Kandidaten.
2. **Die Einteilung H3a/H3b sortiert nach Nachweislage, nicht nach Nähe.** Das Kriterium K2 (zeitgenössische Kritik bis 1860) ist vom Ergebnis unabhängig, trifft aber philologisch schief: Storm und Mommsen stehen mangels Beleg in H3b, obwohl ihr Liedton dem *Buch der Lieder* nahesteht; Meißner steht in H3a, Hartmann und Dingelstedt in H3b, obwohl alle drei überwiegend politische Lyrik schreiben. Zudem fällt die Einteilung weitgehend mit der Gattung zusammen.
3. **Zufallsseiten treffen nicht das Heinische dieser Autoren.** Was die Zeitgenossen an ihnen heinisch fanden, waren bestimmte Lieder. Diese gehen in der Ziehung über ganze Bände unter.
4. **Steinmann 1861** ahmt überwiegend den späten, satirischen Heine nach; der Vergleich mit dem *Buch der Lieder* sagt über die Fähigkeit eines Fälschers, den frühen Ton zu treffen, nichts.
5. **Zeichen-4-Gramme:** Der Quotient entsteht allein aus der Glättung und den Probenzahlen (auch die Heine-Klassen erreichen den Kandidatenwert nicht). Er ist kein Befund.
6. **Folgerung.** Belastbar ist nur die schwache Aussage, dass ein Funktionswort-Maß Rezeptionsnähe nicht erfasst. Die Sätze in der Deutung oben, die weiter gehen (etwa „ein Nachahmer, den die Zeitgenossen als heinisch empfanden, ist stilometrisch nicht leichter zu fassen“), sind in diesem Sinn einzuschränken. Die Rechnungen gehen nicht in den Aufsatz ein.
7. **Ausblick (nicht gerechnet).** Eine philologisch tragfähige Gegenprobe würde je Nachahmer die Lieder im Heine-Ton nach vorab festgelegten formalen und inhaltlichen Kriterien (Gattung, Strophe, Thema, nicht nach Wortgebrauch) auswählen. Eine Überschlagsrechnung mit den vorhandenen Liederproben (Storm, Mommsen, Müller, Gaudy nur Lieder, Beck) ergibt etwa +0,29 statt +0,33 gegenüber H3, also eher eine leichte Minderung des Heine-Werts.
