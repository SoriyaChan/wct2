from fastapi import FastAPI
from .routers import supplier, user, product
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(supplier.router)
app.include_router(product.router)