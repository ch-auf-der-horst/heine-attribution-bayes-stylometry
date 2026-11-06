# -*- coding: utf-8 -*-
"""Gedichttext aus Geibels Gedichten, Berlin: Duncker, 14. Auflage 1849.

Die Abschrift behält Verszeile, historische Schreibung, Kommata und
Apostrophe. Titelblatt, Inhaltsverzeichnis, Seitenzahlen und
Zierlinien fallen weg. Drei Dateien: die Lieder als Intermezzo,
die vier Bücher samt der Widmung, und Sonette samt Distichen.
"""

import os
import re
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "Geibel", "Geibel_Gedichte_1849_Antiqua_1.txt")

PAGE = re.compile(r"^\[(?:o\. S\.|S\. [IVXLC0-9]+)\]$")
RULE = re.compile(r"^[—–\-]+$")
STARS = re.compile(r"^[\*\s]+$")
DATE_LINE = re.compile(r"^Marienbad, im Julius 1846\.$")

BUCKETS = {
    "lieder": "Geibel_Lieder.txt",
    "buecher": "Geibel_Buecher.txt",
    "sonette": "Geibel_Sonette.txt",
}


def clean(line):
    line = unicodedata.normalize("NFC", line.replace("\u00a0", " "))
    line = line.replace("\u2018", "'").replace("\u2019", "'")
    return re.sub(r" {2,}", " ", line.strip())


def keep(line):
    if not line:
        return False
    if PAGE.match(line) or RULE.match(line) or DATE_LINE.match(line):
        return False
    if "*" in line and STARS.match(line):
        return False
    return True


def collapse(lines):
    result = []
    for line in lines:
        if line == "" and (not result or result[-1] == ""):
            continue
        result.append(line)
    while result and result[-1] == "":
        result.pop()
    while result and result[0] == "":
        result.pop(0)
    return result


def bucket_for(line, current):
    if line == "Lieder als Intermezzo.":
        return "lieder"
    if line in {"Erstes Buch.", "Zweites Buch.", "Drittes Buch.", "Viertes Buch."}:
        return "buecher"
    if line in {"Sonette und Distichen", "Neue Sonette"}:
        return "sonette"
    return current


def main():
    raw = open(SRC, encoding="utf-8").read().splitlines()
    inhalt = raw.index("Inhalt.")
    books = [i for i, line in enumerate(raw) if line.strip() == "Erstes Buch."]
    if len(books) < 2:
        raise SystemExit("Beginn der Gedichte nicht gefunden")
    dedication = [clean(line) for line in raw[:inhalt]]
    dedication = [line for line in dedication if keep(line)]
    # Titelblatt vor der Widmung
    if "An Clara Kugler." in dedication:
        dedication = dedication[dedication.index("An Clara Kugler.") :]
    else:
        dedication = []
    body = [clean(line) for line in raw[books[1] :]]

    parts = {"lieder": [], "buecher": list(dedication), "sonette": []}
    current = "buecher"
    for line in body:
        if keep(line):
            current = bucket_for(line, current)
            parts[current].append(line)
        elif parts[current] and parts[current][-1] != "":
            parts[current].append("")

    for key, name in BUCKETS.items():
        lines = collapse(parts[key])
        blob = "\n".join(lines) + "\n"
        if "[S." in blob or "Inhalt." in blob or "Hofbuchhändler" in blob:
            raise SystemExit("Beiwerk geraten in " + name)
        if "…" in blob and re.search(r"…\s+\d+", blob):
            raise SystemExit("Inhaltszeile geraten in " + name)
        for folder in ("corpus_diplomatisch", "Geibel"):
            path = os.path.join(BASE, folder, name)
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(blob)
        words = blob.split()
        print(name)
        print(f"  Zeilen: {len(lines)}")
        print(f"  Wörter: {len(words)}")
        print(f"  Apostrophe: {blob.count(chr(39))}")
        print(f"  Kommata: {blob.count(',')}")
        print("  Anfang:", " / ".join(lines[:3]))


if __name__ == "__main__":
    main()
