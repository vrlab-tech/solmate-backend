from datetime import datetime
from typing import List
from pydantic import BaseModel


class UserInfoBase(BaseModel):
    username: str


class UserCreate(UserInfoBase):
    fullname: str
    password: str


class UserAuthenticate(UserInfoBase):
    password: str


class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class BlogBase(BaseModel):
    title: str
    content: str


class Blog(BlogBase):
    id: int

    class Config:
        orm_mode = True


class Wedding(BaseModel):
    bride_firstname: str
    bride_lastname: str
    groom_firstname: str
    groom_lastname: str
    datetime: datetime
    location: str
    bestman_firstname: str
    bestman_lastname: str
    maidofhonor_firstname: str
    maidofhonor_lastname: str







