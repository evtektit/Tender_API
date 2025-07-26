import importlib
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "sites_config.json")

def load_sites():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def run_all_parsers(query: str):
    results = []
    for site in load_sites():
        try:
            parser_module = importlib.import_module(f"parser.{site['parser']}")
            data = parser_module.search(query)
            results.append({
                "site": site["name"],
                "data": data
            })
        except Exception as e:
            results.append({
                "site": site["name"],
                "error": str(e)
            })
    return results
