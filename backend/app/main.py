from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import Base
from app.database import engine
from app.database import SessionLocal

from app.models import Product, User, Favorite

import app.models


app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "server running"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
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