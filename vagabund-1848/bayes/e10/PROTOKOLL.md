# E-10 Pointenzählung – Protokoll (festgelegt 19.10.2026, 12:45, vor jeder Kodierung)

Frage: Enden die Kandidaten seltener mit einer Pointe als (a) vergleichbare Heine-Lieder, (b) zeitgenössische Heine-Nachahmungen?

Einheit: ein Gedicht; beurteilt werden die letzte Strophe bzw. die letzten zwei Verse vor dem Hintergrund des Gedichts.

Kodierung (ein Kodierer, nicht verblindet; die Schlussverse werden zitiert, damit jede Entscheidung nachprüfbar ist):
- ja (1): ironischer Umschlag / Stimmungsbruch – der Schluss dementiert, ernüchtert oder verspottet die aufgebaute Stimmung (Bathos, Selbstironie, Registerwechsel ins Prosaische/Alltägliche).
- teilweise (0.5): zugespitzte Schlusswendung ohne Ironie – Antithese, überraschender Kontrast, Sentenz.
- nein (0): Schluss setzt die Stimmung fort, rundet ab, steigert oder wiederholt.

Gruppen:
- K: die 10 Kandidaten (Vagabund 1848).
- H: Heine, Buch der Lieder (1827), Lyrisches Intermezzo + Heimkehr; alle Gedichte aus 2–4 vierzeiligen Strophen (Länge wie K); daraus 30 per Zufall (random.seed(1848)).
- N: Nachahmer – Liederbuch dreier Freunde (1843), Zweites Buch (Liebeslieder), alle Gedichte aus 2–6 vierzeiligen Strophen, ohne Byron-Übersetzungen; dazu die Singh-Funde (Bd. 7–9) außer Auszügen (Raabe).

Auswertung: Anteil ja / ja+teilweise je Gruppe; Wilson-Intervalle; LR für „K hat so wenige Pointen“ unter H vs N per Binomial mit dem Gruppenanteil (Glättung (k+0.5)/(n+1)).
Grenze: sagt etwas zu H1 vs H3 (Nachahmer), kaum zu H2 (bewusster Mystifikator kann Pointen meiden). Darf nicht zusätzlich zum Qualitätsurteil gezählt werden.
