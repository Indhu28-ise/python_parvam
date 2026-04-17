# Chat bot 

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Initialize client
client = genai.Client(api_key=API_KEY)

# Model name (Gemma)
MODEL_NAME = "models/gemma-3-4b-it"

# System prompt
SYSTEM_PROMPT = """You are a helpful, friendly, and concise AI assistant.
Keep answers clear and under 200 words unless needed."""

# Chat history
history = []

# Initialize conversation
history.append(types.Content(
    role="user",
    parts=[types.Part.from_text(text=f"System: {SYSTEM_PROMPT}")]
))

history.append(types.Content(
    role="model",
    parts=[types.Part.from_text(text="Understood. I will follow instructions.")]
))


def chat(user_input: str) -> str:
    global history

    # Add user message
    history.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_input)]
    ))

    try:
        # Generate response
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=history,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=300
            )
        )

        reply = response.text if response.text else "⚠️ No response received."

    except Exception as e:
        return f"❌ Error: {str(e)}"

    # Add bot reply to history
    history.append(types.Content(
        role="model",
        parts=[types.Part.from_text(text=reply)]
    ))

    return reply


def main():
    print("=" * 50)
    print("🤖 Gemini AI Chatbot (Gemma Model)")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot: 👋 Goodbye!")
            break

        reply = chat(user_input)
        print(f"Bot: {reply}")


if __name__ == "__main__":
    main()
