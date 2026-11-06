# -*- coding: utf-8 -*-
"""Wählt die Parameter der Studie.

Ohne Umgebungsvariable gilt Studie 1.

    AUTOR_STUDIE=2 python3 analyse/00_lauf.py
    AUTOR_STUDIE=3 python3 analyse/00_lauf.py

Studie 4, Studie 5 und Studie 6 hängen die Heine-Texte nicht aneinander.
Sie laufen nicht über 00_lauf.py, sondern über 11_studie4_naehe.py,
12_studie5_naehe.py und 13_studie6_trennung.py.
"""

import importlib
import os

_wahl = os.environ.get("AUTOR_STUDIE", "1")
_namen = {
    "1": "studie1_parameter",
    "2": "studie2_parameter",
    "3": "studie3_parameter",
    "4": "studie4_parameter",
    "5": "studie5_parameter",
    "6": "studie6_parameter",
}
if _wahl not in _namen:
    raise SystemExit("Unbekannte Studie: " + _wahl)
parameter = importlib.import_module(_namen[_wahl])
