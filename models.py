from sqlalchemy import Column, Integer, String, create_table
from database import metadata

departments = create_table(
    "departments",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("department_name", String),
)

jobs = create_table(
    "jobs",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("job_name", String),
)

employees = create_table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String),
    Column("department_id", Integer),
    Column("job_id", Integer),
)
