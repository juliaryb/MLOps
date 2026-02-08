import datetime
import json
import os

import pendulum

from airflow.providers.standard.operators.python import PythonOperator
from dotenv import load_dotenv
from twelvedata import TDClient

from airflow import DAG

load_dotenv()


def get_data(**kwargs) -> dict:
    logical_date: pendulum.DateTime = kwargs["logical_date"]

    td = TDClient(apikey=os.environ["TWELVEDATA_API_KEY"])

    ts = td.exchange_rate(symbol="USD/EUR", date=logical_date.isoformat())
    data = ts.as_json()
    return data


def save_data(data: dict) -> None:
    print("Saving the data")

    if not data:
        raise ValueError("No data received")

    with open("data.jsonl", "a+") as file:
        file.write(json.dumps(data))
        file.write("\n")


with DAG(
        dag_id="scheduling_dataset_gathering",
        schedule="@daily",
        catchup=True,
        start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
) as dag:
    get_data_op = PythonOperator(task_id="get_data", python_callable=get_data)
    save_data_op = PythonOperator(
        task_id="save_data",
        python_callable=save_data,
        op_kwargs={"data": get_data_op.output},
    )

    get_data_op >> save_data_op
