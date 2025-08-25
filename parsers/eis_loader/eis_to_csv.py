# -*- coding: utf-8 -*-
"""
Сохранение строк в CSV (UTF-8-BOM; разделитель ; для Excel).
"""
from __future__ import annotations
from pathlib import Path
import csv
from typing import Iterable

HEADERS = ["tender_id","subject","customer","price_raw","price_num","deadline","link","source_file"]

def write_csv(rows: Iterable[list], dst: str | Path) -> Path:
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(HEADERS)
        for r in rows:
            w.writerow(r)
    return dst
