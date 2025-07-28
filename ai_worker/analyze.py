from ai_worker.openai_client import ask_gpt

def analyze_text(text: str) -> str:
    # 🔍 можно сюда встроить препроцессинг текста
    return ask_gpt(text)
