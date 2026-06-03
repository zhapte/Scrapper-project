from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import Base
from app.database import engine
from app.database import SessionLocal
from app.models import Product
from app.models import User

import app.models

Base.metadata.create_all(bind=engine)

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


@app.post("/seed-products")
def seed_products(db: Session = Depends(get_db)):
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
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()