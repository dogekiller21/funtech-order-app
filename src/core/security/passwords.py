import base64
import hashlib

import bcrypt


def _prepare_password(password: str) -> bytes:
    """
    Хак, чтобы длина пароля не имела значения
    """
    return base64.b64encode(hashlib.sha256(password.encode()).digest())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(_prepare_password(password), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_prepare_password(password), hashed_password.encode())
