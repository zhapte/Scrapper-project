from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User
from app.services.favorite_service import add_favorite
from app.routers.auth import get_current_user

router = APIRouter()

class FavoriteRequest(BaseModel):
    product_id: UUID
    target_price: Decimal


@router.post("/favorites")
def create_favorite(
    request: FavoriteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        favorite = add_favorite(
            db=db,
            user_id=current_user.user_id,
            product_id=request.product_id,
            target_price=request.target_price
        )

        return {
            "message": "Product added to favorites",
            "favorite_id": favorite.favorite_id,
            "user_id": favorite.user_id,
            "product_id": favorite.product_id,
            "target_price": float(favorite.target_price),
            "notify_enabled": favorite.notify_enabled
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
