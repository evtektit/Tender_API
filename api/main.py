import sys
sys.path.append("/app")  # ⬅ Фикс для Docker
from fastapi import FastAPI, Request
from ai_worker.ai import ask_gpt  # ⬅ теперь всё ок
from ai_worker.ai import ask_gpt

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TenderBot AI is running!"}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    text = data.get("text", "")
    if not text:
        return {"response": "⚠️ Текст не передан"}
    result = ask_gpt(text)
    return {"response": result}  # ⬅ тут была ошибка!

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
