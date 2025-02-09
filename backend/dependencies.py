from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidTokenError)
from sqlmodel import Session

from .models import get_session
from .models.admin import Admin
from .models.users import User
from .utils import ALGORITHM, KEY, TokenType

"""
DATABASE dependencies
"""
SessionDep = Annotated[Session, Depends(get_session)]

"""
Authentication dependencies
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def validate_token(token: str, type: TokenType) -> dict:
    """
    Validate the signature of a token.

    Args:
        token (str): The token to be validated.
        type (TokenType enum): Enum type either access or refresh type.

    Raises:
        HTTPException: If token invalid, expired or unable to decode it.

    Returns:
        dict: The decoded payload from the token.
    """
    if type == TokenType.ACCESS:
        key: str = KEY
    elif type == TokenType.REFRESH:
        key: str = KEY + "refresh"
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unknown token type. check backend logic.",
        )

    try:
        payload = jwt.decode(token, key, ALGORITHM)
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not decode token"
        )


def get_refresh_token_from_cookie(request: Request) -> str:
    """
    Retrieve the refresh token from the cookies.

    Args:
        request (Request): The request object.

    Raises:
        HTTPException: If the refresh token is missing.

    Returns:
        str: The refresh token from the cookies.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing"
        )
    return refresh_token


def get_current_user_payload_from_access(token: str = Depends(oauth2_scheme)) -> int:
    """
    Get the current user payload from the access token.

    Args:
        token (str): The access token, injected via dependency.

    Raises:
        HTTPException: If the token is invalid or belongs to an admin.

    Returns:
        dict: Resource ID from the decoded payload of the token.
    """
    payload = validate_token(token, TokenType.ACCESS)
    if "is_admin" in payload and payload["is_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a user")
    return payload.sub


def get_current_admin_payload_from_access(token: str = Depends(oauth2_scheme)) -> int:
    """
    Get the current admin payload from the access token.

    Args:
        token (str): The access token, injected via dependency.

    Raises:
        HTTPException: If the token is invalid or not for an admin.

    Returns:
        dict: Resource ID from the decoded payload of the token.
    """
    payload = validate_token(token, TokenType.ACCESS)
    if "is_admin" not in payload or not payload["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin"
        )
    return payload.sub


def get_current_user_payload_from_refresh(
    refresh_token: str = Depends(get_refresh_token_from_cookie),
) -> int:
    """
    Get the current user from the refresh token.

    Args:
        refresh_token (str): The refresh token, injected via dependency.

    Raises:
        HTTPException: If the token is invalid or belongs to an admin.

    Returns:
        dict: Resource ID from the decoded payload of the refresh token.
    """
    payload = validate_token(refresh_token, TokenType.REFRESH)
    if "is_admin" in payload and payload["is_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a user")
    return payload.sub


def get_current_admin_payload_from_refresh(
    refresh_token: str = Depends(get_refresh_token_from_cookie),
) -> int:
    """
    Get the current user from the refresh token.

    Args:
        refresh_token (str): The refresh token, injected via dependency.

    Raises:
        HTTPException: If the token is invalid or not for an admin.

    Returns:
        int: Resource ID from the decoded payload of the refresh token.
    """
    payload = validate_token(refresh_token, TokenType.REFRESH)
    if "is_admin" not in payload or not payload["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin"
        )
    return payload.sub


# helper functions to retrives user/admin models
def get_user_model_from_access(
    session: SessionDep, user_id: int = Depends(get_current_user_payload_from_access)
) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def get_user_model_from_refresh(
    session: SessionDep, user_id: int = Depends(get_current_user_payload_from_refresh)
) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def get_admin_model_from_access(
    session: SessionDep, admin_id: int = Depends(get_current_admin_payload_from_access)
) -> User:
    admin = session.get(Admin, admin_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found"
        )
    return admin


def get_admin_model_from_refresh(
    session: SessionDep, admin_id: int = Depends(get_current_admin_payload_from_refresh)
) -> User:
    admin = session.get(Admin, admin_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found"
        )
    return admin


UserAccessDep = Annotated[User, Depends(get_user_model_from_access)]
AdminAccessDep = Annotated[Admin, Depends(get_admin_model_from_access)]

UserRefreshDep = Annotated[User, Depends(get_user_model_from_refresh)]
AdminRefreshDep = Annotated[Admin, Depends(get_admin_model_from_refresh)]

RawUserAccessDep = Depends(get_current_user_payload_from_access)
RawAdminAccessDep = Depends(get_current_admin_payload_from_access)

RawUserRefreshDep = Depends(get_current_user_payload_from_refresh)
RawAdminRefreshDep = Depends(get_current_admin_payload_from_refresh)


LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
