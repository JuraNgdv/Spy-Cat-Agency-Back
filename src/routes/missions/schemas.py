from pydantic import BaseModel
from typing import Optional, List


# ---------- Targets ----------
class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    complete: bool = False


class TargetCreate(TargetBase):
    pass


class TargetUpdateNotes(BaseModel):
    notes: str


class TargetMarkComplete(BaseModel):
    complete: bool = True


class TargetRead(TargetBase):
    id: int

    class ConfigDict:
        from_attributes = True


# ---------- Missions ----------
class MissionBase(BaseModel):
    complete: bool = False


class MissionCreate(MissionBase):
    targets: List[TargetCreate]


class MissionAssignCat(BaseModel):
    cat_id: int


class MissionRead(MissionBase):
    id: int
    cat_id: Optional[int]
    targets: List[TargetRead]

    class ConfigDict:
        from_attributes = True
