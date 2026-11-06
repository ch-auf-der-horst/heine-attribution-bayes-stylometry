# Protokollerweiterung (Entwurf), Nachtrag 2a: H1b, H1c, kleine Proben, Steinmann

Festgehalten am 31. Oktober 2026, 19:40 Uhr (MEZ), vor jeder Rechnung mit H1b, H1c oder Steinmann 1861. Eingefroren durch SHA-256 (`Protokollerweiterung_Nachahmerklassen_Fassung2a.sha256`). Der Nachtrag ergänzt Fassung 2 (16:55 Uhr) und ersetzt sie nicht.

**Grundlage:** die vom Verfasser bereitgestellte Liste `Heine/H1b_H1c_Abgleich_2026-10-31/H1b_Gedichtliste_und_Dateiabgleich.md` und die H1c-Dateien im selben Ordner.

**Entscheidung des Verfassers vom 31.10., 19:03 Uhr:** H1b wird mit kleineren Proben gerechnet.

**Beim Festhalten bekannt:**
- die Länge des Kandidaten: 548 Tokens, also genau eine Probe;
- der Umfang der Texte;
- keine Ergebnisse zu H1b, H1c oder Steinmann.

## 1. H1b: Textgrundlage und Auswahl

**Hauptrechnung: 21 Gedichte der drei halbanonymen Druckgruppen** in der Fassung des Erstdrucks, wie ihn die DHA I bietet. Das sind die linken Seiten (Zeuge J) und der Anhang S. 481–484.

| Gruppe | Gedichte | DHA I |
|---|---|---|
| *Agrippina* 1824, „Lieder von ****e“ | Nr. 1, 3, 5, 6, 7, 8, 10, 11 | S. 482–483, 242, 234, 292–294 |
| *Rheinblüthen* 1825, „Kleine Gedichte von H.“ | Nr. I–VI | S. 258, 256–258, 481, 246, 246, 244 |
| *Biene* 1826, „Kleine Gedichte von H. H.“ | Nr. I–VII | S. 206, 274, 272, 244, 244, 256, 256 |

**Nicht in der Hauptrechnung:** *Agrippina* Nr. 2, 4 und 9. Die DHA I gibt für diese drei nur Verweise auf spätere Fassungen. Die vorhandene Datei enthält bei Nr. 4 die Fassung des *Romanzero* (1851), und Nr. 2 steht als *Emma* I zugleich in H1c.

**Gegenprobe H1b+:** die 21 Gedichte, dazu
- *Agrippina* Nr. 2 und 9 in der vorhandenen späteren Fassung;
- die nicht für den Druck bestimmten Texte <25>–<32> (DHA I, S. 525–530);
- „Wenn junge Herzen brechen“ (DHA I, S. 484).

Das Cuxhaven-Fragment <24> bleibt ausgeschlossen, weil nur die erste Strophe erhalten ist.

**Text:** nur Verstext; Gruppentitel, Nummern, Unterschriften und Vermerke wie „(Geschrieben im Herbste 1823.)“ fallen weg. Die Angleichung erfolgt wie bei allen Klassen mit `angleichen`.

**Bezugsklasse A1 ohne Doppelungen:** Für jede H1b-Probe wird die A1-Bezugsklasse ohne die Gedichte des *Buchs der Lieder* gebildet, die einem Gedicht der Probe entsprechen. Die Entsprechung wird über die ersten vier Wörter ermittelt und in der Ergebnisdatei aufgelistet, so wie bisher mit `calib.a1_minus` bei A2.

## 2. H1c: Textgrundlage und Auswahl

- **Grundlage:** `Gedichtmanifest.json`, *Neue Gedichte* 1844 nach Wikisource.
- **Hauptrechnung:** Gedichte der Abschnitte *Neuer Frühling*, *Verschiedene* und *Romanzen*.
- **Gegenprobe:** dazu die *Zeitgedichte*.
- **Auswahl:** Ganze Inhaltspositionen werden mit dem Startwert 20261031 zufällig gezogen, bis 11.000 Tokens erreicht sind, und dann in der Reihenfolge des Bandes angeordnet. Das entspricht Fassung 1, Abschnitt 3.2 (höchstens 20 Proben).
- *Emma* I („Er steht so starr“) bleibt in H1c, weil es in der H1b-Hauptrechnung nicht vorkommt.

## 3. Kleine Proben (Variante K)

1. **Hauptvariante:** Probengröße 548 wie bisher. H1b hat damit weniger als 3 Proben und wird nur beschreibend berichtet.
2. **Variante K: alle Klassen mit Proben zu 274 Tokens**, nicht nur H1b. Das gilt für H1a (A2), H1b, H1c, H3a und H3b. Merkmalsraum (Vokabular, Mittelwerte und Streuungen aus der Kalibrierung bei 548) und A1-Bezugsklasse (Blöcke zu 548) bleiben unverändert.
3. **Kandidat in Variante K:** Er wird in zwei Hälften zu 274 Tokens geteilt. Sein Wert s_K ist der Mittelwert der s-Werte beider Hälften. Berichtet wird außerdem der Wert jeder Hälfte.
4. **Tor und Wertung** wie bisher. Die Bilanz wird für beide Varianten getrennt berichtet. Die Hauptvariante bleibt maßgeblich, K ist eine Gegenprobe. Hat eine Teilklasse auch in K weniger als 3 Proben, wird sie dort ebenfalls nur beschreibend berichtet.

## 4. Steinmann 1861

- **Zerlegung:** Die bereinigten Dateien werden nach dem Gedichtregister in Gedichte zerlegt.
- **Auswahl:** wie in Fassung 2, Abschnitt 1.3, ohne „IX. Erzählendes“ und „VI. Sonette“, mit dem Startwert 20261031 und bis 11.000 Tokens.
- **Textqualität:** Vor der Rechnung werden drei zufällig gezogene Druckseiten (Startwert 20261101) am Scan gelesen.

## 5. Mischung

**Hauptvariante (548):**
- P(E | H1) aus H1a und H1c im Verhältnis 1 : 1. Gegenproben 2 : 1 und 1 : 2.
- P(E | H3) aus H3a und H3b im Verhältnis 1 : 1. Gegenproben 1 : 3 und 3 : 1.

**Variante K:** H1a : H1b : H1c = 1 : 1 : 1 mit den Gegenproben aus Fassung 2. Die Gewichte für H3 sind dieselben wie in der Hauptvariante.

**Schätzer:** Für jede Teilklasse wird der Anteil der Proben, die mindestens so heine-nah sind wie der Kandidat, mit dem bisherigen Schätzer `rate()` bestimmt. Je Maß gilt LR = Σ w_i · rate_i(H1) / Σ v_j · rate_j(H3). Die Wertung ist der Median der Maße, die das Tor bestehen, begrenzt auf ±0,5.

**Tor:** AUC von H1 gegen H3, aus den gepoolten Proben aller Teilklassen, wie in E-11.
