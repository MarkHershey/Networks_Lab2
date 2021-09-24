from fastapi import HTTPException
from markkk.logger import logger

from .database import admins_collection
from .error_msg import ErrorMsg as MSG


class Access:
    """
    Access Permission Levels:
    """

    @staticmethod
    def is_admin(username: str) -> bool:
        try:
            admin_info: dict = admins_collection.find_one({"username": username})
        except Exception as e:
            logger.error(MSG.DB_QUERY_ERROR)
            logger.error(e)
            raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)
        if admin_info:
            return True
        return False
