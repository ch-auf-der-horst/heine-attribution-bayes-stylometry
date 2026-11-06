# -*- coding: utf-8 -*-
"""Festgelegte Parameter der Studie 1.

Diese Datei ist die einzige Stelle, an der Probenlänge, Seed,
Merkmalzahlen und Schwellen stehen. Die übrigen Skripte lesen sie.
Geändert wird sie vor einem neuen Lauf, nicht danach.

Die Probenlänge ist die Wortzahl von Kandidat_Vagabund.txt.
Ein Wort ist eine durch Leerraum getrennte Zeichenfolge, wie im
Korpusprotokoll. Der Kandidat wird nicht auf 550 Wörter gerundet
und nicht gekürzt.
"""

from pathlib import Path

PROJEKT = Path(__file__).resolve().parents[1]
ANALYSE = Path(__file__).resolve().parent
DATEILISTE = ANALYSE / "studie1_dateien.csv"

STUDIE_NAME = "Studie 1"
SEED = 20261013
LAUF_DATUM = "2026-10-13"
LAUF = PROJEKT / "ergebnisse" / "studie1" / f"lauf_{LAUF_DATUM}_seed{SEED}"

PROBENLAENGE = 548
WIEDERHOLUNGEN = 100

# Häufigste Wörter. Die Eichschwelle gilt allein für MFW.
# MFW_BERICHT wird mitgerechnet und nicht zur Entscheidung verwendet.
MFW = 150
MFW_BERICHT = (100, 300)

# Zeichengramme. Die Eichschwelle gilt allein für ZEICHEN_N.
ZEICHEN_N = 4
ZEICHEN_N_BERICHT = (3, 5)
ZEICHEN_HAEUFIGSTE = 500

# Ein Verfasserpaar gilt als getrennt, wenn die AUC mindestens so hoch ist
# und derselbe Wert in mindestens diesem Anteil der Versatz-Wiederholungen
# der Worthäufigkeiten wieder erreicht wird.
AUC_SCHWELLE = 0.75
ANTEIL_VERSATZ = 0.95

IMPOSTOR_WIEDERHOLUNGEN = 500
IMPOSTOR_MERKMALANTEIL = 0.5
YOUDEN_MINIMUM = 0.5
ANTWORT_BAND = 0.05

# Standardabweichung wie scale() in R: Teilung durch n - 1.
STANDARDABWEICHUNG_DDOF = 1
