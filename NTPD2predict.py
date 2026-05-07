import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

df = load_wine()
X = df.data
Y = df.target

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

#parametry
max_depth = 3

mlflow.set_experiment("Projekt_Wino")
with mlflow.start_run():
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    mlflow.log_param("hiperparametry", max_depth)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, artifact_path="model")

print('trening zakonczony')