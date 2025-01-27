from typing import Any

from fastapi import APIRouter

from ..dependencies import SessionDep
from ..models.users import User, UserCreate, UserOutput
from ..utils import pwd_context

router = APIRouter()


# todo: blacklist for tokens


@router.get("/")
def read_users() -> Any:
    pass


@router.post("/")
def create_user(user_data: UserCreate, session: SessionDep) -> UserOutput:
    # we need to create a user here
    hashed_password = pwd_context.hash(user_data.password)

    new_user = User(**user_data.model_dump(), hashed_password=hashed_password)

    session.add(new_user)
    session.commit()

    session.refresh(new_user)

    return new_user


@router.get("/me")
def read_current_user() -> Any:
    pass


@router.put("/me")
def update_current_user() -> Any:
    pass


@router.delete("/me")
def delete_current_user() -> Any:
    pass


@router.delete("/{user_id}")
def delete_user(user_id: int) -> Any:
    pass


@router.post("/auth/login")
def login_user():
    pass


@router.post("/auth/logout")
def logout_user() -> Any:
    pass
