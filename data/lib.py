import os
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