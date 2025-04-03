from datetime import timedelta
from jose import jwt

from common.config import get_app_settings
from common.datetime import get_utc_now

ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expires = get_utc_now() + expires_delta
    to_encode.update({"exp": expires})
    settings = get_app_settings()
    return jwt.encode(to_encode, settings.jwt_auth_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    settings = get_app_settings()
    return jwt.decode(token, settings.jwt_auth_secret, algorithms=[ALGORITHM])
