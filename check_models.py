
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load API key
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

api_key = os.getenv("GEMINI_API_KEY", "").strip()

if not api_key:
    raise ValueError("GEMINI_API_KEY missing in .env")

client = genai.Client(api_key=api_key)

try:
    print("\nAvailable Gemini models:\n")

    for model in client.models.list():
        name = model.name
        actions = getattr(
            model, "supported_actions", None
        )

        if actions is None or "generateContent" in actions:
            print(name)

except Exception as error:
    print("\nGEMINI API CONNECTION FAILED")
    print("ERROR TYPE:", type(error).__name__)
    print("FULL ERROR DETAILS:", str(error))
    raise SystemExit(1)

finally:
    if "client" in locals():
        client.close()