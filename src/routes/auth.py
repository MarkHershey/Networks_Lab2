# authentications

from fastapi import APIRouter, Depends, HTTPException
from puts.logger import logger

from ..access_utils import Access
from ..auth import AuthHandler
from ..database import *
from ..functional import clean_dict
from ..models.user import User, UserLogin, UserLoginResponse

router = APIRouter(prefix="/api/auth", tags=["User Authentication"])
auth_handler = AuthHandler()


@router.post("/signup", status_code=201)
async def user_sign_up(new_user: User):
    search_count = users_collection.count_documents({"username": new_user.username})
    if search_count > 0:
        raise HTTPException(status_code=400, detail="Username is taken")
    new_user.password = auth_handler.get_password_hash(new_user.password)

    user_dict = dict(new_user.dict())
    try:
        # insert into database
        users_collection.insert_one(user_dict)
        logger.debug(f"New User inserted to DB: {new_user.username}")
    except Exception as e:
        logger.error(f"New User failed to be inserted to DB: {new_user.username}")
        logger.error(e)
        raise HTTPException(status_code=500, detail="Failed to insert into database")
    return "OK"


@router.post("/signin", response_model=UserLoginResponse)
async def user_sign_in(auth_details: UserLogin):
    try:
        user = users_collection.find_one({"username": auth_details.username})
    except Exception as e:
        logger.error("Failed to query user from database.")
        logger.error(e)
        raise HTTPException(status_code=500, detail="Databse Error.")

    if not user or not auth_handler.verify_password(
        auth_details.password, user["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")

    token = auth_handler.encode_token(auth_details.username)
    logger.debug(f"New JWT token generated for user: '{auth_details.username}'")

    clean_dict(user)

    return {"token": token, **user}
