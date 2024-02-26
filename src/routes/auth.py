from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status, Security, Header
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserModel, UserResponse, TokenModel
from src.repository import users as repository_users
from src.services.auth import get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post(
    "/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with the email {body.email} already exists"
        )
    body.password = get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    return {"user": new_user, "detail": "User successfully created"}


@router.post("/access_token", response_model=Optional[TokenModel])
def create_session(user: UserModel, Authorize: AuthJWT = Depends(),
                   db: Session = Depends(get_db)):
    user = db.query(User).filter(and_(user.email == User.email)).first()
    if user:
        access_token = Authorize.create_access_token(subject=user.email)
        refresh_token = Authorize.create_refresh_token(subject=user.email)

        user.refresh_token = refresh_token
        db.commit()
        return {'access_token': access_token, 'refresh_token': refresh_token,
                "token_type": "bearer"}

    raise HTTPException(status_code=401, detail='Invalid credentials')


@router.get("/refresh_token", response_model=TokenModel)
def refresh_token(refresh_token: str = Header(..., alias="Authorization"),
                  Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_refresh_token_required()
    # Check if refresh token is in DB
    user_email = Authorize.get_jwt_subject()
    user = db.query(User).filter(and_(user_email == User.email)).first()
    if f"Bearer {user.refresh_token}" == refresh_token:
        access_token = Authorize.create_access_token(subject=user_email)
        new_refresh_token = Authorize.create_refresh_token(subject=user_email)

        user.refresh_token = new_refresh_token
        db.commit()
        return {'access_token': access_token, 'refresh_token': new_refresh_token,
                "token_type": "bearer"}

    raise HTTPException(status_code=401, detail='Invalid or expired refresh token')
