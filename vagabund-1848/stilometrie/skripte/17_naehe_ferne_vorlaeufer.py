# -*- coding: utf-8 -*-
"""Nähe oder Ferne mit Uhland und dem Wunderhorn neben den übrigen Vergleichstexten.

Dieselbe Regel wie in analyse/15_naehe_ferne.py. Uhlands Lieder und das
Wunderhorn kommen zu Schilda, den Vagabunden-Liedern, Müller und Steinmann
hinzu. Sie stehen nicht auf der Seite Heines. Die Leseregel steht in
analyse/PROTOKOLL_NAEHE_FERNE_VORLAEUFER.md. Der frühere Lauf bleibt
unverändert.

Aufruf vom Projektordner aus:

    python3 analyse/17_naehe_ferne_vorlaeufer.py
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

ORDNER = p.PROJEKT / "ergebnisse" / "naehe_ferne_vorlaeufer"
SEED = [20261013, 12]
VERGLEICH = (
    ("Hektor_Schilda.txt", "Schilda", 7396),
    ("Hektor_Vagabund.txt", "Vagabund", 2143),
    ("Mueller_1.txt", "Müller", 11279),
    ("Steinmann_Lieder.txt", "Steinmann", 492),
    ("Uhland_Lieder.txt", "Uhland", 5985),
    ("Wunderhorn_1806.txt", "Wunderhorn", 53339),
)
SATZ = "Schilda, die Vagabunden-Lieder, Müller, Steinmann, Uhland und das Wunderhorn"


def ausgangssatz(ergebnis):
    if ergebnis == "heine-nah":
        return (
            "Ausgang: heine-nah. Auf beiden Maßen liegt in mindestens der Hälfte der Ziehungen "
            "eine Heine-Probe näher als Schilda, die Vagabunden-Lieder, Müller, Steinmann, Uhland und das Wunderhorn."
        )
    if ergebnis == "heine-fern":
        return (
            "Ausgang: heine-fern. Auf beiden Maßen liegt in mindestens der Hälfte der Ziehungen "
            "einer von Schilda, den Vagabunden-Liedern, Müller, Steinmann, Uhland und dem Wunderhorn jeder Heine-Probe näher."
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
    bericht = "\n".join(
        [
            "# Nähe oder Ferne mit Uhland und dem Wunderhorn",
            "",
            "Dieser Lauf ersetzt die Prüfung ohne Uhland und ohne das Wunderhorn nicht. Beide stehen auf der Seite der Vergleichstexte, nicht auf der Seite Heines.",
            "",
            ausgangssatz(ergebnis),
            "",
            "Entschieden haben die ersten 351 Wörter des Kandidaten. Eine Heine-Probe muss näher liegen als Schilda, als die Vagabunden-Lieder, als Müller, als Steinmann, als Uhland und als das Wunderhorn. Das muss auf beiden Maßen in mindestens der Hälfte der 500 Ziehungen gelten.",
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
            "## Aufgenommene Texte",
            "",
            "Aufgenommen sind dreizehn bekannte Texte und der Kandidat. Jeder bekannte Text bleibt eine eigene Datei. Eine Probe überschreitet keine Grenze zwischen zwei Dateien. Die Merkmale und die Standardwerte kommen nur aus den dreizehn bekannten Texten. Der Kandidat wählt sie nicht mit.",
            "",
            "Die sieben frühen strophischen Heine-Lieder sind dieselben wie in der vorigen Prüfung: Aurora, Biene, Musenalmanach, Agrippina, Heimkehr, Kevlaar und Donna Clara.",
            "",
            "Die Vergleichstexte sind Schilda (`Hektor_Schilda.txt`, die strophischen Lieder, nicht die Knittelverse), die Vagabunden-Lieder I bis XVIII (`Hektor_Vagabund.txt`), Müller Teil 1 (`Mueller_1.txt`), Steinmanns Strophenlieder (`Steinmann_Lieder.txt`, ohne Sonette, ohne Parodie, ohne Wandelnde Blumen und ohne Hofgarten), Uhlands Lieder von 1815 (`Uhland_Lieder.txt`, ohne die Balladen) und das Wunderhorn von 1806 (`Wunderhorn_1806.txt`). Das Wunderhorn ist die anonyme Liedsammlung und kein Verfasserprofil Arnims oder Brentanos.",
            "",
            f"Der Kandidat ist `Kandidat_Vagabund.txt`, {len(kandidat['woerter'])} Wörter. Entschieden wird mit den ersten {n.LAENGE}.",
            "",
            "Nicht aufgenommen sind die Knittelverse, die Introduktion, die Ballade XXI, der Block um XXXV, die Gedichte LXX bis LXXVII, der Ganztext von Schilda, Uhlands Balladen, *Götterdämmerung*, *Ratcliff*, die Juniuslieder, Nordsee, das *Buch der Lieder* von 1827, Steinmanns Sonette, Müller Teil 2, die Teilabschriften des Kandidaten und die Dateien mit der Endung `_ber`.",
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
