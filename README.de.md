# Heine Attribution Studies

Daten, Skripte und Prüfprotokolle zur Echtheitsprüfung von Texten, die Heinrich Heine zugeschrieben oder abgesprochen wurden. Die Prüfungen verbinden philologische Befunde mit kalibrierter Stilometrie in einer bayesianischen Bilanz: Jeder Befund wird als Likelihood-Quotient gewichtet, die Ausgangswahrscheinlichkeit stammt aus einer Referenzklasse vergleichbarer Fälle, und die Unsicherheit wird in Sensitivitätsläufen ausgewiesen.

*English version: [README.md](README.md)*

## Fälle

| Ordner | Gegenstand | Beitrag |
|---|---|---|
| `vagabund-1848/` | zehn Gedichte, die Enno Hektor 1848 in *Der Vagabund* als auf Norderney gefundene Gedichte Heines druckte | auf der Horst, ‚Authenticity as probability‘, eingereicht bei *Digital Scholarship in the Humanities* |

Jeder Ordner hat ein eigenes README mit Aufbau, Reproduktionsanleitung und Zuordnung der Skripte zu Tabellen und Abbildungen.

## Schnellprüfung

```
pip install -r requirements.txt
python vagabund-1848/pruefe.py
```

Das prüft die Prüfsummen, die CSV- und JSON-Dateien und die sechs Skripte, die ohne Heine-Texte laufen. Installation, geprüfte Versionen und Einzelheiten stehen im README des jeweiligen Falls.

## Sprache

Die READMEs liegen auf Englisch und Deutsch vor. Prüfprotokolle, Berichte, Kommentare im Code und Dateinamen sind deutsch, ebenso die untersuchten Texte.

## Einsatz von KI-Werkzeugen

Bei der Entwicklung des Codes und der Aufbereitung der Daten wurden KI-gestützte Werkzeuge (Cursor, Claude) eingesetzt; der Verfasser hat den Code geprüft und die Rechnungen wiederholt. Einzelheiten nennt das AI Disclosure Statement des Beitrags.

## Zitieren

Bitte den Beitrag und dieses Repositorium (Version 1.0.0) zitieren. Eine mit DOI archivierte Fassung folgt mit der Veröffentlichung. Angaben in `CITATION.cff`.

## Lizenz

Code: MIT (`LICENSE`). Eigene Transkriptionen, Protokolle, Ergebnisse, Abbildungen und Dokumentation: CC BY 4.0. Texte aus dem Deutschen Textarchiv: CC BY-SA 4.0. Texte nach modernen wissenschaftlichen Ausgaben und Daten des Heine-Portals sind nicht enthalten. Einzelheiten in `LICENSE-DATEN.md`.

## Kontakt

Christoph auf der Horst, Heinrich-Heine-Universität Düsseldorf  
ORCID: [0000-0002-9372-7537](https://orcid.org/0000-0002-9372-7537)  
GitHub: [ch-auf-der-horst](https://github.com/ch-auf-der-horst)
