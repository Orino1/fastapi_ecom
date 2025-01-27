from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# user base model
class UserBase(SQLModel):
    firstname: str = Field(..., min_length=1, max_length=50)
    lastname: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., unique=True)


# user model in the db
class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    disabled: bool | None = False


# user input create ( schema we get from the request )
class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(min_length=1, max_length=16)


# user input update ( schema we get from the request )
class UserUpdate(SQLModel):
    firstname: str | None = Field(None, min_length=1, max_length=50)
    lastname: str | None = Field(None, min_length=1, max_length=50)
    password: str | None = Field(default=None, min_length=8, max_length=16)


# user output
class UserOutput(UserBase):
    id: int
