# -*- coding: utf-8 -*-
"""Vagabunden-Lieder von Enno Hektor, Der Vagabund 1848.

Die Seitenablesung steht in Hektor/Vagabund/lesen/vagabund_lieder.txt.
Vorlage ist der Druck Der Vagabund, Sommermond VI bis Windmond XI 1848,
die Hefte mit den Vagabunden-Liedern I bis XVIII, Scan
Hektor/Nachtraege/Vagabund_Hektor_Gedichte.pdf. Aufgenommen sind nur
diese Strophenlieder. Die Prosastücke desselben Drucks bleiben draußen:
Ein Sommernachtstraum, Der dumme Tobi, Biographie eines armen Teufels.
Zeitschriftkopf, Seitenzahl und die wiederholte Überschrift
Vagabunden-Lieder fehlen.

Langes s ist s. Der Apostroph ist gerade. Deutsche Anführungen bleiben.
Ein erneuter Lauf schreibt die beiden Textdateien neu und ändert die
Seitenablesung nicht. Die Datei steht nicht in den Dateilisten der
Studien 1 bis 4.
"""

import os
import re
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLE = os.path.join(BASE, "Hektor", "Vagabund", "lesen", "vagabund_lieder.txt")
NAME = "Hektor_Vagabund.txt"
ZIELE = (
    os.path.join(BASE, "corpus_diplomatisch", NAME),
    os.path.join(BASE, "Hektor", NAME),
)
APOSTROPH = {
    "\u2018": "'",
    "\u2019": "'",
    "\u02bc": "'",
    "\u2032": "'",
}
NUMMERN = [
    "I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.",
    "X.", "XI.", "XII.", "XIII.", "XIV.", "XV.", "XVI.", "XVII.", "XVIII.",
]
VERBOTEN = (
    "Sommernachtstraum",
    "dumme Tobi",
    "Biographie",
    "Vagabunden-Lieder",
    "UNSICHER",
)


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
    return "\n".join(zeilen) + "\n"


def pruefe(text):
    for wort in VERBOTEN:
        if wort in text:
            raise SystemExit("Beiwerk im Liedtext: " + wort)
    if "\u2019" in text or "\u2018" in text:
        raise SystemExit("Geschweifter Apostroph")
    bloecke = re.split(r"\n\s*\n", text.strip())
    gesehen = []
    for block in bloecke:
        zeilen = block.splitlines()
        if len(zeilen) == 1 and zeilen[0] in NUMMERN:
            gesehen.append(zeilen[0])
            continue
        if len(zeilen) != 4:
            raise SystemExit("Keine vierzeilige Strophe:\n" + block)
    if gesehen != NUMMERN:
        raise SystemExit("Nummern: " + ", ".join(gesehen))
    if not text.startswith("I.\n"):
        raise SystemExit("Anfang ist nicht I.")
    if "Ich fahre doch zur Hölle." not in text.splitlines()[-1]:
        raise SystemExit("Ende ist nicht die Hölle-Zeile")


def main():
    if not os.path.exists(QUELLE):
        raise SystemExit("Seitenablesung fehlt: " + QUELLE)
    text = normalisiere(open(QUELLE, encoding="utf-8").read())
    pruefe(text)
    for pfad in ZIELE:
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
