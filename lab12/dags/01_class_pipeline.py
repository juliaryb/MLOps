import pandas as pd
import requests
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def get_data() -> dict:
    print("Fetching data from API")

    # New York temperature in 2025
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=40.7143&longitude=-74.006&start_date=2025-01-01&end_date=2025-12-31&hourly=temperature_2m&timezone=auto"

    resp = requests.get(url)
    resp.raise_for_status()

    data = resp.json()
    data = {
        "time": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
    }
    return data


def transform(data: dict) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["temperature"] = df["temperature"].clip(lower=-20, upper=50)
    return df


def save_data(df: pd.DataFrame) -> None:
    print("Saving the data")
    df.to_csv("data.csv", index=False)


with DAG(dag_id="weather_data_classes_api"):
    get_data_op = PythonOperator(task_id="get_data", python_callable=get_data)
    transform_op = PythonOperator(
        task_id="transform",
        python_callable=transform,
        op_kwargs={"data": get_data_op.output},
    )
    load_op = PythonOperator(
        task_id="load", python_callable=save_data, op_kwargs={"df": transform_op.output}
    )

    get_data_op >> transform_op >> load_op
