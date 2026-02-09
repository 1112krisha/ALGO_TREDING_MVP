"""Auth schemas."""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """User registration."""
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """User login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
