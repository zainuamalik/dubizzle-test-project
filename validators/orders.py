from pydantic import BaseModel


class OrderCreate(BaseModel):
    total_amount: float
    status: str = "pending"


class OrderUpdate(BaseModel):
    status: str | None = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str

    class Config:
        orm_mode = True