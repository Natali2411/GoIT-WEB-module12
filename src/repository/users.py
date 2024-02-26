from typing import Type

from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from libgravatar import Gravatar
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


def get_current_user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> \
        Type[User]:
    Authorize.jwt_required()

    current_user = db.query(User).filter(
        User.email == Authorize.get_jwt_subject()).first()
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid user credentials")

    return current_user
