from fastapi import FastAPI
from routes import home, parser_route
app = FastAPI()
app.include_router(home.router)
app.include_router(parser_route.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
