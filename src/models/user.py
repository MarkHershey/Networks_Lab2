from datetime import datetime

from puts.logger import logger
from pydantic import BaseModel, validator

from ..functional import username_normalize, valid_password


class User(BaseModel):
    created_at: datetime = None
    username: str
    password: str
    name: str = None
    email: str = None
    admin: bool = False

    @validator("created_at", pre=True, always=True)
    def default_created_at(cls, v):
        return v or datetime.now()

    @validator("username", pre=True, always=True)
    def validate_username(cls, v):
        _username = username_normalize(v)
        if not _username:
            raise ValueError(
                "username must only contain letters, numbers, and underscores with a length of at least 3 characters."
            )

        return _username

    @validator("password", pre=True, always=True)
    def validate_password(cls, v):
        if not valid_password(v):
            raise ValueError("password not allowable ")
        return v


class UserProfile(BaseModel):
    # For User Profile retrieval and update
    username: str = None
    name: str = None
    email: str = None
    admin: bool = False


class UserData(BaseModel):
    # For Database schema
    username: str = None
    records: list = []


class UserLogin(BaseModel):
    # For User Login Input
    username: str
    password: str


class UserLoginResponse(BaseModel):
    # For User Login Response
    username: str = None
    name: str = None
    email: str = None
    admin: bool = False
    token: str
