from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND
from . import database, models, schemas, crud, utils, auth
from fastapi_jwt_auth import AuthJWT

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index(request: Request, db: Session = Depends(get_db), search: str = "", skip: int = 0, limit: int = 10):
    items = crud.get_items(db, skip=skip, limit=limit, search=search)
    return templates.TemplateResponse("index.html", {"request": request, "items": items, "search": search})

@app.post("/add")
def add(name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    item = schemas.ItemCreate(name=name, description=description)
    crud.create_item(db, item)
    return RedirectResponse("/", status_code=HTTP_302_FOUND)

@app.get("/export")
def export(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return utils.export_to_excel(items)