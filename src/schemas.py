from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field, PastDate


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
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
