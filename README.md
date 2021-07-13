# Evaluierung von Recommendation-Algorithmen für regionale Plattformen

In diesem Repository befindet sich der Quellcode der Bachelorthesis "Evaluierung von Recommendation-Algorithmen für regionale Plattformen" von Sarah Ternus. 

**Anleitung - Einrichten des Projektes**

1. Klonen des Repositorys - `git clone https://gitlab.rlp.net/s18a24897903/bt-ternus.git`
2. Erstellen einer virtuellen Umgebung (conda oder venv) - `python -m venv venv` 
3. Installieren der benoetigten Python Modules gelistet in der requirements.txt - `pip install -r requirements.txt`

**Anleitung - Ausfuehren des Codes**

(Hybriden) Datensatz mit Standorteinbeziehung erstellen:
1. Ordner _database_ unter _src_ erstellen
2. Ordener _location_ unter _datasets_ erstellen
3. Unter _DatasetGenerationOwn_ die Skripte in folgender Reihenfolge ausführen (und ggf. Pfade anpassen):
    - createTables.py
    - fillTables.py
    - generateDatasets.py
4. Dann unter _PredictionAlgorithms_ das Skript includeLocation ausführen (und ggf. Pfade anpassen)

-> Unter Datasets ist nun eine reduzierte CSV-Datei mit der Standorteinbeziehung zu finden

Empfehlung erzeugen:
1. Das Skript zur gewuenschten Recommendation-Technik unter _PredictionAlgorithms_ auswaehlen:
    - memorybased.py
    - modelbased.py
2. In der _main_ die Funktion für gewuenschten Recommendation-Algorithmus auswaehlen:
    - memorybased.py: _calculate_predictions_knn_, _calculate_predictions_knn_means_, _calculate_predictions_knn_zscore_
    - modelbased.py: _calculate_predictions_svd_, _calculate_predictions_svdpp_, _calculate_predictions_nmf_

-> Es werden in der Konsole für jeden Nutzer die besten 10 Recommendations ausgegeben

Recommendation-Algorithmen testen:
1. Das gewuenschte Skript ausfueren zum Testen der Recommendation-Technik
    - testMemorybased.py
    - testModelbased.py
    - testRandom.py





