# -*- coding: utf-8 -*-
"""Heine zugeschriebene Gedichte aus Steinmanns Denkwürdigkeiten, 1857.

Die Seitenablesung steht in Steinmann/lesen/lieder.txt und
Steinmann/lesen/sonette.txt. Vorlage ist Friedrich Arnold Steinmann,
H. Heine. Denkwürdigkeiten und Erlebnisse, 1857, Scan
A_Administration/Steinmann_Heine Denkwürdigkeiten(1857).pdf.
Die Lieder stehen auf den Druckseiten 164–168 und 193–194
(PDF-Seiten 185–189 und 214–215). Die beiden Sonette stehen auf den
Druckseiten 163–164 und 168–169 (PDF-Seiten 184–185 und 189–190).
Die Nachlese steht auf den Druckseiten 13–22, 56–57, 236–238 und 271
(PDF-Seiten 34–43, 77–78, 257–259 und 292).

Steinmann schreibt die Gedichte Heine zu. Sie bleiben eine eigene
Probe und werden keinem Heine-Text zugeschlagen. Die Sonette liegen
getrennt von den Strophenliedern, weil die Liedprobe keine Sonette
misst. Prosarahmen, Fußnote, Seitenzahl und das Schiller-Zitat in der
Rezensionserzählung fehlen.

Langes s ist s. Der Apostroph ist gerade. Deutsche Anführungen bleiben.
Ein erneuter Lauf schreibt die Textdateien neu und ändert die
Seitenablesung nicht. Die Dateien stehen nicht in den Dateilisten der
Studien 1 bis 5. Die Nachlese ist nicht die Probe von Studie 6.
"""

import os
import re
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESEN = os.path.join(BASE, "Steinmann", "lesen")
APOSTROPH = {
    "\u2018": "'",
    "\u2019": "'",
    "\u02bc": "'",
    "\u2032": "'",
}
VERBOTEN = (
    "Musenalmanach",
    "Raßmann",
    "Harzreise",
    "Heimkehr",
    "Schiller",
    "Prolog",
    "UNSICHER",
    "wiedervorführen",
)
TITEL_LIEDER = (
    "Zuckerpastillen für die Geliebte.",
    "Parodie.",
    "Lieder.",
    "Wandelnde Blumen in Berlin.",
)
TITEL_SONETTE = (
    "Burleskes Sonett.",
    "Dresdener Poesie.",
)
NUMMERN = ("I.", "II.", "III.", "IV.", "V.")


def normalisiere(text):
    text = unicodedata.normalize("NFC", text.replace("\u00a0", " ").replace("ſ", "s"))
    for src, dst in APOSTROPH.items():
        text = text.replace(src, dst)
    zeilen = [re.sub(r"[ \t]+", " ", roh).strip() for roh in text.splitlines()]
    while zeilen and zeilen[0] == "":
        zeilen.pop(0)
    while zeilen and zeilen[-1] == "":
        zeilen.pop()
    return "\n".join(zeilen) + "\n"


def bloecke(text):
    return re.split(r"\n\s*\n", text.strip())


def pruefe_gemeinsam(text):
    for wort in VERBOTEN:
        if wort in text:
            raise SystemExit("Beiwerk im Gedichttext: " + wort)
    if "\u2019" in text or "\u2018" in text:
        raise SystemExit("Geschweifter Apostroph")
    if "Schätze" in text:
        raise SystemExit("Schätze wäre eine Glättung; der Druck hat Schäße")


def pruefe_lieder(text):
    pruefe_gemeinsam(text)
    if not text.startswith("Zuckerpastillen für die Geliebte.\n"):
        raise SystemExit("Anfang ist nicht die Zuckerpastille")
    if "Die er üben muß und lieben." not in text.splitlines()[-1]:
        raise SystemExit("Ende ist nicht die Reise-Strophe")
    for notwendig in ("Schäße", "ennüjiret", "ennuyirte", "Türkenshawls", "sein's"):
        if notwendig not in text:
            raise SystemExit("Lesung fehlt: " + notwendig)
    if "Zuleht" in text or "hündisch" in text:
        raise SystemExit("Sonettzeile im Liedtext")
    titel = []
    nummern = []
    for block in bloecke(text):
        zeilen = block.splitlines()
        if len(zeilen) == 1 and zeilen[0] in TITEL_LIEDER:
            titel.append(zeilen[0])
            continue
        if len(zeilen) == 1 and zeilen[0] in NUMMERN:
            nummern.append(zeilen[0])
            continue
        if len(zeilen) not in (4, 6):
            raise SystemExit("Keine Strophe aus vier oder sechs Zeilen:\n" + block)
    if titel != list(TITEL_LIEDER):
        raise SystemExit("Titel: " + ", ".join(titel))
    if nummern != ["I.", "II.", "III.", "IV.", "V.", "I.", "II."]:
        raise SystemExit("Nummern: " + ", ".join(nummern))


def pruefe_sonette(text):
    pruefe_gemeinsam(text)
    if not text.startswith("Burleskes Sonett.\n"):
        raise SystemExit("Anfang ist nicht das burleske Sonett")
    if "Die Abendzeitung sei das Weltorakel." not in text.splitlines()[-1]:
        raise SystemExit("Ende ist nicht das Weltorakel")
    for notwendig in ("Zuleht", "hündisch", "Nostitz", "schwademt", "musiziren"):
        if notwendig not in text:
            raise SystemExit("Lesung fehlt: " + notwendig)
    if "Schäße" in text or "ennüjiret" in text:
        raise SystemExit("Liedzeile im Sonett")
    titel = []
    verse = 0
    for block in bloecke(text):
        zeilen = block.splitlines()
        if len(zeilen) == 1 and zeilen[0] in TITEL_SONETTE:
            titel.append(zeilen[0])
            continue
        if len(zeilen) not in (3, 4):
            raise SystemExit("Kein Sonettabschnitt:\n" + block)
        verse += len(zeilen)
    if titel != list(TITEL_SONETTE):
        raise SystemExit("Titel: " + ", ".join(titel))
    if verse != 28:
        raise SystemExit("Sonettzeilen: %s, erwartet 28" % verse)


def schreibe(name, text, pruefe):
    text = normalisiere(text)
    pruefe(text)
    ziele = (
        os.path.join(BASE, "corpus_diplomatisch", name),
        os.path.join(BASE, "Steinmann", name),
    )
    for pfad in ziele:
        with open(pfad, "w", encoding="utf-8", newline="\n") as ziel:
            ziel.write(text)
    print(name)
    print("  Zeilen:", text.count("\n"))
    print("  Wörter:", len(text.split()))
    print("  Apostrophe:", text.count("'"))
    print("  Kommata:", text.count(","))
    print("  Anfang:", " / ".join(text.splitlines()[:2]))
    print("  Ende:", text.splitlines()[-1])


TITEL_NACHLESE = (
    "Im Hofgarten zu Düsseldorf",
    "Deutschland.",
    "1815.",
    "Traum.",
    "1816.",
    "Seufzer.",
    "Meine Lieder.",
    "Der deutsche Rhein.",
    "Die deutsche Flotte.",
)


def pruefe_nachlese(text):
    pruefe_gemeinsam(text)
    if not text.startswith("Im Hofgarten zu Düsseldorf\n"):
        raise SystemExit("Anfang ist nicht der Hofgarten")
    if "Die Festungsstrafe wird abgeschafft." not in text.splitlines()[-1]:
        raise SystemExit("Ende ist nicht die Flotte")
    for notwendig in ("lezten", "zulezt", "jeßt", "thät", "Schatz", "Lanzen", "schickt'", "Schand'"):
        if notwendig not in text:
            raise SystemExit("Lesung fehlt: " + notwendig)
    for geglaettet in ("Schay", "zuletzt", "eben jetzt", "that man", "Tanzen"):
        if geglaettet in text:
            raise SystemExit("Glättung im Text: " + geglaettet)
    titel = []
    for block in bloecke(text):
        zeilen = block.splitlines()
        if len(zeilen) == 1 and zeilen[0] in TITEL_NACHLESE:
            titel.append(zeilen[0])
            continue
        if len(zeilen) not in (3, 4):
            raise SystemExit("Keine Strophe aus drei oder vier Zeilen:\n" + block)
    if titel != list(TITEL_NACHLESE):
        raise SystemExit("Titel: " + ", ".join(titel))
    if text.count("\nDer Kaiser ritt") != 1:
        raise SystemExit("Der Hofgarten ist nicht genau einmal da")


def main():
    lieder = os.path.join(LESEN, "lieder.txt")
    sonette = os.path.join(LESEN, "sonette.txt")
    nachlese = os.path.join(LESEN, "nachlese.txt")
    for pfad in (lieder, sonette, nachlese):
        if not os.path.exists(pfad):
            raise SystemExit("Seitenablesung fehlt: " + pfad)
    schreibe("Steinmann_Lieder.txt", open(lieder, encoding="utf-8").read(), pruefe_lieder)
    schreibe("Steinmann_Sonette.txt", open(sonette, encoding="utf-8").read(), pruefe_sonette)
    schreibe("Steinmann_Nachlese.txt", open(nachlese, encoding="utf-8").read(), pruefe_nachlese)


if __name__ == "__main__":
    main()
