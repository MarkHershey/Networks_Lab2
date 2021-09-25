# purchase records

from fastapi import APIRouter, Depends, HTTPException
from markkk.logger import logger
from pymongo import ReturnDocument

from ..auth import AuthHandler
from ..database import *
from ..error_msg import ErrorMsg as MSG
from ..functional import clean_dict
from ..models.record import Record
from ..models.user import UserData

router = APIRouter(prefix="/api/records", tags=["Purchase Record"])
auth_handler = AuthHandler()


@router.post("/new", status_code=201)
async def create_new_record(
    new_record: Record, username=Depends(auth_handler.auth_wrapper)
):
    # TODO: user validation
    logger.debug(f"User({username}) creating a new record")

    record_dict = dict(new_record.dict())

    try:
        user_data_dict: dict = user_data_collection.find_one({"username": username})
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    if not user_data_dict:
        user_data_dict = dict(UserData(username=username).dict())
        try:
            user_data_dict.insert_one(user_data_dict)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=500, detail="Failed to insert into database"
            )

    try:
        _updated = user_data_collection.find_one_and_update(
            filter={"username": username},
            update={"$push": {"records": record_dict}},
            return_document=ReturnDocument.AFTER,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Failed to insert into database")
    return
