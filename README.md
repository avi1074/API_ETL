# API_ETL

A simple FastAPI application to upload CSV files and save them into a PostgreSQL database. The application supports uploading details about jobs, employees, and departments.

# Features
CSV Upload: Upload .csv files to be parsed and saved to the PostgreSQL database.
View Jobs: List all the jobs that have been added.
Add Job: Manually add a new job through the API.
Retrieve Job by ID: Fetch details of a specific job by its ID.

# Requirements
Python 3.6+
FastAPI
SQLAlchemy
Pandas
PostgreSQL

# Installation

# API Endpoints

API Endpoints
GET /: Welcome endpoint.
GET /jobs/: Retrieve all jobs.
POST /jobs/: Manually add a new job.
GET /jobs/{job_id}: Retrieve a job by its ID.
POST /jobs/uploadcsv/: Upload a CSV file containing job data.
POST /employees/uploadcsv/: Upload a CSV file containing employee data.
POST /departments/uploadcsv/: Upload a CSV file containing department data.


# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.