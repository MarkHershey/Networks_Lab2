from markkk.logger import logger
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    name: str = None
    email: str = None
    admin: bool = False


class UserLoginResponse(BaseModel):
    username: str = None
    name: str = None
    email: str = None
    admin: bool = False
    token: str
