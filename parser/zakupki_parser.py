from playwright.async_api import async_playwright
from ai_worker.logger import get_logger

logger = get_logger(__name__)

async def search_tenders(query: str) -> list:
    logger.info(f"🔍 Поиск тендеров по: {query}")
    url = f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={query}"

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=20000)
            await page.wait_for_timeout(4000)

            tenders = []
            blocks = await page.locator(".search-registry-entry-block").all()

            for block in blocks[:5]:
                try:
                    title = await block.locator(".registry-entry__header-mid__text").inner_text()
                    price = await block.locator(".price-block__value").inner_text()
                    tenders.append(f"📝 {title.strip()} — 💰 {price.strip()}")
                except:
                    continue

            await browser.close()
            return tenders or ["ℹ️ Данные не извлечены."]

    except Exception as e:
        logger.exception("💥 Ошибка при парсинге Playwright")
        return [f"❌ Ошибка Playwright: {str(e)}"]
