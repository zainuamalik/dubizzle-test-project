# services/user.py
from sqlalchemy.orm import Session
from database.models.users import User
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

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user_id: int, update_data: UserUpdate) -> User | None:
        user = self.get_user(user_id)
        if not user:
            return None
        if update_data.username is not None:
            user.username = update_data.username
        if update_data.email is not None:
            user.email = update_data.email
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    # NEW: List all users (Admin only)
    def list_users(self) -> list[User]:
        return self.db.query(User).all()