from fastapi import APIRouter

from app.request_modesl import ScrapeRequest
from app.services.amazon_scraper import scrape_amazon
from app.services.extract_amazon import extract_amazon_product_info

router = APIRouter()

@router.post("/scrape")
async def scrape(request: ScrapeRequest):
    html = await scrape_amazon(request.url)
    product_info = extract_amazon_product_info(html, request.url)
    return {
        "url" : request.url,
        "product_info": product_info
    }