from playwright.async_api import async_playwright

async def scrape_amazon(url:str) -> str :
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={
                "width": 1920,
                "height": 1080
            }
        )

        page = await context.new_page()
        
        await page.goto(url)
        await page.wait_for_timeout(3000)
        await page.locator("button[type='submit']").click()
        await page.wait_for_timeout(3000)

        html = await page.content()

        await browser.close()

        return html