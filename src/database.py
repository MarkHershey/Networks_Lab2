import os

import pymongo
from puts.logger import logger

_DB_USER = os.environ.get("_DB_USER", "root")
_DB_PASS = os.environ.get("_DB_PASS", "example")
_DB_NAME = os.environ.get("_DB_NAME", "dev")
_DB_DOMAIN = os.environ.get("_DB_SERVICE", "localhost")
_DB_PORT = os.environ.get("_DB_PORT", 27017)

logger.debug(
    f"""-----------------------------------
            MongoDB config:
            
            Host: {_DB_DOMAIN}:{_DB_PORT}
            User: {_DB_USER}
            Database Name: {_DB_NAME}
         -----------------------------------
"""
)

client = pymongo.MongoClient(
    host=[f"{_DB_DOMAIN}:{_DB_PORT}"],
    serverSelectionTimeoutMS=10000,  # 10 second timeout
    username=str(_DB_USER),
    password=str(_DB_PASS),
)

db = client[str(_DB_NAME)]
db_available = False

try:
    # The ismaster command is cheap and does not require auth.
    db.command("ismaster")
    logger.debug("DB Server OK")
    db_available = True
except pymongo.errors.ConnectionFailure:
    logger.error("DB Server Not Available")

### MongoDB Collection Reference ###
# User
users_collection = db["users"]
# Admin
admins_collection = db["admins"]
# User Data
user_data_collection = db["user_data"]
# Records
records_collection = db["records"]
