from sqlmodel import Field, Relationship, SQLModel

# category


class CategoryBase(SQLModel):
    name: str = Field(..., min_length=1, unique=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: str | None = None


class Category(CategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)

    subcategories: list["SubCategory"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete"}, back_populates="category"
    )


# sub category


class SubCategoryBase(SQLModel):
    name: str = Field(..., min_length=1, unique=True)


class SubCategoryCreate(SubCategoryBase):
    pass


class SubCategoryUpdate(SubCategoryBase):
    name: str | None = Field(default=None, min_length=1)


class SubCategory(SubCategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    category_id: int = Field(..., foreign_key="category.id")

    category: Category = Relationship(back_populates="subcategories")
    sizes: list["Size"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete"}, back_populates="subcategory"
    )
    products: list["Product"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}, back_populates="subcategory"
    )


from .products import Product
# imported here to avoid a circular import problem
from .sizes import Size
