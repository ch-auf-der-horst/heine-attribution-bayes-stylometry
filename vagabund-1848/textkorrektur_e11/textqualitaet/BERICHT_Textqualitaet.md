# Textqualität der Hauptauswertung: Bestandsaufnahme und Fehlerquoten

Stand: 30. Oktober 2026. Schritte 1 und 2 der Textprüfung. Es wurde nichts geändert und nichts neu gerechnet.

## 1. Bestandsaufnahme

Grundlage sind die Skripte in `Repositorium_Vorbereitung/Bayes_Arbeitsskripte/kal/` (Klassen in `prep.py`, Nachahmer in `e11prep.py`) und das Protokoll `corpus_diplomatisch/PROTOKOLL.md`.

**Automatische Auffälligkeiten** (`qual.py`): Großbuchstaben mitten im Wort, Ziffern im Wort, Wörter ohne Vokal, typische Fraktur-Fehlformen (fich, ift, uud, dcr …), Sonderzeichen im Wort. Diese Zählung findet nur grobe Fehler; Verlesungen, die wie echte Wörter aussehen (vas für das), erfasst sie nicht.

| Text | Herkunft | Wörter | auffällig je 1000 |
|---|---|---:|---:|
| Kandidat | Abschrift am Druck | 542 | 0,0 |
| Heine, *Buch der Lieder* 1827 | DTA-Transkription, am D1-Faksimile restituiert (`out/Restitution_Protokoll.md`) | 29.059 | 0,6 |
| Heine A2 (Erstdrucke, DHA I Anhang) | Heine-Portal | 17.980 | 0,1 |
| Heine, Einzeltexte (Aurora … Ratcliff) | Docx-Vorlagen | 6.164 | ≈ 0 |
| Hektor, *Vagabund*-Lieder | am Seitenbild gelesen | 2.136 | 0,0 |
| Hektor, *Schilda* | Abschrift, Zweitkollation am Druck | 7.327 | 1,2 |
| Steinmann | am Seitenbild gelesen | 489 | 0,0 |
| Geibel, Lieder / *Juniuslieder* / Bücher | Abschrift 1849 / am Seitenbild gelesen | 3.826 / 4.494 / 22.793 | 0,8 / 0,0 / 0,2 |
| W. Müller 1 / 2 | Docx-Vorlagen | 11.261 / 11.936 | 0,2 / 0,3 |
| *Wunderhorn* | DTA (TEI) | 53.295 | 0,2 |
| Uhland, Lieder | DTA (TEI) | 5.981 | 0,0 |
| **Scherr 1842** (E-11) | **Texterkennung**, regelbereinigt | 12.989 | **3,6** |
| **Müller v. Königswinter 1841** (E-11) | **Texterkennung** | 8.648 | **1,9** |
| **Storm 1843** (E-11) | **Texterkennung** | 4.095 | **1,5** |
| **Th. Mommsen 1843** (E-11) | **Texterkennung** | 9.828 | **2,0** |

Ergebnis: Alle Texte außer den vier Nachahmertexten von E-11 sind abgeschrieben, am Seitenbild gelesen oder stammen aus dem Deutschen Textarchiv. Unkorrigierte Texterkennung betrifft nur E-11 (zusammen rund 35.500 Wörter). Diese Klasse trägt in der Bilanz den Befund der offenen Gegenprobe (+0,43 gegenüber H3, Abschnitt 7.4) und Abb. 1.

Zwei Restpunkte außerhalb von E-11: Für die Heine-Einzeltexte und für W. Müller ist die Vorlage der Docx-Dateien im Protokoll nicht nachgewiesen. Der A2-Text des Heine-Portals enthält nach dem Restitutionsprotokoll vereinzelte Portalfehler („Vielchen“, „Städchen“); diese Klasse ist nicht stichprobenhaft am Druck geprüft.

## 2. Fehlerquote der E-11-Texte

**Verfahren** (`stich.py`, `wer.py`, Startwert 20261030): je Text drei Zufallsseiten mit mindestens 60 Wörtern; Vergleich des bereinigten OCR-Seitentexts, wie er in `e11/texte/` eingeht, mit einer Abschrift am Seitenbild (`ref/`). Gezählt werden Wortfehler (Ersetzung, Auslassung, Einfügung) ohne Groß- und Kleinschreibung, Apostroph und Satzzeichen; römische Gedichtnummern bleiben außer Betracht. Langes s gilt als s.

| Text | Fehler / Wörter | Wortfehlerquote | 95-%-Bereich |
|---|---:|---:|---:|
| Scherr 1842 | 21 / 316 | **6,6 %** | 4,4–9,9 % |
| Storm 1843 | 7 / 340 | 2,1 % | 1,0–4,2 % |
| Müller v. Königswinter 1841 | 3 / 216 | 1,4 % | 0,5–4,0 % |
| Th. Mommsen 1843 | 3 / 337 | 0,9 % | 0,3–2,6 % |
| zusammen | 34 / 1.209 | 2,8 % | 2,0–3,9 % |

Die bisherige Angabe in Endnote 7 („etwa 3 %“) trifft für die Klasse insgesamt zu, verdeckt aber, dass Scherr deutlich schlechter ist.

**Systematische Fehler**

- **d als v gelesen (Scherr):** vas, ven, vem, vie, vu, vurch … im ganzen Scherr-Text 74-mal, bei Müller v. K. 10-mal, bei Mommsen 3-mal. Das trifft Funktionswörter und damit genau die Merkmale, auf denen die Delta-Maße beruhen.
- **tz und ck:** lezten, lebte (letzte), Feßen (Fetzen), Antlig/Antliß (Antlitz), Blie (Blicke).
- **f/k und s/f:** flar (klar), Neft (Nest), Fenießend (genießend).
- **Worttrennung am Zeilenende** bei langen Versen (Mommsen, Scherr): „zehn- tausend“ wird zu zwei Wörtern; zusammen 16 Stellen.
- **Fremdtext:** Das englische Burns-Motto vor Scherrs „Lebwohl“ steht im Scherr-Text. Weitere Mottos sind wahrscheinlich.
- **Verworfene Seite:** Scherr, Bild 102 (rund 100 Wörter), fiel wegen eines Bibliotheksvermerks auf der Seite ganz heraus.

## Folgerung

Die Korrektur lohnt sich und ist überschaubar. Vordringlich ist Scherr. Bei Storm, Müller v. K. und Mommsen genügen gezielte Korrekturen der systematischen Fehler, eine Durchsicht am Seitenbild und das Entfernen von Fremdtext.

## Dateien

- `qual.py`: automatische Auffälligkeiten
- `stich.py`, `auswahl.json`: Stichprobenziehung
- `ocrseiten/`: geprüfte OCR-Seiten; `ref/`: Abschrift am Seitenbild
- `wer.py`, `wer_e11.json`: Fehlerzählung mit allen Einzelfehlern
