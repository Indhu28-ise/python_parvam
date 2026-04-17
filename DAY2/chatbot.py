import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def local_reply(user_input):
    text = user_input.lower().strip()

    if any(word in text for word in ["hi", "hello", "hey"]):
        return "Hello! How can I help you today?"
    if "name" in text:
        return "I am your simple Python chatbot."
    if any(word in text for word in ["bye", "exit", "quit"]):
        return "Goodbye!"
    if "how are you" in text:
        return "I'm doing well and ready to help."

    return f"You said: {user_input}"


def chatbot(user_input):
    if not API_KEY:
        return local_reply(user_input)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        return reply
    except requests.exceptions.RequestException as exc:
        return f"Request failed: {exc}"
    except (KeyError, IndexError, TypeError, ValueError):
        return "Received an unexpected response format from the API."


# Main loop
if __name__ == "__main__":
    print("Chatbot started (type 'exit' to stop)\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Chatbot stopped.")
            break
        
        reply = chatbot(user_input)
        print("Bot:", reply)
