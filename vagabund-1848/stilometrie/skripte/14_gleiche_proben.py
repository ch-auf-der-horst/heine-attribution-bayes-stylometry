# -*- coding: utf-8 -*-
"""Prüfung, ob Verfasser sich trennen, wenn jeder Text gleich viele Proben gibt.

Die Bäume der Studien 4 bis 6 mitteln lange Texte und lassen kurze Texte
eine einzelne Probe sein. Hier zieht Prüfung A 500-mal genau eine Probe
je Text. Prüfung B setzt jede Probe als eigenes Blatt.

Die Leseregel steht in analyse/PROTOKOLL_GLEICHE_PROBEN.md. Sie wird hier
nicht verändert. Studie 1 bis 6 werden nicht angefasst.

Aufruf vom Projektordner aus:

    python3 analyse/14_gleiche_proben.py
"""

import importlib.util
import os
import sys
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

_fig = importlib.util.spec_from_file_location(
    "heine_abbildungen", Path(__file__).resolve().parent / "10_heine_abbildungen.py"
)
fig = importlib.util.module_from_spec(_fig)
_fig.loader.exec_module(fig)

ORDNER = p.PROJEKT / "ergebnisse" / "gleiche_proben"
LAENGE = 351
WIEDERHOLUNGEN = 500
SEED = [20261013, 7]
STOERER = ("Schilda", "Vagabund", "Müller", "Steinmann")
HEINE = (
    ("Heine_Aurora.txt", "Aurora", 1089),
    ("Heine_Biene.txt", "Biene", 351),
    ("Heine_Almanach.txt", "Almanach", 617),
    ("Heine_Agrippina.txt", "Agrippina", 830),
    ("Heine_Heimkehr.txt", "Heimkehr", 2467),
    ("Heine_Kevlaar.txt", "Kevlaar", 397),
    ("Heine_DonnaClara.txt", "Donna Clara", 413),
)
BEKANNT = HEINE + (
    ("Hektor_Schilda.txt", "Schilda", 7396),
    ("Hektor_Vagabund.txt", "Vagabund", 2143),
    ("Mueller_1.txt", "Müller", 11279),
    ("Wunderhorn_1806.txt", "Wunderhorn", 53339),
    ("Uhland_Lieder.txt", "Uhland", 5985),
    ("Geibel_Junius.txt", "Junius", 4534),
    ("Steinmann_Lieder.txt", "Steinmann", 492),
)
KANDIDAT = ("Kandidat_Vagabund.txt", "Kandidat", 548)
OHNE_BLATT = {"Wunderhorn"}

fig.FARBE.update(
    {
        "Schilda": "#9b3a4a",
        "Vagabund": "#b36b2a",
        "Müller": "#3d6b8a",
        "Wunderhorn": "#6e6256",
        "Uhland": "#2f6b4f",
        "Junius": "#6a4a78",
        "Steinmann": "#0b3a5b",
        "Kandidat": "#1c1915",
    }
)


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


def farbe(etikett):
    return fig.farbe_von_etikett(etikett.split(" ")[0] if etikett[-1].isdigit() else etikett)


def matrix_fuer(proben, merkmale, art, n=None):
    if art == "woerter":
        return g.matrix_woerter(proben, merkmale)
    return g.matrix_ngramme(proben, merkmale, n)


def merkmale_gleich(texte, art, n=None):
    """Rang der Merkmale. Jeder Text gibt den Mittelwert seiner Proben, einmal."""
    from collections import Counter

    summe = Counter()
    for text in texte:
        textmittel = Counter()
        teile = len(text["schnitte"])
        for probe in text["schnitte"]:
            if art == "woerter":
                einzel = Counter(g.buchstabenwoerter(probe))
            else:
                einzel = Counter(g.ngramme(probe, n))
            gesamt = sum(einzel.values())
            for merkmal, anzahl in einzel.items():
                textmittel[merkmal] += (anzahl / gesamt) / teile
        summe.update(textmittel)
    anzahl = 300 if art == "woerter" else p.ZEICHEN_HAEUFIGSTE
    return g.haeufigste(summe, anzahl)


def heine_ist_gruppe(baeume, heine):
    ziel = frozenset(heine)
    return sum(ziel in baum for baum in baeume) / len(baeume)


def kandidat_bei_heine(baeume, heine, kandidat):
    kern = frozenset(heine)
    treffer = 0
    for baum in baeume:
        huellen = [klade for klade in baum if kern <= klade]
        kleinste = min(huellen, key=len)
        treffer += kandidat in kleinste
    return treffer / len(baeume)


def groesste_reine_heinegruppe(kladen, heine):
    kern = set(heine)
    rein = [klade for klade in kladen if len(klade) > 1 and set(klade) <= kern]
    if not rein:
        return 0
    return max(len(klade) for klade in rein)


def fmt(wert):
    return f"{wert * 100:.1f} %".replace(".", ",")


def kleinste_huelle(kladen, kern):
    kern = frozenset(kern)
    return min((klade for klade in kladen if kern <= klade), key=len)


def huellenbild(baeume, kern, etiketten):
    """Größe der kleinsten Gruppe aller Heine-Blätter und wer außerdem darin liegt."""
    from collections import Counter

    groessen = []
    dabei = Counter()
    kernsatz = set(kern)
    for baum in baeume:
        huelle = kleinste_huelle(baum, kern)
        groessen.append(len(huelle))
        for blatt in huelle:
            if blatt not in kernsatz:
                dabei[etiketten[blatt]] += 1
    return np.array(groessen), dabei


def groesste_rein(baum, kern):
    kernsatz = set(kern)
    rein = [klade for klade in baum if len(klade) > 1 and set(klade) <= kernsatz]
    if not rein:
        return frozenset()
    return max(rein, key=len)


def main():
    if ORDNER.exists() and os.environ.get("AUTOR_NEUZEICHNEN") != "1":
        raise SystemExit("Der Ordner besteht schon und wird nicht überschrieben: " + str(ORDNER))
    ORDNER.mkdir(parents=True, exist_ok=True)
    for alt in ORDNER.glob("abb_*"):
        alt.unlink()

    bekannt = [laden(*eintrag) for eintrag in BEKANNT]
    kandidat = laden(*KANDIDAT)
    heine_namen = [name for _, name, _ in HEINE]
    etiketten = [text["name"] for text in bekannt] + [kandidat["name"]]
    heine_index = [etiketten.index(name) for name in heine_namen]
    kandidat_index = etiketten.index("Kandidat")
    if etiketten.index("Steinmann") != len(bekannt) - 1:
        raise SystemExit("Steinmann steht nicht am Ende der bekannten Texte")

    rng = np.random.default_rng(np.random.SeedSequence(SEED))
    baeume = {"Wörter 150": [], "Zeichen 4": []}
    for _ in range(WIEDERHOLUNGEN):
        gezogen = []
        for text in bekannt:
            nummer = int(rng.integers(0, len(text["schnitte"])))
            gezogen.append(text["schnitte"][nummer])
        kandidat_probe = kandidat["schnitte"][0]
        worte = g.merkmal_woerter(gezogen, 300)
        zeichen = g.merkmal_ngramme(gezogen, 4, p.ZEICHEN_HAEUFIGSTE)
        for art, merkmale, n, titel in (
            ("woerter", worte[:150], None, "Wörter 150"),
            ("zeichen", zeichen, 4, "Zeichen 4"),
        ):
            zeilen = matrix_fuer(gezogen + [kandidat_probe], merkmale, art, n)
            abstand = abb.kosinus(zeilen, zeilen[:-1])
            if abstand is None:
                raise SystemExit("Abstand in Prüfung A ist nicht bestimmt")
            baeume[titel].append(abb.kladen(abb.upgma(abstand)))

    anteile = {titel: heine_ist_gruppe(liste, heine_index) for titel, liste in baeume.items()}
    kandidat_anteile = {titel: kandidat_bei_heine(liste, heine_index, kandidat_index) for titel, liste in baeume.items()}
    huellen = {titel: huellenbild(liste, heine_index, etiketten) for titel, liste in baeume.items()}
    reine = {
        titel: np.array([len(groesste_rein(baum, heine_index)) for baum in liste])
        for titel, liste in baeume.items()
    }
    getrennt = anteile["Wörter 150"] >= 0.5 and anteile["Zeichen 4"] >= 0.5
    satz_a = (
        "Prüfung A trennt die Verfasser."
        if getrennt
        else "Prüfung A trennt die Verfasser nicht. Alle Heine-Blätter bilden nicht auf beiden Hauptmaßen in mindestens der Hälfte der Durchgänge eine eigene Gruppe."
    )

    def konsens_zeichnen(titel, datei, untertitel):
        liste = baeume[titel]
        gewaehlt, _ = abb.mehrheit(liste, len(etiketten))
        referenz = list(range(len(etiketten)))
        fig.svg_baum(
            abb.baum_aus_kladen(gewaehlt, etiketten, referenz),
            titel,
            untertitel,
            ORDNER / datei,
        )
        abb.svg_stern(
            abb.baum_aus_kladen(gewaehlt, etiketten, referenz),
            etiketten,
            None,
            titel,
            "Mehrheitskonsens der 500 Ziehungen. Gleiche Astlänge, keine Distanz. Nur Gruppen ab 50 Prozent.",
            ORDNER / datei.replace("abb_konsens", "abb_stern"),
            farbe,
            art="gleich",
        )
        return gewaehlt

    konsens_worte = konsens_zeichnen(
        "Wörter 150",
        "abb_konsens_worte.svg",
        "500-mal eine Probe je Text. 150 Wörter. Eine Zahl ist der Anteil der Ziehungen.",
    )
    konsens_zeichen = konsens_zeichnen(
        "Zeichen 4",
        "abb_konsens_zeichen.svg",
        "500-mal eine Probe je Text. 500 häufigste 4-Gramme.",
    )

    blaetter = [text for text in bekannt if text["name"] not in OHNE_BLATT] 
    # Der Kandidat kommt als Blatt dazu, wählt die Merkmale aber nicht.
    wort_liste = merkmale_gleich(blaetter, "woerter")[:150]
    zeichen_liste = merkmale_gleich(blaetter, "zeichen", 4)
    eich_worte = []
    eich_zeichen = []
    for text in blaetter:
        eich_worte.append(matrix_fuer(text["schnitte"], wort_liste, "woerter").mean(axis=0))
        eich_zeichen.append(matrix_fuer(text["schnitte"], zeichen_liste, "zeichen", 4).mean(axis=0))
    eich_worte = np.vstack(eich_worte)
    eich_zeichen = np.vstack(eich_zeichen)

    def blatt_matrix(merkmale, eichung, art, n=None):
        proben = []
        namen = []
        for text in blaetter:
            for nummer, probe in enumerate(text["schnitte"], start=1):
                proben.append(probe)
                namen.append(text["name"] if len(text["schnitte"]) == 1 else f"{text['name']} {nummer}")
        proben.append(kandidat["schnitte"][0])
        namen.append("Kandidat")
        zeilen = matrix_fuer(proben, merkmale, art, n)
        abstand = abb.kosinus(zeilen, eichung)
        if abstand is None:
            raise SystemExit("Abstand in Prüfung B ist nicht bestimmt")
        return namen, abstand

    namen_b, abstand_w = blatt_matrix(wort_liste, eich_worte, "woerter")
    namen_z, abstand_z = blatt_matrix(zeichen_liste, eich_zeichen, "zeichen", 4)
    if namen_b != namen_z:
        raise SystemExit("Die Blätter der beiden Maße stimmen nicht überein")
    heine_b = [
        i
        for i, name in enumerate(namen_b)
        if any(name == heine or name.startswith(heine + " ") for heine in heine_namen)
    ]
    kandidat_b = namen_b.index("Kandidat")
    kladen_w = abb.kladen(abb.upgma(abstand_w))
    kladen_z = abb.kladen(abb.upgma(abstand_z))
    voll_w = frozenset(heine_b) in kladen_w
    voll_z = frozenset(heine_b) in kladen_z
    satz_b = (
        "Prüfung B trennt die Verfasser."
        if voll_w and voll_z
        else "Prüfung B trennt die Verfasser nicht. Nicht alle Heine-Proben liegen auf beiden Maßen in einer Gruppe ohne Schilda, Vagabund, Müller und Steinmann."
    )
    def dendrogramm_b(abstand, titel, datei):
        abb.svg_dendrogramm(
            abb.upgma(abstand),
            namen_b,
            None,
            titel,
            "351 Wörter, Versatz 0. Jede Probe ein Blatt. Das Wunderhorn ist nicht dabei.\nDie Achse ist die Gruppierungshöhe. Keine Ziehung.",
            ORDNER / datei,
            farbe,
        )

    dendrogramm_b(abstand_w, "Jede Probe ein Blatt, 150 Wörter", "abb_dendrogramm_blaetter_worte.svg")
    dendrogramm_b(abstand_z, "Jede Probe ein Blatt, 4-Gramme", "abb_dendrogramm_blaetter_zeichen.svg")

    def zeile_anteil(titel):
        groesse = huellen[titel][0]
        return (
            f"| {titel} | {fmt(anteile[titel])} | {fmt(kandidat_anteile[titel])} "
            f"| {int(np.median(groesse))} | {int(groesse.min())}–{int(groesse.max())} "
            f"| {int(np.median(reine[titel]))} |"
        )

    def fremde(titel):
        _groesse, dabei = huellen[titel]
        teile = []
        for name in etiketten:
            if name in [eintrag[1] for eintrag in HEINE]:
                continue
            teile.append(f"{name} {fmt(dabei[name] / WIEDERHOLUNGEN)}")
        return ", ".join(teile)

    reine_worte = groesste_rein(kladen_w, heine_b)
    reine_zeichen = groesste_rein(kladen_z, heine_b)
    huelle_worte = kleinste_huelle(kladen_w, heine_b)
    huelle_zeichen = kleinste_huelle(kladen_z, heine_b)

    text = "\n".join(
        [
            "# Gleiche Proben",
            "",
            "Diese Prüfung ersetzt Studie 1 bis 6 nicht. Lange Texte sind hier nicht als Mittelwert neben einer einzelnen kurzen Probe gesetzt.",
            "",
            "## Prüfung A. Eine Probe je Text, 500-mal",
            "",
            satz_a,
            "",
            "Getrennt heißt: alle sieben Heine-Blätter bilden eine Gruppe. Schilda, Vagabund, Müller und Steinmann liegen dann draußen. Die Schwelle ist 50 Prozent, auf beiden Hauptmaßen.",
            "",
            "| Maß | Heine-Gruppe | Kandidat in der Hülle | Hülle, Median | Hülle, Spanne | größte reine Heine-Gruppe, Median |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
            zeile_anteil("Wörter 150"),
            zeile_anteil("Zeichen 4"),
            "",
            f"Gruppen im Mehrheitskonsens, ab 50 Prozent: auf den Wörtern {len(konsens_worte)}, auf den Vierergruppen {len(konsens_zeichen)}.",
            "",
            "Außer den sieben Heine-Blättern liegt in der Hülle, Wörter: " + fremde("Wörter 150") + ".",
            "",
            "Zeichen: " + fremde("Zeichen 4") + ".",
            "",
            "Die Hülle und ihr Median entscheiden nicht. Der Anteil des Kandidaten sagt nur, wie oft er in der kleinsten Gruppe steht, die alle Heine-Blätter enthält. Die Spalte Hülle zählt, wie viele der 15 Blätter diese Gruppe umfasst.",
            "",
            "Proben, aus denen gezogen wird:",
            "",
            "\n".join(
                f"- {text['name']}: {len(text['schnitte'])} {'Probe' if len(text['schnitte']) == 1 else 'Proben'}"
                for text in bekannt
            ),
            f"- Kandidat: 1 Probe, die ersten {LAENGE} von {len(kandidat['woerter'])} Wörtern",
            "",
            "## Prüfung B. Jede Probe ein Blatt",
            "",
            satz_b,
            "",
            f"Größte Gruppe, die nur Heine-Proben enthält: auf den Wörtern {len(reine_worte)} von {len(heine_b)} Blättern ({', '.join(namen_b[i] for i in sorted(reine_worte))}), auf den Vierergruppen {len(reine_zeichen)} von {len(heine_b)} ({', '.join(namen_b[i] for i in sorted(reine_zeichen))}).",
            "",
            f"Die kleinste Gruppe, die alle Heine-Proben enthält, umfasst auf den Wörtern {len(huelle_worte)} von {len(namen_b)} Blättern und auf den Vierergruppen {len(huelle_zeichen)} von {len(namen_b)}.",
            "",
            "Der Kandidat liegt in dieser Gruppe: "
            + ("ja" if kandidat_b in huelle_worte else "nein")
            + " auf den Wörtern, "
            + ("ja" if kandidat_b in huelle_zeichen else "nein")
            + " auf den Vierergruppen. Das entscheidet nicht.",
            "",
            f"Blätter: {len(namen_b)}. Das Wunderhorn fehlt in diesem Baum und bleibt in Prüfung A.",
            "",
        ]
    )
    (ORDNER / "BERICHT.md").write_text(text, encoding="utf-8")
    print(satz_a)
    print(zeile_anteil("Wörter 150"))
    print(zeile_anteil("Zeichen 4"))
    print(satz_b)
    print("Geschrieben nach", ORDNER)


if __name__ == "__main__":
    main()
