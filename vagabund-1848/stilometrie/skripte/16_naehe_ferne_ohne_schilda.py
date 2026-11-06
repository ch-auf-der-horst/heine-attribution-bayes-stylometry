# -*- coding: utf-8 -*-
"""Nähe oder Ferne ohne die strophischen Schilda-Lieder.

Dieselbe Regel wie in analyse/15_naehe_ferne.py. Schilda fehlt in der
Ziehung, in den Merkmalen und in den Standardwerten. Die Knittelverse
waren dort schon nicht enthalten. Die Leseregel steht in
analyse/PROTOKOLL_NAEHE_FERNE_OHNE_SCHILDA.md. Der Lauf mit Schilda
bleibt unverändert.

Aufruf vom Projektordner aus:

    python3 analyse/16_naehe_ferne_ohne_schilda.py
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

ORDNER = p.PROJEKT / "ergebnisse" / "naehe_ferne_ohne_schilda"
SEED = [20261013, 11]
VERGLEICH = (
    ("Hektor_Vagabund.txt", "Vagabund", 2143),
    ("Mueller_1.txt", "Müller", 11279),
    ("Steinmann_Lieder.txt", "Steinmann", 492),
)
SATZ = "die Vagabunden-Lieder, Müller und Steinmann"


def ausgangssatz(ergebnis):
    if ergebnis == "heine-nah":
        return (
            "Ausgang: heine-nah. Auf beiden Maßen liegt in mindestens der Hälfte der Ziehungen "
            "eine Heine-Probe näher als die Vagabunden-Lieder, Müller und Steinmann."
        )
    if ergebnis == "heine-fern":
        return (
            "Ausgang: heine-fern. Auf beiden Maßen liegt in mindestens der Hälfte der Ziehungen "
            "einer von den Vagabunden-Liedern, Müller und Steinmann jeder Heine-Probe näher."
        )
    return (
        "Ausgang: unentschieden. Die beiden Maße erreichen nicht gemeinsam die Hälfte "
        "für Nähe und nicht gemeinsam die Hälfte für Ferne."
    )


def main():
    if ORDNER.exists() and os.environ.get("AUTOR_NEUZEICHNEN") != "1":
        raise SystemExit("Der Ordner besteht schon und wird nicht überschrieben: " + str(ORDNER))
    ORDNER.mkdir(parents=True, exist_ok=True)
    n.ORDNER = ORDNER

    bekannt = [n.laden(*eintrag) for eintrag in n.HEINE + VERGLEICH]
    kandidat = n.laden(*n.KANDIDAT)
    namen = [text["name"] for text in bekannt]
    heine_index = [namen.index(name) for _, name, _ in n.HEINE]
    vergleich_index = [namen.index(name) for _, name, _ in VERGLEICH]
    anfang = kandidat["woerter"][: n.LAENGE]
    ende = kandidat["woerter"][-n.LAENGE :]
    ueberlappung = len(
        set(range(n.LAENGE)) & set(range(len(kandidat["woerter"]) - n.LAENGE, len(kandidat["woerter"])))
    )

    rng = np.random.default_rng(np.random.SeedSequence(SEED))
    zeilen = []
    for nummer in range(1, n.WIEDERHOLUNGEN + 1):
        gezogen = []
        for text in bekannt:
            if len(text["schnitte"]) == 1:
                probe = text["schnitte"][0]
            else:
                probe = text["schnitte"][int(rng.integers(0, len(text["schnitte"])))]
            gezogen.append(probe)
        worte = g.merkmal_woerter(gezogen, 300)[: p.MFW]
        zeichen = g.merkmal_ngramme(gezogen, 4, p.ZEICHEN_HAEUFIGSTE)
        for art, merkmale, gramme, mass in (
            ("woerter", worte, None, "Wörter 150"),
            ("zeichen", zeichen, 4, "Zeichen 4"),
        ):
            basis = n.matrix_fuer(gezogen, merkmale, art, gramme)
            for fenster, probe in (("Anfang", anfang), ("Ende", ende)):
                zeile = np.vstack([basis, n.matrix_fuer([probe], merkmale, art, gramme)])
                abstand = n.abb.kosinus(zeile, basis)
                if abstand is None:
                    raise SystemExit("Abstand ist nicht bestimmt")
                stufe, heine, vergleich, i_heine, i_vergleich = n.urteil(
                    abstand[-1, :-1], heine_index, vergleich_index
                )
                zeilen.append(
                    {
                        "ziehung": nummer,
                        "fenster": fenster,
                        "mass": mass,
                        "stufe": stufe,
                        "abstand_heine": f"{heine:.6f}",
                        "abstand_vergleich": f"{vergleich:.6f}",
                        "naechster_heine": namen[i_heine],
                        "naechster_vergleich": namen[i_vergleich],
                    }
                )

    with (ORDNER / "ziehungen.csv").open("w", encoding="utf-8", newline="") as datei:
        schreiber = csv.DictWriter(datei, fieldnames=list(zeilen[0]))
        schreiber.writeheader()
        schreiber.writerows(zeilen)

    def sammeln(fenster):
        nach_mass = {mass: [] for mass in n.MASSE}
        heine_nah = {mass: Counter() for mass in n.MASSE}
        vergleich_nah = {mass: Counter() for mass in n.MASSE}
        abstand_heine = {mass: [] for mass in n.MASSE}
        abstand_vergleich = {mass: [] for mass in n.MASSE}
        for zeile in zeilen:
            if zeile["fenster"] != fenster:
                continue
            mass = zeile["mass"]
            nach_mass[mass].append(zeile["stufe"])
            heine_nah[mass][zeile["naechster_heine"]] += 1
            vergleich_nah[mass][zeile["naechster_vergleich"]] += 1
            abstand_heine[mass].append(float(zeile["abstand_heine"]))
            abstand_vergleich[mass].append(float(zeile["abstand_vergleich"]))
        return nach_mass, heine_nah, vergleich_nah, abstand_heine, abstand_vergleich

    anfang_pack = sammeln("Anfang")
    ende_pack = sammeln("Ende")
    ergebnis = n.ausgang(anfang_pack[0])
    ergebnis_ende = n.ausgang(ende_pack[0])

    def tabelle(pack):
        nach_mass, heine_nah, vergleich_nah, abstand_heine, abstand_vergleich = pack
        koerper = [
            "| Maß | näher an Heine | ferner | gleich | Median Heine | Median Vergleich |",
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
                "Nächster Heine-Text, "
                + mass
                + ": "
                + n.haeufig([name for _, name, _ in n.HEINE], heine_nah[mass])
                + "."
            )
            texte.append(
                "Nächster Vergleichstext, "
                + mass
                + ": "
                + n.haeufig([name for _, name, _ in VERGLEICH], vergleich_nah[mass])
                + "."
            )
        return koerper, texte

    tabelle_anfang, texte_anfang = tabelle(anfang_pack)
    tabelle_ende, texte_ende = tabelle(ende_pack)
    proben = "\n".join(
        f"- {text['name']}: {len(text['schnitte'])} {'Probe' if len(text['schnitte']) == 1 else 'Proben'}"
        for text in bekannt
    )
    bericht = "\n".join(
        [
            "# Nähe oder Ferne ohne Schilda",
            "",
            "Dieser Lauf ersetzt die Prüfung mit Schilda nicht. Schilda fehlt in Ziehung, Merkmalen und Standardwerten. Die Knittelverse waren schon zuvor nicht enthalten.",
            "",
            ausgangssatz(ergebnis),
            "",
            "Entschieden haben die ersten 351 Wörter des Kandidaten. Eine Heine-Probe muss näher liegen als die Vagabunden-Lieder, als Müller und als Steinmann. Das muss auf beiden Maßen in mindestens der Hälfte der 500 Ziehungen gelten.",
            "",
            "## Erste 351 Wörter",
            "",
            *tabelle_anfang,
            "",
            *texte_anfang,
            "",
            "Der häufigste Heine-Text und der Median des Abstands entscheiden nicht.",
            "",
            "## Letzte 351 Wörter",
            "",
            "Dieses Fenster entscheidet nicht. Es überlappt die ersten 351 Wörter in "
            f"{ueberlappung} Wörtern. Nach derselben Regel hieße der Ausgang {ergebnis_ende}.",
            "",
            *tabelle_ende,
            "",
            *texte_ende,
            "",
            "## Proben",
            "",
            proben,
            f"- Kandidat: {len(kandidat['woerter'])} Wörter, entschieden mit den ersten {n.LAENGE}",
            "",
            "Die Abbildungen stehen daneben und entscheiden nicht.",
            "",
        ]
    )
    (ORDNER / "BERICHT.md").write_text(bericht, encoding="utf-8")
    n.zeichnen(zeilen, vergleich=VERGLEICH, vergleich_satz=SATZ)
    print(ausgangssatz(ergebnis))
    print("Letzte 351, ohne Entscheidung:", ergebnis_ende)
    for zeile in tabelle_anfang:
        print(zeile)
    print("Geschrieben nach", ORDNER)


if __name__ == "__main__":
    main()
