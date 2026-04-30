from fastapi import FastAPI

from app.api import categories, orders, products, profiles, users

app = FastAPI(title="Lab1 FastAPI")

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(profiles.router)
app.include_router(orders.router)
