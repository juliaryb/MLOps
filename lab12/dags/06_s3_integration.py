import pandas as pd
import requests
from airflow.sdk import dag, task, ObjectStoragePath

@dag(
    schedule=None,
    catchup=False,
    tags=["exercise_6"],
)

def weather_data_taskflow_api_6():
    @task()
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

    @task()
    def transform(data: dict) -> pd.DataFrame:
        df = pd.DataFrame(data)
        df["temperature"] = df["temperature"].clip(lower=-20, upper=50)
        return df

    @task()
    def save_data(df: pd.DataFrame, logical_date) -> None:

        base = ObjectStoragePath("s3://weather-data/", conn_id="aws_default")
        path = base / f"data_{logical_date.isoformat()}.csv"

        with path.open("w") as file:
            df.to_csv(file, index=False)

    weather_data = get_data()
    transformed_weather_data = transform(weather_data)
    save_data(transformed_weather_data)

weather_data_taskflow_api_6()
