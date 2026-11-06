# -*- coding: utf-8 -*-
"""Parameter der Studie 2.

Dieselben Schwellen, dieselbe Probenlänge und derselbe Seed wie Studie 1.
Geändert ist nur die Dateiliste: kein Text von Geibel geht in die Rechnung.
Der Lauf liegt direkt unter ergebnisse/studie2/.
"""

from pathlib import Path

PROJEKT = Path(__file__).resolve().parents[1]
ANALYSE = Path(__file__).resolve().parent
DATEILISTE = ANALYSE / "studie2_dateien.csv"

STUDIE_NAME = "Studie 2"
SEED = 20261013
LAUF_DATUM = "2026-10-13"
LAUF = PROJEKT / "ergebnisse" / "studie2"

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
