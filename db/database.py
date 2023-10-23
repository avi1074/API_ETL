from sqlalchemy import create_engine, MetaData
import os

user = os.environ.get("USER")
pwd = os.environ.get("PWD")
host = os.environ.get("HOST")

DATABASE_URL = f"postgresql://{user}:{pwd}@{host}:5432/apidatabase"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
