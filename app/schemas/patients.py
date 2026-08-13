from pydantic import BaseModel, ConfigDict, EmailStr


class PatientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str


class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: str
