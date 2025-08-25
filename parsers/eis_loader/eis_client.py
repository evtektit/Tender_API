import os
import requests
from pathlib import Path
from typing import Optional, Dict, Any, Iterable
from parsers.eis_loader import logger
from datetime import datetime
import uuid
import xmltodict
import time
from common.logger import get_logger

logger = get_logger(__name__)
logger.info("eis_loader started!")

DEFAULT_URL = "https://int44.zakupki.gov.ru/eis-integration/services/getDocsIP"

class EISClient:
    def __init__(
        self,
        token: Optional[str] = None,
        base_url: str = DEFAULT_URL,
        out_dir: str | Path = None,
        timeout: int = 90,
        retries: int = 3,
        sleep_between: float = 2.0,
    ):
        self.token = token or os.getenv("EIS_TOKEN") or os.getenv("INDIVIDUAL_PERSON_TOKEN")
        if not self.token:
            raise RuntimeError("Не найден токен. Укажи EIS_TOKEN в .env или передай в конструктор.")

        self.base_url = base_url

        # 📂 out всегда лежит в папке eis_loader
        default_out = Path(__file__).resolve().parent / "out"
        self.out_dir = Path(out_dir) if out_dir else default_out
        self.out_dir.mkdir(parents=True, exist_ok=True)

        self.timeout = timeout
        self.retries = retries
        self.sleep_between = sleep_between

        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "text/xml; charset=utf-8"})

    # ---------- публичные методы ----------

    def get_archive_by_region_date(
        self,
        *,
        region_code: str,
        date_iso: str,   # YYYY-MM-DDTHH:MM:SS
        document_type44: str = "epNotificationEF2020",
        subsystem_type: str = "PRIZ",   # PRIZ/POZ/...
        prefix: str = "eis",
    ) -> Path:
        """Делает SOAP-запрос -> получает archiveUrl -> скачивает ZIP."""

        logger.info(
            "▶️ Запрос архива: region=%s, date=%s, docType=%s, subsystem=%s",
            region_code, date_iso, document_type44, subsystem_type
        )

        envelope = self._build_envelope_region_date(
            region_code=region_code,
            document_type44=document_type44,
            date_iso=date_iso,
            subsystem_type=subsystem_type,
        )

        data = self._post_soap(envelope)
        archive_url = self._extract_archive_url(data)

        zip_name = f"{prefix}_{region_code}_{document_type44}_{date_iso}.zip"
        zip_path = self.out_dir / zip_name

        self._download_zip(archive_url, zip_path)
        return zip_path

    def iter_dates(self, start: str, end: str) -> Iterable[str]:
        """Генератор дат в ISO (включительно)."""
        d0 = datetime.date.fromisoformat(start)
        d1 = datetime.date.fromisoformat(end)
        cur = d0
        while cur <= d1:
            yield cur.isoformat()
            cur += datetime.timedelta(days=1)

    # ---------- внутренние методы ----------

    def _build_envelope_region_date(
        self, *, region_code: str, document_type44: str, date_iso: str, subsystem_type: str
    ) -> str:
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://zakupki.gov.ru/fz44/get-docs-ip/ws">
  <soapenv:Header><individualPerson_token>{self.token}</individualPerson_token></soapenv:Header>
  <soapenv:Body>
    <ws:getDocsByOrgRegionRequest>
      <index>
        <id>{uuid.uuid4()}</id>
        <createDateTime>{now}</createDateTime>
        <mode>PROD</mode>
      </index>
      <selectionParams>
        <orgRegion>{region_code}</orgRegion>
        <subsystemType>{subsystem_type}</subsystemType>
        <documentType44>{document_type44}</documentType44>
        <periodInfo><exactDate>{date_iso}</exactDate></periodInfo>
      </selectionParams>
    </ws:getDocsByOrgRegionRequest>
  </soapenv:Body>
</soapenv:Envelope>"""
        logger.debug("📄 SOAP request:\n%s", xml)
        return xml

    def _post_soap(self, envelope: str) -> Dict[str, Any]:
        last_err = None
        for i in range(1, self.retries + 1):
            try:
                logger.debug("📡 SOAP POST attempt %s/%s", i, self.retries)
                resp = self.session.post(self.base_url, data=envelope.encode("utf-8"), timeout=self.timeout)
                resp.raise_for_status()
                return xmltodict.parse(resp.content)
            except Exception as e:
                last_err = e
                logger.warning("⚠️ Ошибка SOAP-запроса (попытка %s/%s): %s", i, self.retries, e)
                time.sleep(self.sleep_between * i)
        raise RuntimeError(f"SOAP запрос не удался после {self.retries} попыток: {last_err}")

    @staticmethod
    def _extract_archive_url(doc):
        body = doc.get("soap:Envelope", {}).get("soap:Body", {})

        # Ошибка от ЕИС
        fault = body.get("soap:Fault") or body.get("Fault")
        if fault:
            detail = fault.get("faultstring") or fault
            raise RuntimeError(f"SOAP Fault от ЕИС: {detail}")

        # Ответ с archiveUrl
        for key in body.keys():
            if key.endswith("getDocsByOrgRegionResponse") or key.endswith("getDocsByDateResponse"):
                data_info = body[key].get("dataInfo", {})
                url = data_info.get("archiveUrl")
                if not url:
                    logger.debug("📥 SOAP response:\n%s", json.dumps(doc, ensure_ascii=False, indent=2))
                    raise RuntimeError("Пустой результат: документов по фильтру нет (archiveUrl отсутствует).")
                return url

        # Непонятная структура
        logger.debug("📥 SOAP response (unexpected):\n%s", json.dumps(doc, ensure_ascii=False, indent=2))
        raise RuntimeError("Неожиданная структура SOAP-ответа")

    def _download_zip(self, url: str, path: Path):
        logger.info("⬇️ Скачиваем архив: %s", url)
        resp = self.session.get(url, headers={"individualPerson_token": self.token}, timeout=self.timeout)
        resp.raise_for_status()
        with open(path, "wb") as f:
            f.write(resp.content)
        logger.info("✅ Архив сохранён: %s", path)
