from importlib import import_module
from inspect import signature, isclass, isfunction
from ai_worker.logger import get_logger

logger = get_logger("parser")

# реальные модули по твоей структуре
SOURCE_MAP = {
    "rts": "parser.agregators.rts_parser",
    "sber": "parser.agregators.sber_parser",
    "zakazrf": "parser.agregators.zakupki_parser",
    "agregatoreat": "parser.agregators.agregatoreat_parser",
}

CANDIDATE_METHODS = ["search", "run", "parse", "start", "main"]

def _call_with_best_kwargs(func, query: str, limit: int):
    """Аккуратно подставляем только те kwargs, которые функция принимает."""
    try:
        sig = signature(func)
        kwargs = {}
        names = {p.name for p in sig.parameters.values()}
        # возможные имена для query/limit
        for name in ["query", "q", "text", "kw", "keyword", "term"]:
            if name in names:
                kwargs[name] = query
                break
        for name in ["limit", "n", "count", "topk", "max_items"]:
            if name in names:
                kwargs[name] = limit
                break
        return func(**kwargs) if kwargs else func(query)
    except TypeError:
        # крайний случай — попробуем позиционно
        try:
            return func(query, limit)
        except Exception:
            return func(query)

def _run_module(module_name: str, query: str, limit: int):
    mod = import_module(module_name)

    # 1) Ищем подходящий класс с методом из списка
    for attr_name in dir(mod):
        attr = getattr(mod, attr_name)
        if isclass(attr) and attr.__module__ == mod.__name__:
            inst = None
            for m in CANDIDATE_METHODS:
                if hasattr(attr, m):
                    inst = inst or attr()
                    return getattr(inst, m)(query=query, limit=limit) \
                        if "query" in signature(getattr(inst, m)).parameters \
                        else _call_with_best_kwargs(getattr(inst, m), query, limit)

    # 2) Ищем свободные функции
    for m in CANDIDATE_METHODS:
        f = getattr(mod, m, None)
        if f and isfunction(f):
            return _call_with_best_kwargs(f, query, limit)

    raise RuntimeError("Не нашли подходящий класс/функцию в модуле")

def _normalize_item(src: str, item):
    # приводим к общим полям; если словарь — мягко добиваем поля
    if isinstance(item, dict):
        item.setdefault("source", src)
        return item
    return {"source": src, "data": item}

def run_all(query: str, sources: list[str], limit: int = 20):
    logger.info(f"run_all: query='{query}', sources={sources}, limit={limit}")
    results, errors = [], {}
    for src in sources:
        module_name = SOURCE_MAP.get(src)
        if not module_name:
            errors[src] = "Источник не сконфигурирован"
            continue
        try:
            res = _run_module(module_name, query, limit)
            if isinstance(res, list):
                results.extend(_normalize_item(src, r) for r in res)
                logger.info(f"{src}: ok, +{len(res)} items")
            elif res:
                results.append(_normalize_item(src, res))
                logger.info(f"{src}: ok, +1 item")
        except Exception as e:
            msg = str(e)
            errors[src] = msg
            logger.error(f"{src}: error: {msg}")
    return {"count": len(results), "results": results, "errors": errors}
