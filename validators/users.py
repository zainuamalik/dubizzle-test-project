from pydantic import BaseModel


# Pydantic schemas for user operations
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "customer"


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str


    class Config:
        orm_mode = True