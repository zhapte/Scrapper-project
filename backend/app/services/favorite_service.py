from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Favorite, Product

def add_favorite(
    db: Session,
    user_id: UUID,
    product_id: UUID,
    target_price: Decimal,
) -> Favorite:
    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if product is None:
        raise ValueError("Product not found")

    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.product_id == product_id
    ).first()

    if existing_favorite is not None:
        return existing_favorite

    favorite = Favorite(
        user_id=user_id,
        product_id=product_id,
        target_price=target_price
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return favorite