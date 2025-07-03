from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
from parser.zakupki_parser import search_tenders
from app.utils import format_tender_result
from fastapi.responses import JSONResponse
from app.telegram_bot import run_bot
app = FastAPI()

@app.get("/")
def root():
    return {"message": "TenderBot AI is running!"}

@app.get("/search-tenders-telegram", response_class=PlainTextResponse)
def get_tenders_telegram(keyword: str = Query(...), page: int = 1):
    tenders = search_tenders(keyword, page)
    if not tenders:
        return "❌ Ничего не найдено."

    formatted = "\n\n".join([format_tender_result(t) for t in tenders])
    return formatted[:4000]  # Ограничение Telegram

@app.get("/test-parser", response_class=JSONResponse)
def test_parser(keyword: str = "бумага", page: int = 1):
    results = search_tenders(keyword, page)
    return {"results": results}

if __name__ == "__main__":
    run_bot()