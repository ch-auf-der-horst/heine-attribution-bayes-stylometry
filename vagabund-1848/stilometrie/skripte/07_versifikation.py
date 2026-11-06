# -*- coding: utf-8 -*-
"""Beschreibt Strophenform, orthographischen Reim und eine Kadenznäherung.

Liest corpus_diplomatisch/Kandidat_Vagabund.txt sowie die Heine-Dateien
und Hektor_Schilda.txt aus der Dateiliste. Die Beschreibung ist
orthographisch: der Reimkern ist der Wortausgang ab dem letzten Vokal,
mit den Ersetzungen ey→ei, th→t, ß→ss, ph→f. Eine weibliche Kadenz
wird angenommen, wenn das Schlusswort auf e, en, er, el, em oder es
endet. Silbengruppen sind Vokalgruppen, keine gesicherte Silbenzahl.
Das ist keine metrische Edition und kein Ersatz für eine Prüfung am Vers.

Für jede Kandidatenstrophe wird, soweit vorhanden, je eine Strophe
derselben Zeilenzahl aus dem frühen Heine und aus den Hektor-Liedern
gezogen. Der Zufallsstrom ist der dritte Strom des Seeds.

Schreibt 07_strophen_kandidat.csv und 07_strophen_vergleich.csv.
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g


def reimschema(strophe):
    kerne = [g.reimkern(zeile.split()[-1]) for zeile in strophe]
    buchstaben = {}
    zeiger = 0
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    schema = []
    for kern in kerne:
        if not kern or kerne.count(kern) < 2:
            schema.append("x")
            continue
        if kern not in buchstaben:
            buchstaben[kern] = alphabet[zeiger]
            zeiger += 1
        schema.append(buchstaben[kern])
    return "".join(schema)


def beschreibung(strophe):
    silben = [sum(g.silbengruppen(token) for token in zeile.split()) for zeile in strophe]
    weiblich = [g.kadenz_weiblich(zeile.split()[-1]) for zeile in strophe]
    return {
        "zeilen": len(strophe),
        "silbengruppen": "-".join(str(zahl) for zahl in silben),
        "reim": reimschema(strophe),
        "anteil_weibliche_kadenz": sum(weiblich) / len(strophe),
    }


def strophen_aus_rolle(rolle):
    gruppen = []
    for eintrag in g.eintraege(rolle):
        text = g.pfad_zu(eintrag).read_text(encoding="utf-8")
        for strophe in g.strophen(text):
            gruppen.append((eintrag["pfad"], strophe))
    return gruppen


def ziehe(vorrat, zeilen, rng, verbraucht):
    moeglich = [
        nummer
        for nummer, (_, strophe) in enumerate(vorrat)
        if len(strophe) == zeilen and nummer not in verbraucht
    ]
    if not moeglich:
        return None
    wahl = int(rng.choice(moeglich))
    verbraucht.add(wahl)
    return vorrat[wahl]


def main():
    eintrag = g.eintraege("kandidat")[0]
    text = g.pfad_zu(eintrag).read_text(encoding="utf-8")
    kandidat = g.strophen(text)
    heine = strophen_aus_rolle("heine")
    hektor = strophen_aus_rolle("hektor")
    _, _, rng = g.generatoren()
    verbraucht = {"heine": set(), "hektor": set()}

    with (p.LAUF / "07_strophen_kandidat.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["strophe", "zeilen", "silbengruppen", "reim", "anteil_weibliche_kadenz"],
        )
        writer.writeheader()
        for nummer, strophe in enumerate(kandidat, start=1):
            zeile = beschreibung(strophe)
            zeile["strophe"] = nummer
            zeile["anteil_weibliche_kadenz"] = f"{zeile['anteil_weibliche_kadenz']:.4f}"
            writer.writerow(zeile)

    with (p.LAUF / "07_strophen_vergleich.csv").open("w", encoding="utf-8", newline="") as handle:
        felder = [
            "kandidat_strophe",
            "zeilen",
            "kandidat_reim",
            "heine_datei",
            "heine_reim",
            "heine_silbengruppen",
            "hektor_datei",
            "hektor_reim",
            "hektor_silbengruppen",
        ]
        writer = csv.DictWriter(handle, fieldnames=felder)
        writer.writeheader()
        fehlend = {"heine": 0, "hektor": 0}
        for nummer, strophe in enumerate(kandidat, start=1):
            eigen = beschreibung(strophe)
            vergleich = {
                "kandidat_strophe": nummer,
                "zeilen": eigen["zeilen"],
                "kandidat_reim": eigen["reim"],
            }
            for rolle, vorrat in (("heine", heine), ("hektor", hektor)):
                gezogen = ziehe(vorrat, eigen["zeilen"], rng, verbraucht[rolle])
                if gezogen is None:
                    fehlend[rolle] += 1
                    vergleich[f"{rolle}_datei"] = ""
                    vergleich[f"{rolle}_reim"] = ""
                    vergleich[f"{rolle}_silbengruppen"] = ""
                else:
                    pfad, fremd = gezogen
                    fremd_beschreibung = beschreibung(fremd)
                    vergleich[f"{rolle}_datei"] = pfad
                    vergleich[f"{rolle}_reim"] = fremd_beschreibung["reim"]
                    vergleich[f"{rolle}_silbengruppen"] = fremd_beschreibung["silbengruppen"]
            writer.writerow(vergleich)
    print(f"Strophen des Kandidaten: {len(kandidat)}")
    print(f"Ohne Gegenstrophe: Heine {fehlend['heine']}, Hektor {fehlend['hektor']}")


if __name__ == "__main__":
    main()
