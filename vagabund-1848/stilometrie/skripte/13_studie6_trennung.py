# -*- coding: utf-8 -*-
"""Studie 6. Liegt Steinmann außerhalb der Abstände der frühen Heine-Texte?

Steinmanns Strophenlieder sind die Fälschungsprobe. Sie wählen keine
Merkmale und gehen nicht in die Standardwerte ein. Die Heine-Dateien
bleiben einzeln. Sonette und der Kandidat bleiben draußen.

Die Regel steht in analyse/PROTOKOLL_STUDIE6.md. Sie wird hier nicht
verändert. 548 Wörter entscheiden. 351 Wörter werden berichtet.

Aufruf vom Projektordner aus:

    AUTOR_STUDIE=6 python3 analyse/13_studie6_trennung.py

Schreibt nach ergebnisse/studie6/. Studie 1 bis 5 werden nicht angefasst.
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

if os.environ.get("AUTOR_STUDIE") != "6":
    raise SystemExit("Studie 6 verlangt AUTOR_STUDIE=6, sonst läge die Dateiliste einer anderen Studie an.")

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
PROBE = ("Steinmann_Lieder.txt", "Steinmann")
ABLENKER = (
    ("Hektor_Schilda.txt", "Schilda"),
    ("Hektor_Vagabund.txt", "Vagabund"),
    ("Mueller_1.txt", "Müller"),
    ("Wunderhorn_1806.txt", "Wunderhorn"),
    ("Uhland_Lieder.txt", "Uhland"),
    ("Geibel_Junius.txt", "Junius"),
)
BOOTSTRAP = 500
KURZ = 351
HAUPT = ("Wörter 150", "Zeichen 4")

fig.FARBE.update(
    {
        "Steinmann": "#0b3a5b",
        "Schilda": "#9b3a4a",
        "Vagabund": "#b36b2a",
        "Müller": "#3d6b8a",
        "Wunderhorn": "#6e6256",
        "Uhland": "#2f6b4f",
        "Junius": "#6a4a78",
    }
)


def reine_schnitte(woerter, laenge):
    return [woerter[start : start + laenge] for start in range(0, len(woerter) - laenge + 1, laenge)]


def pruefe_liste(eintraege, erwartet, rolle):
    namen = [Path(eintrag["pfad"]).name for eintrag in eintraege]
    if namen != [datei for datei, _ in erwartet]:
        raise SystemExit(f"Die {rolle}-Dateien sind nicht die festgelegten: {namen}")


def referenz_laden():
    if g.eintraege("kandidat") or g.eintraege("hektor"):
        raise SystemExit("Studie 6 hat weder einen Kandidaten noch eine Hektor-Eichung")
    for eintrag in g.eintraege("ausgeschieden"):
        if Path(eintrag["pfad"]).name == "Kandidat_Vagabund.txt":
            continue
        g.lade_text(eintrag)
    heine_eintraege = g.eintraege("heine")
    probe_eintraege = g.eintraege("probe")
    ablenker_eintraege = g.eintraege("ablenker")
    pruefe_liste(heine_eintraege, HEINE, "Heine")
    pruefe_liste(probe_eintraege, (PROBE,), "Probe")
    pruefe_liste(ablenker_eintraege, ABLENKER, "Ablenker")
    sonett = [eintrag for eintrag in g.eintraege("ausgeschieden") if eintrag["pfad"].endswith("Steinmann_Sonette.txt")]
    if len(sonett) != 1:
        raise SystemExit("Die Sonette fehlen in der Ausscheidung")
    texte = []
    for eintrag, (_, name) in zip(heine_eintraege, HEINE):
        texte.append({"name": name, "rolle": "heine", "eintrag": eintrag, "woerter": g.lade_text(eintrag)})
    for eintrag, (_, name) in zip(probe_eintraege, (PROBE,)):
        texte.append({"name": name, "rolle": "probe", "eintrag": eintrag, "woerter": g.lade_text(eintrag)})
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


def mit_probe(bloecke, probe_woerter):
    neu = []
    for block in bloecke:
        if block["rolle"] != "probe":
            neu.append(block)
            continue
        neu.append({**block, "schnitte": [probe_woerter], "rest": len(block["woerter"]) - len(probe_woerter)})
    return neu


def eichproben(bloecke):
    proben = []
    for block in bloecke:
        if block["rolle"] == "heine":
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


def profile_und_abstand(bloecke, merkmale, art, n=None):
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
        if block["rolle"] == "heine":
            eichzeilen.append(profil)
    if len(eichzeilen) < 2 or "Steinmann" not in namen:
        raise SystemExit("Profile oder Probe fehlen")
    zeilen = np.vstack(profilzeilen)
    eichung = np.vstack(eichzeilen)
    abstand = abb.kosinus(zeilen, eichung)
    if abstand is None:
        raise SystemExit("Kosinusabstand ist nicht bestimmt")
    return namen, zeilen, eichung, abstand


def vier(wert):
    return float(f"{wert:.4f}")


def fmt(wert):
    return f"{wert:.4f}".replace(".", ",")


def heine_paare(namen, abstand, heine_namen):
    index = {name: i for i, name in enumerate(namen)}
    vorhanden = [name for name in heine_namen if name in index]
    paare = []
    for stelle, links in enumerate(vorhanden):
        for rechts in vorhanden[stelle + 1 :]:
            paare.append((links, rechts, float(abstand[index[links], index[rechts]])))
    if len(paare) < 1:
        raise SystemExit("Kein Heine-Paar")
    return vorhanden, paare


def stufe_eines_masses(namen, abstand, heine_namen):
    vorhanden, paare = heine_paare(namen, abstand, heine_namen)
    probe = namen.index("Steinmann")
    zu_heine = {name: float(abstand[probe, namen.index(name)]) for name in vorhanden}
    naechster = min(vorhanden, key=lambda name: (zu_heine[name], name))
    kleinste = vier(zu_heine[naechster])
    groesstes_paar = max(paare, key=lambda paar: (vier(paar[2]), paar[0], paar[1]))
    kleinstes_paar = min(paare, key=lambda paar: (vier(paar[2]), paar[0], paar[1]))
    aussen = kleinste > vier(groesstes_paar[2])
    ueberschuss = kleinste - vier(groesstes_paar[2])
    if aussen and ueberschuss >= vier(kleinstes_paar[2]):
        stufe = "deutlich"
    elif aussen:
        stufe = "knapp"
    else:
        stufe = "innerhalb"
    return {
        "stufe": stufe,
        "naechster": naechster,
        "kleinste": kleinste,
        "groesster": vier(groesstes_paar[2]),
        "groesstes_paar": (groesstes_paar[0], groesstes_paar[1]),
        "kleinster": vier(kleinstes_paar[2]),
        "kleinstes_paar": (kleinstes_paar[0], kleinstes_paar[1]),
        "ueberschuss": vier(ueberschuss),
        "zu_heine": {name: vier(wert) for name, wert in zu_heine.items()},
        "paare": [(links, rechts, vier(wert)) for links, rechts, wert in paare],
    }


def ausgang(wort, zeichen):
    draussen = {"deutlich", "knapp"}
    if wort["stufe"] == "deutlich" and zeichen["stufe"] == "deutlich":
        return "deutlich getrennt"
    if wort["stufe"] in draussen and zeichen["stufe"] in draussen:
        return "knapp außerhalb"
    if (wort["stufe"] in draussen) != (zeichen["stufe"] in draussen):
        return "uneinig"
    return "nicht getrennt"


def satz_ausgang(name, wort, zeichen):
    lage = ausgang(wort, zeichen)
    texte = {
        "deutlich getrennt": "Auf beiden Hauptmaßen liegt Steinmann deutlich außerhalb der Heine-Abstände.",
        "knapp außerhalb": "Auf beiden Hauptmaßen liegt Steinmann außerhalb der Heine-Abstände, aber nicht auf beiden deutlich.",
        "uneinig": "Die beiden Hauptmaße trennen Steinmann nicht gleich: eines liegt außerhalb, das andere innerhalb.",
        "nicht getrennt": "Auf beiden Hauptmaßen liegt Steinmann innerhalb der Heine-Abstände. Das Verfahren trennt diesen Text hier nicht von den Originalen.",
    }
    return lage, f"{name}: {texte[lage]}"


def naeher_als_heine(namen, abstand, heine_namen, grenze):
    probe = namen.index("Steinmann")
    andere = []
    for name in namen:
        if name == "Steinmann" or name in heine_namen:
            continue
        if vier(abstand[probe, namen.index(name)]) < grenze:
            andere.append(name)
    return andere


def mass_tabelle(wort, zeichen):
    zeilen = [
        "| Maß | nächster Heine-Text | Abstand | größtes Heine-Paar | dessen Abstand | kleinstes Heine-Paar | dessen Abstand | Überschuss | Stufe |",
        "| --- | --- | ---: | --- | ---: | --- | ---: | ---: | --- |",
    ]
    for titel, befund in (("Wörter 150", wort), ("Zeichen 4", zeichen)):
        zeilen.append(
            "| {titel} | {naechster} | {kleinste} | {gross} | {groesster} | {klein} | {kleinster} | {ueberschuss} | {stufe} |".format(
                titel=titel,
                naechster=befund["naechster"],
                kleinste=fmt(befund["kleinste"]),
                gross="–".join(befund["groesstes_paar"]),
                groesster=fmt(befund["groesster"]),
                klein="–".join(befund["kleinstes_paar"]),
                kleinster=fmt(befund["kleinster"]),
                ueberschuss=fmt(befund["ueberschuss"]),
                stufe=befund["stufe"],
            )
        )
    return "\n".join(zeilen)


def paar_tabelle(wort, zeichen):
    zeichen_nach = {(links, rechts): wert for links, rechts, wert in zeichen["paare"]}
    zeilen = ["| Heine-Paar | Wörter 150 | Zeichen 4 |", "| --- | ---: | ---: |"]
    for links, rechts, wert in sorted(wort["paare"], key=lambda paar: (paar[2], paar[0], paar[1])):
        zeilen.append(f"| {links}–{rechts} | {fmt(wert)} | {fmt(zeichen_nach[(links, rechts)])} |")
    return "\n".join(zeilen)


def abstand_zu_probe(namen, abstand):
    probe = namen.index("Steinmann")
    return {name: float(abstand[probe, i]) for i, name in enumerate(namen) if name != "Steinmann"}


def tabelle(bloecke, spalten, heine_namen):
    kopf = "| Text | Proben | ungenutzt | " + " | ".join(spalten) + " |"
    trenn = "| --- | ---: | ---: | " + " | ".join("---:" for _ in spalten) + " |"
    zeilen = [kopf, trenn]
    for block in bloecke:
        name = block["name"]
        if block["rolle"] == "probe":
            continue
        if name not in spalten["Wörter 150"]:
            zeilen.append(
                f"| {name} | 0 | {block['rest']} | " + " | ".join("—" for _ in spalten) + " |"
            )
            continue
        zellen = " | ".join(fmt(spalten[titel][name]) for titel in spalten)
        zeilen.append(f"| {name} | {len(block['schnitte'])} | {block['rest']} | {zellen} |")
    return "\n".join(zeilen)


def bestand(bloecke):
    zeilen = []
    for block in bloecke:
        anzahl = len(block["schnitte"])
        wort = "Probe" if anzahl == 1 else "Proben"
        zeilen.append(
            f"- {block['name']}: {len(block['woerter'])} Wörter, {anzahl} {wort}, {block['rest']} Wörter nicht verwendet"
        )
    return "\n".join(zeilen)


def neben_zeile(titel, befund):
    return (
        f"{titel}: nächster Heine-Text {befund['naechster']} bei {fmt(befund['kleinste'])}, "
        f"größter Heine-Abstand {fmt(befund['groesster'])}, Stufe {befund['stufe']}. Entscheidet nicht."
    )


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


def svg_balken(pfad, abstand, reihenfolge, schwelle, titel, untertitel):
    werte = [abstand[name] for name in reihenfolge]
    breite, hoehe = 760, 78 + 28 * len(reihenfolge)
    links = 150
    maximale = max(max(werte), schwelle) * 1.08
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}">',
        '<rect width="100%" height="100%" fill="#fbfbfa"/>',
        f'<text x="28" y="28" font-family="Georgia, serif" font-size="16" fill="#222">{abb.xml(titel)}</text>',
        f'<text x="28" y="48" font-family="sans-serif" font-size="12" fill="#555">{abb.xml(untertitel)}</text>',
    ]
    linie = links + schwelle / maximale * 460
    teile.append(
        f'<line x1="{linie:.1f}" y1="58" x2="{linie:.1f}" y2="{hoehe - 16}" stroke="#222" stroke-dasharray="3 3"/>'
    )
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
<title>Studie 6, Abbildungen</title>
<style>
body { font-family: Georgia, serif; max-width: 980px; margin: 32px auto; color: #222; background: #fbfbfa; }
figcaption { font-family: sans-serif; font-size: 14px; color: #333; margin: 8px 0 28px; }
img { max-width: 100%; height: auto; border: 1px solid #e4e0d8; }
</style>
<h1>Studie 6, Abbildungen</h1>
<p>Steinmann ist die Fälschungsprobe. Die gestrichelte Linie ist der größte Abstand zweier Heine-Texte auf diesem Maß. Die Bilder ändern die Studien 1 bis 5 nicht.</p>
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
                "baum_seed": [p.SEED, 6],
                "probenlaenge": p.PROBENLAENGE,
                "nebenlaenge": KURZ,
                "mfw": p.MFW,
                "mfw_bericht": list(p.MFW_BERICHT),
                "zeichen_n": p.ZEICHEN_N,
                "zeichen_n_bericht": list(p.ZEICHEN_N_BERICHT),
                "zeichen_haeufigste": p.ZEICHEN_HAEUFIGSTE,
                "versatz": 0,
                "eichung": "nur Heine-Profile der Tafel",
                "entscheidung": "548, Wörter 150 und Zeichen 4",
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
    probe = next(text for text in texte if text["rolle"] == "probe")
    if len(probe["woerter"]) != probe["eintrag"]["wortzahl"]:
        raise SystemExit("Steinmann hat nicht die Wortzahl der Dateiliste")
    haupt = len(probe["woerter"]) >= p.PROBENLAENGE
    if haupt and reine_schnitte(probe["woerter"], p.PROBENLAENGE) != [probe["woerter"][: p.PROBENLAENGE]]:
        raise SystemExit("Die Hauptprobe ist nicht die erste Scheibe")
    if len(probe["woerter"]) < KURZ:
        raise SystemExit("Steinmann trägt keine Probe von 351 Wörtern")

    bloecke_351 = scheiben(texte, KURZ)
    eich_351 = eichproben(bloecke_351)
    worte_351 = g.merkmal_woerter(eich_351, 300)
    zeichen_351 = {n: g.merkmal_ngramme(eich_351, n, p.ZEICHEN_HAEUFIGSTE) for n in (p.ZEICHEN_N, *p.ZEICHEN_N_BERICHT)}
    bloecke_548 = scheiben(texte, p.PROBENLAENGE) if haupt else None
    eich_548 = eichproben(bloecke_548) if haupt else None
    worte_548 = g.merkmal_woerter(eich_548, 300) if haupt else None
    zeichen_548 = (
        {n: g.merkmal_ngramme(eich_548, n, p.ZEICHEN_HAEUFIGSTE) for n in (p.ZEICHEN_N, *p.ZEICHEN_N_BERICHT)}
        if haupt
        else None
    )

    def spalten_fuer(bloecke, eich_worte, eich_zeichen):
        spalten = {}
        pack = {}
        for anzahl, titel in ((150, "Wörter 150"), (100, "Wörter 100"), (300, "Wörter 300")):
            namen, zeilen, eichung, abstand = profile_und_abstand(bloecke, eich_worte[:anzahl], "woerter")
            spalten[titel] = abstand_zu_probe(namen, abstand)
            pack[titel] = (namen, zeilen, eichung, abstand)
        for n, titel in ((4, "Zeichen 4"), (3, "Zeichen 3"), (5, "Zeichen 5")):
            namen, zeilen, eichung, abstand = profile_und_abstand(bloecke, eich_zeichen[n], "zeichen", n)
            spalten[titel] = abstand_zu_probe(namen, abstand)
            pack[titel] = (namen, zeilen, eichung, abstand)
        namen_i, zeilen_i, eichung_i, abstand_i = profile_und_abstand(bloecke, None, "interpunktion")
        spalten["Interpunktion"] = abstand_zu_probe(namen_i, abstand_i)
        pack["Interpunktion"] = (namen_i, zeilen_i, eichung_i, abstand_i)
        return spalten, pack

    anfang_351 = probe["woerter"][:KURZ]
    ende_351 = probe["woerter"][-KURZ:]
    spalten_anfang, pack_anfang = spalten_fuer(mit_probe(bloecke_351, anfang_351), worte_351, zeichen_351)
    spalten_ende, pack_ende = spalten_fuer(mit_probe(bloecke_351, ende_351), worte_351, zeichen_351)
    if haupt:
        anfang_548 = probe["woerter"][: p.PROBENLAENGE]
        spalten_548, pack_548 = spalten_fuer(mit_probe(bloecke_548, anfang_548), worte_548, zeichen_548)
    else:
        anfang_548 = None
        spalten_548, pack_548 = None, None

    def befund(pack, schluessel):
        namen, _, _, abstand = pack[schluessel]
        return namen, stufe_eines_masses(namen, abstand, heine_namen)

    namen_351, wort_351 = befund(pack_anfang, "Wörter 150")
    _, zeichen_351_befund = befund(pack_anfang, "Zeichen 4")
    _, wort_ende = befund(pack_ende, "Wörter 150")
    _, zeichen_ende = befund(pack_ende, "Zeichen 4")
    lage_351, satz_351 = satz_ausgang("351 Wörter, Anfang", wort_351, zeichen_351_befund)
    lage_ende, satz_ende = satz_ausgang("351 Wörter, Ende", wort_ende, zeichen_ende)
    if haupt:
        namen_548, wort_548 = befund(pack_548, "Wörter 150")
        _, zeichen_548_befund = befund(pack_548, "Zeichen 4")
        lage_548, satz_548 = satz_ausgang("548 Wörter", wort_548, zeichen_548_befund)
    else:
        namen_548, wort_548, zeichen_548_befund = None, None, None
        lage_548 = "keine Probe"
        satz_548 = (
            f"Steinmann hat {len(probe['woerter'])} Wörter und trägt keine Probe von {p.PROBENLAENGE} Wörtern. "
            "Die Haupttabelle wird nicht gebildet. Die Datei wird nicht auf diese Länge gedehnt."
        )

    def fremde(pack, befund_wort, befund_zeichen):
        namen, _, _, abstand_w = pack["Wörter 150"]
        _, _, _, abstand_z = pack["Zeichen 4"]
        return (
            naeher_als_heine(namen, abstand_w, set(heine_namen), befund_wort["kleinste"]),
            naeher_als_heine(namen, abstand_z, set(heine_namen), befund_zeichen["kleinste"]),
        )

    fremd_351_w, fremd_351_z = fremde(pack_anfang, wort_351, zeichen_351_befund)
    if haupt:
        fremd_w, fremd_z = fremde(pack_548, wort_548, zeichen_548_befund)
    else:
        fremd_w, fremd_z = [], []

    def fremd_satz(liste, mass):
        if not liste:
            return f"Auf {mass} liegt kein anderer Text der Tafel näher an Steinmann als der nächste Heine-Text."
        return f"Auf {mass} liegen näher an Steinmann als der nächste Heine-Text: {', '.join(liste)}."

    for alt in p.LAUF.glob("abb_*"):
        alt.unlink()
    for name in ("548_abstaende.csv", "548_heine_paare.csv"):
        ziel = p.LAUF / name
        if ziel.exists():
            ziel.unlink()
    if haupt:
        schreibe_csv(p.LAUF / "548_abstaende.csv", mit_probe(bloecke_548, anfang_548), spalten_548)
        with (p.LAUF / "548_heine_paare.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["links", "rechts", "woerter_150", "zeichen_4"])
            zeichen_nach = {(links, rechts): wert for links, rechts, wert in zeichen_548_befund["paare"]}
            for links, rechts, wert in wort_548["paare"]:
                writer.writerow([links, rechts, f"{wert:.4f}", f"{zeichen_nach[(links, rechts)]:.4f}"])
    schreibe_csv(p.LAUF / "351_anfang_abstaende.csv", mit_probe(bloecke_351, anfang_351), spalten_anfang)
    schreibe_csv(p.LAUF / "351_ende_abstaende.csv", mit_probe(bloecke_351, ende_351), spalten_ende)

    rng = np.random.default_rng(np.random.SeedSequence([p.SEED, 6]))
    csv_zeilen = []

    def baum(pack, schluessel, abbildung, titel, untertitel, datei):
        namen, zeilen, eichung, _ = pack[schluessel]
        baeume, gewaehlt, referenz = zeichne_konsens(
            zeilen, eichung, namen, rng, titel, untertitel, p.LAUF / datei
        )
        csv_zeilen.extend(kladen_zeilen(abbildung, gewaehlt, namen))
        abb.svg_dendrogramm(
            abb.upgma(abb.kosinus(zeilen, eichung)),
            namen,
            abb.anteile_der_kladen(baeume),
            titel.replace("Konsens", "Dendrogramm"),
            "UPGMA auf dem Cosine Delta. Die Zahl ist der Anteil der 500 Bäume in Prozent.\nWaagerecht die Gruppierungshöhe. Eine hellere Zahl liegt unter 50 Prozent.",
            p.LAUF / datei.replace("abb_konsens", "abb_dendrogramm"),
            fig.farbe_von_etikett,
        )
        abb.svg_stern(
            abb.baum_aus_kladen(gewaehlt, namen, referenz),
            namen,
            None,
            titel.replace("Konsens", "Stern"),
            "Mehrheitskonsens. Gleiche Astlänge, keine Distanz. Nur Gruppen ab 50 Prozent.",
            p.LAUF / datei.replace("abb_konsens", "abb_stern_konsens"),
            fig.farbe_von_etikett,
            art="gleich",
        )
        abb.svg_stern(
            abb.upgma(abb.kosinus(zeilen, eichung)),
            namen,
            abb.anteile_der_kladen(baeume),
            titel.replace("Konsens", "Stern nach der Gruppierungshöhe"),
            "Die Mitte ist die letzte UPGMA-Gruppe. Die Astlänge ist die Gruppierungshöhe. Zahlen ab 50.",
            p.LAUF / datei.replace("abb_konsens", "abb_stern"),
            fig.farbe_von_etikett,
            art="hoehe",
        )
        return baeume, namen, referenz

    if haupt:
        baum(
            pack_548,
            "Wörter 150",
            "548_woerter",
            "Konsens, 548 Wörter",
            "Steinmann ist eine Probe. Die Eichung zählt jeden Heine-Text dieser Tafel einmal.\nBiene, Kevlaar und Donna Clara sind kürzer und fehlen.",
            "abb_konsens_548.svg",
        )
        baum(
            pack_548,
            "Zeichen 4",
            "548_zeichen",
            "Konsens nach Zeichen-4-Grammen, 548 Wörter",
            "Eine Probe Steinmann. 500 Bäume, 500 häufigste 4-Gramme. Die Eichung ist nur Heine.",
            "abb_konsens_zeichen.svg",
        )
        leiter = []
        for schluessel in ("Wörter 100", "Wörter 150", "Wörter 300"):
            namen, zeilen, eichung, _ = pack_548[schluessel]
            leiter.append(abb.kladen(abb.upgma(abb.kosinus(zeilen, eichung))))
        gewaehlt_leiter, _ = abb.mehrheit(leiter, len(namen))
        referenz_leiter = abb.blattordnung(abb.upgma(abb.kosinus(pack_548["Wörter 150"][1], pack_548["Wörter 150"][2])))
        fig.svg_baum(
            abb.baum_aus_kladen(gewaehlt_leiter, namen, referenz_leiter),
            "Konsens über die Merkmalleiter, 548 Wörter",
            "Drei Bäume, für 100, 150 und 300 häufigste Wörter. Eine Zahl 100 heißt: der Ast steht in allen drei.",
            p.LAUF / "abb_konsens_mfw.svg",
        )
        csv_zeilen.extend(kladen_zeilen("548_mfw", gewaehlt_leiter, namen))
        _, zeilen_mfw, eichung_mfw, _ = pack_548["Wörter 150"]
        abb.svg_dendrogramm(
            abb.upgma(abb.kosinus(zeilen_mfw, eichung_mfw)),
            namen,
            abb.anteile_der_kladen(leiter),
            "Dendrogramm der Merkmalleiter, 548 Wörter",
            "UPGMA der 150 Wörter. Die Zahl ist der Anteil der drei Merkmalzahlen in Prozent.",
            p.LAUF / "abb_dendrogramm_mfw.svg",
            fig.farbe_von_etikett,
        )
        abb.svg_stern(
            abb.baum_aus_kladen(gewaehlt_leiter, namen, referenz_leiter),
            namen,
            None,
            "Merkmalleiter, sternförmig",
            "Mehrheitskonsens der drei Merkmalzahlen. Gleiche Astlänge, keine Distanz.",
            p.LAUF / "abb_stern_konsens_mfw.svg",
            fig.farbe_von_etikett,
            art="gleich",
        )
        abb.svg_stern(
            abb.upgma(abb.kosinus(zeilen_mfw, eichung_mfw)),
            namen,
            abb.anteile_der_kladen(leiter),
            "Merkmalleiter, sternförmig nach der Gruppierungshöhe",
            "UPGMA der 150 Wörter. Die Zahl ist der Anteil der drei Merkmalzahlen.",
            p.LAUF / "abb_stern_mfw.svg",
            fig.farbe_von_etikett,
            art="hoehe",
        )
    baum(
        pack_anfang,
        "Wörter 150",
        "351_woerter",
        "Konsens, 351 Wörter",
        "Alle sieben Heine-Texte. Steinmann sind die ersten 351 Wörter.\n500 Bäume. Diese Tafel entscheidet nicht.",
        "abb_konsens_351.svg",
    )

    if haupt:
        reihe_548 = [name for name in namen_548 if name != "Steinmann"]
        svg_balken(
            p.LAUF / "abb_profile_548.svg",
            spalten_548["Wörter 150"],
            sorted(reihe_548, key=lambda name: spalten_548["Wörter 150"][name]),
            wort_548["groesster"],
            "Abstand Steinmanns, 548 Wörter",
            "Cosine Delta, 150 Wörter. Die Linie ist der größte Abstand zweier Heine-Texte.",
        )
        svg_balken(
            p.LAUF / "abb_profile_zeichen.svg",
            spalten_548["Zeichen 4"],
            sorted(reihe_548, key=lambda name: spalten_548["Zeichen 4"][name]),
            zeichen_548_befund["groesster"],
            "Abstand Steinmanns, Zeichen-4-Gramme",
            "Cosine Delta, 500 häufigste 4-Gramme. Die Linie ist der größte Abstand zweier Heine-Texte.",
        )
    reihe_351 = [name for name in namen_351 if name != "Steinmann"]
    svg_balken(
        p.LAUF / "abb_profile_351.svg",
        spalten_anfang["Wörter 150"],
        sorted(reihe_351, key=lambda name: spalten_anfang["Wörter 150"][name]),
        wort_351["groesster"],
        "Abstand der ersten 351 Wörter Steinmanns",
        "Diese Tafel entscheidet nicht. Die Linie ist der größte Abstand zweier Heine-Texte.",
    )

    probe_eintrag = probe["eintrag"]
    with (p.LAUF / "eingaben.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["pfad", "rolle", "wortzahl", "sha256", "in_der_merkmalliste"],
        )
        writer.writeheader()
        for zeile in g.dateiliste():
            if Path(zeile["pfad"]).name == "Kandidat_Vagabund.txt":
                writer.writerow(
                    {
                        "pfad": zeile["pfad"],
                        "rolle": zeile["rolle"],
                        "wortzahl": zeile["wortzahl"],
                        "sha256": "",
                        "in_der_merkmalliste": "nein",
                    }
                )
                continue
            writer.writerow(
                {
                    "pfad": zeile["pfad"],
                    "rolle": zeile["rolle"],
                    "wortzahl": zeile["wortzahl"],
                    "sha256": g.pruefsumme(g.pfad_zu(zeile)),
                    "in_der_merkmalliste": "ja" if zeile["rolle"] == "heine" else "nein",
                }
            )

    with (p.LAUF / "konsens_kladen.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["abbildung", "klade", "anteil"])
        writer.writeheader()
        writer.writerows(csv_zeilen)

    neben_pack = pack_548 if haupt else pack_anfang
    neben = []
    for schluessel in ("Wörter 100", "Wörter 300", "Zeichen 3", "Zeichen 5", "Interpunktion"):
        namen, _, _, abstand = neben_pack[schluessel]
        zeile = neben_zeile(schluessel, stufe_eines_masses(namen, abstand, heine_namen))
        if schluessel == "Interpunktion":
            zeile += " Die Interpunktion reiht nicht."
        neben.append(zeile)

    if haupt:
        kopf_548 = [
            "## 548 Wörter",
            "",
            "Das ist die Haupttabelle. Biene, Kevlaar und Donna Clara bleiben darunter. Von Steinmann ist die erste Probe verwendet. "
            + str(len(probe["woerter"]) - p.PROBENLAENGE)
            + " Wörter bleiben liegen.",
            "",
            bestand(mit_probe(bloecke_548, anfang_548)),
            "",
            satz_548,
            "",
            fremd_satz(fremd_w, "den 150 Wörtern"),
            fremd_satz(fremd_z, "den Vierergruppen"),
            "",
            mass_tabelle(wort_548, zeichen_548_befund),
            "",
            "Abstände der Heine-Texte untereinander:",
            "",
            paar_tabelle(wort_548, zeichen_548_befund),
            "",
            "Abstand Steinmanns zu jedem Text der Tafel:",
            "",
            tabelle(mit_probe(bloecke_548, anfang_548), spalten_548, heine_namen),
            "",
            "Nebenmaße, sie entscheiden nicht:",
            "",
            "\n".join(f"- {zeile}" for zeile in neben),
            "",
        ]
    else:
        kopf_548 = [
            "## 548 Wörter",
            "",
            satz_548,
            "",
            "Die Nebentafel mit 351 Wörtern wird gerechnet. Sie tritt nicht an die Stelle der Haupttabelle.",
            "",
        ]

    text = "\n".join(
        [
            "# Studie 6. Original und Steinmann",
            "",
            "Steinmann schreibt die Gedichte Heine zu. Diese Studie behandelt die Strophenlieder als Fälschungsprobe. Sie wählt keine Merkmale und geht nicht in die Standardwerte ein. Die Eichung zählt jeden Heine-Text der Tafel einmal. Die Sonette und der Kandidat sind nicht gerechnet. Studie 1 bis 5 sind nicht neu gerechnet. Ein Text mit einer Probe ist keine Fälschungsrate.",
            "",
            f"Prüfsumme der Probe: {g.pruefsumme(g.pfad_zu(probe_eintrag))}.",
            "",
            *kopf_548,
            "## 351 Wörter, Anfang",
            "",
            "Alle sieben Heine-Texte. Von Steinmann die ersten 351 Wörter. Diese Tafel entscheidet die Haupttabelle nicht.",
            "",
            bestand(mit_probe(bloecke_351, anfang_351)),
            "",
            satz_351,
            "",
            fremd_satz(fremd_351_w, "den 150 Wörtern"),
            fremd_satz(fremd_351_z, "den Vierergruppen"),
            "",
            mass_tabelle(wort_351, zeichen_351_befund),
            "",
            tabelle(mit_probe(bloecke_351, anfang_351), spalten_anfang, heine_namen),
            "",
            *([] if haupt else [
                "Nebenmaße dieser Tafel, sie entscheiden nicht:",
                "",
                "\n".join(f"- {zeile}" for zeile in neben),
                "",
            ]),
            "## 351 Wörter, Ende",
            "",
            "Die letzten 351 Wörter überlappen die ersten. Sie entscheiden nicht.",
            "",
            satz_ende,
            "",
            mass_tabelle(wort_ende, zeichen_ende),
            "",
            tabelle(mit_probe(bloecke_351, ende_351), spalten_ende, heine_namen),
            "",
            f"Ausgang der Haupttabelle: {lage_548}. Die Nebentafel am Anfang lautet: {lage_351}. Das Ende lautet: {lage_ende}. Die Abstände stehen auf der Skala dieser Studie. Sie sind nicht die Profilabstände aus Studie 1 bis 5.",
            "",
        ]
    )
    (p.LAUF / "NAEHE.md").write_text(text, encoding="utf-8")
    bilder = [
        ("abb_stern_351.svg", "Sternförmiger Baum der ersten 351 Wörter. Entscheidet die Haupttabelle nicht."),
        ("abb_stern_konsens_351.svg", "Mehrheitsstern der kürzeren Proben."),
        ("abb_dendrogramm_351.svg", "Dendrogramm der ersten 351 Wörter."),
        ("abb_profile_351.svg", "Abstand der ersten 351 Wörter. Entscheidet die Haupttabelle nicht."),
        ("abb_konsens_351.svg", "Mehrheitskonsens der kürzeren Proben."),
    ]
    if haupt:
        bilder = [
            ("abb_profile_548.svg", "Abstand Steinmanns zu 548 Wörtern. Die Linie ist der größte Heine-Abstand auf den 150 Wörtern."),
            ("abb_profile_zeichen.svg", "Derselbe Abstand auf den Zeichen-4-Grammen."),
            ("abb_stern_548.svg", "Sternförmiger UPGMA-Baum. Die Astlänge ist die Gruppierungshöhe."),
            ("abb_stern_zeichen.svg", "Derselbe sternförmige Baum für die Zeichen-4-Gramme."),
            ("abb_stern_mfw.svg", "Sternförmiger Baum der 150 häufigsten Wörter."),
            ("abb_stern_konsens_548.svg", "Dieselbe Mehrheit als Stern. Die Astlänge ist keine Distanz."),
            ("abb_stern_konsens_zeichen.svg", "Mehrheitsstern der Zeichen-4-Gramme."),
            ("abb_stern_konsens_mfw.svg", "Mehrheitsstern über 100, 150 und 300 häufigste Wörter."),
            ("abb_dendrogramm_548.svg", "Dendrogramm. Die Achse ist die Gruppierungshöhe."),
            ("abb_dendrogramm_zeichen.svg", "Dasselbe Dendrogramm für die Zeichen-4-Gramme."),
            ("abb_dendrogramm_mfw.svg", "Dendrogramm der Merkmalleiter."),
            ("abb_konsens_548.svg", "Mehrheitskonsens. Gezeichnet sind nur Gruppen ab 50 Prozent."),
            ("abb_konsens_zeichen.svg", "Derselbe Mehrheitskonsens für die Zeichen-4-Gramme."),
            ("abb_konsens_mfw.svg", "Mehrheitskonsens über 100, 150 und 300 häufigste Wörter."),
        ] + bilder
    html_uebersicht(bilder)
    print(satz_548)
    if haupt:
        print(fremd_satz(fremd_w, "den 150 Wörtern"))
        print(fremd_satz(fremd_z, "den Vierergruppen"))
    print(satz_351)
    print(fremd_satz(fremd_351_w, "den 150 Wörtern dieser Tafel"))
    print(fremd_satz(fremd_351_z, "den Vierergruppen dieser Tafel"))
    print(satz_ende)
    print("Geschrieben nach", p.LAUF)


if __name__ == "__main__":
    main()
