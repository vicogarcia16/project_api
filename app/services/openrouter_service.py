import httpx
from app.core.exceptions import OpenRouterException
from app.core.config import get_settings

settings = get_settings()

OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY
MODEL = settings.OPENROUTER_MODEL

async def generate_task_description(title: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": settings.user_agent
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente que genera descripciones claras para tareas dadas."},
            {"role": "user", "content": f"Genera una descripción breve y útil para esta tarea: {title}"}
        ],
        "temperature": 0.7,
        "max_tokens": 200,
        "top_p": 0.9,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, headers=headers, json=body, timeout=10)

        if response.status_code != 200:
            raise OpenRouterException()

        content = response.json()
        return content["choices"][0]["message"]["content"].strip()

    except Exception:
        raise OpenRouterException()
