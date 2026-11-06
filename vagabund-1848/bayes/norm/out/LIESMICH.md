# Angeglichene Schicht (Protokoll II.3, Punkt 5)

Erzeugt am 16.10.2026 mit `angleichen.py`. Alle Korpora wurden nach derselben festen Regelliste behandelt. Zeilen, Verse, Satzzeichen und Wortzahl bleiben gleich, das ist im Skript geprüft. Der Kandidat ist nicht enthalten.

## Regeln
- **R1 th → t.** Ausgenommen sind Fremdwörter und Namen, die heute noch th schreiben (Thron, Theater, Zither, Lethe, Bethlehem …), sowie Kompositionsfugen t|h (Gast|hof, Gott|heit, dort|hin, ent|halten …).
- **R2 ey → ei.** Ausgenommen ist der Name Meyer.
- **R3** aͤ/oͤ/uͤ → ä/ö/ü; Ae/Oe/Ue am Wortanfang → Ä/Ö/Ü.
- **R4** Apostrophvarianten → '.
- **R5** alle Anführungszeichen → ".
- **R6** – → —.

## Dateien
- `korpus/*_ang.txt`: die Dateien aus `corpus_diplomatisch` und das restituierte Buch der Lieder.
- `A2/Gedichte`, `A2/Bloecke_548`: A2 in angeglichener Form, gleiche Dateinamen wie in der historischen Fassung.
- `Angleichung_je_Datei.csv`: Zahl der Eingriffe je Regel und Datei.
- `Angleichung_Ersetzungen.csv`: jede einzelne Ersetzung (vorher → nachher, Anzahl), zur Prüfung.
- `angleichen.py`: das Skript. Der Kandidat wird später mit genau diesem Skript angeglichen (Aufruf: `python3 angleichen.py ein.txt aus.txt`).

## Befund zur Schreibung
Die Schreibung „ey“ (sey, bey, zwey) kommt je 1000 Wörter so oft vor:

| Korpus | „ey“ je 1000 Wörter |
| --- | ---: |
| A2 (Heine-Erstdrucke bis 1824) | 9,7 |
| Heines Zeitschriftendrucke (Heine_*.txt) | 3 bis 13 |
| Wunderhorn 1806 | 11 |
| Buch der Lieder 1827 | 2,3 |
| Uhland | 2 |
| Geibel | unter 1 |
| Hektor, Müller, Steinmann | 0 |

Die historische Schreibung markiert damit Druckjahr und Hausschreibung, nicht den Verfasser. Ein Druck von 1848 wie der Kandidat sähe in den Zeichen-4-Grammen schon deshalb „unheinisch“ aus. Prüfung 2d ist deshalb notwendig. Es ist zu erwarten, dass die angeglichene Schicht gilt.

## Hinweis
Die Dateien Heine_Agrippina (Juli 1824) und Heine_Biene (1826) liegen nach der Grenze von A2. Die übrigen Heine_*-Dateien überschneiden sich mit A2. Für die Gegenprobe ist nur A2 maßgeblich.
