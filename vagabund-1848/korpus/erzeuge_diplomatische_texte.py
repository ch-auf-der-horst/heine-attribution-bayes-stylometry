# -*- coding: utf-8 -*-
"""Diplomatische Textschicht aus den Vorlagen mit Interpunktion und Apostrophen.

Quellen:
- Heine/Heine_Aurora(1823).docx
- Heine/Heine_Die Biene_(1823:1826, anonym).docx
- Müller/Wilhelm Müller_1.docx
- Müller/Müller_Waldhornist_2.docx
- Kandidat/Text_Kandidat.pdf (Gedichte I–X; Rahmentext und Gottschall-Notiz bleiben draußen)

Die _ber-Dateien werden nicht verändert.
"""

import os
import re
import unicodedata
import zipfile
from xml.etree import ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def nfc(text):
    return unicodedata.normalize("NFC", text)


def paras(path):
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    out = []
    for paragraph in root.iter(f"{W}p"):
        parts = [node.text or "" for node in paragraph.iter(f"{W}t")]
        out.append("".join(parts))
    return out


def collapse_blanks(lines):
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


def write_text(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def find_dir(prefix):
    for name in os.listdir(BASE):
        if name.startswith(prefix):
            path = os.path.join(BASE, name)
            if os.path.isdir(path):
                return path
    raise FileNotFoundError(prefix)


def find_file(directory, suffix):
    for name in os.listdir(directory):
        if name.endswith(suffix) and not name.startswith("~$"):
            return os.path.join(directory, name)
    raise FileNotFoundError(suffix + " in " + directory)


def split_biene_verses(line):
    """Zeilen wieder trennen, die in der Biene-Datei ohne Leerraum verklebt sind."""
    line = re.sub(r"([a-zäöüß])([A-ZÄÖÜ])", r"\1\n\2", line)
    line = re.sub(r"([,;:.!?])([A-ZÄÖÜ\"„])", r"\1\n\2", line)
    line = re.sub(r" --([A-ZÄÖÜ])", r" --\n\1", line)
    return [nfc(part).strip() for part in line.split("\n") if part.strip()]


def is_aurora_editorial(line):
    if line == "Aurora":
        return True
    if line.startswith("„Siebzehn Lieder"):
        return True
    if line.startswith("Nach HSA"):
        return True
    if re.match(r"DHA\s+[IVX]", line):
        return True
    return False


def is_biene_editorial(line):
    if line.startswith("J3"):
        return True
    if re.match(r"DHA\s+[IVX]", line):
        return True
    return False


def verses_from_docx(path, editorial):
    lines = []
    for paragraph in paras(path):
        raw = nfc(paragraph).strip()
        if not raw:
            lines.append("")
            continue
        if editorial(raw):
            lines.append("")
            continue
        if editorial is is_biene_editorial:
            lines.extend(split_biene_verses(raw))
        else:
            lines.append(raw)
    return collapse_blanks(lines)


def strip_page_marks(line):
    cleaned = re.sub(r"\s*\[\d+\]\s*", " ", line)
    cleaned = re.sub(r" {2,}", " ", cleaned)
    return nfc(cleaned).strip()


def verses_from_mueller(path):
    lines = []
    for paragraph in paras(path):
        if paragraph.strip() == "":
            lines.append("")
            continue
        cleaned = strip_page_marks(paragraph)
        lines.append(cleaned if cleaned else "")
    return collapse_blanks(lines)


KANDIDAT = nfc("""\
I.

Ich lag, im Waldesschatten,
Träumend im grünen Gras,
Die kleinen, zarten Waldblümchen
Erzählten mir dies und das.

Erzählten von ihrer Liebe
Geschichten gar bunt und toll,
So übermüthig neckisch,
So trüb' und trauervoll.

Dazwischen rauschten die Wipfel
Und sangen die Vögelein,
Sie sangen süße Mährchen,
Uralte Melodei'n.

Und seltsam murmelt' das Bächlein
Und blitzte im Sonnenstrahl;
In weiter Ferne aber
Da klagte die Nachtigall.

II.

Es hat über Nacht gethauet,
Die Blumen und Gräser sind nass;
Ich hab' über Nacht geweinet,
Doch weiß ich nicht, um was.

Die Blumen schauen sehnend
Hinauf zur blauen Höh';
Es hat mein Herz beschlichen
Im Traum ein dunkles Weh.

III.

Die junge Möve flattert
Weit über die tiefe See;
O Liebchen, du fernes Liebchen,
Wie wird mir doch so weh!

Sie flattert wol gar hinüber
– Ich sehe sie nicht mehr –
Hinüber zu ihr, hinüber!
Mein Herz, poch' nicht zu sehr.

Wie lieb' ich dich, o Liebchen,
Mit heißer Liebesgluth!
Ach, zwischen uns beiden lieget
Mehr, als die tiefe Fluth.

IV.

Es hat ein Stern geleuchtet
In dunkler, dunkler Nacht,
Da ist aus seinem Schlummer
Der See wildrauschend erwacht.

Das Schilf am Ufer zittert –
Die Nixe taucht hervor
Mit bleichen, blassen Wangen,
Sie schaut zum Stern empor.

Sie schaut mit wildem Sehnen
Empor zum lichten Stern,
Und weinet helle Thränen –
Er strahlt so kalt und fern!

V.

O, könnt' ich dich einmal pressen
Glühend an meine Brust!
Einmal! und dann vergessen
Liebe und Leid und Lust.

Glühende Küsse trinken,
Bis hell der Tag erwacht –
Einmal! dann sterben und sinken
In öde, ewige Nacht.

VI.

Blaublümchen will ich pflücken
Blaublümchen und Rosenblüth';
Die Blumen blühen im Maien,
Die Vögel singen ihr Lied.

Hoch in den Blüthenzweigen
Sie sitzen und singen so frei:
„Wem willst du die Blumen geben
Im hellen, blühenden Mai?"

Wem ich die Blumen will geben?
Ich will sie geben dem Bach,
Der kann sie immer treiben,
Wohin er will und mag.

Und wieder will ich mich setzen
Am kleinen, schnellen Bach,
Und still für mich dort weinen
Und schauen den Blumen nach.

VII.

Die Blumenaugen sehen
Mich an so traut und still,
Als könnten sie verstehen,
Was nur mein Herze will;

Als könnten sie es wissen,
Mein junges Liebesleid,
Das mir ins Herz geschlichen
Zu dieser Frühlingszeit.

VIII.

Beim Frühlingsruf erwachen
Die kleinen Blumen all,
Die Vögel singen und fliegen
Wol über Berg und Thal.

Ach, fern im tiefen Thale,
Wie blühet da der Mai!
Da steht ein feines Häuschen,
Die Vögel fliegen vorbei.

Du süßes Lieb, es fliegen
Vorbei die Vögelein!
Sie können dir nicht sagen
Und klagen meine Pein.

IX.

Sein lautes, herzliches Lachen
Das weckte einst in mir Verlangen,
Dein lautes, herzliches Lachen
Das peinigt mich nun wie Schlangen.

Dein lautes, herzliches Lachen
Und jener dumme Geselle
Verfolgen mich im Traume,
Dann träumt mir von der Hölle.

X.

Vor meiner Liebsten Hause
Da quillt ein Brünnelein,
Da sitz' ich alle Abend
Wol auf dem harten Stein.

Da sitz' ich alle Abend
Bis in die tiefe Nacht,
Und starre nach dem Hause,
Das Brünnlein rauschet sacht.

Das Brünnlein rauschet traurig,
Verlassen steht das Haus,
Die klagenden Winde gehen
Dort hallend ein und aus.

Mein Lieb ist fortgezogen,
Der Brunn ist kühl und tief, –
Fürwahr, mir wäre besser,
Wenn ich da unten schlief!
""")


def kandidat_teil(start, end):
    """Gedichte start bis end einschließlich, römisch I=1 … X=10."""
    marks = ["I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.", "X."]
    lines = KANDIDAT.split("\n")
    # drop trailing empty from split of final newline-less string
    if lines and lines[-1] == "":
        lines.pop()
    indices = [i for i, line in enumerate(lines) if line in marks]
    start_at = indices[start - 1]
    end_at = indices[end] if end < len(indices) else len(lines)
    return lines[start_at:end_at]


DHA_PREFIX = re.compile(r"^DHA\s+[IVX]+,\s*\d+(?:\s*f+\.?)?\s*")


def normalize_heine(text):
    text = nfc(text).replace("\u00a0", " ")
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = re.sub(r"\s*·\s*", " ", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def split_glued(raw):
    """Verse trennen, die in der Vorlage ohne Leerzeichen aneinanderhängen."""
    text = normalize_heine(raw)
    breaks = set()
    quotes = 0
    for i, ch in enumerate(text):
        if ch == '"':
            quotes += 1
        if i == 0:
            continue
        prev = text[i - 1]
        if prev == '"' and ch.isupper():
            glued_to_quote = i >= 2 and not text[i - 2].isspace()
            if quotes % 2 == 1 and glued_to_quote:
                breaks.add(i - 1)
            elif quotes % 2 == 0:
                breaks.add(i)
        elif prev == "'" and ch.isupper() and i >= 2 and text[i - 2].islower():
            breaks.add(i)
        elif prev.islower() and ch.isupper():
            breaks.add(i)
        elif prev in ",;:.!?" and ch.isupper():
            breaks.add(i)
        elif text[i - 3:i] == " --" and ch.isupper():
            breaks.add(i)
    if not breaks:
        return [text] if text else []
    lines = []
    start = 0
    for index in sorted(breaks):
        if index <= start:
            continue
        piece = text[start:index].strip()
        if piece:
            lines.append(piece)
        start = index
    tail = text[start:].strip()
    if tail:
        lines.append(tail)
    return lines


def heine_meta_line(line):
    if line.startswith("Agrippina (="):
        return "drop"
    if line.startswith("Westdeutscher Musenalmanach"):
        return "drop"
    if line.startswith("(nach HSA"):
        return "drop"
    if line == "<ohne Titel>":
        return "drop"
    if line.startswith("{*}"):
        return "blank"
    return None


def verses_heine(path, glued):
    lines = []
    for paragraph in paras(path):
        raw = normalize_heine(paragraph)
        if not raw:
            lines.append("")
            continue
        kind = heine_meta_line(raw)
        if kind == "drop":
            lines.append("")
            continue
        if kind == "blank":
            lines.append("")
            continue
        match = DHA_PREFIX.match(raw)
        if match:
            raw = raw[match.end():].strip()
            if not raw:
                lines.append("")
                continue
        if glued:
            lines.extend(split_glued(raw))
        else:
            lines.append(raw)
    return space_section_marks(collapse_blanks(lines))


def space_section_marks(lines):
    """Leerzeile um reine Abschnittszahlen, wenn die Vorlage sie an den Vers klebt."""
    marked = []
    for line in lines:
        if re.fullmatch(r"[IVX]+\.|\d+", line) and marked and marked[-1] != "":
            marked.append("")
        marked.append(line)
    spaced = []
    for index, line in enumerate(marked):
        spaced.append(line)
        if re.fullmatch(r"[IVX]+\.|\d+", line):
            nxt = marked[index + 1] if index + 1 < len(marked) else ""
            if nxt != "":
                spaced.append("")
    return collapse_blanks(spaced)


def resolve_heine(filename):
    heine = os.path.join(BASE, "Heine")
    target = nfc(filename)
    for name in os.listdir(heine):
        if nfc(name) == target:
            return os.path.join(heine, name)
    raise FileNotFoundError(filename)


def report(label, lines):
    text = "\n".join(lines)
    words = re.findall(r"\S+", text)
    apostrophes = text.count("'")
    commas = text.count(",")
    print(
        f"{label}: zeilen={len(lines)} wörter={len(words)} "
        f"apostrophe={apostrophes} kommata={commas}"
    )


def main():
    heine = os.path.join(BASE, "Heine")
    mueller = find_dir("M")
    # Müller, nicht andere M-Ordner
    for name in os.listdir(BASE):
        if name.replace("ü", "u").replace("\u0308", "") == "Muller" or "ller" in name and os.path.isdir(os.path.join(BASE, name)):
            if "Waldhorn" in "".join(os.listdir(os.path.join(BASE, name))) or any(
                "Waldhorn" in fn or "Wilhelm" in fn for fn in os.listdir(os.path.join(BASE, name))
            ):
                mueller = os.path.join(BASE, name)
                break
    kandidat_dir = os.path.join(BASE, "Kandidat")
    out_dir = os.path.join(BASE, "corpus_diplomatisch")

    aurora_path = os.path.join(heine, "Heine_Aurora(1823).docx")
    biene_path = os.path.join(heine, "Heine_Die Biene_(1823:1826, anonym).docx")
    mueller1_path = find_file(mueller, "_1.docx")
    mueller2_path = find_file(mueller, "Waldhornist_2.docx")

    aurora = verses_from_docx(aurora_path, is_aurora_editorial)
    biene = verses_from_docx(biene_path, is_biene_editorial)
    mueller1 = verses_from_mueller(mueller1_path)
    mueller2 = verses_from_mueller(mueller2_path)
    kandidat = [line for line in KANDIDAT.split("\n") if line is not None]
    if kandidat and kandidat[-1] == "":
        kandidat.pop()

    weitere = {
        "Heine_Agrippina.txt": verses_heine(
            resolve_heine("Heine_Agrippina(1824, anonym).docx"), glued=False
        ),
        "Heine_Almanach.txt": verses_heine(
            resolve_heine("Heine_Westdeutscher Musenalmanach 1823.docx"), glued=False
        ),
        "Heine_Heimkehr.txt": verses_heine(
            resolve_heine("Heine_Heimkehr_Der Gesellschafter.docx"), glued=False
        ),
        "Heine_Kevlaar.txt": verses_heine(
            resolve_heine("Heine_Wallfahrt nach Kevlaar.docx"), glued=True
        ),
        "Heine_DonnaClara.txt": verses_heine(
            resolve_heine("Heine_Donna Clara.docx"), glued=True
        ),
        "Heine_Ballade.txt": verses_heine(
            resolve_heine("Heine_Götterdämmerung.docx"), glued=True
        ),
        "Heine_Ratcliff.txt": verses_heine(
            resolve_heine("Heine_Ratkliff.docx"), glued=True
        ),
    }

    targets = {
        os.path.join(heine, "Heine_Aurora.txt"): aurora,
        os.path.join(out_dir, "Heine_Aurora.txt"): aurora,
        os.path.join(heine, "Heine_Biene.txt"): biene,
        os.path.join(out_dir, "Heine_Biene.txt"): biene,
        os.path.join(mueller, "Mueller_1.txt"): mueller1,
        os.path.join(out_dir, "Mueller_1.txt"): mueller1,
        os.path.join(mueller, "Mueller_2.txt"): mueller2,
        os.path.join(out_dir, "Mueller_2.txt"): mueller2,
        os.path.join(kandidat_dir, "Kandidat_Vagabund.txt"): kandidat,
        os.path.join(out_dir, "Kandidat_Vagabund.txt"): kandidat,
        os.path.join(kandidat_dir, "Kandidat_I-V.txt"): collapse_blanks(kandidat_teil(1, 5)),
        os.path.join(kandidat_dir, "Kandidat_VI-X.txt"): collapse_blanks(kandidat_teil(6, 10)),
    }
    for name, lines in weitere.items():
        targets[os.path.join(heine, name)] = lines
        targets[os.path.join(out_dir, name)] = lines

    # Müller-Dateinamen im Ordner können NFD sein. Bestehende Dateien treffen.
    def existing_or(path):
        directory = os.path.dirname(path)
        base_name = os.path.basename(path)
        target_nfc = nfc(base_name)
        if not os.path.isdir(directory):
            return path
        for name in os.listdir(directory):
            if nfc(name) == target_nfc:
                return os.path.join(directory, name)
        return path

    written = []
    for path, lines in targets.items():
        path = existing_or(path)
        write_text(path, lines)
        written.append((path, lines))

    print("Geschrieben:")
    for path, lines in written:
        report(os.path.relpath(path, BASE), lines)

    blob_aurora = "\n".join(aurora)
    blob_biene = "\n".join(biene)
    blob_m1 = "\n".join(mueller1)
    blob_m2 = "\n".join(mueller2)
    blob_k = "\n".join(kandidat)
    assert "DHA" not in blob_aurora and "DHA" not in blob_biene
    assert "HSA" not in blob_aurora
    assert "an's" in blob_aurora
    assert "Macht's" in blob_biene
    assert "Hab' ich" in blob_biene
    assert "lad'" in blob_m1
    assert "[" not in blob_m2 and "[" not in blob_m1
    assert "trüb'" in blob_k and "Melodei'n" in blob_k and "sitz'" in blob_k
    assert "Gottschall" not in blob_k and "Königskrone" not in blob_k
    assert "Feme" not in blob_k and "schlieft" not in blob_k
    assert blob_k.startswith("I.\n")
    assert "\nX.\n" in blob_k
    for name, lines in weitere.items():
        blob = "\n".join(lines)
        assert "DHA" not in blob and "HSA" not in blob, name
        assert "Agrippina (=" not in blob
        long = [line for line in lines if len(line) > 85]
        if long:
            print("LANGE ZEILEN", name)
            for line in long:
                print(" ", len(line), line)
    assert "Auf den Wällen Salamankas" in "\n".join(weitere["Heine_Agrippina.txt"])
    assert "Altes Kaminstück." in "\n".join(weitere["Heine_Agrippina.txt"])
    assert "an's Fressen" in "\n".join(weitere["Heine_Almanach.txt"])
    assert "Mährchen aus alten Zeiten" in "\n".join(weitere["Heine_Heimkehr.txt"])
    wall = "\n".join(weitere["Heine_Kevlaar.txt"])
    assert "Zu schau'n die Prozession?" in wall
    assert "Inbrünstiglich beten und singen:" in wall
    assert "Gelobt sey'st du Marie!" in wall
    donna = "\n".join(weitere["Heine_DonnaClara.txt"])
    assert "Eu'r Geliebter," in donna
    assert "Unbekannte Ritter vor ihr." in donna
    goetter = "\n".join(weitere["Heine_Ballade.txt"])
    assert "goldnen Lichtern" in goetter and "Lorgnett'" in goetter
    rat = "\n".join(weitere["Heine_Ratcliff.txt"])
    assert "schauert'" in rat and "Marg'reth'" in rat
    assert 'Leute."' in rat
    print("Prüfungen bestanden.")


if __name__ == "__main__":
    main()
