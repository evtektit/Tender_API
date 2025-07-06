from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from parser.zakupki_parser import search_tenders

router = APIRouter()
import os
templates = Jinja2Templates(directory=os.path.join("api", "templates"))

@router.get("/parse")
async def parse_endpoint(request: Request, q: str = Query(...)):
    results = search_tenders(q)

    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(content={"results": results})

    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": results,
        "query": q
    })
