from pydantic import BaseModel


class Employee(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int