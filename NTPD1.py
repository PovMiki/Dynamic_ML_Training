import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import pandas as pd

df = sns.load_dataset("titanic")
print(f'pierwsze wiersze \n{df.head()}')
print(f'rozmiar {df.shape}')
print(f'typy kolumn \n{df.dtypes}')

df_pandas_encoded = pd.get_dummies(df, columns=['class', 'deck', 'sex', 'embarked', 'who', 'embark_town', 'alive'], drop_first=True)
df_encoded = df_pandas_encoded.astype(float)
df_encoded['age']= df_encoded['age'].fillna(df_encoded['age'].mean())
#print(df_encoded.isnull().sum())

X = df_encoded.drop(['survived', 'alive_yes'], axis=1)
Y = df_encoded['survived']

#trenowanie
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# zobaczenie metryk
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))

# zapis
joblib.dump(model, 'model_titanica.joblib')
joblib.dump(X_test, 'dane_testowe.joblib')
