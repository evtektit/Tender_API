from ai_worker.logger import get_logger

logger = get_logger(__name__)

def format_tender_result(tender: dict) -> str:
    logger.debug(f"📦 Форматируем тендер: {tender.get('number')}")
    return (
        f"📌 № {tender.get('number')}\n"
        f"🏢 Заказчик: {tender.get('customer')}\n"
        f"💵 Цена: {tender.get('price')}\n"
        f"🕒 Срок подачи: {tender.get('deadline')}\n"
        f"🔗 Ссылка: {tender.get('url')}\n"
    )
