# Fall 1: Die ‚Norderneyer‘ Gedichte des *Vagabund* (1848)

*English version: [README.md](README.md)*

Texte, Skripte, Prüfprotokolle und Ergebnisse zum Beitrag:

> Christoph auf der Horst: Authenticity as probability: the ‘Norderney’ poems in *Der Vagabund* (1848) and attribution practice in Heine scholarship. Eingereicht bei *Digital Scholarship in the Humanities*.

Eine mit DOI archivierte Fassung folgt mit der Veröffentlichung.

## Gegenstand

Enno Hektor druckte 1848 in seiner Emder Zeitschrift *Der Vagabund* (Hefte IV und V) zehn Gedichte als auf Norderney gefundene Lieder Heinrich Heines. Seit Franzos (1903) und Elster (1925) gelten sie als Werk von Hektors Freund Ernst Warnebold. Der Beitrag prüft die Zuschreibung mit einer bayesianischen Bilanz und kalibrierter Stilometrie. Dieser Ordner macht die Rechnungen nachvollziehbar.

## Aufbau

| Ordner oder Datei | Inhalt |
|---|---|
| `korpus/` | diplomatische Texte des Kandidaten und der Vergleichsautoren (ohne Heine); Erzeugungsskripte; `PROTOKOLL.md` zu Vorlagen und Eingriffen; Verblindung (Pool, Proben, Schlüssel) |
| `bayes/` | Kalibrierung, verblindete Anwendung und Einzelprüfungen E-1 bis E-11 (`kal/`), Angleichung der Schreibung (`norm/`), Nachahmertexte der Gegenprobe (`e11/texte/`), Bilanz (`bilanz/`) |
| `textkorrektur_e11/` | Korrektur der Nachahmertexte am Seitenbild: Bericht, Änderungsprotokoll, Stichproben, Nachrechnung, Daten und Skripte der Abbildungen |
| `abbildungen/` | Abb. 1 und 2 des Beitrags, Tippett-Plot (Anm. 9) |
| `stilometrie/` | Vorstudien außerhalb des Protokolls (Abschnitt 7.6): Skripte, Protokolle, Ergebnisse in Textform |
| `explorativ_ausserhalb_protokoll/` | Unterteilung von H1 und H3 (Anm. 4) und weitere Nachahmerläufe, mit Hinweisen zu den Grenzen der Deutung |
| `quellen/` | Zeitungsrecherche zu Warnebold mit Suchprotokollen (Anm. 3) |
| `PROTOKOLLE_II3_II3a.md` | die datierten Prüfprotokolle II.3 und II.3a (E-1 bis E-11) und das Protokoll zur Vergleichsklasse aus dem Arbeitsdokument (mit englischer Zusammenfassung) |
| `EINGABEN_NICHT_ENTHALTEN.md`, `eingaben_nicht_enthalten.csv` | nicht veröffentlichte Eingaben mit Zielpfad, Quelle, Herstellung und SHA-256-Prüfsumme |
| `LITERATUR.md` | vollständige Angaben zu den Kurzbelegen in diesem Ordner |
| `pruefe.py` | automatische Prüfung des öffentlichen Stands (s. u.) |

## Installation

Python 3.10 oder neuer. Aus dem Wurzelordner des Repositoriums:

```
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # genau geprüfter Stand: requirements-getestet.txt
cd vagabund-1848
```

Geprüft wurde der öffentliche Stand in zwei Umgebungen: Python 3.13.16 mit den Versionen aus `requirements-getestet.txt` sowie Python 3.10.12 mit NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.9, scikit-learn 1.7.2 und Pillow 12.3.0.

## Ohne Heine-Texte nachrechenbar

Sechs Skripte laufen allein mit den Dateien dieses Ordners. Aufruf aus diesem Ordner:

```
python bayes/bilanz/posterior.py                                  # Abschnitt 8.2, Tab. 5
python bayes/bilanz/schwelle.py                                   # Abschnitt 8.3, Anm. 12
python textkorrektur_e11/nachrechnung/tab5_warnebold_neutral.py   # Tab. 5, Zeile ‚Warnebold-Befund gegenüber H3 neutral‘
python textkorrektur_e11/nachrechnung/abb1_EN.py                  # Abb. 1 (aus abb_daten2_korr.json)
python textkorrektur_e11/nachrechnung/abb2_EN.py                  # Abb. 2
python textkorrektur_e11/nachrechnung/tippett_EN.py               # Tippett-Plot und Cllr, Anm. 9 (aus abb_daten2_korr.json)
```

Die Abbildungsskripte schreiben ihre Dateien nach `textkorrektur_e11/nachrechnung/abb/`. Sie verwenden die Schrift Inter, wenn sie installiert ist, sonst die mit Matplotlib gelieferte DejaVu Sans; die Abbildungen unterscheiden sich dann nur in der Schrift von den veröffentlichten.

`python pruefe.py` prüft den öffentlichen Stand in einem Lauf: die Prüfsummen nach `../MANIFEST.sha256`, den Aufbau aller CSV- und JSON-Dateien und die sechs Skripte mit ihren erwarteten Ergebnissen (in einer Wegwerfkopie). Auf GitHub läuft dieselbe Prüfung automatisch (`.github/workflows/pruefung.yml`).

Alle übrigen Rechnungen (Stilometrie, Kalibrierung, verblindete Anwendung, Gegenprobe mit den Nachahmern, Einzelprüfungen E-1 bis E-11) brauchen die Heine-Texte, die hier nicht veröffentlicht werden können. `EINGABEN_NICHT_ENTHALTEN.md` verzeichnet, was fehlt, wo die Skripte es erwarten und wie es hergestellt wurde. Die Ergebnisse dieser Rechnungen stehen in den JSON- und CSV-Dateien und Berichten neben den Skripten.

## Historische Aufbereitungsskripte

Die folgenden Skripte dokumentieren, wie Texte und Proben hergestellt wurden. Sie gehören nicht zur Auswertung und sind nicht für einen Neulauf gedacht: Sie brauchen Vorlagen, die nicht beigegeben sind (Seitenbilder, OCR-Seiten, Word-Transkriptionen, DHA-Daten), und einige würden beigegebene Dateien überschreiben. Mehrere brechen inzwischen vor jedem Schreibzugriff ab, wenn Eingaben fehlen.

- `korpus/erzeuge_*.py`, `korpus/verblindung/*.py`, `bayes/kal/vb/*.py` (Texte und Verblindung; `verblinden.py` verweigert den Lauf, weil der Schlüssel schon besteht)
- `bayes/norm/*.py`, `bayes/e4/prep.py` (Angleichung, Vorbereitung von E-4)
- `bayes/kal/e11prep.py` (rohe OCR der Nachahmerbände; würde die korrigierten Texte überschreiben und bricht ohne `E11PREP_NEU=1` ab)
- `textkorrektur_e11/werkzeug/*`, `textkorrektur_e11/textqualitaet/*` (Korrektur Seite für Seite und Fehlerquoten; die korrigierten Seiten liegen in `seiten_korrigiert.tgz`)
- `explorativ_ausserhalb_protokoll/*/werkzeug/*`
- `quellen/warnebold/zeitungen/*/recherchiere_warnebold_zeitungen.py` (fragt ein Online-Zeitungsportal ab; die Ergebnisse sind im selben Ordner protokolliert)

## Zuordnung zum Beitrag

| Beitrag | Dateien |
|---|---|
| Tab. 2, Abschnitt 5.3 | `bayes/bilanz/referenzklasse.csv` (Fallliste mit Belegen; die Zählung für die Rechnung steht in `posterior.py`) |
| Tab. 3, Anm. 11 (skeptische Werte) | `bayes/bilanz/befunde.csv` |
| Abschnitt 6.4, Pointenzählung | `bayes/e10/PROTOKOLL.md` (die Kodierung zitiert Heine-Verse und ist nicht enthalten) |
| Tab. 4, Abschnitt 7.2 | `bayes/kal/calib.py`, `kalibrierung.json`; Versmerkmale `e3.py`; offene Gegenprobe `openset.py` |
| Abschnitt 7.3, Anm. 6 | `bayes/kal/blind.py`, `blind_ergebnis.json`, `korpus/verblindung/` |
| Abschnitt 7.4, Abb. 1 | `bayes/kal/e11.py`, `e11.json`; `textkorrektur_e11/nachrechnung/abb_daten2_korr.py`, `abb1_EN.py` |
| Abschnitt 7.5 | Einzelprüfungen `bayes/kal/e1.py` bis `e9c.py` (der Kopf jedes Skripts nennt das Protokoll) |
| Abschnitt 7.6 | `stilometrie/` |
| Abschnitt 8.2, Tab. 5, Abb. 2 | `bayes/bilanz/posterior.py`; `textkorrektur_e11/nachrechnung/abb2_EN.py`, `tab5_warnebold_neutral.py` |
| Abschnitt 8.3, Anm. 12 | `bayes/bilanz/schwelle.py` |
| Anm. 8 | `textkorrektur_e11/` |
| Anm. 9 (Bootstrap, Cllr, Tippett-Plot) | `textkorrektur_e11/nachrechnung/abb_daten2_korr.py`, `tippett_EN.py`, `abbildungen/Tippett_Repositorium.*` |
| Anm. 10 (Nähe zum *Buch der Lieder*) | `bayes/nf/e8.py` (braucht die Heine-Texte) |

## Prüfsummen

Maßgeblich ist `../MANIFEST.sha256`; es erfasst jede Datei der veröffentlichten Fassung. Einige Ordner enthalten ältere Prüfsummenlisten aus der Arbeit; sie bleiben als historische Nachweise unverändert:

- `bayes/e11/texte/SHA256SUMS.txt` nennt die Pfade mit dem Präfix `texte_neu/`, dem Ordner, in dem die korrigierten Texte zusammengesetzt wurden. Prüfung im selben Ordner mit `sed 's#texte_neu/##' SHA256SUMS.txt | sha256sum -c`.
- Die `*.sha256`-Dateien in `explorativ_ausserhalb_protokoll/` datieren die Protokollentwürfe und enthalten nach der Prüfsumme eine Zeitzeile.
- `explorativ_ausserhalb_protokoll/Explorativ_E11_Klassen/texte/SHA256SUMS.txt` führt auch vier nicht beigegebene Heine-Dateien (H1b, H1c); ihre Prüfsummen stehen auch in `eingaben_nicht_enthalten.csv`.

## Vorab-Festlegung

Die Prüfprotokolle wurden im Arbeitsdokument jeweils vor dem Öffnen des Kandidaten datiert; sie sind in `PROTOKOLLE_II3_II3a.md` wiedergegeben. Eine externe Registrierung gab es nicht. Nachträgliche Entscheidungen und Abweichungen weist der Beitrag in Abschnitt 5.5 und Tab. 5 aus.

## Einsatz von KI-Werkzeugen

Bei der Entwicklung des Codes und der Aufbereitung der Daten wurden KI-gestützte Werkzeuge (Cursor, Claude) eingesetzt. Der Verfasser hat ihren Einsatz gesteuert, den Code geprüft und die Rechnungen wiederholt. Einzelheiten nennt das AI Disclosure Statement des Beitrags.

## Lizenz

Code: MIT. Eigene Transkriptionen, Protokolle und Ergebnisse: CC BY 4.0. Texte aus dem Deutschen Textarchiv (*Des Knaben Wunderhorn* 1806, Uhland 1815, die 20 Prosaausschnitte in `korpus/e5/dta_prosa_e5.json`), einschließlich ihrer angeglichenen Fassungen und der daraus gezogenen Proben: CC BY-SA 4.0. Einzelheiten in `../LICENSE` und `../LICENSE-DATEN.md`.

## Kontakt

Christoph auf der Horst, Heinrich-Heine-Universität Düsseldorf  
ORCID: [0000-0002-9372-7537](https://orcid.org/0000-0002-9372-7537)
