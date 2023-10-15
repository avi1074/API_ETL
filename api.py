from fastapi import FastAPI, UploadFile, HTTPException
from jobs import Jobs
from io import StringIO
import pandas as pd

app = FastAPI()

# Dummy database
jobs = []



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

@app.post("/uploadcsv/")
async def upload_csv(file: UploadFile = None):
    if file and file.filename.endswith('.csv'):
        # Read the file content
        content = await file.read()
        
        # Convert the content to a pandas dataframe
        try:
            df = pd.read_csv(StringIO(content.decode('utf-8')))
            # Here you can do any operation with the dataframe, e.g., save to a database
            return {"message": f"File '{file.filename}' uploaded successfully!", "data": df.to_dict()}
        
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to parse CSV file.")
    
    else:
        raise HTTPException(status_code=400, detail="Invalid file or file type. Only .csv files are supported.")
