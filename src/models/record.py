from datetime import datetime
from typing import List, Optional, Tuple

from puts.logger import logger
from pydantic import BaseModel, validator

from ..functional import uid_gen


class Record(BaseModel):
    uid: Optional[str] = None  # imply time of record creation
    username: Optional[str] = None
    date_time: Optional[datetime] = None  # time of purchase
    account_id: Optional[str] = None  # account
    amount: float = None  # debit amount or credit amount
    amount_abs: Optional[float] = None  # absolute amount >= 0
    merchant: Optional[str] = None  # seller
    label: Optional[str] = None  # seller label
    bank_ref_code: Optional[str] = None  # bank ref code
    category: Optional[str] = None
    subcategory: Optional[str] = None
    location: Optional[str] = None  # geographic location of the transaction
    link: Optional[str] = None  # online product link
    tags: List[str] = []  # user-defined tags
    reference: Optional[str] = None  # reference number from the receipt / bank record
    remarks: Optional[str] = None
    imported: bool = False
    starred: bool = False  # init to false
    confirmed: bool = False  # init to false if record is auto generated
    excluded: bool = False  # init to false, excluded from amount total computation
    archived: bool = False  # init to false

    @validator("uid", pre=True, always=True)
    def default_uid(cls, v):
        return v or uid_gen("R")

    @validator("date_time", pre=True, always=True)
    def default_date_time(cls, v):
        return v or datetime.now()

    @validator("amount_abs", pre=True, always=True)
    def absolute_amount(cls, v, *, values, **kwargs):
        return v or abs(values["amount"]) if values["amount"] else None


class RecordEdit(BaseModel):
    date_time: Optional[datetime] = None
    account_id: Optional[str] = None
    amount: Optional[float] = None
    amount_abs: Optional[float] = None
    merchant: Optional[str] = None
    label: Optional[str] = None
    bank_ref_code: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    location: Optional[str] = None
    link: Optional[str] = None
    tags: Optional[List[str]] = None
    reference: Optional[str] = None
    remarks: Optional[str] = None
    imported: Optional[bool] = None
    starred: Optional[bool] = None
    confirmed: Optional[bool] = None
    excluded: Optional[bool] = None
    archived: Optional[bool] = None


class RecordsQueryResponse(BaseModel):
    query_time: datetime = None
    count: int
    username: str
    date_range_start: datetime
    date_range_end: datetime
    total_amount = float
    sorted_by: str
    records: List[Record]

    @validator("query_time", pre=True, always=True)
    def default_query_time(cls, v):
        return v or datetime.now()
