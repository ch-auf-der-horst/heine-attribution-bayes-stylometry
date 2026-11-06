# Protokoll der Studie 2

Studie 2 wiederholt Studie 1 mit derselben Probenlänge, demselben Seed und denselben Schwellen. Der einzige Unterschied der Dateiliste ist: `Geibel_Lieder.txt`, `Geibel_Buecher.txt` und `Geibel_Sonette.txt` sind ausgeschieden. Sie werden nicht als Ablenker und nicht als Profil verwendet. Die Dateien werden nur gelesen, um die Wortzahl zu prüfen.

Dieser Lauf ist nach Studie 1 angesetzt. In Studie 1 war Geibel der nächste einzelne Profilabstand. Studie 2 prüft, ob der Ausgang ohne diesen Ablenker derselbe bleibt. Sie ist keine zweite, vorher festgelegte Hauptprüfung.

Aufruf vom Projektordner aus:

    AUTOR_STUDIE=2 python3 analyse/00_lauf.py

Die Ergebnisse liegen in `ergebnisse/studie2/`. Studie 1 wird dabei nicht überschrieben.
