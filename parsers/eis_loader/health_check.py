from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"})

if __name__ == "__main__":
    uvicorn.run("health_check:app", host="0.0.0.0", port=8013)
