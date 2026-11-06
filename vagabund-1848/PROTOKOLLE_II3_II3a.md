# Prüfprotokolle II.3 und II.3a (mit Protokoll zur Vergleichsklasse)

*English summary below.*

## Zu dieser Fassung

Dieser Text gibt die Protokollteile des Arbeitsdokuments „Hektor-Gedichte: Bayesianische Vorgehensweise“ wieder: Teil II bis vor die Ergebnisse (II.1 bis II.3a mit den Ergänzungsverfahren E-1 bis E-11) und aus Teil III das Protokoll zur Vergleichsklasse des Priors (Stufe 2a). Grundlage ist der Stand des Dokuments vom 6. November 2026 (Revision 134). Das Format wurde nach Markdown übertragen. Bei E-9 wurde am 6. November 2026 ein Klammerzusatz zum Anlass des Verfahrens redaktionell weggelassen; der übrige Protokollwortlaut einschließlich der Datierungen ist unverändert. Ergebnisse, Abwägung und Bilanz des Arbeitsdokuments sind nicht wiedergegeben; sie stehen im Aufsatz und in den Ergebnisdateien dieses Ordners.

Die Datierungen sind die im Arbeitsdokument festgehaltenen. Spätere Präzisierungen und Abweichungen sind im Text selbst datiert. Der Wortlaut von II.2 bis E-8 stimmt mit einer im Projekt gesicherten Fassung des Dokuments wörtlich überein (Revision 70; jüngster datierter Eintrag vom 17.10.2026); E-9 bis E-11 und das Protokoll zur Vergleichsklasse kamen danach hinzu und tragen ihre eigenen Daten. Die Protokolle wurden nicht extern registriert; ihre Veröffentlichung hier ist keine nachträgliche Präregistrierung. Prüfbar ist die Verblindung: Der unter II.3 eingetragene SHA-256-Wert der Schlüsseldatei stimmt mit `korpus/verblindung/schluessel/schluessel.json` überein.

Lesehilfen:

- `corpus_diplomatisch/` im Text entspricht im Repositorium `korpus/`.
- Die im Text genannte Vorstudie (Anhang A des Arbeitsdokuments) ist hier nicht wiedergegeben; die Vorstudien außerhalb des Protokolls liegen in `stilometrie/`.
- E-1 bis E-11 (mit Bindestrich) sind die Ergänzungsverfahren dieses Protokolls. E1 bis E25 (ohne Bindestrich) sind die philologischen Befunde aus Teil I des Arbeitsdokuments, der hier nicht wiedergegeben ist; sie sind im Aufsatz (Abschnitte 5 und 6) und in `bayes/bilanz/befunde.csv` beschrieben.
- Verweise auf Teil III (Punkte, Gewichte) beziehen sich auf die Bilanz; die endgültigen Werte stehen in Tab. 3 und 5 des Aufsatzes und in `bayes/bilanz/`.
- Der Kandidat hat nach der Präzisierung vom 16.10.2026 538 statt 548 Wörter.
- Die Kodierung von E-10 wurde vom Autor selbst und nicht verblindet vorgenommen; sie zitiert Heine-Verse und ist nicht enthalten (`bayes/e10/PROTOKOLL.md`).
- Arbeitsordner, die im Text genannt sind (etwa „Ordner Stilurteile“), sind nicht Teil des Repositoriums.

**Nachträgliche Klarstellung zur Vergleichsklasse (Auskunft des Autors vom 6. November 2026):** Die im historischen Protokoll Stufe 2a noch offenen Abgrenzungsfragen sind für die veröffentlichte Fassung wie folgt einzuordnen:

- Texte von Namensvettern, die unter ihrem eigenen Namen „Heine“ zeichneten, zählen nicht als Zuschreibungen an Heinrich Heine und wurden nicht in die Vergleichsklasse aufgenommen.
- Nach der derzeitigen Rekonstruktion des Autors wurde die zusätzlich erwogene engere Vergleichsklasse „mit Fund- oder Herkunftsgeschichte“ nicht gesondert ausgewertet.

Diese Klarstellung erläutert den tatsächlichen Auswertungsstand; sie ist keine rückwirkende Ergänzung der ursprünglichen Vorab-Festlegung.

## English summary

This file reproduces the protocol sections of the working document (in German), converted to Markdown: Part II up to the results (II.1–II.3a, with the supplementary tests E-1 to E-11) and, from Part III, the protocol for the reference class of the prior (stage 2a). The source is the state of the document on 6 November 2026 (revision 134). A parenthetical note on the motivation for E-9 was editorially omitted on 6 November 2026; the remaining protocol wording, including the dates, is unchanged. The wording of II.2 to E-8 is identical to a copy of the document saved in the project (revision 70, latest dated entry 17 October 2026). Dates are those recorded in the working document; later specifications and deviations are dated in the text. The protocols were not registered externally, and publishing them here is not a retrospective preregistration. The SHA-256 value of the blinding key recorded under II.3 matches `korpus/verblindung/schluessel/schluessel.json`. In the text, `corpus_diplomatisch/` corresponds to `korpus/` in this repository; E-1 to E-11 are the supplementary tests, E1 to E25 the philological findings of Part I (not reproduced; see Sections 5 and 6 of the article and `bayes/bilanz/befunde.csv`). E-10 was coded by the author himself, without blinding.

**Retrospective clarification of the reference class (author’s statement of 6 November 2026):** Texts by other authors who signed with their own surname “Heine” were not treated as attributions to Heinrich Heine and were excluded from the reference class. According to the author’s current reconstruction, the additionally proposed narrower class of texts accompanied by a discovery or provenance account was not evaluated separately. This clarification describes the analysis as conducted; it does not retrospectively amend the original prespecification.

---

## Teil II: Stilometrische Prüfung

Teil II beginnt neu: Das Protokoll wird datiert festgelegt, bevor gerechnet wird. Die bisherigen Läufe stehen als Vorstudie in Anhang A und gehen nicht in Teil III ein.

### II.1 Grenzen bei kurzen Texten

- Mindestlänge nach Literatur und Vorstudie; Lernkurve mit 200, 351 und 548 Wörtern (II.4).

### II.2 Korpora und Textschicht

| Klasse | Inhalt | Rolle | Stand |
|---|---|---|---|
| A1 | Buch der Lieder 1827; Liedteile (Lieder, Intermezzo, Heimkehr) getrennt von den übrigen Teilen | Heine-Referenz | restituiert |
| A2 | Heine-Erstdrucke und DHA-Anhang bis Frühjahr 1824 | echter Heine außerhalb des Bandes, Gegenprobe | erzeugt 16.10.2026: 178 Gedichte, 18.101 Wörter, 33 Blöcke; davon nur 3.530 Wörter nie im Buch der Lieder |
| B1 | Hektor, Vagabund-Lieder | H2, gattungsgleich | vorhanden |
| B2 | Hektor, Schilda | H2, Gattungskontrolle | vorhanden |
| C1 | Steinmann | bekannter Fälscher | vorhanden, 492 Wörter |
| C2 | Nachahmer der 1840er (Geibel, weitere nach DHA) | Ersatz für H3 | zu transkribieren |
| C3 | Müller, Wunderhorn | zeitgenössische Liedlyrik | vorhanden |
| D | Kandidat, 10 Gedichte, 548 Wörter | zu prüfen | versiegelt bis II.5 |

- Textschicht: historische Schreibung und eine mechanisch angeglichene Schicht; feste Regeln, für alle Klassen gleich, Vers und Satzzeichen bleiben.
- Proben: Kurze Gedichte werden wie beim Kandidaten in fester Reihenfolge zu Blöcken von 548 Wörtern gefügt.

### II.3 Protokoll

Festgelegt am 2026-10-16 (Stichtag). Jede spätere Änderung gilt als Abweichung (Punkt 10).

1. **Fragen:** H1 : H2 und H1 : H3 werden getrennt geprüft.
2. **Klassen:** H1 : H2 = A2 gegen B1 (Hektors Vagabund-Lieder). H1 : H3 = A2 gegen C1 und C2 (Steinmann, Nachahmer). C3 (Müller, Wunderhorn) nur als Kontrolle, B2 (Schilda) nur zur Gattungsprüfung.
3. **Proben:** 548 Wörter, die Länge des Kandidaten. Kürzere Gedichte werden chronologisch nach Erstdruck zu Blöcken gefügt; ein Rest unter 548 Wörtern bleibt liegen.
4. **A2:** Heine-Erstdrucke und Gedichte des DHA-Anhangs mit Datum bis März 1824; nur strophische Lieder und Romanzen, keine Sonette, keine freien Rhythmen. Ein Gedicht, das in A2 steht, wird für diesen Vergleich aus A1 genommen.
5. **Schreibung:** zwei Schichten, historisch und angeglichen. Die Angleichung folgt einer festen Liste: th → t, ey → ei, aͤ/oͤ/uͤ und Ae/Oe/Ue → ä/ö/ü bzw. Ä/Ö/Ü, Apostrophe und Anführungszeichen vereinheitlicht. Vers, Satzzeichen und alle übrigen Wortformen bleiben.
6. **Maße:** Cosine Delta auf den 150 häufigsten Wörtern und auf Zeichen-4-Grammen; Merkmale und Standardwerte ohne Kandidat und ohne C1.
7. **Schwellen:** Gattung schlägt Verfasser, wenn der Abstand Heine-Lied – Heine-Nordsee in mindestens 60 % der Ziehungen über Heine-Lied – Müller liegt; dann nur Lied gegen Lied. Die angeglichene Schicht gilt, wenn sich die AUC um mehr als 0,05 verschiebt. Tor je Gegensatz: AUC ≥ 0,75 bei 548 Wörtern; sonst wird LR = 1 berichtet.
8. **Umrechnung:** LR = Trefferquote an A2 / Fehlalarmquote an der Gegenklasse, nach derselben Regel, die später für den Kandidaten gilt.
9. **Verblindung:** Ein Skript vergibt Codes an den Kandidaten und acht bis zehn bekannte Blöcke gleicher Länge und schreibt den Schlüssel in eine Datei. Deren SHA-256-Prüfwert wird hier vor dem Lauf eingetragen; geöffnet wird sie erst, wenn alle Ergebnisse festgehalten sind.
10. **Abweichungen:** Jede Änderung nach dem Stichtag kommt mit Datum und Grund in die Liste unten; Ergebnisse vor und nach der Änderung werden beide berichtet.

**Prüfwert der Schlüsseldatei** (SHA-256, erzeugt 2026-10-16 mit `verblinden.py`, 10 Texte X01–X10 zu je 538 Wörtern): `024a86b854c8304eca7a7e079adf20f2fc0d9e5795eb985184f743ad23f46537`. Die Schlüsseldatei liegt ungeöffnet in `corpus_diplomatisch/verblindung/schluessel/`.

**Präzisierungen** (16.10.2026, vor der Kalibrierung festgelegt, wo das Protokoll offen war):

- Zeilen, die nur aus einer Zahl bestehen, entfallen in allen Texten. Der Kandidat hat dadurch 538 statt 548 Wörter; die Täuschungsblöcke sind auf dieselbe Länge gekürzt.
- Zeichen-4-Gramme: die 150 häufigsten, kleingeschrieben, Zeilenumbrüche als Leerzeichen.
- Merkmale und Standardwerte über alle bekannten Blöcke, ohne C1, Kandidat und Täuschungsblöcke.
- Entscheidungsregel: s = Median-Abstand zur Gegenklasse minus Median-Abstand zu den A1-Liedteilen; heine-nah, wenn s > 0.
- Beim Weglassen einer Probe der Gegenklasse entfallen auch ihre Nachbarblöcke, weil sie dieselben Gedichte enthalten können.
- Raten geglättet als (k + 0,5) / (n + 1); Unsicherheit als 95-%-Wilson-Intervall.
- Schreibungsregel: geprüft über alle Gegensätze und beide Verfahren bei 548 Wörtern.
- C1 (Steinmann, 485 Wörter) ergibt keinen Block von 548 Wörtern und entfällt in der Kalibrierung; er wird als Einzelfall berichtet.
- Zehn Täuschungsblöcke (3 × A2, 3 × C2, 3 × C3, 1 × B2) wurden vorab mit Startwert 20261016 bestimmt und aus der Kalibrierung genommen.

**Abweichungen** (beschlossen 2026-10-16, nach der Kalibrierung und vor dem verblindeten Lauf):

1. Für H1 : H3 ist die offene Gegenprobe maßgeblich: Die Fehlalarmquote stammt von Nachahmern, deren Texte nicht im Vergleichssatz liegen. Grund: Warnebolds Texte liegen nicht vor. Die geschlossene Gegenprobe wird daneben berichtet.
2. Die angeglichene Schreibschicht ist Hauptschicht, obwohl die Schreibungsregel nicht ausgelöst wurde. Grund: Der Kandidat ist ein Druck von 1848, die Heine-Referenz stammt aus den 1820er Jahren; die Prüfung 2d kann diesen Fall nicht erfassen. Die historische Schicht läuft als Robustheitsprüfung mit.

### II.3a Ergänzungsprotokoll

Festgelegt am 2026-10-16, nach der Entschlüsselung von II.5 und vor jeder Rechnung mit den drei Ergänzungsverfahren. Der Kandidat ist bekannt; eine erneute Verblindung entfällt, weil alle Regeln mechanisch sind und hier vorab stehen. Reihenfolge je Verfahren: erst Kalibrierung an bekannten Texten, dann der Kandidat. Es gelten Klassen, Proben, Schicht (angeglichen), Entscheidungsregel s > 0, Glättung und Umrechnung in LR aus II.3, soweit unten nichts anderes steht.

**E-1 Textverzerrung** (Stamatatos 2017, Variante DV-MA)

1. Jedes Wort, das nicht zu den 150 häufigsten Wörtern der Trainingstexte gehört, wird durch Sternchen gleicher Länge ersetzt; Satzzeichen bleiben.
2. Auf dem verzerrten Text: 150 häufigste Zeichen-4-Gramme, Cosine Delta, Regel und Kalibrierung wie II.4 (geschlossen und offen).
3. Robustheit: 50 und 300 erhaltene Wörter statt 150.
4. Zweck: Prüfen, ob die knappe Heine-Nähe aus II.5 vom Thema kommt. Für Teil III gilt bei H1 : H2 das vorsichtigere LR aus II.5 und E-1 (näher an 1).

**E-2 Zeta** (Craig’s Zeta, Craig & Kinney 2009)

1. Gruppen: Heine = A1-Liedteile + A2; Hektor = B1 + B2 (alle Hektor-Verse; die Gattungsmischung wird berichtet). Segmente zu 100 Wörtern.
2. Zeta je Wort = Anteil der Heine-Segmente mit dem Wort minus Anteil der Hektor-Segmente mit dem Wort. Je 100 Marker für Heine und Hektor, nur Wörter, die in mindestens 3 Segmenten vorkommen.
3. Wert eines Textes = Anteil seiner Wortformen unter den Heine-Markern minus Anteil unter den Hektor-Markern. Kalibrierung: Blöcke von A2 und B1 einzeln zurückgehalten, Marker jeweils ohne diesen Block neu bestimmt.
4. Zweck: Deutung (welche Wörter ziehen den Kandidaten wohin). Zeta geht nicht als eigenes LR in Teil III ein, weil es mit Delta auf Wörtern zusammenhängt.

**E-3 Versmerkmale** (Befund E14)

1. Proben: Blöcke von rund 548 Wörtern, an Versgrenzen geschnitten, mit erhaltenen Versen und Strophen.
2. Merkmale, mechanisch je Probe:
   - Anteil weiblicher Kadenzen (Versende auf unbetonte Endung -e, -en, -er, -el, -em, -es, -ern, -eln bei mehrsilbigem Schlusswort),
   - Anteil unreiner Reime unter erkannten Reimpaaren (Gleichsetzung ü/i, ö/e, ei/eu/äu, b/p, d/t, g/k),
   - Elisionen (Apostrophe je 100 Wörter),
   - Anteil der Verse ohne Satzzeichen am Ende (Enjambement-Ersatz),
   - mittlere Silbenzahl je Vers und ihre Streuung (Silben = Vokalgruppen),
   - Anteil der Verse mit „Und“ am Anfang,
   - Anteil vierzeiliger Strophen.
3. Die sieben Merkmale werden standardisiert; Cosine Delta, Regel und Kalibrierung wie II.4 (geschlossen und offen).
4. Gewicht in Teil III: Für H1 : H3 geht E-3 als eigenes LR ein, wenn die offene Gegenprobe das Tor (AUC ≥ 0,75) besteht. Für H1 : H2 zählt nur das stärkere von Delta und E-3, weil beide denselben Text messen.

**Für alle drei:** Steinmann (C1) wird als Einzelfall mitgerechnet. Ergebnisse werden vollständig berichtet, auch wenn ein Verfahren nichts ergibt.

**E-4 Datierung des Wortschatzes** (Befund E11). Nachtrag, festgelegt am 2026-10-16 vor jeder Abfrage zum Kandidaten.

1. Stichtag: Unter H1 sind die Gedichte vor März 1824 entstanden. „Vorher“ heißt Belegjahr bis 1824, „nachher“ 1825–1848.
2. Referenz: Deutsches Textarchiv (DTA, Kern und Erweiterungen) über die DDC-Schnittstelle, mit der eingebauten Schreibvarianten-Normalisierung. Treffer von Heine, Hektor und Geibel zählen nicht, damit kein Text sich selbst belegt.
3. Wortformen: jede Wortform der Probe (historische Schicht); Elisionen werden aufgelöst (trüb' → trübe usw.). Hat eine Form vorher keinen Beleg, wird das Lemma abgefragt (Lemma laut DTA-Analyse, sonst die Form selbst).
4. Zusammensetzungen: Ein Wort ohne Vorher-Beleg gilt als *freie Bildung*, wenn es sich in zwei Teile zerlegen lässt (Fugen -s-, -es-, -n-, -en-, -e-, -er- erlaubt), die vorher je mindestens fünfmal belegt sind. Freie Bildungen zählen nicht, weil Lyrik ständig neue Komposita bildet.
5. Verdacht: Was danach ohne Vorher-Beleg bleibt, wird von Hand im Grimmschen Wörterbuch und bei Adelung geprüft. Ein Anachronismus liegt nur vor, wenn auch dort kein Beleg vor 1825 steht und das Wort kein Eigenname, keine Schreibung und keine bloße Flexionsform ist.
6. Wendungen: alle Folgen von vier Wörtern innerhalb der Probe werden als Phrase abgefragt. Ein *Echo* ist eine Folge, die vorher nicht, aber 1825–1848 bei einem anderen Autor belegt ist; Echos werden von Hand gesichtet. Treffer bei Heine selbst werden nur beschrieben.
7. Kalibrierung: dieselbe Prüfung an drei Proben aus dem Pool von II.3: P03 (Heine, A2, Heimkehr 1824), P04 (Geibel, 1840er), P10 (Hektor, Schilda 1847). Sie zeigt, wie viele Verdachtsfälle ein echter Heine-Text von 1824 und Texte der 1840er erzeugen.
8. Gewicht in Teil III (für H1 : H2 und H1 : H3 gleich): ein bestätigter Anachronismus −1,5 Punkte; ein nicht ausräumbarer Verdacht oder ein klares Echo eines nach 1824 gedruckten fremden Textes −0,5; kein Befund +0,1, weil auch ein Nachahmer von 1848 im alten Liedton schreibt und Anachronismen leicht vermeidet.

*Präzisierungen zu E-4* (bei den ersten Testabfragen festgestellt, vor der Auswertung): Die DTA-Abfrage gleicht von sich aus auf Lemma-Ebene ab (Schreibvarianten und Flexion); Schritt 3 fällt damit in einen Schritt zusammen. Wendungen werden ebenso abgefragt; das macht Vorher-Treffer wahrscheinlicher und Echos seltener, wirkt also vorsichtig. Für die Zerlegung nach Regel 4 hat jeder Teil mindestens drei Buchstaben. Während des Laufs bemerkt und behoben: Die Elisionen „Beleid'ger“, „Vertheid'ger“, „beleid'gen“ in der Hektor-Probe wurden zunächst falsch aufgelöst.

**E-5 Prosavergleich: Strandszene und Hektors Prosa** (zu E4). Festgelegt am 2026-10-17 vor jeder Rechnung.

1. Frage: Ist die als Worte des Freundes ausgegebene Strandszene („Der Schatz, den ich gehoben“ bis „las mit Entzücken“, rund 230 Wörter) Hektors Prosa näher als der Prosa anderer Autoren der Zeit?
2. Hektor-Prosa: Nr. IV („Lockspeise“; Rahmen von „Ein merkwürdiger Fund“) und Beilage zu Nr. XI („Eine Geistererscheinung“ mit Fußnote „D. R.“), ohne das zitierte Volksblatt-Stück und ohne den plattdeutschen Leserbrief. Quelle: Scans der Digitalisate (HathiTrust/Google), OCR mit Fraktur-Modell.
3. Vergleichsautoren: Prosa 1825–1848 aus dem DTA, darunter Heines Reisebilder II („Nordsee“) als Vorbild des Tons; je Autor ein Profil gleicher Länge wie Hektors Prosa.
4. Merkmale: 100 häufigste Wörter des Gesamtbestands (vor allem Funktionswörter), Schreibung angeglichen (ſ → s, Kleinschreibung); Cosine Delta. Robustheit: Zeichen-4-Gramme (200).
5. Maß: Anteil der Vergleichsautoren, die weiter von der Strandszene entfernt sind als Hektor (0 bis 1).
6. Kalibrierung: dasselbe Maß für 230-Wörter-Stücke aus Hektors Prosa (jeweils aus seinem Profil herausgenommen) und aus Texten der Vergleichsautoren; AUC. Nur wenn AUC ≥ 0,75, wird das Ergebnis gewertet; sonst nur beschrieben.
7. Bekannte Schwäche: Hektors Prosa ist satirisch, die Strandszene empfindsam; die Gattung kann das Ergebnis stärker prägen als der Verfasser. Ein Ergebnis „Hektor-fern“ ist deshalb kaum aussagekräftig, ein Ergebnis „Hektor-nah“ trotz Gattungsunterschied wäre bemerkenswert.
8. Folge für Teil III: Bei gewertetem Ergebnis „Hektor-nah“ gilt die Szene als von Hektor geschrieben oder bearbeitet; dann fällt ihr Gewicht als Zeugnis für Warnebolds Fähigkeit weg (E20–E22 zurück auf +0,4), und E4 wird leicht stärker Richtung H2 gewertet (−0,25 zusätzlich). Sonst keine Änderung.

**E-6 Entwurfsstufen: Kandidat und Heines früheste Handschriftenstufen** (Anregung Ch. auf der Horst). Festgelegt am 2026-10-17 vor jeder Rechnung.

1. Frage: Lassen sich die Abweichungen des Kandidaten von Heines gedruckten Liedern (E-3: kürzere und gleichmäßigere Verse, weniger Elisionen, mehr Verse ohne Schlusszeichen; dazu viele Verkleinerungsformen) als Entwurfsmerkmale erklären? Hektors Bericht spricht von „flüchtig niedergekritzelten Liedern“.
2. Material: Lesartenapparat DHA I (bereits vorhanden). Gewertet werden nur echte Handschriften (Siglen H, H1, H2, h), nicht Heines Korrekturen in Druckexemplaren (GH, D1h, RI1H, „H (Korr.)“). Bei geschichteten Lesarten zählt die früheste Schicht (1).
3. Stufe 1 (Richtung): Für jede Apparatstelle mit Handschriftlesart wird die Handschrift mit dem Endtext verglichen: fehlendes Satzzeichen am Versende, Elisionen (Apostrophe), Verkleinerungsformen (-lein, -chen), Silben bei ganzen Versen. Ergebnis: in welche Richtung Heine überarbeitet hat und wie groß der Unterschied je Vers ist.
4. Stufe 2 (Test, nur wenn Stufe 1 einen deutlichen Unterschied zeigt): früheste Fassungen der betroffenen Gedichte herstellen; dieselben Merkmale wie E-3 messen; prüfen, ob frühe und späte Stufen trennbar sind (AUC ≥ 0,75), und erst dann, wo der Kandidat liegt.
5. Wertung: Für H1 zählt nur eine positive Lage des Kandidaten bei den frühen Stufen. Dass Entwürfe schwächer sein können, entschuldigt Abweichungen, ist aber kein Befund für Heine. Wenn Stufe 1 zeigt, dass Heines Handschriften die Abweichungen des Kandidaten teilen, fällt das entsprechende Gegenargument in der Darstellung weg; die Punkte von E-3 (+0,4 für H1 gegen H3) bleiben unverändert.
6. Vergleich mit dem „Neuen Frühling“ (DHA II) als zweiter Schritt, sobald der Apparat aus dem Heine-Portal geholt werden kann.

**E-7 Gegenprobe bei gleichem Versmaß** (zu E-3). Festgelegt am 2026-10-17 vor jeder Rechnung.

1. Frage: Liegt die Heine-Nähe des Kandidaten in E-3 nur daran, dass kurzzeilige Lieder anders aussehen als längere Verse? Und ist der kurze, gleichmäßige Vers des Kandidaten auch unter Heines kurzzeiligen Liedern ungewöhnlich?
2. Einheit: nur vierzeilige Strophen, deren Verse alle 5 bis 9 Silben haben (Silben = Vokalgruppen, nach Angleichung). Alle anderen Strophen fallen heraus, in allen Korpora und im Kandidaten gleich.
3. Proben: Blöcke aus so vielen Versen, wie der Kandidat nach dieser Auswahl hat; Korpora und Klassen wie E-3 (A1 Lieder, A2, Hektor B1/B2, Geibel C2, Müller/Wunderhorn C3, Steinmann einzeln).
4. Merkmale: die fünf versbaulichen Merkmale aus E-3 ohne die Überlieferungsmerkmale (weibliche Kadenz, unreine Reime, Silben je Vers, Streuung der Silben, „Und“ am Versanfang); Strophenform entfällt, weil sie hier immer gleich ist.
5. Entscheidung und Kalibrierung wie E-3 (s > 0 heißt heine-nah; geschlossen gegen Geibel, offen gegen Müller/Wunderhorn und gegen Hektor); Tor: AUC ≥ 0,75 offen gegen Müller/Wunderhorn.
6. Gewicht in Teil III: Besteht E-7 das Tor, ersetzt es E-3 für H1 : H3 (Punkte nach seinem LR, höchstens wie E-3). Besteht es das Tor nicht, wird E-3 halbiert (+0,4 → +0,2), weil sein Signal dann am Versmaß hängen kann.
7. Beschreibend: Streuung der Silben je Block bei Heines kurzzeiligen Strophen gegenüber dem Kandidaten.

**E-8 Ungedruckte Vorstufen: Buch der Lieder und „Neuer Frühling“** (zu E13 Privatwissen, Anregung Ch. auf der Horst). Festgelegt am 2026-10-17 vor jeder Rechnung; Daten (DHA II, S. 11–30, 178, 300–386, 854–857) vorher geladen, aber nicht ausgewertet.

1. Gedanke: Ein Nachahmer um 1845 kannte nur Heines Drucke. Teilt der Kandidat Wendungen mit Heines ungedruckten Entwürfen, die in keinem Druck vor 1848 stehen, wäre das Wissen, das nur Heine (oder wer seine Papiere kannte) haben konnte.
2. Ungedruckt (U): Lesarten echter Handschriften (H, H1, H2, h, auch Arbeitsmanuskripte) aus DHA I (Buch der Lieder) und DHA II („Neuer Frühling“ und die dazu nicht gedruckten Gedichte). Nicht: Korrekturen in Druckexemplaren.
3. Gedruckt (P): Heines Texte in allen Fassungen, die vor 1848 gedruckt waren (Buch der Lieder Erstdrucke und Ausgaben, „Neuer Frühling“), dazu die DTA-Belege anderer Autoren vor 1848 aus E-4.
4. Einheiten: im Kandidaten jedes Paar benachbarter Inhaltswörter im selben Vers und jede Dreiwortfolge, nach Angleichung (Kleinschreibung, ß/ss, th/t, ey/ei, Apostroph weg, einfache Endungen weg).
5. Treffer in U, die nicht auch in P stehen, sind „Entwurfstreffer“; sie werden von Hand gesichtet (formelhaft oder unverwechselbar).
6. Kontrolle: dieselbe Zählung für gleich lange Proben bekannter Nachahmer und Zeitgenossen (Steinmann, Geibel, Hektor, Müller/Wunderhorn). Sie zeigt, wie viele Entwurfstreffer ein fremder Text zufällig erzielt.
7. Gewicht in Teil III (gegen H2 und H3 gleich): Liegt der Kandidat über 95 % der Kontrollproben und ist mindestens ein Treffer unverwechselbar, +1; bei zwei oder mehr unverwechselbaren Treffern +1,5. Sonst 0. Ein Treffer nur in gedruckten Fassungen (P) zählt nicht, weil ihn ein Nachahmer kennen konnte.

**E-9 Absicherung gegen Nachahmung, Werkeffekte und Druckereffekte**. Festgelegt am 2026-10-17 vor jeder Rechnung. Grundlage: Delta (150 häufigste Wörter) und Zeichen-4-Gramme auf der angeglichenen Schicht, Blöcke zu 548 Wörtern, sonst wie II.3/II.4.

1. **E-9a Formeln und Reimwörter entfernt.** Im jeweils geprüften Text (Kandidat, A2-Probe, Gegenprobe) werden gestrichen: alle Reimwörter (letztes Wort jedes Verses) und alle Wörter, die ein Inhaltswortpaar bilden, das auch im Buch der Lieder steht (Paarbildung wie E-8; für A2-Proben ohne die Gedichte, die in der Probe stecken). Die Vergleichsklassen bleiben unverändert. Kalibrierung und Kandidat danach wie II.4/II.5. Wertung: Besteht die Kalibrierung (AUC offen gegen Müller/Wunderhorn ≥ 0,75) und bleibt der Kandidat heine-nah gegen Geibel und gegen Hektor, zählt das als Hinweis auf Verfasserschaft statt Pastiche: +0,25 für H1 : H3, Delta für H1 : H2 bleibt. Kippt der Kandidat (bei bestandener Kalibrierung) auf heine-fern, zählt das als Hinweis auf Pastiche: −0,25 für H1 : H3 und Delta für H1 : H2 auf 0. Besteht die Kalibrierung nicht: keine Änderung.
2. **E-9b Kalibrierung auf Werkebene.** Gegenproben werden nur gegen Vergleichsblöcke aus anderen Werken gemessen (Hektor: Vagabund gegen Schilda und umgekehrt, beide als eine Klasse; Geibel: jedes der drei Werke gegen die beiden anderen). A2-Proben wie bisher ohne die entsprechenden Gedichte des Buchs der Lieder. Die so gewonnenen LR ersetzen die bisherigen für Delta in Teil III (Punkte = Logarithmus des LR, höchstens wie bisher).
3. **E-9c Druckereffekt.** Alle Texte werden in Hektors Hausschreibung und die anderen Schreibungen gleichgezogen (ß → ss, „wol“ → „wohl“, Apostrophe weg); dann Zeichen-4-Gramme für H1 : H2 neu, und E-1 (Textverzerrung, 150 erhaltene Wörter) neu. Kehrt sich das Ergebnis des Kandidaten gegenüber Hektor um, war es ein Druckereffekt; dann entfällt der Vorbehalt „Richtung unter E-1 unsicher“ (bzw. er wird verstärkt, wenn das Gegenteil eintritt). Keine eigenen Punkte.

**E-10 Pointenzählung.** Festgelegt am 2026-10-19, 12:45, vor jeder Kodierung. Frage: Enden die Kandidaten seltener mit einer ironischen Pointe als vergleichbare Heine-Lieder und als zeitgenössische Nachahmungen? Einheit ist das Gedicht, beurteilt wird der Schluss (letzte Strophe, letzte zwei Verse).

- **Kodierung:** ja (1) = ironischer Umschlag oder Stimmungsbruch (Ernüchterung, Bathos, Selbstironie, Wechsel ins Prosaische); teilweise (0,5) = zugespitzte Wendung ohne Ironie (Antithese, Kontrast, Sentenz); nein (0) = der Schluss setzt die Stimmung fort, rundet ab oder steigert. Ein Kodierer, nicht verblindet; die Schlussverse jedes Gedichts werden zitiert, damit jede Entscheidung nachprüfbar ist.
- **Gruppen:** K = die 10 Kandidaten. H = Buch der Lieder (1827), Lyrisches Intermezzo und Heimkehr, alle Gedichte aus 2–4 vierzeiligen Strophen (113), daraus 30 per Zufall (Startwert 1848). N = Nachahmer: Liederbuch dreier Freunde (1843), Zweites Buch, alle Gedichte aus 2–6 vierzeiligen Strophen ohne die Byron-Übersetzungen, dazu die Singh-Funde Bd. 7–9 außer Auszügen.
- **Auswertung:** Anteil „ja“ je Gruppe mit Wilson-Intervall; LR für „0 Pointen in 10 Gedichten“ unter H gegen N (Binomial, Anteil geglättet (k+0,5)/(n+1)). Zählt nur für H1 : H3; für H2 kein Wert, weil ein Mystifikator Pointen bewusst meiden kann. Darf nicht zusätzlich zum geplanten Qualitätsurteil gezählt werden.

**E-11 Kalibrierung an zeitgenössischen Heine-Nachahmern.** Festgelegt am 2026-10-19, 13:15, vor jeder Rechnung mit den neuen Texten. Frage: Wie oft liegen Texte echter, von Zeitgenossen als heinisierend beurteilter Nachahmer mindestens so heine-nah wie der Kandidat? Das ersetzt die bisherige Gegenprobe gegen Geibel als Maß für H1 : H3.

- **Nachahmerklasse N (nur Verfasser mit eigenem vollen Block, keine Mischblöcke):** Wolfgang Müller, Junge Lieder (1841); Johannes Scherr, Laute und leise Lieder (1842); Theodor Storm und Theodor Mommsen, Liederbuch dreier Freunde (1843), je nach Inhaltsverzeichnis zugeordnet. Kurze Texte (Gaudy, Boas, Singh-Funde, Tycho Mommsen) bleiben draußen, weil sie keinen Block füllen. Otto Koch (Prosa) und Günther, Mohr (nicht beschafft) entfallen.
- **Text:** eigene Fraktur-OCR, Seitentitel, Seitenzahlen und Überschriften entfernt, sonst unkorrigiert; danach dieselbe Angleichung wie alle Texte (II.3). Die OCR-Fehlerquote wird an je zwei Seiten pro Band am Bild geschätzt und berichtet. OCR-Fehler entfernen einen Text eher von allen Vergleichsklassen; das kann Nachahmer heine-ferner erscheinen lassen und würde Heine begünstigen.
- **Maße, unverändert:** Delta über die 150 häufigsten Wörter, Zeichen-4-Gramme (Blöcke zu 548 Wörtern, Vokabular und z-Werte aus dem bisherigen Training, Nachahmer nicht im Training) und Versmerkmale wie E-7 (gleiches Versmaß, Blöcke zu 116 Versen). Wert je Block s = Abstand zu Geibel minus Abstand zu Heine A1, wie bisher.
- **Kennzahl je Maß:** Anteil der Nachahmer-Blöcke mit s mindestens so groß wie beim Kandidaten, verglichen mit dem Anteil der Heine-A2-Proben. LR = Anteil A2 / Anteil N (geglättet (k+0,5)/(n+1)), mit Wilson-Intervallen.
- **Tor je Maß:** AUC Heine-A2 gegen Nachahmer ≥ 0,75; sonst zählt das Maß 0.
- **Wertung für H1 : H3:** der Median der log10-LR der Maße, die das Tor bestehen, höchstens ±0,5. Er ersetzt die bisherigen H1 : H3-Werte für Delta (0) und E-3 (+0,2) in Teil III; nichts wird zusätzlich gezählt. H1 : H2 bleibt unberührt.
- **Grenze:** 4 Verfasser sind wenig; die Blöcke eines Verfassers sind nicht unabhängig. Berichtet wird deshalb auch der Anteil je Verfasser.

## Aus Teil III: Protokoll zur Vergleichsklasse (Prior)

**Protokoll Stufe 2a neu (Vergleichsklasse)**, festgelegt am 2026-10-20 vor jeder neuen Auszählung. Anlass: Die Funde vom 19./20.10. (Calvaire, Freimüthiger 1833, Zagreb 1842, „Michel“ 1847) erweitern die Klasse; die bisherige Tabelle enthält außerdem zwei Wertungen, die nicht mehr halten (Abendlieder als „unecht“, Calvaire „Boas“ statt Kalisch).

- **Aufnahmekriterien (alle müssen erfüllt sein):** K1 gedruckt zu Heines Lebzeiten (bis Februar 1856); K2 von Dritten, nicht von Heine selbst oder in seinem Auftrag; K3 im Druck als Heines ausgegeben (voller Name, „Heine“ oder eindeutige Chiffre); K4 als bis dahin ungedruckt präsentiert; K5 Verse; K6 ohne vorgelegte Handschrift. Prosa, Nachdrucke bereits gedruckter Heine-Texte und Parodien mit erkennbarer Parodie-Kennzeichnung fallen heraus.
- **Offene Abgrenzungsfragen, vor der Zählung von Ch. auf der Horst zu entscheiden:** (a) Zählt ein Namensvetter, der mit „Heine“ zeichnet, als Zuschreibung an Heine (K3)? (b) Wird zusätzlich eine engere Klasse „mit Fund- oder Herkunftsgeschichte“ gerechnet, die Hektors Fall näher ist?
- **Kodierung des Ausgangs:** echt = von der DHA als Heines anerkannt; unecht = anderer Verfasser nachgewiesen oder von Heine dokumentiert zurückgewiesen; offen = Urteil beruht nur auf Stil oder Konsens (so die Abendlieder nach dem Arbeitspapier vom 19.10.).
- **Rechnung:** Anteil echt = (k+1)/(k+u+2) ohne die offenen Fälle; Empfindlichkeit: offene Fälle je zur Hälfte als echt und unecht. Die neue ausgewogene Prior-Spanne reicht vom ungünstigeren zum günstigeren dieser beiden Werte. Die skeptische Spanne bleibt als Vergleich stehen.
- **Kandidaten (Kriterien noch zu prüfen, Ausgang noch nicht kodiert):** „Der Nachtschmetterling“ (Abendzeitung 1820); „Der Herbst“ (Abend-Zeitung 1821, Unterschrift „Heine“); Röpe, „Das Lied von der Liebe des Mondes“ (Wandsbecker Bote 1828, Chiffre); Abendlieder (Unser Planet 1831); Lieder im Freimüthigen 1833 (von Alexis als von Heine erhalten ausgegeben); An Rosa (Der Komet 1841); „War einst ein munterer Blonder“ (Croatia 1842); Neumann, „Den Gärtner ernährt sein Spaten“ (Croatia 1842 als „ungedrucktes Gedicht von H. Heine“); Calvaire (Die deutsche Flagge 1846); „Michel“ (Sir John Falstaff 1847, gezeichnet H. Heine).
