# Nicht enthaltene Eingaben

*English summary below.*

Einige Eingaben der Rechnungen dürfen oder sollen nicht veröffentlicht werden: Heine-Texte nach der Düsseldorfer Ausgabe (DHA) und dem Heine-Portal, daraus abgeleitete Proben, urheberrechtlich geschützte Literatur sowie umfangreiche Arbeitsmaterialien der Texterfassung. Dieses Verzeichnis nennt für jede fehlende Datei den Ort, an dem die Skripte sie erwarten, und ihre SHA-256-Prüfsumme (`eingaben_nicht_enthalten.csv`, 1.048 Dateien). Wer die Dateien aus den Quellen neu herstellt, kann sie damit Byte für Byte prüfen. Weicht eine neu hergestellte Datei ab, sind auch die Ergebnisse nicht ohne Weiteres vergleichbar.

Alle Zielpfade sind relativ zu diesem Ordner (`vagabund-1848/`). Die Skripte in `bayes/kal/` finden das Korpus über `pfade.py` unter `korpus/`.

## Gruppen

| Gruppe | Zielpfad | Inhalt und Quelle | Herstellung | gebraucht für |
|---|---|---|---|---|
| G1 | `korpus/Heine_*.txt` (9 Dateien) | Heines Gedichte der frühen Drucke (Aurora, Die Biene, Musenalmanach, Agrippina, Heimkehr, Kevlaar, Donna Clara, *Götterdämmerung*, *Ratcliff*), Text nach DHA bzw. Heine-Portal | `korpus/erzeuge_diplomatische_texte.py`; Vorlagen, Umfang und Eingriffe in `korpus/PROTOKOLL.md` | Vorstudien (`stilometrie/`), Kontrollen |
| G2 | `bayes/out/Heine_Buch_der_Lieder_1827_restituiert.txt` | Klasse A1: *Buch der Lieder*, Erstdruck Hamburg 1827 (D1), restituiert | Eingriffe in `bayes/out/Restitution_Protokoll.md` | alle Rechnungen mit A1 |
| G3 | `bayes/out/A2/` (Manifest, 178 Gedichte, 33 Blöcke) | Klasse A2: Heines Erstdrucke und DHA-Anhang bis März 1824, aus DHA 1 im Heine-Portal | Auswahl nach Protokoll II.3, Punkt 4; je Gedicht DHA-Seite, Gedichtanfang, Umfang und Prüfsumme in `bayes/out/A2/A2_Manifest_Metadaten.csv`; Blöcke chronologisch nach `bayes/out/A2/A2_Bloecke.csv` | Kalibrierung, offene Gegenprobe, Verblindung, E-1 bis E-3, E-7, E-9, E-11, Abb. 1, Tippett-Plot |
| G4 | `bayes/norm/out/` (angeglichene Fassungen) | angeglichene Schicht von G1 bis G3 | `bayes/norm/apply.py` mit den Regeln aus Protokoll II.3, Punkt 5; Ersetzungen in `bayes/norm/` | wie G3 |
| G5 | `korpus/verblindung/blind/*/X01, X05, X08`; `korpus/verblindung/pool/*/P01–P03`; dieselben Pool-Dateien unter `bayes/kal/vb/pool/` | die drei Heine-Proben (A2) der Verblindung | `korpus/verblindung/verblinden.py` (Startwert 20261016); Zuordnung im veröffentlichten Schlüssel `korpus/verblindung/schluessel/schluessel.json` | Verblindung (`bayes/kal/blind.py` bricht ohne sie ab) |
| G6 | `bayes/nf/pages.json`, `korpus/e5/dha02_nf.json` | Lesarten und Texte aus DHA I und DHA II („Neuer Frühling“), Heine-Portal | Auszug der im Protokoll E-8 genannten Seiten | E-6, E-8, Anm. 10 |
| G7 | `bayes/e10/` (Kodierung) | Pointenzählung; zitiert die Schlussverse jedes Gedichts | Kodierung nach `bayes/e10/PROTOKOLL.md` | E-10 |
| G8 | `bayes/e4/e4_input.json` | Abfrageliste der Wortschatzdatierung mit der Heine-Kontrollprobe | aus den Proben nach Protokoll E-4 | E-4 |
| G9 | `bayes/e11/mu/`, `bayes/e11/sc/`, `bayes/e11/sct/`, `bayes/lb/` | rohe Fraktur-OCR der Nachahmerbände (Müller 1841, Scherr 1842, *Liederbuch dreier Freunde* 1843) | eigene OCR; historische Aufbereitung `bayes/kal/e11prep.py` | nicht nötig: Die am Seitenbild korrigierten Seiten liegen in `textkorrektur_e11/werkzeug/seiten_korrigiert.tgz`, die fertigen Texte in `bayes/e11/texte/` |
| G10 | `korpus/Heines_Werk_Urteil_Zeitgenossen/` | Singh (Hg.), *Heinrich Heines Werk im Urteil seiner Zeitgenossen*, Bd. 7–9 (PDF und Text) | urheberrechtlich geschützt | E-10 (Gruppe N), Recherche |
| G11 | `explorativ_ausserhalb_protokoll/Explorativ_E11_Klassen/texte/H1b_*.txt`, `H1c_*.txt` | Teilklassen H1b (halbanonyme Gedichte 1824–26) und H1c (*Neue Gedichte* 1844) | `explorativ_ausserhalb_protokoll/Explorativ_E11_Klassen/werkzeug/`; Prüfsummen auch in `texte/SHA256SUMS.txt` | nur explorative Rechnung |

## Reihenfolge für einen Neulauf

1. G1 bis G3 aus den Quellen herstellen und gegen die Prüfsummen prüfen.
2. G4 mit `bayes/norm/apply.py` erzeugen.
3. G5 nicht neu ziehen, sondern die drei Proben nach `korpus/verblindung/pool/pool.json` und dem Schlüssel aus G3 zusammensetzen; `verblinden.py` bricht ab, weil der Schlüssel schon besteht.
4. Dann `bayes/kal/calib.py`, `openset.py`, `blind.py`, `e1.py` bis `e9c.py`, `e11.py` (Reihenfolge wie in `README.de.md`).

Die Prüfsummen und Herstellungsangaben ersetzen nicht die Texte. Sie machen nachprüfbar, ob eine neu hergestellte Eingabe der verwendeten entspricht.

## English summary

Some inputs cannot or should not be published: Heine’s texts from the Düsseldorf edition (DHA) and the Heine-Portal, samples derived from them, copyrighted literature, and bulky working material from text capture. `eingaben_nicht_enthalten.csv` lists every missing file (1,048) with the path at which the scripts expect it, relative to this folder, and its SHA-256 checksum, so that inputs rebuilt from the sources can be verified byte for byte. The table above (in German) groups them by content, source, how they were produced and which analyses need them. For class A2, `bayes/out/A2/A2_Manifest_Metadaten.csv` gives the DHA page, first line, size and checksum of each poem.
