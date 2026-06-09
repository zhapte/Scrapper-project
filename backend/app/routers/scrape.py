from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.request_modesl import ScrapeRequest
from app.services.amazon_scraper import scrape_amazon
from app.services.extract_amazon import extract_amazon_product_info
from app.services.product_service import save_product


router = APIRouter()

@router.post("/scrape")
async def scrape(
    request: ScrapeRequest,
    db: Session = Depends(get_db)
):
    html = await scrape_amazon(request.url)

    product_info = extract_amazon_product_info(html, request.url)
    asin = product_info.get("amazon_asin")
    name = product_info.get("name")
    price = product_info.get("current_price")

    missing_fields = [
        field
        for field, value in {
            "amazon_asin": asin,
            "name": name,
            "current_price": price,
        }.items()
        if value is None
    ]

    if missing_fields:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Could not extract required product fields from the Amazon page.",
                "missing_fields": missing_fields,
                "hint": "Make sure the URL is a product page and Amazon did not return a captcha or blocked page.",
            },
        )

    product = save_product(
        db=db,
        asin=asin,
        name=name,
        price=price,
        product_url=request.url,
        description=product_info.get("description")
    )

    return {
        "message": "Product scraped and saved",
        "url": request.url,
        "product": {
            "product_id": product.product_id,
            "asin": product.amazon_asin,
            "name": product.name,
            "current_price": float(product.current_price),
            "product_url": product.product_url,
            "last_scraped": product.last_scraped
        }
    }
