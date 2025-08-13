from playwright.sync_api import sync_playwright
import pandas as pd
import json

def save_to_csv(data, filename="rts_tenders.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"✅ Сохранено в CSV: {filename}")

def save_to_excel(data, filename="rts_tenders.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"✅ Сохранено в Excel: {filename}")

def run_rts_parser(query: str = "", limit: int = 12):
    result_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Слушаем все ответы
        def handle_response(response):
            if "search" in response.url and response.status == 200:
                try:
                    data = response.json()
                    tenders = data.get("data", {}).get("Items", [])
                    for tender in tenders:
                        result_data.append({
                            "Номер закупки": tender.get("PurchaseNumber"),
                            "Название": tender.get("PurchaseName"),
                            "Цена": tender.get("Price"),
                            "Дата окончания": tender.get("EndDate"),
                            "Ссылка": "https://www.rts-tender.ru" + tender.get("Url", "")
                        })
                except Exception as e:
                    print("Ошибка разбора JSON:", e)

        page.on("response", handle_response)

        # Загружаем страницу и ждём XHR
        page.goto(f"https://www.rts-tender.ru/poisk?SearchString={query}")
        page.wait_for_timeout(5000)



        browser.close()

    return result_data

if __name__ == "__main__":
    data = run_rts_parser()

    if data:
        save_to_csv(data)
        save_to_excel(data)
    else:
        print("❌ Не удалось получить данные.")