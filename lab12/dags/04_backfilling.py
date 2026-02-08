import datetime
import pandas as pd
import requests
import pendulum

from airflow.sdk import dag, task


@dag(
    schedule=datetime.timedelta(days=7),
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=True,
    max_active_runs=1,
    tags=["exercise_2"],
)
def weather_backfilling_taskflow():

    @task()
    def get_data(**kwargs) -> dict:
        print("Fetching data from Open-Meteo API")

        logical_date: pendulum.DateTime = kwargs["logical_date"]

        start_date = logical_date.date()
        end_date = (logical_date + datetime.timedelta(days=6)).date()

        url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 40.7143,   # New York
            "longitude": -74.0060,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "daily": ["temperature_2m_min", "temperature_2m_max"],
            "timezone": "UTC",
        }

        resp = requests.get(url, params=params)
        resp.raise_for_status()

        return resp.json()

    @task()
    def transform(data: dict, **kwargs) -> pd.DataFrame:
        daily = data["daily"]

        df = pd.DataFrame({
                "date": daily["time"],
                "temperature_min": daily["temperature_2m_min"],
                "temperature_max": daily["temperature_2m_max"],
                })

        return df

    @task()
    def save_data(df: pd.DataFrame) -> None:
        print("Saving the data")

        df.to_csv(
            "weather_2026.csv",
            mode="a",
            header=not pd.io.common.file_exists("weather_2026.csv"),
            index=False,
        )

    weather_data = get_data()
    transformed_weather_data = transform(weather_data)
    save_data(transformed_weather_data)


weather_backfilling_taskflow()
