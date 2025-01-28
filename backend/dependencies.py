from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidTokenError)
from sqlmodel import Session

from .models import get_session
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


def get_current_user_from_access(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Get the current user payload from the access token.

    Args:
        token (str): The access token, injected via dependency.

    Raises:
        HTTPException: If the token is invalid or belongs to an admin.

    Returns:
        dict: The decoded payload of the token.
    """
    payload = validate_token(token, TokenType.ACCESS)
    if "is_admin" in payload and payload["is_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a user")
    return payload


def get_current_admin_from_access(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Get the current admin payload from the access token.

    Args:
        token (str): The access token, injected via dependency.

    Raises:
        HTTPException: If the token is invalid or not for an admin.

    Returns:
        dict: The decoded payload of the token.
    """
    payload = validate_token(token, TokenType.ACCESS)
    if "is_admin" not in payload or not payload["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin"
        )
    return payload


def get_current_user_from_refresh(
    refresh_token: str = Depends(get_refresh_token_from_cookie),
) -> dict:
    """
    Get the current user from the refresh token.

    Args:
        refresh_token (str): The refresh token, injected via dependency.

    Raises:
        HTTPException: If the token is invalid or belongs to an admin.

    Returns:
        dict: The decoded payload of the refresh token.
    """
    payload = validate_token(refresh_token, TokenType.REFRESH)
    if "is_admin" in payload and payload["is_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a user")
    return payload


def get_current_admin_from_refresh(
    refresh_token: str = Depends(get_refresh_token_from_cookie),
) -> dict:
    """
    Get the current user from the refresh token.

    Args:
        refresh_token (str): The refresh token, injected via dependency.

    Raises:
        HTTPException: If the token is invalid or not for an admin.

    Returns:
        dict: The decoded payload of the refresh token.
    """
    payload = validate_token(refresh_token, TokenType.REFRESH)
    if "is_admin" not in payload or not payload["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin"
        )
    return payload


UserAccessDep = Annotated[dict, Depends(get_current_user_from_access)]
AdminAccessDep = Annotated[dict, Depends(get_current_admin_from_access)]

UserRefreshDep = Annotated[dict, Depends(get_current_user_from_refresh)]
AdminRefreshDep = Annotated[dict, Depends(get_current_admin_from_refresh)]


LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
