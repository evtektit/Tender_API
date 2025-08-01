from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ai_worker.openai_client import ask_gpt

router = APIRouter()

class GPTRequest(BaseModel):
    prompt: str

@router.api_route("/ai/ask", methods=["GET", "POST"])
async def ask_gpt_api(request: Request):
    if request.method == "GET":
        prompt = request.query_params.get("prompt")
        if not prompt:
            return JSONResponse(content={"error": "Отсутствует параметр ?prompt="}, status_code=422)
        reply = ask_gpt(prompt)
        return JSONResponse(content={"response": reply})

    try:
        body = await request.json()
        prompt = body.get("prompt")
        if not prompt:
            return JSONResponse(content={"error": "В теле запроса должен быть prompt"}, status_code=422)
        reply = ask_gpt(prompt)
        return JSONResponse(content={"response": reply})
    except Exception as e:
        return JSONResponse(content={"response": f"❌ Ошибка разбора запроса: {e}"}, status_code=400)
