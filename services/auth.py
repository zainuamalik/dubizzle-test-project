from datetime import timedelta, datetime, timezone
from jose import jwt
from sqlalchemy.orm import Session
from database.models.users import User
from config.settings import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db


    def authenticate_user(self, username: str, password: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise ValueError("User not found")
        if not pwd_context.verify(password, user.hashed_password):
            raise ValueError("Incorrect password")
        return user


    def create_access_token(self, user: User, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
        to_encode = {"sub": str(user.id), "role": user.role}
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt


    def create_refresh_token(self, user: User, expires_delta: timedelta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)) -> str:
        to_encode = {"sub": str(user.id), "role": user.role}
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt