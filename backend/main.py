from fastapi import FastAPI

from . import lifespan
from .routers import admin, categories, products, sizes, users

app = FastAPI(lifespan=lifespan)


app.include_router(admin.router, prefix="/admin")
app.include_router(categories.router, prefix="/categories")
app.include_router(users.router, prefix="/users")
app.include_router(products.router, prefix="/products")
app.include_router(sizes.router, prefix="/sizes")


@app.get("/")
def read_root():
    return {"msg": "You found the root :)."}
