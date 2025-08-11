# parser/run_parsers.py
import asyncio

async def _maybe_run(mod_name, func_name="run"):
    try:
        mod = __import__(f"parser.{mod_name}", fromlist=[func_name])
        fn = getattr(mod, func_name)
        print(f"[RUN] {mod_name}.{func_name}()")
        res = fn()
        if asyncio.iscoroutine(res):
            await res
    except Exception as e:
        print(f"[WARN] {mod_name}: {e}")

async def main():
    # перечисли свои парсеры; оставь только реально существующие модули
    for m in ["zakupki_parser", "rts_tender", "sber_ast", "agregatoreat"]:
        await _maybe_run(m)

if __name__ == "__main__":
    asyncio.run(main())
