import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from evidently.presets import DataDriftPreset
from evidently import Report
from evidently.presets import ClassificationPreset
from evidently import DataDefinition
from evidently.core.datasets import BinaryClassification
from evidently.core.datasets import Dataset

X_train, y_train = make_classification(n_samples=500, n_features=5, random_state=42)
df_train = pd.DataFrame(X_train, columns=[f"feature_{i}" for i in range(5)])
df_train["target"] = y_train

X_prod, y_prod = make_classification(n_samples=300, n_features=5, random_state=999)
df_prod = pd.DataFrame(X_prod, columns=[f"feature_{i}" for i in range(5)])
df_prod["target"] = y_prod

model = RandomForestClassifier(random_state=42)
model.fit(df_train.drop("target", axis=1), df_train["target"])


df_prod["prediction"] = model.predict(df_prod.drop("target", axis=1))

print("ZBIOR TRENINGOWY")
print(f"wiersze :  {df_train.shape}")
print(f"\ntypy kolumn : {df_train.info()}")

print("ZBIOR PRODUKCYJNY")
print(f"wiersze : : {df_prod.shape}")
print(f"\ntypy kolumn: {df_prod.info()}")

#wykrywanie driftu danych z Evidently

df_prod_features = df_prod.drop(columns=['prediction'], errors='ignore')

data_drift_report = Report(metrics=[
    DataDriftPreset()
])

snapshot = data_drift_report.run(reference_data=df_train, current_data=df_prod_features)

snapshot.save_html("data_drift_report.html")

#analiza jakosci

data_def = DataDefinition(
    classification=[
        BinaryClassification(
            target="target",
            prediction_labels="prediction"
        )
    ]
)

df_train_with_preds = df_train.copy()
df_train_with_preds["prediction"] = model.predict(df_train.drop("target", axis=1))

reference_dataset = Dataset.from_pandas(df_train_with_preds, data_def)
current_dataset = Dataset.from_pandas(df_prod, data_def)

performance_report = Report(metrics=[ClassificationPreset()])

snapshot_p = performance_report.run(reference_dataset, current_dataset)
snapshot_p.save_html("performance_report.html")
