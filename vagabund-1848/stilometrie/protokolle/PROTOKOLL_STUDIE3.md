# Protokoll der Studie 3

Studie 3 wiederholt Studie 1 mit derselben Probenlänge, demselben Seed und denselben Schwellen. Der einzige Unterschied der Dateiliste ist der Geibel-Text. An der Stelle von `Geibel_Lieder.txt` steht `Geibel_Junius.txt`, der Abschnitt Lieder aus Emanuel Geibel, *Juniuslieder*, Stuttgart und Tübingen: Cotta, 1848. `Geibel_Lieder.txt`, `Geibel_Buecher.txt` und `Geibel_Sonette.txt` bleiben ausgeschieden. Sie werden gelesen, um die Wortzahl zu prüfen, und gehen nicht in die Ablenker und nicht in die Profile.

Die Schwellen werden nicht neu gesetzt. Studie 3 ist nach Studie 1 angesetzt. Dort war das Geibel-Profil der Gedichte von 1849 der nächste einzelne Abstand, und der Ausgang war unentschieden. Studie 3 prüft denselben Vergleich mit dem zeitnäheren Liederabschnitt von 1848. Sie ersetzt Studie 1 und Studie 2 nicht.

Aufruf vom Projektordner aus:

    AUTOR_STUDIE=3 python3 analyse/00_lauf.py

Die Ergebnisse liegen in `ergebnisse/studie3/`. Studie 1 und Studie 2 werden dabei nicht überschrieben.
