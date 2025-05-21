from pydantic import BaseModel

class UpdateNotesRequest(BaseModel):
    notes: str

class TargetOut(BaseModel):
    id: int
    name: str
    country: str
    notes: str
    complete: bool

    class ConfigDict:
        from_attributes = True
