import locale
import os
import sentry_sdk
import pandas as pd
import glob
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
  

url = URL.create(
    drivername="postgresql",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    host=os.environ["INSTANCE_UNIX_SOCKET"],
    database=os.environ["DB_NAME"]
)
db = create_engine(url)
conn = db.connect()

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    traces_sample_rate=float(os.environ.get("SENTRY_TRACES_RATE", "0.0")),
    profiles_sample_rate=float(os.environ.get("SENTRY_PROFILE_RATE", "0.0")),
)


def main():
    data_files = glob.glob(os.path.join(os.environ.get("OUT_PATH", "./") , "*.csv"))
    df = pd.DataFrame([], columns=["date", "price", "fetch_timestamp", "scrape_file"]).dropna(axis=1, how="all")
    for file in data_files:
        df_file = pd.read_csv(file)
        df_file['scrape_file'] = os.path.basename(file)
        df_file['resort'] = os.path.basename(file).split("_")[0]
        df = pd.concat([df, df_file])
    
    df.to_sql('data', con=conn, if_exists='replace', index=False)
    print(df.describe())
    


if __name__ == "__main__":
    main()
