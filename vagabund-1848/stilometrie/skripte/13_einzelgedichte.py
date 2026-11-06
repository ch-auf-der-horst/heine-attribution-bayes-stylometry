# -*- coding: utf-8 -*-
"""Einzelgedichte des Kandidaten gegen gleich lange Scheiben.

Jedes der zehn Gedichte bleibt ganz. Die römische Nummer zählt nicht mit.
Aus Heimkehr, den übrigen frühen Heine-Texten, Schilda und den
Vagabunden-Liedern werden Scheiben derselben Länge geschnitten. Der
Kandidat wählt keine Merkmale. Ein Gedicht fällt aus dem Block, wenn es
auf den 150 Wörtern und auf den Vierergruppen weiter vom Mittel der
anderen neun liegt als 95 Prozent der gleich langen Heimkehr-Scheiben
voneinander. Es liegt im Heimkehr-Bereich, wenn es dem Heimkehr-Profil
auf beiden Maßen höchstens so fern ist wie diese Scheiben. Das ist keine
Zuschreibung.

Aufruf vom Projektordner aus:

    AUTOR_STUDIE=5 python3 analyse/13_einzelgedichte.py

Schreibt nach ergebnisse/einzelgedichte/. Studie 1 bis 5 werden nicht
angefasst. Besteht der Ordner schon, bricht der Lauf ab.
"""

import csv
import os
import re
import sys
from pathlib import Path

if os.environ.get("AUTOR_STUDIE") != "5":
    raise SystemExit("Die Einzelgedichte verlangen AUTOR_STUDIE=5, sonst läge eine andere Dateiliste an.")

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from laufwahl import parameter as p
import gemeinsame as g

import importlib.util

_abb = importlib.util.spec_from_file_location(
    "abbildungen_einzel", Path(__file__).resolve().parent / "08_abbildungen.py"
)
abb = importlib.util.module_from_spec(_abb)
_abb.loader.exec_module(abb)

ORDNER = p.PROJEKT / "ergebnisse" / "einzelgedichte"
NUMMER = re.compile(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X)\.$")
HEINE = (
    ("Heine_Aurora.txt", "Aurora"),
    ("Heine_Biene.txt", "Biene"),
    ("Heine_Almanach.txt", "Almanach"),
    ("Heine_Agrippina.txt", "Agrippina"),
    ("Heine_Heimkehr.txt", "Heimkehr"),
    ("Heine_Kevlaar.txt", "Kevlaar"),
    ("Heine_DonnaClara.txt", "Donna Clara"),
)
HEKTOR = (
    ("Hektor_Schilda.txt", "Schilda"),
    ("Hektor_Vagabund.txt", "Vagabund"),
)
QUANTIL = 0.95


def scheiben(woerter, laenge):
    return [woerter[start : start + laenge] for start in range(0, len(woerter) - laenge + 1, laenge)]


def gedichte_lesen(pfad):
    namen = []
    puffern = []
    aktuell = None
    zeilen = []
    for roh in pfad.read_text(encoding="utf-8").splitlines():
        zeile = roh.strip()
        if NUMMER.fullmatch(zeile):
            if aktuell is not None:
                namen.append(aktuell)
                puffern.append(zeilen)
            aktuell = zeile[:-1]
            zeilen = []
        elif aktuell is not None:
            zeilen.append(roh)
    if aktuell is not None:
        namen.append(aktuell)
        puffern.append(zeilen)
    gedichte = []
    for name, block in zip(namen, puffern):
        woerter = g.leerzeichen_woerter("\n".join(block))
        gedichte.append({"name": name, "woerter": woerter, "laenge": len(woerter)})
    if [gedicht["name"] for gedicht in gedichte] != ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]:
        raise SystemExit("Die zehn Gedichte sind nicht I bis X")
    return gedichte


def referenzen():
    texte = []
    for rolle, erwartet in (("heine", HEINE), ("hektor", HEKTOR)):
        eintraege = g.eintraege(rolle)
        namen = [Path(eintrag["pfad"]).name for eintrag in eintraege]
        if namen != [datei for datei, _ in erwartet]:
            raise SystemExit(f"Die {rolle}-Dateien sind nicht die der Studie 5: {namen}")
        for eintrag, (_, name) in zip(eintraege, erwartet):
            texte.append({"name": name, "woerter": g.lade_text(eintrag)})
    return texte


def merkmale(bloecke, art, n=None, anzahl=None):
    proben = []
    for block in bloecke:
        proben.extend(block["scheiben"])
    if art == "woerter":
        return g.merkmal_woerter(proben, anzahl)
    return g.merkmal_ngramme(proben, n, anzahl)


def matrix(proben, art, merkmale_liste, n=None):
    if not proben:
        raise SystemExit("Keine Scheiben")
    if art == "woerter":
        return g.matrix_woerter(proben, merkmale_liste)
    return g.matrix_ngramme(proben, merkmale_liste, n)


def abstand(links, rechts, eichung):
    tafel = abb.kosinus(np.vstack([links, rechts]), eichung)
    if tafel is None:
        raise SystemExit("Kosinusabstand ist nicht bestimmt")
    return float(tafel[0, 1])


def quantil(werte):
    return float(np.quantile(np.array(werte, dtype=float), QUANTIL, method="linear"))


def leave_one_out(vektoren, eichung, ziel):
    anzahl = vektoren.shape[0]
    if anzahl < 3:
        raise SystemExit("Zu wenige Scheiben für den leave-one-out-Vergleich")
    summe = vektoren.sum(axis=0)
    abstaende = []
    for index in range(anzahl):
        centroid = (summe - vektoren[index]) / (anzahl - 1)
        abstaende.append(abstand(vektoren[index], centroid if ziel is None else ziel, eichung))
    return abstaende


def profile(bloecke, art, merkmale_liste, n=None):
    zeilen = []
    scheiben_je_text = {}
    for block in bloecke:
        vektoren = matrix(block["scheiben"], art, merkmale_liste, n)
        zeilen.append(vektoren.mean(axis=0))
        scheiben_je_text[block["name"]] = vektoren
    return np.vstack(zeilen), scheiben_je_text


def fmt(wert):
    return f"{wert:.4f}".replace(".", ",")


def rechne(gedichte, texte, art, merkmale_liste, n=None):
    ergebnisse = []
    cache = {}
    for gedicht in gedichte:
        laenge = gedicht["laenge"]
        if laenge not in cache:
            scheiben_bloecke = []
            for text in texte:
                stuecke = scheiben(text["woerter"], laenge)
                if len(stuecke) < 3:
                    raise SystemExit(f"{text['name']} hat bei {laenge} Wörtern zu wenige Scheiben")
                scheiben_bloecke.append({**text, "scheiben": stuecke})
            eichung, je_text = profile(scheiben_bloecke, art, merkmale_liste[laenge], n)
            namen = [block["name"] for block in scheiben_bloecke]
            heim = je_text["Heimkehr"]
            cache[laenge] = {
                "eichung": eichung,
                "heim_intern": leave_one_out(heim, eichung, None),
                "heim_profil": leave_one_out(heim, eichung, None),
                "profile": {name: eichung[namen.index(name)] for name in ("Heimkehr", "Schilda", "Vagabund")},
            }
        stand = cache[laenge]
        vektor = matrix([gedicht["woerter"]], art, merkmale_liste[laenge], n)[0]
        andere = [stück for stück in gedichte if stück["name"] != gedicht["name"]]
        centroid = matrix([stück["woerter"] for stück in andere], art, merkmale_liste[laenge], n).mean(axis=0)
        zum_block = abstand(vektor, centroid, stand["eichung"])
        zu_profil = {
            name: abstand(vektor, stand["profile"][name], stand["eichung"])
            for name in ("Heimkehr", "Schilda", "Vagabund")
        }
        ergebnisse.append(
            {
                "name": gedicht["name"],
                "laenge": laenge,
                "zum_block": zum_block,
                "block_quantil": quantil(stand["heim_intern"]),
                "zu_heimkehr": zu_profil["Heimkehr"],
                "zu_schilda": zu_profil["Schilda"],
                "zu_vagabund": zu_profil["Vagabund"],
                "profil_quantil": quantil(stand["heim_profil"]),
                "faellt_heraus": zum_block > quantil(stand["heim_intern"]),
                "im_bereich": zu_profil["Heimkehr"] <= quantil(stand["heim_profil"]),
            }
        )
    return ergebnisse


def merkmallisten(texte, laengen):
    listen = {}
    for laenge in laengen:
        bloecke = []
        for text in texte:
            bloecke.append({"scheiben": scheiben(text["woerter"], laenge)})
        listen[laenge] = {
            "woerter": {anzahl: merkmale(bloecke, "woerter", anzahl=anzahl) for anzahl in (150, 100, 300)},
            "zeichen": {n: merkmale(bloecke, "zeichen", n=n, anzahl=p.ZEICHEN_HAEUFIGSTE) for n in (4, 3, 5)},
        }
    return listen


def tabelle(zeilen):
    kopf = (
        "| Gedicht | Wörter | Abstand zu den anderen neun | Heimkehr-Quantil | fällt heraus | "
        "Abstand zu Heimkehr | Bereichsgrenze | im Heimkehr-Bereich | Schilda | Vagabund |"
    )
    trenn = "| --- | ---: | ---: | ---: | --- | ---: | ---: | --- | ---: | ---: |"
    koerper = [kopf, trenn]
    for zeile in zeilen:
        koerper.append(
            "| {name} | {laenge} | {zum_block} | {block_quantil} | {faellt_heraus} | "
            "{zu_heimkehr} | {profil_quantil} | {im_bereich} | {zu_schilda} | {zu_vagabund} |".format(
                name=zeile["name"],
                laenge=zeile["laenge"],
                zum_block=fmt(zeile["zum_block"]),
                block_quantil=fmt(zeile["block_quantil"]),
                faellt_heraus="ja" if zeile["faellt_heraus"] else "nein",
                zu_heimkehr=fmt(zeile["zu_heimkehr"]),
                profil_quantil=fmt(zeile["profil_quantil"]),
                im_bereich="ja" if zeile["im_bereich"] else "nein",
                zu_schilda=fmt(zeile["zu_schilda"]),
                zu_vagabund=fmt(zeile["zu_vagabund"]),
            )
        )
    return "\n".join(koerper)


def satz(primaer_wort, primaer_zeichen):
    beide_block = [
        links["name"]
        for links, rechts in zip(primaer_wort, primaer_zeichen)
        if links["faellt_heraus"] and rechts["faellt_heraus"]
    ]
    beide_bereich = [
        links["name"]
        for links, rechts in zip(primaer_wort, primaer_zeichen)
        if links["im_bereich"] and rechts["im_bereich"]
    ]
    if not beide_bereich:
        tragung = (
            "Kein Gedicht liegt auf beiden Maßen im Heimkehr-Bereich. "
            "Die Einzelprobe kann die Nähe des Blocks nicht auf wenige Gedichte zurückführen."
        )
    elif len(beide_bereich) <= 3:
        tragung = (
            "Im Heimkehr-Bereich beider Maße liegen höchstens drei Gedichte: "
            + ", ".join(beide_bereich)
            + ". Nach der Festlegung wird die Nähe des Blocks von wenigen Gedichten getragen. "
            "Das ist keine Zuschreibung."
        )
    else:
        tragung = (
            "Im Heimkehr-Bereich beider Maße liegen "
            + ", ".join(beide_bereich)
            + ". Die Nähe ist breit geteilt und wird nicht von wenigen Gedichten getragen."
        )
    if beide_block:
        ausreisser = " Auf beiden Maßen fallen aus dem Block: " + ", ".join(beide_block) + "."
    else:
        ausreisser = " Auf beiden Maßen fällt kein Gedicht aus dem Block."
    return tragung + ausreisser


def main():
    if ORDNER.exists() and os.environ.get("AUTOR_NEUZEICHNEN") != "1":
        raise SystemExit("Der Ordner besteht schon und wird nicht überschrieben: " + str(ORDNER))
    kandidat = g.eintraege("kandidat")
    if len(kandidat) != 1 or Path(kandidat[0]["pfad"]).name != "Kandidat_Vagabund.txt":
        raise SystemExit("Der Kandidat ist nicht Kandidat_Vagabund.txt")
    pfad = g.pfad_zu(kandidat[0])
    ganz = g.lade_text(kandidat[0])
    gedichte = gedichte_lesen(pfad)
    summe = sum(gedicht["laenge"] for gedicht in gedichte)
    if len(ganz) != 548 or summe + 10 != 548:
        raise SystemExit(f"Wortzahl der Gedichte stimmt nicht: {summe} plus zehn Nummern, Datei {len(ganz)}")
    texte = referenzen()
    laengen = sorted({gedicht["laenge"] for gedicht in gedichte})
    listen = merkmallisten(texte, laengen)
    wort_150 = rechne(gedichte, texte, "woerter", {laenge: listen[laenge]["woerter"][150] for laenge in laengen})
    zeichen_4 = rechne(gedichte, texte, "zeichen", {laenge: listen[laenge]["zeichen"][4] for laenge in laengen}, 4)
    bericht = {}
    for anzahl in (100, 300):
        bericht[f"Wörter {anzahl}"] = rechne(
            gedichte, texte, "woerter", {laenge: listen[laenge]["woerter"][anzahl] for laenge in laengen}
        )
    for n in (3, 5):
        bericht[f"Zeichen {n}"] = rechne(
            gedichte, texte, "zeichen", {laenge: listen[laenge]["zeichen"][n] for laenge in laengen}, n
        )
    ORDNER.mkdir(parents=True)
    with (ORDNER / "woerter150.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(wort_150[0].keys()))
        writer.writeheader()
        writer.writerows(wort_150)
    with (ORDNER / "zeichen4.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(zeichen_4[0].keys()))
        writer.writeheader()
        writer.writerows(zeichen_4)
    ergebnis = satz(wort_150, zeichen_4)
    text = "\n".join(
        [
            "# Einzelgedichte",
            "",
            "Die Gedichte sind ganz geblieben. Die Nähe des Blocks ist hier keine Zuschreibung. Studie 1 bis 5 sind nicht neu gerechnet.",
            "",
            ergebnis,
            "",
            "## 150 Wörter",
            "",
            tabelle(wort_150),
            "",
            "## Vierergruppen",
            "",
            tabelle(zeichen_4),
            "",
            "100 und 300 Wörter sowie Dreier- und Fünfergruppen entscheiden nicht. Ihre Abstände zum Heimkehr-Profil stehen in den folgenden Zeilen.",
            "",
        ]
    )
    for titel, zeilen in bericht.items():
        text += f"\n### {titel}\n\n"
        text += " | ".join(
            f"{zeile['name']} {fmt(zeile['zu_heimkehr'])}" for zeile in zeilen
        )
        text += "\n"
    (ORDNER / "EINZEL.md").write_text(text + "\n", encoding="utf-8")
    print(ergebnis)
    print("Geschrieben nach", ORDNER)


if __name__ == "__main__":
    main()
