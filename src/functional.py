import string
from datetime import date, datetime, time
from typing import List

from puts.logger import logger
from puts.time import timestamp_microseconds


def uid_gen(prefix: str = "") -> str:
    """
    Generate an unique identifier containing an optional prefix
    and current timestamp in microseconds.
    """
    uid: str = timestamp_microseconds()
    if prefix and isinstance(prefix, str):
        return prefix.strip().upper() + "_" + uid
    else:
        return uid


def username_normalize(username: str) -> str:

    allowable_chars = string.ascii_letters + string.digits + "_"

    if not isinstance(username, str):
        return

    if len(username) < 3:
        return

    username = username.strip()

    for char in username:
        if char not in allowable_chars:
            return

    return username


def valid_password(password: str, min_length: int = 6, max_length: int = 30) -> bool:
    allowable_chars = string.ascii_letters + string.digits + string.punctuation

    if not isinstance(password, str):
        return False

    if min_length <= len(password) <= max_length:
        return False

    if password[0] in string.whitespace:
        return False

    for char in password:
        if char not in allowable_chars:
            return False

    return True


def clean_dict(data: dict) -> None:
    """
    Remove key '_id' and 'password' from dictionary if any.

    Return: None

    Exceptions: Strictly NEVER cause/raise any Exception!
    """
    if not isinstance(data, dict):
        logger.warning(f"Not a dictionary: {type(data)}")
        return

    data.pop("_id", None)
    data.pop("password", None)

    return


def remove_none_value_keys(data: dict) -> None:
    to_be_removed_keys = []
    for key, value in data.items():
        if value is None:
            to_be_removed_keys.append(key)

    for key in to_be_removed_keys:
        data.pop(key, None)

    return


def deduct_list_from_list(host_list: List[str], deduct_list: List[str]) -> None:
    for i in deduct_list:
        # make sure no duplications
        while i in host_list:
            host_list.remove(i)
    return


def convert_date_to_datetime(date_obj: date) -> datetime:
    """
    Convert a datetime.date object to a datetime.datatime object

    Return: datetime

    Exception: AssertionError
    """
    # REF: https://stackoverflow.com/a/11619200
    assert isinstance(date_obj, date), "Not a date object."
    # return the original value if the input is a datetime object
    if isinstance(date_obj, datetime):
        return date_obj
    return datetime.combine(date_obj, time())


def convert_datetime_to_date(datetime_obj: datetime) -> date:
    """
    Convert a datetime.datatime object to a datetime.date object

    Return: datetime

    Exception: AssertionError
    """
    assert isinstance(datetime_obj, datetime), "Not a datetime object."
    return datetime_obj.date()


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
