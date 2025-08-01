# api/routes/parser_route.py

from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from parser.zakupki_parser import search_tenders  # ✅ правильный импорт
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("api", "templates"))

@router.get("/parse")
async def parse_endpoint(request: Request, q: str = Query(...)):
    results = search_tenders(q)  # ✅ вызов внутри функции

    return templates.TemplateResponse("main_template_ui.html", {
        "request": request,
        "parse_results": results,
        "query": q
    })
