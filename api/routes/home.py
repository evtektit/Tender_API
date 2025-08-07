from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

from ai_worker.openai_client import ask_gpt  # 🔌 Обработчик запроса к ИИ

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("api", "templates"))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("main_template_ui.html", {
        "request": request
    })

@router.post("/", response_class=HTMLResponse)
async def ask(request: Request, prompt: str = Form(...)):
    response = ask_gpt(prompt)  # 🧠 Получаем ответ от ИИ
    return templates.TemplateResponse("main_template_ui.html", {
        "request": request,
        "ai_answer": response  # 👈 Это ты можешь вставить в шаблон
    })
