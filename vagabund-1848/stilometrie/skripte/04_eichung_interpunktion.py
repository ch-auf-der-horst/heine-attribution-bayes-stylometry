# -*- coding: utf-8 -*-
"""Eicht Cosine Delta auf den Interpunktionshäufigkeiten.

Liest teilung.json. Der Kandidat wird nicht geöffnet.
Gezählt wird je  Wort der Probe. Ein Bindestrich zwischen zwei
Buchstaben zählt nicht als Satzzeichen. Der Apostroph zählt auch dann,
wenn er im Wort steht.

Diese Eichung geht nicht in die Entscheidungsschwelle ein.
Sie wird nur mitgeteilt, einschließlich der Versatz-Wiederholungen.

Schreibt 04_interpunktion.json und 04_interpunktion_versatz.csv.
"""

import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g


def eiche(proben):
    relativ, namen = g.matrix_interpunktion(proben)
    abstand, behalten = g.kosinus_delta(relativ)
    klassen = ["heine"] * (len(proben) // 2) + ["hektor"] * (len(proben) // 2)
    gleich, verschieden = g.paare(abstand, klassen, {"heine", "hektor"})
    auc = g.auc_gleiche_naeher(gleich, verschieden)
    return {
        "merkmale": [namen[i] for i, nehmen in enumerate(behalten) if nehmen],
        "paare_gleich": int(len(gleich)),
        "paare_verschieden": int(len(verschieden)),
        "median_gleich": float(np.median(gleich)),
        "median_verschieden": float(np.median(verschieden)),
        "auc": auc,
    }


def main():
    teilung = g.lese_json(p.LAUF / "teilung.json")
    primaer = g.proben_primaer(teilung)
    basis = eiche(primaer["heine"] + primaer["hektor"])
    heine, _ = g.wortstrom("heine")
    hektor, _ = g.wortstrom("hektor")
    zeilen = []
    for nummer, block in enumerate(teilung["versatz"], start=1):
        wiederholung = g.proben_aus(heine, block["heine_starts"]) + g.proben_aus(
            hektor, block["hektor_starts"]
        )
        zeilen.append({"wiederholung": nummer, "auc": eiche(wiederholung)["auc"]})
    anteil = float(np.mean([zeile["auc"] >= p.AUC_SCHWELLE for zeile in zeilen]))
    with (p.LAUF / "04_interpunktion_versatz.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["wiederholung", "auc"])
        writer.writeheader()
        for zeile in zeilen:
            writer.writerow({"wiederholung": zeile["wiederholung"], "auc": f"{zeile['auc']:.10f}"})
    g.schreibe_json(
        p.LAUF / "04_interpunktion.json",
        {
            "merkmal": "interpunktion",
            "primaer": basis,
            "anteil_versatz_ueber_schwelle": anteil,
            "geht_in_die_schwelle_ein": False,
        },
    )
    print(f"AUC Interpunktion: {basis['auc']:.4f}")


if __name__ == "__main__":
    main()
