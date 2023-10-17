from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql://postgresql:globant_challenge2023@database-globant.cxxinsslhf6k.us-east-1.rds.amazonaws.com:5432/apidatabase"

engine = create_engine(DATABASE_URL)
metadata = MetaData()