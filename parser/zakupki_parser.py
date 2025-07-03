import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs

BASE_URL = "https://zakupki.gov.ru"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 📌 Поиск тендеров по ключевому слову
def search_tenders(keyword: str, page: int = 1):
    url = f"{BASE_URL}/epz/order/extendedsearch/results.html?pageNumber={page}&searchString={keyword}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка запроса страницы поиска: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    tender_blocks = soup.find_all("div", class_="search-registry-entry-block")

    for block in tender_blocks:
        number_tag = block.find("div", class_="registry-entry__header-mid__number")
        number = number_tag.text.strip() if number_tag else "Без номера"

        name_tag = block.find("div", class_="registry-entry__body-value")
        name = name_tag.text.strip() if name_tag else "Без наименования"

        price_tag = block.find("div", class_="price-block__value")
        price = price_tag.text.strip() if price_tag else "Цена не указана"

        date_tag = block.find("div", class_="data-block__value")
        end_date = date_tag.text.strip() if date_tag else "Дата не указана"

        link_tag = block.find("a", href=True)
        link = f"{BASE_URL}{link_tag['href']}" if link_tag else url

        results.append({
            "number": number,
            "name": name,
            "price": price,
            "end_date": end_date,
            "link": link
        })

    return results

# 📌 Достаёт номер закупки из URL
def extract_reg_number(link):
    parsed = urlparse(link)
    params = parse_qs(parsed.query)
    return params.get("regNumber", [None])[0]

# 📌 Парсит страницу подписи (ЭЦП)
def get_signature_data(reg_number):
    sig_url = f"{BASE_URL}/epz/order/notice/printForm/listModal.html?regNumber={reg_number}"

    try:
        resp = requests.get(sig_url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Ошибка загрузки подписи для {reg_number}: {e}")
        return {}

    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n")
    data = {"ФИО": "", "Организация": "", "Сертификат": "", "Период действия": "", "Подпись": ""}

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        if line.endswith("."):
            data["ФИО"] = line
        if "Организация:" in line:
            data["Организация"] = line.split("Организация:")[-1].strip()
        if "Сертификат:" in line:
            data["Сертификат"] = line.split("Сертификат:")[-1].strip()
        if "Период действия сертификата:" in line:
            data["Период действия"] = line.split("Период действия сертификата:")[-1].strip()

    textarea = soup.find('textarea')
    if textarea:
        data["Подпись"] = textarea.text.strip()

    return data

# 📌 Сохраняет список тендеров в CSV-файл
def save_to_csv(tenders, filename="tenders_with_signatures.csv"):
    with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Номер закупки", "Наименование", "Цена", "Дата окончания", "Ссылка",
            "ФИО подписанта", "Организация", "Сертификат", "Период действия", "Текст подписи"
        ])

        for tender in tenders:
            writer.writerow([
                tender.get("number", ""),
                tender.get("name", ""),
                tender.get("price", ""),
                tender.get("end_date", ""),
                tender.get("link", ""),
                tender.get("ФИО", ""),
                tender.get("Организация", ""),
                tender.get("Сертификат", ""),
                tender.get("Период действия", ""),
                tender.get("Подпись", "")
            ])

# 📌 Главная точка входа: поиск, подписи, сохранение
def parse_tenders_and_save(keyword, page=1, output_file="tenders_with_signatures.csv"):
    tenders = search_tenders(keyword, page)
    for tender in tenders:
        reg_number = extract_reg_number(tender["link"])
        if reg_number:
            sig_data = get_signature_data(reg_number)
            tender.update(sig_data)
    save_to_csv(tenders, output_file)
