import os
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from puts.logger import logger


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # openssl rand -hex 32
    SECRET_KEY = os.environ.get("JWT_SECRET_KEY_PROD")
    if SECRET_KEY in (None, "None", "NA", "N.A.", ""):
        # A fallback value for development
        SECRET_KEY = "ae441da430f40de5b7c30d19243baaa7c2891e7e63a4bc44ad25e10edc408c54"
    ALGORITHM = "HS256"  # HS256 (HMAC with SHA-256)
    ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id: str) -> str:
        payload = {
            "exp": datetime.utcnow()
            + timedelta(days=0, minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
