from typing import Any

from fastapi import APIRouter

router = APIRouter()


# product


@router.get("/")
def read_products() -> Any:
    pass


# passing teh actual subcategory_id in the request body
@router.post("/")
def create_product() -> Any:
    pass


@router.get("/{product_id}")
def read_product(product_id: int) -> Any:
    pass


@router.put("/{product_id}")
def update_product(product_id: int) -> Any:
    pass


@router.delete("/{product_id}")
def delete_product(product_id: int) -> Any:
    pass


# product variants


@router.get("/{product_id}/variants")
def read_product_variants(product_id: int) -> Any:
    pass


@router.post("/{product_id}/variants")
def create_product_variants(product_id: int) -> Any:
    pass


@router.get("/{product_id}/variants/{product_variant_id}")
def read_product_variant(product_id: int, product_variant_id: int) -> Any:
    pass


@router.put("/{product_id}/variants/{product_variant_id}")
def update_product_variants(product_id: int, product_variant_id: int) -> Any:
    pass


@router.delete("/{product_id}/variants/{product_variant_id}")
def delete_product_variant(product_id: int, product_variant_id: int) -> Any:
    pass
