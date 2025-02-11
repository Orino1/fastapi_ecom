from typing import Any

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from ..dependencies import (LoginFormDep, RawAdminAccessDep, RawUserRefreshDep,
                            SessionDep, UserAccessDep, UserRefreshDep)
from ..models.users import (LoginResponse, User, UserCreate, UserOutput,
                            UserUpdate)
from ..utils import create_access_token, create_refresh_token, pwd_context

router = APIRouter()


@router.get("/", response_model=list[UserOutput], dependencies=[RawAdminAccessDep])
def read_users(session: SessionDep) -> list[UserOutput]:
    """Retrieves all users"""
    users = session.exec(select(User)).all()
    return users


@router.post("/", response_model=UserOutput)
def create_user(user_data: UserCreate, session: SessionDep) -> UserOutput:
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(**user_data.model_dump(), hashed_password=hashed_password)
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except IntegrityError as e:
        session.rollback()
        # loggin error here
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is already registered"
        )
    return new_user


@router.get("/me", response_model=UserOutput)
def read_current_user(user: UserAccessDep) -> UserOutput:
    return user


@router.put("/me", response_model=UserOutput)
def update_current_user(
    user_new_data: UserUpdate, user: UserAccessDep, session: SessionDep
) -> Any:
    update_data = user_new_data.model_dump(exclude_unset=True)

    if update_data.get("password"):
        hashed_password = pwd_context.hash(update_data["password"])
        update_data.update({"hashed_password": hashed_password})

        update_data.pop("password")

    for key, val in update_data.items():
        setattr(user, key, val)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/me")
def delete_current_user(user: UserAccessDep, session: SessionDep) -> Any:
    session.delete(user)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{user_id}", dependencies=[RawAdminAccessDep])
def delete_user(user_id: int, session: SessionDep) -> Any:
    # we need the actual user by id
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {user_id} not found.",
        )

    session.delete(user)
    session.commit()

    return {"detail": "User deleted successfully."}


@router.post("/auth/login", response_model=LoginResponse)
def login_user(response: Response, login_data: LoginFormDep, session: SessionDep):
    email = login_data.username
    password = login_data.password

    user = session.exec(select(User).filter_by(email=email)).first()

    if (
        not user
        or not pwd_context.verify(password, user.hashed_password)
        or user.disabled
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Check email or password"
        )

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    response.set_cookie(key="refresh_token", value=refresh_token)
    return {"user": user, "access_token": access_token}


@router.post("/auth/logout", dependencies=[RawUserRefreshDep])
def logout_user(response: Response) -> Any:
    response.delete_cookie(key="refresh_token")
    # access token would be removed from teh frontend by the frontend
    return {"detail": "Successfully logged out"}


@router.get("/auth/refresh", response_model=LoginResponse)
def refresh_user_access_token(user: UserRefreshDep):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Account disabled"
        )
    access_token = create_access_token(str(user.id))
    return {"user": user, "access_token": access_token}
