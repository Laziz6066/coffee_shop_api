# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.db import database
from app.db.database import engine, Base
from app.api.routes import auth, users


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Coffee Shop API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(auth.router)
app.include_router(users.router)
