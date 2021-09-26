import datetime
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from puts.logger import logger

from .routes import auth, record

app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")

origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(record.router)


# print timezone and current time
print()
logger.info(f"Environ 'TZ'    : {os.environ.get('TZ', 'N.A.')}")
logger.info(f"Current Time    : {datetime.datetime.now()}")
logger.info(f"Current UTC Time: {datetime.datetime.utcnow()}")
print()


@app.get("/api")
async def index():
    return {"Hello": "World!"}
