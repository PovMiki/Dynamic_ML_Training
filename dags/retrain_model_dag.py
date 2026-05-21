from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator


def retrain_model():
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import joblib
    import datetime as dt

    #wczytanie
    df = pd.read_csv("data/new_data.csv")
    X = df.drop("target", axis=1)
    y = df["target"]

    #trenowanie
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X, y)

    #zapis z wersjonowaniem
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"data/rf_model_{timestamp}.pkl"
    joblib.dump(clf, model_path)

    #walidacja
    print(f"sciezka : {model_path} dokladnosc : {clf.score(X, y) * 100}%")


#DAG co 1 dzien
with DAG(
        dag_id="DAG2",
        start_date=datetime(2026, 1, 1),
        catchup=False,
        schedule_interval=timedelta(days=1)
) as dag:
    task_retrain = PythonVirtualenvOperator(
        task_id="DAG2_task",
        python_callable=retrain_model,
        requirements=['pandas', 'scikit-learn', 'joblib']
    )