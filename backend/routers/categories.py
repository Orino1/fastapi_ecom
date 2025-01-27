from typing import Any

from fastapi import APIRouter

from ..models.categories import Category, SubCategory

router = APIRouter()

# main categories


@router.get("/")
def read_main_categories() -> Any:
    pass


@router.post("/")
def create_category() -> Any:
    pass


@router.get("/{category_id}")
def read_main_category(category_id: int) -> Any:
    pass


@router.put("/{category_id}")
def update_main_category(category_id: int) -> Any:
    pass


@router.delete("/{category_id}")
def delete_main_category(category_id: int) -> Any:
    pass


# sub categories


@router.get("/{category_id}/subcategories")
def read_subcategories(category_id: int) -> Any:
    pass


@router.post("/{category_id}/subcategories")
def create_subcategory(category_id: int) -> Any:
    pass


@router.get("/{category_id}/subcategories/{subcategory_id}")
def read_subcategory(category_id: int, subcategory_id: int) -> Any:
    pass


@router.put("/{category_id}/subcategories/{subcategory_id}")
def update_subcategory(category_id: int, subcategory_id: int) -> Any:
    pass


@router.delete("/{category_id}/subcategories/{subcategory_id}")
def delete_subcategory(category_id: int, subcategory_id: int) -> Any:
    pass
