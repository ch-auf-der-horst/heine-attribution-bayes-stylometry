# -*- coding: utf-8 -*-
"""Liedtext aus der DTA-TEI von Des Knaben Wunderhorn, Band 1, 1806.

Aufgenommen werden die Lieder im Buchkörper. Nicht aufgenommen werden
die Widmung, der Aufsatz „Von Volksliedern“, die Nachschrift, die
Quellenvermerke unter den Liedern und das Register.
Langes s wird zu s, der Fraktur-Umlaut (Vokal plus übergesetztes e)
wird zum Umlaut. Vier im DTA als Druckfehler markierte Stellen
(kommeu, iu, Duſle, nnd) folgen der dortigen Korrektur.
"""

import os
import re
import unicodedata
import xml.etree.ElementTree as ET

NS = "http://www.tei-c.org/ns/1.0"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML = os.path.join(BASE, "Arnim", "arnim_wunderhorn01_1806.TEI-P5.xml")

UMLAUT = {"a": "ä", "o": "ö", "u": "ü", "A": "Ä", "O": "Ö", "U": "Ü"}


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
        if i + 1 < len(text) and text[i + 1] == "\u0364" and ch in UMLAUT:
            out.append(UMLAUT[ch])
            i += 2
            continue
        if ch == "\u0364":
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
    """Ein lg type=poem besteht aus Strophen-lg, sonst aus Versen."""
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


def main():
    root = ET.parse(XML).getroot()
    body = root.find(f".//{{{NS}}}body")
    songs = None
    for child in list(body):
        if local(child) == "div":
            songs = child
            break
    if songs is None:
        raise SystemExit("Kein Liedteil gefunden")
    lines = []
    for child in list(songs):
        if local(child) == "div":
            lines.extend(song_lines(child))
            if lines and lines[-1] != "":
                lines.append("")
    lines = collapse(lines)
    blob = "\n".join(lines) + "\n"
    if "ſ" in blob or "\u0364" in blob:
        raise SystemExit("langes s oder Fraktur-Umlaut übrig")
    if "Von Volksliedern" in blob or "Nachschrift an den Leser" in blob:
        raise SystemExit("Prosateil geraten in den Liedtext")
    out_names = [
        os.path.join(BASE, "corpus_diplomatisch", "Wunderhorn_1806.txt"),
        os.path.join(BASE, "Arnim", "Wunderhorn_1806.txt"),
    ]
    for path in out_names:
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(blob)
    words = blob.split()
    print(f"Liederzeilen und Überschriften: {len(lines)}")
    print(f"Wörter: {len(words)}")
    print(f"Apostrophe: {blob.count(chr(39))}")
    print(f"Kommata: {blob.count(',')}")
    print("Anfang:")
    print("\n".join(lines[:16]))


if __name__ == "__main__":
    main()
