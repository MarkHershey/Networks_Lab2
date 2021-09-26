from datetime import datetime
from typing import List, Optional, Tuple

from markkk.logger import logger
from pydantic import BaseModel, validator

from ..functional import uid_gen


class Record(BaseModel):
    uid: Optional[str] = None  # imply time of record creation
    date_time: Optional[datetime] = None  # time of purchase
    amount: float  # debit amount or credit amount
    amount_abs: Optional[float] = None  # absolute amount >= 0
    merchant: Optional[str] = None  # seller
    category: Optional[str] = None
    subcategory: Optional[str] = None
    location: Optional[str] = None  # geographic location of the transaction
    link: Optional[str] = None  # online product link
    tags: List[str] = []  # user-defined tags
    reference: Optional[str] = None  # reference number from the receipt / bank record
    remarks: Optional[str] = None
    star_flag: bool = False  # init to false
    confirmed_flag: bool = False  # init to false if record is auto generated
    exclude_flag: bool = False  # init to false

    @validator("uid", pre=True, always=True)
    def default_uid(cls, v):
        return v or uid_gen("R")

    @validator("date_time", pre=True, always=True)
    def default_date_time(cls, v):
        return v or datetime.now()

    @validator("amount_abs", pre=True, always=True)
    def absolute_amount(cls, v, *, values, **kwargs):
        return v or abs(values["amount"])
