from fastapi import FastAPI, Query, Request
from api.routes import ai
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from parser.zakupki_parser import search_tenders, extract_reg_number, get_signature_data
import os
from fastapi import Form
from fastapi.responses import RedirectResponse

app = FastAPI()
app.include_router(ai.router)
# 🔧 Инициализация Jinja2
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# ✅ JSON-версия
@app.get("/search-tenders")
def search_tenders_api(keyword: str = Query(...)):
    tenders = search_tenders(keyword)
    for tender in tenders:
        reg_number = extract_reg_number(tender["link"])
        if reg_number:
            sig_data = get_signature_data(reg_number)
            tender.update(sig_data)
    return JSONResponse(content=tenders)

# ✅ HTML-версия
@app.get("/html", response_class=HTMLResponse)
def search_html(request: Request, keyword: str = Query(...)):
    tenders = search_tenders(keyword)
    for tender in tenders:
        reg_number = extract_reg_number(tender["link"])
        if reg_number:
            sig_data = get_signature_data(reg_number)
            tender.update(sig_data)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "tenders": tenders,
        "keyword": keyword
    })
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
def handle_form(request: Request, keyword: str = Form(...)):
    return RedirectResponse(url=f"/html?keyword={keyword}", status_code=302)

# (если используешь запуск через Python)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
