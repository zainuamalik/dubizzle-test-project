from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database.models import User
from middleware.dependencies import get_db
from security import verify_token
from services.auth import AuthService
from config.settings import settings
from validators.auth import RefreshTokenRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# Endpoint: Create access token
@router.post("/")
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    try:
        user = auth_service.authenticate_user(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    access_token = auth_service.create_access_token(
        user,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = auth_service.create_refresh_token(
        user,
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# Endpoint: Create refresh token
@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
        refresh_data: RefreshTokenRequest,
        db: Session = Depends(get_db)
):
    # Verify the refresh token
    payload = verify_token(refresh_data.refresh_token, is_refresh=True)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # Query the user from the database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    auth_service = AuthService(db)
    # Create new tokens for the user
    new_access_token = auth_service.create_access_token(user)
    new_refresh_token = auth_service.create_refresh_token(user)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }