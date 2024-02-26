from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel, Field, PastDate, EmailStr, validator, StrictStr


class ChannelModel(BaseModel):
    name: str = Field(max_length=50)


class ChannelResponse(ChannelModel):
    id: int

    class Config:
        orm_mode = True


class ContactChannelModel(BaseModel):
    contact_id: int
    channel_id: int
    channel_value: str


class ContactChannelResponse(ContactChannelModel):
    created_by: int
    id: int

    class Config:
        orm_mode = True


class ContactModel(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    birthdate: PastDate
    gender: str = Field(max_length=1, examples=["F", "M"])
    persuasion: str = Field(max_length=50)
    created_at: datetime


class ContactResponse(ContactModel):
    created_by: int
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str = Field(min_length=5)
    refresh_token: str = Field(min_length=5)
    token_type: str = "bearer"


class Settings(BaseModel):
    authjwt_secret_key: str = Field(min_length=5,
                                    default='kajsbdkhagsd123hfj123y5467123')
    authjwt_algorithm: Optional[StrictStr] = "HS256"
    authjwt_token_location: Optional[Sequence[StrictStr]] = {'headers'}
