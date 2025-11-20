"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import timedelta

from api.database import get_db
from api.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    create_user,
    get_current_user,
)
from api.config import settings

router = APIRouter()


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    user = await create_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )
    return user


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token"""
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    await db.commit()

    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """Refresh access token"""
    from jose import JWTError, jwt

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    from api.auth import get_user_by_email
    user = await get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    # Create new tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    """Get current user"""
    return current_user


@router.get("/garmin/authorize")
async def garmin_authorize(current_user = Depends(get_current_user)):
    """Initiate Garmin OAuth flow"""
    # Build OAuth URL
    auth_url = (
        f"https://connect.garmin.com/oauthConfirm?"
        f"oauth_callback={settings.GARMIN_REDIRECT_URI}&"
        f"oauth_consumer_key={settings.GARMIN_CLIENT_ID}"
    )

    return {"authorization_url": auth_url}


@router.get("/garmin/callback")
async def garmin_callback(
    code: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Handle Garmin OAuth callback"""
    # TODO: Exchange code for access token
    # TODO: Store tokens in data_source_auth table
    return {"status": "success", "message": "Garmin connected successfully"}


@router.get("/oura/authorize")
async def oura_authorize(current_user = Depends(get_current_user)):
    """Initiate Oura OAuth flow"""
    auth_url = (
        f"https://cloud.ouraring.com/oauth/authorize?"
        f"client_id={settings.OURA_CLIENT_ID}&"
        f"redirect_uri={settings.OURA_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=daily"
    )

    return {"authorization_url": auth_url}


@router.get("/oura/callback")
async def oura_callback(
    code: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Handle Oura OAuth callback"""
    # TODO: Exchange code for access token
    # TODO: Store tokens in data_source_auth table
    return {"status": "success", "message": "Oura connected successfully"}


@router.get("/strava/authorize")
async def strava_authorize(current_user = Depends(get_current_user)):
    """Initiate Strava OAuth flow"""
    auth_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={settings.STRAVA_CLIENT_ID}&"
        f"redirect_uri={settings.STRAVA_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=read,activity:read_all"
    )

    return {"authorization_url": auth_url}


@router.get("/strava/callback")
async def strava_callback(
    code: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Handle Strava OAuth callback"""
    # TODO: Exchange code for access token
    # TODO: Store tokens in data_source_auth table
    return {"status": "success", "message": "Strava connected successfully"}
