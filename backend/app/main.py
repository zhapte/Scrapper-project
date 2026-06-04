import os

from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.database import SessionLocal

from app.dependencies import get_db

from app.models import Product, User, Favorite
from app.routers.auth import get_current_user
from app.routers.auth import router as auth_router
from app.routers.scrape import router as scrape_router

import app.models


app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:5173",
    "http://127.0.0.1:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(scrape_router)

@app.get("/")
def home():
    return {"message": "server running"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/products")
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Product).all()

@app.get("/favorites")
def get_favorites(db: Session = Depends(get_db)):
    return db.query(Favorite).all()

@app.get("/scrape-list")
def scrape_list(db: Session = Depends(get_db)):
    return (
        db.query(Product)
        .join(Favorite, Product.product_id == Favorite.product_id)
        .filter(Favorite.notify_enabled == True)
        .distinct()
        .all()
    )

