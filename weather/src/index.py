import os
import sentry_sdk
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import date, datetime, timedelta

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    enable_tracing=True,
    traces_sample_rate=float(os.environ.get("SENTRY_TRACES_RATE", "0.0")),
    profiles_sample_rate=float(os.environ.get("SENTRY_PROFILE_RATE", "0.0")),
)


def request_openmeteo(openmeteo, url, location, out_path):
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "start_date": "2024-02-01",
        "end_date": (
            date.today() - timedelta(days=2)
        ).isoformat(),  # Archive data lacks behind
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "snowfall",
            "snow_depth",
            "cloud_cover",
            "cloud_cover_low",
            "cloud_cover_mid",
            "cloud_cover_high",
            "wind_speed_100m",
            "is_day",
            "sunshine_duration",
        ],
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_rain = hourly.Variables(3).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(4).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(5).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(6).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(7).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(8).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(9).ValuesAsNumpy()
    hourly_wind_speed_100m = hourly.Variables(10).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(11).ValuesAsNumpy()
    hourly_sunshine_duration = hourly.Variables(12).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["rain"] = hourly_rain
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["snow_depth"] = hourly_snow_depth
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
    hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
    hourly_data["is_day"] = hourly_is_day
    hourly_data["sunshine_duration"] = hourly_sunshine_duration

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    timestamp = datetime.now().isoformat()
    hourly_dataframe["fetch_timestamp"] = timestamp
    hourly_dataframe.to_csv(
        f"{out_path}/{location['short_name']}_{timestamp}.csv", index=False
    )
    print(hourly_dataframe)


def main():
    cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://archive-api.open-meteo.com/v1/archive"
    locations = [
        {
            "latitude": 46.819325,
            "longitude": 10.258814,
            "name": "Stelvio Pass (Scuol)",
            "short_name": "scuol",
        },  # https://www.google.com/maps/place/Schlivera,+Scuol/@46.8195214,10.2588071,128m/data=!3m1!1e3!4m6!3m5!1s0x478346343f61717d:0xef66791334d034b3!8m2!3d46.815091!4d10.2665439!16s%2Fg%2F11bzv1rrvq?entry=ttu
        {
            "latitude": 46.97897139041747,
            "longitude": 9.416916286976036,
            "name": "Pizolhütte",
            "short_name": "pizol",
        },  # https://www.google.com/maps/place/Pizolh%C3%BCtte/@46.9793703,9.4178282,1023m/data=!3m1!1e3!4m7!3m6!1s0x4784cd6db60c63fb:0x4ac25fa3c12e589a!4b1!8m2!3d46.9788909!4d9.4173669!16s%2Fg%2F1td75frm?entry=ttu
        {
            "latitude": 46.44958957767884,
            "longitude": 7.497891872389865,
            "name": "Metschstand (Adelboden)",
            "short_name": "adelboden",
        },  # https://www.google.com/maps/place/Metschstand/@46.4696774,7.4803062,16525m/data=!3m1!1e3!4m6!3m5!1s0x478efd155d5028d5:0x6e73fc9865ab421a!8m2!3d46.4449626!4d7.4952955!16s%2Fg%2F120kn5tl?entry=ttu
        {
            "latitude": 46.455283684164755,
            "longitude": 7.203307280133644,
            "name": "La Videmanette (Gstaad)",
            "short_name": "gstaad",
        },  # https://www.google.com/maps/place/La+Videmanette/@46.4549067,7.1980502,2066m/data=!3m2!1e3!4b1!4m6!3m5!1s0x478ef2636b28158d:0xad728f797d15fcb6!8m2!3d46.4549!4d7.2032!16s%2Fg%2F119pgctxg?entry=ttu
    ]
    for location in locations:
        with sentry_sdk.start_transaction(op="request", name=location["name"]):
            request_openmeteo(
                openmeteo, url, location, out_path=os.environ.get("OUT_PATH", ".")
            )


if __name__ == "__main__":
    main()
