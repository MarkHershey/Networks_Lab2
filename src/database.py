import os

import pymongo
from puts.logger import logger

_DB_USER = os.environ.get("_DB_USER", "root")
_DB_PASS = os.environ.get("_DB_PASS", "example")
_DB_NAME = os.environ.get("_DB_NAME", "dev")


logger.info(
    f"""-----------------------------------
            MongoDB config:
            
            User: {_DB_USER}
            Database Name: {_DB_NAME}
         -----------------------------------
"""
)
DOMAIN = "localhost"
PORT = 27017

client = pymongo.MongoClient(
    host=[str(DOMAIN) + ":" + str(PORT)],
    serverSelectionTimeoutMS=3000,  # 3 second timeout
    username=_DB_USER,
    password=_DB_PASS,
)

db = client[f"{_DB_NAME}"]
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
