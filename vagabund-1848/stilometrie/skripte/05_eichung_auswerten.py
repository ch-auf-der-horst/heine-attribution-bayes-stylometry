# -*- coding: utf-8 -*-
"""Liest die drei Eichungen und legt fest, ob die Impostors-Prüfung
eine Zuschreibung tragen kann.

Das Tor ist offen, wenn die Primär-AUC der häufigsten Wörter und die
Primär-AUC der Zeichen-4-Gramme mindestens AUC_SCHWELLE erreichen und
mindestens ANTEIL_VERSATZ der Wort-Wiederholungen dieselbe Schwelle
erreichen. Die Interpunktion öffnet das Tor nicht.

Schreibt eichung_tor.json, abstand_woerter.svg und dieselbe Abbildung als PNG.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g


def svg(abstaende_csv, ziel):
    gleich = []
    verschieden = []
    for zeile in abstaende_csv.read_text(encoding="utf-8").splitlines()[1:]:
        felder = zeile.split(",")
        wert = float(felder[4])
        if felder[5] == "gleich":
            gleich.append(wert)
        else:
            verschieden.append(wert)
    breite, hoehe = 640, 160

    def x(wert):
        return 40 + min(max(wert, 0.0), 2.0) / 2.0 * 560

    zeilen = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="40" y="24" font-family="sans-serif" font-size="14">Cosine Delta, häufigste Wörter</text>',
        '<text x="40" y="70" font-family="sans-serif" font-size="12">gleicher Verfasser</text>',
        '<text x="40" y="120" font-family="sans-serif" font-size="12">Heine gegen Hektor</text>',
    ]
    for wert in gleich:
        zeilen.append(f'<circle cx="{x(wert):.1f}" cy="78" r="2.5" fill="#1f4e79" opacity="0.45"/>')
    for wert in verschieden:
        zeilen.append(f'<circle cx="{x(wert):.1f}" cy="128" r="2.5" fill="#8c3a2f" opacity="0.45"/>')
    zeilen.append("</svg>")
    g.schreibe_svg(ziel, "\n".join(zeilen) + "\n")


def main():
    woerter = g.lese_json(p.LAUF / "02_woerter.json")
    zeichen = g.lese_json(p.LAUF / "03_zeichen.json")
    interpunktion = g.lese_json(p.LAUF / "04_interpunktion.json")
    auc_woerter = woerter["primaer"]["auc"]
    auc_zeichen = zeichen["primaer"]["auc"]
    anteil = woerter["anteil_versatz_ueber_schwelle"]
    gruende = []
    if auc_woerter < p.AUC_SCHWELLE:
        gruende.append(
            f"AUC der Wörter {auc_woerter:.4f} liegt unter {p.AUC_SCHWELLE}"
        )
    if auc_zeichen < p.AUC_SCHWELLE:
        gruende.append(
            f"AUC der Zeichen-{p.ZEICHEN_N}-Gramme {auc_zeichen:.4f} liegt unter {p.AUC_SCHWELLE}"
        )
    if anteil < p.ANTEIL_VERSATZ:
        gruende.append(
            f"Nur {anteil:.2f} der Wort-Wiederholungen erreichen {p.AUC_SCHWELLE}"
        )
    tor = not gruende
    g.schreibe_json(
        p.LAUF / "eichung_tor.json",
        {
            "tor_offen": tor,
            "auc_woerter": auc_woerter,
            "auc_zeichen": auc_zeichen,
            "auc_interpunktion": interpunktion["primaer"]["auc"],
            "anteil_versatz_woerter": anteil,
            "auc_schwelle": p.AUC_SCHWELLE,
            "anteil_schwelle": p.ANTEIL_VERSATZ,
            "gruende": gruende,
        },
    )
    svg(p.LAUF / "02_woerter_abstaende.csv", p.LAUF / "abstand_woerter.svg")
    print("Tor offen:" if tor else "Tor geschlossen:", "; ".join(gruende) if gruende else "die Eichung trennt")


if __name__ == "__main__":
    main()
