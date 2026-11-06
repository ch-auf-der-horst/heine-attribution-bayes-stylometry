# -*- coding: utf-8 -*-
"""Studie 5. Abstand des Kandidaten zu Heine, Schilda und den Vagabunden-Liedern.

Die sieben frühen Heine-Texte werden nicht aneinandergehängt. Schilda und
die Vagabunden-Lieder bleiben zwei Texte. In derselben Tafel stehen Müller,
das Wunderhorn, Uhland und die Juniuslieder. Ein eigener Gedichttext Arnims
liegt nicht vor; das Wunderhorn wird nicht unter seinem Namen geführt.
Der Kandidat wählt keine Merkmale und geht nicht in die Standardwerte ein.

Zwei Längen. 548 Wörter sind die Länge des Kandidaten. Texte darunter
fehlen in dieser Rangliste. 351 Wörter sind die Länge der Biene; dort ist
der Kandidat die ersten 351 Wörter. Die letzten 351 Wörter werden berichtet
und entscheiden nicht.

Die Konsensbäume folgen dem Verfahren der Studien. Ihr Zufallsstrom ist
SeedSequence([Seed, 5]).

Aufruf vom Projektordner aus:

    AUTOR_STUDIE=5 python3 analyse/12_studie5_naehe.py

Schreibt nach ergebnisse/studie5/. Studie 1 bis 4 werden nicht angefasst.
Besteht der Ordner schon, bricht der Lauf ab. AUTOR_NEUZEICHNEN=1
schreibt denselben Lauf neu, mit demselben Zufallsstrom.
"""

import csv
import html
import importlib.util
import json
import os
import platform
import sys
from pathlib import Path

if os.environ.get("AUTOR_STUDIE") != "5":
    raise SystemExit("Studie 5 verlangt AUTOR_STUDIE=5, sonst läge die Dateiliste einer anderen Studie an.")

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from laufwahl import parameter as p
import gemeinsame as g

_abb = importlib.util.spec_from_file_location(
    "abbildungen", Path(__file__).resolve().parent / "08_abbildungen.py"
)
abb = importlib.util.module_from_spec(_abb)
_abb.loader.exec_module(abb)

_fig = importlib.util.spec_from_file_location(
    "heine_abbildungen", Path(__file__).resolve().parent / "10_heine_abbildungen.py"
)
fig = importlib.util.module_from_spec(_fig)
_fig.loader.exec_module(fig)

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
ABLENKER = (
    ("Mueller_1.txt", "Müller"),
    ("Wunderhorn_1806.txt", "Wunderhorn"),
    ("Uhland_Lieder.txt", "Uhland"),
    ("Geibel_Junius.txt", "Junius"),
)
BOOTSTRAP = 500
KURZ = 351

fig.FARBE.update(
    {
        "Hektor": "#9b3a4a",
        "Schilda": "#9b3a4a",
        "Vagabund": "#b36b2a",
        "Müller": "#3d6b8a",
        "Wunderhorn": "#4a5568",
        "Uhland": "#2f6b4f",
        "Junius": "#6a4a78",
        "Kandidat": "#1c1915",
    }
)


def reine_schnitte(woerter, laenge):
    return [woerter[start : start + laenge] for start in range(0, len(woerter) - laenge + 1, laenge)]


def pruefe_liste(eintraege, erwartet, rolle):
    namen = [Path(eintrag["pfad"]).name for eintrag in eintraege]
    if namen != [datei for datei, _ in erwartet]:
        raise SystemExit(f"Die {rolle}-Dateien sind nicht die festgelegten: {namen}")


def referenz_laden():
    for eintrag in g.eintraege("ausgeschieden"):
        g.lade_text(eintrag)
    heine_eintraege = g.eintraege("heine")
    hektor_eintraege = g.eintraege("hektor")
    ablenker_eintraege = g.eintraege("ablenker")
    pruefe_liste(heine_eintraege, HEINE, "Heine")
    pruefe_liste(hektor_eintraege, HEKTOR, "Hektor")
    pruefe_liste(ablenker_eintraege, ABLENKER, "Ablenker")
    texte = []
    for eintrag, (_, name) in zip(heine_eintraege, HEINE):
        texte.append({"name": name, "rolle": "heine", "eintrag": eintrag, "woerter": g.lade_text(eintrag)})
    for eintrag, (_, name) in zip(hektor_eintraege, HEKTOR):
        texte.append({"name": name, "rolle": "hektor", "eintrag": eintrag, "woerter": g.lade_text(eintrag)})
    for eintrag, (_, name) in zip(ablenker_eintraege, ABLENKER):
        texte.append({"name": name, "rolle": "ablenker", "eintrag": eintrag, "woerter": g.lade_text(eintrag)})
    return texte


def scheiben(texte, laenge):
    bloecke = []
    for text in texte:
        schnitte = reine_schnitte(text["woerter"], laenge)
        rest = len(text["woerter"]) - laenge * len(schnitte)
        bloecke.append({**text, "schnitte": schnitte, "rest": rest})
    return bloecke


def eichproben(bloecke):
    proben = []
    for block in bloecke:
        if block["rolle"] in {"heine", "hektor"}:
            proben.extend(block["schnitte"])
    if len(proben) < 2:
        raise SystemExit("Zu wenige Eichproben für die Merkmale")
    return proben


def vektor(probe, merkmale, art, n=None):
    if art == "woerter":
        return g.matrix_woerter([probe], merkmale)[0]
    if art == "zeichen":
        return g.matrix_ngramme([probe], merkmale, n)[0]
    matrix, _ = g.matrix_interpunktion([probe])
    return matrix[0]


def profile_und_eichung(bloecke, kandidat, merkmale, art, n=None):
    namen = []
    profilzeilen = []
    eichzeilen = []
    for block in bloecke:
        if not block["schnitte"]:
            continue
        matrix = np.vstack([vektor(schnitt, merkmale, art, n) for schnitt in block["schnitte"]])
        profil = matrix.mean(axis=0)
        namen.append(block["name"])
        profilzeilen.append(profil)
        if block["rolle"] in {"heine", "hektor"}:
            eichzeilen.append(profil)
    if len(eichzeilen) < 2:
        raise SystemExit("Zu wenige Profile für die Standardwerte")
    kandidatzeile = vektor(kandidat, merkmale, art, n)
    zeilen = np.vstack(profilzeilen + [kandidatzeile])
    eichung = np.vstack(eichzeilen)
    abstand = abb.kosinus(zeilen, eichung)
    if abstand is None:
        raise SystemExit("Kosinusabstand ist nicht bestimmt")
    return namen, zeilen, eichung, {name: float(abstand[-1, i]) for i, name in enumerate(namen)}


def merkmale_woerter(proben):
    return g.merkmal_woerter(proben, 300)


def fmt(wert):
    return f"{wert:.4f}".replace(".", ",")


def rang_unter(namen, abstand, nur):
    geordnet = sorted((name for name in namen if name in nur), key=lambda name: (abstand[name], name))
    return {name: stelle for stelle, name in enumerate(geordnet, start=1)}


def naechster_name(namen, abstand, nur):
    return min((name for name in namen if name in nur), key=lambda name: (abstand[name], name))


def tabelle(bloecke, spalten, heine_namen):
    kopf = (
        "| Text | Proben | ungenutzt | "
        + " | ".join(spalten)
        + " | Rang Heine, Wörter 150 | Rang Tafel, Wörter 150 |"
    )
    trenn = "| --- | ---: | ---: | " + " | ".join("---:" for _ in spalten) + " | ---: | ---: |"
    woerter = spalten["Wörter 150"]
    tafelrang = rang_unter(woerter, woerter, set(woerter))
    heinerang = rang_unter(woerter, woerter, set(heine_namen))
    zeilen = [kopf, trenn]
    for block in bloecke:
        name = block["name"]
        if name not in woerter:
            zeilen.append(
                f"| {name} | 0 | {block['rest']} | "
                + " | ".join("—" for _ in spalten)
                + " | — | — |"
            )
            continue
        zellen = " | ".join(fmt(spalten[titel][name]) for titel in spalten)
        heine_zelle = str(heinerang[name]) if name in heinerang else "—"
        zeilen.append(
            f"| {name} | {len(block['schnitte'])} | {block['rest']} | {zellen} | {heine_zelle} | {tafelrang[name]} |"
        )
    return "\n".join(zeilen)


def lesung(abstand_wort, abstand_zeichen, namen, heine_namen):
    wort = naechster_name(namen, abstand_wort, set(heine_namen))
    zeichen = naechster_name(namen, abstand_zeichen, set(heine_namen))
    if wort == zeichen:
        satz = f"Unter den Heine-Texten dieser Tafel nennen die 150 Wörter und die Vierergruppen denselben Text: {wort}."
    else:
        satz = (
            f"Unter den Heine-Texten dieser Tafel nennen die 150 Wörter {wort} "
            f"und die Vierergruppen {zeichen}."
        )
    andere = [name for name in namen if name not in heine_namen]
    naeher = [name for name in andere if abstand_wort[name] < abstand_wort[wort]]
    if naeher:
        satz += " Näher als " + wort + " liegen auf den Wörtern: " + ", ".join(naeher) + "."
    else:
        satz += f" Auf den Wörtern liegt {wort} näher als Schilda, näher als Vagabund und näher als jeder Ablenker."
    naeher_z = [name for name in andere if abstand_zeichen[name] < abstand_zeichen[zeichen]]
    if naeher_z:
        satz += " Näher als " + zeichen + " liegen auf den Vierergruppen: " + ", ".join(naeher_z) + "."
    else:
        satz += (
            f" Auf den Vierergruppen liegt {zeichen} näher als Schilda, näher als Vagabund "
            "und näher als jeder Ablenker."
        )
    return satz, wort, zeichen


def tafel_satz(abstand_wort, abstand_zeichen, namen):
    wort = min(namen, key=lambda name: (abstand_wort[name], name))
    zeichen = min(namen, key=lambda name: (abstand_zeichen[name], name))
    if wort == zeichen:
        return (
            f"Auf der ganzen Tafel nennen die 150 Wörter und die Vierergruppen denselben Text: {wort}. "
            "Das ist eine Reihung, keine Zuschreibung."
        )
    return (
        f"Auf der ganzen Tafel nennen die 150 Wörter {wort} und die Vierergruppen {zeichen}. "
        "Das ist eine Reihung, keine Zuschreibung."
    )


def paar_stuetze(baeume, etiketten):
    k = etiketten.index("Kandidat")
    anteile = {}
    for name in etiketten:
        if name == "Kandidat":
            continue
        ziel = frozenset((etiketten.index(name), k))
        anteile[name] = sum(ziel in baum for baum in baeume) / len(baeume)
    return anteile


def stuetze_text(anteile, heine_namen):
    zeilen = ["| Text | Anteil der Bäume mit dem Kandidaten als Zweiergruppe |", "| --- | ---: |"]
    for name in heine_namen:
        if name not in anteile:
            continue
        zeilen.append(f"| {name} | {anteile[name] * 100:.1f} % |".replace(".", ","))
    return "\n".join(zeilen)


def bootstrap(profilzeilen, eichung, rng):
    spalten = profilzeilen.shape[1]
    baeume = []
    for _ in range(BOOTSTRAP):
        maske = rng.random(spalten) < abb.MERKMALANTEIL
        if int(maske.sum()) < 8:
            continue
        abstand = abb.kosinus(profilzeilen[:, maske], eichung[:, maske])
        if abstand is None:
            continue
        baeume.append(abb.kladen(abb.upgma(abstand)))
    if len(baeume) < BOOTSTRAP * 0.9:
        raise SystemExit("Zu viele Bootstrap-Ziehungen ohne Streuung")
    return baeume


def zeichne_konsens(profilzeilen, eichung, etiketten, rng, titel, untertitel, pfad):
    primaer = abb.kosinus(profilzeilen, eichung)
    if primaer is None:
        raise SystemExit("Konsensbaum ohne Abstand")
    referenz = abb.blattordnung(abb.upgma(primaer))
    baeume = bootstrap(profilzeilen, eichung, rng)
    gewaehlt, _ = abb.mehrheit(baeume, len(etiketten))
    fig.svg_baum(abb.baum_aus_kladen(gewaehlt, etiketten, referenz), titel, untertitel, pfad)
    return baeume, gewaehlt, referenz


def svg_balken(pfad, abstand, reihenfolge, titel, untertitel):
    werte = [abstand[name] for name in reihenfolge]
    breite, hoehe = 760, 78 + 28 * len(reihenfolge)
    links = 150
    maximale = max(werte) * 1.08
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}">',
        '<rect width="100%" height="100%" fill="#fbfbfa"/>',
        f'<text x="28" y="28" font-family="Georgia, serif" font-size="16" fill="#222">{abb.xml(titel)}</text>',
        f'<text x="28" y="48" font-family="sans-serif" font-size="12" fill="#555">{abb.xml(untertitel)}</text>',
    ]
    for nummer, name in enumerate(reihenfolge):
        y = 64 + nummer * 28
        laenge = werte[nummer] / maximale * 460
        farbe = fig.FARBE.get(name, "#333")
        teile.append(
            f'<text x="28" y="{y + 14}" font-family="sans-serif" font-size="13" fill="{farbe}">{abb.xml(name)}</text>'
        )
        teile.append(f'<rect x="{links}" y="{y}" width="{laenge:.1f}" height="16" fill="{farbe}" opacity="0.85"/>')
        teile.append(
            f'<text x="{links + laenge + 8:.1f}" y="{y + 13}" font-family="sans-serif" font-size="12" fill="#333">{werte[nummer]:.2f}</text>'
        )
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")


def html_uebersicht(bilder):
    bloecke = []
    for datei, unterschrift in bilder:
        bloecke.append(
            "<figure>"
            f'<img src="{html.escape(datei)}" alt="{html.escape(unterschrift)}">'
            f"<figcaption>{html.escape(unterschrift)}</figcaption>"
            "</figure>"
        )
    text = """<!DOCTYPE html>
<html lang="de">
<meta charset="utf-8">
<title>Studie 5, Abbildungen</title>
<style>
body { font-family: Georgia, serif; max-width: 980px; margin: 32px auto; color: #222; background: #fbfbfa; }
figcaption { font-family: sans-serif; font-size: 14px; color: #333; margin: 8px 0 28px; }
img { max-width: 100%; height: auto; border: 1px solid #e4e0d8; }
</style>
<h1>Studie 5, Abbildungen</h1>
<p>Jeder Heine-Text ist ein eigenes Blatt. Schilda und die Vagabunden-Lieder sind zwei Blätter. Die Bilder ändern die Studien 1 bis 4 nicht. Impostors werden hier nicht gerechnet.</p>
""" + "\n".join(bloecke) + "\n</html>\n"
    (p.LAUF / "abb_uebersicht.html").write_text(text, encoding="utf-8")


def schreibe_csv(pfad, bloecke, spalten):
    with pfad.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["text", "rolle", "proben", "ungenutzt", *spalten])
        for block in bloecke:
            name = block["name"]
            zeile = [name, block["rolle"], len(block["schnitte"]), block["rest"]]
            for titel in spalten:
                wert = spalten[titel].get(name)
                zeile.append("" if wert is None else f"{wert:.4f}")
            writer.writerow(zeile)


def kladen_zeilen(abbildung, gewaehlt, etiketten):
    zeilen = []
    for klade, anteil in gewaehlt:
        namen = ", ".join(etiketten[i] for i in sorted(klade))
        zeilen.append({"abbildung": abbildung, "klade": namen, "anteil": f"{anteil:.4f}"})
    return zeilen


def rechne_art(bloecke, kandidat, art, eich, merkmale, n=None):
    return profile_und_eichung(bloecke, kandidat, merkmale, art, n)


def bestand(bloecke, laenge):
    zeilen = []
    for block in bloecke:
        anzahl = len(block["schnitte"])
        wort = "Probe" if anzahl == 1 else "Proben"
        zeilen.append(
            f"- {block['name']}: {len(block['woerter'])} Wörter, {anzahl} {wort}, {block['rest']} Wörter nicht verwendet"
        )
    zeilen.append(f"- Kandidat: {laenge} Wörter in dieser Tafel")
    return "\n".join(zeilen)


def main():
    abb.selbsttest()
    if p.LAUF.exists() and os.environ.get("AUTOR_NEUZEICHNEN") != "1":
        raise SystemExit("Der Laufordner besteht schon und wird nicht überschrieben: " + str(p.LAUF))
    p.LAUF.mkdir(parents=True, exist_ok=True)
    (p.LAUF / "parameter.json").write_text(
        json.dumps(
            {
                "studie": p.STUDIE_NAME,
                "seed": p.SEED,
                "baum_seed": [p.SEED, 5],
                "probenlaenge": p.PROBENLAENGE,
                "nebenlaenge": KURZ,
                "mfw": p.MFW,
                "mfw_bericht": list(p.MFW_BERICHT),
                "zeichen_n": p.ZEICHEN_N,
                "zeichen_n_bericht": list(p.ZEICHEN_N_BERICHT),
                "zeichen_haeufigste": p.ZEICHEN_HAEUFIGSTE,
                "versatz": 0,
                "einzeltexte": True,
                "dateiliste": str(p.DATEILISTE.relative_to(p.PROJEKT)),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (p.LAUF / "pakete.txt").write_text(
        "\n".join(
            [
                f"python {platform.python_version()}",
                f"numpy {np.__version__}",
                f"system {platform.platform()}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    texte = referenz_laden()
    heine_namen = [name for _, name in HEINE]
    kandidat_eintrag = g.eintraege("kandidat")
    if len(kandidat_eintrag) != 1 or Path(kandidat_eintrag[0]["pfad"]).name != "Kandidat_Vagabund.txt":
        raise SystemExit("Der Kandidat ist nicht Kandidat_Vagabund.txt")

    bloecke_548 = scheiben(texte, p.PROBENLAENGE)
    bloecke_351 = scheiben(texte, KURZ)
    eich_548 = eichproben(bloecke_548)
    eich_351 = eichproben(bloecke_351)
    worte_548 = merkmale_woerter(eich_548)
    worte_351 = merkmale_woerter(eich_351)
    zeichen_548 = {
        n: g.merkmal_ngramme(eich_548, n, p.ZEICHEN_HAEUFIGSTE) for n in (p.ZEICHEN_N, *p.ZEICHEN_N_BERICHT)
    }
    zeichen_351 = {
        n: g.merkmal_ngramme(eich_351, n, p.ZEICHEN_HAEUFIGSTE) for n in (p.ZEICHEN_N, *p.ZEICHEN_N_BERICHT)
    }

    kandidat = g.lade_text(kandidat_eintrag[0])
    if len(kandidat) != p.PROBENLAENGE:
        raise SystemExit("Der Kandidat hat nicht die festgelegte Probenlänge")
    kandidat_anfang = kandidat[:KURZ]
    kandidat_ende = kandidat[-KURZ:]
    if len(kandidat_anfang) != KURZ or len(kandidat_ende) != KURZ:
        raise SystemExit("Die Scheiben des Kandidaten haben nicht 351 Wörter")

    def spalten_fuer(bloecke, eich_worte, eich_zeichen, kandidat_probe):
        spalten = {}
        pack = {}
        for anzahl, titel in ((150, "Wörter 150"), (100, "Wörter 100"), (300, "Wörter 300")):
            namen, zeilen, eichung, abstand = profile_und_eichung(
                bloecke, kandidat_probe, eich_worte[:anzahl], "woerter"
            )
            spalten[titel] = abstand
            pack[titel] = (namen, zeilen, eichung, abstand)
        for n, titel in ((4, "Zeichen 4"), (3, "Zeichen 3"), (5, "Zeichen 5")):
            namen, zeilen, eichung, abstand = profile_und_eichung(
                bloecke, kandidat_probe, eich_zeichen[n], "zeichen", n
            )
            spalten[titel] = abstand
            pack[titel] = (namen, zeilen, eichung, abstand)
        namen_i, zeilen_i, eichung_i, abstand_i = profile_und_eichung(
            bloecke, kandidat_probe, None, "interpunktion"
        )
        spalten["Interpunktion"] = abstand_i
        return spalten, pack

    spalten_548, pack_548 = spalten_fuer(bloecke_548, worte_548, zeichen_548, kandidat)
    spalten_anfang, pack_anfang = spalten_fuer(bloecke_351, worte_351, zeichen_351, kandidat_anfang)
    spalten_ende, _ = spalten_fuer(bloecke_351, worte_351, zeichen_351, kandidat_ende)

    schreibe_csv(p.LAUF / "548_abstaende.csv", bloecke_548, spalten_548)
    schreibe_csv(p.LAUF / "351_anfang_abstaende.csv", bloecke_351, spalten_anfang)
    schreibe_csv(p.LAUF / "351_ende_abstaende.csv", bloecke_351, spalten_ende)

    namen_548 = pack_548["Wörter 150"][0]
    satz_548, wort_548, zeichen_548_name = lesung(
        spalten_548["Wörter 150"], spalten_548["Zeichen 4"], namen_548, set(heine_namen)
    )
    namen_351 = pack_anfang["Wörter 150"][0]
    satz_351, wort_351, zeichen_351_name = lesung(
        spalten_anfang["Wörter 150"], spalten_anfang["Zeichen 4"], namen_351, set(heine_namen)
    )
    ende_wort = naechster_name(namen_351, spalten_ende["Wörter 150"], set(heine_namen))
    ende_zeichen = naechster_name(namen_351, spalten_ende["Zeichen 4"], set(heine_namen))
    if ende_wort == wort_351 and ende_zeichen == zeichen_351_name:
        satz_ende = (
            f"Die letzten {KURZ} Wörter nennen auf Wörtern und Vierergruppen denselben Heine-Text "
            f"wie die ersten {KURZ}: {ende_wort}."
        )
    else:
        satz_ende = (
            f"Die letzten {KURZ} Wörter nennen auf den 150 Wörtern {ende_wort} "
            f"und auf den Vierergruppen {ende_zeichen}. "
            f"Die ersten {KURZ} nennen {wort_351} und {zeichen_351_name}. Die letzten entscheiden nicht."
        )
    satz_tafel_548 = tafel_satz(spalten_548["Wörter 150"], spalten_548["Zeichen 4"], namen_548)
    satz_tafel_351 = tafel_satz(spalten_anfang["Wörter 150"], spalten_anfang["Zeichen 4"], namen_351)
    neben_namen = heine_namen + ["Schilda", "Vagabund"]

    rng = np.random.default_rng(np.random.SeedSequence([p.SEED, 5]))
    csv_zeilen = []

    def baum(pack, schluessel, abbildung, titel, untertitel, datei):
        namen, zeilen, eichung, _ = pack[schluessel]
        etiketten = namen + ["Kandidat"]
        baeume, gewaehlt, referenz = zeichne_konsens(
            zeilen, eichung, etiketten, rng, titel, untertitel, p.LAUF / datei
        )
        csv_zeilen.extend(kladen_zeilen(abbildung, gewaehlt, etiketten))
        abb.svg_dendrogramm(
            abb.upgma(abb.kosinus(zeilen, eichung)),
            etiketten,
            abb.anteile_der_kladen(baeume),
            titel.replace("Konsens", "Dendrogramm"),
            "UPGMA auf dem Cosine Delta. Die Zahl ist der Anteil der 500 Bäume in Prozent.\nWaagerecht die Gruppierungshöhe. Eine hellere Zahl liegt unter 50 Prozent.",
            p.LAUF / datei.replace("abb_konsens", "abb_dendrogramm"),
            fig.farbe_von_etikett,
        )
        abb.svg_stern(
            abb.baum_aus_kladen(gewaehlt, etiketten, referenz),
            etiketten,
            None,
            titel.replace("Konsens", "Stern"),
            "Mehrheitskonsens. Gleiche Astlänge, keine Distanz. Nur Gruppen ab 50 Prozent.",
            p.LAUF / datei.replace("abb_konsens", "abb_stern_konsens"),
            fig.farbe_von_etikett,
            art="gleich",
        )
        abb.svg_stern(
            abb.upgma(abb.kosinus(zeilen, eichung)),
            etiketten,
            abb.anteile_der_kladen(baeume),
            titel.replace("Konsens", "Stern nach der Gruppierungshöhe"),
            "Die Mitte ist die letzte UPGMA-Gruppe. Die Astlänge ist die Gruppierungshöhe. Zahlen ab 50.",
            p.LAUF / datei.replace("abb_konsens", "abb_stern"),
            fig.farbe_von_etikett,
            art="hoehe",
        )
        return baeume, etiketten, referenz

    baeume_w, etiketten_w, referenz_w = baum(
        pack_548,
        "Wörter 150",
        "548_woerter",
        "Konsens, 548 Wörter",
        "Ein Blatt je Text. 500 Bäume, 150 Wörter. Biene, Kevlaar und Donna Clara sind kürzer und fehlen.\nDie Normierung zählt jeden Heine-Text dieser Tafel, Schilda und Vagabund einmal.",
        "abb_konsens_548.svg",
    )
    baeume_z, etiketten_z, _ = baum(
        pack_548,
        "Zeichen 4",
        "548_zeichen",
        "Konsens nach Zeichen-4-Grammen, 548 Wörter",
        "Ein Blatt je Text. 500 Bäume, 500 häufigste 4-Gramme.",
        "abb_konsens_zeichen.svg",
    )
    leiter = []
    for anzahl, schluessel in ((100, "Wörter 100"), (150, "Wörter 150"), (300, "Wörter 300")):
        namen, zeilen, eichung, _ = pack_548[schluessel]
        abstand = abb.kosinus(zeilen, eichung)
        leiter.append(abb.kladen(abb.upgma(abstand)))
    gewaehlt_leiter, _ = abb.mehrheit(leiter, len(etiketten_w))
    fig.svg_baum(
        abb.baum_aus_kladen(gewaehlt_leiter, etiketten_w, referenz_w),
        "Konsens über die Merkmalleiter, 548 Wörter",
        "Drei Bäume, für 100, 150 und 300 häufigste Wörter. Eine Zahl 100 heißt: der Ast steht in allen drei.",
        p.LAUF / "abb_konsens_mfw.svg",
    )
    csv_zeilen.extend(kladen_zeilen("548_mfw", gewaehlt_leiter, etiketten_w))
    _, zeilen_mfw, eichung_mfw, _ = pack_548["Wörter 150"]
    abb.svg_dendrogramm(
        abb.upgma(abb.kosinus(zeilen_mfw, eichung_mfw)),
        etiketten_w,
        abb.anteile_der_kladen(leiter),
        "Dendrogramm der Merkmalleiter, 548 Wörter",
        "UPGMA der 150 Wörter. Die Zahl ist der Anteil der drei Merkmalzahlen in Prozent. 100 heißt: die Gruppe steht bei 100, 150 und 300.",
        p.LAUF / "abb_dendrogramm_mfw.svg",
        fig.farbe_von_etikett,
    )
    abb.svg_stern(
        abb.baum_aus_kladen(gewaehlt_leiter, etiketten_w, referenz_w),
        etiketten_w,
        None,
        "Merkmalleiter, sternförmig",
        "Mehrheitskonsens der drei Merkmalzahlen. Gleiche Astlänge, keine Distanz.",
        p.LAUF / "abb_stern_konsens_mfw.svg",
        fig.farbe_von_etikett,
        art="gleich",
    )
    abb.svg_stern(
        abb.upgma(abb.kosinus(zeilen_mfw, eichung_mfw)),
        etiketten_w,
        abb.anteile_der_kladen(leiter),
        "Merkmalleiter, sternförmig nach der Gruppierungshöhe",
        "UPGMA der 150 Wörter. Die Zahl ist der Anteil der drei Merkmalzahlen. 100 heißt: die Gruppe steht bei 100, 150 und 300.",
        p.LAUF / "abb_stern_mfw.svg",
        fig.farbe_von_etikett,
        art="hoehe",
    )
    baeume_351, etiketten_351, _ = baum(
        pack_anfang,
        "Wörter 150",
        "351_woerter",
        "Konsens, 351 Wörter",
        "Alle sieben Heine-Texte. Das Blatt Kandidat sind die ersten 351 Wörter.\n500 Bäume, 150 Wörter.",
        "abb_konsens_351.svg",
    )

    stuetze_548 = paar_stuetze(baeume_w, etiketten_w)
    stuetze_zeichen = paar_stuetze(baeume_z, etiketten_z)
    stuetze_351 = paar_stuetze(baeume_351, etiketten_351)

    reihe_548 = sorted(namen_548, key=lambda name: spalten_548["Wörter 150"][name])
    reihe_351 = sorted(namen_351, key=lambda name: spalten_anfang["Wörter 150"][name])
    svg_balken(
        p.LAUF / "abb_profile_548.svg",
        spalten_548["Wörter 150"],
        reihe_548,
        "Abstand des Kandidaten, 548 Wörter",
        "Cosine Delta, 150 häufigste Wörter. Oben ist näher. Ein Balken ist ein Text, nicht eine einzelne Probe.",
    )
    svg_balken(
        p.LAUF / "abb_profile_351.svg",
        spalten_anfang["Wörter 150"],
        reihe_351,
        "Abstand der ersten 351 Wörter des Kandidaten",
        "Cosine Delta, 150 häufigste Wörter. Oben ist näher. Die letzten 197 Wörter des Kandidaten fehlen in diesem Bild.",
    )

    with (p.LAUF / "eingaben.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["pfad", "rolle", "wortzahl", "sha256", "in_der_merkmalliste"],
        )
        writer.writeheader()
        for zeile in g.dateiliste():
            writer.writerow(
                {
                    "pfad": zeile["pfad"],
                    "rolle": zeile["rolle"],
                    "wortzahl": zeile["wortzahl"],
                    "sha256": g.pruefsumme(g.pfad_zu(zeile)),
                    "in_der_merkmalliste": "ja" if zeile["rolle"] in {"heine", "hektor"} else "nein",
                }
            )

    with (p.LAUF / "konsens_kladen.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["abbildung", "klade", "anteil"])
        writer.writeheader()
        writer.writerows(csv_zeilen)

    text = "\n".join(
        [
            "# Studie 5. Heine, Schilda und die Vagabunden-Lieder",
            "",
            "Die Heine-Texte sind nicht gemittelt. Schilda und die Vagabunden-Lieder sind zwei Texte. Der Kandidat hat die Merkmale nicht mitgewählt. Studie 1 bis 4 sind nicht neu gerechnet. Dies ist eine Reihung, keine Zuschreibung. Ein eigener Gedichttext Arnims liegt nicht vor. Das Wunderhorn bleibt die anonyme Sammlung.",
            "",
            f"Prüfsumme des Kandidaten: {g.pruefsumme(g.pfad_zu(kandidat_eintrag[0]))}.",
            "",
            "## 548 Wörter",
            "",
            "Das ist die Hauptrangliste, auf der Länge des ganzen Kandidaten. Biene, Kevlaar und Donna Clara bleiben darunter.",
            "",
            bestand(bloecke_548, p.PROBENLAENGE),
            "",
            satz_548,
            "",
            satz_tafel_548,
            "",
            tabelle(bloecke_548, spalten_548, heine_namen),
            "",
            "Anteil der 500 Wortbäume, in denen der Kandidat mit diesem Text allein eine Gruppe bildet:",
            "",
            stuetze_text(stuetze_548, neben_namen),
            "",
            "Dieselbe Zweiergruppe in den Bäumen der Vierergruppen:",
            "",
            stuetze_text(stuetze_zeichen, neben_namen),
            "",
            "## 351 Wörter, Anfang des Kandidaten",
            "",
            f"Alle sieben Heine-Texte. Vom Kandidaten stehen die ersten {KURZ} Wörter in der Tafel. Die übrigen {p.PROBENLAENGE - KURZ} Wörter bleiben hier ungenutzt.",
            "",
            bestand(bloecke_351, KURZ),
            "",
            satz_351,
            "",
            satz_tafel_351,
            "",
            tabelle(bloecke_351, spalten_anfang, heine_namen),
            "",
            "Zweiergruppen mit dem Kandidaten in den Wortbäumen dieser Tafel:",
            "",
            stuetze_text(stuetze_351, neben_namen),
            "",
            "## 351 Wörter, Ende des Kandidaten",
            "",
            satz_ende,
            "",
            tabelle(bloecke_351, spalten_ende, heine_namen),
            "",
            "Die Abstände stehen auf der Skala dieser Studie. Sie sind nicht die Profilabstände aus Studie 1 bis 4.",
            "",
        ]
    )
    (p.LAUF / "NAEHE.md").write_text(text, encoding="utf-8")
    html_uebersicht(
        [
            ("abb_stern_548.svg", "Sternförmiger UPGMA-Baum der Texte zu 548 Wörtern und des Kandidaten. Die Astlänge ist die Gruppierungshöhe."),
            ("abb_stern_zeichen.svg", "Derselbe sternförmige Baum für die Zeichen-4-Gramme."),
            ("abb_stern_mfw.svg", "Sternförmiger Baum der 150 häufigsten Wörter."),
            ("abb_stern_351.svg", "Sternförmiger Baum der ersten 351 Wörter."),
            ("abb_stern_konsens_548.svg", "Dieselbe Mehrheit als Stern. Die Astlänge ist keine Distanz."),
            ("abb_stern_konsens_zeichen.svg", "Mehrheitsstern der Zeichen-4-Gramme."),
            ("abb_stern_konsens_mfw.svg", "Mehrheitsstern über 100, 150 und 300 häufigste Wörter."),
            ("abb_stern_konsens_351.svg", "Mehrheitsstern der kürzeren Proben."),
            ("abb_dendrogramm_548.svg", "Dendrogramm der Texte, die 548 Wörter tragen, und des Kandidaten. Die Achse ist die Gruppierungshöhe."),
            ("abb_dendrogramm_zeichen.svg", "Dasselbe Dendrogramm für die Zeichen-4-Gramme."),
            ("abb_dendrogramm_mfw.svg", "Dendrogramm der 150 häufigsten Wörter. Die Zahl sagt, in wie viel Prozent der drei Merkmalzahlen die Gruppe steht."),
            ("abb_dendrogramm_351.svg", "Dendrogramm der ersten 351 Wörter. Alle sieben Heine-Texte."),
            ("abb_profile_548.svg", "Abstand des ganzen Kandidaten zu jedem Text, der 548 Wörter trägt."),
            ("abb_konsens_548.svg", "Mehrheitskonsens dieser Texte und des Kandidaten. Gezeichnet sind nur Gruppen ab 50 Prozent."),
            ("abb_konsens_zeichen.svg", "Derselbe Mehrheitskonsens für die Zeichen-4-Gramme."),
            ("abb_konsens_mfw.svg", "Mehrheitskonsens über 100, 150 und 300 häufigste Wörter."),
            ("abb_profile_351.svg", "Abstand der ersten 351 Wörter des Kandidaten, alle sieben Heine-Texte."),
            ("abb_konsens_351.svg", "Mehrheitskonsens der kürzeren Proben. Das Kandidatenblatt ist der Anfang."),
        ]
    )
    print(satz_548)
    print(satz_tafel_548)
    print(satz_351)
    print(satz_tafel_351)
    print(satz_ende)
    print("Geschrieben nach", p.LAUF)


if __name__ == "__main__":
    main()
