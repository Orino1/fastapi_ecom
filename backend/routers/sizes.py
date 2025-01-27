from typing import Any

from fastapi import APIRouter

router = APIRouter()

# sizes


@router.get("/")
def read_sizes() -> Any:
    pass


# passing the category_id in teh body
@router.post("/")
def create_size() -> Any:
    pass


@router.get("/{size_id}")
def read_size(size_id: int) -> Any:
    pass


@router.put("/{size_id}")
def update_size(size_id: int) -> Any:
    pass


@router.delete("/{size_id}")
def delete_size(size_id: int) -> Any:
    pass


# size measurements


@router.get("/{size_id}/measuremenets")
def read_size_measuremenets(size_id: int) -> Any:
    pass


@router.put("/{size_id}/measuremenets")
def update_size_measuremenets(size_id: int) -> Any:
    pass


@router.delete("/{size_id}/measuremenets")
def delete_size_measuremenets(size_id: int) -> Any:
    pass
