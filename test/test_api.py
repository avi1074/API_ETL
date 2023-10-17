from fastapi.testclient import TestClient
from api import app 

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the job API!"}

def test_get_non_existent_table_records():
    response = client.get("/nonexistenttable/")
    assert response.status_code == 400

def test_upload_jobs_csv():
    data = {
        "file": ("test.csv", "id,job\n1,Job1\n2,Job2", "text/csv")
    }
    response = client.post("/jobs/uploadcsv/", files=data)
    assert response.status_code == 200
