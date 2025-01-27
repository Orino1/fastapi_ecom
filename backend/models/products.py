from sqlmodel import Field, Relationship, SQLModel

from .categories import SubCategory

# product


class ProductBase(SQLModel):
    name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    model_height: float | None = Field(default=None, ge=0)
    model_height_unit: str | None = Field(default=None, min_length=1)
    garment_size: int | None = Field(default=None, foreign_key="size.id")
    online_exclusive: bool = Field(default=True)


class Product(ProductBase, table=True):
    id: int = Field(default=None, primary_key=True)
    public_id: str = Field(..., min_length=3, index=True)
    subcategory_id: int = Field(..., foreign_key="subcategory.id")

    subcategory: SubCategory = Relationship(back_populates="products")
    variants: list["ProductVariant"] = Relationship(back_populates="product")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=3)
    description: str | None = Field(default=None, min_length=3)
    model_height: float | None = Field(default=None, ge=0)
    model_height_unit: str | None = Field(default=None, min_length=1)
    garment_size: int | None = Field(default=None, foreign_key="size.id")
    online_exclusive: bool | None = Field(default=None)


class ProductOutput(ProductBase):
    public_id: str
    variants: list["ProductVariantOutput"]


# variants
class ProductVariantBase(SQLModel):
    color_id: int = Field(..., foreign_key="variantcolor.id")
    price: float = Field(..., ge=0)
    discount: float | None = Field(default=None, ge=0, le=100)


class ProductVariant(ProductVariantBase, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(..., foreign_key="product.id")
    thumbnail_id: int = Field(..., foreign_key="thumbnail.id")

    product: Product = Relationship(back_populates="variants")
    color: "VariantColor" = Relationship(back_populates="variants")
    sizes: list["VariantSize"] = Relationship(back_populates="variant")
    thumbnail: "VariantThumbnail" = Relationship(back_populates="variant")
    gallery: list["VariantGallery"] = Relationship(back_populates="variant")


class ProductVariantOutput(SQLModel):
    id: int
    price: float
    discount: float | None
    sizes: list["VariantSizeOutput"]
    color: "VariantColorOutput"
    # thumbnail_url: str
    # gallery: list["VariantGalleryOutput"]


# variant sizes


class VariantSizeBase(SQLModel):
    size_id: int = Field(..., foreign_key="size.id")
    stock: int = Field(..., ge=0)


class VariantSize(VariantSizeBase, table=True):
    id: int = Field(default=None, primary_key=True)
    variant_id: int = Field(..., foreign_key="productvariant.id")

    variant: ProductVariant = Relationship(back_populates="sizes")
    size: "Size" = Relationship(back_populates="variant_sizes")


class VariantSizeCreate(VariantSizeBase):
    pass


class VariantSizeUpdate(SQLModel):
    size_id: int | None = None
    stock: int | None = Field(default=None, ge=0)


class VariantSizeOutput(SQLModel):
    id: int
    size_name: str
    stock: int


# variant thumbnail/gallery


class VariantThumbnailBase(SQLModel):
    image_url: str = Field(..., min_length=1)


class VariantThumbnail(VariantThumbnailBase, table=True):
    id: int = Field(default=None, primary_key=True)
    variant_id: int = Field(..., foreign_key="productvariant.id")
    variant: "ProductVariant" = Relationship(back_populates="thumbnail")


class VariantGalleryBase(SQLModel):
    image_url: str = Field(..., min_length=1)


class VariantGallery(VariantGalleryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    variant_id: int = Field(..., foreign_key="productvariant.id")
    variant: "ProductVariant" = Relationship(back_populates="gallery")


# variant colors


class VariantColorCreate(SQLModel):
    name: str = Field(..., min_length=1, max_length=100, unique=True)
    hex_value: str = Field(..., min_length=7, max_length=7, unique=True)


class VariantColor(VariantColorCreate, table=True):
    id: int = Field(default=None, primary_key=True)


class VariantColorOutput(SQLModel):
    id: int
    name: str
    hex_value: str


class VariantColorUpdate(SQLModel):
    name: str = Field(default=None, min_length=1, max_length=100, unique=True)
    hex_value: str = Field(default=None, min_length=7, max_length=7, unique=True)

from .sizes import Size
