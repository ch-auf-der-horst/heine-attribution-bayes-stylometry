# Protokollerweiterung (Entwurf), Fassung 2: abgestufte Heine- und Nachahmerklassen

Festgehalten am 31. Oktober 2026, gegen 17:15 Uhr (MEZ). Eingefroren durch SHA-256, s. `Protokollerweiterung_Nachahmerklassen_Fassung2.sha256`.

Fassung 2 ergänzt Fassung 1 (`Protokollerweiterung_Nachahmerklassen_Entwurf.md`, 12:30 Uhr) und ersetzt sie nicht. Wo beide voneinander abweichen, gilt Fassung 2.

Status: **Entwurf außerhalb des Hauptprotokolls.** Für den Aufsatz gilt weiter E-11 nach Protokoll II.3a mit den am 31.10. korrigierten Texten, bis die Erweiterung ins Hauptprotokoll übernommen wird.

## 0. Wie die Erweiterung entstanden ist

Die Abstufung der Klassen ist eine philologische Einsicht, die sich erst im Verlauf der Arbeit ergeben hat. Sie folgt aus der eingehenden Beschäftigung mit Heines Lyrik, ihren Varianten und Erstdrucken, dem Briefwechsel und der zeitgenössischen Rezeption.

- **Bei den Nachahmern (H3):** Bekannte und in der Rezeption so genannte Heine-Nachahmer waren in der bisherigen Vergleichsgruppe kaum vertreten. Daher die Teilung in enge und übrige Nachahmer.
- **Bei Heine (H1):** Heines Lyrik ist nicht einheitlich. Ihr Stil verändert sich vom Frühwerk zum mittleren Werk. Heine selbst unterschied zudem Gedichte „zweiter Garnitur“ (Grappin), die er nur halbanonym unter Chiffre drucken ließ oder gar nicht veröffentlichte (DHA I, 858–860; Brief an Robert vom 27.5.1824). Die Frage ist deshalb nicht nur, *ob* die Kandidatengedichte Heine nahestehen, sondern auch, *welchem* Heine.

Zur Nachvollziehbarkeit ist festzuhalten, welche Ergebnisse bei der Festlegung schon bekannt waren:
- alle Ergebnisse der Hauptauswertung;
- die explorativen Läufe mit Gaudy, Beck, Meißner, Hartmann und Dingelstedt vom 31.10., auch die Werte je Verfasser (Berichte in `Explorativ_E11_Gaudy_Beck/` und `Explorativ_E11_Meissner_Hartmann_Dingelstedt/`).

**Nicht bekannt** waren Ergebnisse zu Steinmann 1861 und zu allen Heine-Teilklassen.

## 1. Nachahmerklassen: Belege und Zuordnung

### 1.1 Regeln zu den Kriterien K1–K3

Die Regeln aus Fassung 1 gelten unverändert und werden hier präzisiert:

- **R1:** Ein K2-Beleg muss den Verfasser betreffen; er muss nicht den verwendeten Band betreffen. H3a beschreibt eine Dichterhaltung, nicht einen einzelnen Band. Betrifft der Beleg ein anderes Werk, wird das vermerkt.
- **R2:** K2 verlangt ein ausdrückliches Urteil, den Verfasser als Nachahmer oder Schüler Heines zu sehen, gedruckt spätestens 1860. Ein bloßes Einfluss- oder Ähnlichkeitsurteil („Anklänge“) genügt nicht.
- **R3:** Für K3 gilt der Zeitraum 1829–1848 nicht. Eine Unterschiebung unter Heines Namen ist der Fall, für den H3a gedacht ist, gleich wann sie gedruckt wurde.
- **R4:** Wer keinen Beleg hat, gehört zu H3b. Das ist eine Folge der Entscheidungsregel und kein Nachweis von Heine-Ferne.

Die Belege stammen aus der Recherche vom 31.10.2026 und liegen in `Recherche_Heine_Nachahmungen_1830_1849/Belege_Heine_Einfluss/`.

### 1.2 Zuordnung

| Verfasser, Band | Beleg | Klasse |
|---|---|---|
| Gaudy, *Erato* 1829 („Freud' und Leid“) und Almanach 1833 | K1: Widmung „An H. Heine, als freundschaftlichen Gruß aus der Ferne“ im Band; im *Sabbath-Morgen* (1833) wird „Heine's Buch der Lieder“ genannt | **H3a** |
| Steinmann, *Dichtungen von H. Heine*, 2 Bde., Amsterdam 1861 | K3: Gedichte unter Heines Namen herausgegeben (R3) | **H3a** |
| Meißner, *Gedichte* 1846 | K2 nach R1: [Gottschall], „Die neue deutsche Lyrik“, *Die Gegenwart* 8 (1853), S. 53: der *Sohn des Atta Troll* (1850) als „Heinisirende Dichtung“. Vermerk: Das Urteil betrifft ein späteres Werk; die *Gedichte* von 1846 ordnet Gottschall auf derselben Seite eher Byron und Lenau zu. | **H3a** |
| Beck, *Stille Lieder* I 1840 | Einflussurteil: Engels (Oswald), *Telegraph für Deutschland* Nr. 202–203, Dez. 1839, MEW 41, S. 25: „Heinesche Anklänge“, zu genau diesem Band. Nach R2 kein K2-Beleg. | **H3b**; Gegenprobe in H3a (s. 3.6) |
| Hartmann, *Kelch und Schwert* 1845 und *Neuere Gedichte* 1847 | Minckwitz 1861 und Wurzbach 1862 (Bd. 8, S. 10) zu den *Zeitlosen* (1858). Nach der Zeitgrenze, anderes Werk. Gottschall 1853, S. 53 f., ohne Nachahmungsurteil. | **H3b** |
| Dingelstedt, *Nachtwächter* 1842 | Gottschall 1853, S. 44 f., ohne Nachahmungsurteil; Geiger, ADB 1903, später und zur Prosa | **H3b** |
| Müller von Königswinter, *Junge Lieder* 1841 | Gottschall 1853, S. 64, ohne Nachahmungsurteil; die *Höllenfahrt von Heinrich Heine* (1856) begründet weder K2 noch K3 | **H3b** |
| Scherr, Storm, Th. Mommsen | – | **H3b** |

### 1.3 Steinmann 1861: Textauswahl und Abgrenzung

- **Keine Überschneidung mit der Klasse C1.** C1 („Steinmann_Lieder“, 492 Wörter) stammt aus Steinmanns *Denkwürdigkeiten* von 1857. Der Zyklus „Zuckerpastillen“ kommt in der Ausgabe von 1861 nicht vor.
- **Grundlage:** die Dateien `Steinmann_Heine_Dichtungen_1861_Bd1_bereinigt.txt` und `…_Bd2_bereinigt.txt` mit dem Gedichtregister `Bereinigung/gedichtregister.csv`.
- **Auswahl:** Ausgeschlossen werden die Abschnitte „IX. Erzählendes“ (Verserzählungen) und „VI. Sonette“ (die Liedprobe misst keine Sonette). Aus den übrigen Gedichten beider Bände werden ganze Gedichte mit dem Startwert 20261031 zufällig gezogen, bis 11.000 Tokens erreicht sind. Danach werden sie in der Reihenfolge der Bände angeordnet.
- **Textqualität:** Vor der Rechnung wird die Fehlerquote durch eine Zufallsstichprobe am Druckbild belegt.

## 2. Heine-Klassen

### 2.1 Teilklassen

Die Abgrenzung folgt Heines eigener Druck- und Aufnahmepraxis und der Chronologie, nicht einem Stilmaß.

| Klasse | Inhalt | Grundlage im Projekt |
|---|---|---|
| **H1a** früher Heine | Erstdrucke und Gedichte bis März 1824: *Gedichte* 1822, *Lyrisches Intermezzo* 1823, Zeitschriftendrucke 1817–1824 | bisherige Klasse A2 (`out/A2`, Manifest `A2_Manifest.csv`) |
| **H1b** zweite Garnitur | halbanonym unter Chiffre gedruckte oder ungedruckte Gedichte 1824–1826: „Lieder von ****e“ in der *Agrippina* 1824, *Rheinblüthen* 1825, Roberts *Karlsruher Taschenbuch*, „Kleine Gedichte von H.H.“ in der *Biene* 1826, Ungedrucktes (DHA I, 481 ff.); jeweils in der Fassung des Erstdrucks | `Heine/Heine_Agrippina.txt`, `Heine_Biene.txt`, `Heine_Anonyma.txt`, `Heine_Zu Heimkehr.txt`, `Heine_nicht für Druck bestimmt Heimkehr.txt`; Liste nach DHA I, 858–860 und 481 ff., noch abzugleichen |
| **H1c** mittlerer Heine | *Neue Gedichte* 1844 (ohne die Zeitgedichte in der Hauptrechnung; mit ihnen als Gegenprobe) | **noch nicht im Projekt**, zu beschaffen |

Das *Buch der Lieder* von 1827 (Liedteile, A1L) bleibt der Bezugspunkt des Maßes. Es ist selbst keine Teilklasse, weil der Kandidatenwert s an ihm gemessen wird. Der *Romanzero* (1851) liegt nach dem Erscheinen des Kandidaten 1848 und gehört nicht in die Hauptrechnung. Eine Gegenprobe ist möglich.

### 2.2 Bekannte Probleme

1. **Wenig Text in H1b.** Die vorhandenen Dateien umfassen zusammen etwa 1.700 Wörter mit Doppelungen, also nur zwei bis drei Proben zu 548 Wörtern. Bei weniger als 3 Proben wird H1b nur beschreibend berichtet (Abstand des Kandidaten zu jeder Probe) und geht nicht in die Bilanz ein. Ob kleinere Proben zulässig sind, ist vor der Rechnung zu entscheiden.
2. **Überschneidung mit dem Bezugspunkt.** Mehrere H1b-Gedichte stehen später im *Buch der Lieder*, z. B. Heimkehr 25, 30, 32, 33, 42, 43, 60, 62, 79, 80. Für Proben aus H1a und H1b wird die A1-Bezugsklasse ohne diese Gedichte gebildet, wie bisher mit `calib.a1_minus` für A2.
3. **Schutzrechte.** Texte aus dem Heine-Portal gehen nicht ins öffentliche Repositorium.

## 3. Rechnung

1. **Maße, Probengröße, Kandidatenwert und Tor** wie E-11 nach Protokoll II.3a. `e11.py` bleibt unverändert; nur die Klassenlisten werden gesetzt.
2. **Für jede Teilklasse k** in H1a, H1b, H1c, H3a und H3b: Anteil der Proben, die mindestens so heine-nah sind wie der Kandidat (s ≥ s_K), mit dem bisherigen Schätzer `rate()` und Wilson-Intervall.
3. **Beschreibende Ebene:** Für jede Teilklasse werden Lage und Streuung von s berichtet, ebenso die Stellung des Kandidaten darin. Die Frage „Welchem Heine, welchem Nachahmer steht der Kandidat am nächsten?“ wird zuerst so beantwortet, ohne Bilanz.
4. **Bilanz:** P(E | H1) und P(E | H3) als Mischungen.
   - **Gewichte innerhalb von H1:** Hauptwert H1a : H1b : H1c = 1 : 1 : 1. Gegenproben: 2 : 1 : 1, 1 : 2 : 1, 1 : 1 : 2.
   - **Gewichte innerhalb von H3:** H3a : H3b = 1 : 1 wie in Fassung 1. Gegenproben 1 : 3 und 3 : 1.
   - Der Quotient H1 : H3 wird je Maß gebildet. Die Wertung ist der Median der Maße, die das Tor bestehen, begrenzt auf ±0,5.
5. **Zeichen-4-Gramme:** Zusätzlich wird immer die Variante „neutral“ berichtet (log10 LR = 0). Der Grund: Bisher erreicht keine Nachahmerprobe den Kandidatenwert, der Quotient wächst darum nur mit der Probenzahl.
6. **Gegenproben:** Beck in H3a; Gaudy nur mit den Liedern (Nr. I–XLVI); H1c mit den Zeitgedichten.

## 4. Was welches Ergebnis bedeuten würde

- **Kandidat am nächsten an H1b** (zweite Garnitur), vor H1a und H1c: Er passt zu Heines halbanonym gedruckten Nebenwerken. Das wäre ein Befund mit eigenem philologischem Gewicht, weil auch die *Vagabund*-Gedichte unter Chiffre beziehungsweise Pseudonym erschienen.
- **Am nächsten an H1a oder H1c:** Die Nähe wird entsprechend als „früher“ oder „mittlerer“ Heine-Ton beschrieben.
- **Am nächsten an H3a statt an einer der H1-Klassen:** Das stützt die Deutung als Nachahmung eher als die Echtheit. Die Wertung H1 : H3 sinkt.
- **Keine Teilklasse deutlich näher als die anderen:** Die Abstufung trägt stilometrisch nichts aus. Berichtet wird das als Grenze der Methode.

## 5. Noch offen, vor der Rechnung zu klären

- Liste der H1b-Gedichte nach DHA I, 858–860 und 481 ff., abgeglichen mit den vorhandenen Dateien; Entscheidung über die Probengröße bei weniger als 3 Proben.
- Beschaffung der *Neuen Gedichte* 1844 für H1c.
- Steinmann 1861: Ziehung und Stichprobe nach 1.3.
