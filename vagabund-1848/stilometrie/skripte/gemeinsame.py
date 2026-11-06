# -*- coding: utf-8 -*-
"""Gemeinsame Rechenwege der Studie 1.

Dieses Modul wird von den nummerierten Skripten eingebunden.
Es liest die Dateiliste, schneidet Proben, rechnet Cosine Delta,
die AUC und die Impostors-Anteile.

Ein Wort der Probenlänge ist eine durch Leerraum getrennte Zeichenfolge.
Für die Worthäufigkeiten wird daraus ein Buchstabenwort: Kleinbuchstaben,
mit Apostroph und Bindestrich, die am Wort hängen. Satzzeichen fallen
dort weg. Die Interpunktion wird in einer eigenen Zählung erfasst.
Der Apostroph wird dort zusätzlich gezählt, auch wenn er im Wortbild
stehen bleibt. Die beiden Zählungen werden nicht zu einem Modell
zusammengelegt.

Cosine Delta folgt Smith und Aldridge sowie Evert und anderen:
relative Häufigkeit, Standardwerte über die Proben
(Standardabweichung mit Teilung durch n - 1), Kosinusabstand
1 minus Kosinusähnlichkeit.

Die Impostors-Methode folgt Koppel und Winter sowie Kestemont
und anderen. Der Abstand darin ist der Ružička-Abstand
(1 minus Summe der Minima geteilt durch Summe der Maxima),
gerechnet auf nicht-negativen relativen Häufigkeiten.
"""

import csv
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

from laufwahl import parameter as p

BUCHSTABE = re.compile(r"[^\W\d_]", re.UNICODE)
UEBERSCHRIFT = re.compile(r"^[IVXLCDM]+\.$")

INTERPUNKTION = (
    ("komma", ",，"),
    ("punkt", "."),
    ("frage", "?"),
    ("ausrufe", "!"),
    ("apostroph", "'’"),
    ("semikolon", ";"),
    ("doppelpunkt", ":"),
    ("gedankenstrich", "—–"),
    ("anfuehrung_auf", "„«"),
    ("anfuehrung_zu", "“”»\""),
    ("auslassung", "…"),
)
INTERPUNKT_ZEICHEN = {zeichen for _, gruppe in INTERPUNKTION for zeichen in gruppe}


def dateiliste():
    zeilen = []
    with p.DATEILISTE.open(encoding="utf-8", newline="") as handle:
        for zeile in csv.DictReader(handle):
            zeile["wortzahl"] = int(zeile["wortzahl"])
            zeile["reihenfolge"] = int(zeile["reihenfolge"])
            zeilen.append(zeile)
    return zeilen


def pfad_zu(eintrag):
    return p.PROJEKT / eintrag["pfad"]


def pruefsumme(pfad):
    digest = hashlib.sha256()
    with Path(pfad).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 16), b""):
            digest.update(block)
    return digest.hexdigest()


def leerzeichen_woerter(text):
    return unicodedata.normalize("NFC", text).split()


def lade_text(eintrag):
    pfad = pfad_zu(eintrag)
    if not pfad.is_file():
        raise SystemExit("Datei fehlt: " + eintrag["pfad"])
    woerter = leerzeichen_woerter(pfad.read_text(encoding="utf-8"))
    if len(woerter) != eintrag["wortzahl"]:
        raise SystemExit(
            f"Wortzahl weicht ab: {eintrag['pfad']} hat {len(woerter)}, "
            f"die Dateiliste erwartet {eintrag['wortzahl']}"
        )
    return woerter


def eintraege(rolle):
    zeilen = [zeile for zeile in dateiliste() if zeile["rolle"] == rolle]
    return sorted(zeilen, key=lambda zeile: zeile["reihenfolge"])


def wortstrom(rolle):
    """Hängt die Dateien einer Rolle in der festgelegten Reihenfolge aneinander."""
    if rolle == "kandidat":
        raise SystemExit("Der Kandidat wird nicht als Eichstrom gelesen")
    strom = []
    herkunft = []
    for eintrag in eintraege(rolle):
        woerter = lade_text(eintrag)
        strom.extend(woerter)
        herkunft.append(eintrag["pfad"])
    return strom, herkunft


def proben_aus(woerter, starten):
    laenge = p.PROBENLAENGE
    return [woerter[start : start + laenge] for start in starten]


def proben_primaer(teilung):
    """Baut die Primärproben aus den gespeicherten Anfangsstellen neu."""
    heine, _ = wortstrom("heine")
    hektor, _ = wortstrom("hektor")
    k = teilung["k"]
    proben = {
        "heine": proben_aus(heine, teilung["primaer"]["heine"]["starts"][:k]),
        "hektor": proben_aus(hektor, teilung["primaer"]["hektor"]["starts"][:k]),
    }
    nach_pfad = {zeile["pfad"]: zeile for zeile in dateiliste()}
    for name, block in teilung["primaer"]["ablenker"].items():
        woerter = lade_text(nach_pfad[block["pfad"]])
        proben[name] = proben_aus(woerter, block["starts"])
    return proben


def generatoren():
    folge = np.random.SeedSequence(p.SEED)
    teilung, impostors, verse = folge.spawn(3)
    return (
        np.random.default_rng(teilung),
        np.random.default_rng(impostors),
        np.random.default_rng(verse),
    )


def ziehe_versatz(n_woerter, rng):
    rest = n_woerter % p.PROBENLAENGE
    return int(rng.integers(0, rest + 1))


def schnitte_ab(woerter, versatz):
    laenge = p.PROBENLAENGE
    starten = list(range(versatz, len(woerter) - laenge + 1, laenge))
    return starten, [woerter[start : start + laenge] for start in starten]


def spreiz_schnitte(woerter, anzahl):
    """Nicht überlappende Proben, über den Text verteilt, ohne Zufallszahl."""
    laenge = p.PROBENLAENGE
    kacheln = []
    for start in range(0, len(woerter) - laenge + 1, laenge):
        kacheln.append((start, woerter[start : start + laenge]))
    if len(kacheln) <= anzahl:
        return kacheln
    zeiger = [
        int(round(i * (len(kacheln) - 1) / (anzahl - 1))) for i in range(anzahl)
    ]
    gewaehlt = []
    for nummer in zeiger:
        if nummer not in gewaehlt:
            gewaehlt.append(nummer)
    return [kacheln[nummer] for nummer in gewaehlt]


def buchstabenwort(token):
    roh = token.lower().replace("’", "'")
    zeichen = [ch for ch in roh if ch.isalpha() or ch in "'-"]
    wort = "".join(zeichen).strip("'-")
    if not wort or not any(ch.isalpha() for ch in wort):
        return None
    return wort


def buchstabenwoerter(probe):
    return [wort for token in probe if (wort := buchstabenwort(token))]


def rel_haeufigkeit(zaehlung, merkmale, nenner):
    if nenner <= 0:
        raise SystemExit("Nenner der relativen Häufigkeit ist 0")
    return np.array([zaehlung[merkmal] / nenner for merkmal in merkmale], dtype=float)


def haeufigste(zaehlungen, anzahl):
    geordnet = sorted(zaehlungen.items(), key=lambda paar: (-paar[1], paar[0]))
    if len(geordnet) < anzahl:
        raise SystemExit(f"Nur {len(geordnet)} Merkmale, verlangt sind {anzahl}")
    return [merkmal for merkmal, _ in geordnet[:anzahl]]


def kosinus_delta(relativ):
    """Kosinusabstand der Standardwerte. Spalten ohne Streuung fallen weg."""
    mittel = relativ.mean(axis=0)
    streuung = relativ.std(axis=0, ddof=p.STANDARDABWEICHUNG_DDOF)
    behalten = streuung > 0
    if not np.any(behalten):
        raise SystemExit("Cosine Delta: keine Merkmalspalte mit Streuung")
    standard = (relativ[:, behalten] - mittel[behalten]) / streuung[behalten]
    normen = np.linalg.norm(standard, axis=1, keepdims=True)
    if np.any(normen == 0):
        raise SystemExit("Cosine Delta: eine Probe hat nach der Normierung die Länge 0")
    aehnlichkeit = (standard @ standard.T) / (normen @ normen.T)
    aehnlichkeit = np.clip(aehnlichkeit, -1.0, 1.0)
    abstand = 1.0 - aehnlichkeit
    np.fill_diagonal(abstand, 0.0)
    return abstand, behalten


def paare(abstand, klassen, nur_klassen):
    gleich = []
    verschieden = []
    n = len(klassen)
    for i in range(n):
        if klassen[i] not in nur_klassen:
            continue
        for j in range(i + 1, n):
            if klassen[j] not in nur_klassen:
                continue
            wert = float(abstand[i, j])
            if klassen[i] == klassen[j]:
                gleich.append(wert)
            else:
                verschieden.append(wert)
    return np.array(gleich), np.array(verschieden)


def auc_gleiche_naeher(gleich, verschieden):
    """Anteil der Paare, in denen die gleiche Herkunft näher liegt als die verschiedene."""
    if len(gleich) == 0 or len(verschieden) == 0:
        raise SystemExit("AUC: eine der beiden Paargruppen ist leer")
    verschieden_sortiert = np.sort(verschieden)
    groesser = 0.0
    for wert in gleich:
        rechts = np.searchsorted(verschieden_sortiert, wert, side="right")
        links = np.searchsorted(verschieden_sortiert, wert, side="left")
        groesser += (len(verschieden) - rechts) + 0.5 * (rechts - links)
    return float(groesser / (len(gleich) * len(verschieden)))


def matrix_woerter(proben, merkmale):
    zeilen = []
    for probe in proben:
        woerter = buchstabenwoerter(probe)
        zeilen.append(rel_haeufigkeit(Counter(woerter), merkmale, len(woerter)))
    return np.vstack(zeilen)


def merkmal_woerter(proben, anzahl):
    gesamt = Counter()
    for probe in proben:
        gesamt.update(buchstabenwoerter(probe))
    return haeufigste(gesamt, anzahl)


def zeichenkette(probe):
    return " ".join(token.lower().replace("’", "'") for token in probe)


def ngramme(probe, n):
    kette = zeichenkette(probe)
    if len(kette) < n:
        return []
    return [kette[i : i + n] for i in range(len(kette) - n + 1)]


def merkmal_ngramme(proben, n, anzahl):
    gesamt = Counter()
    for probe in proben:
        gesamt.update(ngramme(probe, n))
    return haeufigste(gesamt, anzahl)


def matrix_ngramme(proben, merkmale, n):
    zeilen = []
    for probe in proben:
        stuecke = ngramme(probe, n)
        zeilen.append(rel_haeufigkeit(Counter(stuecke), merkmale, len(stuecke)))
    return np.vstack(zeilen)


def _zwischen_buchstaben(kette, stelle):
    if stelle <= 0 or stelle + 1 >= len(kette):
        return False
    return kette[stelle - 1].isalpha() and kette[stelle + 1].isalpha()


def interpunktion_zaehlung(probe):
    kette = " ".join(probe)
    zaehlung = Counter()
    for stelle, zeichen in enumerate(kette):
        if zeichen in "'’-" and _zwischen_buchstaben(kette, stelle):
            if zeichen in "'’":
                zaehlung["apostroph"] += 1
            continue
        getroffen = False
        for name, gruppe in INTERPUNKTION:
            if zeichen in gruppe:
                zaehlung[name] += 1
                getroffen = True
                break
        if getroffen:
            continue
        if unicodedata.category(zeichen).startswith("P") and zeichen not in INTERPUNKT_ZEICHEN:
            zaehlung["sonstige"] += 1
    return zaehlung


def interpunktion_namen():
    return [name for name, _ in INTERPUNKTION] + ["sonstige"]


def matrix_interpunktion(proben):
    namen = interpunktion_namen()
    zeilen = []
    for probe in proben:
        zeilen.append(
            rel_haeufigkeit(interpunktion_zaehlung(probe), namen, len(probe))
        )
    return np.vstack(zeilen), namen


def ruzicka(links, rechts):
    nenner = np.maximum(links, rechts).sum()
    if nenner == 0:
        return None
    return float(1.0 - np.minimum(links, rechts).sum() / nenner)


def impostor_anteil(kandidat, ziel, ablenker, rng):
    """Anteil der Ziehungen, in denen das Ziel näher liegt als jeder Ablenker.

    kandidat und ziel sind Vektoren, ablenker eine Matrix mit einer Zeile
    je Ablenker. Die Zufallszahlen sind dieselben wie bei B aufeinanderfolgenden
    Ziehungen der Länge des Vektors.
    """
    if ablenker.ndim != 2 or ablenker.shape[0] == 0:
        raise SystemExit("Impostors: kein Ablenker")
    breite = kandidat.shape[0]
    masken = rng.random((p.IMPOSTOR_WIEDERHOLUNGEN, breite)) < p.IMPOSTOR_MERKMALANTEIL
    genug = masken.sum(axis=1) >= 2
    minimum_ziel = (np.minimum(kandidat, ziel) * masken).sum(axis=1)
    maximum_ziel = (np.maximum(kandidat, ziel) * masken).sum(axis=1)
    paar_min = np.minimum(ablenker[:, None, :], kandidat[None, None, :])
    paar_max = np.maximum(ablenker[:, None, :], kandidat[None, None, :])
    minimum_ablenker = (paar_min * masken[None, :, :]).sum(axis=2)
    maximum_ablenker = (paar_max * masken[None, :, :]).sum(axis=2)
    gueltig = genug & (maximum_ziel > 0) & (maximum_ablenker.min(axis=0) > 0)
    if not np.any(gueltig):
        raise SystemExit("Impostors: keine gültige Ziehung")
    abstand_ziel = 1.0 - minimum_ziel[gueltig] / maximum_ziel[gueltig]
    abstand_ablenker = 1.0 - (
        minimum_ablenker[:, gueltig] / maximum_ablenker[:, gueltig]
    )
    return float(np.mean(abstand_ziel < abstand_ablenker.min(axis=0)))


def profil(relativ):
    return relativ.mean(axis=0)


def youden_schwelle(positiv, negativ):
    """Schwelle mit dem größten Youden-Index. Darüber gilt die Probe als zugehörig."""
    positiv = np.asarray(positiv, dtype=float)
    negativ = np.asarray(negativ, dtype=float)
    kandidaten = np.unique(np.concatenate([positiv, negativ]))
    bester_index = -np.inf
    schranken = []
    for schwelle in kandidaten:
        empfindlichkeit = float(np.mean(positiv >= schwelle))
        spezifitaet = float(np.mean(negativ < schwelle))
        index = empfindlichkeit + spezifitaet - 1.0
        if index > bester_index + 1e-12:
            bester_index = index
            schranken = [float(schwelle)]
        elif abs(index - bester_index) <= 1e-12:
            schranken.append(float(schwelle))
    return float(np.median(schranken)), float(bester_index)


def lage(wert, schwelle):
    if wert >= schwelle + p.ANTWORT_BAND:
        return "darueber"
    if wert <= schwelle - p.ANTWORT_BAND:
        return "darunter"
    return "unbeantwortet"


def strophen(text):
    """Versgruppen. Römische Gedichtnummern sind Überschriften, keine Strophen."""
    gruppen = []
    aktuell = []
    for zeile in unicodedata.normalize("NFC", text).splitlines():
        if not zeile.strip():
            if aktuell:
                gruppen.append(aktuell)
                aktuell = []
            continue
        if UEBERSCHRIFT.match(zeile.strip()):
            if aktuell:
                gruppen.append(aktuell)
                aktuell = []
            continue
        aktuell.append(zeile.strip())
    if aktuell:
        gruppen.append(aktuell)
    return gruppen


def reimkern(token):
    wort = buchstabenwort(token) or ""
    wort = (
        wort.replace("ey", "ei")
        .replace("ß", "ss")
        .replace("th", "t")
        .replace("ph", "f")
    )
    vokale = set("aeiouäöüy")
    stellen = [i for i, zeichen in enumerate(wort) if zeichen in vokale]
    if not stellen:
        return wort
    return wort[stellen[-1] :]


def kadenz_weiblich(token):
    wort = buchstabenwort(token) or ""
    return wort.endswith(("e", "en", "er", "el", "em", "es"))


def silbengruppen(token):
    wort = buchstabenwort(token) or ""
    gruppen = re.findall(r"[aeiouäöüy]+", wort)
    return len(gruppen)


# Vierfache Kantenlänge der SVG-Datei. Bei der üblichen Lesung von
# 96 CSS-Pixeln je Zoll sind das etwa 384 dpi, genug für eine Druckseite.
PNG_MASSSTAB = 4


def _chrome():
    kandidaten = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for pfad in kandidaten:
        if Path(pfad).is_file():
            return pfad
    gefunden = shutil.which("google-chrome") or shutil.which("chromium")
    if gefunden:
        return gefunden
    raise SystemExit("Für die PNG-Abbildungen fehlt Chrome, Chromium oder Edge.")


def schreibe_svg(pfad, text):
    """Schreibt die SVG-Datei und daneben eine PNG-Datei derselben Abbildung."""
    pfad = Path(pfad)
    pfad.write_text(text, encoding="utf-8")
    png_aus_svg(pfad)


def png_aus_svg(svg_pfad):
    """Rastert eine SVG-Datei mit Breite und Höhe auf das Vierfache."""
    svg_pfad = Path(svg_pfad)
    text = svg_pfad.read_text(encoding="utf-8")
    treffer = re.search(
        r'<svg\b[^>]*\bwidth="([0-9.]+)"[^>]*\bheight="([0-9.]+)"',
        text,
    )
    if not treffer:
        raise SystemExit("SVG ohne Breite und Höhe: " + str(svg_pfad))
    breite = int(round(float(treffer.group(1))))
    hoehe = int(round(float(treffer.group(2))))
    png = svg_pfad.with_suffix(".png")
    with tempfile.TemporaryDirectory(prefix="svgpng_") as ordner:
        html = Path(ordner) / "blatt.html"
        html.write_text(
            "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head>"
            f'<body style="margin:0"><img src="{svg_pfad.resolve().as_uri()}" '
            f'width="{breite}" height="{hoehe}" style="display:block"></body></html>',
            encoding="utf-8",
        )
        profil = Path(ordner) / "profil"
        befehl = [
            _chrome(),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={profil}",
            f"--force-device-scale-factor={PNG_MASSSTAB}",
            f"--window-size={breite},{hoehe}",
            f"--screenshot={png.resolve()}",
            html.resolve().as_uri(),
        ]
        ergebnis = subprocess.run(befehl, capture_output=True, text=True)
    if ergebnis.returncode != 0 or not png.is_file():
        meldung = (ergebnis.stderr or ergebnis.stdout or "").strip()
        raise SystemExit("PNG fehlt: " + str(png) + "\n" + meldung[-400:])
    daten = png.read_bytes()
    ist_breite = int.from_bytes(daten[16:20], "big")
    ist_hoehe = int.from_bytes(daten[20:24], "big")
    if ist_breite != breite * PNG_MASSSTAB or ist_hoehe != hoehe * PNG_MASSSTAB:
        raise SystemExit(
            f"PNG hat {ist_breite}×{ist_hoehe}, erwartet sind "
            f"{breite * PNG_MASSSTAB}×{hoehe * PNG_MASSSTAB}: {png}"
        )
    return png


def schreibe_json(pfad, inhalt):
    Path(pfad).write_text(
        json.dumps(inhalt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def lese_json(pfad):
    return json.loads(Path(pfad).read_text(encoding="utf-8"))


def selbsttest():
    relativ = np.array(
        [
            [0.50, 0.50, 0.00],
            [0.40, 0.60, 0.00],
            [0.00, 0.10, 0.90],
            [0.00, 0.20, 0.80],
        ]
    )
    abstand, _ = kosinus_delta(relativ)
    gleich, verschieden = paare(abstand, ["heine", "heine", "hektor", "hektor"], {"heine", "hektor"})
    wert = auc_gleiche_naeher(gleich, verschieden)
    if wert < 0.99:
        raise SystemExit(f"Selbsttest AUC fehlgeschlagen: {wert}")
    if ruzicka(np.array([1.0, 0.0]), np.array([1.0, 0.0])) != 0.0:
        raise SystemExit("Selbsttest Ružička, gleiche Vektoren")
    if ruzicka(np.array([1.0, 0.0]), np.array([0.0, 1.0])) != 1.0:
        raise SystemExit("Selbsttest Ružička, fremde Vektoren")
    if buchstabenwort("Melodei'n.") != "melodei'n":
        raise SystemExit("Selbsttest Wortbild")
    if interpunktion_zaehlung(["trüb'", "und", "Gras,"])["apostroph"] != 1:
        raise SystemExit("Selbsttest Apostroph")
    if interpunktion_zaehlung(["trüb'", "und", "Gras,"])["komma"] != 1:
        raise SystemExit("Selbsttest Komma")
