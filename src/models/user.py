from puts.logger import logger
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    name: str = None
    email: str = None
    admin: bool = False


class UserProfile(BaseModel):
    username: str = None
    name: str = None
    email: str = None
    admin: bool = False


class UserData(BaseModel):
    username: str = None
    records: list = []
    ...  # TODO: add more


class UserLoginResponse(BaseModel):
    username: str = None
    name: str = None
    email: str = None
    admin: bool = False
    token: str
