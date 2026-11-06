# -*- coding: utf-8 -*-
"""Eicht Cosine Delta auf Zeichengrammen.

Liest teilung.json und baut die Proben neu. Der Kandidat wird nicht
geöffnet. Die häufigsten n-Gramme werden nur aus den Heine- und
Hektor-Proben gewählt. Die Kette ist die kleingeschriebene Probe,
Token durch ein Leerzeichen getrennt, Satzzeichen bleiben in der Kette.

Die Entscheidungsschwelle gilt für ZEICHEN_N. ZEICHEN_N_BERICHT
wird nur mitgeteilt. Versatz-Wiederholungen laufen für ZEICHEN_N.

Schreibt 03_zeichen.json und 03_zeichen_versatz.csv.
"""

import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g


def eiche(proben, n):
    merkmale = g.merkmal_ngramme(proben, n, p.ZEICHEN_HAEUFIGSTE)
    relativ = g.matrix_ngramme(proben, merkmale, n)
    abstand, behalten = g.kosinus_delta(relativ)
    klassen = ["heine"] * (len(proben) // 2) + ["hektor"] * (len(proben) // 2)
    gleich, verschieden = g.paare(abstand, klassen, {"heine", "hektor"})
    auc = g.auc_gleiche_naeher(gleich, verschieden)
    return {
        "n": n,
        "merkmale_mit_streuung": int(behalten.sum()),
        "paare_gleich": int(len(gleich)),
        "paare_verschieden": int(len(verschieden)),
        "median_gleich": float(np.median(gleich)),
        "median_verschieden": float(np.median(verschieden)),
        "auc": auc,
    }


def main():
    teilung = g.lese_json(p.LAUF / "teilung.json")
    primaer = g.proben_primaer(teilung)
    proben = primaer["heine"] + primaer["hektor"]
    basis = eiche(proben, p.ZEICHEN_N)
    bericht = {str(n): eiche(proben, n)["auc"] for n in p.ZEICHEN_N_BERICHT}

    heine, _ = g.wortstrom("heine")
    hektor, _ = g.wortstrom("hektor")
    zeilen = []
    for nummer, block in enumerate(teilung["versatz"], start=1):
        wiederholung = g.proben_aus(heine, block["heine_starts"]) + g.proben_aus(
            hektor, block["hektor_starts"]
        )
        zahlen = eiche(wiederholung, p.ZEICHEN_N)
        zeilen.append({"wiederholung": nummer, "auc": zahlen["auc"]})
    anteil = float(np.mean([zeile["auc"] >= p.AUC_SCHWELLE for zeile in zeilen]))

    with (p.LAUF / "03_zeichen_versatz.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["wiederholung", "auc"])
        writer.writeheader()
        for zeile in zeilen:
            writer.writerow({"wiederholung": zeile["wiederholung"], "auc": f"{zeile['auc']:.10f}"})
    g.schreibe_json(
        p.LAUF / "03_zeichen.json",
        {
            "merkmal": "zeichengramme",
            "haeufigste": p.ZEICHEN_HAEUFIGSTE,
            "primaer": basis,
            "auc_bericht": bericht,
            "anteil_versatz_ueber_schwelle": anteil,
            "versatz_schwelle": p.AUC_SCHWELLE,
        },
    )
    print(f"AUC Zeichen-{p.ZEICHEN_N}-Gramme: {basis['auc']:.4f}")
    print(f"Anteil der Versatz-Wiederholungen über {p.AUC_SCHWELLE}: {anteil:.2f}")


if __name__ == "__main__":
    main()
