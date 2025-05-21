from pydantic import BaseModel, condecimal


class SpyCatBase(BaseModel):
    name: str
    experience: int
    breed: str


class SpyCatCreate(SpyCatBase):
    salary: condecimal(gt=0, decimal_places=2)


class SpyCatUpdateSalary(BaseModel):
    salary: condecimal(gt=0, decimal_places=2)


class SpyCatRead(SpyCatBase):
    id: int
    salary: condecimal(gt=0, decimal_places=2)

    class ConfigDict:
        from_attributes = True
