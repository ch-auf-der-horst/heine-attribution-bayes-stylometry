# -*- coding: utf-8 -*-
"""Startet die Studie 1 in der festgelegten Reihenfolge.

Aufruf vom Projektordner aus:

    python3 analyse/00_lauf.py

Legt den Laufordner an und überschreibt ihn nicht, wenn er schon besteht.
Schreibt parameter.json und pakete.txt, dann die Skripte 01 bis 07.
Ein abgebrochener Ordner ohne ENTSCHEIDUNG.md wird nicht wiederverwendet.
Er bleibt liegen, damit der Abbruch sichtbar ist.
"""

import json
import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from laufwahl import parameter as p
import gemeinsame as g

SKRIPTE = (
    "01_proben_schneiden.py",
    "02_eichung_cosine_delta.py",
    "03_eichung_zeichengramme.py",
    "04_eichung_interpunktion.py",
    "05_eichung_auswerten.py",
    "06_impostors_kandidat.py",
    "07_versifikation.py",
    "08_abbildungen.py",
)


def main():
    g.selbsttest()
    if getattr(p, "EINZELTEXTE", False):
        raise SystemExit(
            "Diese Studie hängt die Heine-Texte nicht aneinander. Aufruf: " + p.AUFRUF
        )
    print("Dateiliste:", p.DATEILISTE.name)
    print("Laufordner:", p.LAUF)
    if p.LAUF.exists():
        raise SystemExit(
            "Der Laufordner besteht schon und wird nicht überschrieben: " + str(p.LAUF)
        )
    p.LAUF.mkdir(parents=True)
    parameter = {
        "seed": p.SEED,
        "lauf_datum": p.LAUF_DATUM,
        "probenlaenge": p.PROBENLAENGE,
        "wiederholungen": p.WIEDERHOLUNGEN,
        "mfw": p.MFW,
        "mfw_bericht": list(p.MFW_BERICHT),
        "zeichen_n": p.ZEICHEN_N,
        "zeichen_n_bericht": list(p.ZEICHEN_N_BERICHT),
        "zeichen_haeufigste": p.ZEICHEN_HAEUFIGSTE,
        "auc_schwelle": p.AUC_SCHWELLE,
        "anteil_versatz": p.ANTEIL_VERSATZ,
        "impostor_wiederholungen": p.IMPOSTOR_WIEDERHOLUNGEN,
        "impostor_merkmalanteil": p.IMPOSTOR_MERKMALANTEIL,
        "youden_minimum": p.YOUDEN_MINIMUM,
        "antwort_band": p.ANTWORT_BAND,
        "standardabweichung_ddof": p.STANDARDABWEICHUNG_DDOF,
        "dateiliste": str(p.DATEILISTE.relative_to(p.PROJEKT)),
    }
    (p.LAUF / "parameter.json").write_text(
        json.dumps(parameter, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (p.LAUF / "pakete.txt").write_text(
        "\n".join(
            [
                f"python {platform.python_version()}",
                f"numpy {np.__version__}",
                f"system {platform.platform()}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    for name in SKRIPTE:
        print("---", name)
        subprocess.check_call([sys.executable, str(p.ANALYSE / name)])


if __name__ == "__main__":
    main()
