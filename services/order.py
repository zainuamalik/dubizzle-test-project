from sqlalchemy.orm import Session
from database.models.orders import Order
from pydantic import BaseModel


class OrderCreate(BaseModel):
    total_amount: float
    status: str = "pending"


class OrderUpdate(BaseModel):
    status: str | None = None


class OrderService:
    def __init__(self, db: Session):
        self.db = db


    def create_order(self, user_id: int, order_data: OrderCreate) -> Order:
        new_order = Order(
            user_id=user_id,
            total_amount=order_data.total_amount,
            status=order_data.status
        )
        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)
        return new_order


    def get_order(self, order_id: int) -> Order | None:
        return self.db.query(Order).filter(Order.id == order_id).first()


    def update_order(self, order_id: int, order_data: OrderUpdate) -> Order | None:
        order = self.get_order(order_id)
        if not order:
            return None
        if order_data.status is not None:
            order.status = order_data.status
        self.db.commit()
        self.db.refresh(order)
        return order


    def delete_order(self, order_id: int) -> bool:
        order = self.get_order(order_id)
        if not order:
            return False
        self.db.delete(order)
        self.db.commit()
        return True


    def list_all_orders(self) -> list[Order]:
        return self.db.query(Order).all()


    def list_orders_by_user(self, user_id: int) -> list[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).all()