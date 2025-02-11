import os
from urllib.parse import quote

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from ..models.users import User
from ..utils import pwd_context

load_dotenv()

DB_USERNAME = os.getenv("TEST_DB_USERNAME")
DB_PASSWORD = quote(os.getenv("TEST_DB_PASSWORD").encode())
DB_HOST = os.getenv("TEST_DB_HOST")
DB_PORT = os.getenv("TEST_DB_PORT")
DB_NAME = os.getenv("TEST_DB_NAME")


DB_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)


def get_session():
    with Session(engine) as session:
        yield session


def create_tables():
    SQLModel.metadata.create_all(bind=engine)


def drop_tables():
    SQLModel.metadata.drop_all(bind=engine)


def insert_users():
    session = next(get_session())

    users = [
        User(
            firstname="Alice",
            lastname="Doe",
            email="alice@example.com",
            hashed_password=pwd_context.hash("password123"),
        ),
        User(
            firstname="Bob",
            lastname="Smith",
            email="bob@example.com",
            disabled=1,
            hashed_password=pwd_context.hash("password123"),
        ),
        User(
            firstname="Charlie",
            lastname="Brown",
            email="charlie@example.com",
            hashed_password=pwd_context.hash("password123"),
        ),
    ]

    session.add_all(users)
    session.commit()
