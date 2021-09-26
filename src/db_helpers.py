import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from puts.logger import logger
from puts.time import timestamp_seconds
from pymongo import ReturnDocument

from .auth import AuthHandler
from .database import *
from .error_msg import ErrorMsg as MSG
from .functional import clean_dict
from .models.record import Record
from .models.user import UserData


def check_and_insert_one_record(record: Record, username: str) -> dict:
    """
    This function assumes the username given in the argument is a valid user in the system,
    and the database insertion operation is already authorised.
    """
    assert isinstance(record, Record)
    assert isinstance(username, str)
    record_dict = dict(record.dict())

    try:
        user_data_dict: dict = user_data_collection.find_one({"username": username})
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    if not user_data_dict:
        # create a empty user data object in the database
        user_data_dict = dict(UserData(username=username).dict())
        try:
            user_data_collection.insert_one(user_data_dict)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=500, detail="Failed to insert into database"
            )

    try:
        updated_user_data = user_data_collection.find_one_and_update(
            filter={"username": username},
            update={"$push": {"records": record_dict}},
            return_document=ReturnDocument.AFTER,
        )
        clean_dict(updated_user_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Failed to insert into database")

    return updated_user_data
