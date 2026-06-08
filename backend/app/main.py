import os

from fastapi import FastAPI
from fastapi import Depends
from fastapi import Security
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.dependencies import get_db
from app.models import Product
from app.models import User
from app.routers.auth import get_current_user
from app.routers.auth import router as auth_router

import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "server running"}


@app.post("/seed-products")
def seed_products(
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user),
):
    products = [
        Product(
            name="AirPods Pro",
            url="https://example.com/airpods"
        ),
        Product(
            name="Nintendo Switch",
            url="https://example.com/switch"
        ),
        Product(
            name="Gaming Monitor",
            url="https://example.com/monitor"
        )
    ]

    db.add_all(products)
    db.commit()

    return {
        "message": "Dummy products added",
        "count": len(products)
    }


@app.get("/products")
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user),
):
    return db.query(Product).all()
