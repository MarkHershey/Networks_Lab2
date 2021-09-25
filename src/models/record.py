from datetime import datetime
from typing import List, Optional, Tuple

from markkk.logger import logger
from pydantic import BaseModel


class Record(BaseModel):
    uid: str = None  # imply time of record creation
    date_time: datetime  # time of purchase
    amount: float  # debit amount or credit amount
    merchant: str = None  # seller
    category: str = None
    subcategory: str = None
    location: str = None  # geographic location of the transaction
    link: Optional[str] = None  # online product link
    tags: List[str] = []  # user-defined tags
    reference: Optional[str] = None  # reference number from the receipt / bank record
    remarks: Optional[str] = None
    star_flag: bool = False  # init to false
    confirmed_flag: bool = False  # init to false if record is auto generated
    exclude_flag: bool = False  # init to false
