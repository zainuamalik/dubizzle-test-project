from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from config.settings import OrderStatus
from database.models.base import Base
from sqlalchemy import Enum as SQLEnum

# Data model for Orders table
class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_date = Column(TIMESTAMP, server_default=func.now())
    total_amount = Column(DECIMAL, nullable=False, default=0.0)
    status = Column(SQLEnum(OrderStatus, name="order_status"), nullable=False, default=OrderStatus.pending)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())