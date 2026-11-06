# -*- coding: utf-8 -*-
"""Liedtext aus den manuellen Schilda-Abschriften.

Quellen im Ordner Hektor:
- Hektor_Schilda_Transkriptionsprobe.docx (PDF-Seiten 1–2, Introduktion)
- Hektor_Schilda_Manuell_PDF003-006.docx bis PDF129-131.docx

Nicht verwendet werden die Arbeitsfassung, die Seiten 1–2 und 7–9
gröber wiederholt, und die PDF-Seiten ab 132, eine Verlagsanzeige
mit Gedichten von Hafis in der Übertragung Daumers.
Die Abschriften sind gegen den Druck kollationiert. Getrennte Verszeilen,
die in der Abschrift durch zwei Leerzeichen verbunden waren, stehen wieder
einzeln. Einzelne Lesarten folgen dem Druck, wo die Fraktur-Erkennung
und das Seitenbild übereinstimmen.
"""

import os
import re
import unicodedata
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEKTOR = os.path.join(BASE, "Hektor")

DROP_PARTS = (
    "Manuelle",
    "Transkription",
    "Arbeitsfassung",
    "Arbeitsübertragung",
    "Zweitkollation",
    "Editorisch",
    "Editionshinweis",
    "Historische Orthographie",
    "Historische Schreibung",
    "Historische Schreib",
    "Sichtprüfung",
    "Seitenbild",
    "Digitalisat",
    "Fraktur",
    "Verlagsanhang",
    "Verlagsanzeige",
    "In unserm Verlage",
    "Hafis. Eine Sammlung",
    "Fortsetzung der Gedichtauszüge",
    "Fortsetzung des Verlagsanhangs",
    "handschriftlich",
    "unsichere Lesung",
    "kollationieren",
    "Bogentitel",
    "Gedichttextes",
)
PAGE = re.compile(
    r"^(?:\[)?(?:PDF[-\s]|Druckseite|PDF-Seite|PDF-Seiten)\b",
    re.IGNORECASE,
)


def paras(path):
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    return [
        "".join(node.text or "" for node in paragraph.iter(f"{W}t"))
        for paragraph in root.iter(f"{W}p")
    ]


def normalize(line):
    line = unicodedata.normalize("NFC", line.replace("\u00a0", " "))
    line = line.replace("\u2018", "'").replace("\u2019", "'")
    line = re.sub(r"\s*\[Lesart unsicher\]", "", line)
    line = re.sub(r"\[([A-Za-zäöüÄÖÜß])\]", r"\1", line)
    # Fehlendes Leerzeichen innerhalb eines Verses, nicht ein neuer Vers.
    line = line.replace("scharfemMesser", "scharfem Messer")
    line = line.replace("fauleFleisch", "faule Fleisch")
    line = re.sub(r"([a-zäöüß])\(", r"\1 (", line)
    line = re.sub(r"\s*\([^)]*(?:PDF[-\s]Seite|Druckseite)[^)]*\)", "", line)
    line = re.sub(r"(?:PDF[-\s]Seiten?|Druckseiten?)\s+\d+(?:\s*[–—/-]\s*\d+)?", "", line)
    line = re.sub(r"^[·|\s]+|[·|\s]+$", "", line)
    return line.strip()


def editorial(line):
    if not re.search(r"[A-Za-zÄÖÜäöüß0-9]", line):
        return True
    if line in {"Lieder aus Schilda", "Enno Hektor: Lieder aus Schilda"}:
        return True
    if line.startswith("Enno ") and "Hektor" in line:
        return True
    if line.startswith("Lieder aus Schilda"):
        return True
    if line.startswith("[") and (
        "Fortsetzung" in line or line.startswith("[PDF") or line.startswith("[Druck")
    ):
        return True
    if PAGE.match(line):
        return True
    return any(part in line for part in DROP_PARTS)


# Lesarten, an denen der Druck von der ersten Abschrift abweicht.
REPLACEMENTS = (
    ("Introduktion.", "Introduktion:"),
    ("„Mein Herr!“", "„Wein her!“"),
    ("Geisterfluthen", "Geistesfluthen"),
    ("Lüste über Lüsten", "Witze über Witze"),
    ("Wo's girt,", "Wo's gilt,"),
    ("nicht im Stehn,", "nicht versteht,"),
    ("Judelschaar", "Pudelschaar"),
    ("Saturnaner", "Sekundaner"),
    ("Fratzengesichtern", "Fragengesichtern"),
    ("Entfindet der Muth", "Entsinket der Muth"),
    ("weiß' ich der Schildanerin", "weih' ich der Schildanerinn"),
    ("Ich weiß' dies Lied", "Ich weih' dies Lied"),
    ("bei Erpressen", "bei Expensen"),
    ("Lutti.", "Tutti."),
    ("zum Erektor", "zum Exekutor"),
    ("Erstlegt mir", "Ersiegt mir"),
    ("Verzeih' er doch einen Rath", "Verleih' er doch einen Rath"),
    ("seinen Poeten", "keinen Poeten"),
    ("grausiger Leere", "grauser Leere"),
    ("wir fallen wohl unter den Tisch", "wir sinken wol unter den Tisch"),
    ("Wohl auf dem Bette der Ehre", "Wol auf dem Bette der Ehre"),
    ("fett und prall", "fett und drall"),
    ("öffentlichen Festen", "öffentlichen Feten"),
    ("Lämmerwollenheerde", "Lämmerwolkenheerde"),
    ("lustigen Ritt", "luftigen Ritt"),
    ("unsre Sabel", "unser Sabel"),
    ("gleichwohl", "gleichwol"),
    ("widernwärtig", "widerwärtig"),
    ("Eselstreiber", "Eseltreiber"),
    ("Sturmeschwingen", "Sturmesschwingen"),
    ("fetteste", "fettste"),
    ("Zittr' ich den Beamtenstolz", "Zitir' ich den Beamtenstolz"),
    ("O laßt, das Reich", "O Lust, das Reich"),
    ("Zersplatze", "Zerplatze"),
)


def collate(line):
    for old, new in REPLACEMENTS:
        line = line.replace(old, new)
    return line


def split_glued(line):
    """Verse trennen, die ohne Leerzeichen aneinanderkleben."""
    parts = re.split(
        r"(?<=[,;:.!?—–])(?=[A-ZÄÖÜ„\"])|(?<=[,;:.!?—–][“\"])(?=[A-ZÄÖÜ])|(?<=')(?=[A-ZÄÖÜ])|(?<=[a-zäöüß])(?=[A-ZÄÖÜ])",
        line,
    )
    return [part.strip() for part in parts if part.strip()]


def verse_pieces(line):
    """Zwei Leerzeichen in der Abschrift sind der Zeilenbruch des Drucks."""
    pieces = []
    for part in re.split(r" {2,}", line):
        part = collate(part.strip())
        if not part:
            continue
        if part.startswith("Fortsetzung") or "Fortsetzung" in part and part.startswith("("):
            continue
        part = re.sub(r"\s*\((?:Anfang|Fortsetzung)\)", "", part)
        part = re.sub(r"\s*\[\]", "", part).strip()
        if part:
            pieces.extend(split_glued(part))
    return pieces


def poem_lines(path):
    lines = []
    for raw in paras(path):
        line = normalize(raw)
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if line.startswith("In unserm Verlage") or line.startswith("Hafis."):
            break
        if editorial(line):
            continue
        lines.extend(verse_pieces(line))
    return lines


def collapse(lines):
    result = []
    for line in lines:
        if line == "" and (not result or result[-1] == ""):
            continue
        result.append(line)
    while result and result[0] == "":
        result.pop(0)
    while result and result[-1] == "":
        result.pop()
    return result


def classify_parts(lines):
    """Lied, Knittel, Introduktion, Ballade, XXXV und LXX ohne Überschneidung."""
    start = lines.index("I.")
    intro = lines[:start]
    number = re.compile(r"^[IVXLC]+\.$")
    poems = []
    current = None
    body = []
    for line in lines[start:]:
        if number.match(line):
            if current is not None:
                poems.append((current, body))
            current = line
            body = [line]
        else:
            body.append(line)
    poems.append((current, body))
    knittel = {"XVIII.", "LIIII.", "LIV.", "LXI.", "LXII.", "LXXXII.", "C."}
    lxx = {"LXX.", "LXXI.", "LXXII.", "LXXIII.", "LXXIV.", "LXXV.", "LXXVI.", "LXXVII."}
    seen = {}
    parts = {
        "intro": intro,
        "lied": [],
        "knittel": [],
        "ballade": [],
        "xxxv": [],
        "lxx": [],
    }
    assigned = []
    for name, body in poems:
        seen[name] = seen.get(name, 0) + 1
        if name == "XXI.":
            kind = "ballade"
        elif name == "XXXV." or (name == "XXXVI." and seen[name] == 1) or (
            name == "XXXVII." and seen[name] == 1
        ):
            kind = "xxxv"
        elif name in lxx:
            kind = "lxx"
        elif name in knittel:
            kind = "knittel"
        else:
            kind = "lied"
        if body and body[-1] == "ENDE.":
            body = body[:-1]
        while body and body[-1] == "":
            body.pop()
        parts[kind].extend(body)
        parts[kind].append("")
        assigned.append((name, seen[name], kind, len([x for x in body if x])))
    return parts, assigned


def write_text(folder, name, lines):
    while lines and lines[-1] == "":
        lines.pop()
    blob = "\n".join(lines).rstrip() + "\n"
    path = os.path.join(BASE, folder, name)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(blob)
    return blob


def main():
    names = []
    probe = os.path.join(HEKTOR, "Hektor_Schilda_Transkriptionsprobe.docx")
    if not os.path.isfile(probe):
        raise SystemExit("Transkriptionsprobe fehlt")
    names.append(probe)
    pages = []
    for name in os.listdir(HEKTOR):
        match = re.fullmatch(r"Hektor_Schilda_Manuell_PDF(\d+)-(\d+)\.docx", name)
        if match and int(match.group(1)) < 132:
            pages.append((int(match.group(1)), name))
    for _, name in sorted(pages):
        names.append(os.path.join(HEKTOR, name))
    lines = []
    for path in names:
        lines.extend(poem_lines(path))
        if lines and lines[-1] != "":
            lines.append("")
    lines = collapse(lines)
    blob = "\n".join(lines) + "\n"
    for forbidden in ("Editorisch", "Zweitkollation", "PDF-Seite", "Hafis", "Manuelle Transkription"):
        if forbidden in blob:
            raise SystemExit("Beiwerk übrig: " + forbidden)
    if "Introduktion:" not in blob or "\nI.\n" not in blob or "\nENDE." not in blob:
        raise SystemExit("Anfang oder Schluss des Bandes fehlt")
    if "„Wein her!“" not in blob or "Wo's gilt," not in blob or "nicht versteht," not in blob:
        raise SystemExit("Kollationierte Lesart fehlt")
    if "girt" in blob or "im Stehn" in blob or "Erstlegt" in blob or "Judelschaar" in blob:
        raise SystemExit("Alte Lesart übrig")
    if "Die Karten her!" not in blob or "scharfem Messer" not in blob:
        raise SystemExit("Seiten 3–6 oder die Verszeile mit scharfem Messer fehlen")
    if "scharfem\nMesser" in blob or "faule\nFleisch" in blob:
        raise SystemExit("Vers intern auseinandergerissen")
    out_name = "Hektor_Schilda_1847.txt"
    write_text("Hektor", out_name, list(lines))
    mixed = os.path.join(BASE, "corpus_diplomatisch", out_name)
    if os.path.isfile(mixed):
        os.remove(mixed)
    part_names = {
        "intro": "Hektor_Intro.txt",
        "lied": "Hektor_Schilda.txt",
        "knittel": "Hektor_Knittel.txt",
        "ballade": "Hektor_Ballade.txt",
        "xxxv": "Hektor_XXXV.txt",
        "lxx": "Hektor_LXX.txt",
    }
    parts, assigned = classify_parts(lines)
    print(f"Dateien: {len(names)}")
    print(f"Ganztext Zeilen: {len(lines)} Wörter: {len(blob.split())}")
    for key, filename in part_names.items():
        text = None
        for folder in ("corpus_diplomatisch", "Hektor"):
            text = write_text(folder, filename, list(parts[key]))
        print(f"{filename}: {len(text.split())} Wörter")
    for name, nth, kind, count in assigned:
        print(f"  {name} #{nth} -> {kind} ({count} Zeilen)")


if __name__ == "__main__":
    main()
