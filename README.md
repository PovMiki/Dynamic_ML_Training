Zadanie 1: Zbieranie danych z produkcji i przygotowanie modelu do monitorowania

<img width="752" height="803" alt="image" src="https://github.com/user-attachments/assets/03045ea3-e2d8-4481-9897-0c144108df66" />

Za pomocą make_classification wygenerowałem sztuczne zbiory danych : 
- zbiór historczny reprezentuje dane historyczne które posłużyły do trenowania i walidacji
- zbiór produkcyjny który pozwala na późniejsze badanie Data Drift
W celu uzyskania predykcji zainicjalizowałem RandomForestClassifier. Proces model.fit został przeprowadzony tylko na zbiorze historycznym. Następnie wytrenowany model został użyty do predykcji na danych produkcyjnych

Wywołanie metod .shape i .info pozwoliły na zweryfikowanie poprawności środowiska. Zbiór treningowy posiada wymiary 500,6, produkcyjny 300,7 a raport info potwierdził brak nanów

Zadanie 2 : Wykrywanie driftu danych z biblioteką Evidently

<img width="726" height="260" alt="image" src="https://github.com/user-attachments/assets/13bb0720-894c-4e77-a0f1-0e2ae6c88391" />

Za pomocą obiektu Report skonfigurowałem szablon DataDriftPresent który automatycznie dobiera testy w zależności od typów zmiennych. Wywołanie metody run wymagało podania danych referencyjnych (df_train) i aktualnych (current_data). Ze zbioru produkcyjnego celowo odrzuciłem kolumnę prediction za pomocą .drop aby badać te same cechy

<img width="1725" height="702" alt="image" src="https://github.com/user-attachments/assets/1e70a25e-a7c3-456b-8035-88c8370e9a9d" />


Wyniki porównania zostały zapisane do data_drift_report za pomocą metody .save_html. Dataset Drift wyświetla procentowy udział dryfujących cech. Raport generuje wykresy gęstości rozkładu dla każdej cechy osobno

Zadanie 3: Analiza jakości predykcji po wdrożeniu

<img width="720" height="464" alt="image" src="https://github.com/user-attachments/assets/939eb7a0-ea81-49fa-aacd-5bc81f339b0c" />

Zainicjalizowałem DataDefinition w którym jest klasyfikacja binarna. Wskazuje się tam kolumnę zawierającą rzeczywiste etykiety klas oraz przechowującą decyzje podjęte przez model. Przed dokonaniem ewaluacji df_train musiał zostać uzupełniony o bazowe predykcje aby porównać predykcje. Obie struktury danych DataFrame zostały opakowane za pomocą Dataset.from_pandas()

<img width="1761" height="894" alt="image" src="https://github.com/user-attachments/assets/13736aaa-0a43-435f-aec2-0bf457855129" />

Accuracy dla current wynosi idealnie 1.0 a zbiór referencyjny osiąga 0.353. Confusion Matrix potwierdza że model bezbłędnie klasyfikuje nowe dane z produkcji natomiast generuje masowe błędy na danych historycznych. Zajzd metryk potwierdza wystąpienie Model Drift.

**Wnioski :**

Laboratorium pozwoliło na wdrożenie monitorowania modelu uczenia maszynowego za pomocą Evidently. Analiza wykazała obecność Data Driftu pomiędzy danymi historycznymi a nowym zbiorem produkcyjnym.
