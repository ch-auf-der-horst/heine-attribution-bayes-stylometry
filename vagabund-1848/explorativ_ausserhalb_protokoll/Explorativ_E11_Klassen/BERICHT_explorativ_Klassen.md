# E-11 mit Teilklassen H1a/H1b/H1c und H3a/H3b: explorative Rechnung

Stand: 31. Oktober 2026. **Diese Rechnung steht außerhalb des Auswertungsprotokolls und gehört nicht in den Aufsatz.**

**Grundlage:**
- Protokollerweiterung Fassung 2 (16:55 Uhr) und Nachtrag 2a (19:05 Uhr). Beide wurden vor der Rechnung festgehalten und eingefroren.
- Die Rechnung lief erst danach.
- Alle Festlegungen sind unverändert umgesetzt. Abweichungen und Ergänzungen stehen in Abschnitt 5.

## 1. Texte und Textprüfung

| Klasse | Text | Tokens | Proben 548 | Proben 274 |
|---|---|---:|---:|---:|
| H1a | A2: Heine-Drucke vor März 1824 (wie bisher) | – | 30 | 60 |
| H1b | 21 halbanonyme Gedichte 1824–26, Erstdruck nach DHA I | 1.167 | 2 (beschreibend) | 4 |
| H1b+ | dazu Agrippina 2, 9, <25>–<32>, „Wenn junge Herzen brechen“ | 2.104 | 3 | 7 |
| H1c | *Neue Gedichte* 1844 ohne Zeitgedichte, Ziehung bis 11.000 | 11.052 | 20 | 40 |
| H1c (Gegenprobe) | mit Zeitgedichten | 11.363 | 20 | 41 |
| H3a | Gaudy, Steinmann 1861, Meißner | – | 58 | 117 |
| H3b | Beck, Hartmann, Dingelstedt, Müller, Scherr, Storm, Mommsen | – | 111 | 229 |

**Steinmann 1861:**
- Zerlegung in 165 Gedichte. Der Pool ohne „IX.“ und „VI.“ umfasst 147 Gedichte. Gezogen wurden 105 Gedichte mit 11.029 Tokens.
- Stichprobe mit dem Startwert 20261101: „Scheintodt.“ (Bd. 1, S. 40–41), „Neue Mordgeschichte.“ (Bd. 1, S. 54–55) und „Vorahnung.“ (Bd. 2, S. 77–78). Gelesen wurden sechs Druckseiten mit rund 250 Wörtern, Zeile für Zeile am Scan.
- Ergebnis: **0 Abweichungen.** „Todtemhemde“ und „mögte“ stehen so im Druck.

**H1b gegen das *Buch der Lieder*:**
- 15 der 21 Gedichte haben über die ersten vier Wörter eine Entsprechung im BdL, alle in der *Heimkehr*.
- Diese Gedichte sind für die jeweilige Probe aus der A1-Bezugsklasse entfernt. Die Liste steht in `k_klassen.json`.
- Ohne Entsprechung: Agrippina 1, 5, 6, 7, 10 und Rheinblüthen III.

**Eingefroren:** Alle neuen Texte sind vor der Rechnung mit SHA-256 eingefroren (`texte/SHA256SUMS.txt`, 19:11 Uhr). Ein zweiter Lauf reproduziert `k_klassen.json` bitgenau.

## 2. Hauptvariante (Proben zu 548 Tokens)

**Kandidat:** s = +0,004 (Wort-Delta), +0,234 (Zeichen-4-Gramme), +0,226 (Versmerkmale).

| Teilklasse | Wort-Delta: Proben mindestens so heine-nah wie der Kandidat | Median s |
|---|---:|---:|
| H1a | 21/30 | +0,056 |
| H1b (beschreibend) | 2/2 | +0,150 |
| H1c | 14/20 | +0,032 |
| **H3a** | **12/58 (21 %)** | |
| Gaudy | 3/19 | −0,122 |
| Steinmann 1861 | 4/20 | −0,061 |
| Meißner | 5/19 | −0,082 |
| **H3b** | **27/111 (24 %)** | |
| darin Müller 6/15, Mommsen 7/17, Storm 3/7, Beck 3/11, Dingelstedt 3/19, Scherr 3/23, Hartmann 2/19 | | |

| | Wort-Delta | Zeichen-4-Gramme | Versmerkmale |
|---|---:|---:|---:|
| AUC H1 (H1a+H1c) gegen H3 | 0,841 | 0,802 | 0,671 (Tor nicht bestanden) |
| log10 LR, Gewichte 1 : 1 / 1 : 1 | +0,48 | +0,49 | – |
| **Wertung H1 : H3** | | | **+0,48** |
| Wertung, 4-Gramme neutral | | | +0,24 |

**Getrennt nach Nachahmerklassen (Wort-Delta):**
- LR_a = H1 : H3a ≈ 3,3 (log10 +0,51);
- LR_b = H1 : H3b ≈ 2,8 (log10 +0,45).

**Empfindlichkeit und Gegenproben:**
- Alle Gewichtungen (H1 2 : 1 und 1 : 2, H3 1 : 3 und 3 : 1) liegen zwischen +0,45 und +0,50.
- Beck in H3a: +0,50. Gaudy nur mit den Liedern: +0,45. H1c mit den Zeitgedichten: +0,47.
- Mit neutralen 4-Grammen liegen alle Läufe zwischen +0,23 und +0,25.

## 3. Variante K (Proben zu 274 Tokens, Gegenprobe)

**Kandidat:** Die beiden Hälften liegen im Wort-Delta bei −0,005 und −0,009 (s_K = −0,007) und bei den 4-Grammen bei +0,172 und +0,177. Beide Hälften verhalten sich also gleich.

**Wort-Delta (AUC 0,811):**

| Teilklasse | mindestens so heine-nah |
|---|---:|
| H1a | 44/60 |
| H1b | 4/4 |
| H1c | 29/40 |
| H3a | 27/117 (23 %) |
| H3b | 74/229 (32 %) |

log10 LR +0,45.

**Zeichen-4-Gramme (AUC 0,766):**

| Teilklasse | mindestens so heine-nah |
|---|---:|
| H1a | 5/60 |
| H1b | 2/4 |
| H1c | 0/40 |
| H3a | 0/117 |
| H3b | 3/229 |

log10 LR +1,32.

**Wertung:** in allen Läufen an der Grenze von **+0,50**. Ungekappt liegt sie bei 0,75–1,05, mit neutralen 4-Grammen bei +0,20 bis +0,25. Die Versmerkmale sind in K nicht gerechnet (s. 5).

## 4. Bilanz

Die Bilanz ist mit den Formeln aus 8.1 gerechnet; die übrige H3-Masse bleibt unverändert.

| | bisher, E-11 mit vier Nachahmern (+0,33) | **Klassen, 548 (+0,48)** | Klassen, 4-Gramme neutral (+0,24) | K (+0,50) |
|---|---:|---:|---:|---:|
| Hauptwertung 1 : 5 bis 1 : 3 | 55–67 % | **62–73 %** | 50–63 % | 63–74 % |
| Offene Fälle als unecht, 1 : 7 | 47 % | 54 % | 42 % | 55 % |
| Skeptisch, Referenzklasse | 23–33 % | 28–40 % | 20–29 % | 29–41 % |
| Skeptisch 1 : 7 | 17 % | 22 % | 15 % | 23 % |
| Skeptisch 1 : 20 bis 1 : 7 | 7–17 % | 9–22 % | 6–15 % | 9–23 % |

## 5. Deutung

1. **Die Abstufung von H3 trägt stilometrisch nichts aus.** Der Kandidat liegt im Wort-Delta nicht näher an den rezeptionsnahen Nachahmern als an den fernen. In der Hauptvariante liegen 21 % der H3a-Proben gegen 24 % der H3b-Proben auf Höhe des Kandidaten, in K 23 % gegen 32 %. Das ist der vorab beschriebene Fall „LR_a ≈ LR_b“ (Fassung 1, Abschnitt 5). Er ist ein Befund über die Grenzen der Methode: Rezeptionsnähe und Nähe in den häufigsten Wörtern fallen auseinander. Auch Steinmann 1861 (4/20), der Fälscher, liegt nicht näher am Kandidaten als Storm oder Mommsen.
2. **Die Abstufung von H1 trägt ebenfalls wenig aus.** Der frühe und der mittlere Heine verhalten sich zum Kandidaten gleich: H1a 70 %, H1c 70 % (K: 73 % und 73 %). Die zweite Garnitur H1b liegt in allen Proben auf Höhe des Kandidaten oder heine-näher (2/2, in K 4/4). Ihr Median s ist der höchste aller Klassen. Bei 4 bis 7 Proben ist das nur ein Hinweis, aber er geht in die erwartete Richtung: Die halbanonymen Heimkehr-Vorstufen sind dem *Buch der Lieder* naturgemäß besonders nah.
3. **Die Wertung entspricht fast genau dem gepoolten Lauf mit allen neun Nachahmern.** Dort lag sie bei +0,50 (gekappt), mit neutralen 4-Grammen bei +0,23. Die Mischung macht das Ergebnis unabhängig davon, wie viele Proben auf welche Klasse fallen. Am Stand ändert sie nichts.
4. **Vorbehalt Zeichen-4-Gramme, jetzt deutlicher.**
   - In der Hauptvariante erreichen auch die Heine-Klassen H1a und H1c den Kandidatenwert nie (0/30 und 0/20), ebenso keiner der Nachahmer. Der Kandidat ist in diesem Maß extremer als fast alle Proben, ob von Heine oder nicht. Der Quotient von +0,49 ergibt sich darum nur aus dem Verhältnis der Probenzahlen.
   - In K steigt er auf +1,32, weil H1b mit 2/4 Treffern ein Drittel des Gewichts trägt. Das ist ein Artefakt kleiner Zahlen.
   - Belastbar ist darum nur die Variante „4-Gramme neutral“: +0,20 bis +0,25.
5. **Für die Kernaussage ändert sich nichts.** Ausgewogen liegen alle Varianten zwischen 50 und 74 %, skeptisch zwischen 6 und 41 %. „Zweifelhaft“ trägt; „wahrscheinlich echt“ und „unecht“ tragen nicht.

**Abweichungen und Ergänzungen gegenüber Fassung 2/2a:**
- Die Versmerkmale bilden ihre Proben nach Verszahl, nicht nach Tokens. In Variante K sind sie deshalb nicht gerechnet. In der Hauptvariante bestehen sie das Tor nicht (AUC 0,67), wie in allen bisherigen Läufen.
- Für H1b+ wurde die A1-Bezugsklasse ohne alle Entsprechungen des ganzen Textes gebildet, nicht je Probe, weil die Zusatztexte keine Gedichtkennung tragen. Gefunden wurden dieselben 15 Entsprechungen.
- Die Tabellen geben nur die Hauptgewichte wieder; alle Läufe stehen in `k_klassen.json`.

## 6. Dateien

- `texte/`: Steinmann_1861 mit Auswahlliste und `SHA256SUMS.txt`. Die Heine-Texte (H1b_Haupt, H1b_plus, H1b_manifest, H1c_Haupt, H1c_mitZeit) sind nicht beigegeben (DHA bzw. Heine-Portal); ihre Prüfsummen in `SHA256SUMS.txt` belegen die verwendeten Fassungen.
- `werkzeug/`: `h1b.py` und `ziehen.py`.
- `ergebnisse/`: `e11k.py` und `k_klassen.json`.

## Nachtrag vom 31. Oktober 2026, 22 Uhr: Einschränkungen der Deutung

Nach Durchsicht mit dem Verfasser gilt für alle explorativen Erweiterungen der Nachahmerklasse (Gaudy, Beck, Meißner, Hartmann, Dingelstedt, Steinmann 1861, Teilklassen H3a/H3b):

1. **Gattung statt Heine-Nähe.** Die neu aufgenommenen Proben sind überwiegend Zeit-, Tendenz-, Erzähl- und Balladenlyrik. Das Wort-Delta über die häufigsten Wörter (Pronomen, Artikel, Partikeln) reagiert stark auf die Gattung. Dass diese Proben seltener auf Höhe des Kandidaten liegen, ist deshalb vor allem ein Gattungsbefund. Der Anstieg der Wertung H1 : H3 ist in diesem Sinn eher ein Artefakt der Zusammensetzung der Vergleichsklasse als eine Eigenschaft des Kandidaten.
2. **Die Einteilung H3a/H3b sortiert nach Nachweislage, nicht nach Nähe.** Das Kriterium K2 (zeitgenössische Kritik bis 1860) ist vom Ergebnis unabhängig, trifft aber philologisch schief: Storm und Mommsen stehen mangels Beleg in H3b, obwohl ihr Liedton dem *Buch der Lieder* nahesteht; Meißner steht in H3a, Hartmann und Dingelstedt in H3b, obwohl alle drei überwiegend politische Lyrik schreiben. Zudem fällt die Einteilung weitgehend mit der Gattung zusammen.
3. **Zufallsseiten treffen nicht das Heinische dieser Autoren.** Was die Zeitgenossen an ihnen heinisch fanden, waren bestimmte Lieder. Diese gehen in der Ziehung über ganze Bände unter.
4. **Steinmann 1861** ahmt überwiegend den späten, satirischen Heine nach; der Vergleich mit dem *Buch der Lieder* sagt über die Fähigkeit eines Fälschers, den frühen Ton zu treffen, nichts.
5. **Zeichen-4-Gramme:** Der Quotient entsteht allein aus der Glättung und den Probenzahlen (auch die Heine-Klassen erreichen den Kandidatenwert nicht). Er ist kein Befund.
6. **Folgerung.** Belastbar ist nur die schwache Aussage, dass ein Funktionswort-Maß Rezeptionsnähe nicht erfasst. Die Sätze in der Deutung oben, die weiter gehen (etwa „ein Nachahmer, den die Zeitgenossen als heinisch empfanden, ist stilometrisch nicht leichter zu fassen“), sind in diesem Sinn einzuschränken. Die Rechnungen gehen nicht in den Aufsatz ein.
7. **Ausblick (nicht gerechnet).** Eine philologisch tragfähige Gegenprobe würde je Nachahmer die Lieder im Heine-Ton nach vorab festgelegten formalen und inhaltlichen Kriterien (Gattung, Strophe, Thema, nicht nach Wortgebrauch) auswählen. Eine Überschlagsrechnung mit den vorhandenen Liederproben (Storm, Mommsen, Müller, Gaudy nur Lieder, Beck) ergibt etwa +0,29 statt +0,33 gegenüber H3, also eher eine leichte Minderung des Heine-Werts.
