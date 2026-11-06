# -*- coding: utf-8 -*-
"""Lied- und Balladentext aus der DTA-TEI von Uhlands Gedichten, 1815.

Aufgenommen werden die Abschnitte „Lieder“ und „Balladen und Romanzen“,
jeder in eine eigene Datei. Nicht aufgenommen werden Vorwort,
Sinngedichte, Sonette, die dramatischen Dichtungen und das Inhaltsverzeichnis.
Langes s wird zu s, der geschwungene Apostroph zum geraden.
Drei im DTA als Druckfehler markierte Stellen (uoch, Znm, Wanch)
folgen der dortigen Korrektur. Fußnoten bleiben draußen.
"""

import os
import re
import unicodedata
import xml.etree.ElementTree as ET

NS = "http://www.tei-c.org/ns/1.0"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML = os.path.join(BASE, "Uhland", "uhland_gedichte_1815.TEI-P5.xml")

UMLAUT = {"a": "ä", "o": "ö", "u": "ü", "A": "Ä", "O": "Ö", "U": "Ü"}
SECTIONS = {
    "Lieder.": "Uhland_Lieder.txt",
    "Balladen und Romanzen.": "Uhland_Balladen.txt",
}


def local(el):
    return el.tag.split("}")[-1]


def normalize(text):
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "ſ":
            out.append("s")
            i += 1
            continue
        if ch in {"\u2019", "\u2018"}:
            out.append("'")
            i += 1
            continue
        if i + 1 < len(text) and text[i + 1] == "\u0364" and ch in UMLAUT:
            out.append(UMLAUT[ch])
            i += 2
            continue
        if ch in {"\u0364", "\u0307"}:
            i += 1
            continue
        out.append(ch)
        i += 1
    text = unicodedata.normalize("NFC", "".join(out))
    text = text.replace("\u00a0", " ")
    text = re.sub(r"-\n\s*", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def element_text(el):
    parts = []

    def walk(node):
        if local(node) in {"note", "fw", "pb", "milestone", "lb"}:
            if local(node) == "lb":
                parts.append("\n")
            if node.tail:
                parts.append(node.tail)
            return
        if local(node) == "choice":
            chosen = None
            for child in list(node):
                if local(child) == "corr":
                    chosen = child
                    break
            if chosen is None:
                for child in list(node):
                    if local(child) == "sic":
                        chosen = child
                        break
            if chosen is not None:
                walk(chosen)
            if node.tail:
                parts.append(node.tail)
            return
        if node.text:
            parts.append(node.text)
        for child in list(node):
            walk(child)
        if node.tail:
            parts.append(node.tail)

    walk(el)
    return normalize("".join(parts))


def stanza_lines(lg):
    lines = []
    for child in list(lg):
        if local(child) == "l":
            line = element_text(child)
            if line:
                lines.append(line)
        elif local(child) == "lg":
            if lines:
                lines.append("")
            lines.extend(stanza_lines(child))
    return lines


def poem_lines(lg):
    stanzas = [child for child in list(lg) if local(child) == "lg"]
    if not stanzas:
        return stanza_lines(lg)
    lines = []
    for stanza in stanzas:
        if lines and lines[-1] != "":
            lines.append("")
        lines.extend(stanza_lines(stanza))
    return lines


def song_lines(div):
    lines = []
    head = div.find(f"{{{NS}}}head")
    if head is not None:
        title = element_text(head)
        if title:
            lines.append(title)
            lines.append("")
    for child in list(div):
        if local(child) == "lg":
            lines.extend(poem_lines(child))
            if lines and lines[-1] != "":
                lines.append("")
        elif local(child) == "div":
            lines.extend(song_lines(child))
        elif local(child) == "p":
            speaker = element_text(child)
            if speaker:
                lines.append(speaker)
    return lines


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


def section_text(div):
    lines = []
    head = div.find(f"{{{NS}}}head")
    if head is not None:
        title = element_text(head)
        if title:
            lines.append(title)
            lines.append("")
    for child in list(div):
        if local(child) == "div":
            lines.extend(song_lines(child))
            if lines and lines[-1] != "":
                lines.append("")
    lines = collapse(lines)
    return "\n".join(lines) + "\n"


def main():
    root = ET.parse(XML).getroot()
    body = root.find(f".//{{{NS}}}body")
    found = {}
    for child in list(body):
        if local(child) != "div":
            continue
        head = child.find(f"{{{NS}}}head")
        if head is None:
            continue
        title = element_text(head)
        if title in SECTIONS:
            found[title] = section_text(child)
    missing = [title for title in SECTIONS if title not in found]
    if missing:
        raise SystemExit("Abschnitt fehlt: " + ", ".join(missing))
    for title, blob in found.items():
        if "ſ" in blob or "\u2019" in blob or "\u0364" in blob:
            raise SystemExit("langes s oder Apostroph übrig in " + title)
        if "Vorwort" in blob or "Sinngedichte" in blob or "Cervantes" in blob:
            raise SystemExit("Beiwerk geraten in " + title)
        name = SECTIONS[title]
        for folder in ("corpus_diplomatisch", "Uhland"):
            path = os.path.join(BASE, folder, name)
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(blob)
        words = blob.split()
        print(title)
        print(f"  Zeilen: {blob.count(chr(10))}")
        print(f"  Wörter: {len(words)}")
        print(f"  Apostrophe: {blob.count(chr(39))}")
        print(f"  Kommata: {blob.count(',')}")
        print("  Anfang:", " / ".join(blob.splitlines()[:4]))


if __name__ == "__main__":
    main()
