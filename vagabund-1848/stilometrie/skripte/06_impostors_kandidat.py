# -*- coding: utf-8 -*-
"""Prüft den Kandidaten mit der Impostors-Methode.

Liest teilung.json, eichung_tor.json und zum ersten Mal
corpus_diplomatisch/Kandidat_Vagabund.txt.
Die Merkmalräume stammen aus den Heine- und Hektor-Proben.
Die Schwelle stammt aus der Leave-one-out-Prüfung dieser Proben
und der Ablenker, nicht aus dem Kandidaten.

Reihenfolge der Zufallszahlen im Impostors-Strom:
Wörter, alle Klassen, alle Proben, Ziel Heine dann Hektor;
dann der Kandidat gegen Heine, dann gegen Hektor;
dieselbe Folge für Zeichen-4-Gramme;
dieselbe Folge für die Interpunktion, die nicht entscheidet.

Schreibt 06_impostors.json, 06_impostors_loo.csv und ENTSCHEIDUNG.md.
Ist das Eich-Tor geschlossen, werden die Anteile trotzdem berechnet
und in der Entscheidung nicht als Zuschreibung gelesen.
"""

import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g

ZIELE = ["heine", "hektor"]


def mittel(matrix, ohne=None):
    if ohne is None:
        return matrix.mean(axis=0)
    return np.delete(matrix, ohne, axis=0).mean(axis=0)


def anteil(dokument, ziel, herkunft, index, vektoren, rng):
    zielvektor = mittel(vektoren[ziel], index if herkunft == ziel else None)
    ablenker = []
    for klasse, matrix in vektoren.items():
        if klasse == ziel:
            continue
        if herkunft == klasse:
            if len(matrix) < 2:
                continue
            ablenker.append(mittel(matrix, index))
        else:
            ablenker.append(mittel(matrix))
    return g.impostor_anteil(dokument, zielvektor, np.vstack(ablenker), rng)


def leave_one_out(vektoren, rng, klassen):
    zeilen = []
    for herkunft in klassen:
        for index in range(len(vektoren[herkunft])):
            dokument = vektoren[herkunft][index]
            for ziel in ZIELE:
                zeilen.append(
                    {
                        "herkunft": herkunft,
                        "index": index,
                        "ziel": ziel,
                        "anteil": anteil(dokument, ziel, herkunft, index, vektoren, rng),
                    }
                )
    return zeilen


def schwelle_aus(zeilen):
    positiv = [zeile["anteil"] for zeile in zeilen if zeile["herkunft"] == zeile["ziel"]]
    negativ = [zeile["anteil"] for zeile in zeilen if zeile["herkunft"] != zeile["ziel"]]
    schwelle, index = g.youden_schwelle(positiv, negativ)
    return schwelle, index, positiv, negativ


def urteil(anteil_heine, anteil_hektor, schwelle):
    heine = g.lage(anteil_heine, schwelle)
    hektor = g.lage(anteil_hektor, schwelle)
    if heine == "darueber" and hektor == "darunter":
        return "heine", heine, hektor
    if hektor == "darueber" and heine == "darunter":
        return "hektor", heine, hektor
    if heine == "darueber" and hektor == "darueber":
        return "beide", heine, hektor
    if heine == "darunter" and hektor == "darunter":
        return "keiner", heine, hektor
    return "unbeantwortet", heine, hektor


def gesamt(tor, youden_woerter, youden_zeichen, urteil_woerter, urteil_zeichen, liedton):
    if not tor:
        return (
            "unentschieden",
            "Die Eichung trennt Heine und Hektor bei der Länge des Kandidaten nicht. "
            "Die Impostors-Anteile sind berechnet und werden nicht als Zuschreibung gelesen.",
        )
    if youden_woerter < p.YOUDEN_MINIMUM or youden_zeichen < p.YOUDEN_MINIMUM:
        return (
            "unentschieden",
            "Die Impostors-Prüfung trennt an den bekannten Proben nicht stark genug, "
            "um den Kandidaten zuzuschreiben.",
        )
    if urteil_woerter == "heine" and urteil_zeichen == "heine":
        return (
            "heine-nah",
            "Wörter und Zeichengramme liegen über der Schwelle für Heine und unter der für Hektor.",
        )
    if urteil_woerter == "hektor" and urteil_zeichen == "hektor":
        return (
            "hektor-nah",
            "Wörter und Zeichengramme liegen über der Schwelle für Hektor und unter der für Heine.",
        )
    if urteil_woerter == "keiner" and urteil_zeichen == "keiner" and liedton:
        return (
            "nur-liedton",
            "Weder Heine noch Hektor erreichen die Schwelle, und der Kandidat liegt "
            "im Cosine Delta der Wörter näher an einem Ablenker als an beiden.",
        )
    benannt = {urteil_woerter, urteil_zeichen} & {"heine", "hektor", "beide"}
    if "beide" in (urteil_woerter, urteil_zeichen) or benannt == {"heine", "hektor"}:
        return (
            "gemischt",
            "Die beiden Merkmalgruppen nennen nicht denselben Verfasser, oder beide Schwellen werden überschritten.",
        )
    return (
        "unentschieden",
        "Die Anteile liegen im Band um die Schwelle oder die Merkmalgruppen bleiben ohne gemeinsames Urteil.",
    )


def abstaende_zum_kandidaten(eichrelativ, profile, kandidat):
    mittel = eichrelativ.mean(axis=0)
    streuung = eichrelativ.std(axis=0, ddof=p.STANDARDABWEICHUNG_DDOF)
    behalten = streuung > 0
    def normiert(matrix):
        return (matrix[:, behalten] - mittel[behalten]) / streuung[behalten]
    zeilen = normiert(np.vstack(profile + [kandidat]))
    ziel = zeilen[-1]
    abstaende = []
    for zeile in zeilen[:-1]:
        nenner = np.linalg.norm(zeile) * np.linalg.norm(ziel)
        if nenner == 0:
            raise SystemExit("Kosinusabstand zum Profil ist nicht bestimmt")
        abstaende.append(float(1.0 - np.dot(zeile, ziel) / nenner))
    return abstaende


def main():
    teilung = g.lese_json(p.LAUF / "teilung.json")
    tor = g.lese_json(p.LAUF / "eichung_tor.json")
    proben = g.proben_primaer(teilung)
    klassen = ["heine", "hektor"] + list(teilung["primaer"]["ablenker"])
    for name in klassen:
        if name not in proben or len(proben[name]) < 2:
            raise SystemExit("Zu wenige Proben für " + name)
    eintrag = g.eintraege("kandidat")
    if len(eintrag) != 1:
        raise SystemExit("Die Dateiliste hat nicht genau einen Kandidaten")
    kandidat_woerter = g.lade_text(eintrag[0])
    if len(kandidat_woerter) != p.PROBENLAENGE:
        raise SystemExit("Der Kandidat hat nicht die festgelegte Probenlänge")
    _, rng, _ = g.generatoren()

    eichproben = proben["heine"] + proben["hektor"]
    merkmale_w = g.merkmal_woerter(eichproben, p.MFW)
    vektoren_w = {name: g.matrix_woerter(proben[name], merkmale_w) for name in klassen}
    loo_w = leave_one_out(vektoren_w, rng, klassen)
    schwelle_w, youden_w, _, _ = schwelle_aus(loo_w)
    kandidat_w = g.matrix_woerter([kandidat_woerter], merkmale_w)[0]
    anteil_w = {ziel: anteil(kandidat_w, ziel, None, None, vektoren_w, rng) for ziel in ZIELE}
    namen = ZIELE + [name for name in klassen if name not in ZIELE]
    distanz_w = abstaende_zum_kandidaten(
        np.vstack([vektoren_w["heine"], vektoren_w["hektor"]]),
        [vektoren_w[name].mean(axis=0) for name in namen],
        kandidat_w,
    )

    merkmale_z = g.merkmal_ngramme(eichproben, p.ZEICHEN_N, p.ZEICHEN_HAEUFIGSTE)
    vektoren_z = {
        name: g.matrix_ngramme(proben[name], merkmale_z, p.ZEICHEN_N) for name in klassen
    }
    loo_z = leave_one_out(vektoren_z, rng, klassen)
    schwelle_z, youden_z, _, _ = schwelle_aus(loo_z)
    kandidat_z = g.matrix_ngramme([kandidat_woerter], merkmale_z, p.ZEICHEN_N)[0]
    anteil_z = {ziel: anteil(kandidat_z, ziel, None, None, vektoren_z, rng) for ziel in ZIELE}

    namen_i = g.interpunktion_namen()
    vektoren_i = {}
    for name in klassen:
        matrix, _ = g.matrix_interpunktion(proben[name])
        vektoren_i[name] = matrix
    loo_i = leave_one_out(vektoren_i, rng, klassen)
    schwelle_i, youden_i, _, _ = schwelle_aus(loo_i)
    kandidat_i, _ = g.matrix_interpunktion([kandidat_woerter])
    anteil_i = {ziel: anteil(kandidat_i[0], ziel, None, None, vektoren_i, rng) for ziel in ZIELE}

    urteil_w, lage_wh, lage_wk = urteil(anteil_w["heine"], anteil_w["hektor"], schwelle_w)
    urteil_z, lage_zh, lage_zk = urteil(anteil_z["heine"], anteil_z["hektor"], schwelle_z)
    distanz = dict(zip(namen, distanz_w))
    naechster_ablenker = min(distanz[name] for name in namen if name not in ZIELE)
    liedton = naechster_ablenker < distanz["heine"] and naechster_ablenker < distanz["hektor"]
    ausgang, satz = gesamt(
        tor["tor_offen"], youden_w, youden_z, urteil_w, urteil_z, liedton
    )

    with (p.LAUF / "06_impostors_loo.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["merkmal", "herkunft", "index", "ziel", "anteil"]
        )
        writer.writeheader()
        for merkmal, zeilen in (("woerter", loo_w), ("zeichen", loo_z), ("interpunktion", loo_i)):
            for zeile in zeilen:
                writer.writerow(
                    {
                        "merkmal": merkmal,
                        "herkunft": zeile["herkunft"],
                        "index": zeile["index"],
                        "ziel": zeile["ziel"],
                        "anteil": f"{zeile['anteil']:.10f}",
                    }
                )
    ergebnis = {
        "kandidat": eintrag[0]["pfad"],
        "sha256": g.pruefsumme(g.pfad_zu(eintrag[0])),
        "woerter": len(kandidat_woerter),
        "tor_offen": tor["tor_offen"],
        "woerter_schwelle": schwelle_w,
        "woerter_youden": youden_w,
        "woerter_anteil_heine": anteil_w["heine"],
        "woerter_anteil_hektor": anteil_w["hektor"],
        "woerter_urteil": urteil_w,
        "woerter_lage_heine": lage_wh,
        "woerter_lage_hektor": lage_wk,
        "zeichen_schwelle": schwelle_z,
        "zeichen_youden": youden_z,
        "zeichen_anteil_heine": anteil_z["heine"],
        "zeichen_anteil_hektor": anteil_z["hektor"],
        "zeichen_urteil": urteil_z,
        "zeichen_lage_heine": lage_zh,
        "zeichen_lage_hektor": lage_zk,
        "interpunktion_schwelle": schwelle_i,
        "interpunktion_youden": youden_i,
        "interpunktion_anteil_heine": anteil_i["heine"],
        "interpunktion_anteil_hektor": anteil_i["hektor"],
        "interpunktion_entscheidet": False,
        "cosine_delta_profile": distanz,
        "naechster_ablenker": naechster_ablenker,
        "liedton_cosinus": liedton,
        "ausgang": ausgang,
        "satz": satz,
    }
    g.schreibe_json(p.LAUF / "06_impostors.json", ergebnis)
    (p.LAUF / "ENTSCHEIDUNG.md").write_text(
        "\n".join(
            [
                "# Entscheidung der " + p.STUDIE_NAME,
                "",
                f"Ausgang: {ausgang}.",
                "",
                satz,
                "",
                f"Wörter, Schwelle {schwelle_w:.4f}, Youden {youden_w:.4f}: "
                f"Heine {anteil_w['heine']:.4f}, Hektor {anteil_w['hektor']:.4f}, Urteil {urteil_w}.",
                f"Zeichen-{p.ZEICHEN_N}-Gramme, Schwelle {schwelle_z:.4f}, Youden {youden_z:.4f}: "
                f"Heine {anteil_z['heine']:.4f}, Hektor {anteil_z['hektor']:.4f}, Urteil {urteil_z}.",
                f"Interpunktion wird mitgeteilt und entscheidet nicht: "
                f"Heine {anteil_i['heine']:.4f}, Hektor {anteil_i['hektor']:.4f}.",
                "",
                "Cosine Delta des Kandidaten zu den Profilen, Wörter, Standardwerte aus den Heine- und Hektor-Proben:",
                "",
            ]
            + [f"- {name}: {distanz[name]:.4f}" for name in namen]
            + ["", "Diese Datei ist vom Skript geschrieben, nicht von Hand geändert.", ""]
        ),
        encoding="utf-8",
    )
    print(ausgang)
    print(satz)


if __name__ == "__main__":
    main()
