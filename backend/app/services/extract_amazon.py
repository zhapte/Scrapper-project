from bs4 import BeautifulSoup
from decimal import Decimal
from urllib.parse import urlparse
import re

def extract_amazon_product_info(product_html:str, product_url:str) -> dict:
    soup = BeautifulSoup(product_html, 'html.parser')

    asin = extract_asin(product_url)
    title_tag = soup.select_one("#productTitle")
    meta_title = soup.select_one('meta[name="title"]')
    meta_description = soup.select_one('meta[name="description"]')

    price_tag = soup.select_one(".a-price .a-offscreen")

    name = None
    if title_tag:
        name = title_tag.get_text(strip=True)
    elif meta_title:
        name = meta_title.get("content")

    description = None
    if meta_description:
        description = meta_description.get("content")

    price = None
    if price_tag:
        price_text = price_tag.get_text(strip=True)
        price = clean_price(price_text)

    return {
        "amazon_asin": asin,
        "name": name,
        "description": description,
        "current_price": price,
        "product_url": product_url,
    }



def extract_asin(url: str) -> str | None:
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    if match:
        return match.group(1)
    return None


def clean_price(price_text: str) -> Decimal | None:
    match = re.search(r"[\d,.]+", price_text)
    if not match:
        return None

    cleaned = match.group(0).replace(",", "")
    return Decimal(cleaned)