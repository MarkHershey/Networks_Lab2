# purchase records
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Union

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from puts.logger import logger
from puts.time import timestamp_seconds
from pymongo import ReturnDocument

from ..auth import AuthHandler
from ..database import *
from ..db_helpers import check_and_insert_one_record, query_records
from ..error_msg import ErrorMsg as MSG
from ..functional import clean_dict, json_serial, remove_none_value_keys
from ..models.record import Record, RecordEdit
from ..models.user import UserData
from ..statement_parser import get_records_from_csv

router = APIRouter(prefix="/api/records", tags=["Records"])
auth_handler = AuthHandler()

SRC_ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SRC_ROOT_DIR / "local_db"
FILE_DIR = DATA_DIR / "user_files"

##########################


def save_user_file_to_local(file: UploadFile, username: str, save_name: str) -> Path:
    # ref: https://stackoverflow.com/a/63581187

    user_dir: Path = FILE_DIR / username

    if not user_dir.is_dir():
        os.makedirs(user_dir)

    destination: Path = user_dir / save_name
    try:
        with destination.open(mode="wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            buffer.close()
            return destination
    except Exception as e:
        logger.error(e)
        logger.exception(e)
        return None
    finally:
        file.file.close()


def save_json_to_local(
    json_data: Union[dict, list], username: str, save_name: str
) -> Path:

    user_dir: Path = FILE_DIR / username

    if not user_dir.is_dir():
        os.makedirs(user_dir)

    destination: Path = user_dir / save_name
    try:
        with destination.open(mode="w") as f:
            json.dump(json_data, f, indent=4, default=json_serial)
        return destination
    except Exception as e:
        logger.error(e)
        logger.exception(e)
        return None


##########################


@router.post("/", status_code=201)
async def create_record(
    new_record: Record, username=Depends(auth_handler.auth_wrapper)
):
    logger.debug(f"User({username}) creating a new record")
    updated_user_data = check_and_insert_one_record(new_record, username)
    return updated_user_data


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
    logger.debug(f"User({username}) fetching records")

    q_results: List[dict] = query_records(
        username=username,
        start_time=start_time,
        end_time=end_time,
        tag=tag,
        offset=offset,
        count=count,
        sort_by=sort_by,
        reverse=reverse,
    )

    return q_results


@router.get("/{uid}", response_model=Record)
async def get_single_record(uid: str, username=Depends(auth_handler.auth_wrapper)):
    logger.debug(f"User({username}) getting a record")
    try:
        record_dict: dict = records_collection.find_one(
            filter={"username": username, "uid": uid}
        )
        clean_dict(record_dict)
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    if not record_dict:
        logger.error(MSG.ITEM_NOT_FOUND)
        raise HTTPException(status_code=404, detail=MSG.ITEM_NOT_FOUND)

    return record_dict


@router.put("/{uid}", response_model=Record)
async def update_single_record(
    uid: str, record: RecordEdit, username=Depends(auth_handler.auth_wrapper)
):
    logger.debug(f"User({username}) updating a record")
    record_dict = dict(record.dict())
    remove_none_value_keys(record_dict)

    try:
        _updated = records_collection.find_one_and_update(
            filter={"username": username, "uid": uid},
            update={"$set": record_dict},
            return_document=ReturnDocument.AFTER,
        )
    except Exception as e:
        logger.error(MSG.DB_UPDATE_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_UPDATE_ERROR)

    if not _updated:
        logger.error(MSG.ITEM_NOT_FOUND)
        raise HTTPException(status_code=404, detail=MSG.ITEM_NOT_FOUND)

    return _updated


@router.delete("/{uid}")
async def delete_single_record(uid: str, username=Depends(auth_handler.auth_wrapper)):
    logger.debug(f"User({username}) deleting a record")
    try:
        _delete_result = records_collection.delete_one(
            filter={"username": username, "uid": uid}
        )
    except Exception as e:
        logger.error(MSG.DB_UPDATE_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_UPDATE_ERROR)

    if _delete_result.deleted_count != 1:
        logger.error(MSG.ITEM_NOT_FOUND)
        raise HTTPException(status_code=404, detail=MSG.ITEM_NOT_FOUND)

    return


@router.post("/import", status_code=201)
async def import_records_from_dbs(
    file: UploadFile = File(...), username=Depends(auth_handler.auth_wrapper)
):
    logger.debug(f"User({username}) creating a new record")

    if not str(file.filename).endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid File Format.")

    # Save file to local
    save_name = f"{username}_{timestamp_seconds()}.csv"
    saved_fp: Path = save_user_file_to_local(
        file=file, username=username, save_name=save_name
    )
    if not saved_fp:
        raise HTTPException(status_code=500, detail="Server failed to save the file.")

    data: dict = get_records_from_csv(filepath=saved_fp, username=username, debug=False)

    insertions_count: int = data.get("insertions_count", 0)
    logger.debug(f"{insertions_count} new records imported.")

    return data


@router.get("/export", response_class=FileResponse)
async def export_records_to_json(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    tag: Optional[str] = None,
    offset: int = 0,
    count: int = -1,
    sort_by: str = "transaction time",
    reverse: bool = False,
    username=Depends(auth_handler.auth_wrapper),
):
    logger.debug(f"User({username}) exporting records to json")

    q_results: List[dict] = query_records(
        username=username,
        start_time=start_time,
        end_time=end_time,
        tag=tag,
        offset=offset,
        count=count,
        sort_by=sort_by,
        reverse=reverse,
    )

    # export to json file at local
    export_name = f"{username}_export_{timestamp_seconds()}.json"
    saved_fp: Path = save_json_to_local(
        json_data=q_results, username=username, save_name=export_name
    )
    if not saved_fp:
        raise HTTPException(status_code=500, detail="Export failed.")

    # this is a file response
    return str(saved_fp)
