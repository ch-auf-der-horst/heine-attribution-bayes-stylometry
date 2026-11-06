# Protokoll der diplomatischen Textschicht

Stand: 14. Oktober 2026.

> **Hinweis zum öffentlichen Stand:** Im Repositorium heißt dieser Ordner `korpus/`. Die unten beschriebenen Heine-Dateien (`Heine_*.txt`) und die Kandidatenteile unter `Kandidat/` sind nicht beigegeben; die Heine-Texte stammen aus DHA bzw. Heine-Portal. Die Erzeugungsskripte brauchen Vorlagen (TEI, DOCX, PDF), die ebenfalls nicht beigegeben sind; die fertigen Textdateien liegen bei.

Dieses Protokoll beschreibt den Ordner `corpus_diplomatisch/`. Es hält fest, welche Texte darin liegen, aus welcher Vorlage sie kommen, welche Form sie behalten, was ausgeschieden wurde und warum. Die Skripte in demselben Ordner erzeugen die Textdateien neu. Die `_ber`-Dateien an anderen Stellen des Projekts bleiben unberührt.

## Zweck

Die Schicht dient dem Vergleich von zehn Gedichten, die Enno Hektor 1848 im *Vagabund* (Hefte IV und V) als Heine-Texte von Norderney veröffentlicht hat. Der Kandidat umfasst 29 Strophen und 548 Wörter. Geprüft werden soll, ob diese Gedichte dem frühen Heine (etwa 1822–1826), Hektor oder nur dem Liedton der Zeit nahestehen.

Dafür braucht der Vergleich Verszeile, historische Schreibung, Kommata und Apostrophe. Eine ältere Schicht des Projekts, die Dateien mit dem Zusatz `_ber`, hatte Interpunktion und Anführungen entfernt und die Schreibung modernisiert. Diese Dateien dokumentieren die früheren Läufe. Sie werden nicht verbessert und nicht mit der diplomatischen Schicht in einen Ordner für stylo gelegt.

## Gemeinsame Form

Jede Textdatei ist UTF-8, Unicode-Normalform NFC, mit Zeilenumbruch LF und einer abschließenden Leerzeile. Ein Vers ist eine Zeile. Zwischen Strophen und zwischen Gedichten steht eine Leerzeile. Überschriften bleiben. Der Apostroph ist das gerade Zeichen U+0027. Geschützte Leerzeichen sind gewöhnliche Leerzeichen. Mehrfachleerzeichen sind zusammengezogen.

Beibehalten werden:

- die Schreibung der Vorlage, also auch `th`, `ey`, `ß` und nicht normalisierte Formen;
- Kommata, Punkte, Frage- und Ausrufezeichen, Gedankenstriche und Anführungen;
- Apostrophe und Elisionen als eigene Zeichen im Wort (`geh'`, `an's`, `hatt'`).

Nicht in den Text geschrieben werden editorische Siglen, Seitenzahlen, Inhaltsverzeichnisse, Vorworte, Essays, Register und Fußnoten. Druckfehler, die eine Vorlage selbst als solche ausweist, folgen der dort angegebenen Korrektur. Unmarkierte Abweichungen der Vorlage bleiben stehen und sind unten verzeichnet. Die Schreibung wird nicht nachträglich altertümelnd ergänzt und nicht stillschweigend modernisiert.

Wortzahlen in diesem Protokoll sind Folgen von Zeichen, die durch Leerraum getrennt sind. Überschriften und römische Gedichtnummern zählen mit.

Dieselbe Datei liegt, soweit unten nichts anderes steht, zusätzlich im Verfasserordner. Das sind Kopien, keine zweite Bearbeitung. Die Teile I–V und VI–X des Kandidaten liegen als `Kandidat_I-V.txt` und `Kandidat_VI-X.txt` nur unter `Kandidat/`, damit sie im Vergleichsordner nicht dreifach zählen.

## Dateinamen

Der Name hat die Form `Klasse_Stück.txt`. Das Feld vor dem ersten Unterstrich ist die Klasse, die stylo aus dem Dateinamen liest. Der ganze Name ohne Endung ist die Beschriftung in der Abbildung. Die Namen sind ASCII, ohne Leerzeichen, Klammern oder Kommata. Jahr und Vorlage stehen in diesem Protokoll, nicht im Dateinamen. `Heine_Ballade` ist *Götterdämmerung*, `Heine_Ratcliff` der dramatische Vers, `Mueller_2` der zweite Teil des *Waldhornisten*, `Geibel_Buecher` Widmung und vier Bücher. Der Ganztext von Schilda bleibt `Hektor/Hektor_Schilda_1847.txt` und liegt nicht in diesem Ordner. Die `_ber`-Dateien behalten ihre alten Namen.

Der Ordner ist das Reservoir. Er ist nicht der Eingabeordner eines einzelnen stylo-Laufs. Balladen, Sonette, Müller Teil 2 und das ganze *Wunderhorn* dürfen nicht ungeprüft zusammen mit den Liedern gemessen werden.

## Bestand

| Datei | Wörter | Zeilen | Apostrophe | Kommata | Rolle |
| --- | ---: | ---: | ---: | ---: | --- |
| `Kandidat_Vagabund.txt` | 548 | 164 | 11 | 56 | fraglicher Text, Gedichte I–X |
| `Heine_Aurora.txt` | 1089 | 225 | 57 | 134 | Heine, Strophenlied |
| `Heine_Biene.txt` | 351 | 84 | 4 | 32 | Heine, Strophenlied |
| `Heine_Almanach.txt` | 617 | 154 | 33 | 65 | Heine, Strophenlied |
| `Heine_Agrippina.txt` | 830 | 213 | 26 | 84 | Heine, Strophenlied |
| `Heine_Heimkehr.txt` | 2467 | 614 | 67 | 257 | Heine, Strophenlied |
| `Heine_Kevlaar.txt` | 397 | 101 | 19 | 46 | Heine, Strophenlied |
| `Heine_DonnaClara.txt` | 413 | 109 | 6 | 62 | Heine, Strophenlied |
| `Heine_Ballade.txt` | 608 | 89 | 29 | 67 | Heine, *Götterdämmerung*, eigene Datei |
| `Heine_Ratcliff.txt` | 747 | 112 | 24 | 95 | Heine, dramatischer Vers, eigene Datei |
| `Mueller_1.txt` | 11279 | 2520 | 473 | 1332 | Vergleich im Liedton, Teil 1 |
| `Mueller_2.txt` | 11974 | 2817 | 480 | 1234 | derselbe Verfasser, Teil 2, zurückgehalten |
| `Wunderhorn_1806.txt` | 53339 | 12351 | 303 | 7503 | anonyme Liedsammlung, kein Verfasserprofil |
| `Uhland_Lieder.txt` | 5985 | 1486 | 176 | 626 | Uhland, Lieder |
| `Uhland_Balladen.txt` | 23541 | 5147 | 669 | 2493 | Uhland, Balladen, eigene Datei |
| `Geibel_Lieder.txt` | 3847 | 925 | 109 | 414 | Geibel, 42 Lieder |
| `Geibel_Buecher.txt` | 22970 | 4580 | 628 | 2527 | Geibel, Widmung und vier Bücher |
| `Geibel_Sonette.txt` | 5264 | 972 | 117 | 541 | Geibel, Sonette und Distichen, eigene Datei |
| `Geibel_Junius.txt` | 4534 | 1072 | 104 | 432 | Geibel, *Juniuslieder* 1848, Abschnitt Lieder |
| `Hektor_Intro.txt` | 741 | 110 | 16 | 106 | Hektor, Introduktion 1843, eigene Datei |
| `Hektor_Schilda.txt` | 7396 | 1632 | 259 | 923 | Hektor, strophische Lieder aus Schilda; in den Abbildungen heißt das Blatt Schilda |
| `Hektor_Knittel.txt` | 577 | 128 | 27 | 61 | Hektor, Paarreim, eigene Datei |
| `Hektor_Ballade.txt` | 467 | 96 | 5 | 67 | Hektor, Ballade XXI, eigene Datei |
| `Hektor_XXXV.txt` | 393 | 81 | 27 | 55 | Hektor, XXXV und der folgende Einschub |
| `Hektor_LXX.txt` | 671 | 154 | 32 | 79 | Hektor, Gedichte LXX–LXXVII |
| `Hektor_Vagabund.txt` | 2143 | 480 | 29 | 260 | Hektor, Vagabunden-Lieder I–XVIII, 1848; eigener Text in Studie 5, nicht in den Studien 1–4 |
| `Steinmann_Lieder.txt` | 492 | 130 | 23 | 62 | Steinmann 1857, Strophenlieder ohne den Hofgarten; Probe von Studie 6, nicht Heine |
| `Steinmann_Sonette.txt` | 200 | 39 | 10 | 24 | Steinmann 1857, zwei Heine zugeschriebene Sonette; eigene Datei, nicht in den Studien 1–5 |

Die sieben strophischen Heine-Dateien von Aurora bis *Donna Clara* haben zusammen 6164 Wörter. *Götterdämmerung* und *Ratcliff* bleiben wegen der anderen Gedichtart eigene Dateien.

## Bearbeitung nach Vorlage

### Kandidat

Vorlage ist der Abdruck der Gedichte I–X, Seiten 662–666 eines Nachdrucks, in `Kandidat/Text_Kandidat.pdf`. Die Textdatei ist eine zeilengetreue Abschrift dieses Drucks, nicht die Ausgabe von `pdftotext`. Der Rahmentext „Ein merkwürdiger Fund“ und die Notiz von Gottschall sind nicht enthalten. Die römischen Nummern I.–X. stehen im Text. Die Gesamtdatei heißt `Kandidat_Vagabund.txt`. Die Teile I–V und VI–X heißen `Kandidat_I-V.txt` und `Kandidat_VI-X.txt` und liegen nur unter `Kandidat/`.

Im PDF und in einer älteren Docx-Fassung steht an mehreren Stellen die Ziffer 0 statt des Buchstabens O, und die Texterkennung liest „Feme“ und „schlieft“. Die Abschrift folgt dem Druck: Buchstabe O, „Ferne“, „schlief!“.

Skript: `erzeuge_diplomatische_texte.py`.

### Heine

Vorlagen sind die Docx-Dateien im Ordner `Heine/`, die Interpunktion und Apostrophe noch enthalten:

- `Heine_Aurora(1823).docx`
- `Heine_Die Biene_(1823:1826, anonym).docx`
- `Heine_Agrippina(1824, anonym).docx`
- `Heine_Westdeutscher Musenalmanach 1823.docx`
- `Heine_Heimkehr_Der Gesellschafter.docx`
- `Heine_Wallfahrt nach Kevlaar.docx`
- `Heine_Donna Clara.docx`
- `Heine_Götterdämmerung.docx`
- `Heine_Ratkliff.docx`

Ausgeschieden sind Zeilen der editorischen Nachweise: „Aurora“, „Siebzehn Lieder …“, „Nach HSA …“, „(nach HSA …)“, „Agrippina (= …)“, „Westdeutscher Musenalmanach …“, „&lt;ohne Titel&gt;“ und Zeilen, die mit „J3“ oder „DHA“ beginnen. Steht hinter einer DHA-Zeile noch ein Vers (`DHA I, 292 Auf den Wällen Salamankas`), bleibt der Vers. Die Zeichenfolge `{*}` im Musenalmanach wird zur Leerzeile.

In *Die Biene*, der *Wallfahrt nach Kevlaar*, *Donna Clara*, der *Götterdämmerung* und *Ratcliff* hängen in der Docx Verse ohne Leerzeichen aneinander. Getrennt wird nur dort, wo kein Leerzeichen steht: Kleinbuchstabe vor Großbuchstabe, Satzzeichen vor Großbuchstabe, Apostroph vor Großbuchstabe nach einem Kleinbuchstaben, ` --` vor Großbuchstabe. Ein Bindestrich innerhalb eines Wortes (`Liebes-Eyern`) trennt nicht. Ein Anführungszeichen mitten in der Zeile (`mir "Willkommen"`) trennt nicht. Ein schließendes Anführungszeichen, an dem der nächste Vers ohne Leerzeichen hängt (`Leute."Ein`), bleibt beim ersten Vers.

Abschnittszahlen, die in der Vorlage am Vers kleben, erhalten eine Leerzeile davor und danach. Geschwungene Apostrophe werden gerade. Der Mittelpunkt in `wollt'·ich` wird zum Leerzeichen.

Skript: `erzeuge_diplomatische_texte.py`.

### Müller

Vorlagen sind `Wilhelm Müller_1.docx` und `Müller_Waldhornist_2.docx` im Ordner `Müller/`. Der Ordnername kann in der Dateisystem-Normalform NFD stehen. Seitenzahlen der Form `[12]` sind entfernt. Überschriften bleiben. Teil 2 bleibt eine eigene Datei, damit ein Vergleich auf Teil 1 ihn auslassen kann.

Skript: `erzeuge_diplomatische_texte.py`.

### Wunderhorn

Vorlage ist `Arnim/arnim_wunderhorn01_1806.TEI-P5.xml`, Deutsches Textarchiv, *Des Knaben Wunderhorn*, Band 1, Heidelberg und Frankfurt: Mohr und Zimmer, 1806, DTA-Nummer 16523, TEI P5, Lizenz CC BY-SA 4.0.

Aufgenommen sind die 208 Lieder des Buchkörpers, mit Überschrift, Vers und Strophenabstand. Quellenvermerke unter den Liedern (`Mündlich`, fliegende Blätter und Ähnliches) sind nicht aufgenommen. Ebenfalls nicht aufgenommen sind die Widmung, der Aufsatz „Von Volksliedern“, die Nachschrift an den Leser, das Register der Liederanfänge und das Inhaltsverzeichnis. Das *Wunderhorn* ist eine Sammlung anonymer Lieder, bearbeitet von Arnim und Brentano. Die Datei ist deshalb kein Verfasserprofil Arnims.

Langes ſ wird s. Der Fraktur-Umlaut, ein Vokal mit übergesetztem e (U+0364), wird ä, ö oder ü. Vier Stellen, die das Textarchiv als Druckfehler ausweist (`kommeu`, `iu`, `Dusle`, `nnd`), folgen der dortigen Korrektur `<corr>`. Trennstriche am Zeilenende in Überschriften werden aufgelöst (`Blumengarten`).

Die älteren Dateien `arnim_wunderhorn01_1806 Kopie.txt`, `Kopie1_1.txt` und die vermischte Stichprobe werden nicht überschrieben und nicht verwendet.

Skript: `erzeuge_wunderhorn.py`.

### Uhland

Vorlage ist `Uhland/uhland_gedichte_1815.TEI-P5.xml`, Deutsches Textarchiv, Ludwig Uhland, *Gedichte*, Stuttgart und Tübingen: Cotta, 1815, erste Auflage, TEI P5, Lizenz CC BY-SA 4.0. Download: `https://www.deutschestextarchiv.de/book/download_xml/uhland_gedichte_1815`.

Zwei Dateien:

- `Uhland_Lieder.txt`, der Abschnitt „Lieder“, einschließlich der Frühlings- und Wanderlieder;
- `Uhland_Balladen.txt`.

Nicht aufgenommen sind Vorwort, Sinngedichte, Sonette, Oktaven, Glossen, die dramatischen Dichtungen und das Inhaltsverzeichnis. Sprecherzeilen in „Mönch und Schäfer“ bleiben. Fußnoten bleiben draußen, darunter der Hinweis zu Cervantes und die Erläuterung zu Graf Eberhard.

Langes ſ wird s. Der geschwungene Apostroph U+2019 wird der gerade Apostroph. Ein einzelner kombinierender Punkt über „Er“ in „Graf Eberhards Weißdorn“ entfällt, weil er kein Umlaut ist; die Zeile lautet `Er kam auf frommer Fahrt`. Drei Stellen, die das Textarchiv als Druckfehler ausweist (`uoch`, `Znm`, `Wanch`), folgen `<corr>`.

Die normalisierte TCF-Fassung des Textarchivs wird nicht verwendet. Die Lesefassung der Bibliotheca Augustana für Gedichte von 1822 bis 1829 wird nicht verwendet: sie ist neuhochdeutsch normalisiert (`Tal`, `Glut`, `sei`) und läge damit auf einer anderen Schreibebene als Heine.

Skript: `erzeuge_uhland.py`.

### Geibel

Vorlage der Gedichte von 1849 ist die eine Datei `Geibel/Geibel_Gedichte_1849_Antiqua_1.txt`, eine zeilengetreue Abschrift von Emanuel Geibel, *Gedichte*, 14. Auflage, Berlin: Alexander Duncker, 1849. Die historische Schreibung ist die des Drucks (`Stral`, `Thal`, `Anmuth`, `Aug'`).

Drei Dateien:

- `Geibel_Lieder.txt`, die 42 nummerierten Lieder;
- `Geibel_Buecher.txt`, die Widmung „An Clara Kugler“ und die vier Bücher;
- `Geibel_Sonette.txt`, „Sonette und Distichen aus Griechenland“ und „Neue Sonette“.

Ausgeschieden sind Titelblatt, Verlag, Inhaltsverzeichnis, Seitenzahlen (`[o. S.]`, `[S. 4]`, `[S. VIII]`), Zierlinien aus Gedankenstrichen und Sternchen sowie die Orts- und Datumszeile „Marienbad, im Julius 1846.“ Eingerückte Kehrreime bleiben eigene Verse. Die Quelldatei wird nicht überschrieben.

Für den Vergleich mit dem Kandidaten ist zuerst die Datei der 42 Lieder bestimmt. Die vier Bücher mischen Balladen und andere Gedichte. Die Sonette und Distichen bleiben außerhalb der Liedprobe.

Skript: `erzeuge_geibel.py`.

### Geibel, *Juniuslieder*

Vorlage ist der Druck Emanuel Geibel, *Juniuslieder*, Stuttgart und Tübingen: J. G. Cotta, 1848, Scan der Bayerischen Staatsbibliothek, bsb10108558. Eine diplomatische TEI gibt es nicht. Die Seiten des Abschnitts Lieder, Scan 15 bis 69, das sind die Druckseiten 3 bis 57, sind am Seitenbild abgeschrieben. Langes s ist s. Der Apostroph ist gerade. Deutsche Anführungen bleiben.

Eine Datei: `Geibel_Junius.txt`. Sie beginnt mit „Sei getrost“ und endet mit dem dritten Frühlingslied. Das Motto „Jede Jahreszeit“ auf der Vorseite ist als „Altes Lied“ bezeichnet und nicht Geibel; es fehlt. Titelblatt, Inhalt, Seitenzahlen, Stempel und der Durchdruck leerer Seiten fehlen. Die Überschrift „Vermischte Gedichte“ fehlt. Vermischte Gedichte, Zeitgedichte, Sonette, Gelegenheitsgedichte, der Troubadour, die Balladen, *König Sigurds Brautfahrt* und das Buch der Betrachtung sind noch nicht abgeschrieben.

Die Datei ist der einzige Geibel-Text in Studie 3. In Studie 1 und Studie 2 kommt sie nicht vor. Einzelne Gedichte dieser Sammlung stehen schon in den Gedichten von 1849. Die beiden Dateien dürfen nicht in denselben Eingabeordner.

Eine Stelle ist am engeren Ausschnitt gelesen: Druckseite 50, „Aus dir empor und kränzet klar“. Die erste Lesung *fränzet* war kein Wort.

Skript: `erzeuge_juniuslieder.py`. Es setzt die Seitenablesung in `Geibel/junius_lesen/` zusammen und überschreibt sie nicht.

### Hektor, *Lieder aus Schilda*

Vorlage sind die Dateien `Hektor_Schilda*.docx` im Ordner `Hektor/`. Verwendet werden die Transkriptionsprobe (PDF-Seiten 1–2) und die manuellen Abschriften der PDF-Seiten 3 bis 131. Die Datei `Hektor_Schilda_Fortsetzung_Arbeitsfassung.docx` wiederholt die Seiten 1–2 und 7–9 in schlechterer Form und ist nicht verwendet. Ab der Zeile „In unserm Verlage“ in der Datei der PDF-Seiten 129–131 beginnt eine Verlagsanzeige zu Hafis; sie und die Dateien der PDF-Seiten 132–142 sind nicht Hektor und fehlen im Text. Das Gedicht C und die Zeile `ENDE.` bleiben im Ganztext.

Die Zweitkollation vergleicht die Abschrift mit dem Druck `Hektor/Hektor_Lieder_aus_Schilda.pdf`. Zwei Leerzeichen in der Abschrift sind dort ein Zeilenbruch: der zweite Halbvers steht eingerückt in einer eigenen Zeile und ist im Text wieder eine eigene Zeile. Das ist an Gedicht I auf der Druckseite 9 nachgesehen. `scharfem Messer` und `faules Fleisch` bleiben innerhalb ihres Verses. Geschweifte Apostrophe sind gerade. Seitenvermerke, Klammern wie `(Anfang)` und redaktionelle Fortsetzungszeilen sind entfernt.

Einzelne Wörter folgen dem Druck, wo die Fraktur-Erkennung und das Seitenbild gegen die erste Abschrift stehen: `Wein her`, `Geistesfluthen`, `Witze über Witze`, `gilt`, `versteht`, `Pudelschaar`, `Sekundaner`, `Fragengesichtern`, `Entsinket`, `weih'`, `Schildanerinn`, `Expensen`, `Tutti`, `Exekutor`, `Ersiegt`, `Verleih'`, `keinen Poeten`, `grauser Leere`, `sinken wol`, `drall`, `Feten`, `Lämmerwolkenheerde`, `luftigen Ritt`, `unser Sabel`, `gleichwol`, `widerwärtig`, `Eseltreiber`, `Sturmesschwingen`, `fettste`, `Zitir'`, `O Lust`, `Zerplatze`. Die Überschrift lautet `Introduktion:`. Eine Zeile `(Fortsetzung LXXXIX.)` stand nicht im Druck und ist entfernt. Historische Schreibungen, die beide Lesungen tragen können, sind nicht nach der Erkennung modernisiert. Die römischen Nummern der Abschrift sind stehengeblieben, auch wo sie doppelt oder ungewöhnlich sind (`XXXX`, `LIIII`, zweimal `XXXVI`).

Jede Druckseite des Buchtextes ist mit der Abschrift wortweise abgeglichen. Die Fraktur-Erkennung verliest regelmäßig z und tz als s oder ss und lässt ck aus. Solche Treffer sind dieselbe Wortform und bleiben bei der Abschrift. Die übrigen Wortabweichungen sind am Seitenbild gelesen. Dabei sind `O Lust` und `Zerplatze` übernommen. `staubigen Alten` bleibt Alten: die frühere Lesung Akten war ein Verlesen der Type. `Herr Peß` bleibt stehen; die Type lässt Peß und Petz zu, und Petz wäre der Bär. Ebenso unentschieden, weil die Type sich zu nahe steht: `Maaßen`, `bißchen`, `jauchzt`, `Kolquinten`, `Stempelbogenfitzeln`, `Fratzen` und die römischen Nummern. Die Nummern sind dort, wo die Seite ohnehin offen lag, mit dem Druck gleich (I, XIV, XXXIV, LXXI). Eine eigene Nummernlesung jeder Überschrift ist nicht gemacht. Die Gedichte XIV und LXXI stimmen sonst Zeile für Zeile.

Nicht der ganze Band ist Knittelvers. Die meisten Gedichte sind Strophen mit Reim der geraden Zeilen, wie das Strophenlied. Paarreim, Zeile auf Zeile, steht in XVIII, LIIII, LIV, LXI, LXII, LXXXII und im `Te Deum` (C). Die Introduktion von 1843 ist eine siebenzeilige Strophe und eine eigene Datei. Die Ballade ist Gedicht XXI, nicht der Einschub bei XXXV. Die Datei zu XXXV enthält XXXV, das folgende Gedicht XXXVI und das erste XXXVII, in dem der Ton auf den Stolz wechselt. LXX bis LXXVII sind die Liebesgedichte und eine eigene Datei; LXXV reimt darin paarweise. Dieselben Texte liegen unter `Hektor/`. Der Ganztext `Hektor/Hektor_Schilda_1847.txt` hat 10246 Wörter. Er liegt nicht in `corpus_diplomatisch/`, damit die Teile nicht doppelt gezählt werden.

Skript: `erzeuge_schilda.py`.

### Hektor, Vagabunden-Lieder 1848

Vorlage ist der Druck *Der Vagabund*, Hefte Sommermond VI bis Windmond XI 1848, Scan `Hektor/Nachtraege/Vagabund_Hektor_Gedichte.pdf`. Die Zeitschrift erscheint unter Hektors Namen. Die Abteilung heißt Vagabunden-Lieder und zählt die Gedichte I bis XVIII. Das ist nicht der Kandidat. Der Kandidat sind die Heine zugeschriebenen Gedichte aus den Heften IV und V und liegt in `Kandidat_Vagabund.txt`.

Aufgenommen sind nur die achtzehn Strophenlieder. Jedes Gedicht ist in vierzeilige Strophen gesetzt, mit Reim der geraden Zeilen, wie die strophischen Lieder in `Hektor_Schilda.txt`. Es sind nicht dieselben Gedichte: kein Anfang der Vagabunden-Lieder steht in der Schilda-Datei. Der Paarreim der Datei `Hektor_Knittel.txt` ist damit nicht die einzige Versart Hektors in diesen Jahren. Die Prosastücke desselben Drucks fehlen, weil sie eine andere Textart sind: *Ein Sommernachtstraum*, *Der dumme Tobi* und *Biographie eines armen Teufels*. Zeitschriftkopf, Seitenzahlen und die wiederholte Überschrift fehlen.

Die Abschrift ist am Seitenbild gelesen. Die Fraktur-Erkennung des Scans und die ältere Datei `Hektor/Vagabund/Hektor_Gedichte_Vagabund_1848.txt` sind nur zum Vergleich herangezogen. Diese ältere Datei endet beim Wesir-Gedicht und modernisiert an mehreren Stellen; sie ist nicht überschrieben. Die Datei mit `_ber` ist nicht verwendet. Langes s ist s. Der Apostroph ist gerade. Deutsche Anführungen bleiben. Gedicht XVIII, das Gefängnis-Lied, steht im Druck und in der neuen Datei.

Die Datei liegt in `corpus_diplomatisch/` und als Kopie in `Hektor/`. Studie 5 liest sie als eigenen Text neben `Hektor_Schilda.txt`. Die Dateilisten der Studien 1 bis 4 bleiben bei `Hektor_Schilda.txt`.

Am engen Ausschnitt gelesen und so belassen: `pußt` in V, nicht zu putzt geändert; `an zu fingen` in XI, der Buchstabe hat den Querstrich des f; `sit neben mir` in XVIII, die Type ist kürzer als sitzt; `Langeweil` ohne Apostroph; das Komma in `vom, eigenen Herd`. `schoß` in IX ist die Lesung des Seitenbildes.

Skript: `erzeuge_vagabund.py`. Es setzt die Seitenablesung in `Hektor/Vagabund/lesen/vagabund_lieder.txt` zusammen und überschreibt sie nicht.

### Steinmann, Denkwürdigkeiten 1857

Vorlage ist Friedrich Arnold Steinmann, *H. Heine. Denkwürdigkeiten und Erlebnisse*, 1857, Scan `A_Administration/Steinmann_Heine Denkwürdigkeiten(1857).pdf`. Steinmann schreibt die Gedichte Heine zu und führt sie als verstreute Stücke aus dessen Berliner Jahren vor. Die Harz-Strophen stellt er als einen später verworfenen Prolog zur Harzreise vor, anstelle von „Schwarze Röcke, seid'ne Strümpfe“. Die Dateien heißen nicht `Heine_`. Sie werden dem Heine-Bestand nicht zugeschlagen und stehen in keiner Dateiliste der Studien 1 bis 5. So können sie als Probe dienen, ob das Verfahren eine Heine-Nachdichtung von den frühen Heine-Liedern trennt. Diese Probe ist Studie 6. Die Zahlen stehen in `ergebnisse/studie6/NAEHE.md`, nicht hier.

`Steinmann_Lieder.txt` ist nach der ersten Abschrift geändert. Sie enthält „Zuckerpastillen für die Geliebte“ I–V, „Lieder“ I–II und die sechs Strophen ohne eigene Überschrift von den Seiten 193–194. „Parodie“, „Wandelnde Blumen in Berlin“ und „Im Hofgarten zu Düsseldorf“ stehen nicht darin. In „Lieder“ I steht `Schätze`. `Steinmann_Sonette.txt` enthält „Burleskes Sonett“ und „Dresdener Poesie“. Sonette bleiben eine eigene Datei.

Nicht aufgenommen sind der Prosarahmen, die Seitenzahlen, das Sternchen der Fußnote und das Schiller-Zitat aus „Die Theilung der Erde“, das Steinmann in der Erzählung der ersten Rezension anführt. Die Abschrift ist am Seitenbild gelesen. Die Textebene des Google-Books-Scans ist nur zum Vergleich herangezogen; sie setzt Leerzeichen vor die Satzzeichen und liest an zwei Stellen anders. Langes s ist s. Der Apostroph ist gerade. Deutsche Anführungen bleiben. Dieselben Dateien liegen unter `Steinmann/`.

Am engen Ausschnitt der Sonette gelesen und so belassen: `Zuleht`, die Type hat h und kein zweites l; `hündisch`, die Textebene des Scans liest dort händisch. `Nostitz` ist die Lesung der Type; die Textebene lässt das t aus. Eine eigene Datei `Steinmann_Nachlese.txt` liegt nicht mehr im Ordner.

Skript: `erzeuge_steinmann.py`. Es setzt die Seitenablesung in `Steinmann/lesen/` zusammen und überschreibt sie nicht.

## Ausgeschieden und warum

| Nicht aufgenommen | Grund |
| --- | --- |
| alle Dateien mit `_ber` | Interpunktion entfernt, Schreibung modernisiert; eigene, ältere Schicht |
| Ordner `corpus/` | enthält nur diese `_ber`-Dateien |
| `Heine_Anonyma` | weitgehend *Die Biene*, danach wenige weitere Verse; keine eigene diplomatische Vorlage |
| *Nordsee* | freie Rhythmen, andere Gedichtart als das Strophenlied |
| *Buch der Lieder*, 1827 | spätere Fassung und Mischung der Jahre; die frühen Drucke sind einzeln vorhanden |
| Hektor, die Heine zugeschriebenen Gedichte im *Vagabund*, Hefte IV und V, und die älteren Fraktur-Erkennungen dazu | IV und V sind der Kandidat in `Kandidat_Vagabund.txt`; die Erkennung dieser Seiten bleibt unbrauchbar. Die eigenen Vagabunden-Lieder I–XVIII aus den Heften VI–XI sind davon getrennt und liegen in `Hektor_Vagabund.txt` |
| Hektor, Prosa im *Vagabund* 1848 | *Ein Sommernachtstraum*, *Der dumme Tobi*, *Biographie eines armen Teufels*; andere Textart als das Strophenlied |
| Steinmann, Prosarahmen der *Denkwürdigkeiten* 1857 | Seitenzahlen, Fußnote zur Parodie, Erzählung der Rezension und das darin angeführte Schiller-Zitat; die Gedichte selbst liegen in `Steinmann_Lieder.txt` und `Steinmann_Sonette.txt` |
| Hektor, PDF- und OCR-Fassungen von *Schilda* | nicht zeilengetreu; ersetzt durch die Docx-Abschriften |
| Hektor, Verlagsanzeige ab PDF-Seite 131 und die Dateien 132–142 | nicht Hektor, sondern eine Anzeige zu Hafis |
| Hektor, `Fortsetzung_Arbeitsfassung.docx` | Doppelung der Seiten 1–2 und 7–9, schlechtere Form |
| Uhland, Bibliotheca Augustana, Gedichte 1822–1829 | modernisierte Schreibung |
| Uhland, TextGrid, Ausgabe letzter Hand | modernisierte Schreibung einer Anordnung nach der Ausgabe von 1861 |
| Wunderhorn, Vorwort, Essay, Nachschrift, Register | Prosa oder Beiwerk; würde die Bearbeiter statt des Liedtons messen |
| Geibel, Sonette und Distichen, in der Liedprobe | andere Gedichtart |
| Uhland, Sonette und Dramen | andere Gedichtart; gar nicht erst ausgezogen |

## Stellen, die absichtlich stehengeblieben sind

Diese Formen stehen so in der Vorlage und sind nicht verbessert worden:

- *Die Biene*: `Stralte`.
- Heimkehr im *Gesellschafter*: `Bey dir sjtzen`, `Sie Stadt verlassen`, `Und wenn du stirbst, s.o will ich`.
- Uhland, „Gesang der Nonnen“: `Liebeswonue`.
- Geibel: `Ächte Weihe` und die übrigen historischen Schreibungen des Drucks von 1849.
- Vagabunden-Lieder: `pußt`, `an zu fingen`, `sit neben mir`, `Langeweil` ohne Apostroph, das Komma in `vom, eigenen Herd`.
- Steinmann 1857, Sonette: `Zuleht`, `hündisch`.

In der Heimkehr-Vorlage weicht die Kommazahl um das Komma der ausgeschiedenen DHA-Zeile von der Docx ab. Dasselbe gilt für *Götterdämmerung* und *Ratcliff*. Die Apostrophzahlen stimmen mit den Vorlagen überein.

## Was noch fehlt

Schilda ist seitenweise mit dem Druck abgeglichen. Unentschieden bleiben `Herr Peß`, `Maaßen`, `bißchen`, `jauchzt`, `Kolquinten`, `Stempelbogenfitzeln`, `Fratzen` und die römischen Nummern.

Nicht vorgesehen für diese Schicht sind Eichendorff, Fouqué und Lehmann. Uhland liegt mit den *Gedichten* von 1815 vor. Eine diplomatische Fassung der Uhland-Gedichte von 1822 bis 1829 gibt es im Deutschen Textarchiv nicht.

Von den *Juniusliedern* 1848 ist der Abschnitt Lieder abgeschrieben. Die übrigen Teile des Bandes, von den vermischten Gedichten bis zu *König Sigurds Brautfahrt*, sind noch nicht abgeschrieben.

## Reproduzierbarkeit

Im Ordner `corpus_diplomatisch/`:

- `erzeuge_diplomatische_texte.py` schreibt Kandidat, Heine und Müller neu;
- `erzeuge_wunderhorn.py` schreibt das *Wunderhorn* neu;
- `erzeuge_uhland.py` schreibt die beiden Uhland-Dateien neu;
- `erzeuge_geibel.py` schreibt die drei Geibel-Dateien von 1849 neu;
- `erzeuge_juniuslieder.py` setzt `Geibel_Junius.txt` aus der Seitenablesung neu zusammen;
- `erzeuge_schilda.py` schreibt die sechs Hektor-Teile und den Ganztext `Hektor/Hektor_Schilda_1847.txt` neu;
- `erzeuge_vagabund.py` setzt `Hektor_Vagabund.txt` aus der Seitenablesung in `Hektor/Vagabund/lesen/` neu zusammen;
- `erzeuge_steinmann.py` schrieb die erste Steinmann-Abschrift. Die jetzige Datei `Steinmann_Lieder.txt` ist danach von Hand geändert und wird von diesem Skript nicht wiederhergestellt.

Die Skripte lesen die Vorlagen in den Verfasserordnern und schreiben nach `corpus_diplomatisch/` sowie in den jeweiligen Verfasserordner. Ein erneuter Lauf überschreibt diese Textdateien. Die Quelldateien (Docx, PDF, TEI, die Geibel-Abschrift) und alle `_ber`-Dateien lässt er stehen.

Die erste Zuschreibungsstudie steht unter `analyse/`. Ihr Protokoll ist `analyse/PROTOKOLL_STUDIE1.md`. Sie liest die Dateiliste `analyse/studie1_dateien.csv` und schreibt nach `ergebnisse/studie1/`. Studie 2 wiederholt dasselbe ohne die Texte Geibels und schreibt nach `ergebnisse/studie2/`. Studie 3 wiederholt dasselbe mit den Juniusliedern von 1848 anstelle der Geibel-Lieder von 1849 und schreibt nach `ergebnisse/studie3/`. Der Ordner `corpus_diplomatisch/` ist dafür nicht der Eingabeordner.

Wunderhorn und Uhland unterliegen der Lizenz CC BY-SA 4.0 des Deutschen Textarchivs. Wird der Ordner öffentlich weitergegeben, bleiben diese Angabe und die Lizenz bei den beiden Texten.
