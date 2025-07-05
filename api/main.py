from fastapi import FastAPI
from routes import home, parser_route
app = FastAPI()
app.include_router(home.router)
app.include_router(parser_route.router)