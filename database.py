from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql://username:password@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL)
metadata = MetaData()