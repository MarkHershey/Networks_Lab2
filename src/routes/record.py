# purchase records

from datetime import datetime
from typing import List, Optional, Tuple

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


@router.get("/", response_model=List[Record])
async def get_records(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    tag: Optional[str] = None,
    offset: int = 0,
    count: int = -1,
    sort_by: str = "transaction time",
    reverse: bool = False,
    username=Depends(auth_handler.auth_wrapper),
):
    # TODO: user validation
    logger.debug(f"User({username}) fetching records")

    # record_dict = dict(new_record.dict())

    sort_by_mapping = {
        "record time": "uid",
        "transaction time": "date_time",
        "amount": "amount",
        "absolute amount": "amount",
        "merchant": "merchant",
        "category": "category",
        "subcategory": "subcategory",
    }

    sort_key: str = sort_by_mapping.get(sort_by, "date_time")
    offset = 0 if not isinstance(offset, int) or offset < 0 else offset
    if count == 0:
        return []

    try:
        user_data_dict: dict = user_data_collection.find_one({"username": username})
        clean_dict(user_data_dict)
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    if not user_data_dict:
        raise HTTPException(status_code=404, detail=MSG.DB_QUERY_ERROR)

    user_records: List[dict] = user_data_dict.get("records")
    q_results: List[dict] = []

    if start_time or end_time or tag:
        start_time = datetime(1970, 1, 1) if not start_time else start_time
        end_time = datetime.now() if not end_time else end_time
        filter_tag = False if tag is None else True

        for r in user_records:
            _transaction_time: datetime = r.get("date_time")
            if start_time <= _transaction_time <= end_time:
                if filter_tag and tag in r.get("tags", []):
                    q_results.append(r)

    q_results = list(sorted(q_results, key=lambda x: x[sort_key], reverse=reverse))

    if offset and offset < len(q_results):
        q_results = q_results[offset:]

    if count > 0:
        q_results = q_results[:count]

    return q_results


@router.post("/", status_code=201)
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
