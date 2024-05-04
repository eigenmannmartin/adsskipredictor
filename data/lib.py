import os
import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def prepare():
    load_dotenv()

def get_db_connection():
    url = URL.create(
        drivername="postgresql",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
    )
    db = create_engine(url)
    conn = db.connect()
    print(f"Connected to: {url}")
    return conn


def get_mondays(start, end):
    start = start - datetime.timedelta(days=start.weekday())
    end = end - datetime.timedelta(days=end.weekday())
    current = start
    while current <= end:
        yield current
        current = current + datetime.timedelta(days=7)


def add_axis_mondays(axis, df):
    for monday in get_mondays(df.index.min(), df.index.max()):
        axis.vlines(monday, 0, 1, color='black', linestyle='--')
        axis.text(monday,0, monday.strftime('%a %Y-%m-%d') ,rotation=90)
