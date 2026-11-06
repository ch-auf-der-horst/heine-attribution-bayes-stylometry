# -*- coding: utf-8 -*-
"""Nähe oder Ferne des Kandidaten zu den frühen Heine-Liedern.

Jeder bekannte Text gibt genau eine Probe von 351 Wörtern. Das wird
500-mal wiederholt. Entschieden wird, ob der Kandidat einer Heine-Probe
näher liegt als Schilda, den Vagabunden-Liedern, Müller und Steinmann.
Die Leseregel steht in analyse/PROTOKOLL_NAEHE_FERNE.md. Sie wird hier
nicht verändert. Studie 1 bis 6 und die Prüfung gleicher Proben bleiben
unangetastet.

Aufruf vom Projektordner aus:

    python3 analyse/15_naehe_ferne.py
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

_abb = importlib.util.spec_from_file_location(
    "abbildungen", Path(__file__).resolve().parent / "08_abbildungen.py"
)
abb = importlib.util.module_from_spec(_abb)
_abb.loader.exec_module(abb)

ORDNER = p.PROJEKT / "ergebnisse" / "naehe_ferne"
LAENGE = 351
WIEDERHOLUNGEN = 500
SEED = [20261013, 10]
HEINE = (
    ("Heine_Aurora.txt", "Aurora", 1089),
    ("Heine_Biene.txt", "Biene", 351),
    ("Heine_Almanach.txt", "Almanach", 617),
    ("Heine_Agrippina.txt", "Agrippina", 830),
    ("Heine_Heimkehr.txt", "Heimkehr", 2467),
    ("Heine_Kevlaar.txt", "Kevlaar", 397),
    ("Heine_DonnaClara.txt", "Donna Clara", 413),
)
VERGLEICH = (
    ("Hektor_Schilda.txt", "Schilda", 7396),
    ("Hektor_Vagabund.txt", "Vagabund", 2143),
    ("Mueller_1.txt", "Müller", 11279),
    ("Steinmann_Lieder.txt", "Steinmann", 492),
)
KANDIDAT = ("Kandidat_Vagabund.txt", "Kandidat", 548)
MASSE = ("Wörter 150", "Zeichen 4")


def schnitte(woerter):
    return [woerter[start : start + LAENGE] for start in range(0, len(woerter) - LAENGE + 1, LAENGE)]


def laden(datei, name, wortzahl):
    pfad = p.PROJEKT / "corpus_diplomatisch" / datei
    woerter = g.leerzeichen_woerter(pfad.read_text(encoding="utf-8"))
    if len(woerter) != wortzahl:
        raise SystemExit(f"{datei} hat {len(woerter)} Wörter, erwartet {wortzahl}")
    proben = schnitte(woerter)
    if not proben:
        raise SystemExit(name + " trägt keine Probe von 351 Wörtern")
    return {"name": name, "woerter": woerter, "schnitte": proben}


def matrix_fuer(proben, merkmale, art, n=None):
    if art == "woerter":
        return g.matrix_woerter(proben, merkmale)
    return g.matrix_ngramme(proben, merkmale, n)


def urteil(abstand, heine_index, vergleich_index):
    """Nah, fern oder gleich. Gleich zählt auf keine der beiden Seiten."""
    werte = np.asarray(abstand, dtype=float)
    heine = float(np.min(werte[list(heine_index)]))
    vergleich = float(np.min(werte[list(vergleich_index)]))
    naechster_heine = heine_index[int(np.argmin(werte[list(heine_index)]))]
    naechster_vergleich = vergleich_index[int(np.argmin(werte[list(vergleich_index)]))]
    if heine < vergleich:
        stufe = "nah"
    elif vergleich < heine:
        stufe = "fern"
    else:
        stufe = "gleich"
    return stufe, heine, vergleich, naechster_heine, naechster_vergleich


def anteil(stufen, ziel):
    return sum(stufe == ziel for stufe in stufen) / len(stufen)


def ausgang(nach_mass):
    nah = [anteil(nach_mass[mass], "nah") for mass in MASSE]
    fern = [anteil(nach_mass[mass], "fern") for mass in MASSE]
    if all(wert >= 0.5 for wert in nah) and all(wert < 0.5 for wert in fern):
        return "heine-nah"
    if all(wert >= 0.5 for wert in fern) and all(wert < 0.5 for wert in nah):
        return "heine-fern"
    return "unentschieden"


def fmt(wert):
    return f"{wert * 100:.1f} %".replace(".", ",")


def zahl(wert):
    return f"{wert:.4f}".replace(".", ",")


def haeufig(namen, zaehler):
    teile = []
    for name in namen:
        teile.append(f"{name} {fmt(zaehler[name] / WIEDERHOLUNGEN)}")
    return ", ".join(teile)


NAH = "#1f4e79"
FERN = "#a35d3a"
LINIE = "#d9d0c3"
GITTER = "#e6ddd0"
FARBE_TEXT = {
    "Aurora": "#1f4e79",
    "Biene": "#8a6a12",
    "Almanach": "#2f5d50",
    "Agrippina": "#5c4a6a",
    "Heimkehr": "#8c3a2f",
    "Kevlaar": "#3d5a3d",
    "Donna Clara": "#4a5568",
    "Schilda": "#9b3a4a",
    "Vagabund": "#b36b2a",
    "Müller": "#3d6b8a",
    "Steinmann": "#0b3a5b",
    "Uhland": "#2f6b4f",
    "Wunderhorn": "#6e6256",
}


def dez(wert, stellen=1):
    return f"{wert:.{stellen}f}".replace(".", ",")


def auswahl(zeilen, fenster, mass):
    return [zeile for zeile in zeilen if zeile["fenster"] == fenster and zeile["mass"] == mass]


def schreibe(pfad, teile):
    g.schreibe_svg(ORDNER / pfad, "\n".join(teile) + "\n")


def kopf(breite, hoehe, titel, untertitel):
    zeilen = abb._umbrueche(untertitel, breite - 72)
    teile = abb._kopf(breite, hoehe, 36, titel, zeilen)
    oben = 56 + 16 * len(zeilen)
    return teile, oben


def streuung(zeilen, vergleich_satz="Schilda, die Vagabunden-Lieder, Müller und Steinmann"):
    felder = []
    for mass in MASSE:
        punkte = []
        for zeile in auswahl(zeilen, "Anfang", mass):
            punkte.append(
                (float(zeile["abstand_heine"]), float(zeile["abstand_vergleich"]), zeile["stufe"])
            )
        felder.append(punkte)
    werte = [wert for punkte in felder for punkt in punkte for wert in punkt[:2]]
    lo = min(werte) - 0.04
    hi = max(werte) + 0.04
    seite = 430
    breite = 1080
    untertitel = (
        "Erste 351 Wörter. Jeder Punkt ist eine der 500 Ziehungen. "
        "Liegt er über der Diagonale, ist die nächste Heine-Probe näher als " + vergleich_satz + "."
    )
    teile, oben = kopf(breite, 780, "Nähe in den einzelnen Ziehungen", untertitel)
    feld = oben + 28
    schritt = 0.1

    def px(wert, links):
        return links + (wert - lo) / (hi - lo) * seite

    def py(wert):
        return feld + (hi - wert) / (hi - lo) * seite

    for spalte, (mass, punkte) in enumerate(zip(MASSE, felder)):
        links = 78 + spalte * (seite + 86)
        teile.append(
            f'<text x="{links}" y="{feld - 12}" font-family="Palatino, Georgia, serif" font-size="15" fill="{abb.TINTE}">{abb.xml(mass)}</text>'
        )
        tick = int(lo * 10) / 10
        while tick < hi:
            if tick >= lo:
                teile.append(
                    f'<line x1="{px(tick, links):.1f}" y1="{feld}" x2="{px(tick, links):.1f}" y2="{feld + seite}" stroke="{GITTER}" stroke-width="1"/>'
                )
                teile.append(
                    f'<line x1="{links}" y1="{py(tick):.1f}" x2="{links + seite}" y2="{py(tick):.1f}" stroke="{GITTER}" stroke-width="1"/>'
                )
                teile.append(
                    f'<text x="{links - 8}" y="{py(tick) + 4:.1f}" text-anchor="end" font-family="Palatino, Georgia, serif" font-size="11" fill="#6b645c">{dez(tick)}</text>'
                )
                teile.append(
                    f'<text x="{px(tick, links):.1f}" y="{feld + seite + 18}" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="11" fill="#6b645c">{dez(tick)}</text>'
                )
            tick = round(tick + schritt, 2)
        teile.append(
            f'<line x1="{px(lo, links):.1f}" y1="{py(lo):.1f}" x2="{px(hi, links):.1f}" y2="{py(hi):.1f}" stroke="#8a8175" stroke-width="1" stroke-dasharray="3 4"/>'
        )
        for x_wert, y_wert, stufe in punkte:
            farbe = NAH if stufe == "nah" else FERN
            teile.append(
                f'<circle cx="{px(x_wert, links):.1f}" cy="{py(y_wert):.1f}" r="3.3" fill="{farbe}" fill-opacity="0.38"/>'
            )
        teile.append(
            f'<text x="{links + seite / 2}" y="{feld + seite + 40}" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="12.5" fill="#6b645c">Abstand zur nächsten Heine-Probe</text>'
        )
    teile.append(
        f'<text x="22" y="{feld + seite / 2}" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="12.5" fill="#6b645c" transform="rotate(-90 22 {feld + seite / 2})">Abstand zum nächsten Vergleichstext</text>'
    )
    legende_y = feld + seite + 62
    for farbe, name, x_wert in ((NAH, "näher an Heine", 78), (FERN, "ferner als die vier Texte", 250)):
        teile.append(f'<circle cx="{x_wert}" cy="{legende_y}" r="4.2" fill="{farbe}"/>')
        teile.append(
            f'<text x="{x_wert + 12}" y="{legende_y + 4}" font-family="Palatino, Georgia, serif" font-size="13" fill="{abb.TINTE}">{name}</text>'
        )
    teile.append("</svg>")
    schreibe("abb_streuung.svg", teile)


def unterschied(zeilen):
    reihen = []
    for mass in MASSE:
        werte = [
            float(zeile["abstand_vergleich"]) - float(zeile["abstand_heine"])
            for zeile in auswahl(zeilen, "Anfang", mass)
        ]
        reihen.append(werte)
    alles = [wert for reihe in reihen for wert in reihe]
    lo = min(alles) - 0.02
    hi = max(alles) + 0.02
    bins = 32
    breite_feld = 430
    hoehe_feld = 280
    breite = 1040
    untertitel = (
        "Erste 351 Wörter. Die Differenz ist der Abstand zum nächsten Vergleichstext minus den Abstand zur nächsten Heine-Probe. "
        "Rechts der Null liegt Heine näher."
    )
    teile, oben = kopf(breite, 600, "Wie weit die Nähe reicht", untertitel)
    feld = oben + 26
    hoechste = 1
    zaehlungen = []
    for werte in reihen:
        zaehlung = [0] * bins
        for wert in werte:
            index = min(bins - 1, max(0, int((wert - lo) / (hi - lo) * bins)))
            zaehlung[index] += 1
        zaehlungen.append(zaehlung)
        hoechste = max(hoechste, max(zaehlung))
    for spalte, (mass, zaehlung, werte) in enumerate(zip(MASSE, zaehlungen, reihen)):
        links = 78 + spalte * (breite_feld + 70)
        teile.append(
            f'<text x="{links}" y="{feld - 10}" font-family="Palatino, Georgia, serif" font-size="15" fill="{abb.TINTE}">{abb.xml(mass)}</text>'
        )
        for index, anzahl in enumerate(zaehlung):
            x0 = lo + index * (hi - lo) / bins
            x1 = lo + (index + 1) * (hi - lo) / bins
            mitte = (x0 + x1) / 2
            balken_h = anzahl / hoechste * hoehe_feld
            x_links = links + (x0 - lo) / (hi - lo) * breite_feld
            x_rechts = links + (x1 - lo) / (hi - lo) * breite_feld
            teile.append(
                f'<rect x="{x_links:.1f}" y="{feld + hoehe_feld - balken_h:.1f}" width="{max(0.6, x_rechts - x_links - 0.8):.1f}" height="{balken_h:.1f}" fill="{NAH if mitte >= 0 else FERN}" fill-opacity="0.9"/>'
            )
        null_x = links + (0 - lo) / (hi - lo) * breite_feld
        median = float(np.median(werte))
        median_x = links + (median - lo) / (hi - lo) * breite_feld
        teile.append(
            f'<line x1="{null_x:.1f}" y1="{feld}" x2="{null_x:.1f}" y2="{feld + hoehe_feld}" stroke="{abb.TINTE}" stroke-width="1"/>'
        )
        teile.append(
            f'<line x1="{median_x:.1f}" y1="{feld}" x2="{median_x:.1f}" y2="{feld + hoehe_feld}" stroke="#1c1915" stroke-width="1.2" stroke-dasharray="2 3"/>'
        )
        teile.append(
            f'<text x="{links + breite_feld}" y="{feld - 10}" text-anchor="end" font-family="Palatino, Georgia, serif" font-size="12.5" fill="#6b645c">Median {dez(median, 2)}</text>'
        )
        tick = round(int(lo * 5) / 5, 2)
        while tick <= hi:
            x_wert = links + (tick - lo) / (hi - lo) * breite_feld
            teile.append(
                f'<text x="{x_wert:.1f}" y="{feld + hoehe_feld + 18}" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="11" fill="#6b645c">{dez(tick)}</text>'
            )
            tick = round(tick + 0.2, 2)
        teile.append(
            f'<text x="{links + breite_feld / 2}" y="{feld + hoehe_feld + 42}" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="12.5" fill="#6b645c">Differenz der Abstände, Cosine Delta</text>'
        )
    teile.append(
        f'<text x="20" y="{feld + hoehe_feld / 2}" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="12.5" fill="#6b645c" transform="rotate(-90 20 {feld + hoehe_feld / 2})">Anzahl der Ziehungen</text>'
    )
    teile.append("</svg>")
    schreibe("abb_unterschied.svg", teile)


def anteile(zeilen):
    reihen = []
    for fenster, hinweis in (("Anfang", "entscheidet"), ("Ende", "entscheidet nicht")):
        for mass in MASSE:
            daten = auswahl(zeilen, fenster, mass)
            reihen.append(
                (
                    f"{'150 Wörter' if mass.startswith('Wörter') else 'Vierergruppen'}, {'erste' if fenster == 'Anfang' else 'letzte'} 351",
                    anteil([zeile["stufe"] for zeile in daten], "nah"),
                    anteil([zeile["stufe"] for zeile in daten], "fern"),
                    hinweis,
                )
            )
    breite = 920
    untertitel = (
        "Anteil der 500 Ziehungen. Die ersten 351 Wörter entscheiden. Die letzten 351 Wörter überlappen sie und entscheiden nicht."
    )
    teile, oben = kopf(breite, 360, "Mehrheit der Ziehungen", untertitel)
    links = 250
    balken = 560
    for nummer, (name, nah, fern, hinweis) in enumerate(reihen):
        y_wert = oben + nummer * 42
        teile.append(
            f'<text x="{links - 14}" y="{y_wert + 16}" text-anchor="end" font-family="Palatino, Georgia, serif" font-size="14" fill="{abb.TINTE}">{abb.xml(name)}</text>'
        )
        teile.append(
            f'<rect x="{links}" y="{y_wert}" width="{nah * balken:.1f}" height="24" fill="{NAH}"/>'
        )
        teile.append(
            f'<rect x="{links + nah * balken:.1f}" y="{y_wert}" width="{fern * balken:.1f}" height="24" fill="{FERN}"/>'
        )
        teile.append(
            f'<text x="{links + 10}" y="{y_wert + 16}" font-family="Palatino, Georgia, serif" font-size="12" fill="#f6f1e8">{dez(nah * 100, 1)} %</text>'
        )
        teile.append(
            f'<text x="{links + balken - 8}" y="{y_wert + 16}" text-anchor="end" font-family="Palatino, Georgia, serif" font-size="12" fill="#f6f1e8">{dez(fern * 100, 1)} %</text>'
        )
    y_legende = oben + len(reihen) * 42 + 8
    teile.append(f'<rect x="{links}" y="{y_legende}" width="14" height="14" fill="{NAH}"/>')
    teile.append(
        f'<text x="{links + 20}" y="{y_legende + 12}" font-family="Palatino, Georgia, serif" font-size="13" fill="{abb.TINTE}">näher an Heine</text>'
    )
    teile.append(f'<rect x="{links + 160}" y="{y_legende}" width="14" height="14" fill="{FERN}"/>')
    teile.append(
        f'<text x="{links + 180}" y="{y_legende + 12}" font-family="Palatino, Georgia, serif" font-size="13" fill="{abb.TINTE}">ferner</text>'
    )
    teile.append("</svg>")
    schreibe("abb_anteile.svg", teile)


def naechste(zeilen, gruppe, datei, titel, untertitel):
    namen = [name for _, name, _ in gruppe]
    schluessel = "naechster_heine" if gruppe is HEINE else "naechster_vergleich"
    breite = 920
    zeile_h = 46
    links = 150
    balken = 580
    teile, oben = kopf(breite, 120 + len(namen) * zeile_h + 80, titel, untertitel)
    y_achse = oben + len(namen) * zeile_h + 4
    for tick in (0, 0.2, 0.4, 0.6, 0.8):
        x_wert = links + tick / 0.8 * balken
        teile.append(
            f'<line x1="{x_wert:.1f}" y1="{oben - 4}" x2="{x_wert:.1f}" y2="{y_achse}" stroke="{GITTER}" stroke-width="1"/>'
        )
        teile.append(
            f'<text x="{x_wert:.1f}" y="{y_achse + 16}" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="11" fill="#6b645c">{int(tick * 100)}</text>'
        )
    for nummer, name in enumerate(namen):
        y_wert = oben + nummer * zeile_h
        teile.append(
            f'<text x="{links - 14}" y="{y_wert + 20}" text-anchor="end" font-family="Palatino, Georgia, serif" font-size="14" fill="{FARBE_TEXT[name]}">{abb.xml(name)}</text>'
        )
        for versatz, mass in ((0, "Wörter 150"), (16, "Zeichen 4")):
            daten = auswahl(zeilen, "Anfang", mass)
            wert = sum(zeile[schluessel] == name for zeile in daten) / len(daten)
            farbe = FARBE_TEXT[name] if mass == "Wörter 150" else "#c4b8a8"
            breit = wert / 0.8 * balken
            teile.append(
                f'<rect x="{links}" y="{y_wert + versatz}" width="{breit:.1f}" height="12" fill="{farbe}"/>'
            )
            teile.append(
                f'<text x="{links + breit + 6:.1f}" y="{y_wert + versatz + 10}" font-family="Palatino, Georgia, serif" font-size="11" fill="#6b645c">{dez(wert * 100, 1)} %</text>'
            )
    teile.append(
        f'<text x="{links + balken / 2}" y="{y_achse + 36}" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="12.5" fill="#6b645c">Anteil der 500 Ziehungen, Prozent</text>'
    )
    teile.append(
        f'<text x="{links}" y="{y_achse + 58}" font-family="Palatino, Georgia, serif" font-size="12.5" fill="#6b645c">Die Farbe des Textes zeigt die 150 Wörter. Grau sind die Vierergruppen.</text>'
    )
    teile.append("</svg>")
    schreibe(datei, teile)


def zeichnen(zeilen, vergleich=None, vergleich_satz="Schilda, die Vagabunden-Lieder, Müller und Steinmann"):
    if vergleich is None:
        vergleich = VERGLEICH
    streuung(zeilen, vergleich_satz)
    unterschied(zeilen)
    anteile(zeilen)
    naechste(
        zeilen,
        HEINE,
        "abb_naechster_heine.svg",
        "Welcher Heine-Text der nächste ist",
        "Erste 351 Wörter. Gezählt wird in jeder Ziehung der nächste Heine-Text, auch dann, wenn ein Vergleichstext noch näher liegt. Diese Häufigkeit entscheidet nicht.",
    )
    naechste(
        zeilen,
        vergleich,
        "abb_naechster_vergleich.svg",
        "Welcher Vergleichstext der nächste ist",
        "Erste 351 Wörter. Gezählt wird der nächste unter " + vergleich_satz + ". Diese Häufigkeit entscheidet nicht.",
    )


def satz(ergebnis):
    if ergebnis == "heine-nah":
        return (
            "Ausgang: heine-nah. Auf beiden Maßen liegt in mindestens der Hälfte der Ziehungen "
            "eine Heine-Probe näher als Schilda, die Vagabunden-Lieder, Müller und Steinmann."
        )
    if ergebnis == "heine-fern":
        return (
            "Ausgang: heine-fern. Auf beiden Maßen liegt in mindestens der Hälfte der Ziehungen "
            "einer von Schilda, den Vagabunden-Liedern, Müller und Steinmann jeder Heine-Probe näher."
        )
    return (
        "Ausgang: unentschieden. Die beiden Maße erreichen nicht gemeinsam die Hälfte "
        "für Nähe und nicht gemeinsam die Hälfte für Ferne."
    )


def main():
    if ORDNER.exists() and os.environ.get("AUTOR_NEUZEICHNEN") != "1":
        raise SystemExit("Der Ordner besteht schon und wird nicht überschrieben: " + str(ORDNER))
    ORDNER.mkdir(parents=True, exist_ok=True)

    bekannt = [laden(*eintrag) for eintrag in HEINE + VERGLEICH]
    kandidat = laden(*KANDIDAT)
    namen = [text["name"] for text in bekannt]
    heine_index = [namen.index(name) for _, name, _ in HEINE]
    vergleich_index = [namen.index(name) for _, name, _ in VERGLEICH]
    anfang = kandidat["woerter"][:LAENGE]
    ende = kandidat["woerter"][-LAENGE:]
    if len(anfang) != LAENGE or len(ende) != LAENGE:
        raise SystemExit("Der Kandidat liefert kein Fenster von 351 Wörtern")
    ueberlappung = len(set(range(LAENGE)) & set(range(len(kandidat["woerter"]) - LAENGE, len(kandidat["woerter"]))))

    rng = np.random.default_rng(np.random.SeedSequence(SEED))
    zeilen = []
    for nummer in range(1, WIEDERHOLUNGEN + 1):
        gezogen = []
        for text in bekannt:
            if len(text["schnitte"]) == 1:
                probe = text["schnitte"][0]
            else:
                probe = text["schnitte"][int(rng.integers(0, len(text["schnitte"])))]
            gezogen.append(probe)
        worte = g.merkmal_woerter(gezogen, 300)[: p.MFW]
        zeichen = g.merkmal_ngramme(gezogen, 4, p.ZEICHEN_HAEUFIGSTE)
        for art, merkmale, n, mass in (
            ("woerter", worte, None, "Wörter 150"),
            ("zeichen", zeichen, 4, "Zeichen 4"),
        ):
            basis = matrix_fuer(gezogen, merkmale, art, n)
            for fenster, probe in (("Anfang", anfang), ("Ende", ende)):
                zeile = np.vstack([basis, matrix_fuer([probe], merkmale, art, n)])
                abstand = abb.kosinus(zeile, basis)
                if abstand is None:
                    raise SystemExit("Abstand ist nicht bestimmt")
                stufe, heine, vergleich, i_heine, i_vergleich = urteil(
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
        nach_mass = {mass: [] for mass in MASSE}
        heine_nah = {mass: Counter() for mass in MASSE}
        vergleich_nah = {mass: Counter() for mass in MASSE}
        abstand_heine = {mass: [] for mass in MASSE}
        abstand_vergleich = {mass: [] for mass in MASSE}
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
    ergebnis = ausgang(anfang_pack[0])
    ergebnis_ende = ausgang(ende_pack[0])

    def tabelle(pack):
        nach_mass, heine_nah, vergleich_nah, abstand_heine, abstand_vergleich = pack
        koerper = [
            "| Maß | näher an Heine | ferner | gleich | Median Heine | Median Vergleich |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
        for mass in MASSE:
            koerper.append(
                f"| {mass} | {fmt(anteil(nach_mass[mass], 'nah'))} "
                f"| {fmt(anteil(nach_mass[mass], 'fern'))} "
                f"| {fmt(anteil(nach_mass[mass], 'gleich'))} "
                f"| {zahl(float(np.median(abstand_heine[mass])))} "
                f"| {zahl(float(np.median(abstand_vergleich[mass])))} |"
            )
        texte = []
        for mass in MASSE:
            texte.append(
                f"Nächster Heine-Text, {mass}: {haeufig([name for _, name, _ in HEINE], heine_nah[mass])}."
            )
            texte.append(
                f"Nächster Vergleichstext, {mass}: {haeufig([name for _, name, _ in VERGLEICH], vergleich_nah[mass])}."
            )
        return koerper, texte

    tabelle_anfang, texte_anfang = tabelle(anfang_pack)
    tabelle_ende, texte_ende = tabelle(ende_pack)
    bericht = "\n".join(
        [
            "# Nähe oder Ferne",
            "",
            "Diese Prüfung ersetzt Studie 1 bis 6 nicht. Jeder bekannte Text gibt eine Probe, der Kandidat gibt ein Fenster derselben Länge.",
            "",
            satz(ergebnis),
            "",
            "Entschieden haben die ersten 351 Wörter des Kandidaten. Eine Heine-Probe muss näher liegen als Schilda, als die Vagabunden-Lieder, als Müller und als Steinmann. Das muss auf beiden Maßen in mindestens der Hälfte der 500 Ziehungen gelten. Ferne verlangt dasselbe in der anderen Richtung.",
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
            "Aufgenommen sind elf bekannte Texte und der Kandidat. Jeder bekannte Text bleibt eine eigene Datei. Eine Probe überschreitet keine Grenze zwischen zwei Dateien, und es wird nichts aneinandergehängt. Die Merkmale und die Standardwerte kommen nur aus den elf bekannten Texten, in jeder Ziehung aus genau einer Probe je Text. Der Kandidat wählt sie nicht mit.",
            "",
            "Die frühen strophischen Lieder Heines sind Aurora (`Heine_Aurora.txt`, 1089 Wörter, 3 Proben), die Biene (`Heine_Biene.txt`, 351 Wörter, 1 Probe), der Musenalmanach (`Heine_Almanach.txt`, 617 Wörter, 1 Probe), Agrippina (`Heine_Agrippina.txt`, 830 Wörter, 2 Proben), die Heimkehr (`Heine_Heimkehr.txt`, 2467 Wörter, 7 Proben), Kevlaar (`Heine_Kevlaar.txt`, 397 Wörter, 1 Probe) und Donna Clara (`Heine_DonnaClara.txt`, 413 Wörter, 1 Probe).",
            "",
            "Schilda ist `Hektor_Schilda.txt`, 7396 Wörter und 21 Proben. Das sind die strophischen Lieder aus *Lieder aus Schilda*, mit Reim der geraden Zeilen. Die Knittelverse, also der Paarreim Zeile auf Zeile, stehen nicht in dieser Datei. Sie liegen in `Hektor_Knittel.txt` und sind hier nicht gerechnet. Ebenfalls nicht in der Schilda-Datei und nicht in dieser Prüfung sind die Introduktion von 1843, die Ballade XXI, der Block um XXXV und die Gedichte LXX bis LXXVII. Der Ganztext des Bandes, `Hektor/Hektor_Schilda_1847.txt`, bleibt draußen, damit die Teile nicht doppelt gezählt werden.",
            "",
            "Die Vagabunden-Lieder sind `Hektor_Vagabund.txt`, 2143 Wörter und 6 Proben. Aufgenommen sind die achtzehn strophischen Gedichte I bis XVIII aus *Der Vagabund*, Hefte VI bis XI 1848. Das sind Hektors eigene Lieder und nicht der Kandidat. Die Prosastücke derselben Hefte fehlen.",
            "",
            "Müller ist nur Teil 1 des *Waldhornisten*, `Mueller_1.txt`, 11279 Wörter und 32 Proben. Teil 2 bleibt als Rückhalt draußen.",
            "",
            "Steinmann ist `Steinmann_Lieder.txt`, 492 Wörter und 1 Probe. Darin stehen die Zuckerpastillen I bis V, die Lieder I und II und die sechs Strophen ohne eigene Überschrift von den Seiten 193 bis 194. Die Datei heißt nicht Heine. Nicht darin und nicht in dieser Prüfung sind die Parodie, die Wandelnden Blumen in Berlin, Im Hofgarten zu Düsseldorf und die beiden Sonette. Die Sonette liegen in `Steinmann_Sonette.txt`.",
            "",
            f"Der Kandidat ist `Kandidat_Vagabund.txt`, die Gedichte I bis X, {len(kandidat['woerter'])} Wörter. Entschieden wird mit den ersten {LAENGE}. Die letzten {LAENGE} werden nur mitgeteilt.",
            "",
            "Nicht aufgenommen, weil sie eine andere Form sind oder nicht zu dieser engen Frage gehören: *Götterdämmerung* und *Ratcliff*, Uhlands Lieder und Balladen, das *Wunderhorn*, die Juniuslieder und die übrigen Geibel-Dateien, Nordsee und das *Buch der Lieder* von 1827. Die Teilabschriften des Kandidaten, `Kandidat_I-V.txt` und `Kandidat_VI-X.txt`, und alle Dateien mit der Endung `_ber` bleiben ebenfalls draußen.",
            "",
            "Die Abbildungen stehen daneben und entscheiden nicht.",
            "",
        ]
    )
    (ORDNER / "BERICHT.md").write_text(bericht, encoding="utf-8")
    zeichnen(zeilen)
    print(satz(ergebnis))
    print("Letzte 351, ohne Entscheidung:", ergebnis_ende)
    for zeile in tabelle_anfang:
        print(zeile)
    print("Geschrieben nach", ORDNER)


if __name__ == "__main__":
    main()
