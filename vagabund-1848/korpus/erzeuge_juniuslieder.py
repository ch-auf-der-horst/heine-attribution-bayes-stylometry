# -*- coding: utf-8 -*-
"""Lieder aus Geibels Juniusliedern, Stuttgart und Tübingen: Cotta 1848.

Die Seitenablesung steht in Geibel/junius_lesen/. Jede Datei p00015.txt
bis p00069.txt ist eine Scanseite des Münchener Drucks bsb10108558.
Scanseite 15 ist die Druckseite 3. Aufgenommen ist der Abschnitt Lieder,
von „Sei getrost“ bis zum dritten Frühlingslied. Die Abschnittsüberschrift
„Vermischte Gedichte“ und die leeren Seiten danach bleiben draußen.

Langes s ist s. Der Apostroph ist gerade. Deutsche Anführungen bleiben.
Ein erneuter Lauf schreibt die Datei neu und ändert die Seitenablesung nicht.
"""

import os
import re
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEITEN = os.path.join(BASE, "Geibel", "junius_lesen")
NAME = "Geibel_Junius.txt"
ERSTE = 15
LETZTE = 69
APOSTROPH = {
    "\u2018": "'",
    "\u2019": "'",
    "\u02bc": "'",
    "\u2032": "'",
}


def normalisiere(text):
    text = unicodedata.normalize("NFC", text.replace("\u00a0", " ").replace("ſ", "s"))
    for src, dst in APOSTROPH.items():
        text = text.replace(src, dst)
    zeilen = []
    for roh in text.splitlines():
        zeile = re.sub(r"[ \t]+", " ", roh).strip()
        zeilen.append(zeile)
    while zeilen and zeilen[0] == "":
        zeilen.pop(0)
    while zeilen and zeilen[-1] == "":
        zeilen.pop()
    return zeilen


def ist_ueberschrift(zeile):
    woerter = zeile.split()
    if not zeile.endswith("."):
        return False
    if "," in zeile or ";" in zeile:
        return False
    return 1 <= len(woerter) <= 6


def zusammen():
    bloecke = []
    for nummer in range(ERSTE, LETZTE + 1):
        pfad = os.path.join(SEITEN, "p%05d.txt" % nummer)
        if not os.path.exists(pfad):
            raise SystemExit("Seite fehlt: " + pfad)
        zeilen = normalisiere(open(pfad, encoding="utf-8").read())
        if not zeilen:
            continue
        if "UNSICHER" in zeilen:
            raise SystemExit("Unsichere Lesung noch in " + pfad)
        if bloecke and ist_ueberschrift(zeilen[0]) and bloecke[-1] != "":
            bloecke.append("")
        bloecke.extend(zeilen)
    text = "\n".join(bloecke).strip() + "\n"
    if "Staatsbibliothek" in text or "Vermischte Gedichte" in text:
        raise SystemExit("Beiwerk im Liedtext")
    return text


def main():
    text = zusammen()
    for ordner in ("corpus_diplomatisch", "Geibel"):
        pfad = os.path.join(BASE, ordner, NAME)
        with open(pfad, "w", encoding="utf-8", newline="\n") as ziel:
            ziel.write(text)
    woerter = text.split()
    print(NAME)
    print("  Zeilen:", text.count("\n"))
    print("  Wörter:", len(woerter))
    print("  Apostrophe:", text.count("'"))
    print("  Kommata:", text.count(","))
    print("  Anfang:", " / ".join(text.splitlines()[:3]))
    print("  Ende:", " / ".join(text.splitlines()[-2:]))


if __name__ == "__main__":
    main()
