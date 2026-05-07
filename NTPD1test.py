import joblib

model = joblib.load('model_titanica.joblib')
X_test = joblib.load('dane_testowe.joblib')

przyklad = X_test.iloc[[3]]
wynik = model.predict(przyklad)

print(f"predykcja {wynik[0]}")