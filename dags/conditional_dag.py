from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator


def retrain_and_validate():
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import joblib
    import datetime as dt

    #wczytanie
    df = pd.read_csv("/opt/airflow/dags/new_data.csv")
    X, y = df.drop("target", axis=1), df["target"]

    #trenowanie
    clf = RandomForestClassifier(random_state=42).fit(X, y)
    new_acc = clf.score(X, y) * 100

    #zapis do dags
    tstamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    arch_path = f"/opt/airflow/dags/rf_archive_{tstamp}.pkl"
    joblib.dump(clf, arch_path)

    #walidacja
    if new_acc > 80.0:
        prod_path = "/opt/airflow/dags/rf_production_active.pkl"
        joblib.dump(clf, prod_path)
        print(f"SUKCES: {new_acc}%")
    else:
        print(f"ODRZUCONY: {new_acc}%")


with DAG(
        dag_id="DAG3_logs",
        start_date=datetime(2026, 1, 1),
        catchup=False,
        schedule_interval=timedelta(days=1)
) as dag:
    task_retrain = PythonVirtualenvOperator(
        task_id="run_conditional_retrain",
        python_callable=retrain_and_validate,
        requirements=['pandas', 'scikit-learn', 'joblib']
    )