from pydantic import BaseModel

class Jobs(BaseModel):
    id: int
    job: str