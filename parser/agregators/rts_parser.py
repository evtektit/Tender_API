from playwright.sync_api import sync_playwright

def run_rts_parser(query: str = "", limit: int = 10):
    result_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 👈 Важно: False = показывать окно браузера
        context = browser.new_context()
        page = context.new_page()

        # ⏳ Загружаем главную страницу — обязательно, чтобы пройти анти-DDoS
        page.goto("https://www.rts-tender.ru/poisk")
        page.wait_for_timeout(8000)  # подождать 8 секунд для прохождения проверки

        # 🔗 Прямой XHR-запрос после прохождения защиты
        search_url = (
            f"https://www.rts-tender.ru/api/auction/search?"
            f"SearchString={query}&pageIndex=1&pageSize={limit}"
        )

        def handle_response(response):
            if "auction/search" in response.url and response.status == 200:
                try:
                    data = response.json()
                    tenders = data.get("data", {}).get("Items", [])
                    for tender in tenders:
                        result_data.append({
                            "Название": tender.get("PurchaseName"),
                            "Цена": tender.get("Price"),
                            "Дата окончания": tender.get("EndDate"),
                            "Ссылка": "https://www.rts-tender.ru" + tender.get("Url", ""),
                        })
                except Exception as e:
                    print("❌ Ошибка разбора JSON:", e)

        page.on("response", handle_response)
        page.goto(search_url)
        page.wait_for_timeout(5000)  # ждём, пока ответ обработается

        browser.close()

    return result_data
