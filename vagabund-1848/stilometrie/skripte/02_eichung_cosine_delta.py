# -*- coding: utf-8 -*-
"""Eicht Cosine Delta auf den häufigsten Wörtern.

Liest den Laufordner: teilung.json. Die Wortströme werden aus
corpus_diplomatisch/ neu aufgebaut. Der Kandidat wird nicht geöffnet.
Die Merkmale werden nur aus den Heine- und Hektor-Proben der jeweiligen
Teilung gewählt. Pronomen werden nicht gestrichen.

Die Entscheidungsschwelle gilt für MFW aus studie1_parameter.py.
Die Werte in MFW_BERICHT werden nur mitgeteilt.

Schreibt:
- 02_woerter.json
- 02_woerter_merkmale.txt
- 02_woerter_abstaende.csv
- 02_woerter_versatz.csv
"""

import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g


def kennzahlen(gleich, verschieden, auc):
    return {
        "paare_gleich": int(len(gleich)),
        "paare_verschieden": int(len(verschieden)),
        "median_gleich": float(np.median(gleich)),
        "median_verschieden": float(np.median(verschieden)),
        "perzentil95_gleich": float(np.percentile(gleich, 95)),
        "perzentil05_verschieden": float(np.percentile(verschieden, 5)),
        "auc": auc,
    }


def eiche(proben, anzahl):
    merkmale = g.merkmal_woerter(proben, anzahl)
    relativ = g.matrix_woerter(proben, merkmale)
    abstand, behalten = g.kosinus_delta(relativ)
    klassen = ["heine"] * (len(proben) // 2) + ["hektor"] * (len(proben) // 2)
    gleich, verschieden = g.paare(abstand, klassen, {"heine", "hektor"})
    auc = g.auc_gleiche_naeher(gleich, verschieden)
    return merkmale, relativ, abstand, behalten, klassen, kennzahlen(gleich, verschieden, auc)


def main():
    teilung = g.lese_json(p.LAUF / "teilung.json")
    primaer = g.proben_primaer(teilung)
    proben = primaer["heine"] + primaer["hektor"]
    if len(primaer["heine"]) != len(primaer["hektor"]):
        raise SystemExit("Heine und Hektor haben unterschiedlich viele Primärproben")

    merkmale, relativ, abstand, behalten, klassen, basis = eiche(proben, p.MFW)
    bericht = {}
    for anzahl in p.MFW_BERICHT:
        _, _, _, _, _, zahlen = eiche(proben, anzahl)
        bericht[str(anzahl)] = zahlen["auc"]

    heine, _ = g.wortstrom("heine")
    hektor, _ = g.wortstrom("hektor")
    versatz_zeilen = []
    for nummer, block in enumerate(teilung["versatz"], start=1):
        wiederholung = g.proben_aus(heine, block["heine_starts"]) + g.proben_aus(
            hektor, block["hektor_starts"]
        )
        _, _, _, _, _, zahlen = eiche(wiederholung, p.MFW)
        versatz_zeilen.append({"wiederholung": nummer, "auc": zahlen["auc"]})
    anteil = float(np.mean([zeile["auc"] >= p.AUC_SCHWELLE for zeile in versatz_zeilen]))

    (p.LAUF / "02_woerter_merkmale.txt").write_text(
        "\n".join(merkmale) + "\n", encoding="utf-8"
    )
    with (p.LAUF / "02_woerter_abstaende.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["i", "klasse_i", "j", "klasse_j", "abstand", "paar"]
        )
        writer.writeheader()
        n = len(klassen)
        for i in range(n):
            for j in range(i + 1, n):
                writer.writerow(
                    {
                        "i": i,
                        "klasse_i": klassen[i],
                        "j": j,
                        "klasse_j": klassen[j],
                        "abstand": f"{abstand[i, j]:.10f}",
                        "paar": "gleich" if klassen[i] == klassen[j] else "verschieden",
                    }
                )
    with (p.LAUF / "02_woerter_versatz.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["wiederholung", "auc"])
        writer.writeheader()
        for zeile in versatz_zeilen:
            writer.writerow({"wiederholung": zeile["wiederholung"], "auc": f"{zeile['auc']:.10f}"})

    mittel = relativ.mean(axis=0)
    streuung = relativ.std(axis=0, ddof=p.STANDARDABWEICHUNG_DDOF)
    g.schreibe_json(
        p.LAUF / "02_woerter.json",
        {
            "merkmal": "haeufigste_woerter",
            "mfw": p.MFW,
            "merkmale_mit_streuung": int(behalten.sum()),
            "primaer": basis,
            "auc_bericht": bericht,
            "anteil_versatz_ueber_schwelle": anteil,
            "versatz_schwelle": p.AUC_SCHWELLE,
            "mittel": mittel.tolist(),
            "streuung": streuung.tolist(),
        },
    )
    print(f"AUC Wörter, MFW {p.MFW}: {basis['auc']:.4f}")
    print(f"Anteil der Versatz-Wiederholungen über {p.AUC_SCHWELLE}: {anteil:.2f}")


if __name__ == "__main__":
    main()
