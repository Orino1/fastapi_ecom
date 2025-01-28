import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import lifespan
from .routers import admin, categories, products, sizes, users

app = FastAPI(lifespan=lifespan)

cors_origins = os.getenv("CORS_ORIGINS").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, prefix="/admin")
app.include_router(categories.router, prefix="/categories")
app.include_router(users.router, prefix="/users")
app.include_router(products.router, prefix="/products")
app.include_router(sizes.router, prefix="/sizes")


@app.get("/")
def read_root():
    return {"msg": "You found the root :)."}
