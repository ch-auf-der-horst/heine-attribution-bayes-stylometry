# -*- coding: utf-8 -*-
"""Abstände der frühen Heine-Texte untereinander.

Jede Probe liegt in genau einer Datei. Es wird nicht über eine Textgrenze
geschnitten und nichts aneinandergehängt. Der Kandidat wird nicht geöffnet.
Studie 1 bis 3 bleiben unverändert.

Zwei Längen. 548 Wörter sind die Länge des Kandidaten. Texte darunter
ergeben keine Probe und fehlen in dieser Tafel. 351 Wörter sind die Länge
der Biene, des kürzesten der sieben Texte; damit stehen alle sieben in
einer Tafel. Längere Texte liefern mehrere nicht überlappende Proben.
Der Abstand zweier Texte ist der mittlere Cosine Delta ihrer Proben.
Die Merkmale und die Standardwerte kommen nur aus diesen Proben.

Schreibt nach ergebnisse/heine_texte/.
"""

import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g

ORDNER = p.PROJEKT / "ergebnisse" / "heine_texte"
NAMEN = {
    "Heine_Aurora.txt": "Aurora",
    "Heine_Biene.txt": "Biene",
    "Heine_Almanach.txt": "Almanach",
    "Heine_Agrippina.txt": "Agrippina",
    "Heine_Heimkehr.txt": "Heimkehr",
    "Heine_Kevlaar.txt": "Kevlaar",
    "Heine_DonnaClara.txt": "Donna Clara",
}


def reine_schnitte(woerter, laenge):
    return [woerter[start : start + laenge] for start in range(0, len(woerter) - laenge + 1, laenge)]


def texte_laden():
    geladen = []
    for eintrag in g.eintraege("heine"):
        woerter = g.lade_text(eintrag)
        name = NAMEN[Path(eintrag["pfad"]).name]
        geladen.append({"name": name, "pfad": eintrag["pfad"], "woerter": woerter})
    return geladen


def abstand_woerter(proben):
    merkmale = g.merkmal_woerter(proben, p.MFW)
    relativ = g.matrix_woerter(proben, merkmale)
    abstand, _ = g.kosinus_delta(relativ)
    return abstand


def abstand_zeichen(proben):
    merkmale = g.merkmal_ngramme(proben, p.ZEICHEN_N, p.ZEICHEN_HAEUFIGSTE)
    relativ = g.matrix_ngramme(proben, merkmale, p.ZEICHEN_N)
    abstand, _ = g.kosinus_delta(relativ)
    return abstand


def mittel_zwischen(abstand, von, nach):
    werte = [abstand[i, j] for i in von for j in nach if i < j or von is not nach]
    if von is nach:
        werte = [abstand[i, j] for i in von for j in nach if i < j]
    return float(np.mean(werte)) if werte else None


def tafel(texte, laenge, abstand_von):
    bloecke = []
    for text in texte:
        schnitte = reine_schnitte(text["woerter"], laenge)
        bloecke.append({**text, "schnitte": schnitte, "rest": len(text["woerter"]) - laenge * len(schnitte)})
    verwendbar = [block for block in bloecke if block["schnitte"]]
    proben = [schnitt for block in verwendbar for schnitt in block["schnitte"]]
    abstand = abstand_von(proben)
    grenzen = []
    cursor = 0
    for block in verwendbar:
        grenzen.append(range(cursor, cursor + len(block["schnitte"])))
        cursor += len(block["schnitte"])
    namen = [block["name"] for block in verwendbar]
    matrix = []
    innerhalb = []
    for zeile, von in enumerate(grenzen):
        matrix.append([mittel_zwischen(abstand, von, nach) for nach in grenzen])
        innerhalb.append(mittel_zwischen(abstand, von, von))
    return {
        "laenge": laenge,
        "bloecke": bloecke,
        "namen": namen,
        "matrix": matrix,
        "innerhalb": innerhalb,
        "proben": [len(block["schnitte"]) for block in verwendbar],
    }


def schreibe_csv(pfad, tafel_daten):
    with pfad.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + tafel_daten["namen"] + ["innerhalb", "proben"])
        for name, zeile, innen, anzahl in zip(
            tafel_daten["namen"], tafel_daten["matrix"], tafel_daten["innerhalb"], tafel_daten["proben"]
        ):
            writer.writerow(
                [name]
                + ["" if wert is None else f"{wert:.4f}" for wert in zeile]
                + ["" if innen is None else f"{innen:.4f}", anzahl]
            )


def zelle(wert):
    if wert is None:
        return "—"
    return f"{wert:.3f}".replace(".", ",")


def markdown_tafel(tafel_daten):
    kopf = "| | " + " | ".join(tafel_daten["namen"]) + " | innerhalb |"
    trenn = "| --- | " + " | ".join("---:" for _ in tafel_daten["namen"]) + " | ---: |"
    zeilen = [kopf, trenn]
    for name, zeile, innen in zip(tafel_daten["namen"], tafel_daten["matrix"], tafel_daten["innerhalb"]):
        zeilen.append("| " + name + " | " + " | ".join(zelle(wert) for wert in zeile) + " | " + zelle(innen) + " |")
    return "\n".join(zeilen)


def svg_waerme(pfad, tafel_daten, titel):
    namen = tafel_daten["namen"]
    n = len(namen)
    kante = 78
    rand_links = 110
    rand_oben = 78
    breite = rand_links + n * kante + 24
    hoehe = rand_oben + n * kante + 36
    werte = [wert for zeile in tafel_daten["matrix"] for wert in zeile if wert is not None and wert > 0]
    oben = max(werte) if werte else 1
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}" viewBox="0 0 {breite} {hoehe}">',
        '<rect width="100%" height="100%" fill="#f7f4ee"/>',
        f'<text x="{rand_links}" y="28" font-family="Palatino, Georgia, serif" font-size="16">{titel}</text>',
    ]
    for spalte, name in enumerate(namen):
        teile.append(
            f'<text x="{rand_links + spalte * kante + kante / 2}" y="58" text-anchor="middle" '
            f'font-family="Palatino, Georgia, serif" font-size="11">{name}</text>'
        )
    for zeile, name in enumerate(namen):
        teile.append(
            f'<text x="{rand_links - 8}" y="{rand_oben + zeile * kante + kante / 2 + 4}" text-anchor="end" '
            f'font-family="Palatino, Georgia, serif" font-size="11">{name}</text>'
        )
        for spalte, wert in enumerate(tafel_daten["matrix"][zeile]):
            x = rand_links + spalte * kante
            y = rand_oben + zeile * kante
            if wert is None or wert == 0:
                farbe = "#e6e0d4"
                schrift = ""
            else:
                anteil = min(wert / oben, 1)
                rot = int(90 + 140 * anteil)
                gruen = int(110 - 50 * anteil)
                blau = int(90 - 40 * anteil)
                farbe = f"#{rot:02x}{gruen:02x}{blau:02x}"
                schrift = (
                    f'<text x="{x + kante / 2}" y="{y + kante / 2 + 4}" text-anchor="middle" '
                    f'font-family="Palatino, Georgia, serif" font-size="12" fill="#1c1915">{zelle(wert)}</text>'
                )
            teile.append(f'<rect x="{x + 2}" y="{y + 2}" width="{kante - 4}" height="{kante - 4}" fill="{farbe}"/>')
            teile.append(schrift)
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")


def bestand(tafel_daten):
    zeilen = []
    for block in tafel_daten["bloecke"]:
        anzahl = len(block["schnitte"])
        wort = "Probe" if anzahl == 1 else "Proben"
        zeilen.append(
            f"- {block['name']}: {len(block['woerter'])} Wörter, "
            f"{anzahl} {wort}, {block['rest']} Wörter nicht verwendet"
        )
    return "\n".join(zeilen)


def main():
    if os_studie():
        raise SystemExit("Diese Vorprüfung liest Studie 1 als Dateiliste. AUTOR_STUDIE muss 1 oder ungesetzt sein.")
    texte = texte_laden()
    if [text["name"] for text in texte] != list(NAMEN.values()):
        raise SystemExit("Die Reihenfolge der Heine-Dateien hat sich geändert")
    ORDNER.mkdir(parents=True, exist_ok=True)
    woerter_548 = tafel(texte, p.PROBENLAENGE, abstand_woerter)
    zeichen_548 = tafel(texte, p.PROBENLAENGE, abstand_zeichen)
    woerter_351 = tafel(texte, 351, abstand_woerter)
    zeichen_351 = tafel(texte, 351, abstand_zeichen)
    schreibe_csv(ORDNER / "548_woerter.csv", woerter_548)
    schreibe_csv(ORDNER / "548_zeichen.csv", zeichen_548)
    schreibe_csv(ORDNER / "351_woerter.csv", woerter_351)
    schreibe_csv(ORDNER / "351_zeichen.csv", zeichen_351)
    svg_waerme(ORDNER / "548_woerter.svg", woerter_548, "Cosine Delta, 548 Wörter, häufigste Wörter")
    svg_waerme(ORDNER / "351_woerter.svg", woerter_351, "Cosine Delta, 351 Wörter, häufigste Wörter")
    text = "\n".join(
        [
            "# Abstände der frühen Heine-Texte",
            "",
            "Keine Probe überschreitet eine Textgrenze. Der Kandidat ist nicht eingegangen. Studie 1 bis 3 sind nicht neu gerechnet.",
            "",
            "Cosine Delta auf den 150 häufigsten Wörtern und, daneben, auf den 500 häufigsten Vierergruppen aus Buchstaben. Die Standardwerte kommen aus den Proben derselben Tafel.",
            "",
            "## 548 Wörter",
            "",
            "Das ist die Länge des Kandidaten. Biene, Kevlaar und Donna Clara bleiben darunter und fehlen in der Tafel.",
            "",
            bestand(woerter_548),
            "",
            "Häufigste Wörter. Die Spalte „innerhalb“ ist der mittlere Abstand der Proben desselben Textes. Sie ist nur bei der Heimkehr besetzt, weil nur sie mehrere Proben dieser Länge trägt.",
            "",
            markdown_tafel(woerter_548),
            "",
            "Vierergruppen aus Buchstaben:",
            "",
            markdown_tafel(zeichen_548),
            "",
            "## 351 Wörter",
            "",
            "Das ist die Länge der Biene. Alle sieben Texte haben mindestens eine Probe. Bei den längeren Texten ist der Abstand der Mittelwert über ihre Proben.",
            "",
            bestand(woerter_351),
            "",
            "Häufigste Wörter:",
            "",
            markdown_tafel(woerter_351),
            "",
            "Vierergruppen aus Buchstaben:",
            "",
            markdown_tafel(zeichen_351),
            "",
            "Die Zahlen dieser Tafeln stehen auf einer eigenen Skala. Sie sind nicht die Profilabstände aus Studie 1 bis 3.",
            "",
        ]
    )
    (ORDNER / "ABSTAENDE.md").write_text(text, encoding="utf-8")
    print(markdown_tafel(woerter_548))
    print("---")
    print(markdown_tafel(woerter_351))


def os_studie():
    import os

    wert = os.environ.get("AUTOR_STUDIE", "1")
    return wert not in {"1", ""}


if __name__ == "__main__":
    main()
