# Protokollerweiterung (Entwurf): abgestufte Nachahmerklasse für E-11

Fassung 1, festgehalten am 31. Oktober 2026, 12:30 Uhr (MEZ). Eingefroren durch SHA-256, s. `Protokollerweiterung_Nachahmerklassen_Entwurf.sha256`.

Status: **Entwurf außerhalb des Hauptprotokolls.** Er kann später ganz oder teilweise in das Hauptprotokoll übernommen werden. Bis dahin gilt für den Aufsatz E-11 in der Fassung von Protokoll II.3a (19.10.2026), mit den am 31.10. korrigierten Texten.

## 0. Was beim Schreiben bereits bekannt war

Offenzulegen, weil es die Unabhängigkeit dieses Entwurfs begrenzt:

- alle Ergebnisse der Hauptauswertung, auch E-11 mit den vier bisherigen Nachahmern (+0,33 nach der Textkorrektur vom 31.10.);
- die explorative Rechnung mit Gaudy und Beck vom 31.10. (Bericht in `Explorativ_E11_Gaudy_Beck/`): Beide liegen im Wort-Delta seltener auf Höhe des Kandidaten als die bisherigen Nachahmer; die Wertung H1 : H3 stieg auf +0,40 bis +0,44;
- **nicht** bekannt: irgendein Ergebnis zu Meißner, Hartmann, Dingelstedt oder Steinmann. Für diese Verfasser ist zum Zeitpunkt der Festlegung weder Text bereinigt noch etwas gerechnet.

Anlass ist eine Überlegung des Verfassers: Die Nachahmerhypothese H3 ist bisher eine einzige Mischklasse. Wie hoch ihr Gewicht ausfällt, hängt von ihrer Zusammensetzung ab. Bekanntere Heine-Nachahmer sind darin schwächer vertreten als Storm und Mommsen.

## 1. Fragestellung

Liegt der Kandidat stilometrisch näher an solchen Zeitgenossen, die nach äußeren Kriterien als enge Heine-Nachahmer gelten (H3a), als an Zeitgenossen im allgemeinen Liedton ohne nachweisbaren Heine-Bezug (H3b)? Und wie verändert die Aufteilung von H3 in H3a und H3b die Bilanz?

## 2. Zuordnung zu den Klassen: nur nach äußeren Kriterien

Ein Verfasser gehört zur Klasse **heine-nah (H3a)**, wenn mindestens eines der folgenden Kriterien mit Quelle belegt ist:

- **K1** Ausdrücklicher Bezug im verwendeten Band selbst: Widmung an Heine, Titel- oder Gedichtzusatz „nach Heine“ o. ä., erkennbare Parodie oder Fortschreibung eines Heine-Textes.
- **K2** Zeitgenössische Kritik, spätestens 1860 gedruckt, nennt den Verfasser ausdrücklich als Heine-Nachahmer oder -Schüler. Stelle mit Seite nachweisen.
- **K3** Der Verfasser hat Gedichte unter Heines Namen in Umlauf gebracht (Fälschung, Unterschiebung).

Alle übrigen Verfasser gehören zur Klasse **heine-fern (H3b)**.

**Ausdrücklich ausgeschlossen** als Kriterium für die Zuordnung: jede stilometrische Größe, auch die eigenen Delta-Werte. Ebenso ausgeschlossen ist ein bloßer Eindruck von Heine-Ton ohne Beleg. Das verhindert, dass die Klasse durch das Maß bestimmt wird, an dem der Kandidat gemessen wird.

**Vorläufige Zuordnung.** Die Belege sind noch zu erbringen; wo einer fehlt, gilt der Verfasser als heine-fern.

| Verfasser | Band | Klasse | Kriterium | Beleg |
|---|---|---|---|---|
| Gaudy | *Erato* 1829, „Freud' und Leid“ | nah | K1: Widmung „An H. Heine“ | Erato, S. [1] vor Nr. I [prüfen: genaue Stelle] |
| Steinmann | [Ausgabe prüfen] | nah | K3 | [prüfen] |
| Meißner | *Gedichte* 1846 | nah, falls K2 belegt | K2 | [prüfen] |
| Hartmann | *Kelch und Schwert* 1845; *Neuere Gedichte* 1847 | nah, falls K2 belegt | K2 | [prüfen] |
| Dingelstedt | *Lieder eines kosmopolitischen Nachtwächters* 1842 | nah, falls K1 oder K2 belegt | K1/K2 | [prüfen] |
| Beck | *Stille Lieder* I 1840 | nah, falls K2 belegt | K2 | [prüfen] |
| Müller v. Königswinter | *Junge Lieder* 1841 | fern, falls kein Beleg | – | (Gottschall 1853 prüfen: als Nachahmer genannt?) |
| Scherr, Storm, Th. Mommsen | wie bisher | fern | – | – |

Die Zuordnung wird mit allen Belegen in einer datierten Fassung 2 dieses Dokuments festgeschrieben, **bevor** gerechnet wird. Rechnungen davor gelten als explorativ.

## 3. Texte

1. **Gattung:** nur lyrische Sammlungen aus der Zeit 1829–1848. Ausgeschlossen sind Versepen und epische Zyklen, z. B. Hartmanns *Reimchronik des Pfaffen Maurizius*. Prosa, Dramen und Übersetzungen sind ebenfalls ausgeschlossen.
2. **Umfang je Verfasser:** höchstens 20 Proben zu 548 Tokens, also rund 11.000 Tokens. Reicht ein Band nicht, wird der ganze Band genommen. Ist er größer, werden Druckseiten mit festem Startwert 20261031 zufällig gezogen, bis 11.000 Tokens erreicht sind, und dann in Seitenfolge aneinandergefügt. Gezogen wird aus dem Gedichtteil des Bandes ohne Vorsatz, Inhaltsverzeichnis und Anhang. Bei zwei Bänden eines Verfassers zählen deren Gedichtseiten zusammen als ein Pool.
3. **Textherstellung wie bei E-11** (Bericht vom 31.10.):
   - Fraktur-Erkennung (Tesseract 5, `deu_latf`);
   - regelhafte Reinigung;
   - Korrektur Seite für Seite, im Zweifel am Seitenbild;
   - Paratext entfernen: Widmungen, Abteilungstitel, Fußnoten, Gedichtnummern, fremdsprachige Mottos und Zeilen;
   - Gedichttitel bleiben stehen.

   Fehlerquote durch Zufallsstichprobe am Bild belegen; Ziel unter 1 % Wortfehler. Texte vor der Rechnung mit SHA-256 einfrieren.

## 4. Rechnung

1. **Maße, Probengröße, Bezugsklassen, Kandidatenwert und Tor** wie E-11 (Protokoll II.3a): AUC ≥ 0,75 gegen die gesamte Nachahmerklasse, Wertung = Median der log10-Quotienten der bestandenen Maße, begrenzt auf ±0,5. `e11.py` bleibt unverändert; nur die Liste der Nachahmer wird gesetzt.
2. **Getrennt berechnet** werden die Quotienten
   - LR_a = P(Kandidat | Heine) : P(Kandidat | H3a);
   - LR_b = P(Kandidat | Heine) : P(Kandidat | H3b).
3. **Zusammengefasst** wird über die Mischung, nicht über einen gemeinsamen Pool:

   P(E | H3) = w · P(E | H3a) + (1 − w) · P(E | H3b), daraus der Quotient H1 : H3.

   Damit hängt das Ergebnis nicht mehr davon ab, wie viele Proben zufällig in welcher Teilklasse liegen.
4. **Gewicht w** (Anteil der engen Nachahmer an der Nachahmerhypothese): Hauptwert w = 0,5. Empfindlichkeit w = 0,25 und w = 0,75. Eine philologische Begründung für einen anderen Hauptwert muss vor der Rechnung in Fassung 2 stehen.
5. **Zeichen-4-Gramme:** Hat eine Teilklasse 0 Treffer, so wächst der Quotient bloß mit der Probenzahl. Für dieses Maß wird deshalb zusätzlich die Variante „neutral“ berichtet (log10 LR = 0).
6. **Gattungskontrolle:** zusätzlich berichten ohne die Verfasser, deren Proben überwiegend Zeit- oder Tendenzlyrik sind. Die Einstufung „überwiegend“ erfolgt nach Inhaltsverzeichnis und Gedichttiteln, vor der Rechnung, in Fassung 2.
7. **Bilanz:** Die übrige H3-Masse bleibt unverändert (ausgewogen +0,20, skeptisch −0,40). Berichtet werden dieselben Varianten wie in 8.1.

## 5. Was welches Ergebnis bedeuten würde (vorab festgelegt)

- **Kandidat bei H3a deutlich heine-näher als bei H3b** (LR_a < 1 < LR_b): Der Befund „Liedton der Zeit“ wird zu „Heine-Nähe wie bei engen Nachahmern“. Das spricht für H3a mindestens so sehr wie für H1. Die Wertung H1 : H3 sinkt; es ist zu prüfen, ob „zweifelhaft“ noch trägt.
- **LR_a und LR_b beide > 1:** Der Kandidat liegt näher an Heine als beide Nachahmerklassen. Die Wertung H1 : H3 steigt. Die Aussage „zweifelhaft“ bleibt, sofern der Wert unter der Schwelle von 8.3 bleibt.
- **LR_a ≈ LR_b:** Die Abstufung trägt stilometrisch nichts aus. Für den Aufsatz wäre das ein Befund über die Grenzen der Methode: Rezeptionsnähe und Nähe in den häufigsten Wörtern fallen auseinander.
- **Tor in einer Teilklasse nicht bestanden** (AUC < 0,75): Für diese Teilklasse wird log10 LR = 0 gesetzt, wie bisher bei nicht bestandenen Maßen.

## 6. Offene Punkte für Fassung 2

- Belege K1–K3 je Verfasser.
- Steinmann: Ausgabe, Umfang (reicht er für mindestens 3 Proben?), Textgrundlage. Hinweis: Steinmann steckt bereits in der skeptischen Vorab-Wahrscheinlichkeit (1 : 20). Rechnerisch ist das keine Doppelzählung, weil die Vorab-Wahrscheinlichkeit die Häufigkeit von Fälschungen erfasst und der Quotient den Stil. Im Text ist es aber offen zu sagen.
- Hauptwert für w.
- Einstufung „überwiegend Zeit- oder Tendenzlyrik“ je Verfasser.
- Ob Beck, Band 2, und Meißners Erstausgabe von 1845 nachzubeschaffen sind.
