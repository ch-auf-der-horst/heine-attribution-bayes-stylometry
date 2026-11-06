# -*- coding: utf-8 -*-
"""Parameter der Studie 4.

Dieselben Schwellen, dieselbe Probenlänge und derselbe Seed wie Studie 1.
Die Dateiliste ist die der Studie 3: der einzige Geibel-Text ist der
Abschnitt Lieder der Juniuslieder von 1848. Die Heine-Dateien bleiben
einzeln. Sie werden nicht aneinandergehängt. Deshalb läuft diese Studie
nicht über 00_lauf.py.
"""

from pathlib import Path

PROJEKT = Path(__file__).resolve().parents[1]
ANALYSE = Path(__file__).resolve().parent
DATEILISTE = ANALYSE / "studie4_dateien.csv"

STUDIE_NAME = "Studie 4"
EINZELTEXTE = True
AUFRUF = "AUTOR_STUDIE=4 python3 analyse/11_studie4_naehe.py"
SEED = 20261013
LAUF_DATUM = "2026-10-13"
LAUF = PROJEKT / "ergebnisse" / "studie4"

PROBENLAENGE = 548
WIEDERHOLUNGEN = 100

MFW = 150
MFW_BERICHT = (100, 300)

ZEICHEN_N = 4
ZEICHEN_N_BERICHT = (3, 5)
ZEICHEN_HAEUFIGSTE = 500

AUC_SCHWELLE = 0.75
ANTEIL_VERSATZ = 0.95

IMPOSTOR_WIEDERHOLUNGEN = 500
IMPOSTOR_MERKMALANTEIL = 0.5
YOUDEN_MINIMUM = 0.5
ANTWORT_BAND = 0.05

STANDARDABWEICHUNG_DDOF = 1
