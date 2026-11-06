# -*- coding: utf-8 -*-
"""Schneidet die Eichproben der Studie 1.

Liest die Dateiliste analyse/studie1_dateien.csv.
Verbindet die Heine-Dateien und die Hektor-Lieder zu je einem Wortstrom.
Zieht mit dem Seed aus studie1_parameter.py einen Versatz und schneidet
nicht überlappende Proben der festgelegten Länge. Dieselbe Anzahl
entsteht in den 100 Versatz-Wiederholungen. Ablenker werden ohne
Zufallszahl über den jeweiligen Text verteilt.

Der Kandidat wird in diesem Skript nicht geöffnet.

Schreibt in den Laufordner:
- proben/*.txt, eine Probe je Datei, ein Token je Zeile
- teilung.json mit Versatz und Anfangsstellen
- eingaben.csv mit Prüfsummen der gelesenen Dateien
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from laufwahl import parameter as p
import gemeinsame as g


def klassenname(relativer_pfad):
    stamm = Path(relativer_pfad).stem
    for anfang, name in (
        ("Mueller", "mueller"),
        ("Wunderhorn", "wunderhorn"),
        ("Uhland", "uhland"),
        ("Geibel", "geibel"),
    ):
        if stamm.startswith(anfang):
            return name
    raise SystemExit("Kein Klassenname für " + relativer_pfad)


def schreibe_probe(ordner, name, nummer, probe):
    pfad = ordner / f"{name}_{nummer:02d}.txt"
    pfad.write_text("\n".join(probe) + "\n", encoding="utf-8")


def main():
    if not p.LAUF.is_dir():
        raise SystemExit("Laufordner fehlt. Zuerst 00_lauf.py ausführen.")
    rng, _, _ = g.generatoren()
    for eintrag in g.eintraege("ausgeschieden"):
        g.lade_text(eintrag)
    heine, heine_dateien = g.wortstrom("heine")
    hektor, hektor_dateien = g.wortstrom("hektor")
    versatz_heine = g.ziehe_versatz(len(heine), rng)
    versatz_hektor = g.ziehe_versatz(len(hektor), rng)
    starten_heine, proben_heine = g.schnitte_ab(heine, versatz_heine)
    starten_hektor, proben_hektor = g.schnitte_ab(hektor, versatz_hektor)
    if not proben_heine or not proben_hektor:
        raise SystemExit("Eine Primärteilung hat keine Probe ergeben")
    k = min(len(proben_heine), len(proben_hektor))
    proben_ordner = p.LAUF / "proben"
    proben_ordner.mkdir()
    for nummer, probe in enumerate(proben_heine[:k], start=1):
        schreibe_probe(proben_ordner, "heine", nummer, probe)
    for nummer, probe in enumerate(proben_hektor[:k], start=1):
        schreibe_probe(proben_ordner, "hektor", nummer, probe)

    ablenker = {}
    for eintrag in g.eintraege("ablenker"):
        name = klassenname(eintrag["pfad"])
        woerter = g.lade_text(eintrag)
        paare = g.spreiz_schnitte(woerter, k)
        if len(paare) < 5:
            raise SystemExit(f"{name} liefert weniger als 5 Proben")
        ablenker[name] = {
            "pfad": eintrag["pfad"],
            "starts": [start for start, _ in paare],
            "anzahl": len(paare),
        }
        for nummer, (_, probe) in enumerate(paare, start=1):
            schreibe_probe(proben_ordner, name, nummer, probe)

    versatz = []
    for _ in range(p.WIEDERHOLUNGEN):
        v_heine = g.ziehe_versatz(len(heine), rng)
        v_hektor = g.ziehe_versatz(len(hektor), rng)
        s_heine, _ = g.schnitte_ab(heine, v_heine)
        s_hektor, _ = g.schnitte_ab(hektor, v_hektor)
        if len(s_heine) < k or len(s_hektor) < k:
            raise SystemExit("Eine Versatz-Teilung hat weniger Proben als die Primärteilung")
        versatz.append(
            {
                "heine_offset": v_heine,
                "hektor_offset": v_hektor,
                "heine_starts": s_heine[:k],
                "hektor_starts": s_hektor[:k],
            }
        )

    teilung = {
        "probenlaenge": p.PROBENLAENGE,
        "k": k,
        "heine_dateien": heine_dateien,
        "hektor_dateien": hektor_dateien,
        "heine_woerter": len(heine),
        "hektor_woerter": len(hektor),
        "primaer": {
            "heine": {"offset": versatz_heine, "starts": starten_heine[:k]},
            "hektor": {"offset": versatz_hektor, "starts": starten_hektor[:k]},
            "ablenker": ablenker,
        },
        "versatz": versatz,
    }
    g.schreibe_json(p.LAUF / "teilung.json", teilung)

    with (p.LAUF / "eingaben.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["pfad", "rolle", "wortzahl", "sha256", "in_der_eichung_gelesen"],
        )
        writer.writeheader()
        for zeile in g.dateiliste():
            gelesen = zeile["rolle"] != "kandidat"
            writer.writerow(
                {
                    "pfad": zeile["pfad"],
                    "rolle": zeile["rolle"],
                    "wortzahl": zeile["wortzahl"],
                    "sha256": g.pruefsumme(g.pfad_zu(zeile)) if gelesen else "",
                    "in_der_eichung_gelesen": "nein" if zeile["rolle"] == "kandidat" else "ja",
                }
            )
    print(f"Primärproben je Verfasser: {k}")
    print("Ablenker: " + ", ".join(f"{name} {block['anzahl']}" for name, block in ablenker.items()))
    print(f"Versatz-Wiederholungen: {len(versatz)}")


if __name__ == "__main__":
    main()
