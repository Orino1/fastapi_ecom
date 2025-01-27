from sqlmodel import Field, Relationship, SQLModel

from .categories import SubCategory

# todo: make size name unique and a many to many subcategory_size

# Size


class SizeBase(SQLModel):
    name: str = Field(..., min_length=1, max_length=100)


class Size(SizeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    subcategory_id: int = Field(..., foreign_key="subcategory.id")

    subcategory: SubCategory = Relationship(back_populates="sizes")
    measurements: list["SizeMeasurements"] | None = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}, back_populates="size"
    )
    variant_sizes: list["VariantSize"] = Relationship(back_populates="size")


from .products import VariantSize


class SizeCreate(SizeBase):
    subcategory_id: int


class SizeUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)


# Size measurements


class SizeMeasurementsBase(SQLModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    unit: str = Field(..., max_length=10)
    value: float = Field(..., ge=0)


class SizeMeasurements(SizeMeasurementsBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    size_id: int = Field(..., foreign_key="size.id")

    size: Size = Relationship(back_populates="measurements")


class SizeMeasurementsCreate(SizeMeasurementsBase):
    size_id: int = Field(..., foreign_key="size.id")


class SizeMeasurementsUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    unit: str | None = Field(default=None, max_length=10)
    value: float | None = Field(default=None, ge=0)


class SizeMeasurementsOutput(SQLModel):
    id: int
    name: str
    description: str | None
    unit: str
    value: float
