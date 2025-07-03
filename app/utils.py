def format_tender_result(tender: dict) -> str:
    number = tender.get('number', 'Без номера')
    name = tender.get('name', 'Без наименования')
    price = tender.get('price', 'Цена не указана')
    end_date = tender.get('end_date', 'Дата не указана')
    link = tender.get('link', 'Нет ссылки')

    return (
        f"📌 {number}\n"
        f"📝 {name}\n"
        f"💰 {price}\n"
        f"🗓️ Окончание подачи заявок: {end_date}\n"
        f"🔗 [Ссылка]({link})"
    )
