from fastapi import FastAPI
from sqlalchemy.orm import Session
from database.database import engine, SessionLocal
from database.models.base import Base
from database.models.users import User
from services.user import UserService, UserCreate
from api import auth, users, orders
from contextlib import asynccontextmanager


# Seed function to ensure an admin user exists.
def seed_admin_user():
    db: Session = SessionLocal()
    try:
        user_service = UserService(db)
        existing_admin = db.query(User).filter_by(username="admin").first()
        if not existing_admin:
            admin_data = UserCreate(
                username="admin",
                email="admin@example.com",
                password="AdminPass123",
                role="admin"
            )
            user_service.create_user(admin_data)
            print("Admin user seeded.")
        else:
            print("Admin user already exists.")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    seed_admin_user()
    yield


app = FastAPI(title="User and Order Management API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {"message": "Welcome to the API"}