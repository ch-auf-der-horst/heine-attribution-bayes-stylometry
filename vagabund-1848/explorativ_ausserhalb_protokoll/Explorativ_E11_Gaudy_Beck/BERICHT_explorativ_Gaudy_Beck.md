# E-11 mit Gaudy und Beck – explorative Rechnung

Stand: 31. Oktober 2026. **Diese Rechnung gehört nicht zum Auswertungsprotokoll und nicht in den Aufsatz.** Sie dient nur der Orientierung. Für den Aufsatz müsste die Erweiterung der Nachahmerliste vorher datiert festgelegt werden, mit Auswahlkriterien, die nicht vom Ergebnis abhängen.

## 1. Texte

| Text | Grundlage | Umfang (Tokens) | Proben à 548 |
|---|---|---:|---:|
| Gaudy, *Erato* (1829), Abteilung „Freud' und Leid“ (Nr. I–LVI, S. 1–120), dazu vier Almanachgedichte 1833 | `Gaudy_1829_1833.txt` | 10.641 | 19 |
| dasselbe, nur Nr. I–XLVI (Lieder, ohne Balladen, „Bilder“ und freie Rhythmen) plus Almanach | `Gaudy_Lieder_1829_1833.txt` | 5.721 | 10 |
| Beck, *Stille Lieder*, Bd. 1 (1840), alle Gedichte (S. 1–100) | `Beck_1840.txt` | 6.575 | 11 |

**Wie die Texte entstanden sind.** Die vorhandene Texterkennung war unbrauchbar (Beck) oder mäßig (Gaudy). Beide Bände wurden deshalb neu mit einer Fraktur-Erkennung gelesen (Tesseract 5, Modell `deu_latf`, 300 dpi). Danach:

- regelhafte Reinigung: langes s, Fraktur-Ligaturen (`<` für ch, `>` für ck), Seitenzahlen, Bogensignaturen und „Digitized by Google“ entfernt, Worttrennungen aufgelöst;
- Korrektur jeder Seite:
  - Gaudy durchgehend Seite für Seite am Seitenbild;
  - Beck etwa zur Hälfte am Seitenbild, sonst als Textdurchsicht mit Bildprüfung im Zweifel;
  - die stark durchgeschlagenen Beck-Seiten wurden am Bild neu abgeschrieben.

Jede Änderung steht in `korrektur/` (Korrekturlisten, Änderungsprotokolle, Einzelseiten).

**Entfernt** wurden:

- Google- und Bibliotheksvorsatz, Titelblätter, Widmungen, Abteilungstitel;
- Fußnoten, Verlagsanzeigen, „Fortsetzung im zweiten Bändchen“;
- Gedichtnummern;
- ein italienisches Motto und eine lateinische Zeile bei Gaudy;
- die Widmungszeile an Fouqué.

Gedichttitel blieben stehen, wie bei den übrigen E-11-Texten.

**Stichprobe nach der Korrektur.** Zufällig gezogen (Startwert 20261031) und am Bild vollständig gelesen:

- Beck: 6 Seiten, 454 Wörter;
- Gaudy: 4 Seiten, 322 Wörter.

Ergebnis:

- **0 Wortfehler** (95-%-Obergrenze rund 0,4 %);
- bei Beck 4 fehlende schließende Anführungszeichen. Die Texterkennung lässt dieses Zeichen offenbar oft aus. Die vier Stellen sind korrigiert; im übrigen Beck-Text dürfte es weitere solche Lücken geben. Auf das Wort-Delta wirkt das nicht, auf die Zeichen-4-Gramme nur minimal.

Die Texte sind vor der Rechnung mit SHA-256 eingefroren (`texte/SHA256SUMS.txt`).

## 2. Rechnung

`e11.py` lief unverändert in einer Arbeitskopie. Nur die Liste der Nachahmer wird über eine Umgebungsvariable gesetzt (`ergebnisse/e11x.py`). Der Kontrolllauf V0 mit den vier bisherigen Verfassern reproduziert `e11.json` (Stand nach der Korrektur vom 31.10.) bitgenau: +0,33.

| Variante | Nachahmer | Wort-Delta: AUC | Proben mind. so heine-nah | LR (log10) | 4-Gramme: AUC | LR (log10) | **Wertung H1 : H3** |
|---|---|---:|---:|---:|---:|---:|---:|
| V0 | bisherige vier | 0,811 | 19/62 (31 %) | +0,35 | 0,803 | +0,31 | **+0,33** |
| V1 | vier + Gaudy + Beck | 0,816 | 25/92 (27 %) | +0,40 | 0,800 | +0,48 | **+0,44** |
| V3 | vier + Gaudy (nur Lieder) + Beck | 0,800 | 24/83 (29 %) | +0,38 | 0,776 | +0,43 | **+0,40** |
| V4 | vier + Gaudy | 0,834 | 22/81 | +0,40 | 0,813 | +0,42 | +0,41 |
| V5 | vier + Beck | 0,792 | 22/73 | +0,36 | 0,789 | +0,38 | +0,37 |
| V2 | nur Gaudy + Beck | 0,828 | 6/30 (20 %) | +0,52 | 0,796 | 0,00 | +0,26 |

Die Einzelläufe nur mit Gaudy (V6) oder nur mit Beck (V7) haben zu wenige Proben. Bei V7 besteht nur das Versmaß-Maß das Tor, mit 2 Proben. Beide sind nicht aussagekräftig (`ergebnisse/V6.json`, `V7.json`).

**Wort-Delta je Verfasser:** Proben, die mindestens so heine-nah sind wie der Kandidat.

| Verfasser | Anteil | Quote |
|---|---:|---:|
| Müller v. K. | 6/15 | 40 % |
| Mommsen | 7/17 | 41 % |
| Storm | 3/7 | 43 % |
| Scherr | 3/23 | 13 % |
| **Gaudy** | **3/19** | **16 %** |
| **Beck** | **3/11** | **27 %** (5/11 auf der Heine-Seite) |

Die Versmerkmale bestehen das Tor in keiner Variante mit allen Verfassern.

## 3. Folgen für die Bilanz

Gerechnet mit denselben Formeln wie in 8.1. Die übrige H3-Masse bleibt unverändert, ausgewogen +0,20 und skeptisch −0,40.

| | V0 bisher (+0,33) | V1 (+0,44) | V3 (+0,40) | V2 nur G+B (+0,26) | V1, 4-Gramme neutral (+0,20) |
|---|---:|---:|---:|---:|---:|
| Hauptwertung 1 : 5 bis 1 : 3 | 55–67 % | 61–72 % | 59–70 % | 51–64 % | 48–61 % |
| Offene Fälle als unecht, 1 : 7 | 47 % | 52 % | 50 % | 43 % | 40 % |
| Skeptisch, Referenzklasse | 23–33 % | 27–38 % | 25–36 % | 20–30 % | 18–27 % |
| Skeptisch 1 : 7 | 17 % | 21 % | 20 % | 15 % | 14 % |
| Skeptisch 1 : 20 bis 1 : 7 | 7–17 % | 8–21 % | 8–20 % | 6–15 % | 5–14 % |

## 4. Deutung

1. **Die Erwartung bestätigt sich nicht.** Gaudy und Beck sind im Wortschatz-Delta *weniger* oft auf Höhe des Kandidaten als die bisherigen Nachahmer, besonders Gaudy. Nimmt man sie hinzu, steigt die Wertung H1 : H3 leicht (+0,33 → +0,40 bis +0,44), statt zu fallen. Der „Heine-Ton“ dieser Nachahmer zeigt sich offenbar eher in Motiven und Pointen als in der Verteilung der häufigsten Wörter, die das Delta misst.
2. **Die Verschiebung ist klein.** Sie liegt innerhalb dessen, was die Textkorrektur vom 31.10. in die Gegenrichtung bewirkt hat (−0,10). Alle Varianten halten die Kernaussage: „zweifelhaft“ trägt, „wahrscheinlich echt“ nicht, „unecht“ auch nicht.
3. **Vorbehalt Zeichen-4-Gramme.** Kein Nachahmer erreicht hier den Kandidatenwert (0 Treffer). Der Quotient wächst darum fast nur mit der Zahl der Proben (0/62 → 0/92 hebt log10 LR von 0,31 auf 0,48). Das ist kein inhaltlicher Befund. Die Variante „4-Gramme neutral“ (letzte Spalte) zeigt, was ohne dieses Maß bleibt: 48–61 %.
4. **Vorbehalt Auswahl.** Gaudy und Beck wurden *nach* Kenntnis der bisherigen Ergebnisse gewählt, wenn auch mit der Erwartung, dass sie der Heine-These schaden. Für den Aufsatz taugt die Rechnung erst nach einer datierten Festlegung, welche Nachahmer nach welchem Kriterium dazugehören. Dann gehörten wohl auch Meißner, Hartmann und Dingelstedt dazu, mit dem Vorbehalt der Gattung.

## 5. Dateien

- `texte/`: die drei eingefrorenen Texte mit `SHA256SUMS.txt`;
- `korrektur/`: Korrekturlisten, Änderungsprotokolle (CSV), alle Einzelseiten vor und nach der Korrektur (`seiten.tgz`);
- `werkzeug/`: Reinigungs- und Korrekturskripte;
- `ergebnisse/`: V0–V7 als JSON, dazu `e11x.py`;
- `arbeit/lexikon.tsv`: Wortliste aus dem Korpus (enthält Heine-Portal-Material), **nicht veröffentlichen**.

## Nachtrag vom 31. Oktober 2026, 22 Uhr: Einschränkungen der Deutung

Nach Durchsicht mit dem Verfasser gilt für alle explorativen Erweiterungen der Nachahmerklasse (Gaudy, Beck, Meißner, Hartmann, Dingelstedt, Steinmann 1861, Teilklassen H3a/H3b):

1. **Gattung statt Heine-Nähe.** Die neu aufgenommenen Proben sind überwiegend Zeit-, Tendenz-, Erzähl- und Balladenlyrik. Das Wort-Delta über die häufigsten Wörter (Pronomen, Artikel, Partikeln) reagiert stark auf die Gattung. Dass diese Proben seltener auf Höhe des Kandidaten liegen, ist deshalb vor allem ein Gattungsbefund. Der Anstieg der Wertung H1 : H3 ist in diesem Sinn eher ein Artefakt der Zusammensetzung der Vergleichsklasse als eine Eigenschaft des Kandidaten.
2. **Die Einteilung H3a/H3b sortiert nach Nachweislage, nicht nach Nähe.** Das Kriterium K2 (zeitgenössische Kritik bis 1860) ist vom Ergebnis unabhängig, trifft aber philologisch schief: Storm und Mommsen stehen mangels Beleg in H3b, obwohl ihr Liedton dem *Buch der Lieder* nahesteht; Meißner steht in H3a, Hartmann und Dingelstedt in H3b, obwohl alle drei überwiegend politische Lyrik schreiben. Zudem fällt die Einteilung weitgehend mit der Gattung zusammen.
3. **Zufallsseiten treffen nicht das Heinische dieser Autoren.** Was die Zeitgenossen an ihnen heinisch fanden, waren bestimmte Lieder. Diese gehen in der Ziehung über ganze Bände unter.
4. **Steinmann 1861** ahmt überwiegend den späten, satirischen Heine nach; der Vergleich mit dem *Buch der Lieder* sagt über die Fähigkeit eines Fälschers, den frühen Ton zu treffen, nichts.
5. **Zeichen-4-Gramme:** Der Quotient entsteht allein aus der Glättung und den Probenzahlen (auch die Heine-Klassen erreichen den Kandidatenwert nicht). Er ist kein Befund.
6. **Folgerung.** Belastbar ist nur die schwache Aussage, dass ein Funktionswort-Maß Rezeptionsnähe nicht erfasst. Die Sätze in der Deutung oben, die weiter gehen (etwa „ein Nachahmer, den die Zeitgenossen als heinisch empfanden, ist stilometrisch nicht leichter zu fassen“), sind in diesem Sinn einzuschränken. Die Rechnungen gehen nicht in den Aufsatz ein.
7. **Ausblick (nicht gerechnet).** Eine philologisch tragfähige Gegenprobe würde je Nachahmer die Lieder im Heine-Ton nach vorab festgelegten formalen und inhaltlichen Kriterien (Gattung, Strophe, Thema, nicht nach Wortgebrauch) auswählen. Eine Überschlagsrechnung mit den vorhandenen Liederproben (Storm, Mommsen, Müller, Gaudy nur Lieder, Beck) ergibt etwa +0,29 statt +0,33 gegenüber H3, also eher eine leichte Minderung des Heine-Werts.
