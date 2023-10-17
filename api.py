from fastapi import FastAPI, UploadFile, HTTPException, Depends
from sqlalchemy import exc, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from io import StringIO
from database import engine
from departments import Department
from jobs import Jobs
from employees import Employee
from sql_report import employees_quarter, mean_hired 

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the job API!"}

@app.get("/{table_name}/")
async def get_table_records(table_name: str):
    return await process_get(table_name)

@app.post("/jobs/")
def create_jobs(jobs: dict):
    save_record(jobs, Jobs)

@app.post("/employees/")
def create_jobs(employees: dict):
    save_record(employees, Employee)

@app.post("/department/")
def create_jobs(department: dict):
    save_record(department, Department)

@app.get("/{table_name}/{record_id}")
def get_record(table_name: str, record_id: int):
    return find_one(table_name, record_id)

@app.post("/jobs/uploadcsv/")
async def upload_jobs_csv(file: UploadFile = None):
    return await process_csv(file, "jobs", ['id', 'job'])

@app.post("/employees/uploadcsv/")
async def upload_employees_csv(file: UploadFile = None):
    return await process_csv(file, "employees", ['id', 'name', 'datetime', 'department_id', 'job_id'])

@app.post("/departments/uploadcsv/")
async def upload_departments_csv(file: UploadFile = None):
    return await process_csv(file, "departments", ['id', 'departments'])

@app.post("/query/departments-above-mean-2021/")
async def departments_above_mean_2021():
    return await process_custom_query(mean_hired)

@app.post("/query/employees-count-2021/")
async def employees_count_2021():
    return await process_custom_query(employees_quarter)

def find_one(table_name: str, record_id: int):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    result = db.execute(text(f'SELECT * FROM {table_name} WHERE id = {record_id}'))
    row = result.fetchone()
    db.close()
    if row:
        return row._asdict()
    else:
        raise HTTPException(status_code=404, detail=f"{table_name} not found.")

def save_to_db(df: pd.DataFrame, table_name: str):
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        return True
    except exc.SQLAlchemyError:
        return False

def save_record(data: dict, model):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    new_record = model(**data)
    db.add(new_record)
    db.commit()
    db.close()

async def process_get(table_name: str):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    result = db.execute(text(f'SELECT * FROM {table_name}'))
    rows = result.fetchall()
    dict_representation = [row._asdict() for row in rows]
    db.close()
    return dict_representation

async def process_custom_query(query:str):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    result = db.execute(text(f'{query}'))
    rows = result.fetchall()
    dict_representation = [row._asdict() for row in rows]
    db.close()
    return dict_representation

async def process_csv(file: UploadFile, table_name: str, column_names: list):
    if file and file.filename.endswith('.csv'):
        content = await file.read()
        try:
            df = pd.read_csv(StringIO(content.decode('utf-8')), names=column_names)
            
            if save_to_db(df, table_name):
                return {"message": f"File '{file.filename}' uploaded successfully!", "data": df.to_dict()}
            else:
                raise HTTPException(status_code=500, detail="Failed to insert data into the database.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse CSV file. Error: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Invalid file or file type. Only .csv files are supported.")