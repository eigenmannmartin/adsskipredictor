import os
import sentry_sdk
import pandas as pd
import glob
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


url = URL.create(
    drivername="postgresql",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    host=os.environ["DB_HOST"],
    database=os.environ["DB_NAME"],
)
db = create_engine(url)
conn = db.connect()

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    enable_tracing=True,
    traces_sample_rate=float(os.environ.get("SENTRY_TRACES_RATE", "0.0")),
    profiles_sample_rate=float(os.environ.get("SENTRY_PROFILE_RATE", "0.0")),
)


def main():
    price_files = glob.glob(os.path.join(os.environ.get("PRICES_PATH", "./"), "*.csv"))
    for ind, file in enumerate(price_files):
        print(f"reading: {file}")
        df = pd.read_csv(file)
        df["scrape_file"] = os.path.basename(file)
        df["resort"] = os.path.basename(file).split("_")[0]
        df.to_sql(
            "prices",
            con=conn,
            if_exists="replace" if ind == 0 else "append",
            index=False,
        )
    print(df.describe())

    weather_files = glob.glob(
        os.path.join(os.environ.get("WEATHER_PATH", "./"), "*.csv")
    )
    latest_weather_files = sorted(weather_files, key=os.path.getctime, reverse=True)[
        :5
    ]  # get the 4 latest files
    for ind, file in enumerate(latest_weather_files):
        print(f"reading: {file}")
        df = pd.read_csv(file)
        df["request_file"] = os.path.basename(file)
        df["resort"] = os.path.basename(file).split("_")[0]
        df.to_sql(
            "weather",
            con=conn,
            if_exists="replace" if ind == 0 else "append",
            index=False,
        )
    print(df.describe())


if __name__ == "__main__":
    main()
