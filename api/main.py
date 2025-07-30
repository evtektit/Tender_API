from fastapi import FastAPI
from routes import home, parser_route, ai

app = FastAPI()

# Подключаем роуты
app.include_router(home.router)
app.include_router(parser_route.router)
app.include_router(ai.router)
