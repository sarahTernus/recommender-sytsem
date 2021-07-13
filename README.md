# Evaluierung von Recommendation-Algorithmen für regionale Plattformen

In diesem Repository befindet sich der Quellcode der Bachelorthesis "Evaluierung von Recommendation-Algorithmen für regionale Plattformen" von Sarah Ternus. 

**Anleitung - Einrichten des Projektes**

1. Klonen des Repositorys - `git clone https://gitlab.rlp.net/s18a24897903/bt-ternus.git`
2. Erstellen einer virtuellen Umgebung (conda oder venv) - `python -m venv venv` 
3. Installieren der benötigten Python Modules gelistet in der requirements.txt - `pip install -r requirements.txt`

**Anleitung - Ausführen des Codes**

(Hybriden) Datensatz mit Standorteinbeziehung erstellen:
1. Ordner _database_ unter _src_ erstellen
2. Ordener _location_ unter _datasets_ erstellen
3. Unter _DatasetGenerationOwn_ die Skirpte in folgender Reihenfolge ausführen:
    - createTables.py
    - fillTables.py
    - generateDatasets.py


