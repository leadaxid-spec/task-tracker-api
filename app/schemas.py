from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    sub: int

class TaskCreate(BaseModel):
    title:str
    description:str|None = None

class TaskResponce(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    owner_id: int

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None