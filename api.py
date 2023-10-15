from fastapi import FastAPI
from jobs import Jobs

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
def create_job(job: Job):
    jobs.append(job.dict())
    return job

@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    job = next((job for job in jobs if job["job_id"] == job_id), None)
    if job:
        return job
    else:
        return {"message": "Job not found"}
