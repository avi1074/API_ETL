from pydantic import BaseModel

class Deparments(BaseModel):
    id: int
    deparment: str