import requests
import os
from database import get_chat_history

OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/chat')
OLLAMA_API_MODEL = os.getenv('OLLAMA_API_MODEL', 'llama3.1:latest')

#* Ollama API request function
def ollama_request(user_id, message):
    url = OLLAMA_API_URL
    headers = {"Content-Type": "application/json"}
    history = get_chat_history(user_id)
    history.append({"role": "user", "content": message})
    data = {
        "model": OLLAMA_API_MODEL,
        "messages": history,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()