Zadanie 1 :

Zadanie 2 : 

![img_1.png](img_1.png)

Stworzyłem funkcję która wczytuje dane, następnie za pomocą klasyfikatora RandomForest model jest trenowany. Data i godzina są formatowane do timestampa co robi za wersjonowanie, ponieważ data dopisywana do treningu jest unikalna i nie nadpisze starych modeli nowa data. Za pomocą metody score obliczam dokładność dopasowania modelu co odpowiada za moją walidację. W DAG ustawiłem sztywny harmonogram wykonywania procesu co jeden dzień

![img.png](img.png)

Zielone kółko z dwójką oznacza że DAG odpalił się pomyślnie i zakończył bezbłędnie, schedule 1 day pokazuje że airflow poprawnie przyjął harmonogram trenowania modelu co dzień