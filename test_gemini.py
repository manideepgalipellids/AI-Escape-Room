
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env file from project directory
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

api_key = os.getenv("GEMINI_API_KEY", "").strip()
model_name = os.getenv(
    "GEMINI_MODEL", "gemini-2.5-flash-lite"
).strip()

print("=" * 50)
print("AI ESCAPE ROOM - GEMINI API TEST")
print("=" * 50)

print("API key loaded:", bool(api_key))
print("API key length:", len(api_key))
print("Selected model:", model_name)

if not api_key:
    raise ValueError("GEMINI_API_KEY missing in .env")

client = None

try:
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            api_version="v1beta"
        )
    )

    print("\nConnecting to Gemini API...")

    response = client.models.generate_content(
        model=model_name,
        contents="Say hello in one short sentence."
    )

    print("\nSUCCESS! GEMINI API CONNECTED")
    print("Gemini response:", response.text)

except Exception as error:
    print("\nGEMINI API CONNECTION FAILED")
    print("ERROR TYPE:", type(error).__name__)
    print("FULL ERROR DETAILS:")
    print(str(error))
    raise SystemExit(1)

finally:
    if client is not None:
        client.close()
