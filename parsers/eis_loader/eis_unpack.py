# -*- coding: utf-8 -*-
"""
Распаковка ZIP и извлечение базовых полей из XML извещений (44-ФЗ).
Под разные XSD делаем «гибкие» XPath с fallback.
"""
from __future__ import annotations
from pathlib import Path
import zipfile, re
from lxml import etree
from typing import List

def _clean_num(s: str) -> float | None:
    if not s: return None
    t = re.sub(r"[^\d,\.]", "", s).replace(",", ".")
    try: return float(t)
    except: return None

def _text(el) -> str:
    return (el or "").strip()

def rows_from_zip(zip_path: str | Path) -> List[list]:
    rows: List[list] = []
    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if not name.lower().endswith((".xml", ".atom")):
                continue
            xml_data = z.read(name)
            root = etree.fromstring(xml_data)
            ns = root.nsmap

            def xp(expr: str) -> str:
                try:
                    return root.xpath(f"string({expr})", namespaces=ns).strip()
                except: return ""

            tender_id = xp("//ns2:notificationNumber | //notificationNumber | //commonInfo/purchaseNumber")
            subject   = xp("//ns2:purchaseObjectInfo | //purchaseObjectInfo | //lot/purchaseObjectInfo")
            customer  = xp("//ns2:customer/fullName | //customer/fullName | //lotCustomerInfo/fullName")
            price_raw = xp("//ns2:lot/ns2:maxContractPrice | //lot/maxContractPrice | //maxContractPrice")
            price_num = _clean_num(price_raw)
            deadline  = xp("//ns2:endDate | //endDate | //submissionCloseDateTime | //lotApplications/endDateTime")
            href      = xp("//ns2:href | //href")

            if any([tender_id, subject, customer, price_raw, deadline, href]):
                rows.append([tender_id, subject, customer, price_raw, price_num, deadline, href, name])
    return rows
