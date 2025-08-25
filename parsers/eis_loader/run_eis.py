from dotenv import load_dotenv
from parsers.eis_loader.eis_client import EISClient
from common.logger import get_logger

logger = get_logger("eis_loader", "eis_client.log")

# Загружаем .env
load_dotenv()

if __name__ == "__main__":
    client = EISClient()

    region_code = "16"
    date_iso = "2025-08-19"

    try:
        zip_path = client.get_archive_by_region_date(
            region_code=region_code,
            date_iso=date_iso
        )
        logger.info("🎉 Готово, архив: %s", zip_path)
    except Exception as e:
        logger.error("❌ Ошибка: %s", e)
