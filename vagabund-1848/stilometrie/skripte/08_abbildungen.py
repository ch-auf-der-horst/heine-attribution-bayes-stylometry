# -*- coding: utf-8 -*-
"""Zeichnet die Studie 1. Die Entscheidung wird nicht neu gerechnet.

Liest den bestehenden Laufordner, teilung.json, die Eichdateien und
06_impostors.json. Der Kandidat wird nur für die Abbildungen gelesen,
in denen er als Blatt oder Markierung erscheint.

Zwei Arten von Bäumen, jeweils für Eichproben, Profile, Zeichen-4-Gramme
und die Merkmalleiter:

- Dendrogramm: der UPGMA-Baum der festgelegten Merkmale, rechteckig.
  Die waagerechte Achse ist die Gruppierungshöhe.
- Stern: derselbe Baum, sternförmig um die letzte Gruppe. Die Astlänge
  ist dieselbe Höhe. Dazu der Mehrheitskonsens als Stern mit gleicher
  Astlänge; diese Länge ist keine Distanz.
- Konsensbaum: der Mehrheitskonsens behält jede Klade, die in mindestens
  der Hälfte der Bäume vorkommt. Äste unter dieser Schwelle fehlen.

Der Merkmal-Bootstrap behält jedes festgelegte Merkmal mit
Wahrscheinlichkeit 0,5, 500-mal. Die Merkmalleiter, wie der Bootstrap
Consensus Tree in stylo, baut je einen Baum für 100, 150 und 300
häufigste Wörter. 100 und 300 entscheiden in der Studie nicht.

Weitere Abbildungen: Abstand der Eichproben, Impostors-Anteile,
Abstände zu den Profilen, Wärmebild der Wortabstände.

Schreibt SVG- und PNG-Dateien, 08_konsens_kladen.csv und abb_uebersicht.html
in den Laufordner. Aufruf, wenn der Lauf schon besteht:

    python3 analyse/08_abbildungen.py
"""

import csv
import html
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g

BOOTSTRAP = 500
KONSENS_MINIMUM = 0.5
MERKMALANTEIL = 0.5

FARBE = {
    "heine": "#1f4e79",
    "hektor": "#8c3a2f",
    "mueller": "#2f5d50",
    "wunderhorn": "#4a5568",
    "uhland": "#3d5a3d",
    "geibel": "#5c4a6a",
    "kandidat": "#8a6a12",
}
KLASSENNAME = {
    "heine": "Heine",
    "hektor": "Schilda",
    "mueller": "Müller",
    "wunderhorn": "Wunderhorn",
    "uhland": "Uhland",
    "geibel": "Geibel",
    "kandidat": "Kandidat",
}

def xml(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def kosinus(relativ, eichung):
    """Kosinusabstände. Mittel und Streuung kommen nur aus eichung."""
    mittel = eichung.mean(axis=0)
    streuung = eichung.std(axis=0, ddof=p.STANDARDABWEICHUNG_DDOF)
    behalten = streuung > 0
    if int(behalten.sum()) < 2:
        return None
    standard = (relativ[:, behalten] - mittel[behalten]) / streuung[behalten]
    normen = np.linalg.norm(standard, axis=1, keepdims=True)
    if np.any(normen == 0):
        return None
    aehnlichkeit = (standard @ standard.T) / (normen @ normen.T)
    abstand = 1.0 - np.clip(aehnlichkeit, -1.0, 1.0)
    np.fill_diagonal(abstand, 0.0)
    return abstand


def upgma(abstand):
    """UPGMA. Gibt die Wurzel zurück. Kinder sind nach dem kleineren Blattindex geordnet."""
    n = abstand.shape[0]
    dist = np.full((2 * n, 2 * n), np.inf)
    dist[:n, :n] = abstand
    np.fill_diagonal(dist[:n, :n], np.inf)
    knoten = [
        {"blaetter": frozenset([i]), "kinder": None, "groesse": 1, "index": i, "hoehe": 0.0}
        for i in range(n)
    ]
    aktiv = list(range(n))
    while len(aktiv) > 1:
        beste = None
        for pos_a, a in enumerate(aktiv):
            for b in aktiv[pos_a + 1 :]:
                wert = dist[a, b]
                if beste is None or wert < beste[0]:
                    beste = (wert, a, b)
        wert, links, rechts = beste
        if min(knoten[links]["blaetter"]) > min(knoten[rechts]["blaetter"]):
            links, rechts = rechts, links
        neu = {
            "blaetter": knoten[links]["blaetter"] | knoten[rechts]["blaetter"],
            "kinder": (knoten[links], knoten[rechts]),
            "groesse": knoten[links]["groesse"] + knoten[rechts]["groesse"],
            "index": min(knoten[links]["index"], knoten[rechts]["index"]),
            "hoehe": float(wert),
        }
        neu_id = len(knoten)
        knoten.append(neu)
        for anderer in aktiv:
            if anderer in (links, rechts):
                continue
            dist[neu_id, anderer] = dist[anderer, neu_id] = (
                knoten[links]["groesse"] * dist[links, anderer]
                + knoten[rechts]["groesse"] * dist[rechts, anderer]
            ) / neu["groesse"]
        aktiv = [a for a in aktiv if a not in (links, rechts)] + [neu_id]
    return knoten[aktiv[0]]


def kladen(wurzel):
    gefunden = []

    def lauf(knoten):
        if knoten["kinder"] is None:
            return
        gefunden.append(knoten["blaetter"])
        lauf(knoten["kinder"][0])
        lauf(knoten["kinder"][1])

    lauf(wurzel)
    return gefunden


def blattordnung(wurzel):
    folge = []

    def lauf(knoten):
        if knoten["kinder"] is None:
            folge.append(knoten["index"])
            return
        lauf(knoten["kinder"][0])
        lauf(knoten["kinder"][1])

    lauf(wurzel)
    return folge


def vertraeglich(links, rechts):
    return links.isdisjoint(rechts) or links <= rechts or rechts <= links


def mehrheit(kladen_je_baum, anzahl_blaetter):
    zaehlung = Counter()
    for ein_baum in kladen_je_baum:
        for klade in ein_baum:
            if 1 < len(klade) < anzahl_blaetter:
                zaehlung[klade] += 1
    baeume = len(kladen_je_baum)
    gewaehlt = []
    for klade, anzahl in sorted(zaehlung.items(), key=lambda paar: (-paar[1], -len(paar[0]))):
        anteil = anzahl / baeume
        if anteil < KONSENS_MINIMUM:
            continue
        if all(vertraeglich(klade, andere) for andere, _ in gewaehlt):
            gewaehlt.append((klade, anteil))
    return gewaehlt, baeume


def anteile_der_kladen(baeume):
    """Anteil jedes Astes, auch unter der Mehrheit. Die Wurzel fehlt."""
    zaehlung = Counter()
    for ein_baum in baeume:
        for klade in ein_baum:
            if len(klade) > 1:
                zaehlung[klade] += 1
    nenner = len(baeume)
    return {klade: anzahl / nenner for klade, anzahl in zaehlung.items()}


def baum_aus_kladen(gewaehlt, etiketten, referenz):
    alle = frozenset(range(len(etiketten)))
    teile = [alle] + [frozenset([i]) for i in range(len(etiketten))]
    teile += [klade for klade, _ in gewaehlt]
    stuetze = {klade: anteil for klade, anteil in gewaehlt}
    rang = {blatt: stelle for stelle, blatt in enumerate(referenz)}

    def kinder(klade):
        darin = [teil for teil in teile if teil < klade and teil <= klade]
        maximal = []
        for teil in darin:
            if any(teil < anderer for anderer in darin):
                continue
            maximal.append(teil)
        maximal.sort(key=lambda teil: min(rang[blatt] for blatt in teil))
        return maximal

    def knoten(klade):
        nachfolger = kinder(klade)
        if not nachfolger:
            blatt = next(iter(klade))
            return {"etikett": etiketten[blatt], "kinder": [], "stuetze": None, "blatt": blatt}
        return {
            "etikett": None,
            "kinder": [knoten(teil) for teil in nachfolger],
            "stuetze": stuetze.get(klade),
            "blatt": None,
        }

    return knoten(alle)


def _farbe_studie(etikett):
    zuordnung = {
        "Heine": FARBE["heine"],
        "Hektor": FARBE["hektor"],
        "Schilda": FARBE["hektor"],
        "Müller": FARBE["mueller"],
        "Wunderhorn": FARBE["wunderhorn"],
        "Uhland": FARBE["uhland"],
        "Geibel": FARBE["geibel"],
        "Kandidat": FARBE["kandidat"],
    }
    return zuordnung.get(str(etikett).split()[0], "#5c564e")


PAPIER = "#f6f1e8"
TINTE = "#1c1915"
GEMISCHT = "#5c564e"


def svg_baum(wurzel, titel, untertitel, pfad, farbe_von=None):
    zaehler = {"y": 0}

    def messe(knoten):
        if not knoten["kinder"]:
            knoten["y"] = zaehler["y"]
            zaehler["y"] += 1
            return
        for kind in knoten["kinder"]:
            messe(kind)
        knoten["y"] = sum(kind["y"] for kind in knoten["kinder"]) / len(knoten["kinder"])

    def setze_x(knoten):
        if not knoten["kinder"]:
            knoten["x"] = 1.0
            return
        for kind in knoten["kinder"]:
            setze_x(kind)
        knoten["x"] = min(kind["x"] for kind in knoten["kinder"]) - 1.0

    def schiebe(knoten, delta):
        knoten["x"] += delta
        for kind in knoten["kinder"]:
            schiebe(kind, delta)

    messe(wurzel)
    setze_x(wurzel)
    schiebe(wurzel, -wurzel["x"])
    if farbe_von is None:
        farbe_von = _farbe_studie
    blaetter = zaehler["y"]
    zeile = 28 if blaetter > 14 else 38
    links = 36
    laengster = max((len(knoten["etikett"]) for knoten in _blaetter_von(wurzel)), default=8)
    rechts = min(250, 36 + int(laengster * 7.6))
    spanne = max(knoten_x(wurzel), 1.0)
    breite_ast = min(520, max(168, int(78 * spanne)))
    inhalt = links + breite_ast + rechts
    zeilen_titel = _umbrueche(untertitel, inhalt - links - 28)
    oben = 52 + 17 * len(zeilen_titel)

    def px(x):
        return links + (x / spanne) * breite_ast

    def py(y):
        return oben + y * zeile + zeile / 2

    hoehe = oben + blaetter * zeile + 36
    breite = max(links + breite_ast + rechts, _mindestbreite(links, titel, zeilen_titel))
    teile = _kopf(breite, hoehe, links, titel, zeilen_titel)

    def farbe_klade(knoten):
        namen = [blatt["etikett"] for blatt in _blaetter_von(knoten)]
        farben = {farbe_von(name) for name in namen}
        if len(farben) == 1:
            return next(iter(farben))
        return GEMISCHT

    def zeichne(knoten):
        farbe = farbe_klade(knoten)
        for kind in knoten["kinder"]:
            teile.append(
                f'<line x1="{px(knoten["x"]):.1f}" y1="{py(kind["y"]):.1f}" '
                f'x2="{px(kind["x"]):.1f}" y2="{py(kind["y"]):.1f}" stroke="{farbe_klade(kind)}" '
                f'stroke-width="1.7" stroke-linecap="square"/>'
            )
            zeichne(kind)
        if knoten["kinder"]:
            ys = [py(kind["y"]) for kind in knoten["kinder"]]
            teile.append(
                f'<line x1="{px(knoten["x"]):.1f}" y1="{min(ys):.1f}" '
                f'x2="{px(knoten["x"]):.1f}" y2="{max(ys):.1f}" stroke="{farbe}" stroke-width="1.7"/>'
            )
            if knoten["stuetze"] is not None:
                _zahl(teile, px(knoten["x"]) + 7, py(knoten["y"]) - 7, knoten["stuetze"])
        else:
            farbe_blatt = farbe_von(knoten["etikett"])
            teile.append(
                f'<circle cx="{px(knoten["x"]) + 1:.1f}" cy="{py(knoten["y"]):.1f}" r="3.1" fill="{farbe_blatt}"/>'
            )
            teile.append(
                f'<text x="{px(knoten["x"]) + 12:.1f}" y="{py(knoten["y"]) + 4:.1f}" '
                f'font-family="Palatino, Georgia, serif" font-size="14" fill="{farbe_blatt}">'
                f'{xml(knoten["etikett"])}</text>'
            )

    zeichne(wurzel)
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")


def svg_dendrogramm(wurzel, etiketten, stuetzen, titel, untertitel, pfad, farbe_von=None):
    """Rechteckiges Dendrogramm. Die waagerechte Achse ist die UPGMA-Höhe."""
    if farbe_von is None:
        farbe_von = _farbe_studie
    zaehler = {"y": 0}

    def messe(knoten):
        if knoten["kinder"] is None:
            knoten["y"] = zaehler["y"]
            zaehler["y"] += 1
            return
        messe(knoten["kinder"][0])
        messe(knoten["kinder"][1])
        knoten["y"] = (knoten["kinder"][0]["y"] + knoten["kinder"][1]["y"]) / 2

    messe(wurzel)
    blaetter = zaehler["y"]
    zeile = 30 if blaetter > 14 else 40
    links = 28
    stamm = 18
    breite_ast = 460
    laengster = max((len(name) for name in etiketten), default=8)
    rechts = min(260, 40 + int(laengster * 7.8))
    inhalt = links + stamm + breite_ast + rechts
    zeilen_titel = _umbrueche(untertitel, inhalt - links - 28)
    oben = 56 + 17 * len(zeilen_titel)

    def hoechste(knoten):
        if knoten["kinder"] is None:
            return float(knoten["hoehe"])
        return max(
            float(knoten["hoehe"]),
            hoechste(knoten["kinder"][0]),
            hoechste(knoten["kinder"][1]),
        )

    max_hoehe = max(hoechste(wurzel), 1e-6)

    def px(hoehe):
        return links + stamm + (1.0 - hoehe / max_hoehe) * breite_ast

    def py(y):
        return oben + y * zeile + zeile / 2

    achse_y = oben + blaetter * zeile + 28
    hoehe_bild = achse_y + 36
    breite = max(links + stamm + breite_ast + rechts, _mindestbreite(links, titel, zeilen_titel))
    teile = _kopf(breite, hoehe_bild, links, titel, zeilen_titel)

    def farbe_klade(knoten):
        farben = set()

        def sammle(teil):
            if teil["kinder"] is None:
                farben.add(farbe_von(etiketten[teil["index"]]))
                return
            sammle(teil["kinder"][0])
            sammle(teil["kinder"][1])

        sammle(knoten)
        if len(farben) == 1:
            return next(iter(farben))
        return GEMISCHT

    wurzel_y = py(wurzel["y"])
    teile.append(
        f'<line x1="{links:.1f}" y1="{wurzel_y:.1f}" x2="{px(wurzel["hoehe"]):.1f}" y2="{wurzel_y:.1f}" '
        f'stroke="{GEMISCHT}" stroke-width="1.7"/>'
    )

    def zeichne(knoten):
        if knoten["kinder"] is None:
            farbe = farbe_von(etiketten[knoten["index"]])
            teile.append(
                f'<circle cx="{px(0):.1f}" cy="{py(knoten["y"]):.1f}" r="3.2" fill="{farbe}"/>'
            )
            teile.append(
                f'<text x="{px(0) + 12:.1f}" y="{py(knoten["y"]) + 4:.1f}" '
                f'font-family="Palatino, Georgia, serif" font-size="15" fill="{farbe}">'
                f'{xml(etiketten[knoten["index"]])}</text>'
            )
            return
        links_kind, rechts_kind = knoten["kinder"]
        zeichne(links_kind)
        zeichne(rechts_kind)
        x_eltern = px(knoten["hoehe"])
        ys = [py(links_kind["y"]), py(rechts_kind["y"])]
        teile.append(
            f'<line x1="{x_eltern:.1f}" y1="{min(ys):.1f}" x2="{x_eltern:.1f}" y2="{max(ys):.1f}" '
            f'stroke="{farbe_klade(knoten)}" stroke-width="1.7"/>'
        )
        for kind in (links_kind, rechts_kind):
            teile.append(
                f'<line x1="{x_eltern:.1f}" y1="{py(kind["y"]):.1f}" '
                f'x2="{px(kind["hoehe"]):.1f}" y2="{py(kind["y"]):.1f}" '
                f'stroke="{farbe_klade(kind)}" stroke-width="1.7" stroke-linecap="square"/>'
            )
        if stuetzen is not None and len(knoten["blaetter"]) < blaetter:
            anteil = stuetzen.get(knoten["blaetter"], 0.0)
            _zahl(teile, x_eltern + 6, py(knoten["y"]) - 8, anteil)

    zeichne(wurzel)
    _achse(teile, px(max_hoehe), px(0.0), achse_y, max_hoehe)
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")


def svg_stern(wurzel, etiketten, stuetzen, titel, untertitel, pfad, farbe_von=None, art="hoehe"):
    """Sternförmiger Baum. art hoehe zeichnet UPGMA-Längen, art gleich einen Kladogramm-Stern."""
    if farbe_von is None:
        farbe_von = _farbe_studie
    if art == "hoehe":
        ast = _stern_aus_upgma(wurzel, etiketten, stuetzen or {})
        masstab = True
    elif art == "gleich":
        ast = _stern_aus_konsens(wurzel)
        masstab = False
    else:
        raise SystemExit("Unbekannte Sternart: " + art)
    _stern_winkel(ast, -math.pi / 2, 3 * math.pi / 2)
    _stern_mindestlaenge(ast)
    _stern_orte(ast, 0.0, 0.0)
    _stern_zeichnen(ast, titel, untertitel, pfad, farbe_von, masstab)


def _stern_aus_upgma(knoten, etiketten, stuetzen, eltern_hoehe=None):
    if knoten["kinder"] is None:
        laenge = 0.0 if eltern_hoehe is None else max(0.0, eltern_hoehe - float(knoten["hoehe"]))
        return {"kinder": [], "laenge": laenge, "name": etiketten[knoten["index"]], "stuetze": None}
    kinder = [_stern_aus_upgma(kind, etiketten, stuetzen, float(knoten["hoehe"])) for kind in knoten["kinder"]]
    laenge = 0.0 if eltern_hoehe is None else max(0.0, eltern_hoehe - float(knoten["hoehe"]))
    stuetze = None if eltern_hoehe is None else stuetzen.get(knoten["blaetter"], 0.0)
    return {"kinder": kinder, "laenge": laenge, "name": None, "stuetze": stuetze}


def _stern_aus_konsens(knoten, wurzel=True):
    kinder = [_stern_aus_konsens(kind, False) for kind in knoten["kinder"]]
    return {
        "kinder": kinder,
        "laenge": 0.0 if wurzel else 1.0,
        "name": knoten.get("etikett"),
        "stuetze": None if wurzel else knoten.get("stuetze"),
    }


def _stern_blaetter(knoten):
    if not knoten["kinder"]:
        return 1
    return sum(_stern_blaetter(kind) for kind in knoten["kinder"])


def _stern_winkel(knoten, von, bis):
    knoten["winkel"] = (von + bis) / 2
    kinder = knoten["kinder"]
    if not kinder:
        return
    gewichte = [_stern_blaetter(kind) for kind in kinder]
    summe = sum(gewichte)
    cursor = von
    for kind, gewicht in zip(kinder, gewichte):
        breite = (bis - von) * gewicht / summe
        _stern_winkel(kind, cursor, cursor + breite)
        cursor += breite


def _stern_mindestlaenge(wurzel):
    werte = []

    def sammeln(knoten, ist_wurzel):
        if not ist_wurzel:
            werte.append(knoten["laenge"])
        for kind in knoten["kinder"]:
            sammeln(kind, False)

    sammeln(wurzel, True)
    positiv = [wert for wert in werte if wert > 1e-8]
    if not positiv:
        return
    mindest = 0.035 * max(positiv)
    def heben(knoten, ist_wurzel):
        if not ist_wurzel and knoten["laenge"] < mindest:
            knoten["laenge"] = mindest
        for kind in knoten["kinder"]:
            heben(kind, False)
    heben(wurzel, True)


def _stern_orte(knoten, x, y):
    knoten["x"] = x
    knoten["y"] = y
    for kind in knoten["kinder"]:
        _stern_orte(
            kind,
            x + kind["laenge"] * math.cos(kind["winkel"]),
            y + kind["laenge"] * math.sin(kind["winkel"]),
        )


def _stern_farbe(knoten, farbe_von):
    namen = []

    def sammeln(teil):
        if not teil["kinder"]:
            namen.append(teil["name"])
            return
        for kind in teil["kinder"]:
            sammeln(kind)

    sammeln(knoten)
    farben = {farbe_von(name) for name in namen if name}
    if len(farben) == 1:
        return next(iter(farben))
    return "#2c2c2c"


def _stern_zeichnen(wurzel, titel, untertitel, pfad, farbe_von, masstab):
    blaetter = []

    def sammeln(knoten):
        if not knoten["kinder"]:
            blaetter.append(knoten)
        for kind in knoten["kinder"]:
            sammeln(kind)

    sammeln(wurzel)
    laengster_pfad = _stern_pfad(wurzel)
    mass = (250.0 if len(blaetter) <= 8 else 340.0) / max(laengster_pfad, 1e-6)
    schrift = 15 if len(blaetter) <= 12 else 13

    def px(wert):
        return wert * mass

    for knoten in _stern_alle(wurzel):
        knoten["px"] = px(knoten["x"])
        knoten["py"] = px(knoten["y"])
        knoten["schub"] = 8.0

    def label_xy(blatt):
        return (
            blatt["px"] + blatt["schub"] * math.cos(blatt["winkel"]),
            blatt["py"] + blatt["schub"] * math.sin(blatt["winkel"]),
        )

    def anker(blatt):
        richtung = math.cos(blatt["winkel"])
        if richtung < -0.25:
            return "end"
        if richtung > 0.25:
            return "start"
        return "middle"

    def kasten(blatt):
        x, y = label_xy(blatt)
        breit = schrift * 0.58 * max(len(blatt["name"]), 1)
        hoch = schrift
        seite = anker(blatt)
        if seite == "end":
            links = x - breit
        elif seite == "start":
            links = x
        else:
            links = x - breit / 2
        return (links - 3, y - hoch * 0.72, breit + 6, hoch)

    def trifft(a, b):
        return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]

    for _ in range(24):
        kaesten = [kasten(blatt) for blatt in blaetter]
        bewegt = False
        for i, links in enumerate(kaesten):
            for rechts in kaesten[i + 1 :]:
                if trifft(links, rechts) and blaetter[i]["schub"] < 64:
                    blaetter[i]["schub"] += 6
                    bewegt = True
                    break
        if not bewegt:
            break

    punkte = []
    for knoten in _stern_alle(wurzel):
        punkte.append((knoten["px"], knoten["py"]))
    for blatt in blaetter:
        x, y = label_xy(blatt)
        box = kasten(blatt)
        punkte.append((box[0], box[1]))
        punkte.append((box[0] + box[2], box[1] + box[3]))
        punkte.append((x, y))
    minx = min(punkt[0] for punkt in punkte)
    maxx = max(punkt[0] for punkt in punkte)
    miny = min(punkt[1] for punkt in punkte)
    maxy = max(punkt[1] for punkt in punkte)
    zeilen_titel = _umbrueche(untertitel, 640)
    rand_x, oben = 36, 54 + 16 * len(zeilen_titel)
    unten = 48 if masstab else 28
    breite = max(int(maxx - minx + 2 * rand_x), _mindestbreite(rand_x, titel, zeilen_titel))
    hoehe = int(maxy - miny + oben + unten)

    def sx(x):
        return rand_x + (x - minx)

    def sy(y):
        return oben + (maxy - y)

    teile = _kopf(breite, hoehe, rand_x, titel, zeilen_titel, "#ffffff")

    def linie(eltern, kind):
        farbe = _stern_farbe(kind, farbe_von)
        teile.append(
            f'<line x1="{sx(eltern["px"]):.1f}" y1="{sy(eltern["py"]):.1f}" '
            f'x2="{sx(kind["px"]):.1f}" y2="{sy(kind["py"]):.1f}" '
            f'stroke="{farbe}" stroke-width="1.35" stroke-linecap="round"/>'
        )
        for enkel in kind["kinder"]:
            linie(kind, enkel)

    for kind in wurzel["kinder"]:
        linie(wurzel, kind)

    for knoten in _stern_alle(wurzel):
        if not knoten["kinder"] or knoten["stuetze"] is None or knoten["stuetze"] < KONSENS_MINIMUM:
            continue
        prozent = int(round(100 * knoten["stuetze"]))
        text = str(prozent)
        breit = 7 + 5.6 * len(text)
        x = sx(knoten["px"]) + 7 * math.cos(knoten["winkel"] + math.pi / 2)
        y = sy(knoten["py"]) - 7 * math.sin(knoten["winkel"] + math.pi / 2)
        teile.append(
            f'<rect x="{x - breit / 2:.1f}" y="{y - 7:.1f}" width="{breit:.1f}" height="13" rx="2" '
            f'fill="#2c2c2c"/>'
        )
        teile.append(
            f'<text x="{x:.1f}" y="{y + 3:.1f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
            f'font-size="9" fill="#ffffff">{text}</text>'
        )

    for blatt in blaetter:
        x, y = label_xy(blatt)
        farbe = farbe_von(blatt["name"])
        teile.append(
            f'<text x="{sx(x):.1f}" y="{sy(y):.1f}" text-anchor="{anker(blatt)}" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="{schrift}" fill="{farbe}" '
            f'stroke="#ffffff" stroke-width="3.5" paint-order="stroke fill">{xml(blatt["name"])}</text>'
        )

    if masstab:
        daten = 0.2
        balken = daten * mass
        x0, y0 = 28, hoehe - 22
        teile.append(
            f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0 + balken:.1f}" y2="{y0:.1f}" stroke="#2c2c2c" stroke-width="1.4"/>'
        )
        teile.append(
            f'<text x="{x0 + balken + 6:.1f}" y="{y0 + 4:.1f}" font-family="Helvetica, Arial, sans-serif" '
            f'font-size="11" fill="#4a4a4a">0,2 Gruppierungshöhe</text>'
        )
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")


def _stern_pfad(knoten):
    if not knoten["kinder"]:
        return 0.0
    return max(kind["laenge"] + _stern_pfad(kind) for kind in knoten["kinder"])


def _stern_alle(knoten):
    fund = [knoten]
    for kind in knoten["kinder"]:
        fund.extend(_stern_alle(kind))
    return fund


def _blaetter_von(knoten):
    if not knoten["kinder"]:
        return [knoten]
    fund = []
    for kind in knoten["kinder"]:
        fund.extend(_blaetter_von(kind))
    return fund


def _umbrueche(text, zielbreite):
    zeichen = max(36, int(zielbreite / 7.4))
    zeilen = []
    for absatz in text.split("\n"):
        rest = absatz.strip()
        while rest:
            if len(rest) <= zeichen:
                zeilen.append(rest)
                break
            bruch = rest.rfind(" ", 0, zeichen + 1)
            if bruch < 16:
                bruch = zeichen
            zeilen.append(rest[:bruch].rstrip())
            rest = rest[bruch:].lstrip()
    return zeilen


def _mindestbreite(links, titel, zeilen_titel):
    def px(text, groesse):
        return groesse * 0.55 * len(text)

    laengste = max([px(titel, 20)] + [px(zeile, 12.5) for zeile in zeilen_titel])
    return int(links + laengste + 36)


def _kopf(breite, hoehe, links, titel, zeilen_titel, grund=PAPIER):
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}" viewBox="0 0 {breite} {hoehe}">',
        f'<rect width="100%" height="100%" fill="{grund}"/>',
        f'<text x="{links}" y="28" font-family="Palatino, Georgia, serif" font-size="20" fill="{TINTE}">{xml(titel)}</text>',
    ]
    for nummer, zeile in enumerate(zeilen_titel):
        teile.append(
            f'<text x="{links}" y="{50 + 16 * nummer}" font-family="Palatino, Georgia, serif" font-size="12.5" fill="#6b645c">{xml(zeile)}</text>'
        )
    return teile


def _zahl(teile, x, y, anteil):
    prozent = int(round(100 * anteil))
    schrift = TINTE if anteil >= KONSENS_MINIMUM else "#a3988c"
    gewicht = "600" if anteil >= KONSENS_MINIMUM else "400"
    breit = 8 + 6.2 * len(str(prozent))
    teile.append(
        f'<rect x="{x:.1f}" y="{y - 10:.1f}" width="{breit:.1f}" height="13" rx="2" fill="{PAPIER}"/>'
    )
    teile.append(
        f'<text x="{x + 3:.1f}" y="{y:.1f}" font-family="Palatino, Georgia, serif" font-size="11" '
        f'font-weight="{gewicht}" fill="{schrift}">{prozent}</text>'
    )


def _achse(teile, x_wurzel, x_blatt, y, maximum):
    teile.append(
        f'<line x1="{x_wurzel:.1f}" y1="{y:.1f}" x2="{x_blatt:.1f}" y2="{y:.1f}" stroke="#b7ad9f" stroke-width="1"/>'
    )
    schritt = 0.2 if maximum <= 1.6 else 0.5
    wert = 0.0
    while wert <= maximum + 1e-9:
        x = x_blatt - (wert / maximum) * (x_blatt - x_wurzel)
        teile.append(
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y + 5:.1f}" stroke="#b7ad9f" stroke-width="1"/>'
        )
        teile.append(
            f'<text x="{x:.1f}" y="{y + 17:.1f}" text-anchor="middle" font-family="Palatino, Georgia, serif" '
            f'font-size="11" fill="#6b645c">{wert:.1f}</text>'
        )
        wert += schritt
    teile.append(
        f'<text x="{(x_wurzel + x_blatt) / 2:.1f}" y="{y + 32:.1f}" text-anchor="middle" '
        f'font-family="Palatino, Georgia, serif" font-size="11" fill="#6b645c">Gruppierungshöhe, Cosine Delta</text>'
    )


def knoten_x(knoten):
    werte = [knoten["x"]]
    for kind in knoten["kinder"]:
        werte.append(knoten_x(kind))
    return max(werte)


def bootstrap_baeume(matrizen, eich_zeilen, rng):
    """matrizen: Liste von (n, f), alle dieselbe Spaltenzahl. eich_zeilen wählt die Zeilen der Normierung aus der ersten Matrix."""
    spalten = matrizen[0].shape[1]
    baeume = []
    for _ in range(BOOTSTRAP):
        maske = rng.random(spalten) < MERKMALANTEIL
        if int(maske.sum()) < 8:
            continue
        teile = [matrix[:, maske] for matrix in matrizen]
        gemeinsam = np.vstack(teile)
        eichung = teile[0][eich_zeilen]
        abstand = kosinus(gemeinsam, eichung)
        if abstand is None:
            continue
        wurzel = upgma(abstand)
        baeume.append(kladen(wurzel))
    if len(baeume) < BOOTSTRAP * 0.9:
        raise SystemExit("Zu viele Bootstrap-Ziehungen ohne Streuung")
    return baeume


def schreibe_kladen(pfad, zeilen):
    with pfad.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["abbildung", "klade", "anteil"])
        writer.writeheader()
        writer.writerows(zeilen)


def svg_abstaende(pfad, abstand_csv, auc):
    gleich, verschieden = [], []
    for zeile in csv.DictReader(abstand_csv.open(encoding="utf-8")):
        wert = float(zeile["abstand"])
        if zeile["paar"] == "gleich":
            gleich.append(wert)
        else:
            verschieden.append(wert)
    breite, hoehe = 720, 250
    links, rechts = 150, 30

    def x(wert):
        return links + min(max(wert, 0.0), 2.0) / 2.0 * (breite - links - rechts)

    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}">',
        '<rect width="100%" height="100%" fill="#fbfbfa"/>',
        '<text x="28" y="28" font-family="Georgia, serif" font-size="16" fill="#222">Cosine Delta der Eichproben</text>',
        f'<text x="28" y="48" font-family="sans-serif" font-size="12" fill="#555">150 häufigste Wörter, AUC {auc:.2f}. Kleinere Werte sind näher.</text>',
        '<text x="28" y="100" font-family="sans-serif" font-size="13" fill="#1f4e79">gleicher Verfasser</text>',
        '<text x="28" y="170" font-family="sans-serif" font-size="13" fill="#8c3a2f">Heine gegen Schilda</text>',
    ]
    for wert in gleich:
        teile.append(f'<circle cx="{x(wert):.1f}" cy="108" r="3" fill="#1f4e79" opacity="0.35"/>')
    for wert in verschieden:
        teile.append(f'<circle cx="{x(wert):.1f}" cy="178" r="3" fill="#8c3a2f" opacity="0.35"/>')
    for wert, y, farbe in (
        (float(np.median(gleich)), 108, "#1f4e79"),
        (float(np.median(verschieden)), 178, "#8c3a2f"),
    ):
        teile.append(
            f'<line x1="{x(wert):.1f}" y1="{y - 16}" x2="{x(wert):.1f}" y2="{y + 16}" stroke="{farbe}" stroke-width="2"/>'
        )
    teile.append(
        f'<text x="{links}" y="230" font-family="sans-serif" font-size="12" fill="#555">'
        f'Median gleich {np.median(gleich):.2f}, Median verschieden {np.median(verschieden):.2f}. Die Striche sind die Mediane.</text>'
    )
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")


def svg_impostors(pfad, loo_csv, ergebnis):
    zeilen = list(csv.DictReader(loo_csv.open(encoding="utf-8")))
    breite, hoehe = 760, 430
    links = 170
    felder = [
        ("woerter", "Wörter", 70),
        ("zeichen", "Zeichen-4-Gramme", 250),
    ]
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}">',
        '<rect width="100%" height="100%" fill="#fbfbfa"/>',
        '<text x="28" y="28" font-family="Georgia, serif" font-size="16" fill="#222">Impostors-Anteile</text>',
        '<text x="28" y="48" font-family="sans-serif" font-size="12" fill="#555">Punkte sind bekannte Proben. Rauten sind der Kandidat. Das graue Band ist die Zone ohne Antwort.</text>',
    ]

    def x(wert):
        return links + wert * 540

    for merkmal, titel, y0 in felder:
        schwelle = ergebnis[{"woerter": "woerter_schwelle", "zeichen": "zeichen_schwelle"}[merkmal]]
        teile.append(f'<text x="28" y="{y0 - 16}" font-family="sans-serif" font-size="14" fill="#222">{xml(titel)}</text>')
        teile.append(
            f'<rect x="{x(schwelle - p.ANTWORT_BAND):.1f}" y="{y0 - 8}" '
            f'width="{x(schwelle + p.ANTWORT_BAND) - x(schwelle - p.ANTWORT_BAND):.1f}" height="108" fill="#000" opacity="0.06"/>'
        )
        teile.append(
            f'<line x1="{x(schwelle):.1f}" y1="{y0 - 8}" x2="{x(schwelle):.1f}" y2="{y0 + 100}" stroke="#333" stroke-dasharray="3 3"/>'
        )
        gruppen = (("eigene Herkunft", True, y0 + 24), ("fremde Herkunft", False, y0 + 72))
        for name, eigene, y in gruppen:
            teile.append(f'<text x="28" y="{y + 4}" font-family="sans-serif" font-size="12" fill="#555">{name}</text>')
            werte = [
                float(zeile["anteil"])
                for zeile in zeilen
                if zeile["merkmal"] == merkmal and ((zeile["herkunft"] == zeile["ziel"]) == eigene)
            ]
            for nummer, wert in enumerate(werte):
                versatz = ((nummer % 7) - 3) * 2.2
                teile.append(f'<circle cx="{x(wert):.1f}" cy="{y + versatz:.1f}" r="2.4" fill="#1f4e79" opacity="0.45"/>')
        for ziel, y, farbe in (("heine", y0 + 24, FARBE["heine"]), ("hektor", y0 + 72, FARBE["hektor"])):
            schluessel = f"{merkmal}_anteil_{ziel}"
            wert = ergebnis[schluessel]
            teile.append(
                f'<polygon points="{x(wert):.1f},{y - 7} {x(wert) + 7:.1f},{y} {x(wert):.1f},{y + 7} {x(wert) - 7:.1f},{y}" fill="{farbe}"/>'
            )
    teile.append(
        '<text x="28" y="410" font-family="sans-serif" font-size="12" fill="#555">'
        "Die Raute auf „eigene Herkunft“ ist der Heine-Anteil des Kandidaten, die andere der Schilda-Anteil. "
        "Die gestrichelte Linie ist die Schwelle aus den bekannten Proben.</text>"
    )
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")


def svg_profile(pfad, distanz, reihe):
    werte = [distanz[name] for name in reihe]
    breite, hoehe = 680, 280
    links, oben = 120, 70
    maximale = max(werte) * 1.08
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}">',
        '<rect width="100%" height="100%" fill="#fbfbfa"/>',
        '<text x="28" y="28" font-family="Georgia, serif" font-size="16" fill="#222">Abstand des Kandidaten von den Profilen</text>',
        '<text x="28" y="48" font-family="sans-serif" font-size="12" fill="#555">Cosine Delta der 150 häufigsten Wörter. Ein kürzerer Balken ist näher.</text>',
    ]
    for nummer, name in enumerate(reihe):
        y = oben + nummer * 30
        laenge = werte[nummer] / maximale * 460
        teile.append(f'<text x="28" y="{y + 14}" font-family="sans-serif" font-size="13" fill="{FARBE[name]}">{KLASSENNAME[name]}</text>')
        teile.append(f'<rect x="{links}" y="{y}" width="{laenge:.1f}" height="18" fill="{FARBE[name]}" opacity="0.85"/>')
        teile.append(
            f'<text x="{links + laenge + 8:.1f}" y="{y + 14}" font-family="sans-serif" font-size="12" fill="#333">{werte[nummer]:.2f}</text>'
        )
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")


def svg_waerme(pfad, abstand_csv):
    matrix = np.zeros((22, 22))
    for zeile in csv.DictReader(abstand_csv.open(encoding="utf-8")):
        i, j = int(zeile["i"]), int(zeile["j"])
        wert = float(zeile["abstand"])
        matrix[i, j] = matrix[j, i] = wert
    werte = matrix[np.triu_indices(22, 1)]
    vmin, vmax = float(werte.min()), float(werte.max())
    zelle = 18
    links, oben = 78, 78
    breite = links + 22 * zelle + 36
    hoehe = oben + 22 * zelle + 28
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}">',
        '<rect width="100%" height="100%" fill="#fbfbfa"/>',
        '<text x="28" y="28" font-family="Georgia, serif" font-size="16" fill="#222">Wortabstände der 22 Eichproben</text>',
        '<text x="28" y="48" font-family="sans-serif" font-size="12" fill="#555">Hell ist nah, dunkel ist fern. Oben links Heine, unten rechts Schilda.</text>',
    ]
    etiketten = [f"H{i}" for i in range(1, 12)] + [f"K{i}" for i in range(1, 12)]
    for i, name in enumerate(etiketten):
        teile.append(
            f'<text x="{links + i * zelle + 4}" y="{oben - 8}" font-family="sans-serif" font-size="9" fill="#444">{name}</text>'
        )
        teile.append(
            f'<text x="{links - 22}" y="{oben + i * zelle + 12}" font-family="sans-serif" font-size="9" fill="#444">{name}</text>'
        )
    for i in range(22):
        for j in range(22):
            t = 0.0 if i == j else (matrix[i, j] - vmin) / (vmax - vmin)
            rot = int(255 - t * 210)
            gruen = int(247 - t * 180)
            blau = int(236 - t * 140)
            teile.append(
                f'<rect x="{links + j * zelle}" y="{oben + i * zelle}" width="{zelle - 1}" height="{zelle - 1}" '
                f'fill="rgb({rot},{gruen},{blau})"/>'
            )
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")


def html_uebersicht(ordner, bilder):
    bloecke = []
    for datei, unterschrift in bilder:
        bloecke.append(
            "<figure>"
            f'<img src="{html.escape(datei)}" alt="{html.escape(unterschrift)}">'
            f"<figcaption>{html.escape(unterschrift)}</figcaption>"
            "</figure>"
        )
    name = html.escape(p.STUDIE_NAME)
    text = f"""<!DOCTYPE html>
<html lang="de">
<meta charset="utf-8">
<title>{name}, Abbildungen</title>
<style>
body {{ font-family: Georgia, serif; max-width: 980px; margin: 32px auto; color: #222; background: #fbfbfa; }}
figcaption {{ font-family: sans-serif; font-size: 14px; color: #333; margin: 8px 0 28px; }}
img {{ max-width: 100%; height: auto; border: 1px solid #e4e0d8; }}
</style>
<h1>{name}, Abbildungen</h1>
<p>Die Bilder lesen die gerechnete Studie. Sie ändern den Ausgang in ENTSCHEIDUNG.md nicht.</p>
""" + "\n".join(bloecke) + "\n</html>\n"
    (ordner / "abb_uebersicht.html").write_text(text, encoding="utf-8")


def selbsttest():
    block = np.array(
        [
            [0.0, 0.1, 0.9, 0.9],
            [0.1, 0.0, 0.8, 0.8],
            [0.9, 0.8, 0.0, 0.1],
            [0.9, 0.8, 0.1, 0.0],
        ]
    )
    wurzel = upgma(block)
    gruppen = [klade for klade in kladen(wurzel) if len(klade) == 2]
    if frozenset([0, 1]) not in gruppen or frozenset([2, 3]) not in gruppen:
        raise SystemExit("Selbsttest UPGMA fehlgeschlagen")

    def finde(knoten, ziel):
        if knoten["blaetter"] == ziel and knoten["kinder"] is not None:
            return knoten
        if knoten["kinder"] is None:
            return None
        return finde(knoten["kinder"][0], ziel) or finde(knoten["kinder"][1], ziel)

    paar = finde(wurzel, frozenset([0, 1]))
    if paar is None or abs(paar["hoehe"] - 0.1) > 1e-9:
        raise SystemExit("Selbsttest UPGMA-Höhe fehlgeschlagen")


def main():
    selbsttest()
    if not p.LAUF.is_dir():
        raise SystemExit("Laufordner fehlt. Zuerst 00_lauf.py ausführen.")
    teilung = g.lese_json(p.LAUF / "teilung.json")
    proben = g.proben_primaer(teilung)
    eichproben = proben["heine"] + proben["hektor"]
    kandidat = g.lade_text(g.eintraege("kandidat")[0])
    profil_reihenfolge = ["heine", "hektor"] + list(teilung["primaer"]["ablenker"])
    rng = np.random.default_rng(np.random.SeedSequence([p.SEED, 8]))

    merkmale300 = g.merkmal_woerter(eichproben, 300)
    wort_eich = {anzahl: g.matrix_woerter(eichproben, merkmale300[:anzahl]) for anzahl in (100, 150, 300)}
    wort_profil = {}
    wort_kandidat = {}
    for anzahl in (100, 150, 300):
        je_klasse = [g.matrix_woerter(proben[name], merkmale300[:anzahl]) for name in profil_reihenfolge]
        wort_profil[anzahl] = np.vstack([matrix.mean(axis=0) for matrix in je_klasse])
        wort_kandidat[anzahl] = g.matrix_woerter([kandidat], merkmale300[:anzahl])

    etiketten_eich = [f"Heine {i}" for i in range(1, 12)] + [f"Schilda {i}" for i in range(1, 12)]
    etiketten_profil = [KLASSENNAME[name] for name in profil_reihenfolge] + ["Kandidat"]
    eich_zeilen = np.arange(len(eichproben))

    prim = kosinus(wort_eich[150], wort_eich[150])
    referenz_eich = blattordnung(upgma(prim))
    baeume_eich = bootstrap_baeume([wort_eich[150]], eich_zeilen, rng)
    gewaehlt_eich, _ = mehrheit(baeume_eich, len(etiketten_eich))
    heine_ganz = sum(frozenset(range(11)) in baum for baum in baeume_eich) / len(baeume_eich)
    hektor_ganz = sum(frozenset(range(11, 22)) in baum for baum in baeume_eich) / len(baeume_eich)
    svg_baum(
        baum_aus_kladen(gewaehlt_eich, etiketten_eich, referenz_eich),
        "Konsens der Eichproben",
        (
            f"{len(baeume_eich)} Bäume, 150 Wörter. Gezeichnet sind nur Äste ab 50%.\n"
            f"Heine als ganze Gruppe steht in {heine_ganz:.0%} der Bäume, Schilda in {hektor_ganz:.0%}."
        ),
        p.LAUF / "abb_konsens_eichung.svg",
    )
    svg_dendrogramm(
        upgma(prim),
        etiketten_eich,
        anteile_der_kladen(baeume_eich),
        "Dendrogramm der Eichproben",
        (
            "UPGMA auf dem Cosine Delta der 150 Wörter. Die Zahl ist der Anteil der 500 Bäume in Prozent.\n"
            "Waagerecht die Gruppierungshöhe. Eine hellere Zahl liegt unter 50 Prozent."
        ),
        p.LAUF / "abb_dendrogramm_eichung.svg",
    )
    svg_stern(
        baum_aus_kladen(gewaehlt_eich, etiketten_eich, referenz_eich),
        etiketten_eich,
        None,
        "Eichproben, sternförmig",
        "Mehrheitskonsens. Gleiche Astlänge, keine Distanz. Nur Gruppen ab 50 Prozent.",
        p.LAUF / "abb_stern_konsens_eichung.svg",
        art="gleich",
    )
    svg_stern(
        upgma(prim),
        etiketten_eich,
        anteile_der_kladen(baeume_eich),
        "Eichproben, sternförmig nach der Gruppierungshöhe",
        "Die Mitte ist die letzte UPGMA-Gruppe. Die Astlänge ist die Gruppierungshöhe. Zahlen ab 50.",
        p.LAUF / "abb_stern_eichung.svg",
    )

    profil_zeilen = np.vstack([wort_profil[150], wort_kandidat[150]])
    eichung150 = wort_eich[150]
    prim_profil = kosinus(profil_zeilen, eichung150)
    referenz_profil = blattordnung(upgma(prim_profil))
    baeume_profil = []
    spalten = wort_profil[150].shape[1]
    for _ in range(BOOTSTRAP):
        maske = rng.random(spalten) < MERKMALANTEIL
        if int(maske.sum()) < 8:
            continue
        zeilen = np.vstack([wort_profil[150][:, maske], wort_kandidat[150][:, maske]])
        abstand = kosinus(zeilen, eichung150[:, maske])
        if abstand is None:
            continue
        baeume_profil.append(kladen(upgma(abstand)))
    gewaehlt_profil, _ = mehrheit(baeume_profil, len(etiketten_profil))
    svg_baum(
        baum_aus_kladen(gewaehlt_profil, etiketten_profil, referenz_profil),
        "Konsens der Profile und des Kandidaten",
        f"Merkmal-Bootstrap, {len(baeume_profil)} Bäume, 150 Wörter. Die Normierung stammt aus den Eichproben.",
        p.LAUF / "abb_konsens_profile.svg",
    )
    svg_dendrogramm(
        upgma(prim_profil),
        etiketten_profil,
        anteile_der_kladen(baeume_profil),
        "Dendrogramm der Profile und des Kandidaten",
        (
            "UPGMA, 150 Wörter. Die Zahl ist der Anteil der Bootstrap-Bäume in Prozent.\n"
            "Waagerecht die Gruppierungshöhe. Eine hellere Zahl liegt unter 50 Prozent."
        ),
        p.LAUF / "abb_dendrogramm_profile.svg",
    )
    svg_stern(
        baum_aus_kladen(gewaehlt_profil, etiketten_profil, referenz_profil),
        etiketten_profil,
        None,
        "Profile und Kandidat, sternförmig",
        "Mehrheitskonsens. Gleiche Astlänge, keine Distanz. Nur Gruppen ab 50 Prozent.",
        p.LAUF / "abb_stern_konsens_profile.svg",
        art="gleich",
    )
    svg_stern(
        upgma(prim_profil),
        etiketten_profil,
        anteile_der_kladen(baeume_profil),
        "Profile und Kandidat, sternförmig nach der Gruppierungshöhe",
        "Die Mitte ist die letzte UPGMA-Gruppe. Die Astlänge ist die Gruppierungshöhe. Zahlen ab 50.",
        p.LAUF / "abb_stern_profile.svg",
    )

    merkmale_z = g.merkmal_ngramme(eichproben, p.ZEICHEN_N, p.ZEICHEN_HAEUFIGSTE)
    zeichen_eich = g.matrix_ngramme(eichproben, merkmale_z, p.ZEICHEN_N)
    zeichen_profil = np.vstack(
        [g.matrix_ngramme(proben[name], merkmale_z, p.ZEICHEN_N).mean(axis=0) for name in profil_reihenfolge]
    )
    zeichen_kandidat = g.matrix_ngramme([kandidat], merkmale_z, p.ZEICHEN_N)
    prim_z = kosinus(np.vstack([zeichen_profil, zeichen_kandidat]), zeichen_eich)
    referenz_z = blattordnung(upgma(prim_z))
    baeume_z = []
    spalten_z = zeichen_profil.shape[1]
    for _ in range(BOOTSTRAP):
        maske = rng.random(spalten_z) < MERKMALANTEIL
        if int(maske.sum()) < 8:
            continue
        zeilen = np.vstack([zeichen_profil[:, maske], zeichen_kandidat[:, maske]])
        abstand = kosinus(zeilen, zeichen_eich[:, maske])
        if abstand is None:
            continue
        baeume_z.append(kladen(upgma(abstand)))
    gewaehlt_z, _ = mehrheit(baeume_z, len(etiketten_profil))
    svg_baum(
        baum_aus_kladen(gewaehlt_z, etiketten_profil, referenz_z),
        "Konsens nach Zeichen-4-Grammen",
        f"Merkmal-Bootstrap, {len(baeume_z)} Bäume, 500 häufigste 4-Gramme, Profile und Kandidat.",
        p.LAUF / "abb_konsens_zeichen.svg",
    )
    svg_dendrogramm(
        upgma(prim_z),
        etiketten_profil,
        anteile_der_kladen(baeume_z),
        "Dendrogramm nach Zeichen-4-Grammen",
        (
            "UPGMA, 500 häufigste 4-Gramme. Die Zahl ist der Anteil der Bootstrap-Bäume in Prozent.\n"
            "Waagerecht die Gruppierungshöhe. Eine hellere Zahl liegt unter 50 Prozent."
        ),
        p.LAUF / "abb_dendrogramm_zeichen.svg",
    )
    svg_stern(
        baum_aus_kladen(gewaehlt_z, etiketten_profil, referenz_z),
        etiketten_profil,
        None,
        "Zeichen-4-Gramme, sternförmig",
        "Mehrheitskonsens. Gleiche Astlänge, keine Distanz. Nur Gruppen ab 50 Prozent.",
        p.LAUF / "abb_stern_konsens_zeichen.svg",
        art="gleich",
    )
    svg_stern(
        upgma(prim_z),
        etiketten_profil,
        anteile_der_kladen(baeume_z),
        "Zeichen-4-Gramme, sternförmig nach der Gruppierungshöhe",
        "Die Mitte ist die letzte UPGMA-Gruppe. Die Astlänge ist die Gruppierungshöhe. Zahlen ab 50.",
        p.LAUF / "abb_stern_zeichen.svg",
    )

    leiter = []
    for anzahl in (100, 150, 300):
        zeilen = np.vstack([wort_profil[anzahl], wort_kandidat[anzahl]])
        abstand = kosinus(zeilen, wort_eich[anzahl])
        leiter.append(kladen(upgma(abstand)))
    gewaehlt_leiter, _ = mehrheit(leiter, len(etiketten_profil))
    svg_baum(
        baum_aus_kladen(gewaehlt_leiter, etiketten_profil, referenz_profil),
        "Konsens über die Merkmalleiter",
        "Drei Bäume, für 100, 150 und 300 häufigste Wörter. Eine Zahl 100 heißt: der Ast steht in allen drei.",
        p.LAUF / "abb_konsens_mfw.svg",
    )
    zeilen_mfw = np.vstack([wort_profil[150], wort_kandidat[150]])
    svg_dendrogramm(
        upgma(kosinus(zeilen_mfw, wort_eich[150])),
        etiketten_profil,
        anteile_der_kladen(leiter),
        "Dendrogramm der Merkmalleiter",
        "UPGMA der 150 Wörter. Die Zahl ist der Anteil der drei Merkmalzahlen in Prozent. 100 heißt: die Gruppe steht bei 100, 150 und 300.",
        p.LAUF / "abb_dendrogramm_mfw.svg",
    )
    svg_stern(
        baum_aus_kladen(gewaehlt_leiter, etiketten_profil, referenz_profil),
        etiketten_profil,
        None,
        "Merkmalleiter, sternförmig",
        "Mehrheitskonsens der drei Merkmalzahlen. Gleiche Astlänge, keine Distanz.",
        p.LAUF / "abb_stern_konsens_mfw.svg",
        art="gleich",
    )
    svg_stern(
        upgma(kosinus(zeilen_mfw, wort_eich[150])),
        etiketten_profil,
        anteile_der_kladen(leiter),
        "Merkmalleiter, sternförmig nach der Gruppierungshöhe",
        "UPGMA der 150 Wörter. Die Zahl ist der Anteil der drei Merkmalzahlen. 100 heißt: die Gruppe steht bei 100, 150 und 300.",
        p.LAUF / "abb_stern_mfw.svg",
    )

    kladen_csv = []
    for abbildung, gewaehlt, etiketten in (
        ("eichung_woerter", gewaehlt_eich, etiketten_eich),
        ("profile_woerter", gewaehlt_profil, etiketten_profil),
        ("profile_zeichen", gewaehlt_z, etiketten_profil),
        ("profile_mfw", gewaehlt_leiter, etiketten_profil),
    ):
        for klade, anteil in gewaehlt:
            namen = ", ".join(etiketten[i] for i in sorted(klade))
            kladen_csv.append({"abbildung": abbildung, "klade": namen, "anteil": f"{anteil:.4f}"})
    schreibe_kladen(p.LAUF / "08_konsens_kladen.csv", kladen_csv)

    woerter_json = g.lese_json(p.LAUF / "02_woerter.json")
    svg_abstaende(p.LAUF / "abb_abstaende.svg", p.LAUF / "02_woerter_abstaende.csv", woerter_json["primaer"]["auc"])
    svg_impostors(p.LAUF / "abb_impostors.svg", p.LAUF / "06_impostors_loo.csv", g.lese_json(p.LAUF / "06_impostors.json"))
    svg_profile(
        p.LAUF / "abb_profile.svg",
        g.lese_json(p.LAUF / "06_impostors.json")["cosine_delta_profile"],
        profil_reihenfolge,
    )
    svg_waerme(p.LAUF / "abb_waerme.svg", p.LAUF / "02_woerter_abstaende.csv")
    html_uebersicht(
        p.LAUF,
        [
            (
                "abb_stern_profile.svg",
                "Sternförmiger UPGMA-Baum der Profile und des Kandidaten. Die Mitte ist die letzte Gruppe, die Astlänge die Gruppierungshöhe.",
            ),
            (
                "abb_stern_zeichen.svg",
                "Derselbe sternförmige Baum für die Zeichen-4-Gramme.",
            ),
            (
                "abb_stern_mfw.svg",
                "Sternförmiger Baum der 150 häufigsten Wörter. Die Zahl sagt, in wie viel Prozent der drei Merkmalzahlen die Gruppe steht.",
            ),
            (
                "abb_stern_eichung.svg",
                "Sternförmiger Baum der 22 Eichproben. Enge Gabeln sind frühe Gruppierungen.",
            ),
            (
                "abb_stern_konsens_profile.svg",
                "Dieselbe Mehrheit als Stern. Die Astlänge ist hier keine Distanz.",
            ),
            (
                "abb_stern_konsens_zeichen.svg",
                "Mehrheitsstern der Zeichen-4-Gramme.",
            ),
            (
                "abb_stern_konsens_mfw.svg",
                "Mehrheitsstern über 100, 150 und 300 häufigste Wörter.",
            ),
            (
                "abb_stern_konsens_eichung.svg",
                "Mehrheitsstern der 22 Eichproben. Ungelöste Proben stoßen in der Mitte zusammen.",
            ),
            (
                "abb_dendrogramm_profile.svg",
                "Dendrogramm der Profile und des Kandidaten. Die waagerechte Achse ist die Gruppierungshöhe.",
            ),
            (
                "abb_dendrogramm_zeichen.svg",
                "Dasselbe Dendrogramm für die Zeichen-4-Gramme.",
            ),
            (
                "abb_dendrogramm_mfw.svg",
                "Dendrogramm der 150 häufigsten Wörter. Die Zahl sagt, in wie viel Prozent der drei Merkmalzahlen die Gruppe steht.",
            ),
            (
                "abb_dendrogramm_eichung.svg",
                "Dendrogramm der 22 Eichproben. Die Länge eines Astes ist die Gruppierungshöhe, nicht eine Zeit.",
            ),
            ("abb_konsens_profile.svg", "Mehrheitskonsens aus 500 Merkmal-Bootstraps. Gezeichnet sind nur Gruppen ab 50 Prozent."),
            ("abb_konsens_zeichen.svg", "Derselbe Mehrheitskonsens für die Zeichen-4-Gramme."),
            ("abb_konsens_mfw.svg", "Mehrheitskonsens über 100, 150 und 300 häufigste Wörter."),
            (
                "abb_konsens_eichung.svg",
                "Konsens der 22 Eichproben. Stabile Äste sind kleine Paare. Die beiden Verfasser bilden unter dem Merkmal-Bootstrap keine geschlossene Gruppe.",
            ),
            ("abb_abstaende.svg", "Einzelabstände der Eichung. Die Gruppen sollten auseinanderliegen."),
            ("abb_waerme.svg", "Dieselben Abstände als Wärmebild."),
            ("abb_impostors.svg", "Impostors-Anteile der bekannten Proben und des Kandidaten."),
            ("abb_profile.svg", "Abstand des Kandidaten von jedem Profil."),
        ],
    )
    print(f"Konsens Eichproben: {len(gewaehlt_eich)} Kladen")
    print(f"Konsens Profile: {len(gewaehlt_profil)} Kladen")
    print("Abbildungen geschrieben nach", p.LAUF)


if __name__ == "__main__":
    main()
