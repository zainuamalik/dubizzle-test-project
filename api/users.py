# api/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from middleware.dependencies import get_db, get_current_user
from services.user import UserService, UserCreate, UserUpdate
from validators.users import UserResponse  # Pydantic response model for users

router = APIRouter(prefix="/users", tags=["users"])

# Endpoint: Create a new user (Admin only)
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    service = UserService(db)
    user = service.create_user(user_data)
    return user

# Endpoint: Retrieve user details by ID (Admin, or the user themself)
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Admin can see any user; otherwise, users can only see their own details
    if current_user.role != "admin" and current_user.id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

# Endpoint: Update user details by ID (Admin, or the user themself)
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.role != "admin" and current_user.id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_user = service.update_user(user_id, update_data)
    return updated_user

# Endpoint: Delete a user by ID (Admin only)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    service = UserService(db)
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

# Endpoint: List all users (Admin only)
@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    service = UserService(db)
    # Implement a method in your service to list all users.
    # For this example, we'll assume you add a method called list_users.
    users = service.list_users()  # Make sure this method returns a list of User objects
    return users

# Endpoint: Retrieve profile for the currently logged-in user
@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user = Depends(get_current_user)
):
    # Since get_current_user already ensures token validity,
    # simply return the current user’s info.
    return current_user

# Endpoint: Update profile for the currently logged-in user
@router.put("/me", response_model=UserResponse)
def update_my_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = UserService(db)
    updated_user = service.update_user(current_user.id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user