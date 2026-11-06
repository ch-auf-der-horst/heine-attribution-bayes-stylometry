# -*- coding: utf-8 -*-
"""Abbildungen zu den Abständen der frühen Heine-Texte.

Dieselben Bäume wie in den Studien. Das Dendrogramm ist der UPGMA-Baum;
die waagerechte Achse ist die Gruppierungshöhe, an jeder Gabel steht der
Bootstrap-Anteil. Der Mehrheitskonsens zeichnet nur Äste ab 50 Prozent.
Dazu die Merkmalleiter aus 100, 150 und 300 Wörtern, das Wärmebild der
Proben und die Abstände innerhalb eines Textes gegen die Abstände
zwischen den Texten.

Die Proben überschreiten keine Textgrenze. Der Kandidat wird nicht gelesen.
Der Zufallsstrom ist SeedSequence([Seed der Studie, 9]) und berührt die
Läufe der Studien nicht.

Schreibt nach ergebnisse/heine_texte/.
"""

import csv
import html
import importlib.util
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g

_spec = importlib.util.spec_from_file_location(
    "abbildungen", Path(__file__).resolve().parent / "08_abbildungen.py"
)
abb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(abb)

_heine_spec = importlib.util.spec_from_file_location(
    "heine_texte", Path(__file__).resolve().parent / "09_heine_texte.py"
)
heine = importlib.util.module_from_spec(_heine_spec)
_heine_spec.loader.exec_module(heine)

ORDNER = p.PROJEKT / "ergebnisse" / "heine_texte"
BOOTSTRAP = 500
FARBE = {
    "Aurora": "#1f4e79",
    "Biene": "#8a6a12",
    "Almanach": "#2f5d50",
    "Agrippina": "#5c4a6a",
    "Heimkehr": "#8c3a2f",
    "Kevlaar": "#3d5a3d",
    "Donna Clara": "#4a5568",
}


def proben_der_laenge(laenge):
    etiketten = []
    proben = []
    gruppen = defaultdict(list)
    for text in heine.texte_laden():
        schnitte = heine.reine_schnitte(text["woerter"], laenge)
        for nummer, schnitt in enumerate(schnitte, start=1):
            etikett = text["name"] if len(schnitte) == 1 else f"{text['name']} {nummer}"
            gruppen[text["name"]].append(len(etiketten))
            etiketten.append(etikett)
            proben.append(schnitt)
    return etiketten, proben, gruppen


def profile(proben, gruppen, merkmale, matrix):
    zeilen = []
    namen = []
    for name, indizes in gruppen.items():
        namen.append(name)
        zeilen.append(matrix([proben[i] for i in indizes], merkmale).mean(axis=0))
    return namen, np.vstack(zeilen)


def konsens(relativ, etiketten, rng, eichung=None):
    if eichung is None:
        eichung = relativ
    primaer = abb.kosinus(relativ, eichung)
    referenz = abb.blattordnung(abb.upgma(primaer))
    baeume = abb.bootstrap_baeume([relativ], np.arange(eichung.shape[0]), rng)
    # Die Eichzeilen müssen zur ersten Matrix passen. Bei getrennter Eichung
    # wird unten selbst gezogen.
    gewaehlt, _ = abb.mehrheit(baeume, len(etiketten))
    return baeume, gewaehlt, referenz


def bootstrap_mit_eichung(relativ, eichung, rng):
    spalten = relativ.shape[1]
    baeume = []
    for _ in range(BOOTSTRAP):
        maske = rng.random(spalten) < abb.MERKMALANTEIL
        if int(maske.sum()) < 8:
            continue
        abstand = abb.kosinus(relativ[:, maske], eichung[:, maske])
        if abstand is None:
            continue
        baeume.append(abb.kladen(abb.upgma(abstand)))
    if len(baeume) < BOOTSTRAP * 0.9:
        raise SystemExit("Zu viele Bootstrap-Ziehungen ohne Streuung")
    return baeume


def anteil_ganzer_text(baeume, gruppen):
    saetze = []
    for name, indizes in gruppen.items():
        if len(indizes) < 2:
            continue
        ziel = frozenset(indizes)
        anteil = sum(ziel in baum for baum in baeume) / len(baeume)
        saetze.append(f"{name} {anteil:.0%}")
    return saetze


def farbe_von_etikett(etikett):
    for name in sorted(FARBE, key=len, reverse=True):
        if etikett == name or etikett.startswith(name + " "):
            return FARBE[name]
    return "#5c564e"


def svg_baum(wurzel, titel, untertitel, pfad):
    abb.svg_baum(wurzel, titel, untertitel, pfad, farbe_von=farbe_von_etikett)


def dendrogramm(abstand, etiketten, baeume, titel, untertitel, pfad):
    abb.svg_dendrogramm(
        abb.upgma(abstand),
        etiketten,
        abb.anteile_der_kladen(baeume),
        titel,
        untertitel,
        pfad,
        farbe_von_etikett,
    )


def stern(abstand, etiketten, baeume, titel, untertitel, pfad):
    abb.svg_stern(
        abb.upgma(abstand),
        etiketten,
        abb.anteile_der_kladen(baeume),
        titel,
        untertitel,
        pfad,
        farbe_von=farbe_von_etikett,
        art="hoehe",
    )


def zeichne_konsens(relativ, etiketten, gruppen, rng, titel, untertitel, pfad, eichung=None):
    if eichung is None:
        baeume, gewaehlt, referenz = konsens(relativ, etiketten, rng)
    else:
        primaer = abb.kosinus(relativ, eichung)
        referenz = abb.blattordnung(abb.upgma(primaer))
        baeume = bootstrap_mit_eichung(relativ, eichung, rng)
        gewaehlt, _ = abb.mehrheit(baeume, len(etiketten))
    svg_baum(abb.baum_aus_kladen(gewaehlt, etiketten, referenz), titel, untertitel, pfad)
    return baeume, gewaehlt


def svg_abstaende(pfad, abstand, gruppen):
    gleich, verschieden = [], []
    namen = list(gruppen)
    index = {name: set(indizes) for name, indizes in gruppen.items()}
    n = abstand.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            gleicher_text = any(i in menge and j in menge for menge in index.values())
            (gleich if gleicher_text else verschieden).append(float(abstand[i, j]))
    breite, hoehe = 720, 250
    links, rechts = 170, 30

    def x(wert):
        return links + min(max(wert, 0.0), 2.0) / 2.0 * (breite - links - rechts)

    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}">',
        '<rect width="100%" height="100%" fill="#fbfbfa"/>',
        '<text x="28" y="28" font-family="Georgia, serif" font-size="16" fill="#222">Abstände der reinen Proben</text>',
        '<text x="28" y="48" font-family="sans-serif" font-size="12" fill="#555">351 Wörter, 150 häufigste Wörter. Kleinere Werte sind näher.</text>',
        '<text x="28" y="100" font-family="sans-serif" font-size="13" fill="#1f4e79">innerhalb eines Textes</text>',
        '<text x="28" y="170" font-family="sans-serif" font-size="13" fill="#8c3a2f">zwischen zwei Texten</text>',
    ]
    for wert in gleich:
        teile.append(f'<circle cx="{x(wert):.1f}" cy="108" r="3.5" fill="#1f4e79" opacity="0.45"/>')
    for wert in verschieden:
        teile.append(f'<circle cx="{x(wert):.1f}" cy="178" r="3.5" fill="#8c3a2f" opacity="0.35"/>')
    for werte, y, farbe in ((gleich, 108, "#1f4e79"), (verschieden, 178, "#8c3a2f")):
        teile.append(f'<line x1="{x(float(np.median(werte))):.1f}" y1="{y - 16}" x2="{x(float(np.median(werte))):.1f}" y2="{y + 16}" stroke="{farbe}" stroke-width="2"/>')
    teile.append("</svg>")
    g.schreibe_svg(pfad, "\n".join(teile) + "\n")
    return namen


def svg_waerme(pfad, abstand, etiketten):
    n = len(etiketten)
    werte = abstand[np.triu_indices(n, 1)]
    vmin, vmax = float(werte.min()), float(werte.max())
    kante = 16 if n > 12 else 28
    links, oben = 108, 108
    breite = links + n * kante + 28
    hoehe = oben + n * kante + 28
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}">',
        '<rect width="100%" height="100%" fill="#fbfbfa"/>',
        '<text x="28" y="28" font-family="Georgia, serif" font-size="16" fill="#222">Wortabstände der reinen Proben</text>',
        '<text x="28" y="48" font-family="sans-serif" font-size="12" fill="#555">351 Wörter. Hell ist nah, dunkel ist fern. Proben desselben Textes stehen beieinander.</text>',
    ]
    for i, name in enumerate(etiketten):
        teile.append(
            f'<text x="{links + i * kante + kante}" y="{oben - 6}" text-anchor="end" transform="rotate(-55 {links + i * kante + 4} {oben - 6})" font-family="sans-serif" font-size="10" fill="#444">{abb.xml(name)}</text>'
        )
        teile.append(
            f'<text x="{links - 6}" y="{oben + i * kante + 12}" text-anchor="end" font-family="sans-serif" font-size="10" fill="#444">{abb.xml(name)}</text>'
        )
    for i in range(n):
        for j in range(n):
            t = 0.0 if i == j else (abstand[i, j] - vmin) / (vmax - vmin)
            rot = int(255 - t * 210)
            gruen = int(247 - t * 180)
            blau = int(236 - t * 140)
            teile.append(
                f'<rect x="{links + j * kante}" y="{oben + i * kante}" width="{kante - 1}" height="{kante - 1}" '
                f'fill="rgb({rot},{gruen},{blau})"/>'
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
<title>Heine-Texte, Abbildungen</title>
<style>
body { font-family: Georgia, serif; max-width: 980px; margin: 32px auto; color: #222; background: #fbfbfa; }
figcaption { font-family: sans-serif; font-size: 14px; color: #333; margin: 8px 0 28px; }
img { max-width: 100%; height: auto; border: 1px solid #e4e0d8; }
</style>
<h1>Frühe Heine-Texte, Abbildungen</h1>
<p>Jede Probe liegt in genau einem Text. Die Bilder ändern die drei Studien nicht. Impostors und der Kandidat gehören nicht in diese Vorprüfung.</p>
""" + "\n".join(bloecke) + "\n</html>\n"
    (ORDNER / "abb_uebersicht.html").write_text(text, encoding="utf-8")


def kladen_zeilen(abbildung, gewaehlt, etiketten):
    zeilen = []
    for klade, anteil in gewaehlt:
        namen = ", ".join(etiketten[i] for i in sorted(klade))
        zeilen.append({"abbildung": abbildung, "klade": namen, "anteil": f"{anteil:.4f}"})
    return zeilen


def main():
    abb.selbsttest()
    ORDNER.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(np.random.SeedSequence([p.SEED, 9]))
    csv_zeilen = []

    for laenge, datei, titel in (
        (548, "abb_konsens_548.svg", "Konsens der Proben zu 548 Wörtern"),
        (351, "abb_konsens_351.svg", "Konsens der Proben zu 351 Wörtern"),
    ):
        etiketten, proben, gruppen = proben_der_laenge(laenge)
        merkmale = g.merkmal_woerter(proben, p.MFW)
        relativ = g.matrix_woerter(proben, merkmale)
        baeume, gewaehlt, referenz = konsens(relativ, etiketten, rng)
        teile = anteil_ganzer_text(baeume, gruppen)
        untertitel = (
            f"{len(baeume)} Bäume, 150 Wörter, Merkmalanteil 0,5. Gezeichnet sind Äste ab 50%.\n"
            + (
                "Ein Text mit mehreren Proben steht als ganze Gruppe in: " + ", ".join(teile) + "."
                if teile
                else "Kein Text hat mehr als eine Probe."
            )
        )
        svg_baum(
            abb.baum_aus_kladen(gewaehlt, etiketten, referenz),
            titel,
            untertitel,
            ORDNER / datei,
        )
        dendrogramm(
            abb.kosinus(relativ, relativ),
            etiketten,
            baeume,
            titel.replace("Konsens", "Dendrogramm"),
            "UPGMA auf dem Cosine Delta der 150 Wörter. Die Zahl ist der Anteil der Bootstrap-Bäume in Prozent.\nWaagerecht die Gruppierungshöhe. Eine hellere Zahl liegt unter 50 Prozent.",
            ORDNER / datei.replace("abb_konsens", "abb_dendrogramm"),
        )
        abb.svg_stern(
            abb.baum_aus_kladen(gewaehlt, etiketten, referenz),
            etiketten,
            None,
            titel.replace("Konsens", "Stern"),
            "Mehrheitskonsens. Gleiche Astlänge, keine Distanz. Nur Gruppen ab 50 Prozent.",
            ORDNER / datei.replace("abb_konsens", "abb_stern_konsens"),
            farbe_von=farbe_von_etikett,
            art="gleich",
        )
        stern(
            abb.kosinus(relativ, relativ),
            etiketten,
            baeume,
            titel.replace("Konsens", "Stern nach der Gruppierungshöhe"),
            "Die Mitte ist die letzte UPGMA-Gruppe. Die Astlänge ist die Gruppierungshöhe. Zahlen ab 50.",
            ORDNER / datei.replace("abb_konsens", "abb_stern"),
        )
        csv_zeilen.extend(kladen_zeilen(f"proben_{laenge}", gewaehlt, etiketten))
        if laenge == 351:
            abstand = abb.kosinus(relativ, relativ)
            svg_abstaende(ORDNER / "abb_abstaende.svg", abstand, gruppen)
            svg_waerme(ORDNER / "abb_waerme.svg", abstand, etiketten)
            merkmal_leiter = g.merkmal_woerter(proben, 300)
            profil_namen = list(gruppen)
            wort_profil = {}
            for anzahl in (100, 150, 300):
                namen, matrix = profile(
                    proben,
                    gruppen,
                    merkmal_leiter[:anzahl],
                    lambda stuecke, merkmale: g.matrix_woerter(stuecke, merkmale),
                )
                profil_namen = namen
                wort_profil[anzahl] = matrix
            baeume_p, gewaehlt_p = zeichne_konsens(
                wort_profil[150],
                profil_namen,
                {name: [i] for i, name in enumerate(profil_namen)},
                rng,
                "Konsens der sieben Texte",
                f"Ein Blatt je Text, Mittel der Proben zu 351 Wörtern.\n{BOOTSTRAP} Bäume, 150 häufigste Wörter. Die Normierung wiegt jeden Text einmal.",
                ORDNER / "abb_konsens_profile.svg",
            )
            csv_zeilen.extend(kladen_zeilen("profile_woerter", gewaehlt_p, profil_namen))
            dendrogramm(
                abb.kosinus(wort_profil[150], wort_profil[150]),
                profil_namen,
                baeume_p,
                "Dendrogramm der sieben Texte",
                "UPGMA, ein Blatt je Text. Die Zahl ist der Anteil der Bootstrap-Bäume in Prozent.\nWaagerecht die Gruppierungshöhe. Eine hellere Zahl liegt unter 50 Prozent.",
                ORDNER / "abb_dendrogramm_profile.svg",
            )
            stern(
                abb.kosinus(wort_profil[150], wort_profil[150]),
                profil_namen,
                baeume_p,
                "Sieben Texte, sternförmig nach der Gruppierungshöhe",
                "Die Mitte ist die letzte UPGMA-Gruppe. Die Astlänge ist die Gruppierungshöhe. Zahlen ab 50.",
                ORDNER / "abb_stern_profile.svg",
            )
            abb.svg_stern(
                abb.baum_aus_kladen(
                    gewaehlt_p,
                    profil_namen,
                    abb.blattordnung(abb.upgma(abb.kosinus(wort_profil[150], wort_profil[150]))),
                ),
                profil_namen,
                None,
                "Sieben Texte, sternförmig",
                "Mehrheitskonsens. Gleiche Astlänge, keine Distanz. Nur Gruppen ab 50 Prozent.",
                ORDNER / "abb_stern_konsens_profile.svg",
                farbe_von=farbe_von_etikett,
                art="gleich",
            )

            merkmale_z = g.merkmal_ngramme(proben, p.ZEICHEN_N, p.ZEICHEN_HAEUFIGSTE)
            namen_z, zeichen = profile(
                proben,
                gruppen,
                merkmale_z,
                lambda stuecke, merkmale: g.matrix_ngramme(stuecke, merkmale, p.ZEICHEN_N),
            )
            baeume_z, gewaehlt_z = zeichne_konsens(
                zeichen,
                namen_z,
                {name: [i] for i, name in enumerate(namen_z)},
                rng,
                "Konsens nach Zeichen-4-Grammen",
                "Ein Blatt je Text. 500 häufigste 4-Gramme, Merkmal-Bootstrap.",
                ORDNER / "abb_konsens_zeichen.svg",
            )
            csv_zeilen.extend(kladen_zeilen("profile_zeichen", gewaehlt_z, namen_z))
            dendrogramm(
                abb.kosinus(zeichen, zeichen),
                namen_z,
                baeume_z,
                "Dendrogramm nach Zeichen-4-Grammen",
                "UPGMA, ein Blatt je Text. Die Zahl ist der Anteil der Bootstrap-Bäume in Prozent.\nWaagerecht die Gruppierungshöhe. Eine hellere Zahl liegt unter 50 Prozent.",
                ORDNER / "abb_dendrogramm_zeichen.svg",
            )
            stern(
                abb.kosinus(zeichen, zeichen),
                namen_z,
                baeume_z,
                "Zeichen-4-Gramme, sternförmig nach der Gruppierungshöhe",
                "Die Mitte ist die letzte UPGMA-Gruppe. Die Astlänge ist die Gruppierungshöhe. Zahlen ab 50.",
                ORDNER / "abb_stern_zeichen.svg",
            )
            abb.svg_stern(
                abb.baum_aus_kladen(
                    gewaehlt_z,
                    namen_z,
                    abb.blattordnung(abb.upgma(abb.kosinus(zeichen, zeichen))),
                ),
                namen_z,
                None,
                "Zeichen-4-Gramme, sternförmig",
                "Mehrheitskonsens. Gleiche Astlänge, keine Distanz. Nur Gruppen ab 50 Prozent.",
                ORDNER / "abb_stern_konsens_zeichen.svg",
                farbe_von=farbe_von_etikett,
                art="gleich",
            )

            leiter = []
            for anzahl in (100, 150, 300):
                leiter.append(abb.kladen(abb.upgma(abb.kosinus(wort_profil[anzahl], wort_profil[anzahl]))))
            gewaehlt_leiter, _ = abb.mehrheit(leiter, len(profil_namen))
            referenz = abb.blattordnung(abb.upgma(abb.kosinus(wort_profil[150], wort_profil[150])))
            svg_baum(
                abb.baum_aus_kladen(gewaehlt_leiter, profil_namen, referenz),
                "Konsens über die Merkmalleiter",
                "Drei Bäume, für 100, 150 und 300 häufigste Wörter. Eine Zahl 100 heißt: der Ast steht in allen drei.",
                ORDNER / "abb_konsens_mfw.svg",
            )
            csv_zeilen.extend(kladen_zeilen("profile_mfw", gewaehlt_leiter, profil_namen))
            dendrogramm(
                abb.kosinus(wort_profil[150], wort_profil[150]),
                profil_namen,
                leiter,
                "Dendrogramm der Merkmalleiter",
                "UPGMA der 150 Wörter. Die Zahl ist der Anteil der drei Merkmalzahlen in Prozent. 100 heißt: die Gruppe steht bei 100, 150 und 300.",
                ORDNER / "abb_dendrogramm_mfw.svg",
            )
            abb.svg_stern(
                abb.baum_aus_kladen(gewaehlt_leiter, profil_namen, referenz),
                profil_namen,
                None,
                "Merkmalleiter, sternförmig",
                "Mehrheitskonsens der drei Merkmalzahlen. Gleiche Astlänge, keine Distanz.",
                ORDNER / "abb_stern_konsens_mfw.svg",
                farbe_von=farbe_von_etikett,
                art="gleich",
            )
            stern(
                abb.kosinus(wort_profil[150], wort_profil[150]),
                profil_namen,
                leiter,
                "Merkmalleiter, sternförmig nach der Gruppierungshöhe",
                "UPGMA der 150 Wörter. Die Zahl ist der Anteil der drei Merkmalzahlen. 100 heißt: die Gruppe steht bei 100, 150 und 300.",
                ORDNER / "abb_stern_mfw.svg",
            )

    with (ORDNER / "konsens_kladen.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["abbildung", "klade", "anteil"])
        writer.writeheader()
        writer.writerows(csv_zeilen)

    html_uebersicht(
        [
            ("abb_stern_351.svg", "Sternförmiger UPGMA-Baum der Proben zu 351 Wörtern. Die Astlänge ist die Gruppierungshöhe."),
            ("abb_stern_548.svg", "Sternförmiger UPGMA-Baum der Proben zu 548 Wörtern."),
            ("abb_stern_profile.svg", "Sternförmiger Baum der sieben Texte."),
            ("abb_stern_zeichen.svg", "Sternförmiger Baum der Zeichen-4-Gramme."),
            ("abb_stern_mfw.svg", "Sternförmiger Baum der 150 häufigsten Wörter."),
            ("abb_stern_konsens_351.svg", "Dieselbe Mehrheit der kurzen Proben als Stern. Die Astlänge ist keine Distanz."),
            ("abb_stern_konsens_548.svg", "Mehrheitsstern der Proben zu 548 Wörtern."),
            ("abb_stern_konsens_profile.svg", "Mehrheitsstern der sieben Texte."),
            ("abb_stern_konsens_zeichen.svg", "Mehrheitsstern der Zeichen-4-Gramme."),
            ("abb_stern_konsens_mfw.svg", "Mehrheitsstern über 100, 150 und 300 häufigste Wörter."),
            ("abb_dendrogramm_351.svg", "Dendrogramm der Proben zu 351 Wörtern. Die waagerechte Achse ist die Gruppierungshöhe, die Zahl der Bootstrap-Anteil."),
            ("abb_dendrogramm_548.svg", "Dendrogramm der Proben zu 548 Wörtern. Biene, Kevlaar und Donna Clara fehlen, weil sie kürzer sind."),
            ("abb_dendrogramm_profile.svg", "Dendrogramm der sieben Texte, ein Blatt je Text, häufigste Wörter."),
            ("abb_dendrogramm_zeichen.svg", "Dasselbe Dendrogramm für die Zeichen-4-Gramme."),
            ("abb_dendrogramm_mfw.svg", "Dendrogramm der 150 häufigsten Wörter. Die Zahl sagt, in wie viel Prozent der drei Merkmalzahlen die Gruppe steht."),
            ("abb_konsens_351.svg", "Mehrheitskonsens der Proben zu 351 Wörtern. Gezeichnet sind nur Gruppen ab 50 Prozent."),
            ("abb_konsens_548.svg", "Mehrheitskonsens der Proben zu 548 Wörtern."),
            ("abb_konsens_profile.svg", "Mehrheitskonsens der sieben Texte."),
            ("abb_konsens_zeichen.svg", "Mehrheitskonsens der Zeichen-4-Gramme."),
            ("abb_konsens_mfw.svg", "Mehrheitskonsens über 100, 150 und 300 häufigste Wörter."),
            ("abb_abstaende.svg", "Einzelabstände innerhalb eines Textes und zwischen zwei Texten."),
            ("abb_waerme.svg", "Dieselben Probenabstände als Wärmebild."),
            ("351_woerter.svg", "Mittlerer Wortabstand der Texte bei 351 Wörtern."),
            ("548_woerter.svg", "Mittlerer Wortabstand der Texte bei 548 Wörtern."),
        ]
    )
    print("Abbildungen geschrieben nach", ORDNER)


if __name__ == "__main__":
    main()
