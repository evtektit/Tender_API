from importlib import import_module

SOURCE_MAP = {
    "rts": "parser.etps.rts_tender:RTSTender",
    "sber": "parser.etps.sber_ast:SberAST",
    "zakazrf": "parser.etps.zakazrf:ZakazRF",
    "agregatoreat": "parser.etps.agregatoreat:AgregatorEAT",
}

def run_all(query: str, sources: list[str], limit: int = 20):
    results, errors = [], {}
    for src in sources:
        try:
            mod_name, cls_name = SOURCE_MAP[src].split(":")
            cls = getattr(import_module(mod_name), cls_name)
            parser = cls()
            if hasattr(parser, "search"):
                res = parser.search(query=query, limit=limit)
            elif hasattr(parser, "run"):
                res = parser.run(query=query, limit=limit)
            else:
                res = []
            if res:
                if isinstance(res, list):
                    for r in res:
                        if isinstance(r, dict):
                            r.setdefault("source", src)
                            results.append(r)
                        else:
                            results.append({"source": src, "data": r})
                else:
                    results.append({"source": src, "data": res})
        except Exception as e:
            errors[src] = str(e)
    return {"count": len(results), "results": results, "errors": errors}
