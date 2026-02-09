import json
import os 
import pendulum
from airflow.providers.standard.operators.python import PythonOperator, PythonVirtualenvOperator

from airflow import DAG
from airflow.sdk import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook


POSTGRES_CONN_ID = "postgres_storage"

def twelvedata_api_key() -> str:
    return Variable.get("TWELVEDATA_API_KEY")

def get_data_venv(twd_api_key, logical_date: str) -> dict:
    from twelvedata import TDClient
    import pendulum

    date = pendulum.parse(logical_date)

    td = TDClient(apikey=twd_api_key)
    ts = td.exchange_rate(symbol="USD/EUR", date=date.isoformat())
    return ts.as_json()


def save_data(data: dict) -> None:
    print("Saving the data")

    if not data:
        raise ValueError("No data received")

    symbol = data["symbol"]
    rate = float(data["rate"])

    pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    pg_hook.run(
        """
        INSERT INTO exchange_rates (symbol, rate)
        VALUES (%s, %s)
        """,
        parameters=(symbol, rate),
    )

with DAG(
    dag_id="connections_and_variables",
    schedule="@daily",
    catchup=True,
    start_date=pendulum.datetime(2026, 2, 5, tz="UTC"),
    tags=["exercise_5"],
) as dag:

    get_api_key_op = PythonOperator(
        task_id="get_api_key",
        python_callable=twelvedata_api_key,
    )

    get_data_op = PythonVirtualenvOperator(
        task_id="get_data",
        python_callable=get_data_venv,
        requirements=["twelvedata", "pendulum", "lazy_object_proxy", "cloudpickle"],
        serializer="cloudpickle",
        op_kwargs={
            "twd_api_key": get_api_key_op.output,
            "logical_date": "{{ logical_date }}",
        },
    )


    save_data_op = PythonOperator(
        task_id="save_data",
        python_callable=save_data,
        op_kwargs={"data": get_data_op.output},
    )

    get_api_key_op >> get_data_op >> save_data_op
