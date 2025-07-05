from fastapi import APIRouter, Query
from parser.zakupki_parser import parse_data  # Импорт твоей функции
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/parse")
async def run_parser(q: str = Query(..., description="Ключевое слово или ИНН")):
    result = parse_data(q)
    return JSONResponse(content=result)
