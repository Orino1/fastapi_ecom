from sqlmodel import Field, SQLModel


class AdminBase(SQLModel):
    username: str = Field(min_length=1, max_length=50, unique=True)


class Admin(AdminBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(min_length=1)


class AdminInput(AdminBase):
    password: str = Field(min_length=8, max_length=16)


class AdminOutput(AdminBase):
    id: int
