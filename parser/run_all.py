# parser/run_all.py
from typing import List, Dict, Any
import importlib, inspect
from fastapi.concurrency import run_in_threadpool
from ai_worker.logger import get_logger

logger = get_logger("parser.run_all")

SOURCE_MAP = {
    "rts": "parser.agregators.rts_parser",
    "sber": "parser.agregators.sber_parser",
    "zakazrf": "parser.agregators.zakupki_parser",
    "agregatoreat": "parser.agregators.agregatoreat_parser",
}

CANDIDATES = ("run_rts_parser", "search", "run", "parse", "start", "main")


async def _run_one(src: str, query: str, limit: int) -> List[Dict[str, Any]]:
    mod = importlib.import_module(SOURCE_MAP[src])
    fn = next((getattr(mod, name) for name in CANDIDATES if hasattr(mod, name)), None)
    if not fn:
        raise RuntimeError("Не нашли функцию парсинга (search/run/parse).")

    # подготовим kwargs с учётом фактической сигнатуры
    sig = inspect.signature(fn)
    kwargs = {"query": query, "limit": limit}
    if "logger" in sig.parameters:
        kwargs["logger"] = logger

    # поддержим и async, и sync
    if inspect.iscoroutinefunction(fn):
        part = await fn(**kwargs)
    else:
        part = await run_in_threadpool(lambda: fn(**kwargs))

    # нормализуем результат
    items: List[Dict[str, Any]] = []
    if isinstance(part, list):
        for x in part:
            items.append({"source": src, **(x if isinstance(x, dict) else {"data": x})})
    elif part:
        items.append({"source": src, **(part if isinstance(part, dict) else {"data": part})})

    logger.info(f"{src}: ok, +{len(items)} items")
    return items


async def run_all(query: str, sources: List[str], limit: int = 10) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    errors: Dict[str, str] = {}

    for src in sources:
        try:
            results.extend(await _run_one(src, query, limit))
        except Exception as e:
            errors[src] = str(e)
            logger.error(f"{src}: error: {e}")

    return {"count": len(results), "results": results, "errors": errors}
