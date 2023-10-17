from fastapi import FastAPI, UploadFile, HTTPException, Depends
import pandas as pd
from io import StringIO
from sqlalchemy.orm import sessionmaker
from database import engine
from models import departments, jobs, employees

app = FastAPI()

SessionLocal = sessionmaker(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job API!"}

@app.get("/jobs/")
def get_jobs():
    return jobs

@app.post("/jobs/")
def create_job(job: Jobs):
    jobs.append(job.dict())
    return job

@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    job = next((job for job in jobs if job["job_id"] == job_id), None)
    if job:
        return job
    else:
        return {"message": "Job not found"}


@app.post("/uploadcsv/{table_name}")
async def upload_csv(table_name: str, file: UploadFile = None):
    if table_name not in ["departments", "jobs", "employees"]:
        raise HTTPException(status_code=400, detail="Invalid table name")

    if file and file.filename.endswith('.csv'):
        content = await file.read()
        try:
            df = pd.read_csv(StringIO(content.decode('utf-8')))
            df.to_sql(table_name, engine, if_exists='append', index=False)
            return {"message": f"File '{file.filename}' uploaded successfully!", "data": df.to_dict()}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to parse CSV file.")
    else:
        raise HTTPException(status_code=400, detail="Invalid file or file type. Only .csv files are supported.")


@app.post("/batch-insert/{table_name}")
async def batch_insert(table_name: str, data: list):
    if table_name not in ["departments", "jobs", "employees"]:
        raise HTTPException(status_code=400, detail="Invalid table name")

    if not data or len(data) > 1000:
        raise HTTPException(status_code=400, detail="Data should be between 1 and 1000 rows.")

    with SessionLocal() as session:
        table = globals().get(table_name)
        session.bulk_insert_mappings(table, data)
        session.commit()
    return {"message": f"Inserted {len(data)} rows in {table_name}"}

