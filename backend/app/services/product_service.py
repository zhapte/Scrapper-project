from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Product

def save_product(
    db: Session,
    asin: str,
    name: str,
    price: Decimal,
    product_url: str,
    description: str | None = None,
) -> Product:
    product = db.query(Product).filter(Product.amazon_asin == asin).first()

    if product is None:
        product = Product(
            amazon_asin=asin,
            name=name,
            description=description,
            current_price=price,
            product_url=product_url,
            last_scraped=datetime.now(timezone.utc)
        )
        db.add(product)

    else:
        product.name = name
        product.description = description
        product.current_price = price
        product.product_url = product_url
        product.last_scraped = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product)

    return product
