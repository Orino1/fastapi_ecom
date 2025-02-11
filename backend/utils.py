import os
from datetime import datetime, timedelta
from enum import Enum

import jwt
from passlib.context import CryptContext

from .models.admin import Admin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


KEY: str = os.getenv("JWT_SECRET_KEY")
ACCESS_EXPIRE: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_EXPIRE: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM: str = os.getenv("JWT_ALGORITHM")


class TokenType(Enum):
    """Enumeration for token types"""

    ACCESS: str = "access"
    REFRESH: str = "refresh"


def create_access_token(data: str, is_admin: bool = False) -> str:
    """
    Create an access token.

    Args:
        data (dict): The data to be encoded in the token.
        is_admin (bool): Flag for indecating if the user is an admin.

    Returns:
        str: The generated access token.
    """
    to_encode = {"sub": data}
    expire_in = datetime.now() + timedelta(minutes=ACCESS_EXPIRE)

    to_encode.update({"exp": expire_in, "is_admin": is_admin})
    access_token = jwt.encode(to_encode, KEY, ALGORITHM)

    return access_token


def create_refresh_token(data: str, is_admin: bool = False) -> str:
    """
    Create a refresh token.

    Args:
        data (dict): The data to be encoded in the token.
        is_admin (bool): Flag for indecating if the user is an admin.

    Returns:
        str: The generated refresh token.
    """
    to_encode = {"sub": data}
    expire_in = datetime.now() + timedelta(days=REFRESH_EXPIRE)

    to_encode.update({"exp": expire_in, "is_admin": is_admin})
    refresh_token = jwt.encode(to_encode, KEY + "refresh", ALGORITHM)

    return refresh_token


def check_admin_permissions(admin: Admin, permission: str):
    for admin_role in admin.roles:
        for role_perm in admin_role.role.permissions:
            if role_perm.permission.name == permission:
                return True

    return False
