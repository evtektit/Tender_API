from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from parser.main_parser import run_all_parsers  # ✅ заменили точку входа

router = APIRouter()
import os
templates = Jinja2Templates(directory=os.path.join("api", "templates"))

@router.get("/parse")
async def parse_endpoint(request: Request, q: str = Query(...)):
    results = run_all_parsers(q)  # 🔁 теперь работает через все сайты

    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(content={"results": results})

    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": results,
        "query": q
    })
