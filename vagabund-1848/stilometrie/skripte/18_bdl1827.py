# -*- coding: utf-8 -*-
"""Nähe des Kandidaten zum Buch der Lieder 1827.

Heine ist diese eine Datei, nicht die sieben frühen Lieder. Müller und
das Wunderhorn, Schilda und die Vagabunden-Lieder sind die Vergleichstexte.
Steinmann ist die Fälschungsprobe und wählt keine Merkmale. Die Leseregel
steht in analyse/PROTOKOLL_BDL1827.md.

Aufruf vom Projektordner aus:

    python3 analyse/18_bdl1827.py
"""

import csv
import importlib.util
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

import gemeinsame as g
from laufwahl import parameter as p

_basis = importlib.util.spec_from_file_location(
    "naehe_ferne", Path(__file__).resolve().parent / "15_naehe_ferne.py"
)
n = importlib.util.module_from_spec(_basis)
_basis.loader.exec_module(n)

ORDNER = p.PROJEKT / "ergebnisse" / "bdl1827"
SEED = [20261013, 13]
BAND = ("Heine_Buch_der_Lieder_1827_restituiert.txt", "Buch der Lieder", 29215)
VERGLEICH = (
    ("Mueller_1.txt", "Müller", 11279),
    ("Wunderhorn_1806.txt", "Wunderhorn", 53339),
    ("Hektor_Schilda.txt", "Schilda", 7396),
    ("Hektor_Vagabund.txt", "Vagabund", 2143),
)
STEINMANN = ("Steinmann_Lieder.txt", "Steinmann", 492)
KANDIDAT = ("Kandidat_Vagabund.txt", "Kandidat", 548)
SATZ = "Müller, das Wunderhorn, Schilda, die Vagabunden-Lieder und Steinmann"
TEILE = (
    ("Traumbilder.", "Traumbilder"),
    ("Lieder.", "Lieder"),
    ("Romanzen.", "Romanzen"),
    ("Sonette.", "Sonette"),
    ("Die Heimkehr.", "Heimkehr"),
    ("Aus der Harzreise.", "Harzreise"),
    ("Die Nordsee.", "Nordsee"),
)


def band_laden():
    pfad = p.PROJEKT / "Heine" / BAND[0]
    text = pfad.read_text(encoding="utf-8")
    woerter = []
    grenzen = []
    erwartet = {zeile: name for zeile, name in TEILE}
    for zeile in text.splitlines():
        name = erwartet.get(zeile.strip())
        if name is not None:
            grenzen.append((len(woerter), name))
        woerter.extend(zeile.split())
    if len(woerter) != BAND[2]:
        raise SystemExit(f"{BAND[0]} hat {len(woerter)} Wörter, erwartet {BAND[2]}")
    if [name for _, name in grenzen] != [name for _, name in TEILE]:
        raise SystemExit("Die Teile des Bandes stehen nicht in der erwarteten Folge")
    schnitte = []
    herkunft = []
    for start in range(0, len(woerter) - n.LAENGE + 1, n.LAENGE):
        schnitte.append(woerter[start : start + n.LAENGE])
        teil = grenzen[0][1]
        for grenze, name in grenzen:
            if grenze <= start:
                teil = name
            else:
                break
        herkunft.append(teil)
    return {"name": BAND[1], "woerter": woerter, "schnitte": schnitte, "herkunft": herkunft}


def satz_zu(ergebnis, wer):
    if ergebnis == "heine-nah":
        return f"Ausgang für {wer}: heine-nah."
    if ergebnis == "heine-fern":
        return f"Ausgang für {wer}: heine-fern."
    return f"Ausgang für {wer}: unentschieden."


def main():
    if ORDNER.exists() and os.environ.get("AUTOR_NEUZEICHNEN") != "1":
        raise SystemExit("Der Ordner besteht schon und wird nicht überschrieben: " + str(ORDNER))
    ORDNER.mkdir(parents=True, exist_ok=True)
    n.ORDNER = ORDNER

    band = band_laden()
    vergleich = [n.laden(*eintrag) for eintrag in VERGLEICH]
    steinmann = n.laden(*STEINMANN)
    kandidat = n.laden(*KANDIDAT)
    namen = [band["name"]] + [text["name"] for text in vergleich]
    heine_index = [0]
    vergleich_kandidat = list(range(1, len(namen))) + [len(namen)]
    vergleich_steinmann = list(range(1, len(namen)))
    anfang = kandidat["woerter"][: n.LAENGE]
    ende = kandidat["woerter"][-n.LAENGE :]
    steinmann_probe = steinmann["schnitte"][0]
    ueberlappung = len(
        set(range(n.LAENGE)) & set(range(len(kandidat["woerter"]) - n.LAENGE, len(kandidat["woerter"])))
    )

    rng = np.random.default_rng(np.random.SeedSequence(SEED))
    zeilen = []
    teile_gezogen = Counter()
    for nummer in range(1, n.WIEDERHOLUNGEN + 1):
        gezogen = []
        herkunft = []
        for text in [band] + vergleich:
            if len(text["schnitte"]) == 1:
                index = 0
            else:
                index = int(rng.integers(0, len(text["schnitte"])))
            gezogen.append(text["schnitte"][index])
            herkunft.append(text["herkunft"][index] if "herkunft" in text else "")
        teile_gezogen[herkunft[0]] += 1
        worte = g.merkmal_woerter(gezogen, 300)[: p.MFW]
        zeichen = g.merkmal_ngramme(gezogen, 4, p.ZEICHEN_HAEUFIGSTE)
        for art, merkmale, gramme, mass in (
            ("woerter", worte, None, "Wörter 150"),
            ("zeichen", zeichen, 4, "Zeichen 4"),
        ):
            basis = n.matrix_fuer(gezogen, merkmale, art, gramme)
            zusatz = n.matrix_fuer([steinmann_probe, anfang, ende], merkmale, art, gramme)
            abstand = n.abb.kosinus(np.vstack([basis, zusatz]), basis)
            if abstand is None:
                raise SystemExit("Abstand ist nicht bestimmt")
            namen_plus = namen + ["Steinmann", "Kandidat Anfang", "Kandidat Ende"]
            for fenster, zeile_index in (("Anfang", len(namen) + 1), ("Ende", len(namen) + 2)):
                stufe, heine, andere, i_heine, i_andere = n.urteil(
                    abstand[zeile_index], heine_index, vergleich_kandidat
                )
                zeilen.append(
                    {
                        "ziehung": nummer,
                        "wer": "Kandidat",
                        "fenster": fenster,
                        "mass": mass,
                        "stufe": stufe,
                        "abstand_heine": f"{heine:.6f}",
                        "abstand_vergleich": f"{andere:.6f}",
                        "naechster_heine": namen_plus[i_heine],
                        "naechster_vergleich": namen_plus[i_andere],
                        "teil": herkunft[0],
                    }
                )
            stufe_s, heine_s, andere_s, _, i_andere_s = n.urteil(
                abstand[len(namen)], heine_index, vergleich_steinmann
            )
            zeilen.append(
                {
                    "ziehung": nummer,
                    "wer": "Steinmann",
                    "fenster": "Anfang",
                    "mass": mass,
                    "stufe": stufe_s,
                    "abstand_heine": f"{heine_s:.6f}",
                    "abstand_vergleich": f"{andere_s:.6f}",
                    "naechster_heine": BAND[1],
                    "naechster_vergleich": namen_plus[i_andere_s],
                    "teil": herkunft[0],
                }
            )

    with (ORDNER / "ziehungen.csv").open("w", encoding="utf-8", newline="") as datei:
        schreiber = csv.DictWriter(datei, fieldnames=list(zeilen[0]))
        schreiber.writeheader()
        schreiber.writerows(zeilen)

    def nur(wer, fenster):
        return [zeile for zeile in zeilen if zeile["wer"] == wer and zeile["fenster"] == fenster]

    def pack(auswahl):
        nach_mass = {mass: [] for mass in n.MASSE}
        vergleich_nah = {mass: Counter() for mass in n.MASSE}
        abstand_heine = {mass: [] for mass in n.MASSE}
        abstand_vergleich = {mass: [] for mass in n.MASSE}
        for zeile in auswahl:
            mass = zeile["mass"]
            nach_mass[mass].append(zeile["stufe"])
            vergleich_nah[mass][zeile["naechster_vergleich"]] += 1
            abstand_heine[mass].append(float(zeile["abstand_heine"]))
            abstand_vergleich[mass].append(float(zeile["abstand_vergleich"]))
        return nach_mass, vergleich_nah, abstand_heine, abstand_vergleich

    def tabelle(auswahl, namen_vergleich):
        nach_mass, vergleich_nah, abstand_heine, abstand_vergleich = pack(auswahl)
        koerper = [
            "| Maß | näher am Band | ferner | gleich | Median Band | Median Vergleich |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
        for mass in n.MASSE:
            koerper.append(
                f"| {mass} | {n.fmt(n.anteil(nach_mass[mass], 'nah'))} "
                f"| {n.fmt(n.anteil(nach_mass[mass], 'fern'))} "
                f"| {n.fmt(n.anteil(nach_mass[mass], 'gleich'))} "
                f"| {n.zahl(float(np.median(abstand_heine[mass])))} "
                f"| {n.zahl(float(np.median(abstand_vergleich[mass])))} |"
            )
        texte = []
        for mass in n.MASSE:
            texte.append(
                "Nächster Vergleichstext, "
                + mass
                + ": "
                + n.haeufig(namen_vergleich, vergleich_nah[mass])
                + "."
            )
        return koerper, texte, n.ausgang(nach_mass)

    kandidat_anfang = nur("Kandidat", "Anfang")
    tabelle_anfang, texte_anfang, ergebnis = tabelle(
        kandidat_anfang, [name for _, name, _ in VERGLEICH] + ["Steinmann"]
    )
    tabelle_ende, texte_ende, ergebnis_ende = tabelle(
        nur("Kandidat", "Ende"), [name for _, name, _ in VERGLEICH] + ["Steinmann"]
    )
    tabelle_stein, texte_stein, ergebnis_stein = tabelle(
        nur("Steinmann", "Anfang"), [name for _, name, _ in VERGLEICH]
    )
    teile_satz = ", ".join(
        f"{name} {n.fmt(teile_gezogen[name] / n.WIEDERHOLUNGEN)}" for _, name in TEILE
    )

    bericht = "\n".join(
        [
            "# Buch der Lieder 1827",
            "",
            "Heine ist hier eine Datei, das restituierte Buch der Lieder von 1827, nicht die sieben frühen Lieder. Dieser Lauf ersetzt die früheren Prüfungen nicht.",
            "",
            satz_zu(ergebnis, "den Kandidaten")
            + " Eine Probe des Bandes liegt auf beiden Maßen in mindestens der Hälfte der Ziehungen näher als Müller, das Wunderhorn, Schilda, die Vagabunden-Lieder und Steinmann."
            if ergebnis == "heine-nah"
            else satz_zu(ergebnis, "den Kandidaten")
            + " Die beiden Maße erreichen nicht gemeinsam die festgelegte Hälfte."
            if ergebnis == "unentschieden"
            else satz_zu(ergebnis, "den Kandidaten")
            + " Auf beiden Maßen liegt in mindestens der Hälfte der Ziehungen einer der fünf Vergleichstexte der Bandprobe näher.",
            "",
            "Entschieden haben die ersten 351 Wörter des Kandidaten. Steinmann wählt die Merkmale nicht und geht nicht in die Standardwerte ein.",
            "",
            "## Kandidat, erste 351 Wörter",
            "",
            *tabelle_anfang,
            "",
            *texte_anfang,
            "",
            "Welcher Vergleichstext der nächste ist und aus welchem Teil des Bandes die Probe stammt, entscheidet nicht.",
            "",
            "## Kandidat, letzte 351 Wörter",
            "",
            f"Dieses Fenster entscheidet nicht. Es überlappt die ersten 351 Wörter in {ueberlappung} Wörtern. "
            f"Nach derselben Regel hieße der Ausgang {ergebnis_ende}.",
            "",
            *tabelle_ende,
            "",
            *texte_ende,
            "",
            "## Steinmann als Fälschungsprobe",
            "",
            "Diese Probe entscheidet den Kandidaten nicht. Verglichen wird mit Müller, dem Wunderhorn, Schilda und den Vagabunden-Liedern. "
            + satz_zu(ergebnis_stein, "Steinmann"),
            "",
            *tabelle_stein,
            "",
            *texte_stein,
            "",
            "## Teile des Bandes",
            "",
            f"Die gezogene Probe des Bandes fiel auf die Wörter in diese Teile: {teile_satz}. Auf den Vierergruppen ist die Ziehung dieselbe.",
            "",
            f"Der Band hat {len(band['woerter'])} Wörter und {len(band['schnitte'])} Proben von 351 Wörtern. "
            f"Steinmann lässt {len(steinmann['woerter']) - n.LAENGE} Wörter liegen.",
            "",
            "Die Abbildungen stehen daneben und entscheiden nicht.",
            "",
        ]
    )
    (ORDNER / "BERICHT.md").write_text(bericht, encoding="utf-8")
    n.streuung(kandidat_anfang, SATZ)
    n.unterschied(kandidat_anfang)
    n.anteile(nur("Kandidat", "Anfang") + nur("Kandidat", "Ende"))
    n.naechste(
        kandidat_anfang,
        VERGLEICH + (STEINMANN,),
        "abb_naechster_vergleich.svg",
        "Welcher Vergleichstext der nächste ist",
        "Erste 351 Wörter des Kandidaten. Gezählt wird der nächste unter "
        + SATZ
        + ". Diese Häufigkeit entscheidet nicht.",
    )
    print(satz_zu(ergebnis, "den Kandidaten"))
    print(satz_zu(ergebnis_stein, "Steinmann"))
    print("Letzte 351, ohne Entscheidung:", ergebnis_ende)
    for zeile in tabelle_anfang:
        print(zeile)
    print(teile_satz)
    print("Geschrieben nach", ORDNER)


if __name__ == "__main__":
    main()
