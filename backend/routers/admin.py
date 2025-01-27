from typing import Any

from fastapi import APIRouter

router = APIRouter()

# todo: admin resource must be a structure with permission for moderators with a single root admin


@router.get("/")
def read_admin_details() -> Any:
    pass


@router.put("/")
def update_admin_details() -> Any:
    pass


@router.post("/auth/login")
def login_admin() -> Any:
    pass


@router.post("/auth/logout")
def logout_admin_details() -> Any:
    pass
