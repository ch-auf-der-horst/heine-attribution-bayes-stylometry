"""Zentrale Pfade der Bayes-Arbeitsskripte.

Alle Pfade werden relativ zu diesem Ordner bestimmt. Wer die Skripte an
einen anderen Ort verschiebt, kann sie mit Umgebungsvariablen umlenken:

  BAYES_ARBEIT  Ordner mit kal/, norm/, out/, e11/ (Standard: Elternordner von kal/)
  AA_KORPUS     Ordner corpus_diplomatisch (Standard: wird gesucht, s. u.)

Beim Import wechselt das Arbeitsverzeichnis nach kal/, damit die
Ergebnisdateien (kalibrierung.json, e1.json …) wie bisher dort liegen,
gleich von wo aus ein Skript gestartet wird.
"""
import os
import sys
from pathlib import Path

KAL = Path(__file__).resolve().parent
ARBEIT = Path(os.environ.get('BAYES_ARBEIT', KAL.parent)).resolve()


def _korpus():
    if os.environ.get('AA_KORPUS'):
        return Path(os.environ['AA_KORPUS']).resolve()
    kandidaten = [ARBEIT.parents[1] / 'corpus_diplomatisch',   # AuthorshipAttribution/Repositorium_Vorbereitung/Bayes_Arbeitsskripte
                  ARBEIT.parent / 'korpus',                     # künftiges Repositorium: bayes/ neben korpus/
                  ARBEIT.parent / 'corpus_diplomatisch']
    for k in kandidaten:
        if (k / 'Kandidat_Vagabund.txt').is_file():
            return k
    raise FileNotFoundError('corpus_diplomatisch nicht gefunden; Umgebungsvariable AA_KORPUS setzen.')


KORPUS = _korpus()
KANDIDAT = KORPUS / 'Kandidat_Vagabund.txt'
NORM = ARBEIT / 'norm'
OUT = ARBEIT / 'out'
E11 = ARBEIT / 'e11'

os.chdir(KAL)
if str(NORM) not in sys.path:
    sys.path.insert(0, str(NORM))
