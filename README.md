Zadanie 1 : Konfiguracja środowiska Apache Airflow

<img width="512" height="390" alt="image" src="https://github.com/user-attachments/assets/3cf9651e-09f3-41aa-a3f3-5af9913e4cd0" />

W tym zadaniu wdrożyłem Airflow używając docker compose. W kontenerze uruchomiła się komenda standalone co automatycznie stworzyło bazę danych, przeprowadziło migrację a następnie stworzył unikalne hasło do którego można się dostać za pomocą docker exec cat ... /standalone_admin_password.txt. Jest to metoda bezpieczniejsza i nie produkuje błędów migracyjnych po nadpisywaniu zainicjalizowanej pustej bazy danych danymi pierwszego usera.

<img width="1450" height="542" alt="image" src="https://github.com/user-attachments/assets/3cf31b9d-9a37-4612-8ddc-21c70c936dc7" />

Na localhost 8085 widać że docker poprawnie wstał z Apache Airflow oraz jestem w stanie się do niego zalogować

Zadanie 2 : Prosty DAG do re-trenowania modelu

<img width="843" height="861" alt="image" src="https://github.com/user-attachments/assets/19b4ed53-eb92-4f09-a47f-c2ba0a993c33" />

Stworzyłem funkcję która wczytuje dane, następnie za pomocą klasyfikatora RandomForest model jest trenowany. Data i godzina są formatowane do timestampa co robi za wersjonowanie, ponieważ data dopisywana do treningu jest unikalna i nie nadpisze starych modeli nowa data. Za pomocą metody score obliczam dokładność dopasowania modelu co odpowiada za moją walidację. W DAG ustawiłem sztywny harmonogram wykonywania procesu co jeden dzień

<img width="1770" height="353" alt="image" src="https://github.com/user-attachments/assets/18f25509-86f2-4fe4-9477-130850c9b89b" />

Zielone kółko z dwójką oznacza że DAG odpalił się pomyślnie i zakończył bezbłędnie, schedule 1 day pokazuje że airflow poprawnie przyjął harmonogram trenowania modelu co dzień

Zadanie 3 : Rozszerzenie o walidację i warunkową wymianę modelu

<img width="867" height="783" alt="image" src="https://github.com/user-attachments/assets/e4fcbc51-364b-4cb1-ba55-ac03e6563b93" />

W tym zadaniu po każdym treningu zapisuje model w /models/archive z unikalnym znacznikiem czasu tstamp w nazwie pliku. Dodałem także weryfikacje w postaci porównywania dokładności nowego modelu z progiem 80 %. Jeśli model spełnia tą dokładność to automatycznie kopiuje się go do docelowego katalogu a jak nie to do archiwum

<img width="1840" height="297" alt="image" src="https://github.com/user-attachments/assets/f0189446-2bb8-45f7-baae-33726622c519" />

Po wejściu w Grid pokazuje się że task jest oznaczony jako success i w logach można zobaczyć dokładność modelu który przeszedł.

Wnioski : 

Automatyzacja protokołów Apache Airflow wyeliminowała potrzebę ręcznego uruchamiania skryptów. Zastosowanie mechanizmu walidacji warunkowej zabezpiecza środowisko produkcyjne przed wdrożeniem modeli o zbyt niskiej dokładności
