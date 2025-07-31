from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api.routes import parser_route, ai
from ai_worker.openai_client import ask_gpt
from parser.zakupki_parser import search_tenders
import os
import traceback
app = FastAPI(debug=True)

from logger import get_logger
logger = get_logger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI стартовал")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 FastAPI завершил работу")

templates = Jinja2Templates(directory=os.path.join("api", "templates"))

# Статика (если понадобится позже)
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Подключаем маршруты
app.include_router(parser_route.router)
app.include_router(ai.router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, q: str = None):
    try:
        parse_results = None
        if q:
            parse_results = search_tenders(q)
        return templates.TemplateResponse("main_template_ui.html", {
            "request": request,
            "parse_results": parse_results
        })
    except Exception as e:
        print("💥 Ошибка в index:", e)
        traceback.print_exc()
        return HTMLResponse("❌ Ошибка при отображении страницы", status_code=500)

@app.post("/", response_class=HTMLResponse)
async def ask_ai(request: Request, prompt: str = Form(...)):
    try:
        ai_result = ask_gpt(prompt)
        return templates.TemplateResponse("main_template_ui.html", {
            "request": request,
            "ai_result": ai_result
        })
    except Exception as e:
        print("💥 Ошибка в ask_ai:", e)
        traceback.print_exc()
        return HTMLResponse("❌ Ошибка при работе с AI", status_code=500)