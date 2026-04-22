from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user, get_current_user, get_db
from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.db.models import User
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse

router = APIRouter()

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"],
    summary="Register a new user",
    responses={
        201: {
            "description": "User created successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "role": "user",
                    }
                }
            },
        },
        400: {
            "description": "Username or email already exists.",
            "content": {
                "application/json": {
                    "example": {"detail": "Username is already taken."}
                }
            },
        },
    },
)
def register_user(payload: UserCreate, db: DBSession) -> User:
    normalized_email = payload.email.lower()
    existing_user = db.execute(
        select(User).where(
            or_(User.username == payload.username, User.email == normalized_email)
        )
    ).scalar_one_or_none()

    if existing_user:
        if existing_user.username == payload.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    is_first_user = db.execute(select(User.id).limit(1)).first() is None
    user = User(
        username=payload.username,
        email=normalized_email,
        password=get_password_hash(payload.password),
        role="admin" if is_first_user else "user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/auth/login",
    response_model=Token,
    tags=["Auth"],
    summary="Authenticate a user and return a JWT token",
    responses={
        200: {
            "description": "Token issued successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        401: {
            "description": "Invalid login credentials.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid email or password."}
                }
            },
        },
    },
)
def login_user(payload: UserLogin, db: DBSession) -> Token:
    user = db.execute(
        select(User).where(User.email == payload.email.lower())
    ).scalar_one_or_none()

    if user is None or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        subject=user.id,
        role=user.role,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserResponse,
    tags=["Auth"],
    summary="Get the current logged-in user",
    responses={
        200: {
            "description": "Current authenticated user.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "role": "user",
                    }
                }
            },
        },
        401: {
            "description": "Missing, expired, or invalid token.",
            "content": {
                "application/json": {
                    "examples": {
                        "missing": {
                            "summary": "Missing token",
                            "value": {"detail": "Not authenticated."},
                        },
                        "expired": {
                            "summary": "Expired token",
                            "value": {"detail": "Invalid token."},
                        },
                    }
                }
            },
        },
    },
)
def read_current_user(current_user: CurrentUser) -> User:
    return current_user


@router.get(
    "/users",
    response_model=list[UserResponse],
    tags=["Users"],
    summary="List all users",
    responses={
        200: {
            "description": "List of all registered users.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "username": "admin_user",
                            "email": "admin@example.com",
                            "role": "admin",
                        },
                        {
                            "id": 2,
                            "username": "john_doe",
                            "email": "john@example.com",
                            "role": "user",
                        },
                    ]
                }
            },
        },
        403: {
            "description": "Admin access is required.",
            "content": {
                "application/json": {
                    "example": {"detail": "Admin access required."}
                }
            },
        },
        401: {
            "description": "Missing, expired, or invalid token.",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated."}
                }
            },
        },
    },
)
def list_users(
    db: DBSession,
    _: Annotated[User, Depends(get_admin_user)],
) -> list[User]:
    return list(db.execute(select(User).order_by(User.id.asc())).scalars().all())
