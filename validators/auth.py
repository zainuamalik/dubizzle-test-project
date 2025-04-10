from pydantic import BaseModel, EmailStr


# Validation schema for authentication/authorization data
class TokenData(BaseModel):
    sub: str  # user ID
    role: str # role ID


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class Login(BaseModel):
    username: str
    password: str